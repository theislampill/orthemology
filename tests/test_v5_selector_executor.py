"""Synthetic executor controls. No Lean/source-owned producer is executed."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    exec(compile(path.read_bytes(), str(path), 'exec'), module.__dict__)
    return module


API = load('selector_executor_frozen', ROOT / 'scripts/replay_v5_successors.py')
HELPER = load('selector_executor_helper', ROOT / 'scripts/v5_selector_continuation.py')
EXEC_PATH = ROOT / 'scripts/v5_selector_executor.py'
EXEC = load('selector_executor', EXEC_PATH) if EXEC_PATH.exists() else None
FAMILY = API.selector_g1_load_family()
CAT = FAMILY.selector_g1_catalog(API)
SUITE = CAT['families']['selector']['suite']
TARGETS = SUITE['replay']['target_names']


def synthetic_fixture():
    """Deliberately ineligible old receipt; tests never claim real execution."""
    zero = API.sha(b'SYNTHETIC_ONLY'); start = '2026-10-06T03:00:00Z'; end = '2026-10-06T03:00:03Z'
    hashes = CAT['families']['selector']['source_hashes']
    old = {key: {} for key in HELPER.SC_COMMON}
    old.update(source_hashes_before=hashes, source_hashes_after=hashes, source_inventory_before={},
        output_hashes={}, official_caches_before={}, dependency_reuse={}, stage_results=[])
    prior = {'id': 'SYNTHETIC_FAILED_NOT_ELIGIBLE', 'suite_id': SUITE['id'], 'family': SUITE['family'],
        'suite_sha256': API.canonical(SUITE), 'source_hashes': hashes, 'review_hashes': {},
        'toolchain_sha256': API.canonical(SUITE['toolchain']), 'outcome': 'FAILED', 'proof_scope': 'NONE', 'replay_evidence': old}
    stages = []; children = []
    for spec in SUITE['replay']['stages'][1:]:
        stages.append({'id': spec['id'], 'argv': spec['argv'], 'cwd': '.', 'budget_seconds': spec['timeout_seconds'],
            'started_at': start, 'ended_at': start, 'terminal': 'COMPLETED', 'exit_code': 0, 'log_sha256': zero, 'output_hashes': {}})
        children.append({'stage_id': spec['id'], 'observed_at': start, 'actual_outcome': 'ACCEPT',
            'terminal': 'COMPLETED', 'exit_code': 0, 'log_sha256': zero})
    fresh = [{'id': name, 'argv': ['{builtin:prerequisites}'] if name == '_prerequisites' else ['{tool:lean}', '-j1', '{out}/generated/V5SuccessorReadback.lean'],
        'cwd': '.', 'budget_seconds': 30 if name == '_prerequisites' else 300, 'started_at': start, 'ended_at': end,
        'terminal': 'COMPLETED', 'exit_code': 0, 'log_sha256': zero, 'output_hashes': {}} for name in ('_prerequisites', '_target_audit')]
    return {'started_at': start, 'ended_at': end, 'replay_evidence': {
        'prior': {'receipt': prior, 'receipt_sha256': zero, 'receipt_canonical_sha256': API.canonical(prior),
            'receipt_bytes': 0, 'failure_sha256': zero, 'parent_custody_acceptance_sha256': HELPER.SC_PARENT_CUSTODY},
        'retained_collection': {'parser_id': 'SYNTHETIC_ONLY', 'collector_runner_sha256': zero, 'observed_at': start,
            'collection': {}, 'stage_results': stages, 'child_observations': children, 'control_diagnostics': []},
        'retained_inputs': {}, 'stage_results': fresh}}


BASELINE = synthetic_fixture()
PRIOR = BASELINE['replay_evidence']['prior']['receipt']


def log_text():
    return '\n'.join('V5_BEGIN {name}\n{name} : True\n\'{name}\' does not depend on any axioms\nV5_OWNER {name} {module}\nV5_SAFE {name} 1 []\nV5_END {name}'.format(**row) for row in TARGETS) + '\n'


class ExecutorTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(EXEC, 'Private selector executor has not been implemented')
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name); self.output = self.home / 'output'
        self.tick = datetime(2026, 10, 7, tzinfo=timezone.utc)
        def utc():
            self.tick += timedelta(milliseconds=1)
            return self.tick.isoformat().replace('+00:00', 'Z')
        patch = mock.patch.object(API, 'utc', side_effect=utc); patch.start(); self.addCleanup(patch.stop)

    def run_row(self, terminal='COMPLETED', code=0):
        return {'terminal': terminal, 'exit_code': code, 'started_at': API.utc(), 'ended_at': API.utc(), 'log_sha256': API.sha(log_text().encode())}

    def test_output_must_be_absent_and_disjoint(self):
        protected = self.home / 'retained'; protected.mkdir()
        for output in (protected, protected / 'new', self.home):
            with self.subTest(output=output), self.assertRaises(ValueError):
                EXEC.output_path(output, [protected], api=API)
        self.assertEqual(EXEC.output_path(self.output, [protected], api=API), self.output)

    def test_output_link_parent_refused(self):
        target = self.home / 'target'; target.mkdir(); link = self.home / 'link'; link.symlink_to(target, target_is_directory=True)
        with self.assertRaises(ValueError): EXEC.output_path(link / 'new', [], api=API)

    def test_exact_audit_uses_only_shared_runner_and_no_object_output(self):
        self.output.mkdir(); (self.output / 'project').mkdir(); calls = []
        def runner(argv, cwd, env, log, timeout):
            calls.append(([str(x) for x in argv], str(cwd), dict(env), timeout))
            log.parent.mkdir(parents=True, exist_ok=True); log.write_text(log_text())
            return self.run_row()
        with mock.patch.object(API, 'run_process', side_effect=runner):
            run, raw, invocation = EXEC.audit_once(self.output, {'targets': {r['target_id']: r for r in TARGETS}},
                {'lean': self.home / 'bound-lean'}, {'LEAN_PATH': 'bound-selector:bound-core:bound-official'}, api=API, helper=HELPER, family=FAMILY)
        self.assertEqual(len(calls), 1); self.assertEqual(calls[0][0][1], '-j1'); self.assertNotIn('-o', calls[0][0])
        self.assertEqual(calls[0][3], 300); self.assertEqual(raw, log_text().encode())
        self.assertEqual(invocation['generated_source_sha256'], HELPER.SC_AUDITOR)
        self.assertEqual(json.loads((self.output / 'AUDIT_PROCESS.json').read_bytes()), run)
        self.assertFalse(list(self.output.rglob('*.olean')))

    def test_audit_rejects_wrong_target_or_generator(self):
        for change in ('targets', 'source'):
            self.output.mkdir(exist_ok=True); (self.output / 'project').mkdir(exist_ok=True)
            targets = {r['target_id']: r for r in TARGETS}
            if change == 'targets': targets.pop(next(iter(targets)))
            patch = mock.patch.object(FAMILY, 'selector_g1_audit_source', return_value='foreign') if change == 'source' else mock.patch.object(API, 'utc', wraps=API.utc)
            with patch, mock.patch.object(API, 'run_process', side_effect=AssertionError('Audit must not start')), self.assertRaises(ValueError):
                EXEC.audit_once(self.output, {'targets': targets}, {'lean': 'x'}, {'LEAN_PATH': 'x'}, api=API, helper=HELPER, family=FAMILY)

    def test_actual_terminal_and_safe_readback_required(self):
        outcome, rows = EXEC.audit_result(self.run_row(), log_text().encode(), TARGETS, api=API)
        self.assertEqual(outcome, 'QUALIFIED_DECLARED_SUITE'); self.assertEqual(len(rows), 7)
        for raw in (b'', b'error: missing', log_text().replace('V5_SAFE', 'V5_UNSAFE').encode(), (log_text() + 'warning: untrusted').encode()):
            with self.assertRaises(ValueError): EXEC.audit_result(self.run_row(), raw, TARGETS, api=API)

    def test_failed_and_resource_processes_never_gain_target_credit(self):
        for terminal, code, expected in [('COMPLETED', 1, 'FAILED'), ('TIMEOUT', None, 'RESOURCE_INCONCLUSIVE'), ('INTERRUPTED', None, 'RESOURCE_INCONCLUSIVE')]:
            self.assertEqual(EXEC.audit_result(self.run_row(terminal, code), b'', TARGETS, api=API), (expected, {}))
        for code in (True, 124, 137, -9):
            with self.assertRaises(ValueError): EXEC.audit_result(self.run_row('COMPLETED', code), b'', TARGETS, api=API)

    def test_completed_resource_diagnostic_preserves_exit_without_forged_receipt(self):
        with self.assertRaises(EXEC.AuditRefusal) as raised:
            EXEC.audit_result(self.run_row('COMPLETED', 1), b'maximum number of heartbeats reached', TARGETS, api=API)
        self.assertEqual(raised.exception.outcome, 'RESOURCE_INCONCLUSIVE')

    def test_readonly_guard_forbids_process_and_extraction(self):
        import subprocess, zipfile
        with EXEC.readonly_collection():
            with self.assertRaises(ValueError): subprocess.Popen(['never-run'])
            with self.assertRaises(ValueError): subprocess.run(['never-run'])
            with self.assertRaises(ValueError): os.system('never-run')
            with self.assertRaises(ValueError): zipfile.ZipFile.extract(None, 'never-read')

    def test_public_composition_has_no_raw_log_or_resolved_paths(self):
        receipt = self.compose()
        text = json.dumps(receipt)
        self.assertFalse(str(self.home) in text); self.assertFalse('"log_hex"' in text); self.assertFalse('"audit_log_hex"' in text)
        self.assertEqual(receipt['outcome'], 'QUALIFIED_DECLARED_SUITE'); self.assertEqual(len(receipt['target_readbacks']), 7)
        self.assertEqual(receipt['replay_evidence']['prior']['receipt'], PRIOR)
        self.assertEqual(receipt['replay_evidence']['accounting']['new_child_compilations'], 0)

    def compose(self, terminal='COMPLETED', code=0, raw=None):
        example = deepcopy(BASELINE); e = example['replay_evidence']; e['runner_sha256'] = API.sha(Path(API.__file__).read_bytes())
        e['retained_collection']['collector_runner_sha256'] = e['runner_sha256']
        run = {k: e['stage_results'][-1][k] for k in ('terminal', 'exit_code', 'started_at', 'ended_at', 'log_sha256')}
        run.update(terminal=terminal, exit_code=code, log_sha256=API.sha(log_text().encode() if raw is None else raw))
        return EXEC.compose_receipt({'binding': e['prior'], 'prior': PRIOR}, {'targets': {r['target_id']: r for r in TARGETS}}, SUITE,
            e['retained_collection'], e['retained_inputs'], e['stage_results'][0], run,
            log_text().encode() if raw is None else raw, {'argv': [str(self.home / 'lean')], 'cwd': str(self.home)},
            example['started_at'], example['ended_at'], api=API, helper=HELPER)

    def test_failed_public_composition_keeps_original_failed_and_no_partial_audit(self):
        for terminal, code, outcome in [('COMPLETED', 1, 'FAILED'), ('TIMEOUT', None, 'RESOURCE_INCONCLUSIVE')]:
            record = self.compose(terminal, code, b'')
            self.assertEqual((record['outcome'], record['proof_scope']), (outcome, 'NONE'))
            self.assertEqual(record['target_readbacks'], []); self.assertEqual(record['replay_evidence']['target_audits'], [])

    def test_completed_parser_refusal_writes_actual_process_and_none_scope(self):
        self.output.mkdir(); (self.output / 'logs').mkdir(); process = self.run_row()
        EXEC.write_refusal(self.output, '2026-10-07T00:00:00Z', process, ValueError('private diagnostic'), api=API, helper=HELPER)
        row = json.loads((self.output / 'REFUSAL.json').read_bytes())
        self.assertEqual(row['audit_process'], process); self.assertEqual(row['proof_scope'], 'NONE')
        self.assertEqual(row['outcome'], 'FAILED'); self.assertFalse(row['qualified_receipt_written'])
        self.assertFalse((self.output / 'RECEIPT.json').exists())

    def test_refusal_preserves_process_saved_before_log_association_failure(self):
        self.output.mkdir(); process = self.run_row('TIMEOUT', None); API.write_json(self.output / 'AUDIT_PROCESS.json', process)
        EXEC.write_refusal(self.output, API.utc(), None, ValueError('post-return log mismatch'), api=API, helper=HELPER)
        row = json.loads((self.output / 'REFUSAL.json').read_bytes())
        self.assertEqual(row['audit_process'], process); self.assertEqual(row['outcome'], 'RESOURCE_INCONCLUSIVE')


class MeasurementTests(ExecutorTests):
    # Do not inherit the parent's test methods into the measurement census.
    def setUp(self):
        super().setUp()
        self.prior = self.home / 'prior'; self.core = self.home / 'core'; self.root = self.home / 'sources'
        for path in (self.prior / 'project', self.prior / 'original/build', self.prior / 'archive', self.core / 'original/runtime/build', self.root):
            path.mkdir(parents=True)
        raw = b'-- synthetic source\n'
        (self.prior / 'project/Main.lean').write_bytes(raw); (self.prior / 'archive/Main.lean').write_bytes(raw); (self.root / 'Main.lean').write_bytes(raw)
        self.objects = {}; core_objects = {}
        # Small synthetic sets exercise every census path; the separate exact
        # retained readback verifies the actual 15/167 identities.
        for count, root, prefix, rows in [(2, self.prior, 'original/build/S', self.objects), (3, self.core, 'original/runtime/build/C', core_objects)]:
            for i in range(count):
                name = prefix + str(i) + '.olean'; value = ('synthetic object ' + name).encode(); (root / name).write_bytes(value); rows[name] = API.sha(value)
        self.core_reuse = {'identity': {'objects': core_objects}}
        def custody(root, *, api):
            return {p: {'kind': 'REGULAR_FILE', 'sha256': digest} for p, digest in FAMILY.selector_g1_inventory(api, root).items()}
        acceptance = self.home / 'acceptance.json'; acceptance.write_bytes(b'parent failure custody only')
        self.helper = SimpleNamespace(selector_custody=custody, SC_CUSTODY=API.canonical(custody(self.prior, api=API)),
            SC_PROJECT=API._file_hashes(self.prior / 'project'), SC_CORE_REUSE=API.canonical(self.core_reuse), SC_PARENT_CUSTODY=API.sha(acceptance.read_bytes()))
        self.family = SimpleNamespace(selector_g1_inventory=FAMILY.selector_g1_inventory,
            selector_g1_dependency_join=mock.Mock(return_value=self.core_reuse),
            selector_g1_catalog=lambda api: {'core_suite': {'replay': {'build_roots': ['original/runtime/build']}}})
        self.sources = {'sourceA': {'id': 'sourceA'}}
        self.plan = {'files': {'sourceA': {'path': 'Main.lean'}}, 'contents': {'sourceA': raw}}
        self.suite = {'source_ids': ['sourceA'], 'replay': {'build_roots': ['original/build']}}
        self.checked = {'prior': {'source_hashes': {'sourceA': API.sha(raw)}, 'replay_evidence': {
            'source_inventory_before': {'selector': FAMILY.selector_g1_inventory(API, self.prior / 'archive')},
            'output_hashes': self.objects, 'dependency_reuse': self.core_reuse}},
            'context': {'roots': {'selector': str(self.prior / 'archive')}}}
        self.inputs = {'dependency-run': self.core, 'parent-custody-acceptance': acceptance}
        patch = mock.patch.object(API, 'public_bytes', side_effect=lambda root, source: (root / 'Main.lean').read_bytes())
        patch.start(); self.addCleanup(patch.stop)

    def measure(self):
        return EXEC.measure_retained(self.checked, self.plan, self.suite, self.prior, self.inputs, self.root, self.sources,
            api=API, helper=self.helper, family=self.family)

    def test_measures_every_retained_source_object_and_core_dependency(self):
        value = self.measure(); self.assertEqual(value['objects'], self.objects)
        self.assertEqual(len(value['core_objects']), 3); self.assertEqual(value['core_reuse_sha256'], self.helper.SC_CORE_REUSE)
        self.family.selector_g1_dependency_join.assert_called_once()

    def test_changed_selector_object_source_or_parent_acceptance_refused(self):
        for name in ['project/Main.lean', 'archive/Main.lean', next(iter(self.objects))]:
            path = self.prior / name; original = path.read_bytes(); path.write_bytes(b'changed')
            with self.subTest(name=name), self.assertRaises(ValueError): self.measure()
            path.write_bytes(original)
        self.inputs['parent-custody-acceptance'].write_bytes(b'changed')
        with self.assertRaises(ValueError): self.measure()

    def test_missing_changed_extra_or_linked_core_object_refused(self):
        path = self.core / next(iter(self.core_reuse['identity']['objects'])); original = path.read_bytes()
        path.write_bytes(b'changed')
        with self.assertRaises(ValueError): self.measure()
        path.write_bytes(original); extra = self.core / 'original/runtime/build/extra.olean'; extra.write_bytes(b'extra')
        with self.assertRaises(ValueError): self.measure()
        extra.unlink(); path.unlink()
        with self.assertRaises(ValueError): self.measure()
        target = self.home / 'object'; target.write_bytes(original); path.symlink_to(target)
        with self.assertRaises(ValueError): self.measure()

    def test_changed_public_source_or_reuse_join_refused(self):
        source = self.root / 'Main.lean'; original = source.read_bytes(); source.write_bytes(b'changed')
        with self.assertRaises(ValueError): self.measure()
        source.write_bytes(original); self.family.selector_g1_dependency_join.return_value = {'identity': {'objects': {}}}
        with self.assertRaises(ValueError): self.measure()


# Keep the two sets disjoint without repeating unrelated integration controls.
for _name in list(ExecutorTests.__dict__):
    if _name.startswith('test_') and _name not in MeasurementTests.__dict__:
        setattr(MeasurementTests, _name, None)


class FlowTests(ExecutorTests):
    def flow(self, *, failure=None, changed_after=False, process=None):
        prior = self.home / 'prior'; prior.mkdir(); root = self.home / 'sources'; root.mkdir()
        core = self.home / 'core'; core.mkdir(); acceptance = self.home / 'acceptance'; acceptance.write_bytes(b'x')
        output = self.output; example = deepcopy(BASELINE); e = example['replay_evidence']
        old = PRIOR['replay_evidence']; checked = {'prior': PRIOR, 'binding': e['prior'], 'context': {}}
        plan = {'files': {}, 'contents': {}, 'targets': {r['target_id']: r for r in TARGETS}}
        measured = {'project_sha256': HELPER.SC_PROJECT, 'source_inventory': old['source_inventory_before'],
            'objects': old['output_hashes'], 'core_reuse_sha256': HELPER.SC_CORE_REUSE, 'source_hashes': PRIOR['source_hashes']}
        environment = {'resolved': {'lean': self.home / 'lean'}, 'fingerprints': old['tool_fingerprints'],
            'dependencies': old['dependency_checks'], 'input_hashes': {}, 'caches': old['official_caches_before'],
            'libraries': ['synthetic-official'],
            'env': {'LEAN_PATH': 'synthetic-only'}}
        def collect(*args, **kwargs):
            row = deepcopy(e['retained_collection']); row['collector_runner_sha256'] = API.sha(Path(API.__file__).read_bytes()); row['observed_at'] = API.utc()
            for stage, child in zip(row['stage_results'], row['child_observations']):
                stage['started_at'] = API.utc(); child['observed_at'] = API.utc(); stage['ended_at'] = API.utc()
            return row
        def audit(*args, **kwargs):
            generated = output / 'generated'; generated.mkdir(); (generated / 'V5SuccessorReadback.lean').write_bytes(FAMILY.selector_g1_audit_source(API, TARGETS).encode())
            (output / 'logs/target-audit.log').write_text(log_text())
            run = self.run_row() if process is None else self.run_row(*process)
            API.write_json(output / 'AUDIT_PROCESS.json', run)
            invocation = {'scope': 'SYNTHETIC_ONLY'}; API.write_json(output / 'RESOLVED_AUDIT_INVOCATION.json', invocation)
            if failure == 'audit': raise ValueError('Synthetic audit refusal')
            return run, log_text().encode(), invocation
        after = deepcopy(measured)
        if changed_after: after['objects'] = {'foreign.olean': 'f' * 64}
        measurement = mock.Mock(side_effect=[measured, after])
        if failure == 'before': measurement.side_effect = ValueError('Synthetic preflight refusal')
        with mock.patch.object(EXEC, 'prepare', return_value=(checked, plan, FAMILY)), \
                mock.patch.object(EXEC, 'measure_retained', measurement), \
                mock.patch.object(EXEC, 'environment_measurement', return_value=environment) as environment_call, \
                mock.patch.object(EXEC, 'recollect', side_effect=collect) as recollection, \
                mock.patch.object(EXEC, 'audit_once', side_effect=audit) as audit_call, \
                mock.patch.object(HELPER, 'validate_selector_continuation', return_value={'outcome': 'SYNTHETIC_VALIDATOR_STUB'}) as validation:
            try:
                result = EXEC.execute(SUITE, {}, root, prior, output, {}, {'dependency-run': core, 'parent-custody-acceptance': acceptance},
                    reviews={}, api=API, helper=HELPER)
            except ValueError:
                if not failure and not changed_after: raise
                result = None
            return result, measurement.call_count, environment_call.call_count, recollection.call_count, audit_call.call_count, validation.call_count

    def test_complete_flow_measures_twice_collects_once_and_audits_once(self):
        result, measurements, environment, collections, audits, validation = self.flow()
        self.assertEqual(result['outcome'], 'QUALIFIED_DECLARED_SUITE')
        self.assertEqual((measurements, environment, collections, audits, validation), (2, 2, 1, 1, 1))
        self.assertEqual(result['replay_evidence']['prior']['receipt']['outcome'], 'FAILED')

    def test_preflight_failure_never_starts_collection_or_audit(self):
        result, measurements, environment, collections, audits, validation = self.flow(failure='before')
        self.assertIsNone(result); self.assertEqual((collections, audits, validation), (0, 0, 0))
        self.assertFalse((self.output / 'RECEIPT.json').exists())

    def test_postflight_changed_objects_prevent_public_receipt(self):
        result, measurements, environment, collections, audits, validation = self.flow(changed_after=True)
        self.assertIsNone(result); self.assertEqual((measurements, audits, validation), (2, 1, 0))
        row = json.loads((self.output / 'REFUSAL.json').read_bytes())
        self.assertEqual(row['audit_process']['exit_code'], 0); self.assertEqual(row['proof_scope'], 'NONE')

    def test_post_return_refusal_preserves_actual_audit_process(self):
        result, *counts = self.flow(failure='audit')
        self.assertIsNone(result); row = json.loads((self.output / 'REFUSAL.json').read_bytes())
        self.assertEqual(row['audit_process']['terminal'], 'COMPLETED'); self.assertEqual(row['audit_process']['exit_code'], 0)
        self.assertFalse((self.output / 'RECEIPT.json').exists())


for _name in list(ExecutorTests.__dict__):
    if _name.startswith('test_') and _name not in FlowTests.__dict__:
        setattr(FlowTests, _name, None)


class EnvironmentTests(ExecutorTests):
    def setUp(self):
        super().setUp(); self.suite = deepcopy(SUITE); self.suite['replay']['build_roots'] = []
        lean = self.home / 'lean/bin/lean'; lean.parent.mkdir(parents=True); lean.write_bytes(b'synthetic lean executable')
        python = self.home / 'python'; python.write_bytes(b'synthetic Python executable')
        self.git = self.home / 'git'; self.git.write_bytes(b'synthetic Git executable')
        mathlib = self.home / 'mathlib'; mathlib.mkdir()
        self.tools = {'lean': lean, 'lean-bin': lean.parent, 'python': python, 'mathlib': mathlib}
        self.suite['toolchain']['executable_sha256'] = API.sha(lean.read_bytes())
        for row in self.suite['replay']['tools']:
            row['executable_sha256'] = API.sha((python if row['name'] == 'python' else lean).read_bytes())
        packages = {row['name']: row for row in self.suite['replay']['packages']}
        self.plan = {'packages': packages, 'official': {}, 'modules': {}, 'inputs': {}, 'drivers': {},
            'contents': {row['manifest_source_id']: b'synthetic manifest' for row in packages.values()}}
        for name, row in packages.items():
            repo = mathlib / row['path']; repo.mkdir(parents=True, exist_ok=True)
            if name != 'Cli':
                lib = repo / '.lake/build/lib/lean'; lib.mkdir(parents=True); (lib / 'Official.olean').write_bytes(name.encode())
        lib = lean.parent.parent / 'lib/lean'; lib.mkdir(parents=True); (lib / 'Init.olean').write_bytes(b'synthetic official Lean cache')
        patch = mock.patch.object(API.shutil, 'which', return_value=str(self.git)); patch.start(); self.addCleanup(patch.stop)
        patch = mock.patch.object(FAMILY, 'SELECTOR_G1_GIT_SHA256', API.sha(self.git.read_bytes())); patch.start(); self.addCleanup(patch.stop)
        pins = {row['name']: row['revision'] for row in self.suite['toolchain']['packages']}
        paths = {str(mathlib / row['path']): name for name, row in packages.items()}
        self.calls = []
        def process(argv, cwd, env, log, timeout):
            argv = [str(x) for x in argv]; self.calls.append(argv)
            if argv[1:] == ['--version']:
                text = 'Python 3.11.9\n' if argv[0] == str(python) else 'Lean 4.19.0 6caaee842e94 x86_64-unknown-linux-gnu\n'
            elif argv[-2:] == ['rev-parse', 'HEAD']: text = pins[paths[argv[2]]] + '\n'
            elif argv[-3:] == ['status', '--porcelain', '--untracked-files=no']: text = ''
            else: raise AssertionError('Synthetic environment saw a nonmetadata process')
            log.parent.mkdir(parents=True, exist_ok=True); log.write_text(text)
            return {**self.run_row(), 'log_sha256': API.sha(log.read_bytes())}
        patch = mock.patch.object(API, 'run_process', side_effect=process); patch.start(); self.addCleanup(patch.stop)
        baseline = self.home / 'baseline'; baseline.mkdir()
        resolved, fingerprints, dependencies, env, hashes = API._verify_environment(self.suite, self.plan, self.tools, {}, baseline)
        caches = FAMILY.selector_g1_cache_measurements(API, self.plan, self.tools)
        self.checked = {'prior': {'replay_evidence': {'tool_fingerprints': fingerprints, 'dependency_checks': dependencies, 'official_caches_before': caches}}}
        self.workspace = self.home / 'probe'; self.workspace.mkdir()

    def environment(self):
        return EXEC.environment_measurement(self.checked, self.plan, self.suite, self.tools, {}, self.workspace, api=API, family=FAMILY)

    def test_all_declared_tools_package_pins_and_cache_roots_measured(self):
        result = self.environment()
        self.assertEqual(set(result['caches']), {'lean'} | set(self.plan['packages']))
        self.assertEqual(len(result['dependencies']), 9); self.assertEqual(result['caches']['Cli']['files'], 0)
        events = json.loads((self.workspace / 'METADATA_PROCESSES.json').read_bytes())
        self.assertEqual(len(events), 21); self.assertTrue(all(row['credit'] == 'METADATA_ONLY' for row in events))

    def test_changed_executable_or_cache_refused(self):
        self.tools['lean'].write_bytes(b'changed')
        with self.assertRaises(ValueError): self.environment()
        self.tools['lean'].write_bytes(b'synthetic lean executable')
        (self.tools['mathlib'] / '.lake/build/lib/lean/Official.olean').write_bytes(b'changed')
        with self.assertRaises(ValueError): self.environment()

    def test_foreign_or_linked_cache_refused(self):
        extra = self.tools['mathlib'] / '.lake/packages/Foreign/.lake/build/lib/lean'; extra.mkdir(parents=True); (extra / 'Foreign.olean').write_bytes(b'extra')
        with self.assertRaises(ValueError): self.environment()


for _name in list(ExecutorTests.__dict__):
    if _name.startswith('test_') and _name not in EnvironmentTests.__dict__:
        setattr(EnvironmentTests, _name, None)


if __name__ == '__main__':
    if sys.version_info[:3] != (3, 11, 9) or not sys.dont_write_bytecode:
        raise ValueError('Pinned Python3.11.9 -B required')
    print(sys.version, 'optimized=' + str(sys.flags.optimize), flush=True)
    unittest.main(verbosity=2)
