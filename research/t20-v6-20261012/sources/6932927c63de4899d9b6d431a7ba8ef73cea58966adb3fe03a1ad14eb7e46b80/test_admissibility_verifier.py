#!/usr/bin/env python3
"""Bounded adversarial controls. Weakening exact inventory/path/hash checks breaks these tests."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile,unittest,zipfile
from pathlib import Path
PARSER=argparse.ArgumentParser(); PARSER.add_argument('verifier'); ARGS=PARSER.parse_args()
VERIFIER=Path(ARGS.verifier).resolve()
IDENTITY='T20_Hessian_Admissibility_Research_Checkpoint_20261009'
def sha(b): return hashlib.sha256(b).hexdigest()
def seal(root):
    rows=[{'path':p.relative_to(root).as_posix(),'bytes':len(p.read_bytes()),'sha256':sha(p.read_bytes())} for p in sorted(root.rglob('*')) if p.is_file() and p.name not in {'MANIFEST.json','MANIFEST.sha256'}]
    m={'checkpoint_id':IDENTITY,'status':'INTERMEDIATE_T20_ACTIVE','file_count':len(rows),'files':rows}
    (root/'MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
    (root/'MANIFEST.sha256').write_text(''.join(f'{sha(p.read_bytes())}  {p.relative_to(root).as_posix()}\n' for p in sorted(root.rglob('*')) if p.is_file() and p.name!='MANIFEST.sha256'))
class Checks(unittest.TestCase):
    def setUp(self):
        self.assertTrue(VERIFIER.is_file(),'Portable verifier implementation is not yet present.')
        self.temp=tempfile.TemporaryDirectory(prefix='hessian-verifier-test-'); self.base=Path(self.temp.name)
        self.root=self.base/IDENTITY; self.root.mkdir(); (self.root/'payload.txt').write_text('intact\n')
        (self.root/'BINDINGS.json').write_text('[]\n'); seal(self.root)
    def tearDown(self):
        if hasattr(self,'temp'):self.temp.cleanup()
    def run_tool(self,expected,extra=()):
        out=self.base/'receipt'; p=subprocess.run([sys.executable,str(VERIFIER),'--root',str(self.root),'--output',str(out),*extra],capture_output=True,text=True)
        self.assertEqual(p.returncode==0,expected,p.stdout+p.stderr)
        if not expected:self.assertFalse(out.exists(),'Failure must not create a success receipt.')
    def make_zip(self,mutate=None):
        path=self.base/'test.zip'
        with zipfile.ZipFile(path,'w') as z:
            for p in sorted(self.root.rglob('*')):
                if p.is_file():z.write(p,IDENTITY+'/'+p.relative_to(self.root).as_posix())
            if mutate:mutate(z)
        return path
    def test_01_valid_tree(self):self.run_tool(True)
    def test_02_tamper(self): (self.root/'payload.txt').write_text('changed\n'); self.run_tool(False)
    def test_03_missing(self):(self.root/'payload.txt').unlink(); self.run_tool(False)
    def test_04_extra_file(self):(self.root/'extra.txt').write_text('extra');self.run_tool(False)
    def test_05_extra_directory(self):(self.root/'extra').mkdir();self.run_tool(False)
    def test_06_symlink(self):(self.root/'link').symlink_to(self.root/'payload.txt');self.run_tool(False)
    def test_07_manifest_traversal(self):
        m=json.loads((self.root/'MANIFEST.json').read_text());m['files'][0]['path']='../escape';(self.root/'MANIFEST.json').write_text(json.dumps(m));self.run_tool(False)
    def test_08_duplicate_manifest_path(self):
        m=json.loads((self.root/'MANIFEST.json').read_text());m['files'].append(m['files'][0]);m['file_count']+=1;(self.root/'MANIFEST.json').write_text(json.dumps(m));self.run_tool(False)
    def test_09_duplicate_json_key(self):
        (self.root/'BINDINGS.json').write_text('{"x":1,"x":2}');seal(self.root);self.run_tool(False)
    def test_10_wrong_binding(self):
        (self.root/'BINDINGS.json').write_text(json.dumps([{'path':'payload.txt','sha256':'0'*64}]));seal(self.root);self.run_tool(False)
    def test_11_valid_zip(self):self.run_tool(True,['--archive',str(self.make_zip())])
    def test_12_zip_traversal(self):self.run_tool(False,['--archive',str(self.make_zip(lambda z:z.writestr('../escape.txt','bad')))])
    def test_13_zip_absolute(self):self.run_tool(False,['--archive',str(self.make_zip(lambda z:z.writestr('/escape.txt','bad')))])
    def test_14_zip_backslash(self):self.run_tool(False,['--archive',str(self.make_zip(lambda z:z.writestr(IDENTITY+'\\escape.txt','bad')))])
    def test_15_zip_duplicate(self):
        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter('ignore');p=self.make_zip(lambda z:z.writestr(IDENTITY+'/payload.txt','replacement'))
        self.run_tool(False,['--archive',str(p)])
    def test_16_zip_symlink(self):
        def add(z):
            info=zipfile.ZipInfo(IDENTITY+'/link');info.create_system=3;info.external_attr=(0o120777<<16);z.writestr(info,'payload.txt')
        self.run_tool(False,['--archive',str(self.make_zip(add))])
    def test_17_zip_extra(self):self.run_tool(False,['--archive',str(self.make_zip(lambda z:z.writestr(IDENTITY+'/extra.txt','bad')))])
    def test_18_wrong_archive_hash(self):self.run_tool(False,['--archive',str(self.make_zip()),'--archive-sha256','0'*64])
    def test_19_output_inside_package(self):
        p=subprocess.run([sys.executable,str(VERIFIER),'--root',str(self.root),'--output',str(self.root/'receipt')],capture_output=True,text=True);self.assertNotEqual(p.returncode,0);self.assertFalse((self.root/'receipt').exists())
    def test_20_refuse_existing_output(self):
        out=self.base/'existing';out.mkdir();(out/'keep').write_text('keep');p=subprocess.run([sys.executable,str(VERIFIER),'--root',str(self.root),'--output',str(out)],capture_output=True,text=True);self.assertNotEqual(p.returncode,0);self.assertEqual((out/'keep').read_text(),'keep')
if __name__=='__main__':unittest.main(argv=[sys.argv[0]],verbosity=2)
