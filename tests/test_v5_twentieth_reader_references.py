"""Only sealed finite owner-reader aliases can resolve archive-context links."""
from copy import deepcopy
import json
import re
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
INDEX = 'experiments/orthemology-v5-successors/groups/t20-successor/CONTEXT_SOURCE_INDEX.json'
sys.path.insert(0, str(ROOT / 'scripts'))
import validate_repo as repository


class TwentiethReaderReferenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.sources = json.loads((ROOT / 'docs/provenance/v5-successors/SOURCE_MAP.json').read_text())['sources']
        self.index = json.loads((ROOT / INDEX).read_text())
        self.owner = next(s for s in self.index['public_sources'] if s['owner_archive_path'] == 't20/reading/GUIDE.md')
        self.target = next(s for s in self.index['public_sources'] if s['owner_archive_path'] == 't20/reading/READING_INDEX.json')
        for rel in [INDEX, self.owner['public_path'], self.target['public_path']]:
            target = self.root / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / rel, target)

    def resolves(self, target='READING_INDEX.json', sources=None, owner=None):
        return repository.successor_packet_locator(
            self.root / (owner or self.owner['public_path']), target,
            self.sources if sources is None else sources, self.root)

    def test_exact_owner_and_target_resolve_in_declared_reader_context(self):
        self.assertTrue(self.resolves())

    def test_new_context_link_to_old_reader_requires_both_exact_identities(self):
        owner = next(s for s in self.index['public_sources'] if s['owner_archive_path'] == 't20/final-context-audit/CONTEXT_SCOPE.md')
        target = next(s for s in self.index['public_sources'] if s['owner_archive_path'] == 't20/reading/assessments/ROOT_CURRENT_APPRAISAL_20261007_143400.md')
        for row in (owner, target):
            path = self.root / row['public_path']
            path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / row['public_path'], path)
        markdown = (self.root / owner['public_path']).read_text()
        link = re.search(r'\]\(([^)]*ROOT_CURRENT_APPRAISAL_20261007_143400\.md)\)', markdown).group(1)
        def resolves():
            return repository.successor_packet_locator(self.root / owner['public_path'],
                link, self.sources, self.root)
        self.assertTrue(resolves())
        self.assertFalse(repository.successor_packet_locator(self.root / owner['public_path'],
            target['owner_archive_path'], self.sources, self.root))
        (self.root / target['public_path']).write_bytes(b'changed target')
        self.assertFalse(resolves())

    def test_changed_owner_bytes_do_not_borrow_alias_identity(self):
        path = self.root / self.owner['public_path']
        path.write_bytes(path.read_bytes() + b' ')
        self.assertFalse(self.resolves())

    def test_changed_or_missing_target_bytes_do_not_resolve(self):
        path = self.root / self.target['public_path']
        path.write_bytes(path.read_bytes() + b' ')
        self.assertFalse(self.resolves())
        path.unlink()
        self.assertFalse(self.resolves())

    def test_changed_owner_record_or_duplicate_owner_does_not_resolve(self):
        sources = deepcopy(self.sources)
        owner = next(s for s in sources if s['id'] == self.owner['id'])
        owner['origin_input_id'] += '-changed'
        self.assertFalse(self.resolves(sources=sources))
        sources = deepcopy(self.sources)
        sources.append(deepcopy(next(s for s in sources if s['id'] == self.owner['id'])))
        self.assertFalse(self.resolves(sources=sources))

    def test_missing_or_modified_alias_index_does_not_resolve(self):
        index = self.root / INDEX
        changed = deepcopy(self.index)
        changed['public_sources'] = [s for s in changed['public_sources'] if s['id'] != self.target['id']]
        index.write_text(json.dumps(changed))
        self.assertFalse(self.resolves())
        index.unlink()
        self.assertFalse(self.resolves())

    def test_same_bytes_under_another_owner_do_not_resolve(self):
        other = 'docs/' + 'ordinary-reader.md'
        path = self.root / other
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(self.root / self.owner['public_path'], path)
        self.assertFalse(self.resolves(owner=other))

    def test_missing_escaping_and_unselected_targets_stay_unresolved(self):
        for target in ('not-selected.json', '../../../../outside.md', '/outside.md',
                       'unselected-source-body.pdf', 'READING_INDEX.json/../not-selected.json'):
            with self.subTest(target=target):
                self.assertFalse(self.resolves(target))

    def test_symlink_target_cannot_borrow_selected_bytes(self):
        target = self.root / self.target['public_path']
        other = self.root / 'unbound-target.json'
        target.rename(other)
        target.symlink_to(other)
        self.assertFalse(self.resolves())


if __name__ == '__main__':
    unittest.main()
