"""Final reader-source addition preserves scientific and dated appraisal boundaries."""
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


def read(name):
    return json.loads((PROV / (name + '.json')).read_text())


class TwentiethAddendumTests(unittest.TestCase):
    def index(self):
        path = GROUP / 'READING_REPORT_INDEX.json'
        self.assertTrue(path.is_file(), 'Final sealed reading/report source index is missing')
        return json.loads(path.read_text())

    def test_only_the_finite_public_text_addendum_enters_source_store(self):
        index = self.index()
        self.assertEqual(index['owner_selected_files'], 215)
        self.assertEqual(len(index['public_sources']), 212)
        self.assertEqual(len(index['owner_only_documents']), 3)
        self.assertEqual(len({s['owner_archive_path'] for s in index['public_sources']}), 212)
        sources = {s['id']: s for s in read('SOURCE_MAP')['sources']}
        for item in index['public_sources']:
            source = sources[item['id']]
            raw = (ROOT / source['public_path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), item['public_sha256'])
            self.assertEqual(len(raw), item['public_bytes'])
            raw.decode('utf-8')
        admitted = {s['public_sha256'] for s in sources.values()}
        for doc in index['owner_only_documents']:
            self.assertTrue(doc['owner_archive_path'].endswith('.docx'))
            self.assertNotIn(doc['sha256'], admitted)

    def test_reading_and_packaging_add_no_results_or_execution_credit(self):
        index = self.index()
        self.assertEqual(index['result_count_before'], 261)
        self.assertEqual(index['result_count_after'], 261)
        results = read('RESULT_STATUS')
        self.assertEqual(len([r for r in results['results'] if r['id'] != 'T20-EMERGENCE-TYPE-CONTROL']), 261)
        for status in results['statuses']:
            if status['id'].startswith('T20-'):
                self.assertEqual(status['fresh_evidence'], 'NOT_RUN')
                self.assertEqual(status['receipt_ids'], [])
                self.assertEqual(status['independent_evidence_count'], 0)
        self.assertEqual(len(read('EVIDENCE_BINDINGS')['receipts']), 44)

    def test_final_appraisal_preserves_the_exact_earlier_assessment(self):
        path = PROV / 'T20_ASSESSMENT_HISTORY.json'
        self.assertTrue(path.is_file(), 'The prior assessment snapshot is missing')
        history = json.loads(path.read_text())
        old = history['prior_result']
        self.assertIn('08:40:48', old['conclusion'])
        self.assertIn('withholds sufficient warrant for the stronger common-source route', old['conclusion'])
        self.assertEqual(history['prior_binding']['statement_sha256'], validator.canonical_json_digest(old))
        current = next(r for r in read('RESULT_STATUS')['results'] if r['id'] == old['id'])
        context = read('T20_CONTEXT_REAPPRAISAL_HISTORY')
        dated = context['snapshots'][old['id']]['prior_result']
        self.assertIn('14:34', dated['conclusion'])
        self.assertIn('2026-10-07', current['conclusion'])
        self.assertIn('provisionally accepts', current['conclusion'])
        self.assertIn('universal SourceMode', current['conclusion'])
        self.assertIn('withholds', current['conclusion'])
        self.assertTrue(set(old['source_ids']) < set(current['source_ids']))
        self.assertTrue(set(old['review_ids']) < set(current['review_ids']))
        status = next(s for s in read('RESULT_STATUS')['statuses'] if s['id'] == old['id'])
        self.assertEqual(status, history['prior_status'])

    def test_json_lines_storage_names_preserve_the_five_owner_aliases(self):
        index = self.index()
        renamed = [row for row in index['public_sources'] if 'selected_storage_filename' in row]
        self.assertEqual(len(renamed), 5)
        for row in renamed:
            self.assertTrue(row['owner_archive_path'].endswith('.jsonl'))
            self.assertEqual(Path(row['public_path']).name, row['selected_storage_filename'] + '.txt')
            self.assertTrue(row['public_path'].endswith('.jsonl.txt'))
            self.assertEqual(hashlib.sha256((ROOT / row['public_path']).read_bytes()).hexdigest(), row['public_sha256'])

    def test_frozen_scientific_selection_stays_separate(self):
        index = self.index()
        frozen = json.loads((GROUP / 'SOURCE_INDEX.json').read_text())
        self.assertEqual(len(frozen['selected_sources']), 410)
        self.assertEqual(frozen['selection_sha256'], '2ca55b442d41e8a70c1b550badef15c1dde403ee73e646c640b92d929558f6df')
        self.assertEqual(index['scientific_baseline']['results'], 261)
        self.assertEqual(index['scientific_baseline']['sources'], 3539)
        self.assertFalse(set(r['id'] for r in frozen['selected_sources']) & set(r['id'] for r in index['public_sources']))


if __name__ == '__main__':
    unittest.main()
