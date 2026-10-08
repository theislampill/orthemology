"""Metadata consistency checks only. Hashes and page totals do not prove reading."""
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]

def expand(ranges):
    return [p for a,b in ranges for p in range(a,b+1)]

class SourceCoverageChecks(unittest.TestCase):
    def test_exact_coverage_and_visual_snapshot(self):
        d=json.loads((ROOT/'sources/six_source_coverage.json').read_text(encoding='utf-8'))
        self.assertEqual(len(d['sources']),6)
        self.assertEqual(sum(s['pdf_page_count'] for s in d['sources']),1393)
        self.assertEqual(sum(s['visual_coverage']['combined_count'] for s in d['sources']),190)
        for s in d['sources']:
            expected=list(range(1,s['pdf_page_count']+1))
            self.assertEqual(expand(s['exact_covered_pdf_ranges']),expected)
            credited=[p for c in s['coverage_contributions'] for p in expand(c['credited_pdf_ranges'])]
            self.assertEqual(sorted(credited),expected)
            self.assertEqual(len(set(credited)),len(credited))
            self.assertEqual(s['unique_credited_pdf_pages'],len(credited))
            self.assertEqual(s['missing_pdf_pages'],[])
            self.assertRegex(s['source_sha256'],r'^[0-9a-f]{64}$')
            self.assertTrue(s['actual_supplied_filename'].endswith('.pdf'))
            self.assertTrue(s['verified_supplied_drive_url'].startswith('https://drive.google.com/file/d/'))
            v=s['visual_coverage']
            self.assertEqual(sorted(set(v['reader_reported_pages'])|set(v['supplemental_auditor_pages'])),v['combined_pages'])
            self.assertEqual(len(v['combined_pages']),v['combined_count'])
            self.assertTrue(set(v['combined_pages']).issubset(expected))
            self.assertIs(v['every_page_visually_inspected'],False)
        repair=d['cover_gap_repair']
        self.assertEqual(repair['pdf_pages'],[1,403])
        self.assertIs(repair['resolved'],True)
        s=next(s for s in d['sources'] if s['source_alias']=='attributes_god')
        supplemental=[c for c in s['coverage_contributions'] if c['type']=='supplemental visual reading']
        self.assertEqual([p for c in supplemental for p in expand(c['credited_pdf_ranges'])],[1,403])
        self.assertIs(d['every_page_image_inspected'],False)
        self.assertIs(d['included_primary_text_or_images'],False)

if __name__ == '__main__':
    unittest.main()
