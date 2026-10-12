#!/usr/bin/env python3
"""Unit and subprocess tests for the read-only handoff verifier."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import warnings
import zipfile

import verify_packet as v


def h(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def seal(root: Path, **extra: object) -> dict:
    rows = [{'path': p.relative_to(root).as_posix(), 'bytes': p.stat().st_size,
             'sha256': h(p.read_bytes())} for p in sorted(root.rglob('*'))
            if p.is_file() and p.name not in {'MANIFEST.json', 'MANIFEST.sha256'}]
    m = {'schema': 'orthemology-continuity-packet-v1', 'file_count': len(rows),
         'files': rows, **extra}
    write_manifest(root, m)
    return m


def write_manifest(root: Path, m: dict) -> None:
    data = (json.dumps(m, indent=2) + '\n').encode()
    (root/'MANIFEST.json').write_bytes(data)
    (root/'MANIFEST.sha256').write_text(h(data)+'  MANIFEST.json\n')


class VerificationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)/'packet'
        self.root.mkdir()
        (self.root/'source.txt').write_text('retained original\n')
        self.manifest = seal(self.root)

    def test_valid_directory(self):
        self.assertEqual(v.verify(self.root)['status'], 'PASS')

    def test_changed_payload(self):
        (self.root/'source.txt').write_text('changed\n')
        with self.assertRaises(ValueError): v.verify(self.root)

    def test_missing_payload(self):
        (self.root/'source.txt').unlink()
        with self.assertRaises(ValueError): v.verify(self.root)

    def test_extra_payload(self):
        (self.root/'extra.txt').write_text('new')
        with self.assertRaises(ValueError): v.verify(self.root)

    def test_manifest_checksum(self):
        (self.root/'MANIFEST.json').write_text('{}\n')
        with self.assertRaises(ValueError): v.verify(self.root)

    def test_duplicate_manifest_path(self):
        m=dict(self.manifest);m['files']=m['files']*2;m['file_count']=2
        write_manifest(self.root,m)
        with self.assertRaises(ValueError): v.verify(self.root)

    def test_traversal_manifest_path(self):
        m=dict(self.manifest);m['files']=[dict(m['files'][0],path='../source.txt')]
        write_manifest(self.root,m)
        with self.assertRaises(ValueError): v.verify(self.root)

    def test_wrong_file_count(self):
        m=dict(self.manifest);m['file_count']=20;write_manifest(self.root,m)
        with self.assertRaises(ValueError): v.verify(self.root)

    def test_symlink_is_rejected(self):
        (self.root/'link').symlink_to(self.root/'source.txt')
        with self.assertRaises(ValueError): v.verify(self.root)

    def make_zip(self) -> Path:
        target=Path(self.tmp.name)/'packet.zip'
        with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
            for p in sorted(self.root.rglob('*')):
                if p.is_file(): z.write(p,'packet/'+p.relative_to(self.root).as_posix())
        return target

    def test_valid_zip(self):
        self.assertEqual(v.verify(self.make_zip())['status'],'PASS')

    def test_duplicate_zip_member(self):
        target=self.make_zip()
        with warnings.catch_warnings():
            warnings.simplefilter('ignore')
            with zipfile.ZipFile(target,'a') as z: z.writestr('packet/source.txt',b'again')
        with self.assertRaises(ValueError): v.verify(target)

    def test_zip_traversal(self):
        target=self.make_zip()
        with zipfile.ZipFile(target,'a') as z: z.writestr('packet/../outside.txt',b'bad')
        with self.assertRaises(ValueError): v.verify(target)

    def test_publication_tree_binding(self):
        d=self.root/'public';d.mkdir();(d/'a.txt').write_text('a')
        seal(self.root,publication={'prefix':'public','file_count':1,'git_tree':'0'*40})
        with self.assertRaises(ValueError): v.verify(self.root)

    def test_input_identity_binding(self):
        d=self.root/'inventory';d.mkdir()
        (d/'INPUT_IDENTITIES.json').write_text(json.dumps({'files':[{'path':'source.txt','bytes':18,'sha256':'0'*64}]}))
        seal(self.root)
        with self.assertRaises(ValueError): v.verify(self.root)

    def test_cli_normal_and_optimised_reject_tampering(self):
        script=Path(v.__file__).resolve()
        for flags in [[],['-O']]:
            with self.subTest(flags=flags):
                good=subprocess.run([sys.executable,*flags,'-B',str(script),str(self.root)],capture_output=True,text=True)
                self.assertEqual(good.returncode,0,good.stderr)
                self.assertEqual(json.loads(good.stdout)['status'],'PASS')
        (self.root/'source.txt').write_text('tampered')
        for flags in [[],['-O']]:
            with self.subTest(tampered_flags=flags):
                bad=subprocess.run([sys.executable,*flags,'-B',str(script),str(self.root)],capture_output=True,text=True)
                self.assertNotEqual(bad.returncode,0)
                self.assertIn('FAIL',bad.stderr)

if __name__=='__main__':unittest.main(verbosity=2)
