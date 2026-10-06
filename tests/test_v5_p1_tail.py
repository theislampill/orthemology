"""Private offline/synthetic fixtures. Original producers must never execute."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / 'candidate/scripts/replay_v5_successors.py'
if not SCRIPT.is_file(): SCRIPT = HERE.parent / 'scripts/replay_v5_successors.py'
spec = importlib.util.spec_from_file_location('p1_tail_candidate', SCRIPT)
api = importlib.util.module_from_spec(spec); spec.loader.exec_module(api)
CONTEXT_ENV = 'V5_P1_TAIL_CONTEXT'
CONTEXT_SHA256 = 'a30a90111c3ca225338690828e43a24dc063b1022a25948272d6353413eac15f'
INPUTS = None
if os.environ.get(CONTEXT_ENV):
    context_bytes = Path(os.environ[CONTEXT_ENV]).read_bytes()
    if hashlib.sha256(context_bytes).hexdigest() != CONTEXT_SHA256: raise ValueError('P1 tail private test context identity changed')
    INPUTS = json.loads(context_bytes)
    if INPUTS['schema'] != 'P1-TAIL-TEST-CONTEXT-1' or INPUTS['scope'] != 'OFFLINE_CUSTODY_AND_SYNTHETIC_FIXTURES_ONLY': raise ValueError('Wrong P1 tail test context scope')
    fragment_bytes = Path(INPUTS['source_fragment']).read_bytes()
    if hashlib.sha256(fragment_bytes).hexdigest() != INPUTS['source_fragment_sha256']: raise ValueError('P1 tail fixture source fragment changed')
    FRAGMENT = json.loads(fragment_bytes)
else:
    FRAGMENT = {'sources': [], 'reviews': []}
CATALOG = api.p1_tail_meta
SOURCES = {r['id']: r for r in FRAGMENT['sources']}
REVIEWS = {r['id']: r for r in FRAGMENT['reviews']}
ROOT = Path(INPUTS['source_root']) if INPUTS else None
TOOLS = {k: Path(v) for k, v in INPUTS['tools'].items()} if INPUTS else {}
RETAINED = {'p1-prior-receipt': Path(INPUTS['prior_receipt']), 'p1-prior-command': Path(INPUTS['prior_command']),
            'p1-private-parameters': Path(INPUTS['private_parameters'])} if INPUTS else {}
PRIVATE_SKIP = 'V5_P1_TAIL_CONTEXT absent: private custody fixtures unavailable; no scientific execution is attempted'


@unittest.skipUnless(INPUTS, PRIVATE_SKIP)
class AdmissionCustody(unittest.TestCase):
    def function(self, name):
        value = getattr(api, name, None)
        self.assertTrue(callable(value), 'Missing bounded continuation behavior: ' + name)
        return value

    def suite(self):
        return self.function('p1_tail_descriptor')(api.p1_api(), 'CONTINUATION')

    def test_exact_descriptor_admits_only_four_tail_children_and_41_audit_targets(self):
        suite = self.suite()
        plan = api.validate_suite(suite, SOURCES, ROOT)
        self.assertEqual([x['id'] for x in suite['replay']['tail']], ['SourceShape', 'SourceContract', 'PythonEdges', 'IndependentPythonControls'])
        self.assertEqual(len(suite['replay']['audit_targets']), 41)
        self.assertEqual(suite['replay']['source_python']['version'], '3.12.3')
        self.assertEqual(suite['replay']['budgets']['child_seconds'], 180)
        self.assertEqual(plan['scope'], 'COMPONENTS')
        self.assertEqual(suite['replay']['new_lean_producer_builds'], 0)

    def test_descriptor_rejects_old_python_instead_of_compatible_fallback(self):
        bad = self.suite(); bad['replay']['source_python']['version'] = '3.11.9'
        with self.assertRaises(ValueError): api.validate_suite(bad, SOURCES, ROOT)

    def test_descriptor_rejects_changed_source_or_transitive_import_contract(self):
        bad = self.suite(); bad['replay']['original_suite_sha256'] = '0' * 64
        with self.assertRaises(ValueError): api.validate_suite(bad, SOURCES, ROOT)
        sources = copy.deepcopy(SOURCES)
        sid = next(r['source_id'] for r in CATALOG['original_physical_suite']['replay']['files'] if r['path'] == 'imports/P02A2/ObserverCore.lean')
        sources[sid]['public_sha256'] = '0' * 64
        with self.assertRaises(ValueError): api.validate_suite(self.suite(), sources, ROOT)

    def test_descriptor_rejects_missing_duplicate_or_reordered_tail(self):
        for kind in ('missing', 'duplicate', 'order'):
            bad = self.suite()
            if kind == 'missing': bad['replay']['tail'].pop()
            if kind == 'duplicate': bad['replay']['tail'][1] = copy.deepcopy(bad['replay']['tail'][0])
            if kind == 'order': bad['replay']['tail'].reverse()
            with self.subTest(kind=kind), self.assertRaises(ValueError): api.validate_suite(bad, SOURCES, ROOT)

    def test_source_tool_accepts_exact_312_bytes_without_executing_it(self):
        method = self.function('p1_tail_check_tools')
        with mock.patch.object(api, 'run_process', side_effect=AssertionError('Tool pin gate must not execute')):
            result = method(api.p1_api(), TOOLS)
        self.assertEqual(result['source_python']['version'], '3.12.3')
        self.assertEqual(result['source_python']['sha256'], 'e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f')

    def test_source_tool_rejects_old_311_bytes_before_any_effect(self):
        method = self.function('p1_tail_check_tools')
        bad = dict(TOOLS); bad['python-source'] = Path(INPUTS['orchestration_python'])
        with mock.patch.object(api, 'run_process', side_effect=AssertionError('Wrong interpreter must not run')):
            with self.assertRaises(ValueError): method(api.p1_api(), bad)

    def test_custody_gate_accepts_exact_files_and_rejects_changed_bytes(self):
        method = self.function('p1_tail_verify_custody')
        with tempfile.TemporaryDirectory(prefix='p1-tail-custody-') as td:
            root = Path(td); (root / 'verified.olean').write_bytes(b'SYNTHETIC OBJECT BYTES')
            rows = [{'path': 'verified.olean', 'sha256': hashlib.sha256(b'SYNTHETIC OBJECT BYTES').hexdigest(), 'bytes': 22}]
            self.assertEqual(method(api.p1_api(), root, rows), api.canonical(rows))
            (root / 'verified.olean').write_bytes(b'changed')
            with self.assertRaises(ValueError): method(api.p1_api(), root, rows)

    def test_custody_gate_rejects_extra_missing_unsafe_and_symlink_files(self):
        method = self.function('p1_tail_verify_custody')
        with tempfile.TemporaryDirectory(prefix='p1-tail-custody-') as td:
            root = Path(td); (root / 'one').write_bytes(b'a')
            rows = [{'path': 'one', 'sha256': hashlib.sha256(b'a').hexdigest(), 'bytes': 1}]
            (root / 'extra').write_bytes(b'b')
            with self.assertRaises(ValueError): method(api.p1_api(), root, rows)
            (root / 'extra').unlink(); (root / 'one').unlink()
            with self.assertRaises(ValueError): method(api.p1_api(), root, rows)
            (root / 'one').symlink_to('/dev/null')
            with self.assertRaises(ValueError): method(api.p1_api(), root, rows)
            with self.assertRaises(ValueError): method(api.p1_api(), root, [{'path': '../outside', 'sha256': '0'*64, 'bytes': 0}])

    def test_read_only_retained_join_preserves_failure_and_nine_real_objects(self):
        method = self.function('p1_tail_retain')
        with mock.patch.object(api, 'run_process', side_effect=AssertionError('Custody join must not execute')):
            result = method(api.p1_api(), self.suite(), SOURCES, ROOT, RETAINED, TOOLS)
        self.assertEqual(result['receipt']['outcome'], 'FAILED')
        self.assertEqual(result['receipt']['proof_scope'], 'NONE')
        self.assertEqual(len(result['objects']), 9)
        self.assertEqual(len(result['physical']['children']), 14)
        self.assertEqual([r['outcome'] for r in result['physical']['children']], ['ACCEPT'] * 9 + ['REJECT'] * 4 + ['FAILED'])

    def test_retained_join_rejects_changed_prior_failure_instead_of_overwriting_it(self):
        method = self.function('p1_tail_retain')
        with tempfile.TemporaryDirectory(prefix='p1-tail-receipt-') as td:
            prior = json.loads(RETAINED['p1-prior-receipt'].read_bytes()); prior['outcome'] = 'FRESH_KERNEL_COMPONENTS'
            changed = Path(td) / 'RECEIPT.json'; changed.write_text(json.dumps(prior))
            inputs = dict(RETAINED); inputs['p1-prior-receipt'] = changed
            with mock.patch.object(api, 'run_process', side_effect=AssertionError('Changed receipt must not run')):
                with self.assertRaises(ValueError): method(api.p1_api(), self.suite(), SOURCES, ROOT, inputs, TOOLS)

    def test_original_failed_receipt_remains_valid_under_legacy_public_dispatch(self):
        self.function('p1_tail_descriptor')
        receipt = json.loads(RETAINED['p1-prior-receipt'].read_bytes())
        result = api.validate_receipt(receipt, CATALOG['original_physical_suite'], SOURCES, ROOT)
        self.assertEqual(result['outcome'], 'FAILED')
        self.assertEqual(hashlib.sha256(RETAINED['p1-prior-receipt'].read_bytes()).hexdigest(), 'cced30ee21ffb6edcca015aaf7fdf825c668f8b8dcfb97497d22d6e5fa101ec8')


@unittest.skipUnless(INPUTS, PRIVATE_SKIP)
class TailFiniteTests(unittest.TestCase):
    function = AdmissionCustody.function
    suite = AdmissionCustody.suite
    @classmethod
    def setUpClass(cls):
        method = getattr(api, 'p1_tail_retain', None)
        cls.retained = method(api.p1_api(), api.p1_tail_descriptor(api.p1_api()), SOURCES, ROOT, RETAINED, TOOLS) if method else None

    def finite_fixture(self, out, *, version='3.12.3 (synthetic fixture, not execution)'):
        packet = self.retained['packet']
        obs = json.loads((packet / 'acceptance/evidence/INDEPENDENT_SOURCE_CONTROLS.json').read_bytes())
        obs['python_version'] = version; obs['created_utc'] = '2026-10-06T02:00:00Z'
        dest = out / api.p1_finite_rel; dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(obs, indent=2) + '\n')
        keys = ['status', 'differential_cases', 'outcome_counts', 'seeded_boundary_cases', 'source_ast_bindings']
        return {'SourceShape': (packet / 'acceptance/author/SOURCE_SHAPE_RESULT.json').read_text(),
            'SourceContract': '..\n----------------------------------------------------------------------\nRan 2 tests in 0.001s\n\nOK\n',
            'PythonEdges': (packet / 'acceptance/author/PYTHON_EDGE_CONTROLS.json').read_text(),
            'IndependentPythonControls': json.dumps({k: obs[k] for k in keys}) + '\nDetected mutations: 18\n'}

    def test_finite_parser_preserves_source_census_with_exact_312_and_no_rejection_processes(self):
        parser = self.function('p1_tail_finite')
        with tempfile.TemporaryDirectory(prefix='p1-tail-finite-fixture-') as td:
            out = Path(td); texts = self.finite_fixture(out)
            result = parser(api.p1_api(), self.retained['packet'], out, texts)
            self.assertEqual((result['differential_cases'], result['internal_mutations'], result['rejecting_subprocesses']), (266760, 18, 0))
            self.assertEqual(result['source_shape'], 'IDENTITY_ONLY')

    def test_finite_parser_rejects_old_ast_interpreter_and_wrong_internal_mutation(self):
        parser = self.function('p1_tail_finite')
        with tempfile.TemporaryDirectory(prefix='p1-tail-finite-fixture-') as td:
            out = Path(td); texts = self.finite_fixture(out, version='3.11.9 (known incompatible AST)')
            with self.assertRaises(ValueError): parser(api.p1_api(), self.retained['packet'], out, texts)
            texts = self.finite_fixture(out)
            path = out / api.p1_finite_rel; report = json.loads(path.read_bytes())
            report['mutation_controls'][0]['changed_source_sha256'] = '0' * 64
            path.write_text(json.dumps(report))
            with self.assertRaises(ValueError): parser(api.p1_api(), self.retained['packet'], out, texts)

    def test_finite_parser_rejects_old_shape_pins_missing_child_and_false_summary(self):
        parser = self.function('p1_tail_finite')
        with tempfile.TemporaryDirectory(prefix='p1-tail-finite-fixture-') as td:
            out = Path(td); texts = self.finite_fixture(out)
            for change in ('shape', 'missing', 'summary'):
                bad = dict(texts)
                if change == 'shape': bad['SourceShape'] = '{}'
                if change == 'missing': del bad['SourceContract']
                if change == 'summary': bad['IndependentPythonControls'] = bad['IndependentPythonControls'].replace('Detected mutations: 18', 'Detected mutations: 17')
                with self.subTest(change=change), self.assertRaises(ValueError): parser(api.p1_api(), self.retained['packet'], out, bad)

    def test_runtime_contains_no_wrapper_or_lean_producer_and_only_three_exact_copies(self):
        method = self.function('p1_tail_runtime')
        with tempfile.TemporaryDirectory(prefix='p1-tail-plan-') as td:
            runtime = method(api.p1_api(), self.retained, Path(td) / 'fresh')
            self.assertEqual([c['id'] for c in runtime['events']], CATALOG['tail_names'])
            self.assertTrue(all(c['argv'][0] == str(TOOLS['python-source']) and c['argv'][1] == '-B' for c in runtime['events']))
            self.assertTrue(all('replay.py' not in ' '.join(c['argv']) and '-o' not in c['argv'] for c in runtime['events']))
            self.assertEqual(len(runtime['copies']), 3)
            self.assertEqual(runtime['env']['LEAN_PATH'].split(':')[0], str(self.retained['run'] / 'original/build'))
            self.assertEqual(len(runtime['env']['LEAN_PATH'].split(':')), 9)

    def test_child_classifier_resource_dominates_exit_and_never_grants_rejection(self):
        method = self.function('p1_tail_outcome')
        for terminal, code, raw in [('TIMEOUT', None, b''), ('INTERRUPTED', None, b''), ('COMPLETED', 0, b'out of memory')]:
            self.assertEqual(method(api.p1_api(), {'terminal': terminal, 'exit_code': code}, raw), 'RESOURCE_INCONCLUSIVE')
        self.assertEqual(method(api.p1_api(), {'terminal': 'COMPLETED', 'exit_code': 1}, b'AssertionError'), 'FAILED')
        self.assertEqual(method(api.p1_api(), {'terminal': 'COMPLETED', 'exit_code': 0}, b'OK'), 'ACCEPT')
        with self.assertRaises(ValueError): method(api.p1_api(), {'terminal': 'COMPLETED', 'exit_code': -9}, b'')

    def test_safe_audit_source_remains_namespace_bound_to_exact_41_targets(self):
        method = self.function('p1_tail_runtime')
        with tempfile.TemporaryDirectory(prefix='p1-tail-plan-') as td:
            runtime = method(api.p1_api(), self.retained, Path(td) / 'fresh')
            audit = runtime['audit_source']
            self.assertIn('P1FreshCheckedAudit_', audit)
            self.assertNotIn('namespace V5SuccessorCheckedAudit', audit)
            self.assertEqual(audit, api.p1_audit_source(api.p1_api(), self.suite()['replay']['audit_targets']))


@unittest.skipUnless(INPUTS, PRIVATE_SKIP)
class ExecutionReceiptTests(unittest.TestCase):
    function = AdmissionCustody.function
    suite = AdmissionCustody.suite
    finite_fixture = TailFiniteTests.finite_fixture

    @classmethod
    def setUpClass(cls):
        cls.retained = api.p1_tail_retain(api.p1_api(), api.p1_tail_descriptor(api.p1_api()), SOURCES, ROOT, RETAINED, TOOLS)

    def execute_fixture(self, out, failure=None):
        self.function('p1_tail_execute_suite'); self.function('p1_tail_validate_receipt')
        calls = []
        def synthetic_process(argv, cwd, env, log, timeout):
            argv = [str(a) for a in argv]; calls.append((argv, str(cwd), timeout))
            index = len(calls) - 1; start = api.utc()
            if index < 4:
                # Source reference bytes are fixture data; no source module is imported or run.
                texts = self.finite_fixture(out / 'original')
                report_path = out / 'original' / api.p1_finite_rel
                if index < 3:
                    report_path.unlink()
                else:
                    report = json.loads(report_path.read_bytes()); report['created_utc'] = start
                    report_path.write_text(json.dumps(report, indent=2) + '\n')
                raw = texts[CATALOG['tail_names'][index]].encode()
            else:
                self.assertEqual(index, 4, 'Fixture was asked to execute an unapproved sixth process')
                self.assertNotIn('-o', argv)
                raw = ''.join('V5_BEGIN ' + t['name'] + '\n' + t['name'] + ' : True\n' + "'" + t['name'] + "' does not depend on any axioms\n" +
                    'V5_OWNER ' + t['name'] + ' ' + t['module'] + '\nV5_SAFE ' + t['name'] + ' 1 []\nV5_END ' + t['name'] + '\n'
                    for t in self.suite()['replay']['audit_targets']).encode()
            terminal, code = 'COMPLETED', 0
            if failure and index == failure['index']:
                terminal, code, raw = failure['terminal'], failure['code'], failure['raw']
            Path(log).parent.mkdir(parents=True, exist_ok=True); Path(log).write_bytes(raw)
            return {'terminal': terminal, 'exit_code': code, 'started_at': start, 'ended_at': api.utc(), 'log_sha256': api.sha(raw)}
        with mock.patch.object(api, 'run_process', side_effect=synthetic_process), \
             mock.patch.object(api, 'p1_tail_retain', return_value=self.retained), \
             mock.patch.object(api, 'p1_verify_dependencies', return_value=self.retained['receipt']['replay_evidence']['dependency_checks']), \
             mock.patch.object(api, 'p1_prepare', side_effect=AssertionError('Original wrapper preparation prohibited')), \
             mock.patch.object(api, 'p1_run_original', side_effect=AssertionError('Original wrapper replay prohibited')):
            receipt = api.execute_suite(self.suite(), SOURCES, ROOT, out, TOOLS, RETAINED, reviews=REVIEWS)
        return receipt, calls

    def test_successful_synthetic_tail_has_exact_five_processes_zero_builds_and_old_failure(self):
        with tempfile.TemporaryDirectory(prefix='p1-tail-executor-fixture-') as td:
            out = Path(td) / 'fresh'; receipt, calls = self.execute_fixture(out)
            self.assertEqual(receipt['outcome'], 'FRESH_KERNEL_COMPONENTS')
            self.assertEqual(len(calls), 5)
            self.assertEqual([c[2] for c in calls], [180] * 4 + [300])
            self.assertTrue(all(c[0][0] == str(TOOLS['python-source']) for c in calls[:4]))
            ev = receipt['replay_evidence']
            self.assertEqual((ev['new_builds'], ev['new_wrapper_runs'], ev['independent_evidence_increment']), (0, 0, 0))
            self.assertEqual((ev['retained_builds'], ev['new_finite_processes'], ev['new_audit_processes']), (9, 4, 1))
            self.assertEqual(ev['retained']['outcome'], 'FAILED')
            self.assertEqual(len(ev['target_audits']), 41)
            self.assertEqual(len(receipt['controls']), 17)
            self.assertEqual(ev['finite']['internal_mutations'], 18)
            self.assertEqual(api.validate_receipt(receipt, self.suite(), SOURCES, ROOT)['outcome'], receipt['outcome'])

    def test_resource_or_wrong_source_shape_stops_without_rejection_or_audit_credit(self):
        for failure in [dict(index=0, terminal='TIMEOUT', code=None, raw=b'TIMEOUT'),
                        dict(index=0, terminal='COMPLETED', code=1, raw=b'ValueError: AST shape changed: nat'),
                        dict(index=0, terminal='COMPLETED', code=0, raw=b'{}')]:
            with self.subTest(failure=failure), tempfile.TemporaryDirectory(prefix='p1-tail-failure-fixture-') as td:
                receipt, calls = self.execute_fixture(Path(td) / 'fresh', failure)
                self.assertEqual(len(calls), 1)
                self.assertEqual(receipt['proof_scope'], 'NONE')
                self.assertEqual(receipt['controls'], [])
                self.assertEqual(receipt['target_readbacks'], [])
                self.assertEqual(receipt['replay_evidence']['new_audit_processes'], 0)
                self.assertEqual(receipt['outcome'], 'RESOURCE_INCONCLUSIVE' if failure['terminal'] == 'TIMEOUT' else 'FAILED')

    def test_public_validator_rejects_retained_order_target_closure_and_count_forgery(self):
        with tempfile.TemporaryDirectory(prefix='p1-tail-forgery-fixture-') as td:
            receipt, _ = self.execute_fixture(Path(td) / 'fresh')
            self.assertEqual(receipt['outcome'], 'FRESH_KERNEL_COMPONENTS')
            mutations = [lambda r: r['replay_evidence']['retained'].__setitem__('outcome', 'FRESH_KERNEL_COMPONENTS'),
                lambda r: r['replay_evidence']['stage_results'].reverse(),
                lambda r: r['replay_evidence']['stage_results'].append(copy.deepcopy(r['replay_evidence']['stage_results'][0])),
                lambda r: r['replay_evidence']['target_audits'][0].__setitem__('name', 'FalseOwner.theorem'),
                lambda r: r['replay_evidence']['target_audits'][0].__setitem__('axioms', ['sorryAx']),
                lambda r: r['replay_evidence'].__setitem__('new_builds', 9),
                lambda r: r['replay_evidence']['finite'].__setitem__('rejecting_subprocesses', 18),
                lambda r: r['replay_evidence']['source_python'].__setitem__('version', '3.11.9'),
                lambda r: r['replay_evidence']['dependency_checks_after'].__setitem__('full_inventory_verified', False),
                lambda r: r['replay_evidence'].__setitem__('unexpected_field', 'not admitted')]
            for i, mutate in enumerate(mutations):
                bad = copy.deepcopy(receipt); mutate(bad)
                with self.subTest(mutation=i), self.assertRaises(ValueError): api.validate_receipt(bad, self.suite(), SOURCES, ROOT)

    def test_private_readback_rejects_altered_raw_log_or_duplicate_capture(self):
        method = self.function('p1_tail_readback')
        with tempfile.TemporaryDirectory(prefix='p1-tail-readback-fixture-') as td:
            out = Path(td) / 'fresh'; receipt, _ = self.execute_fixture(out)
            result = method(api.p1_api(), self.suite(), SOURCES, ROOT, out, TOOLS, RETAINED)
            self.assertEqual(result['outcome'], 'FRESH_KERNEL_COMPONENTS')
            raw = out / 'traces/0000.log'; original = raw.read_bytes(); raw.write_bytes(b'changed')
            with self.assertRaises(ValueError): method(api.p1_api(), self.suite(), SOURCES, ROOT, out, TOOLS, RETAINED)
            raw.write_bytes(original); (out / 'traces/9999.json').write_bytes((out / 'traces/0000.json').read_bytes())
            with self.assertRaises(ValueError): method(api.p1_api(), self.suite(), SOURCES, ROOT, out, TOOLS, RETAINED)

    def test_finite_view_joins_same_tail_with_zero_new_processes_and_rejects_failed_parent(self):
        self.function('p1_tail_join_finite')
        with tempfile.TemporaryDirectory(prefix='p1-tail-view-fixture-') as td:
            out = Path(td) / 'physical'; receipt, _ = self.execute_fixture(out)
            suite = api.p1_tail_descriptor(api.p1_api(), 'FINITE_VIEW')
            inputs = {**RETAINED, 'p1-tail-receipt': out / 'RECEIPT.json'}
            with mock.patch.object(api, 'run_process', side_effect=AssertionError('Correlated view must not execute')):
                view = api.execute_suite(suite, SOURCES, ROOT, Path(td) / 'finite', TOOLS, inputs, reviews=REVIEWS)
            self.assertEqual(view['outcome'], 'FINITE_ONLY')
            self.assertEqual(view['replay_evidence']['physical_receipt_sha256'], api.sha((out / 'RECEIPT.json').read_bytes()))
            self.assertEqual(view['replay_evidence']['new_processes'], 0)
            self.assertEqual(api.validate_receipt(view, suite, SOURCES, ROOT)['outcome'], 'FINITE_ONLY')
            self.assertEqual(api.sha(RETAINED['p1-prior-receipt'].read_bytes()), CATALOG['prior']['receipt_sha256'])
            with self.assertRaises(ValueError):
                api.execute_suite(suite, SOURCES, ROOT, Path(td) / 'bad-finite', TOOLS,
                    {**RETAINED, 'p1-tail-receipt': RETAINED['p1-prior-receipt']}, reviews=REVIEWS)


@unittest.skipUnless(INPUTS, PRIVATE_SKIP)
class HardeningTests(unittest.TestCase):
    function = AdmissionCustody.function
    suite = AdmissionCustody.suite

    def test_output_inside_retained_attempt_refuses_before_custody_or_any_effect(self):
        output = RETAINED['p1-prior-receipt'].parent / 'FORBIDDEN_TEST_NEVER_CREATED'
        self.assertFalse(output.exists())
        with mock.patch.object(api, 'p1_tail_retain', side_effect=AssertionError('Unsafe output reached custody')), \
             mock.patch.object(api, 'run_process', side_effect=AssertionError('Unsafe output executed')):
            with self.assertRaises(ValueError): api.execute_suite(self.suite(), SOURCES, ROOT, output, TOOLS, RETAINED, reviews=REVIEWS)
        self.assertFalse(output.exists())

    def test_output_census_refuses_unprescribed_file_before_a_success_claim(self):
        with tempfile.TemporaryDirectory(prefix='p1-tail-output-census-') as td:
            out = Path(td); (out / 'unprescribed.txt').write_text('synthetic extra file')
            with self.assertRaises(ValueError): api.p1_tail_output_rows(api.p1_api(), out)

    def test_review_hash_refuses_forged_but_well_formed_digest(self):
        suite = self.suite(); receipt = api.p1_tail_initial(api.p1_api(), suite, SOURCES, REVIEWS)
        receipt['review_hashes'][suite['review_ids'][0]] = '0' * 64
        with self.assertRaises(ValueError): api.p1_tail_validate_common(api.p1_api(), receipt, suite, SOURCES)


class PackagingAndScopeTests(unittest.TestCase):
    def test_exact_two_assets_match_code_owned_pins_and_catalog(self):
        self.assertEqual(set(api.p1_tail_asset_pins), {'v5_p1_tail_recipes.json', 'v5_p1_tail_assets/p1_tail_recipe.py'})
        for name, pin in api.p1_tail_asset_pins.items():
            data = (SCRIPT.parent / name).read_bytes()
            self.assertEqual(pin, {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
        self.assertEqual(CATALOG, json.loads((SCRIPT.parent / 'v5_p1_tail_recipes.json').read_bytes()))

    def test_missing_and_tampered_assets_refuse_before_helper_execution(self):
        for name in api.p1_tail_asset_pins:
            for mode in ('missing', 'changed'):
                with self.subTest(name=name, mode=mode), tempfile.TemporaryDirectory(prefix='p1-tail-assets-') as td:
                    dest = Path(td) / 'scripts'; shutil.copytree(SCRIPT.parent, dest)
                    asset = dest / name
                    if mode == 'missing': asset.unlink()
                    else: asset.write_bytes(asset.read_bytes() + b'\nraise RuntimeError("must not execute")\n')
                    spec = importlib.util.spec_from_file_location('p1_tail_asset_rejection', dest / SCRIPT.name)
                    module = importlib.util.module_from_spec(spec)
                    with self.assertRaises(ValueError): spec.loader.exec_module(module)

    def test_catalog_and_descriptors_contain_no_private_absolute_paths(self):
        value = json.dumps(CATALOG) + json.dumps(api.p1_tail_descriptor(api.p1_api()))
        for forbidden in ('/home/', '/mnt/', 'C:\\\\Users', '/workspace/shared/'):
            self.assertNotIn(forbidden, value)

    def test_legacy_original_helper_and_catalog_bytes_are_preserved(self):
        self.assertEqual(hashlib.sha256((SCRIPT.parent / 'v5_p1_assets/p1_recipe.py').read_bytes()).hexdigest(), 'f4fbbcc61093bc3ec6467c836a65b8e97294eb9960c722701ba64bed0a91f7ab')
        self.assertEqual(hashlib.sha256((SCRIPT.parent / 'v5_p1_recipes.json').read_bytes()).hexdigest(), '4ae8810e2dac517987ef93f383c597407792dc9bb8e37b7aa1fc1e4ef2967a81')

    def test_resource_failure_cannot_be_an_intended_new_rejection(self):
        for terminal, code in [('TIMEOUT', None), ('INTERRUPTED', None), ('MISSING', None)]:
            self.assertEqual(api.p1_tail_outcome(api.p1_api(), {'terminal': terminal, 'exit_code': code}, b'AssertionError'), 'RESOURCE_INCONCLUSIVE')
        self.assertEqual(api.p1_tail_outcome(api.p1_api(), {'terminal': 'COMPLETED', 'exit_code': 1}, b'AssertionError'), 'FAILED')

    def test_source_and_formal_view_scope_and_no_replay_policy_are_explicit(self):
        formal = api.p1_tail_descriptor(api.p1_api()); finite = api.p1_tail_descriptor(api.p1_api(), 'FINITE_VIEW')
        self.assertEqual((formal['replay']['scope'], finite['replay']['scope']), ('COMPONENTS', 'FINITE'))
        self.assertEqual(CATALOG['policy']['prior_wrapper_replays'], 0)
        self.assertEqual(CATALOG['policy']['new_lean_producer_builds'], 0)
        self.assertEqual(CATALOG['policy']['automatic_retries'], 0)
        self.assertEqual(CATALOG['prior']['failed_child'], 'SourceShape')
        self.assertEqual(len(CATALOG['prior']['completed_prefix']), 13)


if __name__ == '__main__':
    unittest.main(verbosity=2)
