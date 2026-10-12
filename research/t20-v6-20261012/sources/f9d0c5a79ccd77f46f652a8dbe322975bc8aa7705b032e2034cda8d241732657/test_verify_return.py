import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import zipfile

SPEC = importlib.util.spec_from_file_location('verify_return', Path(__file__).with_name('tooling')/'verify_return.py')
v = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(v)


class IntegrityTests(unittest.TestCase):
    def fixture(self, root):
        (root/'paper.md').write_text('A bounded ordinary proof.\n')
        registry = {'subjects':[{'id':'paper','custody':'new_source','qualification':'fresh_ordinary_review',
                       'scope':'Ordinary proof only', 'files':[v.identity(root/'paper.md','paper.md')]}],
                    'unavailable_prior_scopes':[{'id':'old_kernel','status':'unavailable','files':[]}]}
        (root/'EVIDENCE_REGISTRY.json').write_text(json.dumps(registry))
        v.seal(root)

    def test_valid_and_changed(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t); self.fixture(p)
            self.assertEqual(v.verify(p)['status'],'PASS_INTEGRITY')
            (p/'paper.md').write_text('Changed')
            with self.assertRaises(ValueError):v.verify(p)

    def test_extra_and_missing(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t); self.fixture(p); (p/'extra.txt').write_text('extra')
            with self.assertRaises(ValueError):v.verify(p)
            (p/'extra.txt').unlink(); (p/'paper.md').unlink()
            with self.assertRaises(ValueError):v.verify(p)

    def test_unsafe_paths(self):
        for s in ['../x','/x','x/../y','x\\y','C:x','x//y','./x','x\x00y']:
            with self.subTest(s=s),self.assertRaises(ValueError):v.safe_path(Path('/tmp'),s)

    def test_symlink(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t); (p/'x').write_text('x'); (p/'y').symlink_to(p/'x')
            with self.assertRaises(ValueError):v.seal(p)

    def test_scope_binding_is_checked_after_reseal(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t); self.fixture(p)
            data=json.loads((p/'EVIDENCE_REGISTRY.json').read_text())
            data['subjects'][0]['files'][0]['sha256']='0'*64
            (p/'EVIDENCE_REGISTRY.json').write_text(json.dumps(data)); v.seal(p)
            with self.assertRaises(ValueError):v.verify(p)

    def test_unavailable_cannot_claim_payload(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t); self.fixture(p)
            data=json.loads((p/'EVIDENCE_REGISTRY.json').read_text())
            data['unavailable_prior_scopes'][0]['files']=['paper.md']
            (p/'EVIDENCE_REGISTRY.json').write_text(json.dumps(data)); v.seal(p)
            with self.assertRaises(ValueError):v.verify(p)

    def test_compiled_and_raw_cache_rejected(self):
        for name,data in [('x.olean',b'x'),('x.pyc',b'x'),('tool',b'\x7fELFfake'),('x.pdf',b'%PDF'),('sources/raw.html',b'raw'),('primary-inputs/paper.txt',b'raw')]:
            with self.subTest(name=name),tempfile.TemporaryDirectory() as t:
                p=Path(t); q=p/name; q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(data)
                with self.assertRaises(ValueError):v.seal(p)

    def test_archive_duplicates_and_nested_compiled(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'dup.zip'
            with zipfile.ZipFile(p,'w') as z:z.writestr('x','a');z.writestr('x','b')
            with self.assertRaises(ValueError):v.check_zip(p)

    def test_docx_members_are_screened(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)
            with zipfile.ZipFile(p/'report.docx','w') as z:z.writestr('object.olean','x')
            with self.assertRaises(ValueError):v.seal(p)
            p=Path(t)/'bad.zip'
            with zipfile.ZipFile(p,'w') as z:z.writestr('../escape','x')
            with self.assertRaises(ValueError):v.check_zip(p)
            p=Path(t)/'compiled.zip'
            with zipfile.ZipFile(p,'w') as z:z.writestr('x.olean','x')
            with self.assertRaises(ValueError):v.check_zip(p)


if __name__=='__main__':unittest.main()
