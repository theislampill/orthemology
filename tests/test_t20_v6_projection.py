"""Negative controls for the independent T20 v6 public object."""
import hashlib
import json
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'scripts'))
from validate_t20_v6_projection import check_object, safe_path, private_locators, private_uuid, origin_reference_text, PREFIX
from validate_decision_dependencies import is_supersession_registry
import validate_decision_dependencies as decisions


class PublicProjectionTests(unittest.TestCase):
    def test_archival_registry_exception_is_exact(self):
        relative = PREFIX + '/sources/53d15c2fba0185fdbb3bccdd5b586fd67e7f78824a2fd1e8860860ce36560dad/decision-status.yaml'
        body = (pathlib.Path(__file__).resolve().parents[1] / relative).read_text(encoding='utf-8')
        self.assertTrue(is_supersession_registry(relative, body))
        self.assertFalse(is_supersession_registry(relative, body + '\nnew normative claim'))
        self.assertFalse(is_supersession_registry('/'.join(('theory', 'decision-status.yaml')), body))
        self.assertFalse(is_supersession_registry(PREFIX + '/decision-status.yaml', body))
        with tempfile.TemporaryDirectory() as tmp:
            fixture = pathlib.Path(tmp) / relative
            fixture.parent.mkdir(parents=True)
            fixture.write_bytes(body.replace('\n', '\r\n').encode())
            with patch.object(decisions, 'ROOT', tmp):
                raw_text = decisions.read(relative, newline='')
            self.assertFalse(is_supersession_registry(relative, raw_text))

    def test_original_reference_binding_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            directory = root / PREFIX
            directory.mkdir(parents=True)
            src = PREFIX + '/source.md'
            target = '/'.join(('scripts', 'original.py'))
            text = 'Historical source ' + target
            binding = {'schema':'t20-v6-exact-origin-references-v1','records':[
                {'repository_path':src,'public_sha256':hashlib.sha256(text.encode()).hexdigest(),
                 'origin_context':'preserved_source_document', 'references':[
                     {'components':target.split('/'),'occurrences':1}]}]}
            (directory / 'ORIGIN_REFERENCES.json').write_text(json.dumps(binding))
            self.assertNotIn(target, origin_reference_text(src, text, root))
            self.assertEqual(origin_reference_text(src, text + ' changed', root), text + ' changed')
            self.assertEqual(origin_reference_text(PREFIX + '/other.md', text, root), text)

    def test_traversal(self):
        for value in ('../a', '/a', 'a/../b', 'a\\b', 'C:/a', ''):
            with self.assertRaises(ValueError):
                safe_path(value)

    def test_private_body_regardless_of_extension(self):
        self.assertTrue(private_locators('Evidence at /' + 'home/owner/private.txt'))
        self.assertTrue(private_locators('Evidence at /' + 'tmp/owner/page.png'))
        self.assertFalse(private_locators('https://example.org/home/article'))
        self.assertFalse(private_locators(r'pattern: /home/[^/]+/'))

    def test_uuid_in_url_is_not_automatically_public(self):
        identifier = '00000000' + '-0000' * 3 + '-000000000000'
        self.assertTrue(private_uuid('https://example.org/' + identifier, '0' * 64))
        self.assertTrue(private_uuid('https://chatgpt.com/c/' + identifier, '0' * 64))

    def test_tampered_and_missing_body(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            body = b'bounded source evidence\n'
            (root / 'body').write_bytes(body)
            sha = hashlib.sha256(body).hexdigest()
            row = dict(source_sha256=sha, source_bytes=len(body), disposition='ADD_EXACT',
                       repository_path='body', public_sha256=sha, public_bytes=len(body))
            self.assertEqual(check_object(root, row), [])
            (root / 'body').write_bytes(b'changed')
            self.assertTrue(check_object(root, row))
            (root / 'body').unlink()
            self.assertTrue(check_object(root, row))

    def test_changed_bytes_cannot_claim_identity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / 'body').write_bytes(b'projection')
            row = dict(source_sha256='0' * 64, source_bytes=10, disposition='ADD_EXACT',
                       repository_path='body', public_sha256=hashlib.sha256(b'projection').hexdigest(), public_bytes=10)
            self.assertTrue(check_object(root, row))

    def test_held_identity_cannot_have_body(self):
        row = dict(source_sha256='0' * 64, disposition='NOT_PUBLISHED', repository_path='body')
        self.assertTrue(check_object(pathlib.Path('.'), row))

    def test_arbitrary_history_revision_cannot_mask_drift(self):
        row = dict(source_sha256='0' * 64, disposition='REUSE', repository_path='body',
                   repository_revision='HEAD', public_sha256='0' * 64, public_bytes=0)
        self.assertTrue(check_object(pathlib.Path('.'), row))

    def test_symlink_not_a_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = pathlib.Path(tmp)
            (root / 'real').write_bytes(b'x')
            (root / 'link').symlink_to(root / 'real')
            row = dict(source_sha256=hashlib.sha256(b'x').hexdigest(), source_bytes=1,
                       disposition='REUSE', repository_path='link', public_sha256=hashlib.sha256(b'x').hexdigest(), public_bytes=1)
            self.assertTrue(check_object(root, row))


if __name__ == '__main__':
    unittest.main()
