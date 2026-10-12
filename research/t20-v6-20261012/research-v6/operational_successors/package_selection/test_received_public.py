"""Synthetic received-public identity controls; no retained source execution."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
import plan_selection as p
import materialise_selection as m


class ReceivedPublicControls(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.h = p.digest(b'received public research\n')
        self.original = 'e' * 64
        self.receipt = {
            'schema': 't20-received-public-qualification-v1',
            'public_sha256': self.h, 'original_sha256': self.original,
            'repository': 'theislampill/orthemology', 'commit': '7' * 40,
            'repository_path': 'research/source.md',
            'source_reading': {'ledger_sha256': '9' * 64,
                               'pointer': '$/records/5', 'scope': 'complete_body'},
            'equivalence_to_original': 'unverified_original_unavailable'}
        self.source = {'sha256': self.h, 'action': 'include',
            'scope_status': 'full-public-body-original-unavailable',
            'eligibility': {'basis': 'reviewed_received_public_version',
                'decision_reference': 'root-qualified-received-source',
                'content_reviewed_for_distribution': True,
                'resolved_historical_role_filters': []},
            'role': 'authored_argument', 'required_dependencies': [],
            'views': [{'packet': 'received', 'path': 'source.md'}],
            'original_sha256': self.original}
        self.selection = {'schema': p.SCHEMA, 'assembly_authorized': False,
            'audience': 'owner_private_handoff', 'decision_reference': 'reviewed-source',
            'destination': 'selected-v6',
            'baseline_policy': 'separate_unchanged_owner_checkpoint',
            'lookup_sha256': 'b' * 64, 'v5_index_sha256': 'c' * 64,
            'exclusions_sha256': 'd' * 64, 'v5_archive_sha256': 'a' * 64}
        (self.root / 'source.md').write_bytes(b'received public research\n')
        self.v5 = {'zip_sha256': 'a' * 64, 'members': []}

    def inputs(self):
        raw = p.canonical(self.receipt)
        rh = p.digest(raw)
        (self.root / 'receipt.json').write_bytes(raw)
        self.source['received_public_qualification_sha256'] = rh
        receipt_row = copy.deepcopy(self.source)
        for key in ('original_sha256', 'received_public_qualification_sha256'):
            receipt_row.pop(key)
        receipt_row.update(sha256=rh, role='qualified_metadata',
            views=[{'packet': 'received', 'path': 'qualification.json'}])
        receipt_row['eligibility']['basis'] = 'reviewed_distribution_metadata'
        original_row = {'sha256': self.original, 'action': 'identity_only',
                        'scope_status': 'original-unavailable'}
        self.selection['objects'] = [self.source, receipt_row, original_row]
        lookup = {}
        for h, path in ((self.h, 'source.md'), (rh, 'receipt.json')):
            lookup[h] = {'sha256': h, 'source_path': path,
                'bytes': len((self.root / path).read_bytes()),
                'source_hash_verified': True, 'reviewed_digest': h,
                'current_path_digest': h, 'prior_exclusion_reasons': [],
                'sensitive_screen_flags': []}
        lookup[self.original] = {'sha256': self.original, 'source_hash_verified': False,
                                 'current_path_digest': None}
        return lookup

    def build(self, change=None):
        lookup = self.inputs()
        if change:
            change(self.selection, lookup)
        return p.build_plan(self.selection, lookup, self.v5, {}, self.root)

    def test_received_version_preserves_unverified_original_and_cas(self):
        result = self.build()
        obj = next(x for x in result['public_plan']['objects'] if x['sha256'] == self.h)
        self.assertEqual(obj['original_equivalence_status'], 'unverified_original_unavailable')
        self.assertNotIn('transformation_receipt_sha256', obj)
        target = self.root / 'package'
        m.materialise(result, target, [self.root / 'source.md'], self.root)
        m.reconstruct_views(target, self.root / 'views')
        self.assertEqual((self.root / 'views/received/source.md').read_bytes(), b'received public research\n')

    def test_receipt_public_digest_mismatch(self):
        self.receipt['public_sha256'] = 'f' * 64
        with self.assertRaises(ValueError): self.build()

    def test_receipt_original_digest_mismatch(self):
        self.receipt['original_sha256'] = 'f' * 64
        with self.assertRaises(ValueError): self.build()

    def test_receipt_cannot_claim_verified_equivalence(self):
        self.receipt['equivalence_to_original'] = 'verified'
        with self.assertRaises(ValueError): self.build()

    def test_receipt_requires_full_source_reading(self):
        self.receipt['source_reading']['scope'] = 'selected_lines'
        with self.assertRaises(ValueError): self.build()

    def test_receipt_requires_exact_commit_and_safe_path(self):
        for key, value in [('commit', 'main'), ('repository_path', '../source.md'),
                           ('repository', 'unknown/other')]:
            saved = self.receipt[key]
            self.receipt[key] = value
            with self.subTest(key=key), self.assertRaises(ValueError): self.build()
            self.receipt[key] = saved

    def test_original_must_be_identity_only(self):
        with self.assertRaises(ValueError):
            self.build(lambda s, l: s['objects'][2].update(action='omit'))

    def test_receipt_must_be_included_metadata(self):
        for field, value in [('action', 'identity_only'), ('role', 'authored_code')]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.build(lambda s, l: s['objects'][1].update({field: value}))

    def test_source_cannot_mix_projection_receipt(self):
        self.source['transformation_receipt_sha256'] = 'f' * 64
        with self.assertRaises(ValueError): self.build()

    def test_receipt_duplicate_keys_rejected(self):
        lookup = self.inputs()
        raw = b'{"schema":"x","schema":"y"}'
        old = self.source['received_public_qualification_sha256']
        new = p.digest(raw)
        (self.root / 'receipt.json').write_bytes(raw)
        lookup[new] = lookup.pop(old)
        lookup[new].update(sha256=new, bytes=len(raw), reviewed_digest=new, current_path_digest=new)
        self.source['received_public_qualification_sha256'] = new
        self.selection['objects'][1]['sha256'] = new
        with self.assertRaises(ValueError): p.build_plan(self.selection, lookup, self.v5, {}, self.root)

    def test_materialiser_rechecks_qualification_body_before_writes(self):
        result = self.build()
        self.receipt['public_sha256'] = 'f' * 64
        raw = p.canonical(self.receipt)
        new = p.digest(raw)
        old = self.source['received_public_qualification_sha256']
        (self.root / 'receipt.json').write_bytes(raw)
        plan = result['public_plan']
        for obj in plan['objects']:
            if obj['sha256'] == old:
                obj.update(sha256=new, reviewed_digest=new, current_path_digest=new, bytes=len(raw))
                obj['provider']['path'] = 'authored_objects/' + new[:2] + '/' + new
            if obj['sha256'] == self.h:
                obj['received_public_qualification_sha256'] = new
        plan['objects'].sort(key=lambda x: x['sha256'])
        for view in plan['views']:
            if view['sha256'] == old: view['sha256'] = new
        for resolver in result['private_resolution']:
            if resolver['sha256'] == old:
                resolver['sha256'] = new
                resolver['provider']['path'] = 'authored_objects/' + new[:2] + '/' + new
        result['plan_sha256'] = p.digest(p.canonical(plan))
        target = self.root / 'blocked'
        with self.assertRaises(ValueError): m.materialise(result, target, [], self.root)
        self.assertFalse(target.exists())


if __name__ == '__main__': unittest.main()
