import hashlib, importlib.util, json, pathlib, subprocess, tempfile, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
MODULE=ROOT/'validate_package.py'

def load():
    assert MODULE.is_file(), 'package-local validator has not been implemented'
    spec=importlib.util.spec_from_file_location('validate_package', MODULE)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

def fixture(root):
    (root/'payload.txt').write_bytes(b'hello\n')
    doc={'files':[{'path':'payload.txt','sha256':hashlib.sha256(b'hello\n').hexdigest(),'bytes':6}]}
    (root/'PACKAGE_CONTENTS.json').write_text(json.dumps(doc))

class IntegrityTests(unittest.TestCase):
    def test_validator_exists(self):self.assertTrue(MODULE.exists(),'package-local validation is required')
    def test_valid_package(self):
        m=load()
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t);fixture(p);self.assertEqual(m.verify_files(p),1)
    def test_corruption_rejected(self):
        m=load()
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t);fixture(p);(p/'payload.txt').write_text('wrong')
            with self.assertRaises(ValueError):m.verify_files(p)
    def test_extra_rejected(self):
        m=load()
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t);fixture(p);(p/'extra.txt').write_text('wrong')
            with self.assertRaises(ValueError):m.verify_files(p)
    def test_traversal_rejected(self):
        m=load()
        for x in ('../escape','/escape','a/../escape','a//b','./a','a\\b'):
            with self.assertRaises(ValueError):m.safe_path(x)
    def test_symlink_rejected(self):
        m=load()
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t);fixture(p);(p/'payload.txt').unlink();(p/'payload.txt').symlink_to('/dev/null')
            with self.assertRaises(ValueError):m.verify_files(p)
    def test_duplicate_rejected(self):
        m=load()
        with tempfile.TemporaryDirectory() as t:
            p=pathlib.Path(t);fixture(p);d=json.loads((p/'PACKAGE_CONTENTS.json').read_text());d['files']*=2;(p/'PACKAGE_CONTENTS.json').write_text(json.dumps(d))
            with self.assertRaises(ValueError):m.verify_files(p)

if __name__=='__main__': unittest.main()
