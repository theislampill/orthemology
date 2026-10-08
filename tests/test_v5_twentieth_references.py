"""New data retains narrowly digest-bound original/external member semantics."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import validate_internal_references as references
import validate_repo as repository


class TwentiethReferenceTests(unittest.TestCase):
    def setUp(self):
        self.owner = 'docs/provenance/v5-successors/EVIDENCE_BINDINGS.json'
        self.text = (ROOT / self.owner).read_text(encoding='utf-8')
        self.members = {'tests/' + name for name in (
            'test_criterion_model.py', 'test_replay.py', 'test_rule_installation.py')}

    def test_exact_current_binding_retains_only_the_three_original_members(self):
        self.assertEqual(references._original_driver_members(self.owner, self.text), self.members)

    def test_changed_binding_cannot_borrow_original_member_exception(self):
        self.assertEqual(references._original_driver_members(self.owner, self.text + ' '), set())

    def test_same_text_elsewhere_cannot_borrow_owner_exception(self):
        self.assertEqual(references._original_driver_members('docs/' + 'ordinary.json', self.text), set())


class TwentiethDependencyInventoryTests(unittest.TestCase):
    def inventories(self):
        sources = json.loads((ROOT / 'docs/provenance/v5-successors/SOURCE_MAP.json').read_text())['sources']
        for checksum in ('f461e480570d88a8b438fc332b6f3327216df187dedd09c979d47bedbaaa3bba',
                         '8e121ae7ace129ad9270db82ab6682609f5fec12a0d2de4fe567cf8898d6f039'):
            owner = next(s for s in sources if s['public_sha256'] == checksum)
            yield owner, json.loads((ROOT / owner['public_path']).read_text())

    def test_exact_dependency_inventory_has_only_its_declared_external_files(self):
        for owner, document in self.inventories():
            with self.subTest(owner=owner['id']):
                self.assertEqual(set(repository._locked_external_files(document, owner) or {}),
                                 {r['path'] for r in document})

    def test_reference_scan_uses_exact_list_inventory_owner(self):
        for owner, document in self.inventories():
            text = (ROOT / owner['public_path']).read_text()
            cited = lambda src, body: {name for name, _ in references._citation_occurrences(
                src, body, root=ROOT, successor_sources=[owner])}
            external = {r['path'] for r in document if r['path'].startswith('docs/')}
            self.assertTrue(external)
            self.assertFalse(cited(owner['public_path'], text) & external)
            self.assertTrue(cited('docs/' + 'ordinary.json', text) & external)
            changed = deepcopy(document); changed[0]['sha256'] = '0' * 64
            self.assertTrue(cited(owner['public_path'], json.dumps(changed)) & external)

    def test_changed_inventory_or_owner_cannot_borrow_the_external_scope(self):
        for owner, document in self.inventories():
            with self.subTest(owner=owner['id']):
                changed = deepcopy(document); changed[0]['path'] = '../missing.py'
                self.assertIsNone(repository._locked_external_files(changed, owner))
                wrong_owner = deepcopy(owner); wrong_owner['public_sha256'] = '0' * 64
                self.assertIsNone(repository._locked_external_files(document, wrong_owner))


if __name__ == '__main__':
    unittest.main()
