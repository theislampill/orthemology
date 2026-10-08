"""Additive source admission and exact preservation controls at the PR-30 base."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
BASE = 'fd0903d99d657c35e32fddcc8864d2a77930cf40'
PROV = 'docs/provenance/v5-successors/'
sys.path.insert(0, str(ROOT / 'scripts'))
import validate_v5_successors as validator


def read(name):
    return json.loads((ROOT / (PROV + name + '.json')).read_text())


def original(name):
    return json.loads(subprocess.check_output(['git', 'show', BASE + ':' + PROV + name + '.json'], cwd=ROOT))


def indexed(rows):
    return {r['id']: r for r in rows}


class TwentiethDataTests(unittest.TestCase):
    def test_earlier_scientific_and_review_records_are_unchanged(self):
        for name, keys in {
            'SOURCE_MAP': ('sources', 'reviews'),
            'RESULT_STATUS': ('statuses',),
            'EVIDENCE_BINDINGS': ('receipts',),
            'CALCULUS_MAP': ('results',),
            'PUBLIC_PROJECTION': ('reviews',),
        }.items():
            for key in keys:
                current = indexed(read(name)[key])
                for old in original(name)[key]:
                    with self.subTest(document=name, field=key, id=old['id']):
                        self.assertEqual(current[old['id']], old)

    def test_only_two_authorised_prior_conclusions_change(self):
        corrections = read('T20_FIDELITY_CORRECTIONS')['corrections']
        self.assertEqual({r['result_id'] for r in corrections}, {'T16-CORE-ASSURANCE', 'T16-OCCURRENCE'})
        changes = {r['result_id']: r for r in corrections}
        current = indexed(read('RESULT_STATUS')['results'])
        for old in original('RESULT_STATUS')['results']:
            expected = dict(old)
            if old['id'] in changes:
                correction = changes[old['id']]
                self.assertEqual(correction['prior_result'], old)
                self.assertEqual(correction['old_conclusion'], old['conclusion'])
                expected['conclusion'] = correction['new_conclusion']
            self.assertEqual(current[old['id']], expected)

    def test_old_binding_changes_are_limited_to_corrected_statement_hashes(self):
        current = indexed(read('EVIDENCE_BINDINGS')['bindings'])
        results = indexed(read('RESULT_STATUS')['results'])
        for old in original('EVIDENCE_BINDINGS')['bindings']:
            expected = dict(old)
            if old['id'] in {'T16-CORE-ASSURANCE', 'T16-OCCURRENCE'}:
                expected['statement_sha256'] = validator.canonical_json_digest(results[old['id']])
            self.assertEqual(current[old['id']], expected)

    def test_prior_sources_and_suites_preserved_with_authorized_navigation(self):
        authored_navigation = {
            'docs/provenance/v5-successors/README.md',
            'experiments/orthemology-v5-successors/README.md',
        }
        current = {r['path']: r for r in read('PUBLIC_PROJECTION')['allowlist']}
        for old in original('PUBLIC_PROJECTION')['allowlist']:
            path = ROOT / old['path']
            expected = old
            if old['path'] in authored_navigation:
                self.assertEqual(old['kind'], 'AUTHORED')
                self.assertEqual(old['source_ids'], [])
                expected = current[old['path']]
                self.assertEqual(expected['kind'], 'AUTHORED')
                self.assertEqual(expected['source_ids'], [])
            self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), expected['sha256'])
            self.assertEqual(path.stat().st_size, expected['bytes'])
        registry_path = 'experiments/orthemology-v5-successors/registry.json'
        before = json.loads(subprocess.check_output(['git', 'show', BASE + ':' + registry_path], cwd=ROOT))
        after = json.loads((ROOT / registry_path).read_text())
        self.assertEqual(after['suite_ids'], before['suite_ids'])
        for sid in before['suite_ids']:
            self.assertEqual(after['records']['suite:' + sid], before['records']['suite:' + sid])

    def test_all_thirty_t17_t19_rows_preserve_inherited_not_run(self):
        results = [r for r in read('RESULT_STATUS')['results'] if 17 <= r['tranche'] <= 19]
        self.assertEqual(len(results), 30)
        statuses = indexed(read('RESULT_STATUS')['statuses'])
        for row in results:
            status = statuses[row['id']]
            self.assertEqual(status['fresh_evidence'], 'NOT_RUN')
            self.assertEqual(status['independent_evidence_count'], 0)
            self.assertEqual(status['receipt_ids'], [])
            self.assertEqual(row['suite_ids'], [])
            self.assertTrue(row['review_ids'])

    def test_nine_reviewed_document_projections_are_bound(self):
        sources = read('SOURCE_MAP')['sources']
        docs = [s for s in sources if s['origin_input_id'] in {
            'T17-REPORT', 'T17-COMPANION', 'T17-SOURCE-GUIDE',
            'T18-REPORT', 'T18-COMPANION', 'T18-SOURCE-GUIDE',
            'T19-REPORT', 'T19-SOURCE-GUIDE', 'T19-READING-INDEX'}]
        self.assertEqual(len(docs), 9)
        reviews = indexed(read('PUBLIC_PROJECTION')['reviews'])
        for source in docs:
            self.assertEqual(source['projection'], 'DERIVED')
            review = reviews[source['derivation']['review_id']]
            self.assertEqual(review['outcome'], 'CONTENT_REVIEWED')
            self.assertEqual(review['public_sha256'], source['public_sha256'])

    def test_t18_absolute_rejection_sentinel_is_only_reviewed_change(self):
        sources = read('SOURCE_MAP')['sources']
        source = next((s for s in sources if s['origin_input_id'] == 'T18-EVIDENCE'
            and s['member_chain'][-1].endswith('code-evidence/tests/test_replay_contract.py')), None)
        self.assertIsNotNone(source)
        self.assertEqual(source['projection'], 'DERIVED')
        public = (ROOT / source['public_path']).read_bytes()
        diff = json.loads((ROOT / source['derivation']['diff_path']).read_text())
        self.assertEqual(len(diff['edits']), 1)
        edit = diff['edits'][0]
        self.assertEqual(edit['insert_utf8'], '/outside')
        start = edit['offset_bytes']; replacement = edit['insert_utf8'].encode()
        self.assertEqual(public[start:start + len(replacement)], replacement)
        restored = public[:start] + bytes.fromhex(edit['delete_utf8_hex']) + public[start + len(replacement):]
        self.assertEqual(hashlib.sha256(restored).hexdigest(), source['original_sha256'])
        self.assertEqual(len(restored), source['original_bytes'])
        with self.assertRaises(ValueError):
            validator.check_public_text(restored.decode())
        validator.check_public_text(public.decode())


if __name__ == '__main__':
    unittest.main()
