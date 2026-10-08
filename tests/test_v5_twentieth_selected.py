"""Frozen T20 selected-source admission has no implied fresh-science promotion."""
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

EXPECTED = {
    'T20-CHURCH-RAW-PROBE', 'T20-CND-ESSENTIALITY-SCOPE', 'T20-SCALAR-FUSION-IFF',
    'T20-MODAL-CROSSING-COMPLETENESS', 'T20-ORIGINAL-GROUND-ROBUSTNESS',
    'T20-GROUNDED-CONTINUATION-SUPPORT', 'T20-HASE-FURTHER-FAILED-ROUTES',
    'T20-TYPED-ORIGINAL-BEARER-ABC', 'T20-ANCHORED-FIELD-SOURCE',
    'T20-VERACITY-DEPENDENCY-AUDIT', 'T20-PTS-NORMALIZATION-TRANSFER',
    'T20-TRACE-OBSERVATION-COPYING', 'T20-JOINT-SAME-BEARER-MODEL',
    'T20-CONTROLLER-COMPLETENESS-TRANSFER', 'T20-FOUNDATIONAL-PREMISE-SYNTHESIS',
}

PREPARED_PINS = [
    ('RESULT_STATUS', 'results', 246, '1a5e8243d736b8afb86bc2bf783fbc96a2a43ea34ec8c1fb5c56e5b97bd68b1d'),
    ('RESULT_STATUS', 'statuses', 246, '12f76060f17747f515744c0c461c37b8d7c33564c8a2c601ef42ba96dd958249'),
    ('SOURCE_MAP', 'sources', 3128, 'b6e626db528ec54526c65b48643559312f877d749106255c9fc01fb21be2a566'),
    ('SOURCE_MAP', 'reviews', 264, 'fba35f5e6e76604045267965833e2bb97804473046e73d26a7af8f0722c9a2a7'),
    ('EVIDENCE_BINDINGS', 'bindings', 246, 'c81a5ddb05d0ca8d33a3c8010fa2a45d20d6d51557bcbb3d03dd4c1541558ac4'),
    ('EVIDENCE_BINDINGS', 'receipts', 44, '1ad72bc882d7a7f140c8483f72cf7d6d6c2521632f67a3511ba91b343726ccf2'),
    ('CALCULUS_MAP', 'results', 246, '1e90798fe4bbae8f9d8d729c4fd885fc49cf8686b05a6d2c01d6de7a2c812d67'),
    ('PUBLIC_PROJECTION', 'reviews', 24, 'f70a9bacecb142196f1adbdbefedc37448d92a9436dd6db99505389e10941a2b'),
    ('SUPERSESSION', 'selectors', 244, '1fed7fc8ffb0d0502ef9b6c9bbec6596743a60399a6e661773982aa86439feb2'),
]


def read(name):
    return json.loads((PROV / (name + '.json')).read_text())


class TwentiethSelectedTests(unittest.TestCase):
    def test_prepared_predecessor_rows_keep_their_exact_identities(self):
        for document, key, count, checksum in PREPARED_PINS:
            with self.subTest(document=document, field=key):
                rows = read(document)[key][:count]
                self.assertEqual(validator.canonical_json_digest(rows), checksum)

    def test_selected_results_are_present_without_private_inventory_placeholder(self):
        rows = {r['id']: r for r in read('RESULT_STATUS')['results']}
        self.assertTrue(EXPECTED <= rows.keys(), sorted(EXPECTED - rows.keys()))
        self.assertNotIn('T20-GLOBAL-PLENITUDE-APPRAISAL', rows)

    def test_selected_native_science_remains_not_run(self):
        rows = {r['id']: r for r in read('RESULT_STATUS')['results']}
        statuses = {r['id']: r for r in read('RESULT_STATUS')['statuses']}
        self.assertTrue(EXPECTED <= statuses.keys(), sorted(EXPECTED - statuses.keys()))
        for rid in EXPECTED:
            with self.subTest(result=rid):
                self.assertEqual(statuses[rid]['fresh_evidence'], 'NOT_RUN')
                self.assertEqual(statuses[rid]['receipt_ids'], [])
                self.assertEqual(statuses[rid]['independent_evidence_count'], 0)
                self.assertEqual(rows[rid]['suite_ids'], [])
                self.assertEqual(statuses[rid]['research_disposition'], 'CANDIDATE')

    def test_effective_selection_has_exact_content_and_no_duplicate_historical_recipe(self):
        index_path = GROUP / 'SOURCE_INDEX.json'
        self.assertTrue(index_path.is_file(), 'The finite selected-source index is missing')
        index = json.loads(index_path.read_text())
        self.assertEqual(index['selection_sha256'], '2ca55b442d41e8a70c1b550badef15c1dde403ee73e646c640b92d929558f6df')
        self.assertEqual(index['curation_seal_sha256'], '0fdbb585f265f071aa2a4a333d4cff0e1873a3b0e61131cb89360c25d2b3955f')
        self.assertEqual(len(index['selected_sources']), 410)
        keys = {(s['component'], s['logical_path']) for s in index['selected_sources']}
        self.assertEqual(len(keys), 410)
        sources = {s['id']: s for s in read('SOURCE_MAP')['sources']}
        for selected in index['selected_sources']:
            source = sources[selected['id']]
            raw = (ROOT / source['public_path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), selected['public_sha256'])
            self.assertEqual(len(raw), selected['public_bytes'])
            self.assertEqual(source['public_sha256'], selected['public_sha256'])
        self.assertEqual(len({s['public_sha256'] for s in index['selected_sources']}), 396)

    def test_actual_derivations_keep_diff_identities_without_private_diff_bodies(self):
        index_path = GROUP / 'SOURCE_INDEX.json'
        self.assertTrue(index_path.is_file(), 'The finite selected-source index is missing')
        selected = json.loads(index_path.read_text())['selected_sources']
        sources = {s['id']: s for s in read('SOURCE_MAP')['sources']}
        transformed = [sources[s['id']] for s in selected if s['registration_kind'] == 'ORIGINAL_TO_PUBLIC_DERIVATION']
        packaging = [sources[s['id']] for s in selected if s['registration_kind'] == 'NEW_AUTHORED_PACKAGING_INPUT']
        self.assertEqual(len(transformed), 73)
        self.assertEqual(len(packaging), 31)
        for source in transformed:
            self.assertEqual(source['projection'], 'DERIVED')
            self.assertIsNone(source['derivation']['diff_path'])
            self.assertNotEqual(source['original_sha256'], source['public_sha256'])
        for source in packaging:
            self.assertEqual(source['projection'], 'EXACT')
            self.assertEqual(source['original_sha256'], source['public_sha256'])
            self.assertIsNone(source['derivation'])

    def test_statement_bindings_match_scoped_new_rows(self):
        rows = {r['id']: r for r in read('RESULT_STATUS')['results']}
        bindings = {r['id']: r for r in read('EVIDENCE_BINDINGS')['bindings']}
        self.assertTrue(EXPECTED <= rows.keys(), sorted(EXPECTED - rows.keys()))
        for rid in EXPECTED:
            self.assertEqual(bindings[rid]['statement_sha256'], validator.canonical_json_digest(rows[rid]))
        for rid in ('T20-PTS-NORMALIZATION-TRANSFER', 'T20-CONTROLLER-COMPLETENESS-TRANSFER',
                    'T20-HASE-FURTHER-FAILED-ROUTES'):
            self.assertEqual(rows[rid]['math_form'], 'ORDINARY')
        self.assertIn('OPEN', rows['T20-SCALAR-FUSION-IFF']['residual_scope'])

    def test_current_synthesis_appraisal_is_separate_from_t19_history(self):
        rows = {r['id']: r for r in read('RESULT_STATUS')['results']}
        self.assertIn('T20-FOUNDATIONAL-PREMISE-SYNTHESIS', rows)
        row = rows['T20-FOUNDATIONAL-PREMISE-SYNTHESIS']
        self.assertEqual(row['math_form'], 'SOURCE_ASSESSMENT')
        self.assertIn('2026-10-07', row['conclusion'])
        self.assertIn('withholds', row['conclusion'])
        self.assertIn('T19', row['residual_scope'])
        self.assertIn('T19-COMMON-CONNECTED-SOURCE', rows)

    def test_final_assembly_keeps_acceptance_receipts_separate(self):
        path = GROUP / 'ASSEMBLY_STATE.json'
        self.assertTrue(path.is_file(), 'Partial assembly state is missing')
        state = json.loads(path.read_text())
        self.assertEqual(state['status'], 'LAST_FINITE_SUPPLIED_INPUTS_ASSEMBLED')
        self.assertEqual(state['native_final_gate'], 'CONSULT_SEPARATE_EXACT_TREE_OWNER_HANDOFF')
        self.assertEqual(state['whole_diff_independent_review'], 'CONSULT_SEPARATE_EXACT_TREE_OWNER_HANDOFF')
        self.assertEqual(state['fresh_clean_apply'], 'CONSULT_SEPARATE_EXACT_TREE_OWNER_HANDOFF')
        self.assertEqual(state['fresh_pdf_rebuild'], 'BLOCKED_EXACT_DOCKER_POPPLER_ENVIRONMENT')


if __name__ == '__main__':
    unittest.main()
