"""Synthetic packaging controls. No inherited source is executed or imported."""
import copy
import importlib.util
import tempfile
import unittest
from pathlib import Path
import plan_selection as p


class MaterialiserControls(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.find_spec('materialise_selection')
        self.assertIsNotNone(spec, 'selected-source materialiser is not implemented')
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.sources = self.root / 'sources'
        self.sources.mkdir()
        self.data = b'raise RuntimeError("must never execute")\n'
        self.h = p.digest(self.data)
        (self.sources / 'source.py').write_bytes(self.data)
        self.rec = {'sha256': self.h, 'bytes': len(self.data), 'source_path': 'sources/source.py',
                    'source_hash_verified': True, 'reviewed_digest': self.h,
                    'current_path_digest': self.h, 'prior_exclusion_reasons': [],
                    'sensitive_screen_flags': []}
        self.row = {'sha256': self.h, 'action': 'include', 'scope_status': 'source-only',
                    'eligibility': {'basis': 'reviewed_owner_authored',
                     'decision_reference': 'reviewed-selection', 'content_reviewed_for_distribution': True,
                     'resolved_historical_role_filters': []},
                    'role': 'authored_code', 'required_dependencies': [],
                    'views': [{'packet': 'one', 'path': 'source.py'},
                              {'packet': 'two', 'path': 'source.py'}]}
        selection = {'schema': p.SCHEMA, 'assembly_authorized': False, 'audience': 'public_repository',
                     'decision_reference': 'reviewed-selection', 'destination': 'selected-v6',
                     'baseline_policy': 'separate_unchanged_owner_checkpoint',
                     'lookup_sha256': 'b'*64, 'v5_index_sha256': 'c'*64, 'exclusions_sha256': 'd'*64,
                     'v5_archive_sha256': 'a'*64, 'objects': [self.row]}
        self.result = p.build_plan(selection, {self.h: self.rec},
                                   {'zip_sha256': 'a'*64, 'members': []}, {}, self.root)
        self.out = self.root / 'package'

    def bind(self):
        self.result['plan_sha256'] = p.digest(p.canonical(self.result['public_plan']))

    def run_materialise(self, destination=None):
        return self.m.materialise(self.result, destination or self.out, [self.sources], self.root)

    def rejects(self, destination=None):
        target = destination or self.out
        with self.assertRaises(ValueError):
            self.run_materialise(target)
        self.assertFalse(target.exists())

    def test_cas_once_two_logical_views_and_deterministic_receipt(self):
        receipt = self.run_materialise()
        self.assertEqual(receipt, self.run_materialise(self.root / 'package2'))
        objects = list((self.out / 'authored_objects').glob('*/*'))
        self.assertEqual(objects, [self.out / 'authored_objects' / self.h[:2] / self.h])
        self.assertEqual(objects[0].read_bytes(), self.data)
        self.assertFalse((self.out / 'one').exists())
        view_map = p.parse((self.out / 'VIEW_MAP.json').read_bytes())
        self.assertEqual(view_map['views'], self.result['public_plan']['views'])
        self.assertEqual(view_map['plan_sha256'], self.result['plan_sha256'])
        self.assertEqual(p.parse((self.out / 'MATERIALISATION.json').read_bytes()), receipt)
        for f in self.out.rglob('*.json'):
            self.assertNotIn(str(self.root), f.read_text())
        self.assertEqual((self.sources / 'source.py').read_bytes(), self.data)

    def test_v5_provider_becomes_self_contained_cas(self):
        provider = {'kind': 'separate_v5_member', 'archive_sha256': 'a'*64, 'member': 'old/source.py'}
        self.result['public_plan']['objects'][0]['provider'] = provider
        self.result['private_resolution'][0]['provider'] = copy.deepcopy(provider)
        self.bind()
        self.run_materialise()
        self.assertEqual((self.out / 'authored_objects' / self.h[:2] / self.h).read_bytes(), self.data)
        self.assertEqual(len(list(self.out.rglob('*'))), 6)

    def test_digest_drift_before_writes(self):
        (self.sources / 'source.py').write_bytes(b'changed')
        self.rejects()

    def test_malformed_and_stale_plan_digest(self):
        for value in ['not-a-hash', 'f'*64]:
            with self.subTest(value=value):
                self.result['plan_sha256'] = value
                self.rejects()

    def test_existing_output_untouched(self):
        self.out.mkdir()
        (self.out / 'sentinel').write_bytes(b'keep')
        with self.assertRaises(ValueError):
            self.run_materialise()
        self.assertEqual(list(self.out.iterdir()), [self.out / 'sentinel'])

    def test_protected_root_overlap(self):
        self.rejects(self.sources / 'new')
        absent = self.root / 'preserved'
        with self.assertRaises(ValueError):
            self.m.materialise(self.result, absent, [absent / 'child'], self.root)
        self.assertFalse(absent.exists())

    def test_symlink_destination_parent(self):
        (self.root / 'alias').symlink_to(self.root, target_is_directory=True)
        self.rejects(self.root / 'alias' / 'new')

    def test_source_symlink_rejected(self):
        (self.root / 'alias').symlink_to(self.sources, target_is_directory=True)
        self.result['private_resolution'][0]['source_path'] = 'alias/source.py'
        self.rejects()

    def test_identity_only_is_not_copied_and_dependency_stays_blocked(self):
        other = 'e'*64
        self.result['public_plan']['objects'].append({
            'sha256': other, 'action': 'identity_only', 'reviewed_digest': other,
            'current_path_digest': None, 'scope_status': 'identity-only',
            'exclusion_categories': ['private_machine_locators'], 'availability': 'held_excluded'})
        self.result['public_plan']['objects'][0]['required_dependencies'] = [other]
        blocker = {'consumer': self.h, 'dependency': other, 'reason': 'required_dependency_not_delivered'}
        self.result['public_plan']['replay_blockers'] = [blocker]
        self.bind()
        self.run_materialise()
        self.assertFalse((self.out / 'authored_objects' / other[:2] / other).exists())
        self.assertEqual(p.parse((self.out / 'PUBLIC_PLAN.json').read_bytes())['replay_blockers'], [blocker])

    def test_identity_only_view_rejected(self):
        self.result['public_plan']['objects'][0]['action'] = 'identity_only'
        self.bind()
        self.rejects()

    def test_private_resolver_exact_parity(self):
        original = copy.deepcopy(self.result['private_resolution'])
        for bad in [[], original + original, [dict(original[0], sha256='e'*64)],
                    [dict(original[0], proposed_operation='execute')],
                    [dict(original[0], provider={'kind': 'wrong'})]]:
            with self.subTest(bad=bad):
                self.result['private_resolution'] = bad
                self.rejects()

    def test_independent_public_eligibility_rejected(self):
        original = copy.deepcopy(self.result)
        for field, value in [('eligibility_basis', 'lookup_identity'), ('role', 'unknown'),
                             ('exclusion_categories', ['private_machine_locators']),
                             ('bytes', True), ('bytes', len(self.data)+1)]:
            with self.subTest(field=field):
                self.result = copy.deepcopy(original)
                self.result['public_plan']['objects'][0][field] = value
                self.bind()
                self.rejects()

    def test_plan_state_and_execution_rejected(self):
        original = copy.deepcopy(self.result)
        for key, value in [('state', 'ASSEMBLED'), ('source_execution_selected', True)]:
            self.result = copy.deepcopy(original)
            self.result['public_plan'][key] = value
            self.bind()
            self.rejects()

    def test_unsafe_collision_and_prefix_triplet(self):
        for names in [['one/A', 'one/A-other', 'one/A/deep.py'],
                      ['one/a/b', 'one/a/b-other', 'ONE/A/B/deep.py'],
                      ['one/a.py', 'ONE/A.py'], ['../escape'], ['one/CON'], ['one/a?b']]:
            with self.subTest(names=names):
                self.result['public_plan']['views'] = [{'path': n, 'sha256': self.h} for n in names]
                self.bind()
                self.rejects()

    def test_casefold_directory_alias_rejected(self):
        self.result['public_plan']['views'] = [
            {'path': 'one/Dir/a.py', 'sha256': self.h},
            {'path': 'one/dir/b.py', 'sha256': self.h}]
        self.bind()
        self.rejects()

    def test_missing_views_or_unknown_view_identity_rejected(self):
        for views in [[], [{'path': 'one/a.py', 'sha256': 'e'*64}]]:
            self.result['public_plan']['views'] = views
            self.bind()
            self.rejects()

    def test_private_metadata_in_public_plan_rejected(self):
        self.result['public_plan']['private_resolution'] = str(self.sources)
        self.bind()
        self.rejects()

    def test_omitted_dependency_blocker_rejected(self):
        self.result['public_plan']['objects'][0]['required_dependencies'] = ['e'*64]
        self.bind()
        self.rejects()


class ReconstructionControls(unittest.TestCase):
    setUp = MaterialiserControls.setUp
    run_materialise = MaterialiserControls.run_materialise

    def prepare(self):
        self.assertTrue(hasattr(self.m, 'reconstruct_views'), 'view reconstruction is not implemented')
        self.run_materialise()
        self.views_out = self.root / 'views'

    def rejects(self, destination=None):
        target = destination or self.views_out
        with self.assertRaises(ValueError):
            self.m.reconstruct_views(self.out, target)
        self.assertFalse(target.exists())

    def rebind_package(self, plan):
        # Rebind all unkeyed public hashes to test semantic validation independently.
        plan_hash = p.digest(p.canonical(plan))
        view_map = p.parse((self.out / 'VIEW_MAP.json').read_bytes())
        view_map['plan_sha256'] = plan_hash
        view_map['views'] = plan['views']
        receipt = p.parse((self.out / 'MATERIALISATION.json').read_bytes())
        receipt['plan_sha256'] = plan_hash
        receipt['view_map_sha256'] = p.digest(p.canonical(view_map))
        receipt['view_count'] = len(view_map['views'])
        for name, value in [('PUBLIC_PLAN.json', plan), ('VIEW_MAP.json', view_map),
                            ('MATERIALISATION.json', receipt)]:
            (self.out / name).write_bytes(p.canonical(value))

    def test_valid_two_views_are_independent_copies(self):
        self.prepare()
        receipt = self.m.reconstruct_views(self.out, self.views_out)
        self.assertEqual(receipt, self.m.reconstruct_views(self.out, self.root / 'views2'))
        self.assertEqual(sorted(str(f.relative_to(self.views_out)) for f in self.views_out.rglob('*') if f.is_file()),
                         ['one/source.py', 'two/source.py'])
        cas = self.out / 'authored_objects' / self.h[:2] / self.h
        for name in ['one/source.py', 'two/source.py']:
            f = self.views_out / name
            self.assertEqual(f.read_bytes(), self.data)
            self.assertFalse(f.is_symlink())
            self.assertNotEqual(f.stat().st_ino, cas.stat().st_ino)
        (self.views_out / 'one/source.py').write_bytes(b'changed view')
        self.assertEqual(cas.read_bytes(), self.data)
        self.assertEqual((self.views_out / 'two/source.py').read_bytes(), self.data)

    def test_tampered_store_body_before_writes(self):
        self.prepare()
        (self.out / 'authored_objects' / self.h[:2] / self.h).write_bytes(b'tampered')
        self.rejects()

    def test_unsafe_traversal_even_with_rebound_hashes(self):
        self.prepare()
        plan = self.result['public_plan']
        plan['views'] = [{'path': '../escape', 'sha256': self.h}]
        self.rebind_package(plan)
        self.rejects()

    def test_sibling_intervened_prefix_triplet(self):
        self.prepare()
        plan = self.result['public_plan']
        plan['views'] = [{'path': path, 'sha256': self.h}
                         for path in ['one/A', 'one/A-other', 'one/A/source.py']]
        self.rebind_package(plan)
        self.rejects()

    def test_stale_view_map(self):
        self.prepare()
        view_map = p.parse((self.out / 'VIEW_MAP.json').read_bytes())
        view_map['views'][0]['path'] = 'one/wrong.py'
        (self.out / 'VIEW_MAP.json').write_bytes(p.canonical(view_map))
        self.rejects()

    def test_map_cannot_add_unselected_views_even_if_rehashed(self):
        self.prepare()
        view_map = p.parse((self.out / 'VIEW_MAP.json').read_bytes())
        view_map['views'].append({'path': 'extra/source.py', 'sha256': self.h})
        (self.out / 'VIEW_MAP.json').write_bytes(p.canonical(view_map))
        receipt = p.parse((self.out / 'MATERIALISATION.json').read_bytes())
        receipt['view_map_sha256'] = p.digest(p.canonical(view_map))
        receipt['view_count'] += 1
        (self.out / 'MATERIALISATION.json').write_bytes(p.canonical(receipt))
        self.rejects()

    def test_output_inside_input_rejected(self):
        self.prepare()
        self.rejects(self.out / 'views')

    def test_output_must_be_fresh_sibling(self):
        self.prepare()
        other = self.root / 'other'
        other.mkdir()
        self.rejects(other / 'views')

    def test_existing_output_untouched(self):
        self.prepare()
        self.views_out.mkdir()
        (self.views_out / 'keep').write_bytes(b'keep')
        with self.assertRaises(ValueError):
            self.m.reconstruct_views(self.out, self.views_out)
        self.assertEqual(list(self.views_out.iterdir()), [self.views_out / 'keep'])

    def test_symlink_store_body_rejected(self):
        self.prepare()
        body = self.out / 'authored_objects' / self.h[:2] / self.h
        body.unlink()
        body.symlink_to(self.sources / 'source.py')
        self.rejects()

    def test_symlink_metadata_rejected(self):
        self.prepare()
        plan = self.out / 'PUBLIC_PLAN.json'
        external = self.root / 'external.json'
        external.write_bytes(plan.read_bytes())
        plan.unlink()
        plan.symlink_to(external)
        self.rejects()

    def test_unselected_store_body_rejected(self):
        self.prepare()
        extra = self.out / 'authored_objects' / self.h[:2] / ('e'*64)
        extra.write_bytes(b'unselected')
        self.rejects()

    def test_boolean_integer_receipt_confusion_rejected(self):
        self.prepare()
        receipt = p.parse((self.out / 'MATERIALISATION.json').read_bytes())
        receipt['object_count'] = True
        (self.out / 'MATERIALISATION.json').write_bytes(p.canonical(receipt))
        self.rejects()

    def test_missing_completion_receipt_rejected(self):
        self.prepare()
        (self.out / 'MATERIALISATION.json').unlink()
        self.rejects()


if __name__ == '__main__':
    unittest.main()
