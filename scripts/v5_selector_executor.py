"""Exact selector recollection and missing-audit execution. No producer replay."""
from contextlib import contextmanager
from copy import deepcopy
import json
import os
from pathlib import Path
import re
import subprocess
from unittest import mock
import zipfile


class AuditRefusal(ValueError):
    def __init__(self, message, outcome='FAILED'):
        super().__init__(message)
        self.outcome = outcome


@contextmanager
def readonly_collection():
    def forbidden(*args, **kwargs):
        raise ValueError('Retained selector recollection forbids processes and extraction')
    with mock.patch.object(subprocess, 'Popen', forbidden), mock.patch.object(subprocess, 'run', forbidden), \
            mock.patch.object(os, 'system', forbidden), mock.patch.object(zipfile.ZipFile, 'extract', forbidden), \
            mock.patch.object(zipfile.ZipFile, 'extractall', forbidden):
        yield


def output_path(output, protected, *, api):
    return api._ac_exec_output(output, protected, api)


def prepare(suite, sources, root, prior, tools, inputs, reviews, *, api, helper):
    a = api; family = a.selector_g1_load_family()
    a.require(suite['id'] == 'd06-selector' and a.canonical(suite) == helper.SC_SUITE, 'Wrong exact selector suite')
    plan = family.selector_g1_validate_suite(a, suite, sources, root)
    a.require(set(tools) == {'lean', 'lean-bin', 'python', 'mathlib'}, 'Missing or foreign selector tool binding')
    a.require(set(inputs) == set(plan['inputs']) | {'dependency-run', 'dependency-receipt', 'parent-custody-acceptance'}, 'Missing or foreign selector retained input')
    a.require(isinstance(reviews, dict) and set(suite['review_ids']) <= set(reviews), 'Current source reviews are missing')
    prior = a.no_symlinks(prior).absolute()
    raw = a.path_in(prior, 'RECEIPT.json').read_bytes(); failure = a.path_in(prior, 'FAILURE.json').read_bytes()
    a.require(a.sha(raw) == helper.SC_PRIOR_RAW and a.sha(failure) == helper.SC_FAILURE, 'Original failed selector receipt/failure changed')
    parent = a.no_symlinks(inputs['parent-custody-acceptance']).read_bytes()
    a.require(a.sha(parent) == helper.SC_PARENT_CUSTODY, 'Parent failure/custody acceptance changed')
    original = a.read_json(a.path_in(prior, 'RECEIPT.json'))
    binding = {'receipt': original, 'receipt_sha256': a.sha(raw), 'receipt_canonical_sha256': a.canonical(original),
        'receipt_bytes': len(raw), 'failure_sha256': a.sha(failure), 'parent_custody_acceptance_sha256': a.sha(parent)}
    helper._sc_prior({'prior': binding}, suite, sources, root, a, family, plan)
    review_sources = {}
    for rid in suite['review_ids']:
        review = reviews[rid]; sid = review['source_id']; digest = a.sha(a.public_bytes(root, sources[sid]))
        a.require(digest == review['review_sha256'] == original['review_hashes'][rid], 'Source-bound current review changed')
        review_sources[rid] = {'source_id': sid, 'sha256': digest}
    context = a.read_json(a.path_in(prior, 'TRACE_CONTEXT.json'))
    a.require(Path(context['out']) == prior / 'original' and Path(context['cwd']) == prior / 'project'
        and Path(context['trace']) == prior / 'traces/original-selector', 'Retained selector context points elsewhere')
    a.require(Path(context['dependency_run']).resolve() == Path(inputs['dependency-run']).resolve(), 'Qualified core root changed')
    for key in ('lean', 'python', 'mathlib'):
        a.require(Path(tools[key]).resolve() == Path(context[key]).resolve(), 'Retained tool location changed')
    a.require(Path(tools['lean-bin']).resolve() == Path(tools['lean']).resolve().parent, 'Lean aliases differ')
    a.require(set(context['archives']) == set(plan['inputs']), 'Retained source archive set differs')
    for key in plan['inputs']:
        a.require(Path(inputs[key]).resolve() == Path(context['archives'][key]).resolve(), 'Original archive location changed')
    return {'prior': original, 'binding': binding, 'context': context, 'review_sources': review_sources}, plan, family


def measure_retained(checked, plan, suite, prior, inputs, root, sources, *, api, helper, family):
    a = api; old = checked['prior']['replay_evidence']; context = checked['context']
    custody = helper.selector_custody(prior, api=a)
    a.require(a.canonical(custody) == helper.SC_CUSTODY, 'Selector typed custody changed')
    project = a._file_hashes(a.path_in(prior, 'project'))
    a.require(project == helper.SC_PROJECT, 'Retained selector project changed')
    for sid, row in plan['files'].items():
        a.require(a.path_in(prior / 'project', row['path']).read_bytes() == plan['contents'][sid], 'Retained selected source changed')
    hashes = {sid: a.sha(a.public_bytes(root, sources[sid])) for sid in suite['source_ids']}
    a.require(hashes == checked['prior']['source_hashes'], 'Current public selector source changed')
    reviews = {rid: a.sha(a.public_bytes(root, sources[row['source_id']])) for rid, row in checked.get('review_sources', {}).items()}
    a.require(reviews == {rid: row['sha256'] for rid, row in checked.get('review_sources', {}).items()}, 'Current review source changed')
    inventories = {key: family.selector_g1_inventory(a, Path(path)) for key, path in context['roots'].items()}
    a.require(inventories == old['source_inventory_before'], 'Original complete source packet changed')
    objects = a._ac_exec_objects(prior, old['output_hashes'], suite['replay']['build_roots'], a)
    with readonly_collection():
        core = family.selector_g1_dependency_join(a, 'selector', context, inputs, root, sources)
    a.require(a.canonical(core) == helper.SC_CORE_REUSE, 'Qualified core source/object/transitive join changed')
    core_suite = family.selector_g1_catalog(a)['core_suite']
    core_objects = a._ac_exec_objects(Path(inputs['dependency-run']), old['dependency_reuse']['identity']['objects'], core_suite['replay']['build_roots'], a)
    parent_raw = a.no_symlinks(inputs['parent-custody-acceptance']).read_bytes()
    a.require(a.sha(parent_raw) == helper.SC_PARENT_CUSTODY, 'Parent failure/custody acceptance changed')
    return {'custody_sha256': a.canonical(custody), 'project_sha256': project, 'source_hashes': hashes, 'review_hashes': reviews,
            'source_inventory': inventories, 'objects': objects, 'core_objects': core_objects,
            'core_reuse_sha256': a.canonical(core), 'parent_custody_acceptance_sha256': a.sha(parent_raw)}


def environment_measurement(checked, plan, suite, tools, inputs, workspace, *, api, family):
    a = api; old = checked['prior']['replay_evidence']; environment_suite = deepcopy(suite)
    environment_suite['replay']['build_roots'] = []
    git = Path(a.shutil.which('git') or '')
    a.require(git.is_file() and a.sha(git.read_bytes()) == family.SELECTOR_G1_GIT_SHA256, 'Metadata Git executable changed')
    a.require(all(row['kind'] == 'GIT' for row in plan['packages'].values()), 'Unreviewed selector package kind')
    definitions = {'lean': {**suite['toolchain'], 'path_kind': 'EXECUTABLE'}}
    definitions.update({row['name']: row for row in suite['replay']['tools']})
    allowed = set()
    for name, definition in definitions.items():
        executable = Path(tools[name]).absolute()
        if definition['path_kind'] == 'BIN_DIRECTORY': executable /= 'lean' if definition['kind'] == 'LEAN' else 'python'
        elif definition['path_kind'] == 'DISTRIBUTION_ROOT': executable = executable / 'bin' / ('lean' if definition['kind'] == 'LEAN' else 'python')
        allowed.add((str(executable), '--version'))
    for row in plan['packages'].values():
        repo = str(a.path_in(tools['mathlib'], row['path'], dot=True))
        allowed.add((str(git), '-C', repo, 'rev-parse', 'HEAD'))
        allowed.add((str(git), '-C', repo, 'status', '--porcelain', '--untracked-files=no'))
    original_process = a.run_process; namespace = a._verify_environment.__globals__; events = []
    a.require(namespace.get('run_process') is original_process, 'Environment probe runner is not the shared reviewed runner')
    def metadata_process(argv, cwd, env, log, timeout):
        vector = tuple(str(value) for value in argv)
        a.require(vector in allowed and Path(cwd) == workspace and timeout == 30, 'Selector prerequisite attempted a nonmetadata command')
        a.require(Path(log).absolute().is_relative_to(workspace.absolute()), 'Metadata log escaped fresh output')
        run = original_process(argv, cwd, env, log, timeout)
        events.append({'argv': list(vector), 'cwd': str(cwd), 'log_path': str(log), 'timeout_seconds': timeout,
            'credit': 'METADATA_ONLY', **run})
        a.write_json(workspace / 'METADATA_PROCESSES.json', events)
        return run
    try:
        namespace['run_process'] = metadata_process
        resolved, fingerprints, dependencies, env, input_hashes = a._verify_environment(environment_suite, plan, tools,
            {key: inputs[key] for key in plan['inputs']}, workspace)
    finally:
        namespace['run_process'] = original_process
        a.write_json(workspace / 'METADATA_PROCESSES.json', events)
    a.require(fingerprints == old['tool_fingerprints'] and dependencies == old['dependency_checks'], 'Current tools or all package pins differ')
    caches = family.selector_g1_cache_measurements(a, plan, tools)
    a.require(caches == old['official_caches_before'], 'Current official cache census differs')
    libraries = [*family.selector_g1_verified_library_paths(a, plan, tools), Path(resolved['lean']).resolve().parent.parent / 'lib/lean']
    return {'resolved': resolved, 'fingerprints': fingerprints, 'dependencies': dependencies, 'input_hashes': input_hashes,
        'caches': caches, 'libraries': [str(path) for path in libraries], 'env': env}


def recollect(checked, plan, prior, output, suite, *, api, helper, family):
    a = api; old = checked['prior']['replay_evidence']; parent = a.indexed(old['stage_results'])['original-selector']
    started = a.utc(); context = checked['context']
    with readonly_collection():
        collection = family.selector_g1_collect(a, 'selector', context, parent, prior)
        a.require(a.canonical(collection) == helper.SC_COLLECTION, 'Complete retained collection changed')
        events = family.selector_g1_events(a, 'selector', context)
    raw = a.indexed(collection['child_observations'], 'source_child_id')
    originals = {row['id']: row for row in events['children']}; stages = []; observations = []; diagnostics = []
    for spec in suite['replay']['stages'][1:]:
        a.require(spec['argv'][:1] == ['{builtin:observe-child}'] and spec['argv'][1] == 'original-selector', 'Selector observation would execute a new source stage')
        began = a.utc(); child = raw[spec['argv'][2]]
        log = a.no_symlinks(originals[child['source_child_id']]['log']).read_bytes()
        a.require(a.sha(log) == child['log_sha256'], 'Original observed child log changed')
        target = a.path_in(output, 'logs/observed/' + spec['id'] + '.log'); target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream: stream.write(log)
        ended = a.utc()
        stages.append({'id': spec['id'], 'argv': spec['argv'], 'cwd': spec['cwd'], 'budget_seconds': spec['timeout_seconds'],
            'started_at': began, 'ended_at': ended, 'terminal': child['terminal'], 'exit_code': child['exit_code'], 'log_sha256': child['log_sha256'], 'output_hashes': {}})
        observations.append({**child, 'stage_id': spec['id'], 'parent_stage_id': 'original-selector',
            'physical_run_sha256': collection['trace_sha256'], 'parent_log_sha256': parent['log_sha256'], 'observed_at': ended})
        for cid in spec['control_ids']:
            diagnostics.append({'control_id': cid, 'stage_id': spec['id'], 'prerequisite_stage_ids': spec['depends_on'],
                'expected': spec['expected_diagnostics'], 'observed_log_sha256': child['log_sha256'], 'match': 'MATCHED'})
    result = {'parser_id': 'selector-exact-source-collector-v1', 'collector_runner_sha256': a.sha(Path(a.__file__).read_bytes()),
        'observed_at': started, 'collection': collection, 'stage_results': stages, 'child_observations': observations, 'control_diagnostics': diagnostics}
    a.write_json(output / 'RETAINED_COLLECTION.json', result)
    return result


def audit_result(run, raw, targets, *, api):
    a = api; terminal, code = run['terminal'], run['exit_code']
    if terminal in {'TIMEOUT', 'INTERRUPTED'}:
        a.require(code is None, 'Resource terminal has a fabricated process exit')
        return 'RESOURCE_INCONCLUSIVE', {}
    a.require(terminal == 'COMPLETED' and type(code) is int and 0 <= code < 124, 'Invalid actual audit terminal')
    text = raw.decode('utf-8')
    if re.search(r'timed out|out of memory|maximum (?:number of heartbeats|recursion depth)|deterministic timeout|WALL_CLOCK_LIMIT', text, re.I):
        # v1 cannot represent this semantic resource result by changing its
        # actual COMPLETED/exit facts. Preserve a private refusal instead.
        raise AuditRefusal('Completed audit reported resource exhaustion', 'RESOURCE_INCONCLUSIVE')
    if code:
        return 'FAILED', {}
    a.require(not re.search(r'error:|warning:|sorryAx|UNCHECKED_DEPENDENCY|UNSAFE_OR_PARTIAL_DEPENDENCY|INCOMPLETE_PROOF_CLOSURE', text), 'Audit has a diagnostic or unsafe closure')
    a.require(len(targets) == 7, 'Selector audit target census changed')
    return 'QUALIFIED_DECLARED_SUITE', a.parse_readbacks(text, targets)


def audit_once(output, plan, resolved, env, *, api, helper, family):
    a = api; targets = list(plan['targets'].values())
    a.require(len(targets) == 7, 'Selector audit needs the seven exact targets')
    body = family.selector_g1_audit_source(a, targets).encode()
    a.require(a.sha(body) == helper.SC_AUDITOR, 'Exact selector auditor changed')
    generated = a.path_in(output, 'generated'); a.require(not generated.exists(), 'Generated auditor must be fresh'); generated.mkdir()
    path = generated / 'V5SuccessorReadback.lean'
    with path.open('xb') as stream:
        stream.write(body)
    argv = [resolved['lean'], '-j1', path]; cwd = a.path_in(output, 'project'); log = output / 'logs/target-audit.log'
    invocation = {'argv': [str(value) for value in argv], 'cwd': str(cwd), 'timeout_seconds': 300,
        'lean_path': env['LEAN_PATH'].split(os.pathsep), 'generated_source_sha256': helper.SC_AUDITOR,
        'scope': 'ONE_EXACT_SELECTOR_TARGET_AUDIT_NO_PRODUCER_OR_OBJECT_BUILD'}
    a.write_json(output / 'RESOLVED_AUDIT_INVOCATION.json', invocation)
    run = a.run_process(argv, cwd, env, log, 300)
    a.write_json(output / 'AUDIT_PROCESS.json', run)
    raw = a.no_symlinks(log).read_bytes()
    a.require(a.sha(raw) == run['log_sha256'], 'Actual audit log changed after process return')
    return run, raw, invocation


def compose_receipt(checked, plan, suite, collection, retained_inputs, pre, run, raw, invocation, started, ended, *, api, helper):
    a = api; prior = checked['prior']; old = prior['replay_evidence']
    outcome, audits = audit_result(run, raw, list(plan['targets'].values()), api=a)
    success = outcome == 'QUALIFIED_DECLARED_SUITE'
    stage = {'id': '_target_audit', 'argv': ['{tool:lean}', '-j1', '{out}/generated/V5SuccessorReadback.lean'],
        'cwd': '.', 'budget_seconds': 300, **run, 'output_hashes': {}}
    stages = [deepcopy(pre), stage]; controls = []; children = a.indexed(collection['child_observations'], 'stage_id')
    expected = a.indexed(suite['controls'])
    for spec in suite['replay']['stages'][1:]:
        child = children[spec['id']]
        for cid in spec['control_ids']:
            control = expected[cid]; actual = child['actual_outcome']
            a.require(actual == control['expected_outcome'], 'Retained source control differs')
            controls.append({key: control[key] for key in ('id', 'source_id', 'target_id', 'role', 'expected_outcome_sha256')} | {
                'actual_outcome': actual, 'actual_outcome_sha256': a.sha(actual.encode()), 'terminal': child['terminal'],
                'exit_code': child['exit_code'], 'log_sha256': child['log_sha256']})
    evidence = {key: deepcopy(old[key]) for key in helper.SC_COMMON}
    evidence.update(schema=helper.SC_SCHEMA, runner_sha256=a.sha(Path(a.__file__).read_bytes()),
        continuation_module_sha256=a.sha(Path(helper.__file__).read_bytes()),
        cache_policy='RETAINED_SELECTOR_AND_QUALIFIED_CORE_FRESH_TARGET_AUDIT_ONLY',
        stage_results=stages, target_audits=[{'target_id': tid, **row, 'stage_id': '_target_audit', 'log_sha256': run['log_sha256']} for tid, row in audits.items()],
        output_hashes={'generated/V5SuccessorReadback.lean': helper.SC_AUDITOR}, prior=deepcopy(checked['binding']),
        retained_custody=helper._sc_custody_binding(), retained_collection=deepcopy(collection),
        retained_inputs=deepcopy(retained_inputs), accounting=deepcopy(helper.SC_ACCOUNTING),
        fresh_audit={'recipe': 'selector-retained-closure-audit-v1', 'generated_source_sha256': helper.SC_AUDITOR,
            'resolved_invocation_sha256': a.canonical(invocation), 'argv_provenance': 'RESOLVED_FROM_BOUND_INPUTS',
            'library_roots': ['{prior}/original/build', '{qualified-core}/original/runtime/build', '{pinned-official-caches}'],
            'traversal_bound': 1000000, 'distinct_declaration_accounting': 'ENQUEUE_ONCE_NO_DEPENDENCY_DROPPED', 'fresh_custom_objects': 0})
    receipt = {key: deepcopy(prior[key]) for key in ('suite_id', 'family', 'suite_sha256', 'source_hashes', 'review_hashes', 'toolchain_sha256')}
    receipt.update(id='d06-selector-audit-continuation-' + a.sha((started + a.canonical(invocation)).encode())[:16],
        invocation=['replay_v5_successors.py', '--selector-audit-continuation', '--suite', 'd06-selector', '--prior', '{prior}', '--out', '{out}'],
        outcome=outcome, proof_scope='DECLARED_SUITE' if success else 'NONE', exit_code=0 if success else 1,
        started_at=started, ended_at=ended, controls=controls,
        stages=[{key: row[key] for key in ('id', 'terminal', 'exit_code', 'log_sha256')} for row in stages],
        log_sha256=a.canonical({row['id']: row['log_sha256'] for row in stages}),
        axioms=sorted({axis for row in audits.values() for axis in row['axioms']}),
        target_readbacks=[{'target_id': row['id'], 'source_id': row['source_id'], 'target_sha256': row['target_sha256'], 'outcome': 'CHECKED'} for row in suite['targets']] if success else [],
        replay_evidence=evidence)
    return receipt


def write_refusal(output, started, run, error, *, api, helper):
    a = api; process_file = output / 'AUDIT_PROCESS.json'
    if run is None and process_file.is_file():
        run = a.read_json(a.no_symlinks(process_file))
    metadata = []
    for phase in ('prerequisites-before', 'prerequisites-after'):
        path = output / phase / 'METADATA_PROCESSES.json'
        if path.is_file(): metadata.extend(a.read_json(a.no_symlinks(path)))
    resource = (run is not None and run.get('terminal') in {'TIMEOUT', 'INTERRUPTED'}) or any(
        row.get('terminal') in {'TIMEOUT', 'INTERRUPTED'} for row in metadata) or isinstance(error, KeyboardInterrupt)
    outcome = getattr(error, 'outcome', 'RESOURCE_INCONCLUSIVE' if resource else 'FAILED')
    a.write_json(output / 'REFUSAL.json', {'status': 'SELECTOR_CONTINUATION_REFUSED', 'outcome': outcome, 'proof_scope': 'NONE',
        'started_at': started, 'ended_at': a.utc(), 'audit_process': run, 'error': type(error).__name__ + ': ' + str(error),
        'prior_receipt_sha256': helper.SC_PRIOR_RAW, 'parent_custody_acceptance_sha256': helper.SC_PARENT_CUSTODY,
        'qualified_receipt_written': False})


def execute(suite, sources, root, prior, output, tools, inputs, *, reviews=None, api, helper):
    a = api; root = Path(root); prior = a.no_symlinks(prior).absolute()
    protected = [root, prior, *inputs.values(), *tools.values(), Path(a.__file__).parent, Path(helper.__file__).parent]
    output = output_path(output, protected, api=a)
    checked, plan, family = prepare(suite, sources, root, prior, tools, inputs, reviews, api=a, helper=helper)
    pins = {str(path): a.sha(path.read_bytes()) for path in (Path(a.__file__), Path(helper.__file__), Path(__file__), Path(family.__file__))}
    output.mkdir(parents=True); (output / 'logs').mkdir(); project = output / 'project'; project.mkdir()
    started = a.utc(); run = None
    a.write_json(output / 'ATTEMPT.json', {'schema': 'selector-audit-only-private-attempt-v1', 'started_at': started,
        'prior_receipt_sha256': helper.SC_PRIOR_RAW, 'parent_custody_acceptance_sha256': helper.SC_PARENT_CUSTODY,
        'scope': 'RECOLLECT_RETAINED_SELECTOR_AND_EXECUTE_ONLY_MISSING_TARGET_AUDIT'})
    try:
        for sid, row in plan['files'].items():
            path = a.path_in(project, row['path']); path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as stream: stream.write(plan['contents'][sid])
        before = measure_retained(checked, plan, suite, prior, inputs, root, sources, api=a, helper=helper, family=family)
        phase = output / 'prerequisites-before'; phase.mkdir()
        env_before = environment_measurement(checked, plan, suite, tools, inputs, phase, api=a, family=family)
        libraries = [str(a.path_in(prior, 'original/build')), str(a.path_in(inputs['dependency-run'], 'original/runtime/build')), *env_before['libraries']]
        a.require(len(libraries) == len(set(libraries)), 'Duplicate selector audit library root')
        for library in libraries: a.no_symlinks(library)
        env = dict(env_before['env']); env['LEAN_PATH'] = os.pathsep.join(libraries)
        a.write_json(output / 'RETAINED_INPUT_CHECKS_BEFORE.json', {**before, 'official_caches': env_before['caches']})
        prelog = output / 'logs/prerequisites.log'
        prelog.write_text('Exact failed selector, current sources/reviews/tools/packages, retained selector/core objects and no-follow custody verified.\n', encoding='utf-8')
        pre = {'id': '_prerequisites', 'argv': ['{builtin:prerequisites}'], 'cwd': '.', 'budget_seconds': 30,
            'started_at': started, 'ended_at': a.utc(), 'terminal': 'COMPLETED', 'exit_code': 0, 'log_sha256': a.sha(prelog.read_bytes()), 'output_hashes': {}}
        collection = recollect(checked, plan, prior, output, suite, api=a, helper=helper, family=family)
        audit_error = None
        try:
            run, raw, invocation = audit_once(output, plan, env_before['resolved'], env, api=a, helper=helper, family=family)
        except (ValueError, OSError, KeyError, TypeError, KeyboardInterrupt) as error:
            audit_error = error
        # A post-return association refusal still receives physical postchecks.
        phase = output / 'prerequisites-after'; phase.mkdir(); post_errors = []
        try:
            env_after = environment_measurement(checked, plan, suite, tools, inputs, phase, api=a, family=family)
            a.require(env_after == env_before, 'Sources/tools/packages/inputs/cache libraries changed during audit')
        except (ValueError, OSError, KeyError, TypeError, KeyboardInterrupt) as error:
            post_errors.append(error)
        try:
            after = measure_retained(checked, plan, suite, prior, inputs, root, sources, api=a, helper=helper, family=family)
            a.require(after == before, 'Retained selector or qualified core changed during audit')
            a.write_json(output / 'RETAINED_INPUT_CHECKS_AFTER.json', after)
        except (ValueError, OSError, KeyError, TypeError, KeyboardInterrupt) as error:
            post_errors.append(error)
        if post_errors:
            a.write_json(output / 'POSTFLIGHT_REFUSAL.json', {'errors': [type(error).__name__ + ': ' + str(error) for error in post_errors]})
            raise post_errors[0]
        if audit_error is not None: raise audit_error
        for path, digest in pins.items():
            a.require(a.sha(a.no_symlinks(path).read_bytes()) == digest, 'Executor/validator/source adapter changed during audit')
        expected_project = a.canonical({row['path']: a.sha(plan['contents'][sid]) for sid, row in plan['files'].items()})
        a.require(a._file_hashes(project) == expected_project, 'Fresh selected source projection changed')
        a.require(not list(output.rglob('*.olean')), 'Continuation created a custom compiler object')
        a.require(a.sha(a.path_in(output, 'generated/V5SuccessorReadback.lean').read_bytes()) == helper.SC_AUDITOR, 'Generated audit source changed')
        a.require(a.path_in(output, 'logs/target-audit.log').read_bytes() == raw and a.sha(raw) == run['log_sha256'], 'Audit log changed during postflight')
        a.require(a.read_json(output / 'RESOLVED_AUDIT_INVOCATION.json') == invocation, 'Resolved audit invocation changed')
        retained_inputs = {'project_before_sha256': before['project_sha256'], 'project_after_sha256': after['project_sha256'],
            'source_inventory_before': before['source_inventory'], 'source_inventory_after': after['source_inventory'],
            'objects_before': before['objects'], 'objects_after': after['objects'],
            'core_reuse_before_sha256': before['core_reuse_sha256'], 'core_reuse_after_sha256': after['core_reuse_sha256'],
            'official_caches_before': env_before['caches'], 'official_caches_after': env_after['caches']}
        receipt = compose_receipt(checked, plan, suite, collection, retained_inputs, pre, run, raw, invocation, started, a.utc(), api=a, helper=helper)
        helper.validate_selector_continuation(receipt, suite, sources, root, api=a)
        a.write_json(output / 'RECEIPT.json', receipt)
        return receipt
    except (ValueError, OSError, KeyError, TypeError, KeyboardInterrupt) as error:
        write_refusal(output, started, run, error, api=a, helper=helper)
        raise
