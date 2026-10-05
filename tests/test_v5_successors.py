"""Adversarial successor integrity and scope gates, entirely offline."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5_successor_fixtures import (AREA, PROV, OLD, OLDPROV, add_suite, digest,
    fixture_suite_validator, fixture_receipt_validator, make_bundle, put, put_bytes, raw_hash, rebind, save_bundle, source)

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/validate_v5_successors.py'


class SuccessorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if SCRIPT.exists():
            spec = importlib.util.spec_from_file_location('v5_successors', SCRIPT)
            cls.v = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.v)

    def setUp(self):
        self.assertTrue(SCRIPT.is_file(), 'Successor validator is not implemented')
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.bundle, self.anchor = make_bundle(self.root)

    def validate(self):
        save_bundle(self.root, self.bundle)
        return self.v.validate_bundle(self.bundle, self.root, baseline_anchor=self.anchor,
                                      suite_validator=fixture_suite_validator,
                                      receipt_validator=fixture_receipt_validator)

    def reject(self, message=None, reseal=False):
        if reseal:
            rebind(self.bundle)
        with self.assertRaisesRegex(ValueError, message or '.'):
            self.validate()

    def test_positive_written_fixture_does_not_claim_fresh_evidence(self):
        summary = self.validate()
        self.assertEqual(summary['results'], 1)
        self.assertEqual(summary['fresh_qualified_results'], 0)

    def test_positive_declared_suite_is_exactly_scoped(self):
        add_suite(self.root, self.bundle)
        self.assertEqual(self.validate()['fresh_qualified_results'], 1)

    def mixed_component_scope(self):
        self.bundle['results'][0].update(math_form='MIXED', claim_scope='COMPONENT')
        self.bundle['statuses'][0].update(inherited_evidence='MIXED_SCOPED',
            fresh_evidence='FRESH_KERNEL_COMPONENTS', implementation_reach='FORMAL_COMPONENT')

    def test_qualified_receipt_supports_scoped_component_evidence(self):
        for math_form in ['FORMAL', 'MIXED']:
            with self.subTest(math_form=math_form):
                self.bundle, self.anchor = make_bundle(self.root)
                suite, receipt = add_suite(self.root, self.bundle)
                original_receipt = deepcopy(receipt)
                self.mixed_component_scope()
                self.bundle['results'][0]['math_form'] = math_form
                rebind(self.bundle)
                self.assertEqual(self.validate()['fresh_qualified_results'], 0)
                self.assertEqual(self.bundle['receipts'], [original_receipt])
                self.assertEqual(self.bundle['statuses'][0]['fresh_evidence'], 'FRESH_KERNEL_COMPONENTS')

    def test_one_qualified_receipt_supports_formal_and_mixed_results(self):
        suite, receipt = add_suite(self.root, self.bundle)
        component = deepcopy(self.bundle['results'][0])
        component.update(id='T09-MIXED-COMPONENT', family='mixed-fixture-family',
                         math_form='MIXED', claim_scope='COMPONENT')
        status = deepcopy(self.bundle['statuses'][0])
        status.update(id=component['id'], inherited_evidence='MIXED_SCOPED',
                      fresh_evidence='FRESH_KERNEL_COMPONENTS', implementation_reach='FORMAL_COMPONENT')
        self.bundle['results'].append(component)
        self.bundle['statuses'].append(status)
        calculus = deepcopy(self.bundle['calculus'][0])
        calculus['id'] = component['id']
        self.bundle['calculus'].append(calculus)
        self.bundle['avenues'][0]['result_ids'].append(component['id'])
        self.bundle['selectors'].append({'family': component['family'], 'result_id': component['id'],
                                         'statement_sha256': digest(component)})
        suite['result_families'].append(component['family'])
        receipt['suite_sha256'] = digest(suite)
        original_receipt = deepcopy(receipt)
        rebind(self.bundle)
        summary = self.validate()
        self.assertEqual(summary['results'], 2)
        self.assertEqual(summary['fresh_qualified_results'], 1)
        self.assertEqual(self.bundle['receipts'], [original_receipt])
        self.assertEqual(status['receipt_ids'], self.bundle['statuses'][0]['receipt_ids'])
        self.assertEqual(status['fresh_evidence'], 'FRESH_KERNEL_COMPONENTS')

    def test_component_receipt_still_supports_component_evidence(self):
        suite, receipt = add_suite(self.root, self.bundle)
        self.mixed_component_scope()
        receipt.update(outcome='FRESH_KERNEL_COMPONENTS', proof_scope='COMPONENTS')
        rebind(self.bundle)
        self.assertEqual(self.validate()['fresh_qualified_results'], 0)

    def test_qualified_receipt_cannot_promote_mixed_scope(self):
        for field, value in [('claim_scope', 'WHOLE_RESULT'), ('claim_scope', 'DECLARED_SUITE'),
                             ('fresh_evidence', 'QUALIFIED_DECLARED_SUITE'),
                             ('inherited_evidence', 'KERNEL_DECLARED_SUITE')]:
            with self.subTest(field=field, value=value):
                self.bundle, self.anchor = make_bundle(self.root)
                add_suite(self.root, self.bundle)
                self.mixed_component_scope()
                record = self.bundle['results'][0] if field == 'claim_scope' else self.bundle['statuses'][0]
                record[field] = value
                self.reject('Mixed written result requires component kernel scope', reseal=True)

    def test_qualified_receipt_cannot_make_ordinary_component_formal(self):
        add_suite(self.root, self.bundle)
        self.mixed_component_scope()
        self.bundle['results'][0]['math_form'] = 'ORDINARY'
        self.reject('Written result cannot acquire whole kernel/formal status', reseal=True)

    def test_component_evidence_rejects_receipt_from_unbound_suite(self):
        suite, receipt = add_suite(self.root, self.bundle)
        self.mixed_component_scope()
        other_suite = deepcopy(suite)
        other_suite['id'] = 'other-suite'
        self.bundle['suites'].append(other_suite)
        receipt.update(suite_id=other_suite['id'], suite_sha256=digest(other_suite))
        self.reject('Cross-family receipt outside result suites', reseal=True)

    def test_component_evidence_requires_exact_source_domain_calculus(self):
        for field, value in [('source_ids', ['source-review']), ('domain', 'BARE_INPUT'),
                             ('calculus', 'OTHER')]:
            with self.subTest(field=field):
                self.bundle, self.anchor = make_bundle(self.root)
                add_suite(self.root, self.bundle)
                self.mixed_component_scope()
                self.bundle['results'][0][field] = value
                if field == 'source_ids':
                    self.bundle['reviews'][0]['reviewed_source_ids'] = value
                rebind(self.bundle)
                self.bundle['bindings'][0]['suite_targets'][0]['target_ids'] = ['target-ok']
                self.reject('Result target source/domain/calculus mismatch')

    def test_finite_or_failed_receipt_cannot_support_component_evidence(self):
        for outcome, proof_scope in [('FINITE_ONLY', 'FINITE'), ('FAILED', 'NONE'),
                                     ('RESOURCE_INCONCLUSIVE', 'NONE')]:
            with self.subTest(outcome=outcome):
                self.bundle, self.anchor = make_bundle(self.root)
                suite, receipt = add_suite(self.root, self.bundle)
                self.mixed_component_scope()
                receipt.update(outcome=outcome, proof_scope=proof_scope)
                if outcome == 'FAILED':
                    receipt['exit_code'] = 1
                    receipt['stages'][0]['exit_code'] = 1
                elif outcome == 'RESOURCE_INCONCLUSIVE':
                    receipt['exit_code'] = None
                    receipt['stages'][0].update(terminal='TIMEOUT', exit_code=None)
                self.reject('Fresh evidence does not match receipt outcome', reseal=True)

    def test_deleted_frozen_file_rejected(self):
        (self.root / OLD / 'registry.json').unlink()
        self.reject('Frozen|preserv')

    def test_changed_frozen_file_rejected(self):
        (self.root / OLD / 'registry.json').write_bytes(b'changed')
        self.reject('Frozen|preserv')

    def test_added_frozen_file_rejected(self):
        put_bytes(self.root, OLD + '/extra.json', b'{}')
        self.reject('Frozen|preserv')

    def test_candidate_cannot_reseal_changed_baseline(self):
        row = self.bundle['preservation']['files'][0]
        row['sha256'] = put_bytes(self.root, row['path'], b'changed')
        row['bytes'] = 7
        self.bundle['baseline_binding']['preservation_sha256'] = put(self.root, PROV + '/PRESERVATION.json', self.bundle['preservation'])
        self.reject('anchor|baseline|preserv')

    def test_unknown_result_field_rejected(self):
        self.bundle['results'][0]['overall_pass'] = True
        self.reject('fields', reseal=True)

    def test_unknown_fresh_enum_rejected(self):
        self.bundle['statuses'][0]['fresh_evidence'] = 'PASS'
        self.reject('enum|fresh')

    def test_duplicate_json_key_rejected(self):
        path = self.root / 'malformed.json'
        path.write_text('{"x":1,"x":2}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.v.read_json(path)

    def test_nonfinite_json_rejected(self):
        for token in ['NaN', 'Infinity', '-Infinity', '1e999', '[1e999]']:
            with self.subTest(token=token):
                path = self.root / 'malformed.json'
                path.write_text('{"x":' + token + '}', encoding='utf-8')
                with self.assertRaises(ValueError):
                    self.v.read_json(path)

    def test_malformed_json_rejected(self):
        path = self.root / 'malformed.json'
        path.write_text('{"unfinished":', encoding='utf-8')
        with self.assertRaises(ValueError):
            self.v.read_json(path)

    def test_review_coverage_is_union_of_scoped_reviews(self):
        extra = source(self.root, 'second-proof', b'Additional declared lemma.\n', 'Lemma.md')
        self.bundle['sources'].append(extra)
        self.bundle['public_allowlist'].append({'path': extra['public_path'], 'sha256': extra['public_sha256'],
            'bytes': extra['public_bytes'], 'kind': 'SOURCE', 'source_ids': [extra['id']]})
        self.bundle['results'][0]['source_ids'].append(extra['id'])
        review = deepcopy(self.bundle['reviews'][0])
        review.update(id='review-b', reviewed_source_ids=[extra['id']])
        self.bundle['reviews'].append(review)
        self.bundle['results'][0]['review_ids'].append(review['id'])
        rebind(self.bundle)
        self.assertEqual(self.validate()['results'], 1)

    def test_stopped_review_cannot_qualify_fresh_evidence(self):
        add_suite(self.root, self.bundle)
        self.bundle['reviews'][0]['outcome'] = 'STOPPED'
        self.reject('review|Review', reseal=True)

    def test_physical_suite_can_declare_result_family_separately(self):
        suite, receipt = add_suite(self.root, self.bundle)
        suite['family'] = 'physical-umbrella'
        receipt.update(family=suite['family'], suite_sha256=digest(suite))
        rebind(self.bundle)
        self.assertEqual(self.validate()['fresh_qualified_results'], 1)

    def test_undeclared_result_family_rejected(self):
        suite, receipt = add_suite(self.root, self.bundle)
        suite['result_families'] = ['unrelated-result-family']
        receipt['suite_sha256'] = digest(suite)
        self.reject('family', reseal=True)

    def test_qualified_receipt_requires_detailed_receipt_seam(self):
        add_suite(self.root, self.bundle)
        with self.assertRaisesRegex(ValueError, 'receipt'):
            self.v.validate_bundle(self.bundle, self.root, baseline_anchor=self.anchor,
                suite_validator=fixture_suite_validator, receipt_validator=False)

    def test_unknown_receipt_field_rejected(self):
        suite, receipt = add_suite(self.root, self.bundle)
        receipt['overall_pass'] = True
        self.reject('fields', reseal=True)

    def test_incomplete_positive_infrastructure_cannot_qualify_controls(self):
        suite, receipt = add_suite(self.root, self.bundle)
        receipt['stages'][0].update(terminal='MISSING', exit_code=None)
        self.reject('stages', reseal=True)

    def test_expected_rejection_stage_retains_its_actual_exit(self):
        for expected_exit in [1, 2]:
            with self.subTest(expected_exit=expected_exit):
                self.bundle, self.anchor = make_bundle(self.root)
                suite, receipt = add_suite(self.root, self.bundle)
                receipt['stages'].append({'id': 'declared-rejection', 'terminal': 'COMPLETED',
                    'exit_code': expected_exit, 'log_sha256': 'f' * 64})
                rebind(self.bundle)
                save_bundle(self.root, self.bundle)
                observed = []
                def declared_receipt_validator(actual, declared_suite, sources, root):
                    fixture_receipt_validator(actual, declared_suite, sources, root)
                    observed.append(actual['stages'][1]['exit_code'])
                    if actual['stages'][1]['exit_code'] != expected_exit:
                        raise ValueError('Wrong source-prescribed rejection exit')
                summary = self.v.validate_bundle(self.bundle, self.root, baseline_anchor=self.anchor,
                    suite_validator=fixture_suite_validator, receipt_validator=declared_receipt_validator)
                self.assertEqual(summary['fresh_qualified_results'], 1)
                self.assertEqual(observed, [expected_exit])

    def test_resource_exit_in_successful_stage_cannot_earn_credit(self):
        for resource_exit in [124, 137, 143, True, -9]:
            with self.subTest(resource_exit=resource_exit):
                self.bundle, self.anchor = make_bundle(self.root)
                suite, receipt = add_suite(self.root, self.bundle)
                receipt['stages'].append({'id': 'resource-failure', 'terminal': 'COMPLETED',
                    'exit_code': resource_exit, 'log_sha256': 'f' * 64})
                self.reject('stages|exit', reseal=True)

    def test_detailed_receipt_stage_rejection_is_propagated(self):
        suite, receipt = add_suite(self.root, self.bundle)
        receipt['stages'][0]['exit_code'] = 2
        rebind(self.bundle)
        save_bundle(self.root, self.bundle)
        def declared_receipt_validator(actual, declared_suite, sources, root):
            if actual['stages'][0]['exit_code'] != 0:
                raise ValueError('Source-prescribed positive stage must exit zero')
        with self.assertRaisesRegex(ValueError, 'Source-prescribed positive'):
            self.v.validate_bundle(self.bundle, self.root, baseline_anchor=self.anchor,
                suite_validator=fixture_suite_validator, receipt_validator=declared_receipt_validator)

    def test_unapproved_axiom_rejected(self):
        suite, receipt = add_suite(self.root, self.bundle)
        receipt['axioms'] = ['sorryAx']
        self.reject('axiom', reseal=True)

    def test_inherited_written_cannot_be_whole_kernel(self):
        self.bundle['results'][0].update(math_form='ORDINARY', claim_scope='WHOLE_RESULT')
        self.bundle['statuses'][0]['inherited_evidence'] = 'KERNEL_DECLARED_SUITE'
        self.reject('kernel|formal|written', reseal=True)

    def test_loaded_bundle_rejects_unknown_document_field(self):
        path = self.root / PROV / 'SOURCE_MAP.json'
        doc = self.v.read_json(path)
        doc['silently_ignored'] = True
        checksum = put(self.root, PROV + '/SOURCE_MAP.json', doc)
        self.bundle['registry']['records']['SOURCE_MAP']['sha256'] = checksum
        put(self.root, AREA + '/registry.json', self.bundle['registry'])
        loaded = self.v.load_bundle(self.root)
        with self.assertRaisesRegex(ValueError, 'record'):
            self.v.validate_bundle(loaded, self.root, baseline_anchor=self.anchor)

    def test_missing_public_source_rejected(self):
        (self.root / self.bundle['sources'][0]['public_path']).unlink()
        self.reject('Missing')

    def test_same_name_different_module_bytes_rejected(self):
        (self.root / self.bundle['sources'][0]['public_path']).write_bytes(b'theorem ok : False := by contradiction')
        self.reject('source|hash|bytes')

    def test_swapped_source_binding_hash_rejected(self):
        self.bundle['bindings'][0]['sources']['source-proof']['public_sha256'] = self.bundle['sources'][1]['public_sha256']
        self.reject('source.*binding|source association')

    def test_missing_review_rejected(self):
        self.bundle['reviews'] = []
        self.reject('review')

    def test_swapped_review_hash_rejected(self):
        self.bundle['reviews'][0]['review_sha256'] = self.bundle['sources'][0]['public_sha256']
        self.reject('review|Review')

    def test_wrong_review_target_rejected(self):
        self.bundle['reviews'][0]['target'] = 'Unrelated statement'
        self.reject('review|Review')

    def test_direct_nonarchive_input_keeps_null_archive(self):
        row = self.bundle['sources'][0]
        row.update(origin_input_sha256=row['original_sha256'], origin_archive_sha256=None, member_chain=[])
        self.assertEqual(self.validate()['sources'], 2)

    def test_direct_input_cannot_invent_original_hash(self):
        row = self.bundle['sources'][0]
        row.update(origin_archive_sha256=None, member_chain=[])
        self.reject('input|archive')

    def test_exact_projection_requires_original_public_equality(self):
        self.bundle['sources'][0]['original_sha256'] = 'f' * 64
        self.reject('EXACT|projection')

    def test_derived_projection_requires_reviewed_diff(self):
        row = self.bundle['sources'][0]
        row.update(projection='DERIVED', original_sha256='f' * 64)
        self.bundle['statuses'][0]['custody'] = 'DERIVED'
        self.reject('deriv|DERIVED', reseal=True)

    def test_private_diff_can_have_public_content_review(self):
        row = self.bundle['sources'][0]
        row.update(projection='DERIVED', original_sha256='f' * 64,
                   derivation={'diff_path': None, 'diff_sha256': 'd' * 64,
                               'review_id': 'projection-a', 'preserved_scope': 'Exact theorem content.'})
        self.bundle['projection_reviews'] = [{'id': 'projection-a', 'source_id': row['id'],
            'original_sha256': row['original_sha256'], 'public_sha256': row['public_sha256'],
            'diff_sha256': 'd' * 64, 'scope': 'Exact theorem content.', 'outcome': 'CONTENT_REVIEWED',
            'reviewer_kind': 'INTEGRATOR_CONTENT_REVIEW'}]
        self.bundle['statuses'][0]['custody'] = 'DERIVED'
        rebind(self.bundle)
        self.assertEqual(self.validate()['sources'], 2)
        self.bundle['projection_reviews'][0]['outcome'] = 'PENDING'
        self.reject('projection|review|DERIVED', reseal=True)

    def test_unlisted_group_payload_rejected(self):
        put_bytes(self.root, AREA + '/groups/example/unlisted.md', b'Unlisted artifact.\n')
        self.reject('allowlist|inventory')

    def test_custody_only_cannot_carry_public_path(self):
        self.bundle['sources'][0]['projection'] = 'CUSTODY_ONLY'
        self.reject('custody|CUSTODY')

    def test_ordinary_written_result_cannot_be_whole_kernel(self):
        add_suite(self.root, self.bundle)
        self.bundle['results'][0].update(math_form='ORDINARY', claim_scope='WHOLE_RESULT')
        self.reject('kernel|formal|written', reseal=True)

    def test_finite_result_cannot_be_total_service(self):
        self.bundle['statuses'][0].update(fresh_evidence='FINITE_ONLY', implementation_reach='TOTAL_SERVICE')
        self.reject('enum|reach')

    def test_calculus_map_cannot_conflate_has_e_and_plus(self):
        self.bundle['results'][0]['calculus'] = 'P01AC.ExtensionalRepair.HasE'
        self.bundle['calculus'][0]['calculus'] = 'P01AC.Intensional.Plus.HasPlus'
        self.reject('calculus', reseal=True)

    def test_canonical_calculus_adoption_rejected(self):
        self.bundle['calculus'][0]['canonical_adoption'] = 'ADOPTED'
        self.reject('adopt|enum')

    def test_wrong_toolchain_rejected(self):
        suite, receipt = add_suite(self.root, self.bundle)
        suite['toolchain']['version'] = '4.20.0'
        receipt['suite_sha256'] = digest(suite)
        receipt['toolchain_sha256'] = digest(suite['toolchain'])
        self.reject('Lean|toolchain|version', reseal=True)

    def test_suite_requires_detailed_validation_seam(self):
        add_suite(self.root, self.bundle)
        with self.assertRaisesRegex(ValueError, 'replay|suite'):
            self.v.validate_bundle(self.bundle, self.root, baseline_anchor=self.anchor,
                                  suite_validator=False)

    def test_source_control_target_mismatch_rejected(self):
        suite, receipt = add_suite(self.root, self.bundle)
        suite['controls'][1]['target_id'] = 'unrelated-target'
        receipt['suite_sha256'] = digest(suite)
        self.reject('control|target', reseal=True)

    def test_source_prescribed_counterexample_proof_can_qualify(self):
        suite, receipt = add_suite(self.root, self.bundle)
        control = suite['controls'][1]
        control.update(role='COUNTEREXAMPLE_PROOF', expected_outcome='ACCEPT', expected_outcome_sha256=raw_hash(b'ACCEPT'))
        receipt['controls'][1].update(role='COUNTEREXAMPLE_PROOF', expected_outcome_sha256=raw_hash(b'ACCEPT'),
            actual_outcome='ACCEPT', actual_outcome_sha256=raw_hash(b'ACCEPT'), exit_code=0)
        receipt['suite_sha256'] = digest(suite)
        rebind(self.bundle)
        self.assertEqual(self.validate()['fresh_qualified_results'], 1)

    def test_control_role_cannot_be_relabelled_in_receipt(self):
        suite, receipt = add_suite(self.root, self.bundle)
        receipt['controls'][1]['role'] = 'COUNTEREXAMPLE_PROOF'
        self.reject('role|control', reseal=True)

    def test_counterexample_role_cannot_expect_process_rejection(self):
        suite, receipt = add_suite(self.root, self.bundle)
        suite['controls'][1]['role'] = 'COUNTEREXAMPLE_PROOF'
        receipt['suite_sha256'] = digest(suite)
        receipt['controls'][1]['role'] = 'COUNTEREXAMPLE_PROOF'
        self.reject('role|control', reseal=True)

    def test_report_suite_target_mismatch_rejected(self):
        add_suite(self.root, self.bundle)
        self.bundle['bindings'][0]['suite_targets'][0]['target_ids'] = ['unknown-target']
        self.reject('target')

    def test_cross_family_receipt_rejected_even_when_rebound(self):
        suite, receipt = add_suite(self.root, self.bundle)
        receipt['family'] = 'other-family'
        self.reject('family|foreign', reseal=True)

    def test_receipt_changed_after_binding_rejected(self):
        suite, receipt = add_suite(self.root, self.bundle)
        receipt['log_sha256'] = 'f' * 64
        self.reject('receipt.*binding|receipt.*digest')

    def test_missing_negative_control_rejected(self):
        suite, receipt = add_suite(self.root, self.bundle)
        receipt['controls'].pop()
        self.reject('control', reseal=True)

    def test_timeout_is_not_semantic_rejection(self):
        suite, receipt = add_suite(self.root, self.bundle)
        receipt['controls'][1].update(terminal='TIMEOUT', exit_code=None)
        self.reject('control|terminal', reseal=True)

    def test_resource_exit_cannot_be_concrete_rejection(self):
        for exit_code in [124, 137, 143, True, -9]:
            with self.subTest(exit_code=exit_code):
                self.bundle, self.anchor = make_bundle(self.root)
                suite, receipt = add_suite(self.root, self.bundle)
                receipt['controls'][1]['exit_code'] = exit_code
                self.reject('control|exit', reseal=True)

    def test_control_outcome_hash_cannot_be_swapped(self):
        suite, receipt = add_suite(self.root, self.bundle)
        receipt['controls'][1]['actual_outcome_sha256'] = raw_hash(b'ACCEPT')
        self.reject('outcome|control', reseal=True)

    def test_target_readback_hash_cannot_be_swapped(self):
        suite, receipt = add_suite(self.root, self.bundle)
        receipt['target_readbacks'][0]['target_sha256'] = 'f' * 64
        self.reject('target|readback', reseal=True)

    def test_bare_input_does_not_substitute_for_certificate_domain(self):
        suite, receipt = add_suite(self.root, self.bundle)
        self.bundle['results'][0]['domain'] = 'BARE_INPUT'
        suite['targets'][0]['domain'] = 'SUPPLIED_CERTIFICATE'
        receipt['suite_sha256'] = digest(suite)
        self.reject('domain|target', reseal=True)

    def test_stale_selector_rejected(self):
        self.bundle['selectors'][0]['statement_sha256'] = 'f' * 64
        self.reject('selector')

    def test_duplicate_current_selector_rejected(self):
        self.bundle['selectors'].append(deepcopy(self.bundle['selectors'][0]))
        self.reject('selector|Duplicate')

    def test_supersession_cycle_rejected(self):
        row = self.bundle['results'][0]
        self.bundle['supersession'] = [{'from': row['id'], 'to': row['id'], 'relation': 'REFINES',
            'target': row['target'], 'basis_source_ids': row['source_ids'], 'retained_scope': 'Same exact scope.'}]
        self.reject('cycle')

    def test_copy_not_independent_evidence(self):
        duplicate = deepcopy(self.bundle['sources'][0])
        duplicate['id'] = 'copied-proof'
        self.bundle['sources'].append(duplicate)
        self.bundle['public_allowlist'][0]['source_ids'].append(duplicate['id'])
        self.bundle['results'][0]['source_ids'].append(duplicate['id'])
        self.bundle['reviews'][0]['reviewed_source_ids'].append(duplicate['id'])
        self.bundle['statuses'][0]['independent_evidence_count'] = 2
        self.reject('independent|distinct', reseal=True)

    def test_empirical_reanalysis_cannot_be_replication(self):
        self.bundle['empirical'] = [{'id': 'T07-FIXTURE', 'activity': 'EXPERIMENTAL_REPLICATION',
                                    'data_scope': 'Existing observations.', 'limitations': ['No new collection.']}]
        self.reject('empirical|enum')

    def test_candidate_sense_cannot_be_adopted(self):
        self.bundle['statuses'][0]['external_warrants']['terminology_adoption'] = 'ESTABLISHED'
        self.reject('warrant|enum')

    def test_forbidden_private_locator_rejected(self):
        self.bundle['results'][0]['limitations'] = ['Loaded from C:\\Users\\private\\session.json']
        self.reject('Private|private', reseal=True)

    def test_public_http_citation_path_is_not_a_private_filesystem_path(self):
        self.bundle['results'][0]['limitations'] = [
            'Reference: https://anggtwu.net/tmp/hindley_seldin__lambda-calculus_and_combinators_an_introduction.pdf',
            'Public route: https://example.org/home/agent/published-paper.pdf']
        rebind(self.bundle)
        self.assertEqual(self.validate()['results'], 1)

    def test_citation_exception_does_not_hide_real_private_locator(self):
        for text in ['https://example.org/paper.pdf followed by /tmp/private.json',
                     'https://example.org/paper.pdf?local=/tmp/private.json',
                     'https:///tmp/private.json', 'file:///tmp/private.json',
                     '/home/agent/private.json', 'C:\\Users\\private\\session.json']:
            with self.subTest(text=text):
                self.bundle['results'][0]['limitations'] = [text]
                self.reject('Private|private', reseal=True)

    def test_http_path_exception_does_not_hide_credentials(self):
        self.bundle['results'][0]['limitations'] = ['https://example.org/tmp/ghp_' + 'a' * 32]
        self.reject('credential|Private', reseal=True)

    def test_forbidden_private_payload_rejected(self):
        private = source(self.root, 'private-source', b'Private input /home/agent/session.json\n', 'private.md')
        self.bundle['sources'].append(private)
        self.reject('Private|private')

    def test_unsafe_public_path_rejected(self):
        self.bundle['sources'][0]['public_path'] = '../outside.lean'
        self.reject('Unsafe|path')

    def test_missing_status_is_not_success(self):
        self.bundle['statuses'] = []
        self.reject('status|Status')

    def test_old_obligation_requires_exact_literal_owner(self):
        self.bundle['obligations'] = [{'id': 'U01', 'owner_path': OLDPROV + '/SIXTH_FINAL_OVERLAY.json',
            'owner_sha256': self.anchor['legacy_overlay']['sha256'], 'statement': 'invented closed obligation',
            'result_ids': [], 'disposition': 'PRESERVED_OPEN', 'residual': 'Still open.'}]
        self.reject('owner|statement')

    def test_avenue_set_must_be_complete_twelve(self):
        self.bundle['avenues'].pop()
        self.reject('avenue')

    def test_legacy_endpoint_must_match_frozen_json_value(self):
        row = self.bundle['results'][0]
        self.bundle['legacy_endpoints'] = [{'id': 'legacy-control', 'owner_path': OLDPROV + '/SIXTH_FINAL_OVERLAY.json',
            'owner_sha256': self.anchor['legacy_overlay']['sha256'], 'json_pointer': '/fixture',
            'statement': 'forged legacy acceptance', 'target': row['target'], 'domain': row['domain'], 'calculus': row['calculus']}]
        self.reject('legacy|Legacy')

    def test_legacy_correction_preserves_historical_bytes(self):
        row = self.bundle['results'][0]
        self.bundle['legacy_endpoints'] = [{'id': 'legacy-control', 'owner_path': OLDPROV + '/SIXTH_FINAL_OVERLAY.json',
            'owner_sha256': self.anchor['legacy_overlay']['sha256'], 'json_pointer': '/fixture',
            'statement': 'overlay', 'target': row['target'], 'domain': row['domain'], 'calculus': row['calculus']}]
        self.bundle['supersession'] = [{'from': 'legacy-control', 'to': row['id'], 'relation': 'CORRECTS',
            'target': row['target'], 'basis_source_ids': row['source_ids'], 'retained_scope': 'Corrects only the declared target.'}]
        self.assertEqual(self.validate()['results'], 1)


if __name__ == '__main__':
    unittest.main()
