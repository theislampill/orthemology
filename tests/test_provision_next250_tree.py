import copy
import hashlib
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import json

spec = importlib.util.spec_from_file_location('provision', Path(__file__).resolve().parents[1] / 'scripts/provision_next250_tree.py')
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)

class TreeControls(unittest.TestCase):
    def setUp(self):
        self.flat = b'100644 blob ' + b'a' * 40 + b'\tpublic/metadata.json\0'
        self.change = [{'path': 'public/metadata.json', 'before_entry': self.flat.decode(),
                        'after_entry': '100644 blob ' + 'b' * 40 + '\tpublic/metadata.json\0'}]

    def test_exact_git_tree_serialization(self):
        oid, objects = p.reconstruct(self.flat, self.change)
        child = b'100644 metadata.json\0' + bytes.fromhex('b' * 40)
        child_oid = hashlib.sha1(b'tree ' + str(len(child)).encode() + b'\0' + child).hexdigest()
        root = b'40000 public\0' + bytes.fromhex(child_oid)
        self.assertEqual(oid, hashlib.sha1(b'tree ' + str(len(root)).encode() + b'\0' + root).hexdigest())
        self.assertEqual(objects[child_oid], child)

    def test_wrong_original_identity_rejected(self):
        self.change[0]['before_entry'] = self.change[0]['before_entry'].replace('a' * 40, 'c' * 40)
        with self.assertRaisesRegex(ValueError, 'before entry'): p.reconstruct(self.flat, self.change)

    def test_wrong_after_identity_changes_root(self):
        good = p.reconstruct(self.flat, self.change)[0]
        self.change[0]['after_entry'] = self.change[0]['after_entry'].replace('b' * 40, 'c' * 40)
        self.assertNotEqual(p.reconstruct(self.flat, self.change)[0], good)

    def test_missing_original_rejected(self):
        with self.assertRaisesRegex(ValueError, 'before entry'): p.reconstruct(b'', self.change)

    def test_duplicate_or_unsafe_domain_rejected(self):
        with self.assertRaises(ValueError): p.reconstruct(self.flat, self.change * 2)
        self.change[0]['path'] = '../held/source'
        with self.assertRaisesRegex(ValueError, 'unsafe'): p.reconstruct(self.flat, self.change)

    def test_metadata_symlink_rejected_before_target_read(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d); (root / 'metadata').symlink_to(root / 'held')
            with self.assertRaisesRegex(ValueError, 'symlink'): p.read_metadata(root, 'metadata/file')

    def test_wrong_expected_root_refuses_before_any_object_write(self):
        q = {'verdict': 'QUALIFIED_PROVISIONAL_INPUT',
             'published_base': {'commit': 'c' * 40, 'tree': 'd' * 40},
             'tree': 'e' * 40, 'permitted_changes': self.change}
        body = json.dumps(q).encode()
        identity = [hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest(),
                    hashlib.sha256(body).hexdigest(), len(body)]
        b = {'published_base': q['published_base'], 'provisional_input': {
            'tree': q['tree'], 'expected_document': q, 'qualification': {
                'path': 'docs/provenance/r0002-next250-receiver/PROVISIONAL-QUALIFICATION.json',
                'role': 'provisional_qualification', 'origin': 'reviewed_receipt', 'identity': identity}}}
        def invoke(root, *args, **kwargs):
            if args[0] == 'rev-parse': return ('d' * 40 + '\n').encode()
            if args[0] == 'merge-base': return b''
            if args[0] == 'ls-tree': return self.flat
            self.fail('unexpected write operation')
        with mock.patch.object(p, 'read_metadata', side_effect=[b'NEXT250_BINDING = ' + repr(b).encode(), body]), mock.patch.object(p, 'git', side_effect=invoke) as calls:
            with self.assertRaisesRegex(ValueError, 'reconstructed provisional tree differs'): p.provision('.')
            self.assertFalse(any(c.args[1] == 'hash-object' for c in calls.call_args_list))

    def test_binding_extraction_does_not_execute_source(self):
        self.assertEqual(p.binding_from_source("raise RuntimeError('do not execute')\nNEXT250_BINDING = {'ok': True}"), {'ok': True})

if __name__ == '__main__': unittest.main()
