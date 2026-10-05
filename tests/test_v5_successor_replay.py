"""Adversarial boundaries for the source-bound successor replay interface."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import subprocess
import tempfile
import types
import unittest
import zipfile
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/replay_v5_successors.py'
LEAN_SHA = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
AREA = 'experiments/orthemology-v5-successors/source-store'


def sha(value):
    return hashlib.sha256(value.encode() if isinstance(value, str) else value).hexdigest()


def canonical(value):
    return sha(json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(',', ':'), allow_nan=False))


def add_source(root, sources, sid, filename, body):
    data = body.encode()
    digest = sha(data)
    relative = AREA + '/' + digest + '/' + filename
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    sources[sid] = {'id': sid, 'origin_input_id': 'FIXTURE', 'origin_input_sha256': 'a' * 64,
                    'origin_archive_sha256': 'b' * 64, 'member_chain': [filename],
                    'original_sha256': digest, 'original_bytes': len(data), 'public_path': relative,
                    'public_sha256': digest, 'public_bytes': len(data), 'projection': 'EXACT',
                    'projection_basis': 'Synthetic adversarial fixture.', 'review_scope': 'Fixture only.',
                    'derivation': None}
    return sid


def fixture(root):
    sources = {}
    add_source(root, sources, 'proof', 'Proof.lean', 'import Init\nnamespace Fixture\ntheorem ok : True := True.intro\nend Fixture\n')
    add_source(root, sources, 'bad', 'BadProof.lean', 'import Proof\nexample : False := True.intro\n')
    add_source(root, sources, 'guide', 'Contract.md', 'The negative control must report type mismatch after the positive proof.\n')
    stages = [
        {'id': 'positive', 'kind': 'LEAN_COMPILE', 'driver_id': None,
         'argv': ['{tool:lean}', '-j1', '-o', '{build}/Proof.olean', '{project}/Proof.lean'],
         'cwd': '.', 'depends_on': [], 'timeout_seconds': 30, 'output_paths': ['build/Proof.olean'],
         'control_ids': ['positive'], 'expected_exit_codes': [0], 'expected_diagnostics': []},
        {'id': 'negative', 'kind': 'NEGATIVE_CONTROL', 'driver_id': None,
         'argv': ['{tool:lean}', '-j1', '{project}/BadProof.lean'], 'cwd': '.',
         'depends_on': ['positive'], 'timeout_seconds': 30, 'output_paths': [],
         'control_ids': ['negative'], 'expected_exit_codes': [1],
         'expected_diagnostics': [{'source_id': 'guide', 'literal': 'type mismatch', 'sha256': sha('type mismatch')}]},
    ]
    replay = {'schema': 'orthemology-v5-replay-v1', 'scope': 'COMPONENTS',
        'files': [{'source_id': sid, 'path': name, 'role': role} for sid, name, role in
                  [('proof', 'Proof.lean', 'PROOF'), ('bad', 'BadProof.lean', 'NEGATIVE'), ('guide', 'Contract.md', 'REVIEW')]],
        'modules': [{'name': 'Proof', 'source_id': 'proof', 'imports': ['Init']},
                    {'name': 'BadProof', 'source_id': 'bad', 'imports': ['Init', 'Proof']}],
        'module_order': ['Proof'], 'positive_roots': ['Proof'], 'audit_roots': [],
        'negative_roots': ['BadProof'], 'runtime_roots': [],
        'official_imports': [
            {'module': 'Init', 'package': 'lean-release', 'path': 'Init.lean',
             'sha256': '94c76e813fdf92a0375566c1c7f3335cf269703da809c6189dc0de09d66b0204'},
            {'module': 'Lean.Elab.Command', 'package': 'lean-release', 'path': 'Lean/Elab/Command.lean',
             'sha256': 'ada0e6af60d9f4b2ab1538eecb73e5c34a9a742e462c835ae34bdddc60794be7'},
            {'module': 'Lean.Util.CollectAxioms', 'package': 'lean-release', 'path': 'Lean/Util/CollectAxioms.lean',
             'sha256': '26e92bcf497bd81e3a236e648c2dc75b19d084f0e929c5dea43376437fe4355a'}],
        'target_names': [{'target_id': 'main', 'module': 'Proof', 'name': 'Fixture.ok'}],
        'package_manifest_source_id': None, 'packages': [], 'tools': [], 'external_inputs': [],
        'fixtures': [], 'drivers': [], 'stages': stages, 'build_roots': ['build']}
    statement = 'theorem ok : True := True.intro'
    controls = [{'id': cid, 'source_id': sid, 'target_id': 'main', 'role': role,
                 'expected_outcome': outcome, 'expected_outcome_sha256': sha(outcome)}
                for cid, sid, role, outcome in [('positive', 'proof', 'POSITIVE', 'ACCEPT'),
                                               ('negative', 'bad', 'MUTATION_REJECTION', 'REJECT')]]
    suite = {'id': 'fixture', 'family': 'fixture', 'result_families': ['fixture'],
             'origin_archive_sha256': 'b' * 64, 'source_ids': list(sources), 'review_ids': ['review'],
             'targets': [{'id': 'main', 'source_id': 'proof', 'declaration': statement,
                          'target_sha256': sha(statement), 'domain': 'SOURCE_TEXT', 'calculus': 'NONE'}],
             'controls': controls, 'toolchain': {'kind': 'LEAN', 'version': '4.19.0',
             'platform': 'linux-x86_64', 'executable_sha256': LEAN_SHA, 'packages': []}, 'replay': replay}
    return suite, sources, {'review': {'review_sha256': sources['guide']['public_sha256']}}


class SuccessorReplayTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = None
        if SCRIPT.exists():
            spec = importlib.util.spec_from_file_location('successor_replay_under_test', SCRIPT)
            cls.r = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(cls.r)

    def setUp(self):
        self.assertIsNotNone(self.r, 'Successor replay implementation is absent')
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.root = self.base / 'repo'
        self.root.mkdir()
        self.suite, self.sources, self.reviews = fixture(self.root)

    def validate(self):
        return self.r.validate_suite(self.suite, self.sources, self.root)

    def test_exact_manifest_projects_original_bytes_only(self):
        self.validate()
        self.r.project_suite(self.suite, self.sources, self.root, self.base / 'out')
        self.assertEqual((self.base / 'out/project/Proof.lean').read_bytes(),
                         (self.root / self.sources['proof']['public_path']).read_bytes())
        self.assertFalse(list((self.base / 'out').rglob('*.olean')))

    def test_swapped_source_fails_before_output_creation(self):
        (self.root / self.sources['proof']['public_path']).write_text('changed')
        with self.assertRaises(ValueError):
            self.r.project_suite(self.suite, self.sources, self.root, self.base / 'out')
        self.assertFalse((self.base / 'out').exists())

    def test_unknown_field_and_bool_budget_fail(self):
        self.suite['replay']['undeclared'] = True
        with self.assertRaises(ValueError): self.validate()
        del self.suite['replay']['undeclared']
        self.suite['replay']['stages'][0]['timeout_seconds'] = True
        with self.assertRaises(ValueError): self.validate()

    def test_components_cannot_self_declare_complete_original_suite(self):
        self.suite['replay']['scope'] = 'DECLARED_SUITE'
        with self.assertRaises(ValueError): self.validate()

    def test_python_bytecode_cannot_enter_a_source_projection(self):
        add_source(self.root, self.sources, 'bytecode', 'json.pyc', 'not admitted even when UTF-8')
        self.suite['source_ids'].append('bytecode')
        self.suite['replay']['files'].append({'source_id': 'bytecode', 'path': 'json.pyc', 'role': 'DATA'})
        with self.assertRaises(ValueError): self.validate()

    def test_reviewed_suite_approval_binds_sources_targets_and_control_roles(self):
        self.suite['replay']['scope'] = 'DECLARED_SUITE'
        approved = self.r.declared_suite_fingerprint(self.suite, self.sources)
        with mock.patch.dict(self.r.APPROVED_DECLARED_SUITES, {self.suite['id']: approved}):
            self.validate()
            original = copy.deepcopy(self.suite)
            self.suite['targets'][0]['target_sha256'] = 'f' * 64
            with self.assertRaises(ValueError): self.validate()
            self.suite = copy.deepcopy(original)
            self.suite['controls'][0]['role'] = 'COUNTEREXAMPLE_PROOF'
            with self.assertRaises(ValueError): self.validate()
            self.suite = original
            self.sources[self.suite['source_ids'][0]]['public_sha256'] = 'e' * 64
            self.assertNotEqual(approved, self.r.declared_suite_fingerprint(self.suite, self.sources))

    def test_module_alias_or_unequal_namespace_collision_fails(self):
        self.suite['replay']['modules'][1]['name'] = 'Proof'
        with self.assertRaises(ValueError): self.validate()

    def test_quarantined_fixture_path_is_not_an_imported_module_identifier(self):
        self.suite['replay']['files'][1]['path'] = 'verification/negative-controls/BadProof.lean'
        self.suite['replay']['modules'][1]['name'] = 'verification.negative-controls.BadProof'
        self.suite['replay']['negative_roots'] = ['verification.negative-controls.BadProof']
        self.suite['replay']['stages'][1]['argv'][-1] = '{project}/verification/negative-controls/BadProof.lean'
        self.validate()

    def test_standalone_positive_fixture_path_cannot_become_an_import_or_object(self):
        self.suite['replay']['files'][1]['path'] = 'verification/positive-controls/BadProof.lean'
        self.suite['replay']['files'][1]['role'] = 'AUDIT'
        self.suite['replay']['modules'][1]['name'] = 'verification.positive-controls.BadProof'
        self.suite['replay']['negative_roots'] = []
        self.suite['replay']['audit_roots'] = ['verification.positive-controls.BadProof']
        stage = self.suite['replay']['stages'][1]
        stage['kind'] = 'POSITIVE_CONTROL'; stage['expected_exit_codes'] = [0]; stage['expected_diagnostics'] = []
        stage['argv'][-1] = '{project}/verification/positive-controls/BadProof.lean'
        self.suite['controls'][1].update(role='POSITIVE', expected_outcome='ACCEPT', expected_outcome_sha256=sha('ACCEPT'))
        self.validate()
        self.suite['replay']['module_order'].append('verification.positive-controls.BadProof')
        with self.assertRaises(ValueError): self.validate()

    def test_original_assert_source_checker_cannot_run_optimized_or_arbitrary_args(self):
        driver = {'id': 'source-check', 'recipe': 't11-substitution-source-check-v1'}
        plan = {'drivers': {'source-check': driver}}
        stage = {'kind': 'SOURCE_CHECK', 'driver_id': 'source-check', 'cwd': '.', 'output_paths': [],
                 'argv': ['{tool:python}', '-B', '{driver:source-check}']}
        self.r._validate_argv(stage, plan)
        for args in [['{tool:python}', '-O', '{driver:source-check}'], stage['argv'] + ['--unchecked']]:
            with self.assertRaises(ValueError): self.r._validate_argv({**stage, 'argv': args}, plan)

    def test_t14_source_checker_prevalidates_exact_selected_root_paths(self):
        r = self.r
        records = [{'file': 'Root' + str(i) + '.lean', 'sha256': sha('theorem ok : True := True.intro\n')} for i in range(65)]
        for row in records[53:]: row['bytes'] = len(b'theorem ok : True := True.intro\n')
        lock = {'baseline': records[:53], 'intensional': records[53:59], 'extensional': records[59:]}
        values = {row['file']: b'theorem ok : True := True.intro\n' for row in records}
        values.update({'verification/verify_sources.py': b'# synthetic checker\n',
                       'verification/source-lock.json': json.dumps(lock).encode(),
                       'lakefile.lean': b'import Lake\n', 'lake-manifest.json': b'{}', 'lean-toolchain': b'leanprover/lean4:v4.19.0'})
        plan = {'files': {name: {'path': name} for name in values},
                'file_paths': {name: {'source_id': name} for name in values}, 'contents': values}
        driver = {'recipe': 't14-identity-verify_sources-v1', 'source_id': 'verification/verify_sources.py'}
        r.source_checker_inputs(driver, plan)
        for changed in ['../Root0.lean', '/Root0.lean', 'verification/../Root0.lean', 'Missing.lean']:
            with self.subTest(path=changed):
                bad = copy.deepcopy(plan); invalid = copy.deepcopy(lock); invalid['baseline'][0]['file'] = changed
                bad['contents']['verification/source-lock.json'] = json.dumps(invalid).encode()
                with self.assertRaises(ValueError): r.source_checker_inputs(driver, bad)
        bad = copy.deepcopy(plan); bad['contents']['Root0.lean'] += b'-- substituted\n'
        with self.assertRaises(ValueError): r.source_checker_inputs(driver, bad)
        bad = copy.deepcopy(plan); invalid = copy.deepcopy(lock); invalid['intensional'][0]['bytes'] = True
        bad['contents']['verification/source-lock.json'] = json.dumps(invalid).encode()
        with self.assertRaises(ValueError): r.source_checker_inputs(driver, bad)
        bad = copy.deepcopy(plan); bad['file_paths']['verification/json.py'] = {'source_id': 'shadow'}
        with self.assertRaises(ValueError): r.source_checker_inputs(driver, bad)

    def test_t14_original_type_control_requires_exactly_one_intended_error(self):
        stage = {'kind': 'NEGATIVE_CONTROL', 'argv': ['{tool:lean}', '-j1', '{project}/verification/negative-controls/Bad.lean']}
        log = 'verification/negative-controls/Bad.lean:5:0: error: application type mismatch\n  given : False\n'
        self.r.check_t14_stage(stage, log, {})
        for text in [log + 'Other.lean:1:0: error: type mismatch\n', log.replace('application type mismatch', 'unknown constant'), 'type mismatch\n']:
            with self.subTest(text=text), self.assertRaises(ValueError): self.r.check_t14_stage(stage, text, {})

    def test_original_checksum_preflight_covers_every_projected_package_file(self):
        values = {'.gitignore': b'.lake\n', 'README.md': b'Original source contract.\n'}
        values['SHA256SUMS'] = ''.join(sha(data) + '  ' + name + '\n' for name, data in values.items()).encode()
        plan = {'file_paths': {name: {'source_id': name} for name in values}, 'contents': values}
        self.r.check_checksum_manifest(plan, 2)
        for changed in [values['SHA256SUMS'].replace(b'README.md', b'../README.md'),
                        values['SHA256SUMS'].splitlines(keepends=True)[0],
                        values['SHA256SUMS'] + values['SHA256SUMS'].splitlines(keepends=True)[0]]:
            bad = copy.deepcopy(plan); bad['contents']['SHA256SUMS'] = changed
            with self.assertRaises(ValueError): self.r.check_checksum_manifest(bad, 2)
        bad = copy.deepcopy(plan); bad['contents']['README.md'] += b'changed'
        with self.assertRaises(ValueError): self.r.check_checksum_manifest(bad, 2)

    def test_tool_directory_arguments_preserve_their_declared_meaning(self):
        exe = self.base / 'distribution/bin/lean'
        for kind, expected in [('EXECUTABLE', exe), ('BIN_DIRECTORY', exe.parent), ('DISTRIBUTION_ROOT', exe.parent.parent)]:
            self.assertEqual(self.r.tool_argument({'path_kind': kind}, exe), expected)
        with self.assertRaises(ValueError): self.r.tool_argument({'path_kind': 'UNCHECKED'}, exe)

    def test_archive_projection_rejects_escape_symlink_collision_and_custom_objects(self):
        def archive(label, rows):
            path = self.base / (label + '.zip')
            with zipfile.ZipFile(path, 'w') as stream:
                for name, data in rows: stream.writestr(name, data)
            return path
        path = archive('valid', [('runtime/src/Proof.lean', b'theorem ok : True := True.intro\n')])
        actual = self.r.extract_source_zip(path, self.base / 'valid-source')
        self.assertEqual(actual, {'runtime/src/Proof.lean': sha(b'theorem ok : True := True.intro\n')})
        with self.assertRaises(ValueError): self.r.extract_source_zip(path, self.base / 'valid-source')
        link = zipfile.ZipInfo('link.lean'); link.create_system = 3; link.external_attr = 0o120777 << 16
        for label, rows in [('escape', [('../Proof.lean', b'')]), ('absolute', [('/Proof.lean', b'')]),
                            ('collision', [('A.lean', b'a'), ('a.lean', b'b')]),
                            ('link', [(link, b'elsewhere')]), ('object', [('Proof.olean', b'old object')])]:
            with self.subTest(label=label), self.assertRaises(ValueError):
                self.r.extract_source_zip(archive(label, rows), self.base / ('out-' + label))

    def test_original_driver_trace_only_admits_reviewed_vectors_and_budget(self):
        trace = self.base / 'original-trace'; trace.mkdir()
        argv = [sys.executable, '-c', 'print("measured child")']
        invoke = self.r.trace_reviewed_commands(subprocess.run, trace, [argv], [], 180)
        kwargs = {'stdout': subprocess.PIPE, 'stderr': subprocess.STDOUT, 'text': True, 'timeout': 180}
        with self.assertRaises(ValueError): invoke(argv + ['--unreviewed'], **kwargs)
        with self.assertRaises(ValueError): invoke(argv, **{**kwargs, 'timeout': None})
        result = invoke(argv, **kwargs); self.assertEqual(result.returncode, 0)
        row = self.r.read_json(trace / '0000.json')
        self.assertEqual((row['argv'], row['terminal'], row['exit_code']), (argv, 'COMPLETED', 0))
        with self.assertRaises(ValueError): invoke(argv, **kwargs)

    def test_original_read_only_check_output_preserves_its_python_call_contract(self):
        trace = self.base / 'read-only-trace'; trace.mkdir()
        argv = [sys.executable, '--version']; original = subprocess.run
        invoke = self.r.trace_reviewed_commands(original, trace, [], [argv], 180)
        with mock.patch.object(subprocess, 'run', invoke):
            self.assertIn('Python', subprocess.check_output(argv, text=True))
        self.assertEqual(list(trace.iterdir()), [])
        with self.assertRaises(ValueError): invoke(argv, stdout=subprocess.PIPE, check=True, timeout=1)

    def test_source_owned_cwd_and_absent_child_timeout_are_preserved(self):
        trace = self.base / 'cwd-trace'; trace.mkdir()
        argv = [sys.executable, '-c', 'print("original cwd child")']
        invoke = self.r.trace_reviewed_commands(subprocess.run, trace, [argv], [], None,
                                               working_directories=[self.base], record_outputs=True)
        kwargs = {'cwd': self.base, 'stdout': subprocess.PIPE, 'stderr': subprocess.STDOUT, 'text': True}
        with self.assertRaises(ValueError): invoke(argv, **{**kwargs, 'cwd': trace})
        with self.assertRaises(ValueError): invoke(argv, **{**kwargs, 'timeout': 30})
        self.assertEqual(invoke(argv, **kwargs).returncode, 0)
        row = self.r.read_json(trace / '0000.json')
        self.assertEqual((row['cwd'], row['output_hashes']), (str(self.base), {}))

    def test_custody_driver_requires_exact_archive_member_and_original_digest(self):
        source = {'projection': 'CUSTODY_ONLY', 'public_sha256': None,
            'original_sha256': 'a' * 64, 'original_bytes': 99, 'origin_archive_sha256': 'b' * 64,
            'member_chain': ['component.zip', 'root/replay.py']}
        contract = {'driver_sha256': 'a' * 64, 'driver_bytes': 99, 'archive_sha256': 'b' * 64,
                    'root': 'root', 'driver_path': 'replay.py'}
        self.r.check_custody_driver(source, contract)
        for change in [{'original_sha256': 'c' * 64}, {'origin_archive_sha256': 'd' * 64},
                       {'member_chain': ['component.zip', 'other/replay.py']}, {'original_bytes': 100},
                       {'projection': 'DERIVED'}, {'public_sha256': 'e' * 64}]:
            with self.assertRaises(ValueError): self.r.check_custody_driver({**source, **change}, contract)

    def test_original_child_output_hash_is_captured_at_completion(self):
        trace = self.base / 'object-trace'; trace.mkdir(); output = self.base / 'Fresh.olean'
        argv = [sys.executable, '-c', 'from pathlib import Path; import sys; Path(sys.argv[-1]).write_bytes(b"fresh object")', '-o', str(output)]
        call = self.r.trace_reviewed_commands(subprocess.run, trace, [argv], [], None,
                                             working_directories=[self.base], record_outputs=True)
        call(argv, cwd=self.base, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        row = self.r.read_json(trace / '0000.json')
        self.assertEqual(row['output_hashes'], {str(output): sha('fresh object')})
        output.write_bytes(b'later replacement')
        self.assertNotEqual(row['output_hashes'][str(output)], sha(output.read_bytes()))
        another = self.r.trace_reviewed_commands(subprocess.run, trace, [argv], [], None,
                                                 working_directories=[self.base], record_outputs=True)
        with self.assertRaises(ValueError):
            another(argv, cwd=self.base, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def test_t15_original_assertion_driver_requires_exact_normal_arguments(self):
        r = self.r; body = b'assert True\n'; path = 'verification/verify_sources.py'; recipe = 't15-identity-verify_sources-v1'
        driver = {'id': 'source', 'source_id': 'source', 'recipe': recipe, 'sha256': sha(body), 'argument_meanings': {}, 'external_input_id': None}
        row = {'source_id': 'source', 'path': path, 'role': 'DRIVER'}
        plan = {'files': {'source': row}, 'file_paths': {path: row}, 'contents': {'source': body}}
        stage = {'id': 'source-check', 'kind': 'SOURCE_CHECK', 'driver_id': 'source', 'cwd': '.', 'argv': ['{tool:python}', '{project}/' + path],
                 'output_paths': [], 'expected_exit_codes': [0], 'control_ids': []}
        with mock.patch.dict(r.T15_SOURCE_RECIPES, {recipe: (path, sha(body), 'SOURCE_CHECK')}):
            r.validate_t15_argv(stage, driver, plan)
            for option in ['-O', '-OO', '--help']:
                bad = copy.deepcopy(stage); bad['argv'].insert(1, option)
                with self.assertRaises(ValueError): r.validate_t15_argv(bad, driver, plan)
            with self.assertRaises(ValueError): r.validate_t15_driver({**driver, 'sha256': '0' * 64}, plan)

    def test_t15_ambient_child_python_is_bound_without_import_execution(self):
        r = self.r; binary = self.base / 'python3'; binary.write_bytes(b'synthetic interpreter identity')
        with mock.patch.object(r, 'T15_PYTHON_SHA', sha(binary.read_bytes())), mock.patch.object(r.shutil, 'which', return_value=str(binary)):
            self.assertIn('T15_AMBIENT_PYTHON3_BINDING_PASS', r.verify_t15_python3({'python': binary}, {'PATH': str(self.base)}))
            with self.assertRaises(ValueError): r.verify_t15_python3({'python': binary}, {'PATH': str(self.base), 'PYTHONOPTIMIZE': '1'})
            wrong = self.base / 'other-python'; wrong.write_bytes(binary.read_bytes())
            with self.assertRaises(ValueError): r.verify_t15_python3({'python': wrong}, {'PATH': str(self.base)})

    def test_t15_safe_closure_readback_keeps_names_axioms_and_auxiliary_roles(self):
        r = self.r; path = 'verification/RestrictedKernelAudit.lean'
        source = b'let ns := `Fixture\n#audit_safe_closure Fixture.proof\n'
        plan = {'file_paths': {path: {'source_id': 'audit'}}, 'contents': {'audit': source}}
        stage = {'id': 'restricted', 'kind': 'LEAN_AUDIT', 'argv': ['{tool:lean}', '-j1', '{project}/' + path]}
        text = ('RESTRICTED_NONPROOF_RUNTIME_AUXILIARY Fixture.compiler; unsafe=true; partial=false\n'
                'RESTRICTED_KERNEL_AUDIT_PASS safeRoots=2; theorems=1; nonproofRuntimeAuxiliaries=1; reachableCheckedDeclarations=3; axioms=[propext,\n Quot.sound]; unsafeOrPartialDependencies=0\n'
                'SAFE_CLOSURE_PASS Fixture.proof; declarations=3; axioms=[propext]\n')
        r.check_t15_stage(stage, text, plan)
        for changed in [text.replace('Fixture.compiler', 'Foreign.compiler'), text.replace('axioms=[propext]', 'axioms=[sorryAx]'),
                        text.replace('unsafeOrPartialDependencies=0', 'unsafeOrPartialDependencies=1'),
                        text.replace('SAFE_CLOSURE_PASS Fixture.proof', 'SAFE_CLOSURE_PASS Fixture.other'), text + text.splitlines()[-1] + '\n']:
            with self.assertRaises(ValueError): r.check_t15_stage(stage, changed, plan)

    def test_t15_original_fifteen_source_mutations_remain_aggregate_only(self):
        r = self.r; path = 'verification/test_source_checks.py'; labels = ['fixture_' + str(n) for n in range(15)]
        source = ''.join("run_mutation('" + name + "', lambda root: None)\n" for name in labels).encode()
        plan = {'file_paths': {path: {'source_id': 'driver'}}, 'contents': {'driver': source}}
        stage = {'id': 'mutations', 'kind': 'DRIVER', 'argv': ['{tool:python}', '{project}/' + path], 'control_ids': []}
        text = ''.join('EXPECTED_SOURCE_REJECTION: ' + name + '\n' for name in labels) + 'SOURCE_CONTROL_MUTATIONS_PASS: fifteen deliberate invalid successors rejected\n'
        r.check_t15_stage(stage, text, plan)
        self.assertEqual(stage['control_ids'], [])
        self.assertNotIn('child_observations', plan)
        for changed in [text.split('\n', 1)[1], text + 'EXPECTED_SOURCE_REJECTION: fixture_0\n', text.replace('fixture_0', 'foreign', 1)]:
            with self.assertRaises(ValueError): r.check_t15_stage(stage, changed, plan)

    def test_t15_exporter_is_single_final_and_cannot_overlap_sources(self):
        r = self.r; source = b'-- synthetic exact exporter\n'; path = r.T15_EXPORT_SOURCE
        plan = {'file_paths': {path: {'source_id': 'exporter'}}, 'contents': {'exporter': source}}
        stage = {'id': 'original-audit-verification-ExportDeclarationInventory', 'kind': 'LEAN_AUDIT', 'driver_id': None, 'cwd': '.',
                 'argv': ['{tool:lean}', '-j1', '{project}/' + path], 'output_paths': [r.T15_EXPORT_OUTPUT], 'expected_exit_codes': [0]}
        suite = {'replay': {'drivers': [{'recipe': name} for name in r.T15_SOURCE_RECIPES], 'module_order': [], 'stages': [stage]}}
        with mock.patch.object(r, 'T15_EXPORT_SHA', sha(source)), mock.patch.object(r, 'source_checker_inputs_t15'):
            self.assertTrue(r.t15_export_stage(stage, plan)); r.validate_t15_package(suite, plan)
            bad = copy.deepcopy(suite); bad['replay']['stages'].append({'argv': ['other']})
            with self.assertRaises(ValueError): r.validate_t15_package(bad, plan)
            bad = copy.deepcopy(suite); bad['replay']['module_order'] = ['verification.ExportDeclarationInventory']
            with self.assertRaises(ValueError): r.validate_t15_package(bad, plan)
            plan['file_paths']['.verification-results'] = {'source_id': 'collision'}
            self.assertFalse(r.t15_export_stage(stage, plan))

    def test_t15_export_inventory_preserves_boolean_metadata_and_exact_census(self):
        r = self.r; source = b'-- synthetic exact exporter\n'; path = r.T15_EXPORT_SOURCE
        plan = {'file_paths': {path: {'source_id': 'exporter'}, 'MODULES.json': {'source_id': 'modules'}},
                'contents': {'exporter': source, 'modules': json.dumps(['Module' + str(n) for n in range(88)]).encode()}}
        stage = {'id': 'original-audit-verification-ExportDeclarationInventory', 'kind': 'LEAN_AUDIT', 'driver_id': None, 'cwd': '.',
                 'argv': ['{tool:lean}', '-j1', '{project}/' + path], 'output_paths': [r.T15_EXPORT_OUTPUT], 'expected_exit_codes': [0]}
        rows = [{'module': 'Module0', 'name': 'Fixture.proof', 'theorem': True, 'unsafe': False, 'partial': False},
                {'module': 'Module0', 'name': 'Fixture.compiler', 'theorem': False, 'unsafe': True, 'partial': False}]
        output = self.base / 'export'; destination = output / r.T15_EXPORT_OUTPUT; destination.parent.mkdir(parents=True)
        text = 'DECLARATION_INVENTORY_PASS modules=88; declarations=2\n'
        with mock.patch.object(r, 'T15_EXPORT_SHA', sha(source)):
            r.write_json(destination, rows); r.check_t15_stage(stage, text, plan, output)
            with self.assertRaises(ValueError): r.check_t15_stage(stage, text.replace('declarations=2', 'declarations=3'), plan, output)
            rows[1]['theorem'] = 0; r.write_json(destination, rows)
            with self.assertRaises(ValueError): r.check_t15_stage(stage, text, plan, output)

    def _t15_finite_reference_fixture(self, recipe_name):
        r = self.r; recipe = r.T15_REFERENCE_RECIPES[recipe_name]
        values = {recipe['source']: b'# Synthetic interface fixture; never executed.\n'}
        if 'stdin' in recipe: values[recipe['stdin']] = b'{"fixture":true}\n'
        if recipe['cwd'] == 'univariate-reference':
            values['python-reference/certificate_checker.py'] = b'# Synthetic dependency.\n'
        patches = mock.patch.dict(r.T15_REFERENCE_FILES, {name: sha(raw) for name, raw in values.items()})
        patches.start(); self.addCleanup(patches.stop)
        files = {name: {'source_id': name, 'path': name} for name in values}
        driver = {'id': 'reference', 'recipe': recipe_name, 'source_id': recipe['source'],
                  'sha256': sha(values[recipe['source']]), 'argument_meanings': recipe['meanings'], 'external_input_id': None}
        stage = {'id': recipe['stage'], 'driver_id': 'reference', 'kind': recipe['kind'], 'cwd': recipe['cwd'],
                 'argv': ['{tool:python}', *recipe['args']], 'timeout_seconds': 300, 'depends_on': [],
                 'output_paths': [], 'control_ids': [], 'expected_exit_codes': [0], 'expected_diagnostics': []}
        return stage, {'files': files, 'file_paths': files, 'contents': values, 'drivers': {'reference': driver}}

    def test_t15_finite_reference_admits_only_original_normal_argument_forms(self):
        for recipe in self.r.T15_REFERENCE_RECIPES:
            stage, plan = self._t15_finite_reference_fixture(recipe)
            self.r._validate_argv(stage, plan)
            for changed in [dict(stage, argv=[stage['argv'][0], '-O', *stage['argv'][1:]]),
                            dict(stage, argv=stage['argv'] + ['--arbitrary']), dict(stage, cwd='elsewhere')]:
                with self.assertRaises(ValueError): self.r._validate_argv(changed, plan)

    def test_t15_finite_stdin_and_pythonpath_are_source_owned_only(self):
        for recipe in ['t15-json-reference-decide-example-v1', 't15-json-reference-verify-example-v1',
                       't15-univariate-reference-tests-v1']:
            stage, plan = self._t15_finite_reference_fixture(recipe)
            project = self.base / recipe; project.mkdir()
            for name, raw in plan['contents'].items():
                path = project / name; path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(raw)
            env = self.r.t15_reference_environment(stage, plan, project, {'PATH': '/fixture'})
            stream = self.r.t15_reference_stdin(stage, plan, project)
            if recipe == 't15-univariate-reference-tests-v1':
                self.assertIsNone(stream)
                self.assertEqual(env['PYTHONPATH'], str(project / 'python-reference'))
            else:
                self.assertNotIn('PYTHONPATH', env)
                self.assertEqual(stream.read_bytes(), b'{"fixture":true}\n')
                stream.write_bytes(b'changed input')
                with self.assertRaises(ValueError): self.r.t15_reference_stdin(stage, plan, project)
            for key in ['PYTHONPATH', 'PYTHONHOME', 'PYTHONOPTIMIZE']:
                with self.assertRaises(ValueError): self.r.t15_reference_environment(stage, plan, project, {key: 'unreviewed'})

    def test_t15_finite_cli_output_requires_strict_boolean_identity(self):
        for recipe, good, bad in [
                ('t15-json-reference-decide-example-v1', '{"equal":true,"counterexample":null}', '{"equal":1,"counterexample":null}'),
                ('t15-json-reference-verify-example-v1', '{"accepted":true}', '{"accepted":1}')]:
            stage, plan = self._t15_finite_reference_fixture(recipe)
            self.r.check_t15_reference_stage(stage, good, plan)
            for invalid in [bad, good[:-1] + ',"foreign":true}', good + good]:
                with self.assertRaises(ValueError): self.r.check_t15_reference_stage(stage, invalid, plan)

    def test_t15_finite_runtime_admits_only_three_exact_generated_phases(self):
        r = self.r; path = 'restricted-runtime/check_runtime_agreement.py'; raw = b'# Synthetic generator fixture.\n'
        driver = {'id': 'runtime', 'recipe': r.T15_RUNTIME_RECIPE, 'source_id': path, 'sha256': sha(raw),
                  'external_input_id': None, 'argument_meanings': {'checker': 'SOURCE_FILE', 'output': 'OUTPUT_DIRECTORY', '--verify-lean': 'LITERAL'}}
        files = {path: {'source_id': path, 'path': path}}
        plan = {'files': files, 'file_paths': files, 'contents': {path: raw}, 'drivers': {'runtime': driver}}
        cases = [
            ('runtime-prepare', r.T15_RUNTIME_ARGS, r.T15_RUNTIME_PREPARED, 'compile-IdentityChecker', 600),
            ('runtime-lean', ['{tool:lean}', '-j1', '{out}/runtime/RuntimeAgreement.lean'], ['runtime/lean-output.txt'], 'runtime-prepare', 1800),
            ('runtime-verify', r.T15_RUNTIME_ARGS + ['--verify-lean'], ['runtime/VERIFIED_RESULT.json'], 'runtime-lean', 600)]
        with mock.patch.dict(r.T15_RUNTIME_FILES, {path: sha(raw)}):
            for name, argv, outputs, parent, budget in cases:
                stage = {'id': name, 'kind': 'DRIVER', 'driver_id': 'runtime', 'cwd': '.', 'argv': argv,
                         'output_paths': outputs, 'depends_on': [parent], 'timeout_seconds': budget,
                         'expected_exit_codes': [0], 'expected_diagnostics': [], 'control_ids': []}
                r._validate_argv(stage, plan)
                for invalid in [dict(stage, argv=argv + ['--extra']), dict(stage, output_paths=['runtime/other']),
                                dict(stage, depends_on=[]), dict(stage, timeout_seconds=budget + 1)]:
                    with self.assertRaises(ValueError): r._validate_argv(invalid, plan)

    def test_t15_finite_runtime_capture_is_exact_fresh_and_preserves_partial_bytes(self):
        output = self.base / 'runtime-out'; (output / 'runtime').mkdir(parents=True)
        log = self.base / 'partial.log'; log.write_bytes(b'partial stdout\npartial stderr\xff')
        stage = {'id': 'runtime-lean', 'output_paths': ['runtime/lean-output.txt']}
        self.r.capture_t15_runtime_stdout(stage, log, output)
        self.assertEqual((output / 'runtime/lean-output.txt').read_bytes(), log.read_bytes())
        with self.assertRaises(ValueError): self.r.capture_t15_runtime_stdout(stage, log, output)
        with self.assertRaises(ValueError): self.r.capture_t15_runtime_stdout(dict(stage, output_paths=['other']), log, output)

    def test_t15_finite_runtime_rows_require_every_ordered_boolean_observation(self):
        cases = [{'equal': True}, {'equal': False}]
        good = '[true,true,true]\n[false,false,true]\n'
        self.r.read_t15_runtime_rows(good, cases)
        for invalid in [good.splitlines()[0], good + good, good.replace('true', '1', 1),
                        '[false,false,true]\n[true,true,true]\n']:
            with self.assertRaises(ValueError): self.r.read_t15_runtime_rows(invalid, cases)

    def test_t15_finite_runtime_changed_preparation_stops_before_generated_execution(self):
        output = self.base / 'changed-runtime'; (output / 'runtime').mkdir(parents=True)
        for name in self.r.T15_RUNTIME_PREPARED: (output / name).write_bytes(b'changed')
        evidence = {'output_hashes': {name: sha(b'original') for name in self.r.T15_RUNTIME_PREPARED}}
        with self.assertRaisesRegex(ValueError, 'Prior fresh runtime output'):
            self.r.check_t15_runtime_inputs({'id': 'runtime-lean'}, {}, output, evidence)

    def test_history_capture_preserves_separate_streams_and_source_bytes(self):
        r = self.r; trace = self.base / 'history-capture'; trace.mkdir()
        script = self.base / 'child.py'
        script.write_text('import sys\nprint("stdout")\nprint("stderr", file=sys.stderr)\n')
        argv = [sys.executable, str(script)]; original = script.read_bytes()
        invoke = r.trace_reviewed_commands(subprocess.run, trace, [argv], [[sys.executable, '--version']], None,
            capture_output=True, record_outputs=True, source_hashes={str(script): sha(original)})
        self.assertIn('Python', invoke([sys.executable, '--version'], capture_output=True, text=True, check=True).stdout)
        with self.assertRaises(ValueError): invoke(argv, capture_output=True, text=True, timeout=30)
        script.write_bytes(original + b'# changed\n')
        with self.assertRaises(ValueError): invoke(argv, capture_output=True, text=True)
        self.assertEqual(list(trace.iterdir()), [])
        script.write_bytes(original)
        result = invoke(argv, capture_output=True, text=True)
        row = r.read_json(trace / '0000.json')
        self.assertEqual((result.stdout, result.stderr), ('stdout\n', 'stderr\n'))
        self.assertEqual((trace / '0000.log').read_bytes(), b'stdout\nstderr\n')
        self.assertEqual((trace / '0000.stdout.log').read_bytes(), b'stdout\n')
        self.assertEqual((trace / '0000.stderr.log').read_bytes(), b'stderr\n')
        self.assertEqual(row['source_sha256'], sha(original))
        self.assertEqual(row['stdout_sha256'], sha(result.stdout))
        self.assertEqual(row['stderr_sha256'], sha(result.stderr))
        with self.assertRaises(ValueError): invoke(argv, capture_output=True, text=True)

    def test_history_generated_claim_bytes_are_source_owned(self):
        r = self.r
        body = r.history_claim_source('revocation_omission_is_safe')
        self.assertEqual(body, ('import NegativeControls\nopen InterlockHistory InterlockHistory.Controls\n'
            'example : ¬ BrokenLands revoked NoRevocation command 11 := by decide\n').encode())
        with self.assertRaises(ValueError): r.history_claim_source('unreviewed')
        source = {'projection': 'CUSTODY_ONLY', 'public_sha256': None,
            'original_sha256': r.HISTORY_CONTRACT['driver_sha256'], 'original_bytes': r.HISTORY_CONTRACT['driver_bytes'],
            'origin_archive_sha256': r.HISTORY_CONTRACT['archive_sha256'], 'member_chain': ['history.zip', 'replay.py']}
        r.check_custody_driver(source, r.HISTORY_CONTRACT)
        with self.assertRaises(ValueError): r.check_custody_driver({**source, 'member_chain': ['history.zip', '/replay.py']}, r.HISTORY_CONTRACT)

    def test_history_timeout_keeps_both_partial_streams_without_rejection_code(self):
        r = self.r; trace = self.base / 'history-timeout'; trace.mkdir()
        call = r.traced_run(subprocess.run, trace, capture_output=True)
        argv = [sys.executable, '-c', 'import sys,time; print("partial out",flush=True); print("partial err",file=sys.stderr,flush=True); time.sleep(2)']
        with self.assertRaises(subprocess.TimeoutExpired): call(argv, capture_output=True, text=True, timeout=0.3)
        row = r.read_json(trace / '0000.json')
        self.assertEqual((row['terminal'], row['exit_code']), ('TIMEOUT', None))
        stdout = (trace / '0000.stdout.log').read_bytes(); stderr = (trace / '0000.stderr.log').read_bytes()
        self.assertIn(b'partial out', stdout); self.assertIn(b'partial err', stderr)
        self.assertEqual((trace / '0000.log').read_bytes(), stdout + stderr)
        self.assertEqual(row['log_sha256'], sha(stdout + stderr))
        self.assertTrue(r.trace_resource_inconclusive(trace))

    def test_history_scenarios_require_actual_exact_cases_and_source(self):
        r = self.r; source = self.base / 'dynamic_interlock.py'
        value = {'status': 'PASS', 'scope': 'bounded source correspondence corroboration only',
                 'source': str(source), 'cases': copy.deepcopy(r.HISTORY_CASES)}
        r.check_history_scenarios(value, str(source))
        for changed in [dict(value, source='different.py'), dict(value, cases=value['cases'][:-1]), dict(value, status='FAIL')]:
            with self.assertRaises(ValueError): r.check_history_scenarios(changed, str(source))
        changed = copy.deepcopy(value); changed['cases'][2]['reprepare'] = 0
        with self.assertRaises(ValueError): r.check_history_scenarios(changed, str(source))

    @unittest.skipUnless(os.environ.get('V5_REPLAY_TEST_LEAN'), 'Explicit official Lean test binding required')
    def test_history_archive_cwd_compiles_nested_source_and_checks_external_control(self):
        r = self.r
        with tempfile.TemporaryDirectory() as directory:
            out = Path(directory)
            project = out / 'project'; project.mkdir()
            archive = out / 'archives/source'; archive.mkdir(parents=True)
            source = archive / 'nested/CwdFixture.lean'; source.parent.mkdir()
            source.write_text('theorem cwd_ok : True := True.intro\n')
            build = out / 'original/build'; build.mkdir(parents=True)
            control = out / 'original/Control.lean'
            control.write_text('import CwdFixture\nexample : True := cwd_ok\nexample : (1 : Nat) = 2 := by decide\n')
            driver = {'recipe': r.HISTORY_RECIPE, 'external_input_id': 'source'}
            mappings = {'archive:source': archive, 'project': project}
            symbol = r.history_launch_cwd(driver)
            cwd = Path(r._expand(symbol, mappings))
            lean = Path(os.environ['V5_REPLAY_TEST_LEAN'])
            self.assertEqual(r.sha(lean.read_bytes()), r.LEAN_SHA)
            env = r._clean_environment(); env['LEAN_PATH'] = str(build)
            result = r.run_process([lean, '-j1', '-o', build / 'CwdFixture.olean', source], cwd, env, out / 'compile.log', 30)
            self.assertEqual((result['terminal'], result['exit_code']), ('COMPLETED', 0), (out / 'compile.log').read_text())
            self.assertTrue((build / 'CwdFixture.olean').is_file())
            result = r.run_process([lean, '-j1', control], cwd, env, out / 'control.log', 30)
            self.assertEqual((result['terminal'], result['exit_code']), ('COMPLETED', 1))
            for literal in r.HISTORY_DIAGNOSTICS:
                self.assertIn(literal, (out / 'control.log').read_text())
            self.assertNotIn('unknown', (out / 'control.log').read_text().lower())


    def test_history_launch_cwd_and_failed_legacy_binding_are_strict(self):
        r = self.r
        driver = {'id': 'driver', 'recipe': r.HISTORY_RECIPE, 'external_input_id': 'source', 'sha256': r.HISTORY_CONTRACT['driver_sha256']}
        stage = {'id': 'original', 'driver_id': 'driver', 'cwd': '.', 'argv': ['{tool:python}', '-B', '{driver:driver}', '--lean', '{tool:lean}', '--mathlib', '{dependency:mathlib}', '--output', '{out}/original']}
        plan = {'drivers': {'driver': driver}, 'stages': {'original': stage, 'observe': {'id': 'observe', 'driver_id': 'driver', 'argv': ['{builtin:observe-child}', 'original', 'HistoryModel']}}}
        parent = {'id': 'original', 'terminal': 'COMPLETED', 'exit_code': 1, 'log_sha256': r.sha(b'failed')}
        launch = {'parent_stage_id': 'original', 'driver_sha256': driver['sha256'], 'source_argv': stage['argv'], 'launch_argv': r.history_tracer_argv(stage), 'runner_sha256': r.HISTORY_LEGACY_FAILED_RUNNER, 'trace_sha256': r.sha(b'trace'), 'parent_log_sha256': parent['log_sha256'], 'child_count': 1}
        evidence = {'driver_invocations': [launch], 'child_observations': [], 'runner_sha256': r.HISTORY_LEGACY_FAILED_RUNNER, 'output_hashes': {}}
        r.validate_child_evidence(evidence, plan, {'original': parent}, False)
        changed = copy.deepcopy(evidence)
        changed['runner_sha256'] = changed['driver_invocations'][0]['runner_sha256'] = 'a' * 64
        with self.assertRaises(ValueError):
            r.validate_child_evidence(changed, plan, {'original': parent}, False)
        changed['driver_invocations'][0]['launch_cwd'] = '{archive:source}'
        r.validate_child_evidence(changed, plan, {'original': parent}, False)
        for value in ['{project}', '{archive:foreign}', '.', None]:
            bad = copy.deepcopy(changed); bad['driver_invocations'][0]['launch_cwd'] = value
            with self.subTest(cwd=value), self.assertRaises(ValueError):
                r.validate_child_evidence(bad, plan, {'original': parent}, False)


    def test_history_collector_binds_original_order_streams_claims_and_objects(self):
        r = self.r; out = self.base / 'history'; trace = out / 'traces/original'; trace.mkdir(parents=True)
        driver = {'id': 'driver', 'recipe': r.HISTORY_RECIPE, 'external_input_id': 'archive', 'sha256': r.HISTORY_CONTRACT['driver_sha256']}
        stage = {'id': 'original', 'driver_id': 'driver', 'argv': ['{tool:python}', '-B', '{driver:driver}',
                 '--lean', '{tool:lean}', '--mathlib', '{dependency:mathlib}', '--output', '{out}/original']}
        parent = {'id': 'original', 'terminal': 'COMPLETED', 'exit_code': 0, 'started_at': '2026-10-05T00:00:00Z',
                  'ended_at': '2026-10-05T00:00:03Z', 'log_sha256': sha('parent')}
        plan = {'drivers': {'driver': driver}, 'modules': {n: {'source_id': n} for n, _, _ in r.HISTORY_PATHS},
                'file_paths': {'control-source/check_controls.py': {'source_id': 'claims'},
                               'control-source/source_replay.py': {'source_id': 'scenarios'}},
                'targets': {}, 'contents': {'claims': b'# exact fixture claims', 'scenarios': b'# exact fixture scenario'}, 'stages': {'original': stage}}
        plan['history_children'] = r.history_specs('archive', plan)
        archive = self.base / 'archive'
        mappings = {'out': out, 'project': out / 'project', 'tool:lean': self.base / 'lean',
                    'tool:python': self.base / 'python', 'archive:archive': archive}
        specs = list(plan['history_children'].values()); rows = []; negatives = []; stages = {'original': parent}
        scenarios = {'status': 'PASS', 'source': str(archive / r.HISTORY_DYNAMIC),
            'scope': 'bounded source correspondence corroboration only', 'cases': r.HISTORY_CASES}
        for index, spec in enumerate(specs):
            name = spec['id']; negative = bool(spec['exit_code']); scenario = name == 'source-replay'
            source = r.history_claim_source(name) if negative else plan['contents']['scenarios'] if scenario else ('-- ' + name).encode()
            if not negative and not scenario: plan['contents'][name] = source
            path = Path(r._expand(spec['argv'][-1], mappings)); path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(source)
            stdout = json.dumps(scenarios) + '\n' if scenario else 'checked\n' if not negative else 'fixture: error: ' + r.HISTORY_DIAGNOSTICS[0] + '\n'
            stderr = r.HISTORY_DIAGNOSTICS[1] + '\n' if negative else ''
            text = stdout + stderr; log = out / spec['log']; log.parent.mkdir(parents=True, exist_ok=True); log.write_bytes(text.encode())
            if scenario:
                (out / 'original/logs/source-replay.json').write_bytes(stdout.encode())
                (out / 'original/logs/source-replay.stderr').write_bytes(stderr.encode())
            for suffix, data in [('log', text), ('stdout.log', stdout), ('stderr.log', stderr)]:
                (trace / f'{index:04}.{suffix}').write_bytes(data.encode())
            outputs = {}
            if spec['output_path']:
                obj = out / spec['output_path']; obj.parent.mkdir(parents=True, exist_ok=True); obj.write_bytes(('fresh ' + name).encode()); outputs[str(obj)] = sha(obj.read_bytes())
            argv = [r._expand(a, mappings) for a in spec['argv']]
            r.write_json(trace / f'{index:04}.json', {'index': index, 'argv': argv, 'cwd': str(archive),
                'started_at': '2026-10-05T00:00:01Z', 'ended_at': '2026-10-05T00:00:02Z', 'terminal': 'COMPLETED',
                'exit_code': spec['exit_code'], 'log_sha256': sha(text), 'stdout_sha256': sha(stdout), 'stderr_sha256': sha(stderr),
                'source_sha256': sha(source), 'output_hashes': outputs})
            if negative: negatives.append({'control': name, 'exit_code': 1, 'expected_false_claim_rejected': True})
            elif not scenario: rows.append({'stage': name, 'exit_code': 0, 'command': argv})
            sid = 'observe-' + name; plan['stages'][sid] = {'id': sid, 'driver_id': 'driver', 'argv': ['{builtin:observe-child}', 'original', name]}
            stages[sid] = {'id': sid, 'terminal': 'COMPLETED', 'exit_code': spec['exit_code'], 'log_sha256': sha(text),
                          'started_at': '2026-10-05T00:00:04Z', 'ended_at': '2026-10-05T00:00:05Z'}
        r.write_json(out / 'original/controls/RESULTS.json', negatives)
        version = 'Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)'
        (out / 'original/logs/toolchain.log').write_text(version + '\n' + LEAN_SHA + '\n')
        result = {'status': 'PASS_PORTABLE_SOURCE_REPLAY', 'completed_utc': '2026-10-05T00:00:02+00:00',
            'public_manifest_sha256': r.HISTORY_FILES['PUBLIC_MANIFEST.json'], 'original_to_public_sha256': r.HISTORY_FILES['ORIGINAL_TO_PUBLIC.json'],
            'source_archive_sha256': r.HISTORY_ORIGIN_SHA, 'scientific_candidate_snapshot_sha256': r.HISTORY_FILES[r.HISTORY_KERNEL + 'REVIEW_SNAPSHOT_V2.json'],
            'scientific_review_receipt_sha256': r.HISTORY_FILES[r.HISTORY_KERNEL + 'independent-review-v2/RECEIPT.json'],
            'compiler_sha256': LEAN_SHA, 'compiler_version': version, 'mathlib_commit': 'c44e0c8ee63ca166450922a373c7409c5d26b00b',
            'mathlib_source_files_verified': 6816, 'compiled_cache_used_read_only': True, 'independent_cache_rebuild_claimed': False,
            'compiled_stages': rows, 'false_claim_rejections': 7, 'accepted_source_scenarios': 7, 'archive_executable_modes_required': False,
            'shell_scripts_executed': [], 'all_projected_inputs_unchanged': True, 'claim_ceiling': r.HISTORY_CEILING}
        r.write_json(out / 'original/REPLAY_RECEIPT.json', result)
        text = '\n'.join(r.HISTORY_TERMINAL + ['Receipt: ' + str(out / 'original/REPLAY_RECEIPT.json')]) + '\n'
        def collect(): return r.history_collect_children(stage, parent, text, plan, out, mappings)
        children, invocation, objects = collect()
        self.assertEqual((len(children), len(objects), invocation['child_count']), (17, 5, 17))
        evidence = {'driver_invocations': [invocation], 'child_observations': [dict(c, stage_id='observe-' + c['source_child_id'], observed_at='2026-10-05T00:00:05Z') for c in children.values()],
                    'output_hashes': objects, 'runner_sha256': invocation['runner_sha256']}
        r.validate_child_evidence(evidence, plan, stages, True)
        bad = copy.deepcopy(evidence); bad['child_observations'][7]['generated_source_sha256'] = '0' * 64
        with self.assertRaises(ValueError): r.validate_child_evidence(bad, plan, stages, True)
        for field, value in [('terminal', 'TIMEOUT'), ('exit_code', 124), ('argv', ['foreign']), ('source_sha256', '0' * 64)]:
            row = r.read_json(trace / '0007.json'); r.write_json(trace / '0007.json', dict(row, **{field: value}))
            with self.subTest(field=field), self.assertRaises(ValueError): collect()
            r.write_json(trace / '0007.json', row)
        mutated = out / 'original/controls/revocation_omission_is_safe.lean'; original = mutated.read_bytes(); mutated.write_bytes(original + b'-- later edit')
        with self.assertRaises(ValueError): collect()
        mutated.write_bytes(original)
        stream = trace / '0007.stderr.log'; original = stream.read_bytes(); stream.write_bytes(b'replaced diagnostic')
        with self.assertRaises(ValueError): collect()
        stream.write_bytes(original)
        obj = out / 'original/build/HistoryModel.olean'; obj.write_bytes(b'late object replacement')
        with self.assertRaises(ValueError): collect()

    def test_attribution_collector_binds_every_original_child_and_immediate_object(self):
        r = self.r; out = self.base / 'attribution'; trace = out / 'traces/original'; trace.mkdir(parents=True)
        driver = {'id': 'driver', 'recipe': r.ATTR_RECIPE, 'sha256': r.ATTR_CONTRACT['driver_sha256']}
        stage = {'id': 'original', 'driver_id': 'driver', 'argv': ['{tool:python}', '-B', '{driver:driver}',
                 '--lean', '{tool:lean}', '--mathlib', '{dependency:mathlib}', '--output', '{out}/original']}
        parent = {'id': 'original', 'terminal': 'COMPLETED', 'exit_code': 0, 'started_at': '2026-10-05T00:00:00Z',
                  'ended_at': '2026-10-05T00:00:03Z', 'log_sha256': sha('parent')}
        plan = {'drivers': {'driver': driver}, 'modules': {n: {'source_id': n, 'imports': ['Init']} for n, _, _ in r.ATTR_PATHS},
                'official': {'Init': {}}, 'targets': {}, 'contents': {}, 'stages': {'original': stage}}
        plan['attribution_children'] = r.attribution_specs('archive', plan)
        mappings = {'out': out, 'tool:lean': self.base / 'lean', 'archive:archive': self.base / 'archive'}
        rows = []; lines = []; stages = {'original': parent}
        for index, spec in enumerate(plan['attribution_children'].values()):
            name = spec['id']; negative = spec['exit_code'] == 1
            names = ['Fixture.check' + str(i) for i in range(50)] if name == 'AxiomAudit' else []
            source = ''.join('#print axioms ' + n + '\n' for n in names).encode() or ('-- ' + name).encode()
            plan['contents'][name] = source
            text = r.ATTR_DIAGNOSTICS[name] + '\nFalse\n' if negative else ''.join("'" + n + "' does not depend on any axioms\n" for n in names)
            log = out / spec['log']; log.parent.mkdir(parents=True, exist_ok=True); log.write_bytes(text.encode())
            (trace / f'{index:04}.log').write_bytes(text.encode())
            outputs = {}
            if spec['output_path']:
                object_path = out / spec['output_path']; object_path.parent.mkdir(parents=True, exist_ok=True)
                object_path.write_bytes(('fresh ' + name).encode()); outputs[str(object_path)] = sha(object_path.read_bytes())
            r.write_json(trace / f'{index:04}.json', {'index': index, 'argv': [r._expand(a, mappings) for a in spec['argv']],
                'cwd': r._expand(spec['cwd'], mappings), 'started_at': '2026-10-05T00:00:01Z', 'ended_at': '2026-10-05T00:00:02Z',
                'terminal': 'COMPLETED', 'exit_code': spec['exit_code'], 'log_sha256': sha(text), 'output_hashes': outputs})
            rows.append({'name': name, 'source': spec['source_path'], 'source_sha256': sha(source), 'exit_code': spec['exit_code'],
                         'status': 'EXPECTED_REJECTION' if negative else 'PASS', 'log': spec['log'].removeprefix('original/')})
            lines.append(('EXPECTED_REJECTION: ' if negative else 'PASS: ') + name)
            sid = 'observe-' + name
            plan['stages'][sid] = {'id': sid, 'driver_id': 'driver', 'argv': ['{builtin:observe-child}', 'original', name]}
            stages[sid] = {'id': sid, 'terminal': 'COMPLETED', 'exit_code': spec['exit_code'], 'log_sha256': sha(text),
                           'started_at': '2026-10-05T00:00:04Z', 'ended_at': '2026-10-05T00:00:05Z'}
        lines.append('PASS: exact central targets, Regression, supplement, independent proofs, axiom audit, and three expected mutant diagnostics')
        result = {'status': 'PASS', 'lean_sha256': LEAN_SHA, 'mathlib_revision': 'c44e0c8ee63ca166450922a373c7409c5d26b00b',
            'public_manifest_sha256': r.ATTR_MANIFESTS['PUBLIC_MANIFEST.json'], 'central_manifest_sha256': r.ATTR_MANIFESTS['sources/central-v1/MANIFEST.json'],
            'controls_manifest_sha256': r.ATTR_MANIFESTS['sources/controls-v1/MANIFEST.json'], 'independent_acceptance_sha256': r.ATTR_MANIFESTS['review/REVIEW_RECEIPT.json'],
            'public_entries': 125, 'external_source_files_verified': 7506, 'fresh_build': True, 'custom_oleans_reused': False,
            'external_compiled_cache_trusted': True, 'successful_stages': 18, 'expected_rejected_mutants': 3, 'central_theorems_axiom_audited': 50, 'steps': rows}
        r.write_json(out / 'original/REPLAY_RECEIPT.json', result)
        def collect(): return r.attribution_collect_children(stage, parent, '\n'.join(lines) + '\n', plan, out, mappings)
        children, invocation, objects = collect()
        self.assertEqual((len(children), invocation['child_count'], len(objects)), (21, 21, 10))
        evidence = {'runner_sha256': invocation['runner_sha256'], 'driver_invocations': [invocation], 'output_hashes': objects,
                    'child_observations': [{**row, 'stage_id': 'observe-' + name, 'observed_at': '2026-10-05T00:00:05Z'} for (_, name), row in children.items()]}
        r.validate_child_evidence(evidence, plan, stages, True)
        for change in [{'cwd': '{project}'}, {'exit_code': 0}, {'actual_outcome': 'ACCEPT'}, {'source_id': 'RootImage'}]:
            bad = copy.deepcopy(evidence); bad['child_observations'][-1].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError): r.validate_child_evidence(bad, plan, stages, True)
        object_path = out / 'original/build/RootImage.olean'; saved = object_path.read_bytes(); object_path.write_bytes(b'substituted')
        with self.assertRaises(ValueError): collect()
        object_path.write_bytes(saved)
        saved = (trace / '0018.json').read_bytes(); bad = r.read_json(trace / '0018.json'); bad['exit_code'] = 0
        r.write_json(trace / '0018.json', bad)
        with self.assertRaises(ValueError): collect()
        (trace / '0018.json').write_bytes(saved)
        result['steps'][-1]['status'] = 'PASS'; r.write_json(out / 'original/REPLAY_RECEIPT.json', result)
        with self.assertRaises(ValueError): collect()

    def test_attribution_negative_needs_its_exact_child_and_concrete_diagnostic(self):
        r = self.r; name = 'count_labels_as_roots'; spec = r.attribution_specs('input')[name]
        row = {'name': name, 'source': spec['source_path'], 'source_sha256': sha('source'),
               'exit_code': 1, 'status': 'EXPECTED_REJECTION', 'log': spec['log'].removeprefix('original/')}
        text = 'fixture.lean:1:0: error: unsolved goals\nFalse'
        captured = {'terminal': 'COMPLETED', 'exit_code': 1, 'log_sha256': sha(text)}
        r.check_attribution_child(spec, row, captured, text, sha('source'))
        for change in [{'exit_code': 0}, {'exit_code': 124}, {'source_sha256': sha('other')}, {'name': 'foreign'}]:
            with self.assertRaises(ValueError): r.check_attribution_child(spec, {**row, **change}, captured, text, sha('source'))
        with self.assertRaises(ValueError): r.check_attribution_child(spec, row, {**captured, 'terminal': 'TIMEOUT'}, text, sha('source'))
        for suffix in ['\nunknown module Mathlib', '\nmaximum recursion depth exceeded']:
            wrong = text + suffix
            with self.assertRaises(ValueError): r.check_attribution_child(spec, row, {**captured, 'log_sha256': sha(wrong)}, wrong, sha('source'))

    def test_attribution_external_sources_are_rechecked_against_original_manifest(self):
        r = self.r; archive = self.base / 'archive'; (archive / 'dependencies').mkdir(parents=True)
        external = self.base / 'mathlib'; external.mkdir(); source = external / 'Pinned.lean'; source.write_bytes(b'exact source')
        rows = {'files': [{'path': 'Pinned.lean', 'size': 12, 'sha256': sha(b'exact source')}]}
        manifest = archive / 'dependencies/SOURCE_MANIFEST.json'; r.write_json(manifest, rows)
        with mock.patch.dict(r.ATTR_MANIFESTS, {'dependencies/SOURCE_MANIFEST.json': sha(manifest.read_bytes())}):
            r.verify_attribution_dependencies(archive, external)
            source.write_bytes(b'changed bytes')
            with self.assertRaises(ValueError): r.verify_attribution_dependencies(archive, external)
        source.write_bytes(b'exact source'); rows['files'][0]['path'] = '../mathlib/Pinned.lean'; r.write_json(manifest, rows)
        with mock.patch.dict(r.ATTR_MANIFESTS, {'dependencies/SOURCE_MANIFEST.json': sha(manifest.read_bytes())}):
            with self.assertRaises(ValueError): r.verify_attribution_dependencies(archive, external)

    def test_original_owned_build_parent_stays_absent_until_driver_runs(self):
        output = self.base / 'deferred-build'; (output / 'logs').mkdir(parents=True)
        suite = {'toolchain': {'kind': 'PYTHON', 'version': '.'.join(map(str, sys.version_info[:3])),
                  'platform': 'test', 'executable_sha256': sha(Path(sys.executable).read_bytes()), 'packages': []},
                 'replay': {'tools': [], 'build_roots': ['original/runtime/build']}}
        plan = {'packages': {}, 'inputs': {}, 'drivers': {'core': {'recipe': self.r.CORE_RECIPE}}}
        self.r._verify_environment(suite, plan, {'python': sys.executable}, {}, output)
        self.assertFalse((output / 'original').exists())

    def test_core_observations_bind_real_terminals_sources_and_fresh_objects(self):
        r = self.r; driver = {'id': 'core', 'recipe': r.CORE_RECIPE, 'sha256': r.CORE_FILES['replay.py']}
        parent = {'id': 'original', 'driver_id': 'core', 'argv': ['{tool:python}', '-B', '{driver:core}',
                  '--lean-bin', '{tool:lean-bin}', '--mathlib', '{dependency:mathlib}', '--out', '{out}/original', '--mode', 'runtime']}
        plan = {'drivers': {'core': driver}, 'stages': {'original': parent}, 'contents': {}, 'core_children': {}}
        stages = {'original': {'id': 'original', 'terminal': 'COMPLETED', 'exit_code': 0,
                  'started_at': '2026-10-05T00:00:00Z', 'ended_at': '2026-10-05T00:00:03Z', 'log_sha256': sha('parent')}}
        launch = {'parent_stage_id': 'original', 'driver_sha256': driver['sha256'], 'source_argv': parent['argv'],
                  'launch_argv': r.core_tracer_argv(parent), 'runner_sha256': sha('runner'), 'trace_sha256': sha('trace'),
                  'parent_log_sha256': sha('parent'), 'child_count': 168}
        evidence = {'runner_sha256': sha('runner'), 'driver_invocations': [launch], 'child_observations': [], 'output_hashes': {}}
        for index in range(168):
            name = 'RuntimeReadback' if index == 167 else 'Module' + str(index)
            child = 'runtime/' + name; sid = 'observe-' + name
            spec = r.core_child_spec(child, name, 'runtime/src/' + name + '.lean', 'archive')
            plan['core_children'][child] = spec; plan['contents'][name] = b'exact source'
            plan['stages'][sid] = {'id': sid, 'driver_id': 'core', 'argv': ['{builtin:observe-child}', 'original', child]}
            stages[sid] = {'id': sid, 'terminal': 'COMPLETED', 'exit_code': 0, 'started_at': '2026-10-05T00:00:04Z',
                           'ended_at': '2026-10-05T00:00:05Z', 'log_sha256': sha(child)}
            objects = {spec['output_path']: sha(name)} if spec['output_path'] else {}
            evidence['output_hashes'].update(objects)
            evidence['child_observations'].append({'stage_id': sid, 'source_child_id': child, 'parent_stage_id': 'original',
                'driver_sha256': driver['sha256'], 'parser_id': r.CORE_RECIPE, 'mode': 'NONEXECUTING_OBSERVATION',
                'argv_provenance': 'CAPTURED', 'argv': spec['argv'], 'cwd': '{project}', 'started_at': '2026-10-05T00:00:01Z',
                'ended_at': '2026-10-05T00:00:02Z', 'observed_at': '2026-10-05T00:00:05Z', 'physical_run_sha256': sha('trace'),
                'parent_log_sha256': sha('parent'), 'terminal': 'COMPLETED', 'exit_code': 0, 'actual_outcome': 'ACCEPT',
                'log_sha256': sha(child), 'source_id': name, 'source_sha256': sha(b'exact source'),
                'output_hashes': objects, 'result_record_sha256': sha('original record')})
        r.validate_child_evidence(evidence, plan, stages, True)
        changes = [{'source_child_id': 'foreign'}, {'parent_stage_id': 'foreign'}, {'terminal': 'TIMEOUT'},
                   {'exit_code': None}, {'exit_code': True}, {'exit_code': 124}, {'actual_outcome': 'REJECT'},
                   {'argv': ['derived']}, {'source_id': 'Module1'}, {'source_sha256': sha('different')},
                   {'output_hashes': {'original/runtime/build/Module0.olean': sha('old object')}}]
        for change in changes:
            bad = copy.deepcopy(evidence); bad['child_observations'][0].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError): r.validate_child_evidence(bad, plan, stages, True)
        for change in [{'child_count': 167}, {'launch_argv': parent['argv']}, {'parent_log_sha256': sha('wrong')}]:
            bad = copy.deepcopy(evidence); bad['driver_invocations'][0].update(change)
            with self.subTest(change=change), self.assertRaises(ValueError): r.validate_child_evidence(bad, plan, stages, True)
        bad = copy.deepcopy(evidence); bad['child_observations'].pop()
        with self.assertRaises(ValueError): r.validate_child_evidence(bad, plan, stages, True)
        bad = copy.deepcopy(evidence); bad['child_observations'].append(bad['child_observations'][0])
        with self.assertRaises(ValueError): r.validate_child_evidence(bad, plan, stages, True)
        bad_stages = copy.deepcopy(stages); bad_stages['original']['exit_code'] = 1
        with self.assertRaises(ValueError): r.validate_child_evidence(evidence, plan, bad_stages, True)

    def test_original_core_summary_cannot_override_captured_child_failure(self):
        r = self.r; spec = r.core_child_spec('runtime/Proof', 'proof', 'runtime/src/Proof.lean', 'archive')
        parent = {'terminal': 'COMPLETED', 'exit_code': 0, 'started_at': '2026-10-05T00:00:00Z', 'ended_at': '2026-10-05T00:00:03Z'}
        captured = {'terminal': 'COMPLETED', 'exit_code': 0, 'argv': ['actual'], 'started_at': '2026-10-05T00:00:01Z',
                    'ended_at': '2026-10-05T00:00:02Z', 'log_sha256': sha(b'')}
        row = {'suite': 'runtime', 'module': 'Proof', 'exit_code': 0, 'command': ['actual'],
               'log_sha256': sha(b''), 'has_resource_diagnostic': False, 'elapsed_seconds': 0.1}
        r.check_core_child(spec, row, captured, parent, '', ['actual'])
        for change in [{'terminal': 'TIMEOUT'}, {'exit_code': None}, {'exit_code': 1}, {'argv': ['unrecorded']},
                       {'log_sha256': sha('changed')}, {'ended_at': '2026-10-05T00:00:04Z'}]:
            with self.assertRaises(ValueError): r.check_core_child(spec, row, {**captured, **change}, parent, '', ['actual'])

    def test_original_child_compiler_resource_diagnostic_is_inconclusive(self):
        trace = self.base / 'resource-trace'; trace.mkdir()
        for terminal, code, text, expected in [('COMPLETED', 1, 'error: (deterministic) timeout at whnf', True),
                ('COMPLETED', 1, 'error: application type mismatch', False), ('TIMEOUT', None, '', True),
                ('INTERRUPTED', None, '', True), ('COMPLETED', 0, 'timeout_definition : True', False)]:
            (trace / '0000.log').write_bytes(text.encode())
            self.r.write_json(trace / '0000.json', {'terminal': terminal, 'exit_code': code, 'log_sha256': sha(text)})
            self.assertEqual(self.r.trace_resource_inconclusive(trace), expected)

    def test_core_collector_requires_original_logs_complete_census_and_emitted_objects(self):
        r = self.r; output = self.base / 'core-collector'; trace = output / 'traces/original'; trace.mkdir(parents=True)
        stage = {'id': 'original', 'driver_id': 'core', 'argv': ['{tool:python}', '-B', '{driver:core}',
                 '--lean-bin', '{tool:lean-bin}', '--mathlib', '{dependency:mathlib}', '--out', '{out}/original', '--mode', 'runtime']}
        parent = {'terminal': 'COMPLETED', 'exit_code': 0, 'started_at': '2026-10-05T00:00:00Z',
                  'ended_at': '2026-10-05T00:00:03Z', 'log_sha256': sha('parent')}
        pin = {'name': 'mathlib', 'revision': 'a' * 40}
        plan = {'core_children': {}, 'contents': {'pins': json.dumps({'packages': [pin]}).encode()},
                'file_paths': {'DEPENDENCY_PINS.json': {'source_id': 'pins'}}, 'targets': {}, 'modules': {}, 'official': {'Init': {}}}
        mappings = {'out': output, 'archive:archive': output / 'source', 'tool:lean': self.base / 'lean'}
        rows = []; progress = []
        for i in range(168):
            name = 'RuntimeReadback' if i == 167 else 'Module' + str(i)
            spec = r.core_child_spec('runtime/' + name, name, 'runtime/src/' + name + '.lean', 'archive')
            plan['core_children'][spec['id']] = spec
            source = b'theorem fixture : True := True.intro\n'; text = ''
            if i == 167:
                source = ''.join('#print axioms Test.t' + str(n) + '\n' for n in range(13)).encode()
                text = ''.join("'Test.t" + str(n) + "' depends on axioms: [propext]\n" for n in range(13))
            plan['contents'][name] = source
            plan['modules'][name] = {'source_id': name, 'imports': r.imports(source.decode())}
            actual = [r.core_expand(arg, mappings) for arg in spec['argv']]
            log = output / spec['log']; log.parent.mkdir(parents=True, exist_ok=True); log.write_bytes(text.encode())
            (trace / f'{i:04}.log').write_bytes(log.read_bytes())
            r.write_json(trace / f'{i:04}.json', {'index': i, 'argv': actual, 'cwd': str(output / 'project'),
                'started_at': '2026-10-05T00:00:01Z', 'ended_at': '2026-10-05T00:00:02Z',
                'terminal': 'COMPLETED', 'exit_code': 0, 'log_sha256': sha(log.read_bytes())})
            row = {'suite': 'runtime', 'module': name, 'command': actual, 'source_sha256': sha(source),
                   'exit_code': 0, 'elapsed_seconds': 0.1, 'log': spec['log'].removeprefix('original/'),
                   'log_sha256': sha(log.read_bytes()), 'has_resource_diagnostic': False}
            if spec['output_path']:
                obj = output / spec['output_path']; obj.parent.mkdir(parents=True, exist_ok=True); obj.write_bytes(name.encode())
                row['object_sha256'] = sha(obj.read_bytes())
            rows.append(row); progress.append('runtime ' + name + ' 0')
        value = {'status': 'COMPLETED_FRESH_REPLAY', 'mode': 'runtime', 'source_manifest_sha256': r.CORE_FILES['SOURCE_MANIFEST.json'],
            'official_dependency_cache_trusted': True, 'custom_objects_reused': False, 'heartbeat_flags_added': False,
            'original_runtime_mutant_retried': False, 'historical_statuses_unchanged': True, 'parallel_processes': 1,
            'wall_clock_per_module_seconds': 180, 'runtime': {'status': 'FRESH_EXACT_CLOSURE_AND_AXIOM_READBACK_PASS',
                'custom_modules': 167, 'axiom_readbacks': 13, 'semantic_result': 'EXACT_MUTATED_UNIVERSAL_STATEMENT_FALSE_BY_POSITIVE_MEASURE_COUNTEREXAMPLE',
                'selector_kind': 'KERNEL_CERTIFIED_CLASSICAL_EXISTENTIAL_NOT_EVALUATED_NATIVE_NUMERALS'},
            'dependency_identity': {'dependency_writes': False, 'official_cache_objects_trusted': True,
                'mathlib': {**pin, 'mode': 'CLEAN_EXACT_GIT', 'tracked_clean': True, 'unexpected_lean_sources': False}, 'packages': []}, 'runs': rows}
        result = output / 'original/RESULT.json'; r.write_json(result, value)
        children, invocation, objects = r.core_collect_children(stage, parent, '\n'.join(progress), plan, output, mappings)
        self.assertEqual((len(children), invocation['child_count'], len(objects)), (168, 168, 167))
        for field, wrong in [('source_sha256', sha('foreign')), ('object_sha256', sha('old object')), ('exit_code', 1), ('module', 'Foreign')]:
            bad = copy.deepcopy(value); bad['runs'][0][field] = wrong; r.write_json(result, bad)
            with self.subTest(field=field), self.assertRaises(ValueError): r.core_collect_children(stage, parent, '\n'.join(progress), plan, output, mappings)
        bad = copy.deepcopy(value); bad['runs'].pop(); r.write_json(result, bad)
        with self.assertRaises(ValueError): r.core_collect_children(stage, parent, '\n'.join(progress), plan, output, mappings)
        r.write_json(result, value); (trace / '0000.log').write_bytes(b'contradictory actual log')
        with self.assertRaises(ValueError): r.core_collect_children(stage, parent, '\n'.join(progress), plan, output, mappings)

    def test_t14_dynamic_audit_census_does_not_count_compiler_auxiliaries_as_safe_roots(self):
        stage = {'kind': 'LEAN_AUDIT', 'argv': ['{tool:lean}', '-j1', '{project}/verification/IndependentKernelChecks.lean']}
        names = ['P01AC.ExtensionalRepair.item' + str(i) for i in range(157)]
        text = '\n'.join('INDEPENDENT_AXIOMS ' + name + ': [propext]' for name in names) + '\n'
        text += 'COMPILER_AUXILIARY ' + names[0] + ': unsafe=true partial=false\n'
        text += ''.join('EXACT_RETAINED_CONSTRUCTOR old' + str(i) + ' = new' + str(i) + '\n' for i in range(54))
        text += 'EXACT_NEW_SCHEMA P01AC.ExtensionalRepair.HasE.piExt\nEXACT_NEW_SCHEMA P01AC.ExtensionalRepair.HasE.allExt\n'
        text += 'CONVERSION_EXACT_EIGHT_IMPORTED_GENERATORS\nINDEPENDENT_AXIOM_PASS 157 declarations; 1 compiler auxiliaries; no new axioms\n'
        text += 'LOGICAL_SAFETY_CLOSURE_PASS 156 safe namespace roots; 1000 total reachable declarations; no unsafe or partial dependencies\n'
        text += 'WITNESS_FINITE_SYNTACTIC_CONSTRUCTION_PASS PiExt=[P01AC.ExtensionalRepair.arrow_identity_has] AllExt=[P01AC.ExtensionalRepair.separation_has]\n'
        self.r.check_t14_stage(stage, text, {})
        for changed in [text.replace('157 declarations', '156 declarations'), text.replace('156 safe namespace roots', '157 safe namespace roots'),
                        text.replace('[propext]', '[sorryAx]', 1), text.replace('INDEPENDENT_AXIOM_PASS', 'MISSING_MARKER'),
                        text + 'INDEPENDENT_AXIOMS ' + names[0] + ': [propext]\n']:
            with self.subTest(text=changed[-180:]), self.assertRaises(ValueError): self.r.check_t14_stage(stage, changed, {})

    def test_written_finite_assert_recipe_does_not_allow_optimized_or_redirected_execution(self):
        driver = {'id': 'exhaustive', 'recipe': 't10-exhaustive-v1', 'source_id': 'source'}
        plan = {'drivers': {'exhaustive': driver}}
        stage = {'kind': 'REFERENCE_TESTS', 'driver_id': 'exhaustive', 'cwd': self.r.T10_CHECKER,
                 'output_paths': ['project/' + self.r.T10_CHECKER + '/logs/exhaustive_results.json'],
                 'argv': ['{tool:python}', '-B', '{driver:exhaustive}']}
        self.r._validate_argv(stage, plan)
        for args in [stage['argv'][:2] + ['-O'] + stage['argv'][2:], stage['argv'] + ['--unchecked']]:
            with self.assertRaises(ValueError): self.r._validate_argv({**stage, 'argv': args}, plan)

    def test_child_trace_records_real_exit_argv_interval_and_stdout(self):
        trace = self.base / 'trace'; trace.mkdir()
        command = [sys.executable, '-I', '-c', 'import sys; print("intended child failure"); sys.exit(1)']
        call = self.r.traced_run(subprocess.run, trace)
        result = call(command, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        record = self.r.read_json(trace / '0000.json')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(record['argv'], command)
        self.assertEqual(record['terminal'], 'COMPLETED')
        self.assertEqual(record['exit_code'], 1)
        self.assertEqual(record['log_sha256'], self.r.sha(result.stdout.encode()))
        self.assertLessEqual(record['started_at'], record['ended_at'])
        with self.assertRaises(ValueError): call(command, shell=True)
        call([sys.executable, '-I', '-c', 'import sys; sys.exit(124)'], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        killed = self.r.read_json(trace / '0001.json')
        self.assertEqual((killed['terminal'], killed['exit_code']), ('INTERRUPTED', None))

    def test_child_trace_timeout_remains_explicit_and_preserves_original_exception(self):
        trace = self.base / 'timeout-trace'; trace.mkdir()
        call = self.r.traced_run(subprocess.run, trace)
        with self.assertRaises(subprocess.TimeoutExpired):
            call([sys.executable, '-I', '-c', 'import time; time.sleep(5)'], text=True,
                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=0.02)
        record = self.r.read_json(trace / '0000.json')
        self.assertEqual((record['terminal'], record['exit_code']), ('TIMEOUT', None))

    def test_trace_entrypoint_preserves_original_driver_context_and_restores_instrumentation(self):
        r = self.r; review = self.base / 'review'; review.mkdir(); candidate = self.base / 'candidate'; candidate.mkdir()
        driver = review / 'run_independent_mutations.py'
        driver.write_text('import subprocess,sys\nassert sys.argv[1] == "--candidate"\nassert __name__ == "__main__"\nsubprocess.run([sys.executable,"-I","-c","raise SystemExit(1)"],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)\n')
        hashes = {}
        for name in ('run_independent_review.py', 'independent_models.py'):
            (review / name).write_bytes(b'# reviewed test fixture\n'); hashes[r.T10_REVIEW + '/' + name] = r.sha((review / name).read_bytes())
        for name in ('context_effects.py', 'read_cover.py'):
            (candidate / name).write_bytes(b'# reviewed candidate fixture\n'); hashes[r.T10_CHECKER + '/' + name] = r.sha((candidate / name).read_bytes())
        argv_before = sys.argv[:]; path_before = sys.path[:]; original_run = subprocess.run
        with mock.patch.dict(r.T10_FINITE_RECIPES, {'t10-independent-mutations-v1': ('fixture', r.sha(driver.read_bytes()))}), mock.patch.dict(r.T10_FILES, hashes):
            if sys.flags.optimize:
                with self.assertRaises(ValueError): r.trace_t10_driver(driver, self.base / 'trace-entry', ['--candidate', str(candidate), '--directory', str(self.base / 'mutants')])
            else:
                r.trace_t10_driver(driver, self.base / 'trace-entry', ['--candidate', str(candidate), '--directory', str(self.base / 'mutants')])
                self.assertEqual(r.read_json(self.base / 'trace-entry/0000.json')['exit_code'], 1)
        self.assertIs(subprocess.run, original_run)
        self.assertEqual((sys.argv, sys.path), (argv_before, path_before))

    def test_observed_child_requires_its_real_parent_terminal_and_unique_identity(self):
        row = {'source_child_id': 'current_only', 'parent_stage_id': 'mutations', 'terminal': 'COMPLETED',
               'exit_code': 1, 'log_sha256': 'a' * 64, 'argv': ['captured'], 'started_at': '2026-10-05T00:00:01Z',
               'ended_at': '2026-10-05T00:00:02Z'}
        parent = {'id': 'mutations', 'terminal': 'COMPLETED', 'exit_code': 0,
                  'started_at': '2026-10-05T00:00:00Z', 'ended_at': '2026-10-05T00:00:03Z'}
        self.r.check_child_terminal(row, parent, 'current_only', ['captured'], set())
        for change in [{'source_child_id': 'foreign'}, {'parent_stage_id': 'other'}, {'terminal': 'TIMEOUT'},
                       {'exit_code': None}, {'exit_code': 124}, {'argv': ['derived']}, {'ended_at': '2026-10-05T00:00:04Z'}]:
            with self.assertRaises(ValueError): self.r.check_child_terminal({**row, **change}, parent, 'current_only', ['captured'], set())
        with self.assertRaises(ValueError): self.r.check_child_terminal(row, {**parent, 'exit_code': 1}, 'current_only', ['captured'], set())
        with self.assertRaises(ValueError): self.r.check_child_terminal(row, parent, 'current_only', ['captured'], {('mutations', 'current_only')})

    def test_observation_receipt_binds_instrumented_launch_and_rejects_missing_or_relabelled_children(self):
        r = self.r; driver = {'id': 'driver', 'recipe': 't10-independent-mutations-v1', 'sha256': 'b' * 64}
        parent = {'id': 'mutations', 'driver_id': 'driver', 'argv': ['{tool:python}', '-B', '{driver:driver}', '--candidate', '{project}/' + r.T10_CHECKER, '--directory', '{out}/mutation-copies']}
        observation = {'id': 'observe', 'driver_id': 'driver', 'argv': ['{builtin:observe-child}', 'mutations', 'current_only']}
        plan = {'stages': {'mutations': parent, 'observe': observation}, 'drivers': {'driver': driver},
                'file_paths': {r.T10_CHECKER + '/context_effects.py': {'source_id': 'candidate'}}, 'contents': {'candidate': b'Ref(consumed)'}}
        stages = {'mutations': {'id': 'mutations', 'terminal': 'COMPLETED', 'exit_code': 0, 'started_at': '2026-10-05T00:00:00Z', 'ended_at': '2026-10-05T00:00:03Z', 'log_sha256': 'c' * 64},
                  'observe': {'id': 'observe', 'terminal': 'COMPLETED', 'exit_code': 1, 'started_at': '2026-10-05T00:00:04Z', 'ended_at': '2026-10-05T00:00:05Z', 'log_sha256': 'd' * 64}}
        launch = {'parent_stage_id': 'mutations', 'driver_sha256': driver['sha256'], 'source_argv': parent['argv'], 'launch_argv': r.t10_tracer_argv(parent),
                  'runner_sha256': 'a' * 64, 'trace_sha256': 'e' * 64, 'parent_log_sha256': 'c' * 64, 'child_count': 9}
        child = {'stage_id': 'observe', 'source_child_id': 'current_only', 'parent_stage_id': 'mutations', 'driver_sha256': driver['sha256'],
                 'parser_id': driver['recipe'], 'mode': 'NONEXECUTING_OBSERVATION', 'argv_provenance': 'CAPTURED', 'argv': r.t10_child_argv('current_only'), 'cwd': '{project}',
                 'started_at': '2026-10-05T00:00:01Z', 'ended_at': '2026-10-05T00:00:02Z', 'observed_at': '2026-10-05T00:00:05Z', 'physical_run_sha256': 'e' * 64,
                 'parent_log_sha256': 'c' * 64, 'terminal': 'COMPLETED', 'exit_code': 1, 'actual_outcome': 'REJECT', 'log_sha256': 'd' * 64,
                 'mutated_source_sha256': r.sha(b'Ref(0)'), 'matched_source_literals': ['direct stack'], 'result_record_sha256': 'f' * 64}
        evidence = {'runner_sha256': 'a' * 64, 'driver_invocations': [launch], 'child_observations': [child]}
        r.validate_child_evidence(evidence, plan, stages, True)
        for change in [{'child_observations': []}, {'driver_invocations': []}, {'child_observations': [child, child]},
                       {'child_observations': [{**child, 'source_child_id': 'foreign'}]},
                       {'child_observations': [{**child, 'argv_provenance': 'DERIVED_FROM_REVIEWED_RECIPE'}]},
                       {'child_observations': [{**child, 'physical_run_sha256': '9' * 64}]},
                       {'child_observations': [{**child, 'exit_code': None}]},
                       {'driver_invocations': [{**launch, 'launch_argv': parent['argv']}]},
                       {'driver_invocations': [{**launch, 'parent_log_sha256': '8' * 64}]}]:
            with self.assertRaises(ValueError): r.validate_child_evidence({**evidence, **change}, plan, stages, True)

    def test_original_mutation_parser_requires_actual_child_records_and_exact_mutant_bytes(self):
        r = self.r
        originals = {name: ('\n'.join(before for _, file, changes in r._t10_MUTATIONS if file == name for before, _ in changes)).encode()
                     for name in ('context_effects.py', 'read_cover.py')}
        mutation_driver = b'original-driver-fixture'
        review_driver = ' '.join(s for values in r.T10_CHILD_DIAGNOSTICS.values() for s in values).encode()
        artifacts = {}; records = []
        for name, filename, changes in r._t10_MUTATIONS:
            mutated = originals[filename].decode(); replacements = []
            for before, after in changes:
                replacements.append({'old': before, 'new': after, 'occurrences': mutated.count(before)})
                mutated = mutated.replace(before, after)
            last = 'AssertionError: ' + r.T10_CHILD_DIAGNOSTICS[name][0]
            artifacts[name] = {**originals, filename: mutated.encode(), 'run.log': ('Traceback (most recent call last):\n' + last + '\n').encode()}
            records.append({'name': name, 'candidate_file': filename, 'mutated_sha256': r.sha(mutated.encode()), 'replacements': replacements,
                            'exit': 1, 'killed_by_independent_assertion': True, 'last_line': last, 'seconds': 0.1})
        hashes = {key: r.sha(value) for key, value in originals.items()}
        result = {'status': 'PASS', 'count': 9, 'mutation_boundary': 'only reviewer-owned file copies; original files unchanged', 'source_hashes': hashes, 'records': records}
        stdout = ''.join(name + ' KILLED\n' for name in r.T10_CHILD_DIAGNOSTICS).encode()
        def check(value, children):
            return r._t10_checked_mutation_children(json.dumps(value).encode(), stdout, originals, children, mutation_driver, review_driver)
        with mock.patch.multiple(r, _t10_MUTATION_DRIVER_SHA256=r.sha(mutation_driver), _t10_REVIEW_DRIVER_SHA256=r.sha(review_driver), _t10_ORIGINAL_HASHES=hashes):
            self.assertEqual(len(check(result, artifacts)), 9)
            for code in (0, True, 124, None, -9):
                changed = copy.deepcopy(result); changed['records'][0]['exit'] = code
                with self.assertRaises(ValueError): check(changed, artifacts)
            changed = copy.deepcopy(artifacts); changed['current_only']['context_effects.py'] += b'unapproved change'
            with self.assertRaises(ValueError): check(result, changed)
            changed = copy.deepcopy(artifacts); del changed['current_only']['run.log']
            with self.assertRaises(ValueError): check(result, changed)

    def test_finite_semantic_assertions_are_accept_and_require_complete_distinctions(self):
        r = self.r; names = r.T10_GROUPS['semantic']
        result = {'status': 'PASS', 'semantic_mutants': 16, 'killed': 16, 'scope': 'finite fixture',
                  'results': [{'id': name, 'status': 'KILLED', 'correct': 'a', 'mutant': 'b', 'mechanism': 'explicit inequality'} for name in names]}
        actual = r._t10_checked_semantic_assertions(json.dumps(result).encode(), names)
        self.assertEqual({row['actual_outcome'] for row in actual}, {'ACCEPT'})
        result['results'][0]['mutant'] = 'a'
        with self.assertRaises(ValueError): r._t10_checked_semantic_assertions(json.dumps(result).encode(), names)

    def test_isolated_control_objects_take_precedence_only_from_declared_outputs(self):
        plan = {'build_roots': ['build', 'control'], 'stages': {
            'prerequisite': {'output_paths': ['control/KernelAudit.olean']}}}
        stage = {'output_paths': [], 'depends_on': ['prerequisite']}
        env = {'LEAN_PATH': os.pathsep.join([str(self.base/'build'), str(self.base/'official')])}
        result = self.r.stage_environment(stage, plan, self.base, env)
        self.assertEqual(result['LEAN_PATH'].split(os.pathsep)[0], str(self.base/'control'))
        self.assertEqual(env['LEAN_PATH'].split(os.pathsep)[0], str(self.base/'build'))

    def test_fresh_control_build_root_is_explicit_and_cannot_alias_sources(self):
        stage = self.suite['replay']['stages'][0]
        self.suite['replay']['build_roots'] = ['prereq-control']
        stage['argv'][3] = '{out}/prereq-control/Proof.olean'
        stage['output_paths'] = ['prereq-control/Proof.olean']
        self.validate()
        stage['argv'][3] = '{out}/undeclared/Proof.olean'
        stage['output_paths'] = ['undeclared/Proof.olean']
        with self.assertRaises(ValueError): self.validate()

    def test_file_fixture_copies_exact_input_before_changing_disposable_copy(self):
        original = self.base / 'locked.zip'
        original.write_bytes(b'exact original data')
        plan = {'inputs': {'data': {'id': 'data', 'kind': 'FILE'}}, 'input_manifests': {}}
        row = {'id': 'changed', 'input_id': 'data', 'operation': 'APPEND_CHANGED_BYTES', 'path': None}
        out = self.base / 'output'; out.mkdir()
        changed = self.r._make_fixture(row, plan, {'data': original}, out)
        self.assertEqual(original.read_bytes(), b'exact original data')
        self.assertEqual(changed.read_bytes(), b'exact original data\nchanged-byte-control\n')
        with self.assertRaises(ValueError): self.r._make_fixture(row, plan, {'data': original}, out)

    def test_reviewed_empirical_argv_cannot_redirect_input_or_add_python_code(self):
        driver = {'id': 'analysis', 'recipe': 't15-empirical-reanalyse-v1'}
        plan = {'drivers': {'analysis': driver}, 'inputs': {'decisions_zip': {'kind': 'FILE'}, 'summary_xlsx': {'kind': 'FILE'}}, 'fixtures': {}}
        stage = {'kind': 'REFERENCE_TESTS', 'driver_id': 'analysis', 'cwd': '.', 'output_paths': ['aggregate.json'],
                 'argv': ['{tool:python}', '-B', '{driver:analysis}', '--decisions-zip', '{input:decisions_zip}',
                          '--summary-xlsx', '{input:summary_xlsx}', '--output', '{out}/aggregate.json']}
        self.r._validate_argv(stage, plan)
        for argv in [stage['argv'] + ['-c', 'print(1)'], stage['argv'][:-1] + ['{input:decisions_zip}']]:
            with self.assertRaises(ValueError): self.r._validate_argv({**stage, 'argv': argv}, plan)

    def test_empirical_verbose_tests_require_actual_complete_successes(self):
        names = ['test_a', 'test_b']
        good = 'test_a (test_package.PackageTests.test_a) ... ok\ntest_b (test_package.PackageTests.test_b) ... ok\nRan 2 tests in 0.2s\n\nOK\n'
        self.r.check_unittest_log(good, names)
        for log in [good.replace('test_b (test_package.PackageTests.test_b) ... ok\n', ''),
                    good.replace('... ok', '... skipped reason', 1), good.replace('Ran 2', 'Ran 1')]:
            with self.assertRaises(ValueError): self.r.check_unittest_log(log, names)

    def test_original_readbacks_require_exact_inventory_and_allowed_axioms(self):
        good = "'First.a' does not depend on any axioms\n'Second.b' depends on axioms: [propext, Classical.choice]\n"
        self.r.check_original_readbacks(good, ['First.a', 'Second.b'])
        for bad in [good.splitlines()[0], good + good, good.replace('Second.b', 'Other.b'), good.replace('propext', 'sorryAx')]:
            with self.assertRaises(ValueError): self.r.check_original_readbacks(bad, ['First.a', 'Second.b'])

    def test_original_readback_resolves_exact_source_namespace_not_suffix(self):
        source = 'namespace Outer.Review\nmutual\ndef value : Nat := 1\nend\nsection\n#print axioms witness\nend\nend Outer.Review\n#print axioms Global.witness\n'
        known = [{'name': 'Outer.Review.witness'}, {'name': 'Other.witness'}, {'name': 'Global.witness'}]
        names = self.r.source_readback_names(source, known)
        self.assertEqual(names, ['Outer.Review.witness', 'Global.witness'])
        good = "'Outer.Review.witness' does not depend on any axioms\n'Global.witness' depends on axioms: [propext]\n"
        self.r.check_original_readbacks(good, names)
        with self.assertRaises(ValueError): self.r.check_original_readbacks(good.replace('Outer.Review.witness', 'Other.witness'), names)

    def test_source_local_dotted_theorem_readbacks_keep_their_namespace(self):
        source = 'namespace Outer.Review\ntheorem Expr.one : True := True.intro\nsection\ntheorem Expr.two : True := True.intro\nend\n#print axioms Expr.one\n#print axioms Expr.two\nend Outer.Review\n'
        expected = ['Outer.Review.Expr.one', 'Outer.Review.Expr.two']
        for known in [[], [{'name': 'Expr.one'}, {'name': 'Other.Expr.two'}]]:
            self.assertEqual(self.r.source_readback_names(source, known), expected)
        log = "'Outer.Review.Expr.one' does not depend on any axioms\n'Outer.Review.Expr.two' depends on axioms: [propext,\n Classical.choice,\n Quot.sound]\n"
        self.r.check_original_readbacks(log, self.r.source_readback_names(source, []))
        for wrong in [log.replace('Outer.Review.Expr.one', 'Expr.one'), log.replace('Quot.sound', 'sorryAx'), log + log]:
            with self.assertRaises(ValueError): self.r.check_original_readbacks(wrong, expected)

    def test_source_local_readback_resolution_uses_only_prior_explicit_theorems(self):
        source = 'namespace Outer\n#print axioms Expr.later\ntheorem Expr.later : True := True.intro\n#print axioms Expr.later\nend Outer\nnamespace Foreign\n#print axioms Expr.later\nend Foreign\n'
        self.assertEqual(self.r.source_readback_names(source, []), ['Expr.later', 'Outer.Expr.later', 'Expr.later'])
        explicit = 'namespace Outer\ntheorem _root_.Global.proof : True := True.intro\n#print axioms _root_.Global.proof\nend Outer\n'
        self.assertEqual(self.r.source_readback_names(explicit, []), ['Global.proof'])

    def test_unused_tool_dependency_needs_pin_but_not_a_nonexistent_library(self):
        library = self.base / 'no-cli-library'
        self.assertEqual(self.r.package_library('Cli', library, {}), [])
        with self.assertRaises(self.r.MissingTool):
            self.r.package_library('Cli', library, {'Cli': {'package': 'Cli'}})

    def test_case_insensitive_projection_collision_fails(self):
        self.suite['replay']['files'][1]['path'] = 'proof.lean'
        with self.assertRaises(ValueError): self.validate()

    def test_import_assertion_must_match_actual_source(self):
        self.suite['replay']['modules'][0]['imports'] = []
        with self.assertRaises(ValueError): self.validate()

    def test_positive_closure_cannot_import_negative_fixture(self):
        add_source(self.root, self.sources, 'proof', 'Proof.lean', 'import BadProof\nnamespace Fixture\ntheorem ok : True := True.intro\nend Fixture\n')
        self.suite['replay']['modules'][0]['imports'] = ['Init', 'BadProof']
        with self.assertRaises(ValueError): self.validate()

    def test_runtime_word_does_not_replace_actual_proof_audit(self):
        add_source(self.root, self.sources, 'proof', 'Proof.lean', 'import Init\nnamespace Fixture\nunsafe def auxiliary : Nat := 0\ntheorem ok : True := True.intro\nend Fixture\n')
        self.validate()

    def test_undeclared_command_and_compiler_options_fail(self):
        self.suite['replay']['stages'][0]['argv'] = ['python', '-c', 'print(1)']
        with self.assertRaises(ValueError): self.validate()

    def test_missing_positive_prerequisite_fails(self):
        self.suite['replay']['stages'][1]['depends_on'] = []
        with self.assertRaises(ValueError): self.validate()

    def test_omitted_control_and_unbound_diagnostic_fail(self):
        self.suite['replay']['stages'][1]['control_ids'] = []
        with self.assertRaises(ValueError): self.validate()
        self.suite['replay']['stages'][1]['control_ids'] = ['negative']
        self.suite['replay']['stages'][1]['expected_diagnostics'][0]['literal'] = 'invented reason'
        with self.assertRaises(ValueError): self.validate()

    def test_wrong_official_binary_and_package_pins_fail(self):
        self.suite['toolchain']['executable_sha256'] = 'f' * 64
        with self.assertRaises(ValueError): self.validate()
        self.suite['toolchain']['executable_sha256'] = LEAN_SHA
        self.suite['toolchain']['packages'] = [{'name': 'mathlib', 'revision': 'bad', 'sha256': 'a' * 64}]
        with self.assertRaises(ValueError): self.validate()

    def test_extra_tool_cannot_replace_the_primary_tool(self):
        self.suite['replay']['tools'] = [{'name': 'lean', 'kind': 'PYTHON', 'version': '3.11.9', 'platform': 'test',
                                        'executable_sha256': sha('python'), 'path_kind': 'EXECUTABLE'}]
        with self.assertRaises(ValueError): self.validate()

    def test_source_and_output_traversal_fail(self):
        for field, value in [('path', '../outside.lean'), ('path', 'C:/outside.lean'), ('path', 'nested//Proof.lean')]:
            original = self.suite['replay']['files'][0][field]
            self.suite['replay']['files'][0][field] = value
            with self.assertRaises(ValueError): self.validate()
            self.suite['replay']['files'][0][field] = original
        self.suite['replay']['stages'][0]['output_paths'] = ['../outside.olean']
        with self.assertRaises(ValueError): self.validate()

    def test_source_symlink_fails(self):
        original = self.root / self.sources['proof']['public_path']
        other = self.base / 'other.lean'
        other.write_bytes(original.read_bytes())
        original.unlink()
        try: original.symlink_to(other)
        except OSError as error: self.skipTest('Host cannot create a symlink: ' + str(error))
        with self.assertRaises(ValueError): self.validate()

    def test_output_reuse_and_repository_output_fail_without_damage(self):
        occupied = self.base / 'occupied'
        occupied.mkdir()
        (occupied / 'retain').write_text('preserve')
        for output in [occupied, self.root / 'new-output']:
            with self.assertRaises(ValueError):
                self.r.project_suite(self.suite, self.sources, self.root, output)
        self.assertEqual((occupied / 'retain').read_text(), 'preserve')
        self.assertFalse((self.root / 'new-output').exists())

    def test_missing_tool_is_blocked_and_receipt_is_not_qualified(self):
        receipt = self.r.execute_suite(self.suite, self.sources, self.root, self.base / 'out', {}, {}, reviews=self.reviews)
        self.assertEqual((receipt['outcome'], receipt['exit_code'], receipt['proof_scope']), ('BLOCKED_TOOLCHAIN', 2, 'NONE'))
        self.r.validate_receipt(receipt, self.suite, self.sources, self.root)
        saved = json.loads((self.base / 'out/RECEIPT.json').read_text())
        self.assertEqual(saved, receipt)

    def test_wrong_binary_never_executes_or_earns_credit(self):
        fake = self.base / 'lean'
        fake.write_bytes(b'not an official executable')
        receipt = self.r.execute_suite(self.suite, self.sources, self.root, self.base / 'out', {'lean': fake}, {}, reviews=self.reviews)
        self.assertEqual((receipt['outcome'], receipt['exit_code']), ('FAILED', 1))

    def test_stale_receipt_and_fabricated_success_fail(self):
        receipt = self.r.execute_suite(self.suite, self.sources, self.root, self.base / 'out', {}, {}, reviews=self.reviews)
        stale = copy.deepcopy(receipt)
        stale['suite_sha256'] = 'f' * 64
        with self.assertRaises(ValueError): self.r.validate_receipt(stale, self.suite, self.sources, self.root)
        receipt['outcome'] = 'QUALIFIED_DECLARED_SUITE'
        receipt['exit_code'] = 0
        receipt['proof_scope'] = 'DECLARED_SUITE'
        with self.assertRaises(ValueError): self.r.validate_receipt(receipt, self.suite, self.sources, self.root)

    def synthetic_completed_receipt(self):
        receipt = self.r._initial_receipt(self.suite, self.sources, self.reviews)
        ev = receipt['replay_evidence']
        definitions = {'lean': self.suite['toolchain'], **{r['name']: r for r in self.suite['replay']['tools']}}
        ev['tool_fingerprints'] = {name: {key: row[key] for key in ('kind', 'version', 'platform', 'executable_sha256')} |
                                   {'version_log_sha256': sha(name)} for name, row in definitions.items()}
        for row in ev['stage_results']:
            row.update(terminal='COMPLETED', exit_code=1 if row['id'] == 'negative' else 0)
            if row['id'] == 'positive': row['output_hashes'] = {'build/Proof.olean': sha('object')}
        ev['output_hashes'] = {'build/Proof.olean': sha('object')}
        stages = {row['id']: row for row in ev['stage_results']}
        ev['target_audits'] = [{'target_id': 'main', 'name': 'Fixture.ok', 'type_sha256': sha('True'), 'axioms': [],
                               'closure_status': 'CHECKED_SAFE', 'checked_declarations': 1,
                               'stage_id': '_target_audit', 'log_sha256': stages['_target_audit']['log_sha256']}]
        for control, stage in zip(self.suite['controls'], self.suite['replay']['stages']):
            actual = control['expected_outcome']
            receipt['controls'].append({key: control[key] for key in ('id', 'source_id', 'target_id', 'role', 'expected_outcome_sha256')} |
                {'actual_outcome': actual, 'actual_outcome_sha256': sha(actual), 'terminal': 'COMPLETED',
                 'exit_code': stages[stage['id']]['exit_code'], 'log_sha256': sha(b'')})
            ev['control_diagnostics'].append({'control_id': control['id'], 'stage_id': stage['id'],
                'prerequisite_stage_ids': stage['depends_on'], 'expected': stage['expected_diagnostics'],
                'observed_log_sha256': sha(b''), 'match': 'MATCHED'})
        receipt['stages'] = [{key: row[key] for key in ('id', 'terminal', 'exit_code', 'log_sha256')} for row in ev['stage_results']]
        receipt.update(outcome='FRESH_KERNEL_COMPONENTS', proof_scope='COMPONENTS', exit_code=0,
                       log_sha256=canonical({row['id']: row['log_sha256'] for row in ev['stage_results']}))
        return receipt

    def test_receipt_recomputes_import_and_every_declared_tool_fingerprint(self):
        self.suite['replay']['tools'] = [{'name': 'python', 'kind': 'PYTHON', 'version': '3.11.9', 'platform': 'test',
                                        'executable_sha256': sha('python'), 'path_kind': 'EXECUTABLE'}]
        receipt = self.synthetic_completed_receipt()
        self.r.validate_receipt(receipt, self.suite, self.sources, self.root)
        for change in ['imports', 'missing_extra', 'substituted_extra', 'version']:
            bad = copy.deepcopy(receipt); ev = bad['replay_evidence']
            if change == 'imports': ev['import_fingerprints']['Proof'] = sha('wrong imports')
            elif change == 'missing_extra': del ev['tool_fingerprints']['python']
            elif change == 'substituted_extra': ev['tool_fingerprints']['python']['executable_sha256'] = sha('different binary')
            else: ev['tool_fingerprints']['python']['version'] = '3.12.0'
            with self.assertRaises(ValueError, msg=change): self.r.validate_receipt(bad, self.suite, self.sources, self.root)

    def test_reserved_audit_invocation_is_not_producer_selected(self):
        receipt = self.synthetic_completed_receipt()
        self.r.validate_receipt(receipt, self.suite, self.sources, self.root)
        receipt['replay_evidence']['stage_results'][-1]['argv'] = ['unapproved-auditor']
        with self.assertRaises(ValueError): self.r.validate_receipt(receipt, self.suite, self.sources, self.root)

    def test_receipt_rechecks_dependency_revision_and_source_manifest(self):
        pin = 'c' * 40
        add_source(self.root, self.sources, 'lock', 'lake-manifest.json', json.dumps({'packages': [{'name': 'mathlib', 'rev': pin}]}))
        self.suite['source_ids'].append('lock')
        self.suite['replay']['files'].append({'source_id': 'lock', 'path': 'lake-manifest.json', 'role': 'LOCK'})
        self.suite['replay']['package_manifest_source_id'] = 'lock'
        self.suite['replay']['packages'] = [{'name': 'mathlib', 'kind': 'GIT', 'path': '.', 'manifest_source_id': 'lock'}]
        self.suite['toolchain']['packages'] = [{'name': 'mathlib', 'revision': pin, 'sha256': canonical({'name': 'mathlib', 'revision': pin})}]
        receipt = self.synthetic_completed_receipt()
        receipt['replay_evidence']['dependency_checks'] = {'mathlib': {'kind': 'GIT', 'revision': pin,
            'manifest_sha256': self.sources['lock']['public_sha256'], 'tracked_clean': True,
            'cache_policy': 'TRUSTED_PINNED_OFFICIAL_CACHE', 'head_log_sha256': sha('head'), 'status_log_sha256': sha('clean')}}
        self.r.validate_receipt(receipt, self.suite, self.sources, self.root)
        for field, wrong in [('revision', 'd' * 40), ('manifest_sha256', sha('other lock')), ('tracked_clean', False)]:
            bad = copy.deepcopy(receipt); bad['replay_evidence']['dependency_checks']['mathlib'][field] = wrong
            with self.assertRaises(ValueError, msg=field): self.r.validate_receipt(bad, self.suite, self.sources, self.root)

    def test_target_audit_timeout_remains_resource_inconclusive(self):
        def environment(suite, plan, tools, inputs, output):
            (output / 'build').mkdir()
            return {'lean': Path('synthetic')}, {}, {}, {}, {}
        def child(argv, cwd, env, log, timeout):
            log = Path(log)
            if 'V5SuccessorReadback' in str(argv[-1]):
                log.write_text('audit budget exhausted')
                terminal, code = 'TIMEOUT', None
            elif '-o' in argv:
                Path(argv[argv.index('-o') + 1]).write_bytes(b'object')
                log.write_text('')
                terminal, code = 'COMPLETED', 0
            else:
                log.write_text('type mismatch')
                terminal, code = 'COMPLETED', 1
            return {'terminal': terminal, 'exit_code': code, 'started_at': self.r.utc(), 'ended_at': self.r.utc(), 'log_sha256': sha(log.read_bytes())}
        with mock.patch.object(self.r, '_verify_environment', side_effect=environment), mock.patch.object(self.r, 'run_process', side_effect=child):
            receipt = self.r.execute_suite(self.suite, self.sources, self.root, self.base / 'timeout-audit', {}, {}, reviews=self.reviews)
        self.assertEqual((receipt['outcome'], receipt['exit_code']), ('RESOURCE_INCONCLUSIVE', 1))
        self.assertEqual(receipt['stages'][-1]['terminal'], 'TIMEOUT')

    def test_rejection_requires_exact_code_diagnostic_and_positive_stage(self):
        stage = self.suite['replay']['stages'][1]
        result = {'terminal': 'COMPLETED', 'exit_code': 1}
        completed = {'positive': {'terminal': 'COMPLETED', 'exit_code': 0, 'matched': True}}
        self.assertTrue(self.r.assess_stage(stage, result, 'error: type mismatch', completed))
        for bad_result, text, prerequisites in [
            ({'terminal': 'TIMEOUT', 'exit_code': None}, 'type mismatch', completed),
            ({'terminal': 'COMPLETED', 'exit_code': 124}, 'type mismatch', completed),
            (result, 'unknown module Proof', completed),
            (result, 'type mismatch\nunknown module Proof', completed),
            (result, 'type mismatch', {}),
        ]:
            with self.assertRaises(ValueError): self.r.assess_stage(stage, bad_result, text, prerequisites)

    def test_resource_exit_cannot_be_declared_an_expected_rejection(self):
        for code in [124, 137, 143, -9, True]:
            self.suite['replay']['stages'][1]['expected_exit_codes'] = [code]
            with self.assertRaises(ValueError): self.validate()

    def test_real_process_keeps_nonzero_and_timeout_distinct(self):
        result = self.r.run_process([sys.executable, '-c', 'print("concrete"); raise SystemExit(2)'],
                                    self.base, dict(os.environ), self.base / 'concrete.log', 10)
        self.assertEqual((result['terminal'], result['exit_code']), ('COMPLETED', 2))
        result = self.r.run_process([sys.executable, '-c', 'import time; time.sleep(10)'],
                                    self.base, dict(os.environ), self.base / 'timeout.log', 0.1)
        self.assertEqual((result['terminal'], result['exit_code']), ('TIMEOUT', None))

    def transcript(self):
        return ('V5_BEGIN Fixture.ok\nFixture.ok : True\n'
                "'Fixture.ok' does not depend on any axioms\n"
                'V5_OWNER Fixture.ok Proof\nV5_SAFE Fixture.ok 11 []\nV5_END Fixture.ok\n')

    def test_exact_target_owner_axioms_and_complete_closure_are_required(self):
        targets = self.suite['replay']['target_names']
        actual = self.r.parse_readbacks(self.transcript(), targets)
        self.assertEqual(actual['main']['axioms'], [])
        self.assertEqual(actual['main']['checked_declarations'], 11)
        for bad in [self.transcript() * 2, self.transcript().replace('V5_END Fixture.ok', ''),
                    self.transcript().replace('V5_OWNER Fixture.ok Proof', 'V5_OWNER Fixture.ok Foreign'),
                    self.transcript().replace('does not depend on any axioms', 'depends on axioms: [sorryAx]'),
                    self.transcript().replace('V5_SAFE Fixture.ok 11 []', 'V5_SAFE Fixture.ok 0 []')]:
            with self.assertRaises(ValueError): self.r.parse_readbacks(bad, targets)

    def test_readback_markers_match_complete_names_not_shared_prefixes(self):
        second = self.transcript().replace('Fixture.ok', 'Fixture.ok_type')
        targets = self.suite['replay']['target_names'] + [{'target_id': 'second', 'name': 'Fixture.ok_type', 'module': 'Proof'}]
        parsed = self.r.parse_readbacks(self.transcript() + second, targets)
        self.assertEqual(set(parsed), {'main', 'second'})

    def test_duplicate_json_keys_and_nonfinite_numbers_fail(self):
        for content in ['{"id":1,"id":2}', '{"budget":NaN}']:
            path = self.base / 'bad.json'
            path.write_text(content)
            with self.assertRaises(ValueError): self.r.read_json(path)

    @unittest.skipUnless(os.environ.get('V5_REPLAY_TEST_LEAN'), 'Explicit official Lean test binding required')
    def test_official_lean_shared_dependency_graph_uses_unique_declaration_budget(self):
        # Forty declarations share an increasingly dense predecessor graph.
        # Its distinct closure fits 128 visits, while repeated edges do not.
        declarations = ['namespace SharedFixture', 'theorem leaf : True := True.intro',
                        'def choose (left : True) (_right : True) : True := left']
        for index in range(40):
            value = 'leaf'
            for predecessor in range(index):
                value = f'choose node{predecessor} ({value})'
            declarations.append(f'theorem node{index} : True := {value}')
        declarations.append('end SharedFixture')
        check = '''run_cmd do
  let (count, _) ← V5SuccessorCheckedAudit.audit `SharedFixture.node39
  unless count < 128 do throwError "Fixture distinct closure exceeds its test budget"
  logInfo "SHARED_CLOSURE_CHECKED"
'''
        header = self.r._audit_source([])
        for label, budget, extra, expected in [
                ('shared', 128, '', 'SHARED_CLOSURE_CHECKED'),
                ('bounded', 2, '', 'INCOMPLETE_PROOF_CLOSURE'),
                ('forged', 128, 'axiom forged : True\n', 'UNAPPROVED_AXIOM')]:
            body = '\n'.join(declarations)
            if extra: body = extra + body.replace('theorem leaf : True := True.intro', 'theorem leaf : True := forged')
            source = self.base / (label + '.lean')
            source.write_text(header.replace('[:1000000]', f'[:{budget}]') + body + '\n' + check, encoding='utf8')
            log = self.base / (label + '.log')
            result = self.r.run_process([os.environ['V5_REPLAY_TEST_LEAN'], '-j1', source], self.base, dict(os.environ), log, 60)
            text = log.read_text(encoding='utf8')
            self.assertEqual(result['terminal'], 'COMPLETED', text)
            self.assertEqual(result['exit_code'], 0 if label == 'shared' else 1, text)
            self.assertIn(expected, text)

    @unittest.skipUnless(os.environ.get('V5_REPLAY_TEST_LEAN'), 'Explicit official Lean test binding required')
    def test_official_lean_t14_audit_message_format(self):
        body = '''import Lean
namespace P01AC
theorem first : True := True.intro
theorem second : True := first
end P01AC
open Lean Elab Command
run_cmd do
  let checks : Array Name := #[`P01AC.first, `P01AC.second]
  for n in checks do
    let axs ← Lean.collectAxioms n
    logInfo m!"{n}: {axs}"
  logInfo m!"AXIOM_AUDIT_PASS: {checks.size} checked theorem closures contain no extra assumptions."
  let piSites : Array Name := #[`P01AC.ExtensionalRepair.arrow_identity_has]
  let allSites : Array Name := #[`P01AC.ExtensionalRepair.separation_has]
  logInfo m!"WITNESS_FINITE_SYNTACTIC_CONSTRUCTION_PASS PiExt={piSites} AllExt={allSites}"
'''
        source = self.base / 'Format.lean'; source.write_text(body, encoding='utf8')
        log = self.base / 'format.log'
        result = self.r.run_process([os.environ['V5_REPLAY_TEST_LEAN'], '-j1', source], self.base, dict(os.environ), log, 60)
        text = log.read_text(encoding='utf8')
        self.assertEqual((result['terminal'], result['exit_code']), ('COMPLETED', 0), text)
        stage = {'kind': 'LEAN_AUDIT', 'argv': ['{tool:lean}', '-j1', '{project}/verification/AxiomAudit.lean']}
        plan = {'file_paths': {'verification/AxiomAudit.lean': {'source_id': 'audit'}}, 'contents': {'audit': body.encode()}}
        self.r.check_t14_stage(stage, text, plan)
        self.assertIn('PiExt=[P01AC.ExtensionalRepair.arrow_identity_has] AllExt=[P01AC.ExtensionalRepair.separation_has]', text)

    @unittest.skipUnless(os.environ.get('V5_REPLAY_TEST_LEAN'), 'Explicit official Lean test binding required')
    def test_official_lean_fresh_closure_and_actual_hole_rejection(self):
        tools = {'lean': Path(os.environ['V5_REPLAY_TEST_LEAN'])}
        add_source(self.root, self.sources, 'proof', 'Proof.lean',
                   'import Init\nnamespace Fixture\nunsafe def auxiliary : Nat := 0\ntheorem ok : True := True.intro\nend Fixture\n')
        receipt = self.r.execute_suite(self.suite, self.sources, self.root, self.base / 'safe', tools, {}, reviews=self.reviews)
        self.assertEqual((receipt['outcome'], receipt['exit_code']), ('FRESH_KERNEL_COMPONENTS', 0),
                         '\n'.join(p.read_text(errors='replace') for p in (self.base / 'safe/logs').glob('*')))
        self.assertEqual(receipt['replay_evidence']['target_audits'][0]['closure_status'], 'CHECKED_SAFE')
        self.assertEqual(receipt['controls'][1]['exit_code'], 1)
        self.assertEqual(receipt['controls'][1]['actual_outcome'], 'REJECT')
        add_source(self.root, self.sources, 'proof', 'Proof.lean',
                   'import Init\nnamespace Fixture\ntheorem ok : True := by sorry\nend Fixture\n')
        receipt = self.r.execute_suite(self.suite, self.sources, self.root, self.base / 'hole', tools, {}, reviews=self.reviews)
        self.assertEqual((receipt['outcome'], receipt['exit_code']), ('FAILED', 1))
        self.assertEqual(receipt['replay_evidence']['target_audits'], [])


class ImportedReadbackTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('imported_readback_adapter', SCRIPT)
        cls.r = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.r)

    def plan(self, bodies, targets=()):
        return {'modules': {name: {'name': name, 'source_id': name, 'imports': self.r.imports(body)} for name, body in bodies.items()},
                'contents': {name: body.encode() for name, body in bodies.items()},
                'official': {'Init': {}}, 'targets': {str(i): row for i, row in enumerate(targets)}}

    def names(self, bodies, source='Readback', targets=()):
        return self.r.source_readback_names_in_plan(source, self.plan(bodies, targets))

    def test_open_names_resolve_from_exact_transitive_imports_and_multiline_declarations(self):
        bodies = {'Owner': 'namespace Exact\ntheorem first : True := True.intro\ntheorem second\n    : True := first\nend Exact\n',
                  'Bridge': 'import Owner\n', 'Readback': 'import Bridge\nopen Exact\n#print axioms first\n#print axioms second\n'}
        self.assertEqual(self.names(bodies), ['Exact.first', 'Exact.second'])
        log = "'Exact.first' does not depend on any axioms\n'Exact.second' does not depend on any axioms\n"
        self.r.check_original_readbacks(log, self.names(bodies))
        with self.assertRaises(ValueError): self.r.check_original_readbacks(log.replace('Exact.first', 'Other.first'), self.names(bodies))

    def test_unimported_or_changed_owner_cannot_supply_opened_readback(self):
        bodies = {'Owner': 'namespace Exact\ntheorem proof : True := True.intro\nend Exact\n',
                  'Readback': 'open Exact\n#print axioms proof\n'}
        self.assertEqual(self.names(bodies, targets=[{'name': 'Exact.proof'}]), ['proof'])
        bodies['Readback'] = 'import Owner\nopen Exact\n#print axioms proof\n'
        self.assertEqual(self.names(bodies), ['Exact.proof'])
        bodies['Owner'] = bodies['Owner'].replace('theorem proof', 'theorem different')
        with self.assertRaises(ValueError):
            self.r.check_original_readbacks("'Exact.proof' does not depend on any axioms\n", self.names(bodies))

    def test_open_scope_and_named_selection_do_not_leak(self):
        bodies = {'Owner': 'namespace Exact\ndef value : Nat := 1\ntheorem proof : True := True.intro\nend Exact\n',
                  'Readback': 'import Owner\nsection\nopen Exact (\n proof\n)\n#print axioms proof\n#print axioms value\nend\n#print axioms proof\n'}
        self.assertEqual(self.names(bodies), ['Exact.proof', 'value', 'proof'])

    def test_ambiguous_opened_names_are_not_resolved_by_target_map_or_output(self):
        bodies = {'One': 'namespace One\ntheorem proof : True := True.intro\nend One\n',
                  'Two': 'namespace Two\ntheorem proof : True := True.intro\nend Two\n',
                  'Readback': 'import One Two\nopen One Two\n#print axioms proof\n'}
        with self.assertRaises(ValueError): self.names(bodies, targets=[{'name': 'One.proof'}])
        bodies['Readback'] = 'import One Two\nopen One Two\nnamespace Local\ntheorem proof : True := True.intro\n#print axioms proof\nend Local\n'
        self.assertEqual(self.names(bodies), ['Local.proof'])

    def test_comments_strings_private_names_and_later_declarations_do_not_authorize_open(self):
        bodies = {'Owner': 'namespace Exact\n-- theorem hidden : True := True.intro\ndef text := "theorem hidden : True := True.intro"\nprivate theorem hidden : True := True.intro\nend Exact\n',
                  'Readback': 'import Owner\nopen Exact\n#print axioms hidden\nnamespace Exact\ntheorem later : True := True.intro\nend Exact\n'}
        self.assertEqual(self.names(bodies), ['hidden'])
        bodies['Readback'] = 'import Owner\nopen Exact hiding text\n#print axioms hidden\n'
        with self.assertRaises(ValueError): self.names(bodies)

    def test_import_closure_must_match_source_and_must_not_cycle(self):
        bodies = {'Owner': 'namespace Exact\ntheorem proof : True := True.intro\nend Exact\n',
                  'Readback': 'open Exact\n#print axioms proof\n'}
        plan = self.plan(bodies); plan['modules']['Readback']['imports'].append('Owner')
        with self.assertRaises(ValueError): self.r.source_readback_names_in_plan('Readback', plan)
        bodies['Readback'] = 'import Owner\nopen Exact\n#print axioms proof\n'; bodies['Owner'] = 'import Readback\n' + bodies['Owner']
        with self.assertRaises(ValueError): self.names(bodies)

    @unittest.skipUnless(os.environ.get('V5_REPLAY_TEST_LEAN'), 'Explicit official Lean test binding required')
    def test_official_lean_imported_readbacks_match_source_derived_names(self):
        bodies = {'Owner': 'namespace Exact\ntheorem proof\n    : True := True.intro\nend Exact\n',
                  'Readback': 'import Owner\nopen Exact\n#print axioms proof\n'}
        expected = self.names(bodies)
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp); env = dict(os.environ, LEAN_PATH=temp); lean = os.environ['V5_REPLAY_TEST_LEAN']
            for name, body in bodies.items(): (root / (name + '.lean')).write_text(body, encoding='utf8')
            for name in bodies:
                log = root / (name + '.log')
                argv = [lean, '-j1'] + (['-o', str(root / 'Owner.olean')] if name == 'Owner' else []) + [str(root / (name + '.lean'))]
                result = self.r.run_process(argv, root, env, log, 30)
                self.assertEqual((result['terminal'], result['exit_code']), ('COMPLETED', 0), log.read_text())
            self.r.check_original_readbacks((root / 'Readback.log').read_text(), expected)


class AuditContinuationExecutorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location("audit_continuation_under_test", SCRIPT)
        cls.r = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.r)

    def setUp(self):
        self.assertTrue(hasattr(self.r, "_execute_audit_continuation"), "Continuation executor is absent")
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.source = self.base / 'source'; self.source.mkdir()
        self.prior = self.base / 'prior'; self.prior.mkdir()

    def test_fresh_output_must_be_disjoint_from_every_consumed_input(self):
        good = self.base / 'new'
        self.assertEqual(self.r._ac_exec_output(good, [self.source, self.prior], self.r), good)
        self.assertFalse(good.exists())
        for bad in [self.source, self.prior, self.source / 'generated', self.prior / 'audit', self.base]:
            with self.subTest(path=bad), self.assertRaises(ValueError):
                self.r._ac_exec_output(bad, [self.source, self.prior], self.r)
        alias = self.base / 'alias'; alias.symlink_to(self.prior, target_is_directory=True)
        with self.assertRaises(ValueError): self.r._ac_exec_output(alias / 'new', [self.source, self.prior], self.r)

    def test_inventory_binds_every_retained_file_and_refuses_symlink_alias(self):
        (self.prior / 'a').write_bytes(b'first')
        (self.prior / 'sub').mkdir(); (self.prior / 'sub/b').write_bytes(b'second')
        rows, digest = self.r._ac_exec_inventory(self.prior, self.r)
        self.assertEqual(rows, {'a': self.r.sha(b'first'), 'sub/b': self.r.sha(b'second')})
        self.assertEqual(digest, self.r._file_hashes(self.prior))
        (self.prior / 'sub/b').write_bytes(b'changed')
        self.assertNotEqual(self.r._ac_exec_inventory(self.prior, self.r)[1], digest)
        (self.prior / 'alias').symlink_to(self.prior / 'a')
        with self.assertRaises(ValueError): self.r._ac_exec_inventory(self.prior, self.r)

    def test_custom_objects_require_exact_original_producer_census_and_bytes(self):
        path = self.prior / 'original/runtime/build/A.olean'; path.parent.mkdir(parents=True); path.write_bytes(b'fresh-original')
        relative = path.relative_to(self.prior).as_posix()
        expected = {relative: self.r.sha(path.read_bytes())}
        self.assertEqual(self.r._ac_exec_objects(self.prior, expected, ['original/runtime/build'], self.r), expected)
        extra = path.with_name('foreign.olean'); extra.write_bytes(b'not-produced')
        with self.assertRaises(ValueError): self.r._ac_exec_objects(self.prior, expected, ['original/runtime/build'], self.r)
        extra.unlink(); path.write_bytes(b'stale-object')
        with self.assertRaises(ValueError): self.r._ac_exec_objects(self.prior, expected, ['original/runtime/build'], self.r)

    def test_absent_unimported_cli_cache_is_not_fabricated_or_generalized(self):
        lean = self.base / 'lean'; lean.mkdir(); (lean / 'Init.olean').write_bytes(b'official fixture')
        cli = self.base / 'Cli-absent'
        plan = {'packages': {'Cli': {}}, 'official': {}}
        rows, inventories = self.r._ac_exec_caches({'lean': lean, 'Cli': cli}, plan, self.r)
        by_name = {row['root_id']: row for row in rows}
        self.assertEqual(by_name['Cli']['file_count'], 0)
        self.assertEqual(by_name['Cli']['tree_before_sha256'], self.r.canonical({}))
        self.assertNotEqual(by_name['Cli']['cache_policy'], by_name['lean']['cache_policy'])
        self.assertEqual(inventories['Cli'], {})
        self.assertFalse(cli.exists())
        plan['official'] = {'Cli': {'package': 'Cli'}}
        with self.assertRaises(ValueError): self.r._ac_exec_caches({'lean': lean, 'Cli': cli}, plan, self.r)
        plan = {'packages': {'Batteries': {}}, 'official': {}}
        with self.assertRaises(ValueError): self.r._ac_exec_caches({'lean': lean, 'Batteries': cli}, plan, self.r)

    def test_generated_auditor_is_fixed_and_written_only_once(self):
        out = self.base / 'new'; out.mkdir()
        plan = {'targets': {'a': {'name': 'Fixture.ok', 'module': 'Fixture', 'target_id': 'a'}}}
        expected = self.r.sha(self.r._audit_source(list(plan['targets'].values())).encode())
        with mock.patch.object(self.r, 'AC_AUDIT_SOURCE', expected, create=True):
            target = self.r._ac_exec_generate(out, plan, self.r)
            self.assertEqual(self.r.sha(target.read_bytes()), expected)
            with self.assertRaises(ValueError): self.r._ac_exec_generate(out, plan, self.r)
        other = self.base / 'other'; other.mkdir()
        with mock.patch.object(self.r, 'AC_AUDIT_SOURCE', '0' * 64, create=True):
            with self.assertRaises(ValueError): self.r._ac_exec_generate(other, plan, self.r)
        self.assertFalse((other / 'generated').exists())

    def test_resource_or_parser_failure_cannot_become_complete_audit(self):
        target = {'target_id': 'a', 'module': 'Fixture', 'name': 'Fixture.ok'}
        good = "V5_BEGIN Fixture.ok\nFixture.ok : True\n'Fixture.ok' does not depend on any axioms\nV5_OWNER Fixture.ok Fixture\nV5_SAFE Fixture.ok 1 []\nV5_END Fixture.ok\n"
        for terminal, code, outcome in [('TIMEOUT', None, 'RESOURCE_INCONCLUSIVE'), ('INTERRUPTED', None, 'RESOURCE_INCONCLUSIVE'), ('COMPLETED', 1, 'FAILED')]:
            observed, audits = self.r._ac_exec_result({'terminal': terminal, 'exit_code': code}, good, [target], self.r)
            self.assertEqual((observed, audits), (outcome, {}))
        outcome, audits = self.r._ac_exec_result({'terminal': 'COMPLETED', 'exit_code': 0}, good, [target], self.r)
        self.assertEqual(outcome, 'QUALIFIED_DECLARED_SUITE'); self.assertEqual(set(audits), {'a'})
        for run, text in [({'terminal': 'COMPLETED', 'exit_code': 0}, ''), ({'terminal': 'COMPLETED', 'exit_code': 124}, good), ({'terminal': 'TIMEOUT', 'exit_code': 1}, good)]:
            with self.assertRaises(ValueError): self.r._ac_exec_result(run, text, [target], self.r)

    def execution_fixture(self):
        a = types.SimpleNamespace(**vars(self.r))
        a.AC_PRIOR = {'receipt_sha256': '', 'receipt_canonical_sha256': '', 'receipt_bytes': 0,
                      'failed_audit_source_sha256': self.r.sha(b'old audit'), 'failed_audit_log_sha256': self.r.sha(b'old log'),
                      'failure_record_sha256': self.r.sha(b'old failure'), 'original_result_sha256': self.r.sha(b'old result'),
                      'physical_trace_sha256': 'a' * 64}
        a.AC_ACCOUNTING = {'new_source_owned_physical_runs': 0, 'new_child_compilations': 0,
                          'new_custom_objects': 0, 'new_target_audit_processes': 1, 'independent_evidence_increment': 0}
        a.AC_SCHEMA = 'test-continuation'; a.AC_CACHE_POLICY = 'test-retained-cache-policy'
        suite = {'id': 'd06-core-runtime', 'source_ids': ['source'], 'review_ids': ['review'], 'targets': [
            {'id': 'a', 'source_id': 'source', 'target_sha256': 'b' * 64}],
            'replay': {'build_roots': ['original/build'], 'external_inputs': [{'expected_sha256': 'c' * 64}]}}
        body = b'namespace Fixture\ntheorem ok : True := True.intro\nend Fixture\n'
        plan = {'targets': {'a': {'target_id': 'a', 'module': 'Fixture', 'name': 'Fixture.ok'}},
                'files': {'source': {'path': 'Fixture.lean'}}, 'contents': {'source': body}, 'packages': {}, 'official': {}}
        a.AC_AUDIT_SOURCE = self.r.sha(self.r._audit_source(list(plan['targets'].values())).encode())
        project = self.prior / 'project'; project.mkdir(); (project / 'Fixture.lean').write_bytes(body)
        artifact = self.prior / 'original/build/Fixture.olean'; artifact.parent.mkdir(parents=True); artifact.write_bytes(b'producer object')
        objects = {'original/build/Fixture.olean': self.r.sha(artifact.read_bytes())}
        for path, data in [('generated/V5SuccessorReadback.lean', b'old audit'), ('logs/target-audit.log', b'old log'),
                           ('FAILURE.json', b'old failure'), ('original/RESULT.json', b'old result')]:
            p = self.prior / path; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(data)
        evidence = {'descriptor_sha256': self.r.canonical(suite['replay']), 'closure_sha256': 'e' * 64, 'source_hashes_before': {'source': self.r.sha(body)},
                    'source_hashes_after': {'source': self.r.sha(body)}, 'import_fingerprints': {},
                    'tool_fingerprints': {'lean': {'executable_sha256': 'f' * 64}}, 'dependency_checks': {},
                    'child_observations': [], 'driver_invocations': []}
        prior = {'id': 'old', 'suite_id': 'fixture', 'family': 'fixture', 'suite_sha256': '1' * 64,
                 'source_hashes': {'source': self.r.sha(body)}, 'review_hashes': {'review': '2' * 64}, 'toolchain_sha256': '3' * 64,
                 'outcome': 'FAILED', 'proof_scope': 'NONE', 'exit_code': 1, 'controls': [], 'replay_evidence': evidence,
                 'ended_at': '2020-01-01T00:00:00Z'}
        encoded = json.dumps(prior).encode(); (self.prior / 'RECEIPT.json').write_bytes(encoded)
        a.AC_PRIOR.update(receipt_sha256=self.r.sha(encoded), receipt_canonical_sha256=self.r.canonical(prior), receipt_bytes=len(encoded))
        a.AC_RETAINED_TREE = self.r._ac_exec_inventory(self.prior, self.r)[1]
        a.AC_SUITE_SHA256 = self.r.canonical(suite); a.AC_APPROVAL = 'a' * 64
        a.APPROVED_DECLARED_SUITES = {'d06-core-runtime': a.AC_APPROVAL}
        a.AC_PROJECT_TREE = self.r._ac_exec_inventory(project, self.r)[1]
        a.AC_PRIOR_KEYS = {'receipt_sha256', 'receipt_canonical_sha256', 'receipt_bytes', 'receipt', 'failed_audit_source_sha256', 'failed_audit_log_sha256', 'failure_record_sha256'}
        a.validate_suite = mock.Mock(return_value=plan)
        a.public_bytes = mock.Mock(return_value=body)
        a._ac_eligible_prior = mock.Mock(return_value=(prior, evidence, {'_prerequisites': {}, 'original-driver': {}, '_target_audit': {}}, objects))
        a.validate_audit_continuation = mock.Mock(return_value={'outcome': 'QUALIFIED_DECLARED_SUITE'})
        a.import_fingerprints = mock.Mock(return_value={})
        a.closure_fingerprint = mock.Mock(return_value='e' * 64)
        tool = self.base / 'tool/bin/lean'; tool.parent.mkdir(parents=True); tool.write_bytes(b'exact executable')
        cache = tool.parent.parent / 'lib/lean'; cache.mkdir(parents=True); (cache / 'Init.olean').write_bytes(b'official fixture')
        fingerprints = {'lean': {'executable_sha256': self.r.sha(tool.read_bytes())}}
        evidence['tool_fingerprints'] = fingerprints
        # Seal fixture after its actual declared tool fingerprint is known.
        encoded = json.dumps(prior).encode(); (self.prior / 'RECEIPT.json').write_bytes(encoded)
        a.AC_PRIOR.update(receipt_sha256=self.r.sha(encoded), receipt_canonical_sha256=self.r.canonical(prior), receipt_bytes=len(encoded))
        a.AC_RETAINED_TREE = self.r._ac_exec_inventory(self.prior, self.r)[1]
        a._verify_environment = mock.Mock(return_value=({'lean': tool}, fingerprints, {}, {'LEAN_PATH': str(cache)}, {}))
        a.run_process = mock.Mock()
        def audit(argv, cwd, env, log, timeout):
            self.assertEqual(argv, [tool, '-j1', self.base / 'new/generated/V5SuccessorReadback.lean'])
            self.assertEqual(cwd, project); self.assertEqual(timeout, 300)
            self.assertEqual(env['LEAN_PATH'].split(os.pathsep), [str(self.prior / 'original/build'), str(cache)])
            text = "V5_BEGIN Fixture.ok\nFixture.ok : True\n'Fixture.ok' does not depend on any axioms\nV5_OWNER Fixture.ok Fixture\nV5_SAFE Fixture.ok 1 []\nV5_END Fixture.ok\n"
            Path(log).write_text(text)
            return {'terminal': 'COMPLETED', 'exit_code': 0, 'started_at': self.r.utc(), 'ended_at': self.r.utc(), 'log_sha256': self.r.sha(text.encode())}
        a.run_process.side_effect = audit
        return a, suite, plan, {'source': {'public_sha256': self.r.sha(body)}}, {'review': {'review_sha256': '2' * 64}}, artifact

    def execute_fixture(self, data):
        a, suite, plan, sources, reviews, _ = data
        self.assertTrue(hasattr(self.r, '_execute_audit_continuation'), 'Full audit-only executor is absent')
        return self.r._execute_audit_continuation(suite, sources, self.source, self.prior, self.base / 'new', {}, {}, reviews=reviews, adapter=a)

    def test_full_executor_runs_only_the_missing_audit_and_preserves_prior(self):
        data = self.execution_fixture(); a = data[0]
        before = self.r._ac_exec_inventory(self.prior, self.r)
        receipt = self.execute_fixture(data)
        self.assertEqual(receipt['outcome'], 'QUALIFIED_DECLARED_SUITE')
        self.assertEqual(a.run_process.call_count, 1)
        self.assertEqual(a._verify_environment.call_count, 2)
        self.assertEqual(self.r._ac_exec_inventory(self.prior, self.r), before)
        self.assertEqual(receipt['replay_evidence']['prior']['receipt']['outcome'], 'FAILED')
        self.assertEqual([row['id'] for row in receipt['stages']], ['_prerequisites', '_target_audit'])
        self.assertEqual(receipt['replay_evidence']['accounting']['new_child_compilations'], 0)
        self.assertEqual(set(receipt['replay_evidence']['output_hashes']), {'generated/V5SuccessorReadback.lean'})
        self.assertTrue((self.base / 'new/RECEIPT.json').is_file())
        self.assertFalse((self.base / 'new/project').exists())

    def test_stale_retained_input_refuses_before_any_audit(self):
        data = self.execution_fixture(); data[-1].write_bytes(b'changed before invocation')
        with self.assertRaises(ValueError): self.execute_fixture(data)
        data[0].run_process.assert_not_called()
        self.assertFalse((self.base / 'new/RECEIPT.json').exists())

    def test_foreign_suite_and_reused_output_cannot_start_an_audit(self):
        data = self.execution_fixture(); data[1]['id'] = 'foreign'
        with self.assertRaises(ValueError): self.execute_fixture(data)
        data[0].run_process.assert_not_called()
        self.assertFalse((self.base / 'new').exists())
        data[1]['id'] = 'd06-core-runtime'; (self.base / 'new').mkdir()
        with self.assertRaises(ValueError): self.execute_fixture(data)
        data[0].run_process.assert_not_called()

    def test_absent_prior_is_a_missing_prerequisite(self):
        a, suite, _, sources, reviews, _ = self.execution_fixture()
        with self.assertRaises(self.r.MissingInput):
            self.r._execute_audit_continuation(suite, sources, self.source, self.base / 'absent-prior', self.base / 'new',
                                              {}, {}, reviews=reviews, adapter=a)
        a.run_process.assert_not_called()
        self.assertFalse((self.base / 'new').exists())

    def test_post_audit_retained_change_cannot_be_saved_as_success(self):
        data = self.execution_fixture(); original = data[0].run_process.side_effect
        def changed(*args):
            result = original(*args); data[-1].write_bytes(b'changed during audit'); return result
        data[0].run_process.side_effect = changed
        with self.assertRaises(ValueError): self.execute_fixture(data)
        self.assertEqual(data[0].run_process.call_count, 1)
        self.assertFalse((self.base / 'new/RECEIPT.json').exists())
        refusal = self.r.read_json(self.base / 'new/REFUSAL.json')
        self.assertEqual(refusal['audit_process']['exit_code'], 0)
        self.assertEqual(refusal['status'], 'CONTINUATION_REFUSED')

    def test_post_audit_cache_change_or_prerequisite_refusal_has_no_receipt(self):
        data = self.execution_fixture(); original = data[0].run_process.side_effect
        def changed(*args):
            result = original(*args)
            (self.base / 'tool/lib/lean/Init.olean').write_bytes(b'changed official object')
            return result
        data[0].run_process.side_effect = changed
        with self.assertRaises(ValueError): self.execute_fixture(data)
        self.assertFalse((self.base / 'new/RECEIPT.json').exists())
        self.assertEqual(self.r.read_json(self.base / 'new/REFUSAL.json')['audit_process']['exit_code'], 0)

    def test_continuation_runner_cannot_change_after_process_start(self):
        data = self.execution_fixture(); a = data[0]
        runner = self.base / 'frozen-runner.py'; runner.write_bytes(b'synthetic reviewed runner')
        a.__file__ = str(runner); original = a.run_process.side_effect
        def changed(*args):
            result = original(*args); runner.write_bytes(b'changed while audit ran'); return result
        a.run_process.side_effect = changed
        with self.assertRaises(ValueError): self.execute_fixture(data)
        self.assertFalse((self.base / 'new/RECEIPT.json').exists())
        self.assertEqual(self.r.read_json(self.base / 'new/REFUSAL.json')['audit_process']['exit_code'], 0)

    def test_changed_tool_readback_refuses_before_audit(self):
        data = self.execution_fixture(); value = list(data[0]._verify_environment.return_value)
        value[1] = {'lean': {'executable_sha256': 'f' * 64}}
        data[0]._verify_environment.return_value = tuple(value)
        with self.assertRaises(ValueError): self.execute_fixture(data)
        data[0].run_process.assert_not_called()
        self.assertIsNone(self.r.read_json(self.base / 'new/REFUSAL.json')['audit_process'])
        self.assertFalse((self.base / 'new/RECEIPT.json').exists())

    @unittest.skipUnless(os.environ.get('V5_REPLAY_TEST_LEAN'), 'Explicit official Lean test binding required')
    def test_official_lean_continuation_reads_retained_object_without_recompilation(self):
        data = self.execution_fixture(); a, _, _, _, _, artifact = data
        lean = Path(os.environ['V5_REPLAY_TEST_LEAN'])
        self.assertEqual(self.r.sha(lean.read_bytes()), LEAN_SHA)
        env = dict(os.environ); env['LEAN_PATH'] = str(lean.parent.parent / 'lib/lean')
        build = self.r.run_process([lean, '-j1', '-o', artifact, self.prior / 'project/Fixture.lean'],
                              self.prior / 'project', env, self.base / 'fixture-compile.log', 60)
        self.assertEqual((build['terminal'], build['exit_code']), ('COMPLETED', 0))
        a._ac_eligible_prior.return_value[-1]['original/build/Fixture.olean'] = self.r.sha(artifact.read_bytes())
        prior = a._ac_eligible_prior.return_value[0]
        fingerprints = {'lean': {'executable_sha256': self.r.sha(lean.read_bytes())}}
        prior['replay_evidence']['tool_fingerprints'] = fingerprints
        encoded = json.dumps(prior).encode(); (self.prior / 'RECEIPT.json').write_bytes(encoded)
        a.AC_PRIOR.update(receipt_sha256=self.r.sha(encoded), receipt_canonical_sha256=self.r.canonical(prior), receipt_bytes=len(encoded))
        a.AC_RETAINED_TREE = self.r._ac_exec_inventory(self.prior, self.r)[1]
        before = self.r._ac_exec_inventory(self.prior, self.r)
        a._verify_environment.return_value = ({'lean': lean}, fingerprints, {}, env, {})
        a.run_process.side_effect = self.r.run_process
        result = self.execute_fixture(data)
        self.assertEqual(result['outcome'], 'QUALIFIED_DECLARED_SUITE')
        self.assertEqual(a.run_process.call_count, 1)
        self.assertEqual(self.r._ac_exec_inventory(self.prior, self.r), before)
        self.assertGreater(result['replay_evidence']['target_audits'][0]['checked_declarations'], 0)

    def test_zero_exit_with_unparseable_audit_keeps_actual_zero_in_refusal(self):
        data = self.execution_fixture(); original = data[0].run_process.side_effect
        def wrong(*args):
            result = original(*args); Path(args[3]).write_bytes(b'unrelated output\n')
            result['log_sha256'] = self.r.sha(Path(args[3]).read_bytes()); return result
        data[0].run_process.side_effect = wrong
        with self.assertRaises(ValueError): self.execute_fixture(data)
        self.assertFalse((self.base / 'new/RECEIPT.json').exists())
        self.assertEqual(self.r.read_json(self.base / 'new/REFUSAL.json')['audit_process']['exit_code'], 0)

    def test_completed_audit_failure_and_resource_terminal_do_not_gain_targets(self):
        for terminal, code, outcome in [('COMPLETED', 1, 'FAILED'), ('TIMEOUT', None, 'RESOURCE_INCONCLUSIVE')]:
            with self.subTest(terminal=terminal), tempfile.TemporaryDirectory() as directory:
                previous_base, previous_prior, previous_source = self.base, self.prior, self.source
                self.base = Path(directory); self.prior = self.base / 'prior'; self.prior.mkdir(); self.source = self.base / 'source'; self.source.mkdir()
                try:
                    data = self.execution_fixture(); original = data[0].run_process.side_effect
                    def failure(*args):
                        result = original(*args); result.update(terminal=terminal, exit_code=code); return result
                    data[0].run_process.side_effect = failure
                    receipt = self.execute_fixture(data)
                    self.assertEqual(receipt['outcome'], outcome); self.assertEqual(receipt['proof_scope'], 'NONE')
                    self.assertEqual(receipt['target_readbacks'], []); self.assertEqual(receipt['replay_evidence']['target_audits'], [])
                finally:
                    self.base, self.prior, self.source = previous_base, previous_prior, previous_source

    def test_receipt_dispatch_uses_only_the_explicit_continuation_schema(self):
        marker = {'status': 'synthetic dispatch fixture'}
        with mock.patch.object(self.r, 'validate_audit_continuation', return_value=marker) as validation:
            self.assertEqual(self.r.validate_receipt({'replay_evidence': {'schema': self.r.AC_SCHEMA}}, {}, {}, self.base), marker)
        self.assertEqual(validation.call_count, 1)
        self.assertEqual(validation.call_args.kwargs['adapter'].__file__, self.r.__file__)


class AuditContinuationValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('continuation_validation_under_test', SCRIPT)
        cls.r = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.r)

    def test_actual_prior_anchor_and_canonical_value_are_not_caller_resealable(self):
        r = self.r
        binding = {key: {} if key == 'receipt' else r.AC_PRIOR[key] for key in r.AC_PRIOR_KEYS}
        binding['receipt_sha256'] = 'f' * 64
        with self.assertRaisesRegex(ValueError, 'Changed prior trust anchor'):
            r._ac_eligible_prior({'prior': binding}, {}, {}, Path('.'), r, {})
        binding['receipt_sha256'] = r.AC_PRIOR['receipt_sha256']
        binding['receipt'] = {key: None for key in r.AC_RECEIPT_KEYS}
        with self.assertRaisesRegex(ValueError, 'Substituted original receipt'):
            r._ac_eligible_prior({'prior': binding}, {}, {}, Path('.'), r, {})

    def test_pure_eligibility_rejects_missing_ledger_after_ordinary_receipt_validation(self):
        r = self.r
        prior = {key: None for key in r.AC_RECEIPT_KEYS}
        prior.update(outcome='FAILED', proof_scope='NONE', exit_code=1,
                     replay_evidence={'schema': 'orthemology-v5-replay-evidence-v2',
                                      'runner_sha256': r.AC_PRIOR['runner_sha256'], 'stage_results': []})
        anchor = {**r.AC_PRIOR, 'receipt_canonical_sha256': r.canonical(prior)}
        binding = {key: prior if key == 'receipt' else anchor[key] for key in r.AC_PRIOR_KEYS}
        adapter = types.SimpleNamespace(**vars(r)); adapter.validate_receipt = mock.Mock()
        with mock.patch.object(r, 'AC_PRIOR', anchor), self.assertRaisesRegex(ValueError, 'Incomplete original stage set/order'):
            r._ac_eligible_prior({'prior': binding}, {}, {}, Path('.'), adapter, {'stages': {}})
        adapter.validate_receipt.assert_called_once_with(prior, {}, {}, Path('.'))

    def test_pure_continuation_validator_rejects_runner_accounting_auditor_and_policy_changes(self):
        r = self.r
        # Isolate the new envelope gates from delegated ordinary source checks
        # and filesystem collection. Those are tested by the executor fixtures.
        suite = {'id': 'd06-core-runtime'}; plan = {'targets': {}}
        adapter = types.SimpleNamespace(**vars(r)); adapter.validate_suite = mock.Mock(return_value=plan)
        adapter.APPROVED_DECLARED_SUITES = {suite['id']: r.AC_APPROVAL}
        generated = r.sha(r._audit_source([]).encode())
        prior = {key: {} for key in ('suite_id', 'family', 'suite_sha256', 'source_hashes', 'review_hashes', 'toolchain_sha256')}
        prior.update(id='original-failed', controls=[])
        old = {key: {} for key in ('descriptor_sha256', 'closure_sha256', 'source_hashes_before', 'source_hashes_after',
                                   'import_fingerprints', 'tool_fingerprints', 'dependency_checks')}
        record = {key: None for key in r.AC_RECEIPT_KEYS}
        record.update({key: prior[key] for key in ('suite_id', 'family', 'suite_sha256', 'source_hashes', 'review_hashes', 'toolchain_sha256')})
        record.update(id='d06-core-runtime-audit-continuation-SYNTHETIC', controls=[], outcome='FAILED', proof_scope='NONE', exit_code=1,
                      target_readbacks=[], axioms=[], invocation=['replay_v5_successors.py', '--audit-continuation', '--suite', suite['id'], '--prior', '{prior}', '--out', '{out}'])
        evidence = {key: None for key in r.AC_EVIDENCE_KEYS}; evidence.update(old)
        evidence.update(schema=r.AC_SCHEMA, cache_policy=r.AC_CACHE_POLICY, runner_sha256=r.sha(SCRIPT.read_bytes()),
                        accounting=dict(r.AC_ACCOUNTING), output_hashes={'generated/V5SuccessorReadback.lean': generated}, target_audits=[],
                        fresh_audit={'recipe': 'checked-closure-deduplicated-enqueue-v1', 'generated_source_sha256': generated,
                            'resolved_invocation_sha256': 'd' * 64, 'argv_provenance': 'RESOLVED_FROM_BOUND_INPUTS', 'traversal_bound': 1000000,
                            'distinct_declaration_accounting': 'ENQUEUE_ONCE_NO_DEPENDENCY_DROPPED', 'fresh_custom_objects': 0})
        record['replay_evidence'] = evidence
        with mock.patch.object(r, 'AC_SUITE_SHA256', r.canonical(suite)), mock.patch.object(r, 'AC_AUDIT_SOURCE', generated), \
             mock.patch.object(r, '_ac_eligible_prior', return_value=(prior, old, {}, {})), \
             mock.patch.object(r, '_ac_retained_inputs'), mock.patch.object(r, '_ac_fresh_stages', return_value={'terminal': 'COMPLETED', 'exit_code': 1}):
            self.assertEqual(r.validate_audit_continuation(record, suite, {}, Path('.'), adapter=adapter)['outcome'], 'FAILED')
            # This consumed executor may remain valid when unrelated recipes
            # change the current adapter; the exact auditor/scope gates remain.
            record['replay_evidence']['runner_sha256'] = '37f79cecd8cc76604c37a0d48288898abd22bd2fccdc0353f753ac31bdc34e89'
            self.assertEqual(r.validate_audit_continuation(record, suite, {}, Path('.'), adapter=adapter)['outcome'], 'FAILED')
            for change, message in [({'runner_sha256': 'f' * 64}, 'Wrong executing continuation runner'),
                                    ({'runner_sha256': r.AC_PRIOR['runner_sha256']}, 'Wrong executing continuation runner'),
                                    ({'cache_policy': 'CALLER_TRUSTED_CACHE'}, 'Unknown continuation schema/policy'),
                                    ({'accounting': {**r.AC_ACCOUNTING, 'new_custom_objects': 1}}, 'Duplicate or invented execution/build credit'),
                                    ({'accounting': {**r.AC_ACCOUNTING, 'new_custom_objects': False}}, 'Duplicate or invented execution/build credit'),
                                    ({'fresh_audit': {**evidence['fresh_audit'], 'generated_source_sha256': 'f' * 64}}, 'Changed auditor recipe/bound')]:
                with self.subTest(change=change), self.assertRaisesRegex(ValueError, message):
                    altered = copy.deepcopy(record); altered['replay_evidence'].update(change)
                    r.validate_audit_continuation(altered, suite, {}, Path('.'), adapter=adapter)


if __name__ == '__main__':
    unittest.main(verbosity=2)
