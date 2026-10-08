"""One bounded late interpretation result; prior owners and source seals survive."""
import hashlib
import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROV = ROOT / 'docs/provenance/v5-successors'
GROUP = ROOT / 'experiments/orthemology-v5-successors/groups/t20-successor'
sys.path.insert(0, str(ROOT / 'scripts'))
import validate_v5_successors as validator
LATE = 'T20-EMERGENCE-TYPE-CONTROL'


def read(name):
    return json.loads((PROV / (name + '.json')).read_text())


class TwentiethLateAppendTests(unittest.TestCase):
    def test_one_narrow_late_owner_is_added_without_inflating_old_rows(self):
        results = read('RESULT_STATUS')['results']
        rows = {r['id']: r for r in results}
        self.assertTrue(LATE in rows, 'The bounded late owner is missing')
        self.assertEqual(len(results), 262)
        self.assertEqual(sum(r['tranche'] == 20 for r in results), 16)
        row = rows[LATE]
        self.assertEqual(row['claim_scope'], 'COMPONENT')
        self.assertEqual(row['math_form'], 'FORMAL')
        self.assertEqual(row['domain'], 'UNBOUNDED_MODEL')
        self.assertEqual(row['calculus'], 'OTHER')
        self.assertIn('chosen', row['conclusion'].lower())
        self.assertIn('metaphysical', row['residual_scope'])

    def test_all_existing_results_and_statuses_are_exactly_preserved(self):
        document = read('RESULT_STATUS')
        history = read('T20_CONTEXT_REAPPRAISAL_HISTORY')['snapshots']
        historical = [history[r['id']]['prior_result'] if r['id'] in history else r
                      for r in document['results'][:261]]
        self.assertEqual(validator.canonical_json_digest(historical),
                         '578b86ea0281050288472f0d0d3d98dcde98a4830987c79aaf8a52470f9053c1')
        self.assertEqual(validator.canonical_json_digest(document['statuses'][:261]),
                         '69f499ce50ec66cfbc3e8979a0c3e6fc5408fcceb1b879b04ce5fb14f0d46f94')

    def test_late_original_research_is_not_a_native_receipt(self):
        rows = {r['id']: r for r in read('RESULT_STATUS')['statuses']}
        self.assertTrue(LATE in rows, 'The bounded late owner is missing')
        status = rows[LATE]
        self.assertEqual(status['fresh_evidence'], 'NOT_RUN')
        self.assertEqual(status['inherited_evidence'], 'KERNEL_COMPONENTS')
        self.assertEqual(status['receipt_ids'], [])
        self.assertEqual(status['independent_evidence_count'], 0)
        self.assertEqual(len(read('EVIDENCE_BINDINGS')['receipts']), 44)

    def test_frozen_reader_index_is_not_rewritten_as_latest_selection(self):
        old = GROUP / 'READING_REPORT_INDEX.json'
        self.assertEqual(hashlib.sha256(old.read_bytes()).hexdigest(), 'd7019c0d287c8570735983fb0dd7c8f53db9f6ad615adee967e067bd7e9a8135')
        path = GROUP / 'FINAL_SOURCE_INDEX.json'
        self.assertTrue(path.is_file(), 'Combined final finite source lookup is missing')
        index = json.loads(path.read_text())
        previous = json.loads(old.read_text())
        self.assertEqual(index['public_sources'][:212], previous['public_sources'])
        self.assertEqual(len(index['public_sources']), 265)
        self.assertEqual(len(index['owner_only_documents']), 5)

    def test_new_statement_is_bound_to_real_selected_sources(self):
        rows = {r['id']: r for r in read('RESULT_STATUS')['results']}
        self.assertTrue(LATE in rows, 'The bounded late owner is missing')
        row = rows[LATE]
        sources = {r['id']: r for r in read('SOURCE_MAP')['sources']}
        binding = next(r for r in read('EVIDENCE_BINDINGS')['bindings'] if r['id'] == LATE)
        self.assertEqual(binding['statement_sha256'], validator.canonical_json_digest(row))
        old = read('T20_CONTEXT_REAPPRAISAL_HISTORY')['snapshots'][LATE]['prior_result']
        self.assertEqual(len(old['source_ids']), 19)
        self.assertTrue(set(old['source_ids']) < set(row['source_ids']))
        self.assertTrue(all(sid in sources for sid in row['source_ids']))
        self.assertEqual(row['suite_ids'], [])
        self.assertIn('temporal', row['residual_scope'].lower())


    def test_context_append_preserves_exact_checkpoint_records(self):
        history = read('T20_CONTEXT_REAPPRAISAL_HISTORY')
        expected = {'T20-FOUNDATIONAL-PREMISE-SYNTHESIS', LATE}
        self.assertEqual(set(history['snapshots']), expected)
        self.assertEqual(history['prior_candidate_tree'], 'fadbecadf440641d117d9eabb44faf2fae2ceab4')
        results = read('RESULT_STATUS')['results']
        restored = [history['snapshots'][r['id']]['prior_result'] if r['id'] in expected else r for r in results]
        self.assertEqual(validator.canonical_json_digest(restored), '9429cf85e341ff9e0fdae3bc0edcd3e48f10049210ae0f343b1ca8e3e9cf6e1c')
        self.assertEqual(validator.canonical_json_digest(read('RESULT_STATUS')['statuses']), '88e381ec7e11297385dbb5751a47b7016402b495618fa2d7098917d1c2ce237c')
        for document, key, count, checksum in [
            ('SOURCE_MAP', 'sources', 3806, '94fb2ef0d0573ec08e1dc96117feb5ddb3f3e595df6c39b0429e4e65ec75fb8b'),
            ('SOURCE_MAP', 'reviews', 281, '41b256972eb00035bf78d0831913e9e372782a0caaabdd399f620302047d58bb'),
            ('PUBLIC_PROJECTION', 'reviews', 324, 'caace4629fc92f38b5b0fa23bc72390de4b05c81a27d49b86e7865a36f0f2ad1'),
            ('EVIDENCE_BINDINGS', 'receipts', 44, '1ad72bc882d7a7f140c8483f72cf7d6d6c2521632f67a3511ba91b343726ccf2'),
        ]:
            self.assertEqual(validator.canonical_json_digest(read(document)[key][:count]), checksum)
        for rid, snapshot in history['snapshots'].items():
            self.assertEqual(snapshot['prior_binding']['statement_sha256'], validator.canonical_json_digest(snapshot['prior_result']))
            self.assertEqual(snapshot['prior_selector']['statement_sha256'], snapshot['prior_binding']['statement_sha256'])
            self.assertEqual(snapshot['prior_status'], next(s for s in read('RESULT_STATUS')['statuses'] if s['id'] == rid))
        current = {r['id']: r for r in results}
        self.assertEqual(current[LATE]['conclusion'], history['snapshots'][LATE]['prior_result']['conclusion'])
        for rid in expected:
            before = history['snapshots'][rid]['prior_result']
            allowed = {'source_ids', 'evidence_keys', 'review_ids', 'limitations', 'residual_scope'}
            if rid != LATE:
                allowed.add('conclusion')
            self.assertEqual({k:v for k,v in before.items() if k not in allowed},
                             {k:v for k,v in current[rid].items() if k not in allowed})

    def test_context_sources_are_finite_and_do_not_add_results_or_science(self):
        index = json.loads((GROUP / 'CONTEXT_SOURCE_INDEX.json').read_text())
        prior = json.loads((GROUP / 'FINAL_SOURCE_INDEX.json').read_text())
        self.assertEqual(hashlib.sha256((GROUP / 'FINAL_SOURCE_INDEX.json').read_bytes()).hexdigest(),
                         'a55268b34f64fc40700afe2a3d4a525a57d2ae3101e261a3da23e0a59dc23d41')
        self.assertEqual(index['public_sources'][:265], prior['public_sources'])
        self.assertEqual(index['owner_only_documents'], prior['owner_only_documents'])
        self.assertEqual(len(index['public_sources']), 286)
        self.assertEqual(index['layers'][-1]['selection_sha256'], '00bf802818563d942f047401fe6d9eed8b2c2cf1ea9f91a03c576783aa45adc4')
        self.assertEqual(len(read('SOURCE_MAP')['sources']), 3828)
        self.assertEqual(len(read('RESULT_STATUS')['results']), 262)
        rows = {r['id']: r for r in read('RESULT_STATUS')['results']}
        self.assertIn('No full-premise countermodel', rows['T20-FOUNDATIONAL-PREMISE-SYNTHESIS']['residual_scope'])
        self.assertIn('P2b', rows['T20-FOUNDATIONAL-PREMISE-SYNTHESIS']['residual_scope'])
        self.assertIn('global inactivity', rows[LATE]['residual_scope'])
        self.assertIn('per-kind', rows[LATE]['residual_scope'])
        for rid in ('T20-FOUNDATIONAL-PREMISE-SYNTHESIS', LATE):
            row = rows[rid]
            binding = next(b for b in read('EVIDENCE_BINDINGS')['bindings'] if b['id'] == rid)
            self.assertEqual(binding['statement_sha256'], validator.canonical_json_digest(row))
            self.assertEqual(set(binding['sources']), set(row['source_ids']))
            self.assertEqual(set(binding['reviews']), set(row['review_ids']))
            self.assertEqual(binding['receipts'], {})
            self.assertEqual(row['suite_ids'], [])


if __name__ == '__main__':
    unittest.main()
