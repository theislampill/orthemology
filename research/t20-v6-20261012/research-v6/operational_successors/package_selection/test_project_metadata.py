"""Synthetic controls for a pure metadata projection helper; no corpus access.

Run from this directory with both:
    PYTHONDONTWRITEBYTECODE=1 python -m unittest -v test_project_metadata
    PYTHONDONTWRITEBYTECODE=1 python -O -m unittest -v test_project_metadata
Tests intentionally use unittest checks, never optimizable assert statements.
"""
import copy
from decimal import Decimal
import hashlib
import importlib.util
import json
import unittest


def sha(data):
    return hashlib.sha256(data).hexdigest()


def encode(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode('utf-8')


class ProjectionControls(unittest.TestCase):
    def setUp(self):
        module = importlib.util.find_spec('project_metadata')
        self.assertIsNotNone(module, 'metadata projection helper is not implemented')
        self.m = importlib.util.module_from_spec(module)
        module.loader.exec_module(self.m)
        self.identity = 'a' * 64
        self.local = '/home/private-owner/source.json'
        self.obj = {
            'source_path': self.local,
            'formula': r'∀x∈ℚ: f(x)=a/b + \\alpha − (x≤1) ∧ x≠0',
            'literal_slashes': r'https://example.org/a/b \\server\share',
            'quote': '“原文 / exact \\ quotation”',
            'truth': True, 'count': 1, 'null': None,
            'scope': 'Navigation metadata only; no scientific admission.',
            'nested': {'path': 'preserved', 'values': [False, 2, 'x/y~z']},
        }
        self.raw = encode(self.obj)
        self.spec, self.approval = self.manifests(self.raw, '/source_path', self.local)

    def manifests(self, raw, pointer, old_value, new_value=None, disposition='included'):
        if new_value is None:
            new_value = 'authored_objects/aa/' + self.identity
        row = {'pointer': pointer, 'role': 'source_locator', 'old_value': old_value,
               'new_value': new_value,
               'resolved_identity': {'sha256': self.identity, 'disposition': disposition}}
        field = {'pointer': pointer, 'role': 'source_locator',
                 'output_form': 'relative_reference' if disposition == 'included' else 'identity_record',
                 'decision_reference': 'synthetic-reviewed-field-v1'}
        return ({'schema': 't20-metadata-projection-spec-v1', 'source_sha256': sha(raw),
                 'replacements': [row]},
                {'schema': 't20-metadata-field-approval-v1', 'source_sha256': sha(raw),
                 'fields': [field]})

    def project(self, raw=None, spec=None, approval=None):
        return self.m.project_metadata(self.raw if raw is None else raw,
                                       encode(self.spec if spec is None else spec),
                                       encode(self.approval if approval is None else approval))

    def rejects(self, raw=None, spec=None, approval=None):
        with self.assertRaises(self.m.ProjectionError):
            self.project(raw, spec, approval)

    def test_changes_exactly_one_approved_value_and_deterministic(self):
        before = (self.raw, copy.deepcopy(self.spec), copy.deepcopy(self.approval))
        projected, receipt = self.project()
        expected = copy.deepcopy(self.obj)
        expected['source_path'] = self.spec['replacements'][0]['new_value']
        self.assertEqual(json.loads(projected), expected)
        self.assertEqual(self.project(), (projected, receipt))
        self.assertEqual(before, (self.raw, self.spec, self.approval))
        self.assertNotEqual(sha(projected), sha(self.raw))

    def test_public_receipt_binds_exact_inputs_and_omits_original_locator(self):
        projected, receipt = self.project()
        self.assertEqual(receipt['schema'], 't20-metadata-projection-receipt-v1')
        self.assertEqual(receipt['source_sha256'], sha(self.raw))
        self.assertEqual(receipt['projected_sha256'], sha(projected))
        self.assertEqual(receipt['specification_sha256'], sha(encode(self.spec)))
        self.assertEqual(receipt['approved_fields_sha256'], sha(encode(self.approval)))
        self.assertIs(receipt['unselected_values_verified'], True)
        row = receipt['replacements'][0]
        self.assertEqual(row['pointer'], '/source_path')
        self.assertEqual(row['role'], 'source_locator')
        self.assertEqual(row['original_value_sha256'], sha(encode(self.local)))
        self.assertEqual(row['new_value'], self.spec['replacements'][0]['new_value'])
        self.assertEqual(row['resolved_identity'], self.spec['replacements'][0]['resolved_identity'])
        self.assertEqual(row['permitted_field_decision'], {
            'decision_reference': 'synthetic-reviewed-field-v1', 'output_form': 'relative_reference'})
        self.assertNotIn(self.local, encode(receipt).decode())
        self.assertNotIn('old_value', encode(receipt).decode())

    def test_all_scientific_strings_and_types_unchanged(self):
        projected, _ = self.project()
        got = json.loads(projected)
        for key in self.obj.keys() - {'source_path'}:
            self.assertEqual(got[key], self.obj[key], key)
            self.assertIs(type(got[key]), type(self.obj[key]), key)
        self.assertIs(type(got['truth']), bool)
        self.assertIs(type(got['count']), int)

    def test_arbitrary_original_json_value_can_be_explicit_locator(self):
        for old in [None, False, 1, 1.5, ['old', {'path': 'old'}], {'private': 'old'}]:
            with self.subTest(old=old):
                raw = encode({'locator': old, 'science': {'value': [1, False, None]}})
                spec, approval = self.manifests(raw, '/locator', old)
                projected, _ = self.project(raw, spec, approval)
                self.assertEqual(json.loads(projected)['science'], {'value': [1, False, None]})

    def test_lossless_unselected_numbers_including_huge_exponents(self):
        raw = b'{"source_path":"/home/private-owner/source.json","n":0.123456789012345678901234567890,"huge":1e400,"tiny":1e-400,"negative_zero":-0.00,"integer":123456789012345678901234567890}'
        spec, approval = self.manifests(raw, '/source_path', self.local)
        projected, _ = self.project(raw, spec, approval)
        old = json.loads(raw, parse_float=Decimal)
        new = json.loads(projected, parse_float=Decimal)
        for key in old.keys() - {'source_path'}:
            self.assertEqual(new[key], old[key])
            self.assertIs(type(new[key]), type(old[key]))
            if isinstance(old[key], Decimal):
                self.assertEqual(new[key].as_tuple(), old[key].as_tuple())

    def test_decimal_old_value_is_checked_without_float_rounding(self):
        raw = b'{"locator":0.123456789012345678901234567890}'
        spec, approval = self.manifests(raw, '/locator', 'PLACEHOLDER')
        spec_bytes = encode(spec).replace(b'"PLACEHOLDER"', b'0.123456789012345678901234567890')
        self.m.project_metadata(raw, spec_bytes, encode(approval))
        with self.assertRaises(self.m.ProjectionError):
            self.m.project_metadata(raw, spec_bytes.replace(b'123456789012345678901234567890', b'123456789012345678901234567891'), encode(approval))

    def test_explicit_array_indices_and_pointer_escapes(self):
        raw = encode({'items': [{'a/b': {'~locator': self.local}}, 'keep'], 'a~1b': self.local})
        spec, approval = self.manifests(raw, '/items/0/a~1b/~0locator', self.local)
        extra = copy.deepcopy(spec['replacements'][0]); extra['pointer'] = '/a~01b'
        field = copy.deepcopy(approval['fields'][0]); field['pointer'] = '/a~01b'
        spec['replacements'].append(extra); approval['fields'].append(field)
        projected, _ = self.project(raw, spec, approval)
        got = json.loads(projected)
        self.assertEqual(got['items'][1], 'keep')
        self.assertEqual(got['items'][0]['a/b']['~locator'], extra['new_value'])
        self.assertEqual(got['a~1b'], extra['new_value'])

    def test_empty_object_key_and_numeric_object_keys_are_literal(self):
        for key in ['', '01', '-', '0']:
            with self.subTest(key=key):
                raw = encode({key: self.local})
                spec, approval = self.manifests(raw, '/' + key, self.local)
                projected, _ = self.project(raw, spec, approval)
                self.assertEqual(json.loads(projected)[key], spec['replacements'][0]['new_value'])

    def test_top_level_array_supported(self):
        raw = encode(['keep', self.local])
        spec, approval = self.manifests(raw, '/1', self.local)
        projected, _ = self.project(raw, spec, approval)
        self.assertEqual(json.loads(projected), ['keep', spec['replacements'][0]['new_value']])

    def test_relative_view_reference_allowed(self):
        self.spec['replacements'][0]['new_value'] = 'views/packet-1/subdir/source.json'
        projected, _ = self.project()
        self.assertEqual(json.loads(projected)['source_path'], self.spec['replacements'][0]['new_value'])

    def test_explicit_excluded_and_unresolved_identity_records(self):
        for kind in ['excluded', 'unresolved']:
            with self.subTest(kind=kind):
                record = {'kind': kind, 'sha256': self.identity, 'replay_blocked': True}
                spec, approval = self.manifests(self.raw, '/source_path', self.local, record, kind)
                projected, receipt = self.project(spec=spec, approval=approval)
                self.assertEqual(json.loads(projected)['source_path'], record)
                self.assertEqual(receipt['replacements'][0]['new_value'], record)
                self.assertNotIn(self.local, encode(receipt).decode())

    def test_wrong_source_digest_in_spec_or_approval_rejected(self):
        for target in ['spec', 'approval']:
            with self.subTest(target=target):
                obj = copy.deepcopy(getattr(self, target)); obj['source_sha256'] = 'f' * 64
                self.rejects(**{target: obj})
        self.rejects(raw=self.raw + b' ')

    def test_nonbytes_inputs_rejected(self):
        for index in range(3):
            args = [self.raw, encode(self.spec), encode(self.approval)]
            args[index] = args[index].decode()
            with self.subTest(index=index), self.assertRaises(self.m.ProjectionError):
                self.m.project_metadata(*args)

    def test_duplicate_json_keys_rejected_in_all_inputs(self):
        for index in range(3):
            args = [self.raw, encode(self.spec), encode(self.approval)]
            if index == 0:
                # Bind the changed source bytes so digest checks cannot mask a
                # permissive parser. A last-key-wins parser would accept this.
                raw = b'{"source_path":"shadow",' + self.raw[1:]
                spec, approval = self.manifests(raw, '/source_path', self.local)
                args = [raw, encode(spec), encode(approval)]
            else:
                args[index] = b'{"schema":"shadow",' + args[index][1:]
            with self.subTest(index=index), self.assertRaises(self.m.ProjectionError):
                self.m.project_metadata(*args)
        raw = b'{"source_path":"x","nested":{"a":1,"a":2}}'
        spec, approval = self.manifests(raw, '/source_path', 'x')
        self.rejects(raw, spec, approval)

    def test_nonfinite_constants_rejected_in_all_inputs(self):
        for constant in [b'NaN', b'Infinity', b'-Infinity']:
            for index in range(3):
                args = [self.raw, encode(self.spec), encode(self.approval)]
                args[index] = args[index][:-1] + b',"bad":' + constant + b'}'
                with self.subTest(constant=constant, index=index), self.assertRaises(self.m.ProjectionError):
                    self.m.project_metadata(*args)

    def test_invalid_json_encoding_and_bom_rejected(self):
        for raw in [b'\xff', b'\xef\xbb\xbf' + self.raw, b'{', b'{"x":"\\ud800"}', self.raw + b'{}']:
            with self.subTest(raw=raw):
                spec, approval = self.manifests(raw, '/source_path', self.local)
                self.rejects(raw, spec, approval)

    def test_missing_pointer_rejected(self):
        for pointer in ['/absent', '/nested/absent', '/truth/path', '/nested/values/99']:
            with self.subTest(pointer=pointer):
                spec, approval = self.manifests(self.raw, pointer, self.local)
                self.rejects(spec=spec, approval=approval)

    def test_invalid_pointer_and_array_aliases_rejected(self):
        for pointer in ['', '#/source_path', 'source_path', '/bad~', '/bad~2', '/nested/values/01',
                        '/nested/values/-', '/nested/values/+1', '/nested/values/١', '/nested/values/*']:
            with self.subTest(pointer=pointer):
                spec, approval = self.manifests(self.raw, pointer, self.local)
                self.rejects(spec=spec, approval=approval)

    def test_duplicate_pointer_rejected_in_specs_and_approvals(self):
        spec = copy.deepcopy(self.spec); spec['replacements'] *= 2
        self.rejects(spec=spec)
        approval = copy.deepcopy(self.approval); approval['fields'] *= 2
        self.rejects(approval=approval)

    def test_parent_child_overlap_rejected_in_either_order(self):
        raw = encode({'parent': {'locator': self.local}})
        spec, approval = self.manifests(raw, '/parent', {'locator': self.local})
        child_spec, child_approval = self.manifests(raw, '/parent/locator', self.local)
        spec['replacements'] += child_spec['replacements']; approval['fields'] += child_approval['fields']
        for reverse in [False, True]:
            if reverse:
                spec['replacements'].reverse(); approval['fields'].reverse()
            with self.subTest(reverse=reverse):
                self.rejects(raw, spec, approval)

    def test_pointer_prefix_without_token_overlap_is_allowed(self):
        raw = encode({'path': self.local, 'pathology': self.local})
        spec, approval = self.manifests(raw, '/path', self.local)
        second, second_approval = self.manifests(raw, '/pathology', self.local)
        spec['replacements'] += second['replacements']; approval['fields'] += second_approval['fields']
        projected, _ = self.project(raw, spec, approval)
        self.assertEqual(json.loads(projected)['path'], json.loads(projected)['pathology'])

    def test_stale_old_values_and_bool_numeric_equivalence_rejected(self):
        self.spec['replacements'][0]['old_value'] = 'stale'
        self.rejects()
        for old, stale in [(True, 1), (1, True), (1, 1.0), (1.0, 1), ([True], [1]), ({'x': False}, {'x': 0})]:
            with self.subTest(old=old, stale=stale):
                raw = encode({'locator': old})
                spec, approval = self.manifests(raw, '/locator', stale)
                self.rejects(raw, spec, approval)

    def test_unapproved_pointer_and_role_mismatch_rejected(self):
        approval = copy.deepcopy(self.approval); approval['fields'][0]['pointer'] = '/formula'
        self.rejects(approval=approval)
        approval = copy.deepcopy(self.approval); approval['fields'][0]['role'] = 'dependency_locator'
        self.rejects(approval=approval)
        for value in ['', 'scientific_formula', '/home/private', True]:
            spec = copy.deepcopy(self.spec); approval = copy.deepcopy(self.approval)
            spec['replacements'][0]['role'] = value; approval['fields'][0]['role'] = value
            self.rejects(spec=spec, approval=approval)

    def test_omitted_approved_pointer_rejected(self):
        approval = copy.deepcopy(self.approval)
        extra = copy.deepcopy(approval['fields'][0]); extra['pointer'] = '/nested/path'
        approval['fields'].append(extra)
        self.rejects(approval=approval)

    def test_empty_replacements_and_empty_approval_rejected(self):
        spec = copy.deepcopy(self.spec); spec['replacements'] = []
        approval = copy.deepcopy(self.approval); approval['fields'] = []
        self.rejects(spec=spec); self.rejects(approval=approval)
        self.rejects(spec=spec, approval=approval)

    def test_unsafe_relative_references_rejected(self):
        for path in ['/abs/path', '../source.json', 'views/p/../source.json', 'views//source.json',
                     'views/p/./source.json', 'views/p/source.json/', 'views/p\\source.json',
                     'C:/private/source.json', 'https://example.org/source.json', 'file:///source',
                     'views/p/a?token=x', 'views/p/a#frag', 'views/p/a%2f..%2fx', 'views/p/a:b',
                     'views/p/a\x00b', 'views/p/a\nb', 'views/p/a\x7fb', 'views/p/a\u202eb',
                     'views/p/a ', 'views/p/a.', 'views/p/CON.txt', 'views/p/com¹.txt',
                     'views/p/libfile_123', 'views/p/file_' + 'b' * 32,
                     'views/p/Sentinel_marker', 'views/p/cafe\u0301.json',
                     'other/p/source.json', 'views/source.json', 'views/p/*', 'views/p/<x>',
                     'authored_objects/ab/' + self.identity, 'authored_objects/aa/' + 'b' * 64,
                     'authored_objects/aa/' + self.identity + '/child']:
            with self.subTest(path=path):
                spec = copy.deepcopy(self.spec); spec['replacements'][0]['new_value'] = path
                self.rejects(spec=spec)

    def test_identity_and_form_mismatches_rejected(self):
        for identity in [{'sha256': 'not-a-digest', 'disposition': 'included'},
                         {'sha256': 'a' * 64, 'disposition': 'excluded'},
                         {'sha256': 'a' * 64, 'disposition': 'included', 'path': self.local}]:
            spec = copy.deepcopy(self.spec); spec['replacements'][0]['resolved_identity'] = identity
            self.rejects(spec=spec)
        approval = copy.deepcopy(self.approval); approval['fields'][0]['output_form'] = 'identity_record'
        self.rejects(approval=approval)
        self.approval['fields'][0]['output_form'] = 'unknown'
        self.rejects()

    def test_identity_records_require_permission_exact_identity_and_replay_block(self):
        valid = {'kind': 'excluded', 'sha256': self.identity, 'replay_blocked': True}
        spec, approval = self.manifests(self.raw, '/source_path', self.local, valid, 'excluded')
        for change in [{'replay_blocked': False}, {'replay_blocked': 1}, {'sha256': 'b' * 64},
                       {'kind': 'unresolved'}, {'path': self.local}]:
            modified = copy.deepcopy(spec); modified['replacements'][0]['new_value'].update(change)
            self.rejects(spec=modified, approval=approval)
        approval['fields'][0]['output_form'] = 'relative_reference'
        self.rejects(spec=spec, approval=approval)

    def test_unknown_schema_and_fields_rejected(self):
        for name in ['spec', 'approval']:
            for change in [{'schema': 'unknown'}, {'surprise': True}]:
                obj = copy.deepcopy(getattr(self, name)); obj.update(change)
                self.rejects(**{name: obj})
        spec = copy.deepcopy(self.spec); spec['replacements'][0]['wildcard'] = True
        self.rejects(spec=spec)
        approval = copy.deepcopy(self.approval); approval['fields'][0]['wildcard'] = True
        self.rejects(approval=approval)

    def test_missing_manifest_fields_rejected(self):
        for target, array in [('spec', 'replacements'), ('approval', 'fields')]:
            for key in getattr(self, target)[array][0]:
                with self.subTest(target=target, key=key):
                    obj = copy.deepcopy(getattr(self, target)); del obj[array][0][key]
                    self.rejects(**{target: obj})

    def test_private_decision_or_pointer_cannot_leak_into_receipt(self):
        for decision in ['/home/private/approval', 'https://private/token', 'libfile_sensitive']:
            approval = copy.deepcopy(self.approval); approval['fields'][0]['decision_reference'] = decision
            self.rejects(approval=approval)
        raw = encode({'/home/private/source': self.local})
        spec, approval = self.manifests(raw, '/~1home~1private~1source', self.local)
        self.rejects(raw, spec, approval)

    def test_accidental_unselected_value_change_is_detected_after_serialization(self):
        canonical = self.m._canonical

        def broken_serializer(value):
            if type(value) is dict and 'formula' in value:
                value = copy.deepcopy(value)
                value['formula'] = 'accidental scientific edit'
            return canonical(value)

        self.m._canonical = broken_serializer
        self.rejects()

    def test_accidental_selected_value_change_is_detected_after_serialization(self):
        canonical = self.m._canonical

        def broken_serializer(value):
            if type(value) is dict and 'source_path' in value:
                value = copy.deepcopy(value)
                value['source_path'] = 'views/wrong/value.json'
            return canonical(value)

        self.m._canonical = broken_serializer
        self.rejects()

    def test_integral_decimal_tokens_keep_decimal_type_and_exponent(self):
        for token in [b'1e0', b'-0e0', b'1e1', b'10.0', b'1.000', b'0.00']:
            with self.subTest(token=token):
                raw = b'{"source_path":"/home/private-owner/source.json","n":' + token + b'}'
                spec, approval = self.manifests(raw, '/source_path', self.local)
                projected, _ = self.project(raw, spec, approval)
                old = json.loads(raw, parse_float=Decimal)['n']
                new = json.loads(projected, parse_float=Decimal)['n']
                self.assertIs(type(new), Decimal)
                self.assertEqual(new.as_tuple(), old.as_tuple())

    def test_receipt_and_projected_bytes_do_not_alias_input_objects(self):
        projected, receipt = self.project()
        receipt['replacements'][0]['resolved_identity']['sha256'] = 'f' * 64
        receipt['replacements'][0]['new_value'] = 'changed'
        projected2, receipt2 = self.project()
        self.assertEqual(projected, projected2)
        self.assertEqual(receipt2['replacements'][0]['resolved_identity']['sha256'], self.identity)


if __name__ == '__main__':
    unittest.main()
