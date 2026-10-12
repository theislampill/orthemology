from pathlib import Path
import hashlib,json,tempfile,unittest
from verify_packet import verify,VerificationError


def h(b):return hashlib.sha256(b).hexdigest()

def manifest(root,extra=None):
    data={'format':'t20-synthesis-manifest-v1','files':[
        {'path':'data/a.txt','bytes':3,'sha256':h(b'abc')},
        {'path':'readme.md','bytes':6,'sha256':h(b'readme')}],
        'directories':['data','empty']}
    if extra:data=extra(data)
    b=(json.dumps(data,sort_keys=True,indent=2)+'\n').encode()
    (root/'MANIFEST.json').write_bytes(b)
    (root/'MANIFEST.sha256').write_text(h(b)+'  MANIFEST.json\n')


class VerifierTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'packet';self.root.mkdir()
        (self.root/'data').mkdir();(self.root/'empty').mkdir()
        (self.root/'data/a.txt').write_bytes(b'abc');(self.root/'readme.md').write_bytes(b'readme');manifest(self.root)
    def tearDown(self):self.tmp.cleanup()
    def rejects(self):
        with self.assertRaises(VerificationError):verify(self.root)
    def test_valid(self):self.assertEqual(verify(self.root)['files'],2)
    def test_changed(self):(self.root/'data/a.txt').write_bytes(b'abd');self.rejects()
    def test_missing(self):(self.root/'data/a.txt').unlink();self.rejects()
    def test_extra_file(self):(self.root/'extra').write_text('x');self.rejects()
    def test_extra_directory(self):(self.root/'extra').mkdir();self.rejects()
    def test_missing_empty_directory(self):(self.root/'empty').rmdir();self.rejects()
    def test_wrong_manifest_digest(self):(self.root/'MANIFEST.sha256').write_text('0'*64+'  MANIFEST.json\n');self.rejects()
    def test_duplicate_path(self):
        manifest(self.root,lambda d:{**d,'files':d['files']+[d['files'][0]]});self.rejects()
    def test_traversal(self):
        def change(d):d['files'][0]['path']='../escape';return d
        manifest(self.root,change);self.rejects()
    def test_absolute(self):
        def change(d):d['files'][0]['path']='/escape';return d
        manifest(self.root,change);self.rejects()
    def test_wrong_size(self):
        def change(d):d['files'][0]['bytes']=4;return d
        manifest(self.root,change);self.rejects()
    def test_wrong_file_digest(self):
        def change(d):d['files'][0]['sha256']='0'*64;return d
        manifest(self.root,change);self.rejects()
    def test_malformed_json(self):
        b=b'{broken';(self.root/'MANIFEST.json').write_bytes(b);(self.root/'MANIFEST.sha256').write_text(h(b)+'  MANIFEST.json\n');self.rejects()
    def test_symlink_file(self):
        (self.root/'data/a.txt').unlink();(self.root/'data/a.txt').symlink_to(self.root/'readme.md');self.rejects()
    def test_symlink_root(self):
        p=self.root.parent/'alias';p.symlink_to(self.root,target_is_directory=True)
        with self.assertRaises(VerificationError):verify(p)

if __name__=='__main__':unittest.main(verbosity=2)
