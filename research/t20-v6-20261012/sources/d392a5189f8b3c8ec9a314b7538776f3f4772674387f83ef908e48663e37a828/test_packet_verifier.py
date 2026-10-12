import hashlib,json,tempfile,unittest,zipfile
from pathlib import Path
from verify_packet import verify_directory,verify_zip

class PacketVerifierTests(unittest.TestCase):
    def fixture(self,root):
        data=b'finite evidence\n';(root/'proof.txt').write_bytes(data)
        m={'schema':1,'files':{'proof.txt':{'sha256':hashlib.sha256(data).hexdigest(),'bytes':len(data)}}}
        (root/'MANIFEST.json').write_text(json.dumps(m))
        return m
    def test_pristine_directory(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);self.fixture(r);self.assertTrue(verify_directory(r)['ok'])
    def test_mutation_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);self.fixture(r);(r/'proof.txt').write_bytes(b'changed evidence\n')
            self.assertFalse(verify_directory(r)['ok'])
    def test_missing_member_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);self.fixture(r);(r/'proof.txt').unlink()
            self.assertFalse(verify_directory(r)['ok'])
    def test_unsealed_extra_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);self.fixture(r);(r/'unsealed.py').write_text('pass')
            self.assertFalse(verify_directory(r)['ok'])
    def test_parent_traversal_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t);m=self.fixture(r);m['files']['../escape']=m['files'].pop('proof.txt')
            (r/'MANIFEST.json').write_text(json.dumps(m));self.assertFalse(verify_directory(r)['ok'])
    def test_pristine_zip(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t)/'core';r.mkdir();self.fixture(r);zpath=Path(t)/'p.zip'
            with zipfile.ZipFile(zpath,'w') as z:
                for p in r.iterdir():z.write(p,'packet/'+p.name)
            self.assertTrue(verify_zip(zpath)['ok'])
    def test_duplicate_zip_member_rejected(self):
        with tempfile.TemporaryDirectory() as t:
            r=Path(t)/'core';r.mkdir();self.fixture(r);zpath=Path(t)/'p.zip'
            import warnings
            with warnings.catch_warnings():
                warnings.simplefilter('ignore')
                with zipfile.ZipFile(zpath,'w') as z:
                    for p in r.iterdir():z.write(p,'packet/'+p.name)
                    z.writestr('packet/proof.txt',b'other')
            self.assertFalse(verify_zip(zpath)['ok'])

if __name__=='__main__':unittest.main(verbosity=2)
