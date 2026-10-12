import hashlib,importlib.util,json,pathlib,subprocess,tempfile,unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'package'/'apply_additive.py'

def module():
    assert SCRIPT.exists(), 'safe additive apply has not been implemented'
    spec=importlib.util.spec_from_file_location('apply_additive',SCRIPT);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def git(p,*args):return subprocess.check_output(['git','-C',str(p),*args],stderr=subprocess.DEVNULL,text=True).strip()

def repo(p):
    git(p,'init');git(p,'config','user.name','Fixture');git(p,'config','user.email','fixture@example.invalid')
    (p/'anchor').write_text('baseline\n');git(p,'add','anchor');git(p,'commit','-m','fixture')
    return {'commit':git(p,'rev-parse','HEAD'),'tree':git(p,'rev-parse','HEAD^{tree}'),'preimages':[{'path':'anchor','git_blob_sha1':git(p,'rev-parse','HEAD:anchor'),'sha256':hashlib.sha256(b'baseline\n').hexdigest(),'bytes':9}],'destination':'research/proposal'}

class ApplyTests(unittest.TestCase):
    def test_clean_baseline(self):
        m=module()
        with tempfile.TemporaryDirectory(dir=ROOT/'private') as t:
            p=pathlib.Path(t);pins=repo(p);self.assertEqual(m.check_repository(p,pins),p/'research/proposal')
    def test_wrong_commit(self):
        m=module()
        with tempfile.TemporaryDirectory(dir=ROOT/'private') as t:
            p=pathlib.Path(t);pins=repo(p);pins['commit']='0'*40
            with self.assertRaises(ValueError):m.check_repository(p,pins)
    def test_wrong_preimage(self):
        m=module()
        with tempfile.TemporaryDirectory(dir=ROOT/'private') as t:
            p=pathlib.Path(t);pins=repo(p);pins['preimages'][0]['git_blob_sha1']='0'*40
            with self.assertRaises(ValueError):m.check_repository(p,pins)
    def test_dirty(self):
        m=module()
        with tempfile.TemporaryDirectory(dir=ROOT/'private') as t:
            p=pathlib.Path(t);pins=repo(p);(p/'anchor').write_text('changed')
            with self.assertRaises(ValueError):m.check_repository(p,pins)
    def test_untracked(self):
        m=module()
        with tempfile.TemporaryDirectory(dir=ROOT/'private') as t:
            p=pathlib.Path(t);pins=repo(p);(p/'extra').write_text('new')
            with self.assertRaises(ValueError):m.check_repository(p,pins)
    def test_existing_destination(self):
        m=module()
        with tempfile.TemporaryDirectory(dir=ROOT/'private') as t:
            p=pathlib.Path(t);pins=repo(p);(p/'research/proposal').mkdir(parents=True)
            with self.assertRaises(ValueError):m.check_repository(p,pins)
    def test_assume_unchanged_drift(self):
        m=module()
        with tempfile.TemporaryDirectory(dir=ROOT/'private') as t:
            p=pathlib.Path(t);pins=repo(p);git(p,'update-index','--assume-unchanged','anchor');(p/'anchor').write_text('changed')
            self.assertEqual(git(p,'status','--porcelain'),'')
            with self.assertRaises(ValueError):m.check_repository(p,pins)
    def test_skip_worktree_drift(self):
        m=module()
        with tempfile.TemporaryDirectory(dir=ROOT/'private') as t:
            p=pathlib.Path(t);pins=repo(p);git(p,'update-index','--skip-worktree','anchor');(p/'anchor').write_text('changed')
            self.assertEqual(git(p,'status','--porcelain'),'')
            with self.assertRaises(ValueError):m.check_repository(p,pins)
    def test_index_flags_rejected_even_without_drift(self):
        m=module()
        with tempfile.TemporaryDirectory(dir=ROOT/'private') as t:
            p=pathlib.Path(t);pins=repo(p);git(p,'update-index','--skip-worktree','anchor')
            with self.assertRaises(ValueError):m.check_repository(p,pins)
    def test_copy_exclusive(self):
        m=module()
        with tempfile.TemporaryDirectory(dir=ROOT/'private') as t:
            p=pathlib.Path(t);s=p/'source';s.mkdir();(s/'x').write_bytes(b'bytes');d=p/'dest'
            m.copy_additive(s,d);self.assertEqual((d/'x').read_bytes(),b'bytes')
            with self.assertRaises(FileExistsError):m.copy_additive(s,d)

if __name__=='__main__':unittest.main()
