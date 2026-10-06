"""Public-only regression for the exact retained G1 membership correction.

Run after the D08 fragment is joined. No compiler, archive extraction, metadata
process or scientific driver is needed. Environment overrides are test paths,
never production trust inputs.
"""
import copy
from contextlib import ExitStack
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
from unittest import mock
import zipfile

ROOT = Path(os.environ.get('G1_MEMBERSHIP_TEST_ROOT', Path(__file__).resolve().parents[1]))
ADAPTER = Path(os.environ.get('G1_MEMBERSHIP_TEST_ADAPTER', ROOT / 'scripts/replay_v5_successors.py'))
FRAGMENT = Path(os.environ.get('G1_MEMBERSHIP_TEST_FRAGMENT', ROOT / 'docs/provenance/v5-successors/fragments/D08.json'))
VALIDATOR = Path(os.environ.get('G1_MEMBERSHIP_TEST_VALIDATOR', ROOT / 'scripts/validate_v5_successors.py'))

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

class G1MembershipPublicTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.effects = ExitStack(); cls.addClassCleanup(cls.effects.close)
        for owner, name in [(subprocess, 'Popen'), (subprocess, 'run'), (subprocess, 'call'),
                            (shutil, 'unpack_archive'), (zipfile.ZipFile, 'extract'), (zipfile.ZipFile, 'extractall')]:
            cls.effects.enter_context(mock.patch.object(owner, name, side_effect=AssertionError('Forbidden effect: ' + name)))
        cls.a = load('_public_g1_membership_adapter', ADAPTER)
        cls.d02 = load('_public_g1_membership_d02', VALIDATOR)
        fragment = json.loads(FRAGMENT.read_bytes())
        catalog = json.loads((ADAPTER.parent / 'replay_v5_successor_assets/selector_g1/replay_selector_g1_catalog.json').read_bytes())
        cls.sources = copy.deepcopy(catalog['sources'])
        for row in fragment['sources']:
            if row['id'] in cls.sources and row != cls.sources[row['id']]:
                raise ValueError('Public source record differs from the frozen catalogue')
            cls.sources[row['id']] = row
        cls.reviews = {r['id']:r for r in fragment['reviews']}
        cls.suite = next(s for s in fragment['suites'] if s['id'] == 'd08-g1')
        cls.receipt = next(r for r in fragment['receipts'] if r['suite_id'] == 'd08-g1')
        cls.old = catalog['families']['g1']['suite']
        cls.prior = cls.receipt['replay_evidence']['prior']['receipt']

    def check(self, receipt=None):
        self.a.validate_receipt(self.receipt if receipt is None else receipt, self.suite, self.sources, ROOT)

    def test_exact_corrected_public_suite_passes_d02_and_d03(self):
        try: self.d02._suite(self.suite, self.sources, self.reviews, ROOT, self.a.validate_suite)
        except ValueError as error: self.fail('Exact metadata suite rejected: ' + str(error))
        self.assertEqual(len(self.suite['source_ids']), 109)
        self.assertEqual(len(self.suite['replay']['files']), 107)
        self.assertEqual(self.suite['replay'], self.old['replay'])

    def test_actual_public_wrapper_passes_without_new_measurements(self):
        try: self.d02._receipt(self.receipt, self.suite, self.sources, self.reviews, ROOT, self.a.validate_receipt)
        except ValueError as error: self.fail('Exact public wrapper rejected: ' + str(error))
        self.d02._public_values(self.receipt)
        self.assertEqual(len(self.receipt['source_hashes']), 109)
        self.assertEqual(len(self.prior['replay_evidence']['source_hashes_before']), 107)
        self.assertEqual(len(self.prior['replay_evidence']['source_inventory_before']['g1']), 127)

    def test_bool_or_nonzero_accounting_is_rejected(self):
        for key in ['new_processes','new_builds','new_audits','new_independence']:
            for value in [False, 0.0, 1]:
                changed = copy.deepcopy(self.receipt); changed['replay_evidence']['accounting'][key] = value
                with self.subTest(key=key,value=value), self.assertRaises(ValueError): self.check(changed)

    def test_swapped_membership_and_changed_prior_are_rejected(self):
        swapped = copy.deepcopy(self.receipt); swapped['replay_evidence']['membership'].reverse()
        with self.assertRaises(ValueError): self.check(swapped)
        changed = copy.deepcopy(self.receipt)
        old = changed['replay_evidence']['prior']['receipt']; old['replay_evidence']['source_hashes_before'] = {}
        changed['replay_evidence']['prior']['receipt_canonical_sha256'] = self.a.canonical(old)
        with self.assertRaises(ValueError): self.check(changed)

    def test_naive_raw_relabel_and_changed_execution_fields_are_rejected(self):
        changed = copy.deepcopy(self.prior); changed['suite_sha256'] = self.a.canonical(self.suite)
        changed['source_hashes'] = self.receipt['source_hashes']
        with self.assertRaises(ValueError): self.check(changed)
        changed = copy.deepcopy(self.receipt); changed['exit_code'] = False
        with self.assertRaises(ValueError): self.check(changed)

    def test_view_and_near_matches_refuse_effects(self):
        cases = [self.suite]
        near = copy.deepcopy(self.suite); near['source_ids'].reverse(); cases.append(near)
        near = copy.deepcopy(self.suite); near['targets'][0]['target_sha256'] = '0'*64; cases.append(near)
        scratch = os.environ.get('G1_MEMBERSHIP_TEST_SCRATCH')
        with tempfile.TemporaryDirectory(dir=scratch) as directory:
            output = Path(directory) / 'absent'
            for suite in cases:
                with self.subTest(digest=self.a.canonical(suite)), mock.patch.object(Path, 'mkdir', side_effect=AssertionError('No output creation')):
                    with self.assertRaises(ValueError): self.a.project_suite(suite, self.sources, ROOT, output)
                    with self.assertRaises(ValueError): self.a.execute_suite(suite, self.sources, ROOT, output, {}, {}, reviews=self.reviews)
            self.assertFalse(output.exists())

    def test_original_descriptor_route_and_raw_receipt_are_unchanged(self):
        self.assertTrue(callable(getattr(self.a, 'g1_membership_load', None)))
        old = self.a.g1_membership_load().original_replay_suite(adapter=self.a)
        self.assertEqual(self.a.canonical(old), 'b6ba8c2ceb6b645ed6d1f33162eb872d87f369d2ed342b3514a771ab35895a91')
        self.a.validate_suite(old, self.sources, ROOT)
        self.d02._receipt(self.prior, old, self.sources, self.reviews, ROOT, self.a.validate_receipt)

    def test_malformed_metadata_cannot_override_legacy_guards(self):
        for key, value in [('schema', []), ('schema', {}), ('provenance','FRESH_EXECUTION'), ('trust',True)]:
            changed = copy.deepcopy(self.receipt); changed['replay_evidence'][key] = value
            with self.subTest(key=key,value=value), self.assertRaises(ValueError): self.check(changed)

if __name__ == '__main__': unittest.main(verbosity=2)
