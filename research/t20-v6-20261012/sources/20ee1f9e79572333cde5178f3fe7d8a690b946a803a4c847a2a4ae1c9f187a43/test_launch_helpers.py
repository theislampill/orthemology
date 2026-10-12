"""Small real-subprocess regression tests for the private launch helpers."""
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile

TOOLS = Path(os.environ.get('LAUNCH_TOOLS', str(Path(__file__).resolve().parents[1] / 'tools')))

class LaunchTests(unittest.TestCase):
    def command(self, name, args, optimized=False):
        return subprocess.run([sys.executable, '-S', *(['-O'] if optimized else []), '-B', str(TOOLS / name), *args], capture_output=True, text=True, timeout=10)

    def check_input(self, data=b'yes', claimed=b'yes', missing=False, link=False):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); (root/'tools').mkdir(); (root/'inputs').mkdir()
            shutil.copyfile(TOOLS/'verify_inputs.py', root/'tools/verify_inputs.py')
            p=root/'inputs/test.txt'
            if link:
                (root/'other.txt').write_bytes(data); p.symlink_to(root/'other.txt')
            elif not missing: p.write_bytes(data)
            (root/'INPUTS.json').write_text(json.dumps({'inputs':[{'path':'inputs/test.txt','bytes':len(claimed),'sha256':hashlib.sha256(claimed).hexdigest()}]}),encoding='utf-8')
            return [subprocess.run([sys.executable,'-S',*(['-O'] if opt else []),'-B',str(root/'tools/verify_inputs.py')],capture_output=True,text=True,timeout=10).returncode for opt in (False,True)]

    def test_valid_input_normal_and_optimized(self): self.assertEqual(self.check_input(), [0,0])
    def test_bad_hash_rejected_normal_and_optimized(self): self.assertTrue(all(self.check_input(data=b'bad')))
    def test_bad_size_rejected_normal_and_optimized(self): self.assertTrue(all(self.check_input(data=b'longer')))
    def test_missing_input_rejected_normal_and_optimized(self): self.assertTrue(all(self.check_input(missing=True)))
    @unittest.skipUnless(hasattr(os,'symlink'), 'symlinks unavailable')
    def test_symlink_input_rejected(self): self.assertTrue(all(self.check_input(link=True)))

    def unpack(self, entries, mode=False, existing=False):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); archive=root/'input.zip'; dest=root/'output'
            if existing: dest.mkdir(); (dest/'keep.txt').write_bytes(b'keep')
            with zipfile.ZipFile(archive,'w') as z:
                for name, data, perms in entries:
                    info=zipfile.ZipInfo(name); info.create_system=3; info.external_attr=perms<<16
                    z.writestr(info,data)
            result=self.command('unpack_frozen.py',['--archive',str(archive),'--dest',str(dest)],mode)
            contents={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file() and p!=archive}
            modes={p.relative_to(dest).as_posix():stat.S_IMODE(p.stat().st_mode) for p in dest.rglob('*') if p.is_file()} if dest.exists() else {}
            return result.returncode, contents, modes

    def rejected(self, entries, existing=False):
        for opt in (False,True):
            with self.subTest(optimized=opt, names=[x[0] for x in entries]):
                code, files, _=self.unpack(entries,opt,existing)
                self.assertNotEqual(code,0)
                expected={'output/keep.txt':b'keep'} if existing else {}
                self.assertEqual(files,expected, 'Refusal must not leave extracted files or write outside destination')

    def test_valid_archive_and_modes(self):
        for opt in (False,True):
            code,files,modes=self.unpack([('pkg/run.sh',b'#!/bin/sh\n',stat.S_IFREG|0o755),('pkg/data.txt',b'yes',stat.S_IFREG|0o644)],opt)
            self.assertEqual(code,0); self.assertEqual(len(files),2)
            if os.name=='posix': self.assertEqual(modes['pkg/run.sh'],0o755)
    def test_parent_traversal_refused(self): self.rejected([('../escaped.txt',b'bad',stat.S_IFREG|0o644)])
    def test_windows_paths_refused(self):
        for name in ['C:/escape.txt',r'folder\escape.txt']:
            self.rejected([(name,b'bad',stat.S_IFREG|0o644)])
    def test_git_metadata_refused(self): self.rejected([('pkg/.git/config',b'bad',stat.S_IFREG|0o644)])
    def test_symlink_member_refused(self): self.rejected([('link',b'elsewhere',stat.S_IFLNK|0o777)])
    def test_case_collision_refused(self): self.rejected([('Data.txt',b'a',stat.S_IFREG|0o644),('data.txt',b'b',stat.S_IFREG|0o644)])
    def test_file_parent_collision_refused(self): self.rejected([('data',b'a',stat.S_IFREG|0o644),('data/child',b'b',stat.S_IFREG|0o644)])
    def test_existing_destination_refused(self): self.rejected([('new.txt',b'a',stat.S_IFREG|0o644)],existing=True)
    def test_all_names_checked_before_first_write(self): self.rejected([('good.txt',b'ok',stat.S_IFREG|0o644),('../bad.txt',b'bad',stat.S_IFREG|0o644)])
    def test_privileged_mode_refused(self): self.rejected([('run',b'bad',stat.S_IFREG|0o4755)])

if __name__=='__main__': unittest.main()
