"""Electronic-source metadata controls, not new mathematics or primary reading."""
from pathlib import Path
import hashlib
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]

class MinhajElectronicScopeChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.record = json.loads((ROOT / 'sources/minhaj_electronic_read_scope.json').read_text(encoding='utf-8'))

    def test_exact_urls_and_bounded_body_ranges(self):
        d = self.record
        u5 = 'https://islamicbook.ws/tarekh/mnhaj-005.html'
        u6 = 'https://islamicbook.ws/tarekh/mnhaj-006.html'
        uw = 'https://ar.wikisource.org/wiki/منهاج_السنة_النبوية/20'
        self.assertEqual(d['source_urls'], [u5, u6, uw])
        groups = d['bounded_reading_groups']
        self.assertEqual(len(groups), 3)
        self.assertEqual([(r['url'], r['retrieved_body_lines_inclusive']) for r in groups[0]['reads']], [(u6, [108, 133]), (uw, [92, 178])])
        for group in groups[1:]:
            self.assertEqual([(r['url'], r['retrieved_body_lines_inclusive']) for r in group['reads']], [(u5, [350, 354]), (u6, [7, 21])])
        for group in groups:
            self.assertRegex(group['reading_receipt_sha256'], r'^[0-9a-f]{64}$')
            for r in group['reads']:
                self.assertRegex(r['bounded_capture_sha256'], r'^[0-9a-f]{64}$')
                self.assertGreater(r['bounded_capture_bytes'], 0)

    def test_printed_mapping_and_retrieval_limits(self):
        d = self.record
        self.assertEqual(d['print_mapping']['status'], 'CITATION_AND_SEARCH_DERIVED_NOT_PRINT_COLLATED')
        self.assertEqual(d['print_mapping']['reported_combined_page_range'], [321, 328])
        self.assertIs(d['print_mapping']['edition_specific_mapping_verified'], False)
        for key in ['included_primary_body_text_or_images', 'whole_work_read_claimed', 'printed_edition_collation_performed', 'manuscript_collation_performed', 'independent_witness_claimed', 'new_primary_reading_by_packaging', 'philosophical_disposition_included']:
            self.assertIs(d[key], False)
        self.assertIs(d['islamweb_retrieval_scope']['direct_body_read_credited'], False)
        self.assertEqual(d['islamweb_retrieval_scope']['reported_open_failures'], 2)
        self.assertIn('Tool/cache', d['islamweb_retrieval_scope']['failure_classification'])

    def test_earlier_coverage_snapshots_unchanged(self):
        snapshots = self.record['preserved_coverage_snapshots']
        self.assertEqual(len(snapshots), 2)
        for item in snapshots:
            p = ROOT / item['metadata_file']
            self.assertEqual(hashlib.sha256(p.read_bytes()).hexdigest(), item['sha256'])
            self.assertIs(item['unchanged'], True)
        self.assertEqual(snapshots[0]['supplied_pdf_pages'], 1393)
        self.assertEqual(snapshots[0]['supplied_pdf_count'], 6)
        self.assertEqual(snapshots[1]['additional_scan_pdf_pages'], 938)
        self.assertEqual(snapshots[1]['bounded_unique_main_text_pdf_pages'], 78)
        self.assertEqual(snapshots[1]['bounded_unique_context_pdf_pages'], 17)

    def test_exact_named_companion_document_bindings(self):
        d = json.loads((ROOT / 'RELATED_ARTIFACTS.json').read_text(encoding='utf-8'))
        self.assertEqual(d['status'], 'EXACT_NAMED_COMPANION_DOCUMENT_IDENTITIES')
        expected = [
            ('main_report', 'Orthemology_Seventeenth_Research_Final_v1_20261005.docx', '8cd31636e50ea255b5b630a16ad08cd7c6f79020aaad92ee6cd8f39c04d66608', 65239),
            ('source_guide', 'Orthemology_Seventeenth_Foundational_Source_Guide_Final_v1_20261005.docx', '6a923bf2d079f8bbf81f5736259a2299696185f0cd7bb5b2779ebd3ccb5ed3a9', 56611),
            ('mathematical_companion', 'Orthemology_Seventeenth_Mathematical_Companion_Final_v1_20261005.docx', '764c038e4cd2febb74c23e19c15cc86f6377c65f376964b3a33512a7ac83cf89', 45148),
        ]
        self.assertEqual([(x['role'], x['filename'], x['sha256'], x['bytes']) for x in d['documents']], expected)
        self.assertTrue(all(x['included_in_this_directory'] is False for x in d['documents']))
        source = d['companion_source']
        self.assertEqual(source['sha256'], '4e314f3943df0600fb2166031a696dd1d4a80e9afe407a58d7d9371447091401')
        self.assertEqual(hashlib.sha256((ROOT / source['path']).read_bytes()).hexdigest(), source['sha256'])
        relation = d['mathematical_companion_relationship']
        self.assertEqual(relation['publication_sha256'], expected[2][2])
        self.assertEqual(relation['preserved_predecessor_sha256'], '53506955a03bf7da8357c0cbb17e4caca5addb2a53bb163907d8e443afb8477a')
        self.assertEqual(relation['native_omml_objects_unchanged'], 398)
        self.assertEqual(relation['added_front_matter'], ['Prepared by dot, an AI assistant powered by OpenAI', '5 October 2026'])
        self.assertIs(relation['new_mathematical_result'], False)


if __name__ == '__main__':
    unittest.main()
