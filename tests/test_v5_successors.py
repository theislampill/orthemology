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
# Production replay helpers import their pinned siblings during interface checks.
sys.path.insert(0, str(SCRIPT.parent))


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

    def test_result_calculus_cannot_conflate_has_e_and_plus(self):
        self.bundle['results'][0]['calculus'] = 'P01AC.ExtensionalRepair.HasE'
        suite, _ = add_suite(self.root, self.bundle)
        suite['targets'][0]['calculus'] = 'P01AC.Intensional.Plus.HasPlus'
        self.bundle['receipts'][0]['suite_sha256'] = digest(suite)
        self.reject('Result target source/domain/calculus mismatch', reseal=True)

    def test_canonical_calculus_adoption_rejected(self):
        self.bundle['statuses'][0]['research_disposition'] = 'ADOPTED'
        self.reject('enum')

    def test_external_terminology_adoption_rejected(self):
        self.bundle['statuses'][0]['external_warrants']['terminology_adoption'] = 'ESTABLISHED'
        self.reject('enum')

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
        self.bundle['results'][0]['limitations'] = ['Loaded from C:' + '\\Users\\private\\session.json']
        self.reject('Private|private', reseal=True)

    def test_workspace_locator_rejected_in_decoded_status(self):
        for text in ['/' + 'workspace/scratch/case/source.lean',
                     'file://' + '/workspace/scratch/case/source.lean',
                     'https://' + '/workspace/scratch/case/source.lean',
                     'https://example.org/paper?local=' + '/workspace/scratch/case/source.lean']:
            with self.subTest(text=text):
                self.bundle['results'][0]['limitations'] = [text]
                self.reject('Private|private', reseal=True)

    def test_workspace_locator_rejected_in_exact_json_payload(self):
        raw = json.dumps({'recorded_member': {'path': '/' + 'workspace/scratch/case/source.lean'}}).encode()
        for encoded in [raw, raw.replace(b'/', b'\\u002f')]:
            with self.subTest(encoded=encoded):
                row = source(self.root, 'workspace-metadata', encoded, 'provenance.json')
                with self.assertRaisesRegex(ValueError, 'Private|private'):
                    self.v._sources({'sources': [row], 'reviews': [], 'projection_reviews': []}, self.root)

    def test_public_workspace_url_and_relative_path_remain_valid(self):
        self.bundle['results'][0]['limitations'] = [
            'https://example.org/workspace/published-source.lean',
            'docs/workspace/source.lean', 'workspace/source.lean']
        rebind(self.bundle)
        self.assertEqual(self.validate()['results'], 1)

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
                     '/home/agent/private.json', 'C:' + '\\Users\\private\\session.json']:
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


class ConsolidatedCalculusMapTests(unittest.TestCase):
    """One exact historical view; active results and input evidence stay live."""
    REGISTRY = 'experiments/orthemology-v5-successors/registry.json'
    RESULT = 'docs/provenance/v5-successors/RESULT_STATUS.json'
    MAP = 'docs/provenance/v5-successors/CALCULUS_MAP.json'
    MAP_SHA = 'd0644ef40458d17ac19710e4d1ecdc2cc974a54d73b4053641979f9ce1f74759'

    @classmethod
    def setUpClass(cls):
        import os
        import subprocess
        cls.os, cls.subprocess = os, subprocess
        path = SCRIPT.with_name('resolve_t20_v6_source.py')
        spec = importlib.util.spec_from_file_location('calculus_source', path)
        cls.source = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.source)
        root = SCRIPT.parents[1]
        cls.bodies = {path: (root / path).read_bytes() for path in
                      (cls.REGISTRY, cls.RESULT, *cls.source.SUCCESSOR_CALCULUS_GUIDES)}

    def git(self, *args):
        env = {k: v for k, v in self.os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1', GIT_ALLOW_PROTOCOL='',
                   GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=self.os.devnull,
                   GIT_CONFIG_SYSTEM=self.os.devnull, GIT_TERMINAL_PROMPT='0')
        return self.subprocess.check_output(['/usr/bin/git', '--no-replace-objects',
            '--literal-pathspecs', *args], cwd=self.root, env=env)

    def put(self, path, body):
        node = self.root / path
        node.parent.mkdir(parents=True, exist_ok=True)
        node.write_bytes(body)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='calculus-view-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.git('init', '-q', '--template=')
        for path, body in self.bodies.items():
            self.put(path, body)
        self.git('add', '--', *self.bodies)

    def assert_rejected(self):
        with self.assertRaises((ValueError, OSError)):
            self.source.successor_calculus_map_bytes(self.root)

    def test_exact_registry_inverse_and_all_nineteen_inputs(self):
        import hashlib
        document = json.loads(self.bodies[self.REGISTRY])
        inputs = {path: value.encode() for path, value in document.pop('preserved_source_inputs').items()}
        self.assertEqual(len(inputs), 19)
        self.assertNotIn('CALCULUS_MAP', document['records'])
        document['records']['CALCULUS_MAP'] = {'path': self.MAP, 'sha256': self.MAP_SHA}
        expected = (json.dumps(document, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode()
        self.assertEqual(hashlib.sha256(expected).hexdigest(),
                         'bd3a917d7225c18112915f5afaef373a864d176880bd6045c9ea291dd2308088')
        originals, absent, original_registry, _ = self.source._successor_input_catalog(self.root)
        self.assertEqual(original_registry, expected)
        self.assertEqual(originals, inputs)
        self.assertEqual(absent, set(inputs))

    def test_exact_map_with_present_staged_and_unstaged_absence(self):
        import hashlib
        historical = self.source.successor_calculus_map_bytes(self.root)
        self.assertEqual((len(historical), hashlib.sha256(historical).hexdigest()), (69376, self.MAP_SHA))
        self.assertEqual(self.source.successor_calculus_map_absences(self.root), {self.MAP})
        rows = json.loads(historical)['results']
        self.assertEqual(len(rows), 262)
        self.assertTrue(all(row['canonical_adoption'] == 'NOT_ADOPTED' for row in rows))
        self.put(self.MAP, historical)
        self.git('add', '--', self.MAP)
        self.assertEqual(self.source.successor_calculus_map_absences(self.root), set())
        (self.root / self.MAP).unlink()
        self.assertEqual(self.source.successor_calculus_map_absences(self.root), {self.MAP})
        self.git('update-index', '--remove', '--', self.MAP)
        self.assertEqual(self.source.successor_calculus_map_bytes(self.root), historical)

    def test_active_result_missing_tampered_or_mixed_index_is_rejected(self):
        (self.root / self.RESULT).unlink()
        self.assert_rejected()
        self.put(self.RESULT, self.bodies[self.RESULT] + b' ')
        self.assert_rejected()
        self.git('add', '--', self.RESULT)
        self.put(self.RESULT, self.bodies[self.RESULT])
        self.assert_rejected()

    def test_old_registry_cannot_admit_map_absence_or_hide_changed_input(self):
        old = json.loads(self.bodies[self.REGISTRY])
        old['records']['CALCULUS_MAP'] = {'path': self.MAP, 'sha256': self.MAP_SHA}
        self.put(self.REGISTRY, (json.dumps(old, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode())
        self.git('add', '--', self.REGISTRY)
        self.assert_rejected()
        # The previous input consolidation remains independently usable.
        self.assertEqual(len(self.source.successor_input_absences(self.root)), 19)
        changed = json.loads(self.bodies[self.REGISTRY])
        path = next(iter(changed['preserved_source_inputs']))
        changed['preserved_source_inputs'][path] += ' '
        self.put(self.REGISTRY, (json.dumps(changed, sort_keys=True, ensure_ascii=False, indent=2) + '\n').encode())
        self.git('add', '--', self.REGISTRY)
        self.assert_rejected()

    def test_present_or_staged_map_corruption_is_not_an_absence(self):
        self.put(self.MAP, b'{"results": []}\n')
        self.assert_rejected()
        self.git('add', '--', self.MAP)
        (self.root / self.MAP).unlink()
        self.assert_rejected()

    def test_guide_edits_have_exact_original_inverses_and_no_tamper_allowance(self):
        import hashlib
        for path, spec in self.source.SUCCESSOR_CALCULUS_GUIDES.items():
            original = self.source.successor_calculus_guide_source_bytes(self.root, path)
            self.assertEqual((hashlib.sha256(original).hexdigest(), len(original)), spec['original'][1:])
        path = next(iter(self.source.SUCCESSOR_CALCULUS_GUIDES))
        self.put(path, self.bodies[path] + b'\n')
        self.assert_rejected()
        self.git('add', '--', path)
        self.put(path, self.bodies[path])
        self.assert_rejected()

    def guide_allowlist_context(self):
        spec = importlib.util.spec_from_file_location('calculus_allowlist_successors', SCRIPT)
        validator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(validator)
        document = json.loads((SCRIPT.parents[1] / PROV / 'PUBLIC_PROJECTION.json').read_bytes())
        matches = [row for row in document['allowlist'] if row['path'] == PROV + '/README.md']
        self.assertEqual(len(matches), 1)
        return validator, matches[0]

    def test_allowlist_accepts_current_guide_with_its_original_authored_identity(self):
        import hashlib
        validator, row = self.guide_allowlist_context()
        self.assertEqual(row, {'path': PROV + '/README.md', 'kind': 'AUTHORED',
            'source_ids': [], 'bytes': 8164,
            'sha256': '1a5e06b45752fc2d01118b39550fdea297d5781954111a589c81e612f0823c93'})
        body = self.bodies[row['path']]
        self.assertEqual((len(body), hashlib.sha256(body).hexdigest()),
            (8213, '233561ef29c12585d4fcc76fa18591127f9f3bb001fcee7ad46a8a356f654537'))
        try:
            validator._allowlist({'public_allowlist': [row]}, self.root, {})
        except ValueError as error:
            self.fail('Exact current guide must retain its original allowlist view: ' + str(error))

    def test_allowlist_rejects_changes_to_the_original_guide_row(self):
        validator, row = self.guide_allowlist_context()
        mutations = [
            {'kind': 'METADATA'},
            {'source_ids': ['fixture-source']},
            {'sha256': '0' * 64},
            {'bytes': row['bytes'] + 1},
            {'bytes': 8213, 'sha256': '233561ef29c12585d4fcc76fa18591127f9f3bb001fcee7ad46a8a356f654537'},
        ]
        sources = {'fixture-source': {'id': 'fixture-source', 'public_path': None}}
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                changed = dict(row, **mutation)
                with self.assertRaisesRegex(ValueError, 'Original calculus guide allowlist identity changed'):
                    validator._allowlist({'public_allowlist': [changed]}, self.root, sources)

    def test_allowlist_enforces_live_and_staged_calculus_owner_identities(self):
        validator, row = self.guide_allowlist_context()
        bundle = {'public_allowlist': [row]}
        validator._allowlist(bundle, self.root, {})
        guide = row['path']
        self.put(guide, self.bodies[guide] + b'\n')
        with self.assertRaisesRegex(ValueError, 'calculus live owner'):
            validator._allowlist(bundle, self.root, {})
        self.git('add', '--', guide)
        self.put(guide, self.bodies[guide])
        with self.assertRaisesRegex(ValueError, 'calculus live owner'):
            validator._allowlist(bundle, self.root, {})
        self.git('add', '--', guide)
        self.put(self.RESULT, self.bodies[self.RESULT] + b' ')
        self.git('add', '--', self.RESULT)
        self.put(self.RESULT, self.bodies[self.RESULT])
        with self.assertRaisesRegex(ValueError, 'calculus live owner'):
            validator._allowlist(bundle, self.root, {})
        self.git('add', '--', self.RESULT)
        (self.root / guide).unlink()
        with self.assertRaises((ValueError, OSError)):
            validator._allowlist(bundle, self.root, {})

    def test_allowlist_keeps_unlisted_authored_payloads_exact(self):
        import hashlib
        validator, _ = self.guide_allowlist_context()
        path = '/'.join(('docs', 'allowlist-fixture.md'))
        body = b'# Ordinary authored fixture\n'
        self.assertNotIn(path, validator._source.SUCCESSOR_CALCULUS_GUIDES)
        self.put(path, body)
        row = {'path': path, 'kind': 'AUTHORED', 'source_ids': [],
               'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest()}
        validator._allowlist({'public_allowlist': [row]}, self.root, {})
        self.put(path, body + b'changed\n')
        with self.assertRaisesRegex(ValueError, 'Changed public allowlist payload'):
            validator._allowlist({'public_allowlist': [row]}, self.root, {})



class HistoricalPreservationConsumerTests(unittest.TestCase):
    """History authentication and current availability have separate owners."""
    PRES = PROV + '/PRESERVATION.json'
    BIND = PROV + '/BASELINE_BINDING.json'

    @classmethod
    def setUpClass(cls):
        import os
        import subprocess
        cls.os, cls.subprocess = os, subprocess
        spec = importlib.util.spec_from_file_location('preservation_successors', SCRIPT)
        cls.v = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.v)
        root = SCRIPT.parents[1]
        cls.raw_inventory = (root / cls.PRES).read_bytes()
        cls.inventory = json.loads(cls.raw_inventory)
        cls.binding = json.loads((root / cls.BIND).read_bytes())
        cls.graph = json.loads((root / PROV / 'SUPERSESSION.json').read_bytes())
        cls.obligations = json.loads((root / PROV / 'OBLIGATION_CROSSWALK.json').read_bytes())['obligations']
        cls.result_data = json.loads((root / PROV / 'RESULT_STATUS.json').read_bytes())
        cls.source_data = json.loads((root / PROV / 'SOURCE_MAP.json').read_bytes())
        env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1', GIT_ALLOW_PROTOCOL='')
        cls.objects = subprocess.check_output(['/usr/bin/git', '--no-replace-objects',
            'rev-parse', '--path-format=absolute', '--git-path', 'objects'], cwd=root, env=env).decode().strip()

    def git(self, *args):
        env = {k: v for k, v in self.os.environ.items() if not k.startswith('GIT_')}
        env.update(GIT_NO_LAZY_FETCH='1', GIT_NO_REPLACE_OBJECTS='1', GIT_ALLOW_PROTOCOL='',
                   GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=self.os.devnull,
                   GIT_CONFIG_SYSTEM=self.os.devnull, GIT_TERMINAL_PROMPT='0')
        return self.subprocess.check_output(['/usr/bin/git', '--no-replace-objects',
            '--literal-pathspecs', *args], cwd=self.root, env=env)

    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix='preservation-history-')
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.git('init', '-q', '--template=')
        (self.root / '.git/objects/info/alternates').write_text(self.objects + '\n')
        put_bytes(self.root, self.PRES, self.raw_inventory)
        self.git('add', '--', self.PRES)
        self.bundle = {'baseline_binding': deepcopy(self.binding), 'preservation': deepcopy(self.inventory),
            'registry': {'baseline_commit': self.binding['base_commit'], 'baseline_tree': self.binding['base_tree'],
                'records': {'PRESERVATION': {'path': self.PRES, 'sha256': self.binding['preservation_sha256']}}}}

    def preserve(self):
        return self.v._preservation(self.bundle, self.root, self.v.BASELINE_ANCHOR)

    def test_all_original_identities_without_a_historical_checkout(self):
        files = self.preserve()
        self.assertEqual(len(files), 1200)
        self.assertEqual(files, {row['path']: row for row in self.inventory['files']})
        self.assertTrue(all(not (self.root / path).exists() for path in self.v.FROZEN_ROOTS))

    def test_inventory_body_memory_and_staged_tampering_are_rejected(self):
        self.bundle['preservation']['files'][0]['bytes'] += 1
        with self.assertRaisesRegex(ValueError, 'In-memory preservation'):
            self.preserve()
        self.bundle['preservation'] = deepcopy(self.inventory)
        put_bytes(self.root, self.PRES, self.raw_inventory + b' ')
        with self.assertRaisesRegex(ValueError, 'pinned preservation inventory'):
            self.preserve()
        self.git('add', '--', self.PRES)
        put_bytes(self.root, self.PRES, self.raw_inventory)
        with self.assertRaisesRegex(ValueError, 'mixed or untracked native edition'):
            self.preserve()

    def test_wrong_ancestor_and_original_owner_identity_are_rejected(self):
        self.bundle['baseline_binding']['base_commit'] = '0' * 40
        with self.assertRaisesRegex(ValueError, 'baseline trust anchor'):
            self.preserve()
        row = self.graph['legacy_endpoints'][0]
        with self.assertRaisesRegex(ValueError, 'bound ancestor'):
            self.v._original_owner_bytes(self.root, row['owner_path'], '0' * 64, self.v.BASELINE_ANCHOR)
        wrong = dict(self.v.BASELINE_ANCHOR, base_tree='0' * 40)
        with self.assertRaisesRegex(ValueError, 'ancestor tree'):
            self.v._original_owner_bytes(self.root, row['owner_path'], row['owner_sha256'], wrong)

    def test_every_original_obligation_statement_remains_at_its_exact_owner(self):
        cache = {}
        for row in self.obligations:
            key = (row['owner_path'], row['owner_sha256'])
            if key not in cache:
                cache[key] = self.v._original_owner_bytes(self.root, *key, self.v.BASELINE_ANCHOR)
            self.assertIn(row['statement'], cache[key].decode('utf-8'))
        self.assertEqual((len(self.obligations), len(cache)), (118, 10))

    def test_both_inconclusive_legacy_observations_and_graph_binding_remain_exact(self):
        files = self.preserve()
        bundle = {'legacy_endpoints': deepcopy(self.graph['legacy_endpoints']),
                  'supersession': self.graph['edges'], 'selectors': self.graph['selectors']}
        results = {row['id']: row for row in self.result_data['results']}
        statuses = {row['id']: row for row in self.result_data['statuses']}
        sources = {row['id']: row for row in self.source_data['sources']}
        for row in bundle['legacy_endpoints']:
            raw = self.v._original_owner_bytes(self.root, row['owner_path'], row['owner_sha256'], self.v.BASELINE_ANCHOR)
            observed = self.v._pointer(self.v._input_json_bytes(raw), row['json_pointer'])
            self.assertEqual(observed['status'], 'INCONCLUSIVE')
            self.assertEqual(observed['exit_code'], 1)
        self.v._graph(bundle, self.root, results, statuses, sources, files, self.v.BASELINE_ANCHOR)
        bundle['legacy_endpoints'][0]['statement'] = bundle['legacy_endpoints'][0]['statement'].replace('INCONCLUSIVE', 'REJECTED')
        with self.assertRaisesRegex(ValueError, 'Legacy endpoint statement changed'):
            self.v._graph(bundle, self.root, results, statuses, sources, files, self.v.BASELINE_ANCHOR)

    def test_original_owner_present_and_staged_corruption_cannot_hide_as_absence(self):
        row = self.graph['legacy_endpoints'][0]
        raw = self.v._original_owner_bytes(self.root, row['owner_path'], row['owner_sha256'], self.v.BASELINE_ANCHOR)
        put_bytes(self.root, row['owner_path'], raw)
        self.git('add', '--', row['owner_path'])
        self.assertEqual(self.v._original_owner_bytes(self.root, row['owner_path'], row['owner_sha256'], self.v.BASELINE_ANCHOR), raw)
        put_bytes(self.root, row['owner_path'], raw + b' ')
        with self.assertRaisesRegex(ValueError, 'Changed present original owner'):
            self.v._original_owner_bytes(self.root, row['owner_path'], row['owner_sha256'], self.v.BASELINE_ANCHOR)
        self.git('add', '--', row['owner_path'])
        (self.root / row['owner_path']).unlink()
        with self.assertRaisesRegex(ValueError, 'changed staged'):
            self.v._original_owner_bytes(self.root, row['owner_path'], row['owner_sha256'], self.v.BASELINE_ANCHOR)

    def test_current_source_and_suite_consumers_still_reject_absence_and_tamper(self):
        bundle, _ = make_bundle(self.root)
        self.v._sources(bundle, self.root)
        source = bundle['sources'][0]
        path = self.root / source['public_path']
        raw = path.read_bytes()
        legacy_row = {'id': source['id'], 'path': source['public_path'],
                      'sha256': source['public_sha256'], 'bytes': source['public_bytes']}
        self.assertEqual(self.v._legacy.source_bytes(self.root, legacy_row), raw)
        path.unlink()
        with self.assertRaises((ValueError, OSError)):
            self.v._sources(bundle, self.root)
        with self.assertRaises((ValueError, OSError)):
            self.v._legacy.source_bytes(self.root, legacy_row)
        path.write_bytes(raw + b' ')
        with self.assertRaises((ValueError, OSError)):
            self.v._sources(bundle, self.root)
        with self.assertRaises((ValueError, OSError)):
            self.v._legacy.source_bytes(self.root, legacy_row)
        path.write_bytes(raw)
        suite, _ = add_suite(self.root, bundle)
        self.v._record_files(bundle, self.root)
        suite_path = self.root / bundle['registry']['records']['suite:' + suite['id']]['path']
        body = suite_path.read_bytes()
        suite_path.unlink()
        with self.assertRaises((ValueError, OSError)):
            self.v._record_files(bundle, self.root)
        suite_path.write_bytes(body + b' ')
        with self.assertRaises((ValueError, OSError)):
            self.v._record_files(bundle, self.root)


if __name__ == '__main__':
    unittest.main()
