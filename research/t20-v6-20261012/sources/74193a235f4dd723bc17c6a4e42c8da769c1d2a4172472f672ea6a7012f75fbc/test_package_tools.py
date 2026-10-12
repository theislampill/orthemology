"""Disposable negative controls for archive and manifest integrity."""
import unittest, tempfile, hashlib, json, zipfile
from pathlib import Path
import diagnostics as d

class PackageTests(unittest.TestCase):
    def tool(self,name):
        try: import package_tools
        except ImportError: self.fail('package_tools is not implemented')
        self.assertTrue(hasattr(package_tools,name));return getattr(package_tools,name)
    def tree(self,root):
        root.mkdir();(root/'a.txt').write_bytes(b'alpha')
        m={'schema':'t20-deep-dive-manifest-v1','files':[{'path':'a.txt','bytes':5,'sha256':hashlib.sha256(b'alpha').hexdigest()}]}
        b=(json.dumps(m,sort_keys=True,indent=2)+'\n').encode()
        (root/'MANIFEST.json').write_bytes(b);(root/'MANIFEST.sha256').write_text(hashlib.sha256(b).hexdigest()+'  MANIFEST.json\n')
    def test_accept_clean_tree(self):
        verify=self.tool('verify_tree')
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'p';self.tree(root);self.assertEqual(verify(root)['payload_files'],1)
    def test_changed_bytes_fail(self):
        verify=self.tool('verify_tree')
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'p';self.tree(root);(root/'a.txt').write_bytes(b'bravo')
            with self.assertRaises(ValueError):verify(root)
    def test_extra_member_fails(self):
        verify=self.tool('verify_tree')
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'p';self.tree(root);(root/'extra').write_bytes(b'x')
            with self.assertRaises(ValueError):verify(root)
    def test_missing_member_fails(self):
        verify=self.tool('verify_tree')
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'p';self.tree(root);(root/'a.txt').unlink()
            with self.assertRaises(ValueError):verify(root)
    def test_manifest_tamper_fails(self):
        verify=self.tool('verify_tree')
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'p';self.tree(root);(root/'MANIFEST.json').write_bytes(b'{}')
            with self.assertRaises(ValueError):verify(root)
    def test_symlink_rejected(self):
        verify=self.tool('verify_tree')
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'p';self.tree(root);(root/'a.txt').unlink();(root/'a.txt').symlink_to(root/'MANIFEST.json')
            with self.assertRaises(ValueError):verify(root)
    def test_bad_paths(self):
        safe=self.tool('safe_relative_name')
        for name in ('../x','/x','a/../x','a\\x','C:x','a//x','./x','a/./x',''):
            with self.subTest(name=name):
                with self.assertRaises(ValueError):safe(name)
    def test_good_path(self):
        safe=self.tool('safe_relative_name');self.assertEqual(str(safe('reports/a.md')),'reports/a.md')
    def test_zip_valid_and_existing_destination_refused(self):
        extract=self.tool('safe_extract')
        with tempfile.TemporaryDirectory() as t:
            root=Path(t)/'p';self.tree(root);z=Path(t)/'p.zip';out=Path(t)/'out'
            with zipfile.ZipFile(z,'w') as f:
                for p in root.iterdir():f.write(p,'packet/'+p.name)
            result=extract(z,out);self.assertEqual(result,out/'packet');self.assertTrue(result.is_dir())
            with self.assertRaises(ValueError):extract(z,out)
    def test_zip_traversal_preflight(self):
        extract=self.tool('safe_extract')
        with tempfile.TemporaryDirectory() as t:
            z=Path(t)/'bad.zip';out=Path(t)/'out'
            with zipfile.ZipFile(z,'w') as f:f.writestr('../escape','x')
            with self.assertRaises(ValueError):extract(z,out)
            self.assertFalse(out.exists());self.assertFalse((Path(t)/'escape').exists())
    def test_zip_duplicate_rejected(self):
        extract=self.tool('safe_extract')
        with tempfile.TemporaryDirectory() as t:
            z=Path(t)/'bad.zip';out=Path(t)/'out'
            with zipfile.ZipFile(z,'w') as f:
                f.writestr('packet/a','x');f.writestr('packet/a','y')
            with self.assertRaises(ValueError):extract(z,out)
            self.assertFalse(out.exists())
    def test_zip_symlink_rejected(self):
        extract=self.tool('safe_extract')
        with tempfile.TemporaryDirectory() as t:
            z=Path(t)/'bad.zip';out=Path(t)/'out'
            with zipfile.ZipFile(z,'w') as f:
                info=zipfile.ZipInfo('packet/link');info.create_system=3;info.external_attr=(0o120777<<16);f.writestr(info,'../../x')
            with self.assertRaises(ValueError):extract(z,out)
            self.assertFalse(out.exists())

if __name__=='__main__':unittest.main()
