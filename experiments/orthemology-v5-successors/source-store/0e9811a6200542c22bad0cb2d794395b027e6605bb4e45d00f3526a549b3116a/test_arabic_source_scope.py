"""Consistency of published reading-scope metadata; no primary-source reading."""
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

def expand(ranges):
    return {n for a, b in ranges for n in range(a, b + 1)}

class AdditionalArabicScopeChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((ROOT / 'sources/additional_arabic_source_scope.json').read_text(encoding='utf-8'))

    def test_source_identity_and_exclusions(self):
        d = self.record
        self.assertEqual(d['source']['sha256'], 'f3855f50414e18100e28d6d64e4367f9fe9fc6f1915a077b91c204be43a96333')
        self.assertEqual(d['source']['pdf_page_count'], 938)
        self.assertEqual(d['source']['bytes'], 18364577)
        self.assertIs(d['whole_scan_read'], False)
        self.assertIs(d['original_manuscripts_inspected'], False)
        self.assertIs(d['included_primary_text_or_images'], False)

    def test_exact_bounded_page_union(self):
        d = self.record
        union = set()
        for r in d['continuous_main_text_reads']:
            ps = expand([r['pdf_range']])
            self.assertEqual(len(ps), r['pages'])
            self.assertEqual(r['pdf_range'], [n + 100 for n in r['printed_range']])
            self.assertRegex(r['reading_receipt_sha256'], r'^[0-9a-f]{64}$')
            union |= ps
        self.assertEqual(union, expand(d['unique_main_text_pdf_ranges']))
        self.assertEqual(len(union), 78)
        self.assertEqual(d['unique_main_text_pdf_pages'], 78)
        c = d['separately_bounded_context_reads']
        context = set(c['title_and_imprint_pdf_pages'] + c['table_of_contents_pdf_pages']) | expand(c['introductory_witness_and_editorial_context_pdf_ranges'])
        self.assertEqual(len(context), c['unique_context_pdf_pages'])
        self.assertEqual(len(context), 17)
        self.assertFalse(union & context)
        self.assertFalse((union | context) & set(c['navigation_only_not_credited_pdf_pages']))
        self.assertFalse((union | context) & expand(c['rendered_but_unseen_not_credited_pdf_ranges']))

    def test_separate_supplied_pdf_record(self):
        d = self.record['six_supplied_pdf_coverage_relation']
        p = ROOT / d['metadata_file']
        import hashlib
        self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), d['metadata_sha256'])
        supplied = json.loads(p.read_text(encoding='utf-8'))
        self.assertEqual(len(supplied['sources']), 6)
        self.assertEqual(supplied['total_supplied_pdf_pages'], 1393)
        self.assertEqual(sum(s['pdf_page_count'] for s in supplied['sources']), 1393)
        self.assertNotIn(self.record['source']['sha256'], [s['source_sha256'] for s in supplied['sources']])
        self.assertIs(d['unchanged'], True)

    def test_printed_witness_distinction(self):
        d = self.record['edition_and_manuscript_distinction']
        self.assertIn('printed edition, not a manuscript', d['kaf'])
        self.assertIn('Neither original witness was independently inspected', d['qualification'])
        self.assertIn('399–450', d['sad'])

if __name__ == '__main__':
    unittest.main()
