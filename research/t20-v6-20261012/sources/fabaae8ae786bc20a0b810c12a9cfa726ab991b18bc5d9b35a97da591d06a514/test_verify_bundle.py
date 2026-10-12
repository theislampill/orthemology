"""Boundary tests for the independent, data-free delivery verifier."""
import hashlib, importlib.util, io, json, os, stat, subprocess, sys, tempfile, unittest, zipfile
from pathlib import Path
SCRIPT = Path(__file__).resolve().parents[1] / 'verify_bundle.py'

class DeliveryVerifierTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='evidence verifier test ')
        self.root = Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()
    def make_zip(self, members):
        out = io.BytesIO()
        with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
            for name, data in members: z.writestr(name, data)
        return out.getvalue()
    def bundle(self, files=None, rows=None, extra=None, archives=None):
        files = files or {'README.md': b'read me\n'}
        rows = rows if rows is not None else [{'path':n,'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()} for n,d in files.items()]
        manifest = json.dumps({'format':1,'files':rows,'archives':archives or []}).encode()
        return self.make_zip([('Evidence/BUNDLE_MANIFEST.json',manifest)]+ [('Evidence/'+n,d) for n,d in files.items()]+(extra or []))
    def run_script(self, blob=None, args=()):
        if blob is not None:
            archive=self.root/'bundle.zip';archive.write_bytes(blob)
            args=['--archive',str(archive),'--expected-sha256',hashlib.sha256(blob).hexdigest(),*args]
        return subprocess.run([sys.executable,'-B',str(SCRIPT),*args],capture_output=True,text=True,cwd=self.root)
    def assert_rejected(self, blob, fragment, args=()):
        r=self.run_script(blob,args); self.assertNotEqual(r.returncode,0,r.stdout);self.assertIn(fragment,r.stderr)
    def test_verifier_exists(self): self.assertTrue(SCRIPT.is_file(), 'Verifier implementation is missing')
    def test_clean_bundle_and_spaced_fresh_extraction(self):
        out=self.root/'new extraction with spaces';r=self.run_script(self.bundle(),['--extract-to',str(out)])
        self.assertEqual(r.returncode,0,r.stderr);self.assertEqual((out/'Evidence/README.md').read_bytes(),b'read me\n')
        self.assertEqual(json.loads(r.stdout)['status'],'PASS_INTEGRITY_AND_SAFE_EXTRACTION_ONLY')
    def test_corrupt_expected_digest(self):
        p=self.root/'bundle.zip';p.write_bytes(self.bundle());r=self.run_script(args=['--archive',str(p),'--expected-sha256','0'*64]);self.assertNotEqual(r.returncode,0);self.assertIn('archive SHA-256',r.stderr)
    def test_archive_requires_external_digest(self):
        p=self.root/'bundle.zip';p.write_bytes(self.bundle());r=self.run_script(args=['--archive',str(p)]);self.assertNotEqual(r.returncode,0);self.assertIn('expected-sha256',r.stderr)
    def test_changed_payload(self): self.assert_rejected(self.bundle(rows=[{'path':'README.md','bytes':8,'sha256':'0'*64}]),'file digest')
    def test_unlisted_file(self): self.assert_rejected(self.bundle(extra=[('Evidence/extra.txt',b'x')]),'file census')
    def test_missing_file(self): self.assert_rejected(self.bundle(rows=[{'path':'missing.txt','bytes':1,'sha256':'0'*64}]),'file census')
    def test_traversal(self): self.assert_rejected(self.bundle(extra=[('Evidence/../escape',b'x')]),'unsafe archive path')
    def test_absolute_path(self): self.assert_rejected(self.bundle(extra=[('/escape',b'x')]),'unsafe archive path')
    def test_windows_path(self): self.assert_rejected(self.bundle(extra=[('C:/escape',b'x')]),'unsafe archive path')
    def test_backslash(self): self.assert_rejected(self.bundle(extra=[('Evidence\\escape',b'x')]),'unsafe archive path')
    def test_windows_device_name(self): self.assert_rejected(self.bundle(extra=[('Evidence/CON.txt',b'x')]),'unsafe archive path')
    def test_windows_trailing_dot(self): self.assert_rejected(self.bundle(extra=[('Evidence/name.',b'x')]),'unsafe archive path')
    def test_unicode_normalization_collision(self): self.assert_rejected(self.bundle(extra=[('Evidence/café.txt',b'x'),('Evidence/café.txt',b'y')]),'normalization collision')
    def test_duplicate_member(self):
        with __import__('warnings').catch_warnings():
            __import__('warnings').simplefilter('ignore');blob=self.bundle(extra=[('Evidence/README.md',b'x')])
        self.assert_rejected(blob,'duplicate')
    def test_case_collision(self): self.assert_rejected(self.bundle(extra=[('Evidence/readme.md',b'x')]),'case collision')
    def test_symlink_member(self):
        i=zipfile.ZipInfo('Evidence/link');i.create_system=3;i.external_attr=(stat.S_IFLNK|0o777)<<16
        self.assert_rejected(self.bundle(extra=[(i,b'elsewhere')]),'non-regular')
    def test_existing_extraction_refused(self):
        out=self.root/'existing';out.mkdir();(out/'sentinel').write_text('keep')
        self.assert_rejected(self.bundle(),'already exists',['--extract-to',str(out)]);self.assertEqual((out/'sentinel').read_text(),'keep')
    def test_symlink_parent_refused(self):
        real=self.root/'real';real.mkdir();link=self.root/'linked';link.symlink_to(real,target_is_directory=True)
        self.assert_rejected(self.bundle(),'symlink',['--extract-to',str(link/'fresh')]);self.assertFalse((real/'fresh').exists())
    def test_malformed_manifest_duplicate_rows(self):
        row={'path':'README.md','bytes':8,'sha256':hashlib.sha256(b'read me\n').hexdigest()}
        self.assert_rejected(self.bundle(rows=[row,row]),'duplicate manifest')
    def test_nested_archive_checked_before_writes(self):
        nested=self.make_zip([('../bad',b'x')]);out=self.root/'must not exist'
        blob=self.bundle(files={'source.zip':nested},archives=[{'path':'source.zip','extraction_id':'source','members':1,'uncompressed_bytes':1}])
        self.assert_rejected(blob,'unsafe archive path',['--extract-to',str(out)]);self.assertFalse(out.exists())
    def test_clean_nested_extraction(self):
        nested=self.make_zip([('Source/hello.txt',b'hello')]);out=self.root/'packages'
        blob=self.bundle(files={'source.zip':nested},archives=[{'path':'source.zip','extraction_id':'source','members':1,'uncompressed_bytes':5}])
        r=self.run_script(blob,['--extract-packages-to',str(out)]);self.assertEqual(r.returncode,0,r.stderr);self.assertEqual((out/'source/Source/hello.txt').read_bytes(),b'hello')
    def test_nested_count_mismatch(self):
        nested=self.make_zip([('Source/hello.txt',b'hello')]);self.assert_rejected(self.bundle(files={'source.zip':nested},archives=[{'path':'source.zip','extraction_id':'source','members':2,'uncompressed_bytes':5}]),'archive inventory')
    def test_directory_symlink_rejected(self):
        d=self.root/'directory';d.mkdir();(d/'README.md').symlink_to('/dev/null');(d/'BUNDLE_MANIFEST.json').write_text(json.dumps({'format':1,'files':[],'archives':[]}))
        r=self.run_script(args=['--directory',str(d)]);self.assertNotEqual(r.returncode,0);self.assertIn('symlink',r.stderr)
    def test_optimized_python_refused(self):
        r=subprocess.run([sys.executable,'-O',str(SCRIPT)],capture_output=True,text=True);self.assertNotEqual(r.returncode,0);self.assertIn('optimized',r.stderr)

if __name__=='__main__': unittest.main()
