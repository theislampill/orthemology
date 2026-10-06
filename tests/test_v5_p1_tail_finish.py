"""Private offline correction fixtures; no original scientific process may run."""
import copy
import base64
import hashlib
import importlib.util
import json
import os
import re
from pathlib import Path
import tempfile
import unittest
from unittest import mock

HERE = Path(__file__).resolve().parent
CONTEXT_SHA = '28e4d550f8865bb292a56f69cac0bc6c1bc15b049d42535c7428336b6299916a'
context_path = Path(os.environ.get('V5_P1_TAIL_FINISH_CONTEXT', HERE / 'P1_TAIL_FINISH_TEST_CONTEXT.json'))
CONTEXT = None
if context_path.is_file():
    raw = context_path.read_bytes()
    if hashlib.sha256(raw).hexdigest() != CONTEXT_SHA: raise ValueError('Changed private finish test context')
    CONTEXT = json.loads(raw)
LEGACY = os.environ.get('P1_FINISH_LEGACY_REPRO') == '1'
SCRIPT = Path(CONTEXT['frozen_base']) if LEGACY else HERE / 'candidate/scripts/replay_v5_successors.py'
if not SCRIPT.is_file(): SCRIPT = HERE.parent / 'scripts/replay_v5_successors.py'
spec = importlib.util.spec_from_file_location('p1_finish_fixture_adapter', SCRIPT)
api = importlib.util.module_from_spec(spec); spec.loader.exec_module(api)
if CONTEXT:
    raw = Path(CONTEXT['source_fragment']).read_bytes()
    if hashlib.sha256(raw).hexdigest() != CONTEXT['source_fragment_sha256']: raise ValueError('Changed fixture source fragment')
    FRAGMENT = json.loads(raw)
    SOURCES = {r['id']: r for r in FRAGMENT['sources']}
    REVIEWS = {r['id']: r for r in FRAGMENT['reviews']}
    ROOT = Path(CONTEXT['source_root'])
    TOOLS = {k: Path(v) for k, v in CONTEXT['tools'].items()}
    OLD_INPUTS = {'p1-prior-receipt': Path(CONTEXT['prior_receipt']), 'p1-prior-command': Path(CONTEXT['prior_command']),
                  'p1-private-parameters': Path(CONTEXT['private_parameters'])}
    INPUTS = {**OLD_INPUTS, 'p1-failed-tail-receipt': Path(CONTEXT['failed_tail_receipt']),
              'p1-failed-tail-command': Path(CONTEXT['failed_tail_command'])}
SKIP = 'Private P1 finish custody context unavailable; no scientific execution'
old_context = None
finish_context = None

class Fixture(unittest.TestCase):
    def function(self, name):
        value = getattr(api, name, None)
        self.assertTrue(callable(value), 'Missing source-bound finish behavior: ' + name)
        return value

    def old_context(self):
        global old_context
        if old_context is None:
            old_context = api.p1_tail_retain(api.p1_api(), api.p1_tail_descriptor(api.p1_api()), SOURCES, ROOT, OLD_INPUTS, TOOLS)
        return old_context

    def finish_context(self):
        global finish_context
        if finish_context is None:
            finish_context = self.function('p1_tail_finish_retain')(api.p1_api(), self.suite(), SOURCES, ROOT, INPUTS, TOOLS)
        return finish_context

    def suite(self, mode='CONTINUATION'):
        return self.function('p1_tail_finish_descriptor')(api.p1_api(), mode)

    def assert_public_boundary(self, receipt, output):
        def strings(value):
            if isinstance(value, str): yield value
            elif isinstance(value, list):
                for item in value: yield from strings(item)
            elif isinstance(value, dict):
                for key, item in value.items():
                    yield key
                    yield from strings(item)
        values = list(strings(receipt)); rendered = json.dumps(receipt, sort_keys=True)
        for value in values:
            self.assertIsNone(re.search(r'(?i)(/home/|/mnt/[a-z]/|[a-z]:[\\/]|file://)', value), 'Private absolute locator in public receipt')
        roots = [output, INPUTS['p1-failed-tail-receipt'].parent]
        for root in roots:
            for pattern in ('traces/*.log', 'traces/*.json', 'original/logs/*.log'):
                for path in root.glob(pattern):
                    raw = path.read_bytes()
                    if len(raw) < 64: continue
                    for encoded in (raw.hex(), base64.b64encode(raw).decode()):
                        self.assertNotIn(encoded, rendered, 'Reversible raw evidence transport in public receipt')
                    text = raw.decode('utf8', errors='replace')
                    for value in values: self.assertNotIn(text, value, 'Full raw log/capture in public receipt')

    def execute_fixture(self, output, failure=None, legacy=False):
        original = self.old_context()
        retained = None if legacy else self.finish_context()
        calls = []
        def process(argv, cwd, env, log, timeout):
            argv = [str(x) for x in argv]
            calls.append({'argv': argv, 'cwd': str(cwd), 'timeout': timeout})
            started = api.utc()
            packet = original['packet']
            if argv[-1].endswith('independent_source_controls.py'):
                report_path = output / 'original' / api.p1_finite_rel
                # This assertion is at the real subprocess boundary. The fixture
                # never supplies the implementation's missing parent directory.
                self.assertTrue(report_path.parent.is_dir(), 'Original driver evidence directory absent at actual process boundary')
                report = json.loads((packet / 'acceptance/evidence/INDEPENDENT_SOURCE_CONTROLS.json').read_bytes())
                report['python_version'] = '3.12.3 (fixture; no source executed)'
                report['created_utc'] = started
                report_path.write_text(json.dumps(report, indent=2) + '\n')
                keys = ['status', 'differential_cases', 'outcome_counts', 'seeded_boundary_cases', 'source_ast_bindings']
                raw = (json.dumps({k: report[k] for k in keys}) + '\nDetected mutations: 18\n').encode()
            elif argv[-1].endswith('source_contract.py') and '/controls/' not in argv[-1]:
                raw = (packet / 'acceptance/author/SOURCE_SHAPE_RESULT.json').read_bytes()
            elif argv[-1].endswith('test_source_contract.py'):
                raw = b'..\n----------------------------------------------------------------------\nRan 2 tests in 0.001s\n\nOK\n'
            elif argv[-1].endswith('check_python_edges.py'):
                raw = (packet / 'acceptance/author/PYTHON_EDGE_CONTROLS.json').read_bytes()
            else:
                self.assertNotIn('-o', argv)
                self.assertEqual(timeout, 300)
                raw = ''.join('V5_BEGIN ' + t['name'] + '\n' + t['name'] + ' : True\n' + "'" + t['name'] + "' does not depend on any axioms\n" +
                    'V5_OWNER ' + t['name'] + ' ' + t['module'] + '\nV5_SAFE ' + t['name'] + ' 1 []\nV5_END ' + t['name'] + '\n'
                    for t in api.p1_tail_descriptor(api.p1_api())['replay']['audit_targets']).encode()
            terminal, code = 'COMPLETED', 0
            if failure and len(calls) - 1 == failure['index']:
                terminal, code, raw = failure['terminal'], failure['code'], failure['raw']
            Path(log).write_bytes(raw)
            return {'terminal': terminal, 'exit_code': code, 'started_at': started, 'ended_at': api.utc(), 'log_sha256': api.sha(raw)}
        with mock.patch.object(api, 'run_process', side_effect=process), \
             mock.patch.object(api, 'p1_tail_retain', return_value=original), \
             mock.patch.object(api, 'p1_verify_dependencies', return_value=original['receipt']['replay_evidence']['dependency_checks']), \
             mock.patch.object(api, 'p1_prepare', side_effect=AssertionError('Forbidden original wrapper preparation')), \
             mock.patch.object(api, 'p1_run_original', side_effect=AssertionError('Forbidden original wrapper execution')):
            if legacy:
                receipt = api.execute_suite(api.p1_tail_descriptor(api.p1_api()), SOURCES, ROOT, output, TOOLS, OLD_INPUTS, reviews=REVIEWS)
            else:
                with mock.patch.object(api, 'p1_tail_finish_retain', return_value=retained):
                    receipt = api.execute_suite(self.suite(), SOURCES, ROOT, output, TOOLS, INPUTS, reviews=REVIEWS)
        self.assert_public_boundary(receipt, output)
        return receipt, calls


class Packaging(unittest.TestCase):
    def test_hash_bound_catalog_tamper_is_refused(self):
        with tempfile.TemporaryDirectory(prefix='p1-finish-assets-') as td:
            directory = Path(td)
            for name in api.p1_tail_finish_asset_pins:
                dest = directory / name; dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes((Path(api.__file__).parent / name).read_bytes())
            catalog = directory / 'v5_p1_tail_finish_recipes.json'
            catalog.write_bytes(catalog.read_bytes() + b' ')
            with mock.patch.object(api, '__file__', str(directory / 'adapter.py')), self.assertRaises(ValueError):
                api.p1_tail_finish_load_assets()

    def test_missing_reviewed_helper_is_refused(self):
        with tempfile.TemporaryDirectory(prefix='p1-finish-assets-') as td:
            directory = Path(td); name = 'v5_p1_tail_finish_recipes.json'
            (directory / name).write_bytes((Path(api.__file__).parent / name).read_bytes())
            with mock.patch.object(api, '__file__', str(directory / 'adapter.py')), self.assertRaises(FileNotFoundError):
                api.p1_tail_finish_load_assets()

@unittest.skipUnless(CONTEXT, SKIP)
class BoundaryRepro(Fixture):
    def test_process_boundary_requires_the_source_owned_evidence_directory(self):
        with tempfile.TemporaryDirectory(prefix='p1-finish-boundary-') as td:
            receipt, calls = self.execute_fixture(Path(td) / 'new', legacy=LEGACY)
            self.assertEqual(receipt['outcome'], 'FRESH_KERNEL_COMPONENTS')
            self.assertEqual(len(calls), 2)
            self.assertTrue(calls[0]['argv'][-1].endswith('independent_source_controls.py'))
            self.assertEqual([r['timeout'] for r in calls], [180, 300])

@unittest.skipUnless(CONTEXT, SKIP)
class Admission(Fixture):
    def test_descriptor_has_only_remaining_child_and_same_41_targets(self):
        suite = self.suite(); plan = api.validate_suite(suite, SOURCES, ROOT)
        self.assertEqual(plan['execute_names'], ['IndependentPythonControls', '_target_audit'])
        self.assertEqual(plan['reused_names'], ['SourceShape', 'SourceContract', 'PythonEdges'])
        self.assertEqual(len(plan['audit_targets']), 41)
        self.assertEqual(plan['budgets']['outer_seconds'], 3780)
        for field in ('execute_names', 'reused_names'):
            bad = copy.deepcopy(suite); bad['replay'][field].reverse()
            if bad == suite: bad['replay'][field].append('SourceShape')
            with self.assertRaises(ValueError): api.validate_suite(bad, SOURCES, ROOT)

    def test_retained_failure_and_successful_prefix_are_exact(self):
        context = self.finish_context()
        self.assertEqual(context['tail_receipt']['outcome'], 'FAILED')
        stages = context['tail_receipt']['replay_evidence']['stage_results']
        self.assertEqual([s['exit_code'] for s in stages], [0, 0, 0, 1])
        self.assertEqual(len(context['original']['objects']), 9)
        self.assertEqual([s['id'] for s in context['prefix']], ['SourceShape', 'SourceContract', 'PythonEdges'])

    def test_wrong_prior_and_changed_source_are_refused_without_effect(self):
        self.function('p1_tail_finish_retain')
        with self.assertRaises(ValueError):
            api.p1_tail_finish_retain(api.p1_api(), self.suite(), SOURCES, ROOT,
                {**INPUTS, 'p1-failed-tail-receipt': OLD_INPUTS['p1-prior-receipt']}, TOOLS)
        bad = copy.deepcopy(self.suite()); bad['replay']['source_python']['version'] = '3.11.9'
        with self.assertRaises(ValueError): api.validate_suite(bad, SOURCES, ROOT)
        bad_sources = copy.deepcopy(SOURCES)
        source_id = self.suite()['replay']['files'][0]['source_id']
        bad_sources[source_id]['public_sha256'] = '0' * 64
        with self.assertRaises(ValueError): api.validate_suite(self.suite(), bad_sources, ROOT)

    def test_changed_retained_capture_is_refused_before_readback_or_execution(self):
        with tempfile.TemporaryDirectory(prefix='p1-finish-retained-') as td:
            copied = Path(td) / 'tail'; copied.mkdir()
            for row in api.p1_tail_finish_meta['prior_tail']['run_files']:
                path = copied / row['path']; path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes((INPUTS['p1-failed-tail-receipt'].parent / row['path']).read_bytes())
            (copied / 'traces/0001.log').write_bytes(b'changed retained capture')
            with mock.patch.object(api, 'p1_tail_readback', side_effect=AssertionError('Changed custody reached readback')), \
                 mock.patch.object(api, 'run_process', side_effect=AssertionError('Custody check must not execute')):
                with self.assertRaises(ValueError):
                    api.p1_tail_finish_retain(api.p1_api(), self.suite(), SOURCES, ROOT,
                        {**INPUTS, 'p1-failed-tail-receipt': copied / 'RECEIPT.json'}, TOOLS)

    def test_changed_imported_closure_refuses_before_output_effect(self):
        retained = self.finish_context()
        with tempfile.TemporaryDirectory(prefix='p1-finish-closure-') as td:
            output = Path(td) / 'new'
            with mock.patch.object(api, 'p1_tail_finish_retain', return_value=retained), \
                 mock.patch.object(api, 'p1_verify_dependencies', return_value={'changed': True}), \
                 mock.patch.object(api, 'run_process', side_effect=AssertionError('Changed closure must not execute')):
                with self.assertRaises(ValueError):
                    api.execute_suite(self.suite(), SOURCES, ROOT, output, TOOLS, INPUTS, reviews=REVIEWS)
            self.assertFalse(output.exists())

    def test_existing_retained_output_or_overlapping_root_refuses_before_effect(self):
        output = INPUTS['p1-failed-tail-receipt'].parent / 'FORBIDDEN_NEVER_CREATED'
        self.assertFalse(output.exists())
        self.function('p1_tail_finish_execute_suite')
        with mock.patch.object(api, 'p1_tail_finish_retain', side_effect=AssertionError('Unsafe output reached custody')), \
             mock.patch.object(api, 'run_process', side_effect=AssertionError('Forbidden scientific execution')):
            with self.assertRaises(ValueError): api.execute_suite(self.suite(), SOURCES, ROOT, output, TOOLS, INPUTS, reviews=REVIEWS)
        self.assertFalse(output.exists())

@unittest.skipUnless(CONTEXT, SKIP)
class Execution(Fixture):
    def test_success_keeps_original_intervals_and_separates_reused_three_from_new_one(self):
        with tempfile.TemporaryDirectory(prefix='p1-finish-success-') as td:
            receipt, calls = self.execute_fixture(Path(td) / 'new')
            self.assertEqual(receipt['outcome'], 'FRESH_KERNEL_COMPONENTS')
            ev = receipt['replay_evidence']
            self.assertEqual(ev['retained_tail'], self.finish_context()['tail_receipt'])
            self.assertEqual(ev['retained_prefix'], self.finish_context()['prefix'])
            self.assertEqual([s['id'] for s in ev['stage_results']], ['IndependentPythonControls', '_target_audit'])
            self.assertEqual((ev['new_finite_processes'], ev['new_audit_processes'], ev['new_builds'], ev['independent_evidence_increment']), (1, 1, 0, 0))
            self.assertEqual(len(calls), 2)
            self.assertEqual(len(receipt['controls']), 17)
            self.assertEqual(ev['finite']['internal_mutations'], 18)
            self.assertEqual(len(ev['target_audits']), 41)
            self.assertEqual(api.validate_receipt(receipt, self.suite(), SOURCES, ROOT)['outcome'], 'FRESH_KERNEL_COMPONENTS')

    def test_failure_or_resource_stops_before_audit_and_never_grants_rejection(self):
        for terminal, code, raw in [('COMPLETED', 1, b'AssertionError'), ('TIMEOUT', None, b'TIMEOUT'), ('COMPLETED', 0, b'out of memory')]:
            with self.subTest(terminal=terminal, code=code), tempfile.TemporaryDirectory(prefix='p1-finish-failure-') as td:
                receipt, calls = self.execute_fixture(Path(td) / 'new', dict(index=0, terminal=terminal, code=code, raw=raw))
                self.assertEqual(len(calls), 1)
                self.assertEqual(receipt['proof_scope'], 'NONE')
                self.assertEqual(receipt['controls'], [])
                self.assertEqual(receipt['replay_evidence']['new_audit_processes'], 0)
                self.assertEqual(receipt['replay_evidence']['stage_results'][0]['rejecting_subprocesses'], 0)
                self.assertEqual(receipt['outcome'], 'FAILED' if code == 1 else 'RESOURCE_INCONCLUSIVE')

    def test_public_validator_refuses_changed_prior_counts_order_private_payload_and_audit(self):
        with tempfile.TemporaryDirectory(prefix='p1-finish-forgery-') as td:
            receipt, _ = self.execute_fixture(Path(td) / 'new')
            mutations = [lambda e: e['retained_prefix'][0].__setitem__('started_at', '2000-01-01T00:00:00Z'),
                lambda e: e['retained_tail'].__setitem__('outcome', 'FRESH_KERNEL_COMPONENTS'),
                lambda e: e.__setitem__('new_finite_processes', 4), lambda e: e['stage_results'].reverse(),
                lambda e: e['stage_results'].append(copy.deepcopy(e['stage_results'][0])),
                lambda e: e['target_audits'][0].__setitem__('axioms', ['sorryAx']),
                lambda e: e['target_audits'][0].__setitem__('name', 'Wrong.name'),
                lambda e: e.__setitem__('raw_capture', '/home/agent/private'),
                lambda e: e['finite'].__setitem__('rejecting_subprocesses', 18)]
            for i, mutate in enumerate(mutations):
                bad = copy.deepcopy(receipt); mutate(bad['replay_evidence'])
                with self.subTest(mutation=i), self.assertRaises(ValueError): api.validate_receipt(bad, self.suite(), SOURCES, ROOT)

    def test_private_readback_refuses_mutated_new_capture_without_replaying_sources(self):
        self.function('p1_tail_finish_readback')
        with tempfile.TemporaryDirectory(prefix='p1-finish-readback-') as td:
            out = Path(td) / 'new'; receipt, _ = self.execute_fixture(out)
            with mock.patch.object(api, 'run_process', side_effect=AssertionError('Readback must not execute')):
                checked = api.p1_tail_finish_readback(api.p1_api(), self.suite(), SOURCES, ROOT, out, TOOLS, INPUTS)
                self.assertEqual(checked, receipt)
                raw = out / 'traces/0003.log'; raw.write_bytes(b'changed')
                with self.assertRaises(ValueError): api.p1_tail_finish_readback(api.p1_api(), self.suite(), SOURCES, ROOT, out, TOOLS, INPUTS)

    def test_finite_view_is_one_correlated_zero_process_join(self):
        with tempfile.TemporaryDirectory(prefix='p1-finish-view-') as td:
            out = Path(td) / 'new'; receipt, _ = self.execute_fixture(out)
            suite = self.suite('FINITE_VIEW')
            with mock.patch.object(api, 'run_process', side_effect=AssertionError('Finite view must not execute')):
                view = api.execute_suite(suite, SOURCES, ROOT, Path(td) / 'view', TOOLS,
                    {**INPUTS, 'p1-finish-receipt': out / 'RECEIPT.json'}, reviews=REVIEWS)
            self.assertEqual(view['outcome'], 'FINITE_ONLY')
            self.assertEqual(view['replay_evidence']['new_processes'], 0)
            self.assertEqual(view['replay_evidence']['physical_receipt'], receipt)
            self.assertEqual(api.validate_receipt(view, suite, SOURCES, ROOT)['outcome'], 'FINITE_ONLY')
            self.assert_public_boundary(view, out)

if __name__ == '__main__': unittest.main(verbosity=2)
