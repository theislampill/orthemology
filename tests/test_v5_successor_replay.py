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



def copy_replay_scripts(destination):
    """Packaging fixtures include the complete eagerly loaded adapter closure."""
    import shutil
    shutil.copytree(SCRIPT.parent, destination, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))


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


class HistoryContinuationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('history_continuation_under_test', SCRIPT)
        cls.r = importlib.util.module_from_spec(spec); spec.loader.exec_module(cls.r)

    def setUp(self):
        self.assertTrue(hasattr(self.r, '_execute_history_audit_continuation'), 'History audit-only executor is absent')
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.source = self.base / 'source'; self.source.mkdir()
        self.prior = self.base / 'prior'; self.prior.mkdir()

    def execution_fixture(self):
        data = AuditContinuationExecutorTests.execution_fixture(self)
        a, suite, plan, sources, reviews, artifact = data
        prior = a._ac_eligible_prior.return_value[0]; old = prior['replay_evidence']
        suite['id'] = a.HC_SUITE
        suite['controls'] = [{'id': 'observed-positive', 'source_id': 'source', 'target_id': 'a', 'role': 'POSITIVE',
                              'expected_outcome': 'ACCEPT', 'expected_outcome_sha256': self.r.sha(b'ACCEPT')}]
        plan['stages'] = {'original-driver': {'id': 'original-driver'}, 'observe-positive': {
            'id': 'observe-positive', 'control_ids': ['observed-positive']}}
        prior.update(suite_id=suite['id'], controls=[])
        old.update(driver_invocations=[{'parent_stage_id': 'original-driver', 'runner_sha256': '0' * 64}],
                   stage_results=[{'id': '_prerequisites'}, {'id': 'original-driver'}])
        audit = {'scope': 'SYNTHETIC SOURCE/LOG ASSOCIATION', 'names': ['Fixture.ok']}
        collection = {'parser_id': 'fixture', 'parser_revision': 'fixture', 'collector_runner_sha256': self.r.sha(Path(a.__file__).read_bytes()),
            'observed_at': self.r.utc(), 'driver_invocations': old['driver_invocations'], 'child_observations': [],
            'stage_results': [{'id': 'observe-positive', 'terminal': 'COMPLETED', 'exit_code': 0, 'log_sha256': 'a' * 64}],
            'control_diagnostics': [], 'output_hashes': {'original/build/Fixture.olean': self.r.sha(artifact.read_bytes())},
            'source_audit_sha256': self.r.canonical(audit)}
        a.HC_OBJECTS = dict(collection['output_hashes'])
        a.HC_SOURCE_AUDIT_SHA256 = self.r.canonical(audit)
        a.HC_COLLECTION_SHA256 = self.r._hc_collection_digest(collection, a)
        a.HC_SUITE_SHA256 = self.r.canonical(suite)
        a.HC_APPROVAL = 'a' * 64; a.APPROVED_DECLARED_SUITES = {suite['id']: a.HC_APPROVAL}
        a.HC_AUDIT_SOURCE = a.AC_AUDIT_SOURCE
        a.HC_PROJECT_TREE = a.AC_PROJECT_TREE
        original = json.dumps({'status': 'SYNTHETIC PRODUCER RESULT'}).encode()
        (self.prior / 'original/REPLAY_RECEIPT.json').write_bytes(original)
        encoded = json.dumps(prior).encode(); (self.prior / 'RECEIPT.json').write_bytes(encoded)
        a.HC_PRIOR = {'receipt_sha256': self.r.sha(encoded), 'receipt_canonical_sha256': self.r.canonical(prior),
                     'receipt_bytes': len(encoded), 'failure_record_sha256': self.r.sha(b'old failure'),
                     'original_receipt_sha256': self.r.sha(original), 'original_receipt_canonical_sha256': self.r.canonical(json.loads(original)),
                     'original_receipt_bytes': len(original)}
        a.HC_RETAINED_TREE = self.r._ac_exec_inventory(self.prior, a)[1]
        a._hc_prior = mock.Mock(return_value=(prior, old, {row['id']: row for row in old['stage_results']}))
        a._hc_exec_collection = mock.Mock(return_value=(collection, audit))
        a.validate_history_continuation = mock.Mock(return_value={'outcome': 'QUALIFIED_DECLARED_SUITE'})
        return data

    def execute_fixture(self, data):
        a, suite, _, sources, reviews, _ = data
        return self.r._execute_history_audit_continuation(suite, sources, self.source, self.prior,
            self.base / 'new', {}, {}, reviews=reviews, adapter=a)

    def test_history_continuation_collects_old_children_and_runs_only_missing_audit(self):
        data = self.execution_fixture(); a = data[0]
        before = self.r._ac_exec_inventory(self.prior, a)
        receipt = self.execute_fixture(data)
        self.assertEqual(receipt['outcome'], 'QUALIFIED_DECLARED_SUITE')
        self.assertEqual(a.run_process.call_count, 1)
        self.assertEqual(a._verify_environment.call_count, 2)
        self.assertEqual(a._hc_exec_collection.call_count, 1)
        self.assertEqual(self.r._ac_exec_inventory(self.prior, a), before)
        self.assertEqual([row['id'] for row in receipt['stages']], ['_prerequisites', '_target_audit'])
        self.assertEqual(receipt['replay_evidence']['prior']['receipt']['outcome'], 'FAILED')
        self.assertEqual(receipt['controls'][0]['exit_code'], 0)
        self.assertEqual(receipt['replay_evidence']['accounting']['new_child_compilations'], 0)
        self.assertFalse((self.base / 'new/project').exists())

    def test_history_continuation_changed_retained_object_stops_before_audit(self):
        data = self.execution_fixture(); data[-1].write_bytes(b'changed object')
        with self.assertRaises(ValueError): self.execute_fixture(data)
        data[0].run_process.assert_not_called()
        self.assertFalse((self.base / 'new/RECEIPT.json').exists())

    def test_history_continuation_collection_and_source_audit_are_independently_pinned(self):
        data = self.execution_fixture(); a = data[0]
        collection, audit = a._hc_exec_collection.return_value
        collection['output_hashes']['original/build/Fixture.olean'] = 'f' * 64
        with self.assertRaises(ValueError): self.execute_fixture(data)
        a.run_process.assert_not_called()
        self.assertIsNone(self.r.read_json(self.base / 'new/REFUSAL.json')['audit_process'])

    def test_history_continuation_rejects_changed_source_audit_even_when_collection_is_resealed(self):
        data = self.execution_fixture(); a = data[0]
        collection, audit = a._hc_exec_collection.return_value
        audit['names'] = ['Foreign.name']
        collection['source_audit_sha256'] = self.r.canonical(audit)
        a.HC_COLLECTION_SHA256 = self.r._hc_collection_digest(collection, a)
        with self.assertRaises(ValueError): self.execute_fixture(data)
        a.run_process.assert_not_called()

    def test_history_continuation_changed_tool_binding_stops_before_collection(self):
        data = self.execution_fixture(); a = data[0]
        values = list(a._verify_environment.return_value); values[1] = {'lean': {'executable_sha256': 'f' * 64}}
        a._verify_environment.return_value = tuple(values)
        with self.assertRaises(ValueError): self.execute_fixture(data)
        a._hc_exec_collection.assert_not_called(); a.run_process.assert_not_called()

    def test_history_continuation_post_audit_changes_preserve_actual_zero_as_refusal(self):
        data = self.execution_fixture(); original = data[0].run_process.side_effect
        def changed(*args):
            run = original(*args); data[-1].write_bytes(b'changed after audit'); return run
        data[0].run_process.side_effect = changed
        with self.assertRaises(ValueError): self.execute_fixture(data)
        self.assertEqual(self.r.read_json(self.base / 'new/REFUSAL.json')['audit_process']['exit_code'], 0)
        self.assertFalse((self.base / 'new/RECEIPT.json').exists())

    def test_history_continuation_resource_keeps_retained_controls_without_new_target_credit(self):
        data = self.execution_fixture(); original = data[0].run_process.side_effect
        def timeout(*args):
            return {**original(*args), 'terminal': 'TIMEOUT', 'exit_code': None}
        data[0].run_process.side_effect = timeout
        receipt = self.execute_fixture(data)
        self.assertEqual((receipt['outcome'], receipt['proof_scope']), ('RESOURCE_INCONCLUSIVE', 'NONE'))
        self.assertEqual(receipt['target_readbacks'], [])
        self.assertEqual(receipt['replay_evidence']['target_audits'], [])
        self.assertEqual(receipt['controls'][0]['actual_outcome'], 'ACCEPT')
        self.assertIsNone(receipt['stages'][-1]['exit_code'])

    def test_history_continuation_parser_error_does_not_invent_a_process_failure(self):
        data = self.execution_fixture()
        def malformed(argv, cwd, env, log, timeout):
            Path(log).write_bytes(b'no target readback')
            return {'terminal': 'COMPLETED', 'exit_code': 0, 'started_at': self.r.utc(), 'ended_at': self.r.utc(),
                    'log_sha256': self.r.sha(Path(log).read_bytes())}
        data[0].run_process.side_effect = malformed
        with self.assertRaises(ValueError): self.execute_fixture(data)
        self.assertEqual(self.r.read_json(self.base / 'new/REFUSAL.json')['audit_process']['exit_code'], 0)
        self.assertFalse((self.base / 'new/RECEIPT.json').exists())

    def test_history_continuation_collection_digest_excludes_only_new_parser_attribution(self):
        data = self.execution_fixture(); collection = data[0]._hc_exec_collection.return_value[0]
        original = self.r._hc_collection_digest(collection, self.r)
        changed = copy.deepcopy(collection); changed['collector_runner_sha256'] = 'f' * 64
        changed['observed_at'] = '2030-01-01T00:00:00Z'
        self.assertEqual(self.r._hc_collection_digest(changed, self.r), original)
        changed['driver_invocations'][0]['runner_sha256'] = 'e' * 64
        self.assertNotEqual(self.r._hc_collection_digest(changed, self.r), original)

    def test_history_continuation_prior_bytes_canonical_and_failure_anchors_are_not_resealable(self):
        data = self.execution_fixture(); a = data[0]
        self.r._hc_exec_prior(self.prior, a)
        path = self.prior / 'RECEIPT.json'; original = path.read_bytes()
        path.write_bytes(original + b'\n')
        with self.assertRaises(ValueError): self.r._hc_exec_prior(self.prior, a)
        a.HC_PRIOR['receipt_bytes'] += 1; a.HC_PRIOR['receipt_sha256'] = self.r.sha(path.read_bytes())
        (self.prior / 'FAILURE.json').write_bytes(b'forged failure')
        with self.assertRaises(ValueError): self.r._hc_exec_prior(self.prior, a)

    def test_history_continuation_dispatch_and_prior_trust_anchor_remain_explicit(self):
        with mock.patch.object(self.r, 'validate_history_continuation', return_value={'checked': True}) as validate:
            value = self.r.validate_receipt({'replay_evidence': {'schema': self.r.HC_SCHEMA}}, {}, {}, self.source)
        self.assertEqual(value, {'checked': True}); validate.assert_called_once()
        bad = {**self.r.HC_PRIOR, 'receipt': {}, 'receipt_sha256': '0' * 64}
        with self.assertRaises(ValueError): self.r._hc_prior({'prior': bad}, {}, {}, self.source, self.r, {})

    def test_history_pure_fresh_ledger_refuses_replayed_children_and_resource_credit(self):
        r = self.r
        stages = [{'id': sid, 'argv': argv, 'cwd': '.', 'budget_seconds': budget,
                   'started_at': '2026-01-01T00:00:01Z', 'ended_at': '2026-01-01T00:00:02Z',
                   'terminal': 'COMPLETED', 'exit_code': 0, 'log_sha256': 'a' * 64, 'output_hashes': {}}
                  for sid, argv, budget in [('_prerequisites', ['{builtin:prerequisites}'], 30),
                      ('_target_audit', ['{tool:lean}', '-j1', '{out}/generated/V5SuccessorReadback.lean'], 300)]]
        stages[1]['started_at'] = '2026-01-01T00:00:02Z'
        def check(rows):
            receipt = {'started_at': '2026-01-01T00:00:00Z', 'ended_at': '2026-01-01T00:00:03Z',
                'stages': [{key: row[key] for key in ('id', 'terminal', 'exit_code', 'log_sha256')} for row in rows],
                'log_sha256': r.canonical({row['id']: row['log_sha256'] for row in rows})}
            return r._hc_fresh(receipt, {'stage_results': rows}, {'ended_at': '2025-01-01T00:00:00Z'}, r)
        self.assertEqual(check(stages)['id'], '_target_audit')
        for change in [dict(stages[1], id='original-driver'), dict(stages[1], terminal='TIMEOUT', exit_code=1),
                       dict(stages[1], exit_code=False), dict(stages[1], budget_seconds=301),
                       dict(stages[1], output_hashes={'Fresh.olean': 'b' * 64})]:
            with self.subTest(change=change), self.assertRaises(ValueError): check([stages[0], change])

    def test_history_pure_retained_checks_require_exact_tree_objects_and_cache_policy(self):
        r = self.r; collection = {'child_observations': [], 'driver_invocations': []}
        suite = {'replay': {'external_inputs': [{'expected_sha256': 'a' * 64}]}}
        plan = {'packages': {'Cli': {}}, 'official': {}}
        checks = {'mode': 'REUSED_CAMPAIGN_EXECUTION', 'stage_ids': ['_prerequisites', 'original-driver'],
            'physical_trace_sha256': r.HC_TRACE, 'original_result_sha256': r.HC_PRIOR['original_receipt_sha256'],
            'child_ledger_sha256': r.canonical([]), 'driver_invocations_sha256': r.canonical([]),
            'archive_sha256': 'a' * 64, 'retained_tree_before_sha256': r.HC_RETAINED_TREE,
            'retained_tree_after_sha256': r.HC_RETAINED_TREE, 'project_sources_before_sha256': r.HC_PROJECT_TREE,
            'project_sources_after_sha256': r.HC_PROJECT_TREE, 'custom_objects_before': dict(r.HC_OBJECTS),
            'custom_objects_after': dict(r.HC_OBJECTS), 'official_cache_measurements': [
                {'root_id': 'lean', 'measurement_phase': 'CONTINUATION_ONLY', 'tree_before_sha256': 'b' * 64,
                 'tree_after_sha256': 'b' * 64, 'file_count': 1, 'cache_policy': 'TRUSTED_PINNED_OFFICIAL_CACHE'},
                {'root_id': 'Cli', 'measurement_phase': 'CONTINUATION_ONLY', 'tree_before_sha256': r.canonical({}),
                 'tree_after_sha256': r.canonical({}), 'file_count': 0, 'cache_policy': 'ABSENT_UNIMPORTED_PINNED_PACKAGE_CACHE'}]}
        r._hc_retained(checks, collection, suite, plan, r)
        for key, value in [('retained_tree_after_sha256', 'f' * 64), ('custom_objects_after', {}),
                           ('physical_trace_sha256', 'f' * 64), ('stage_ids', ['_prerequisites']),
                           ('official_cache_measurements', checks['official_cache_measurements'][:1])]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                r._hc_retained({**checks, key: value}, collection, suite, plan, r)
        plan['official'] = {'Cli': {'package': 'Cli'}}
        with self.assertRaises(ValueError): r._hc_retained(checks, collection, suite, plan, r)

    @unittest.skipUnless(os.environ.get('V5_REPLAY_TEST_LEAN'), 'Explicit official Lean test binding required')
    def test_official_lean_history_continuation_uses_retained_object_without_rebuilding(self):
        data = self.execution_fixture(); a, _, plan, _, _, artifact = data
        lean = Path(os.environ['V5_REPLAY_TEST_LEAN']); self.assertEqual(self.r.sha(lean.read_bytes()), LEAN_SHA)
        env = dict(os.environ); env['LEAN_PATH'] = str(lean.parent.parent / 'lib/lean')
        run = self.r.run_process([lean, '-j1', '-o', artifact, self.prior / 'project/Fixture.lean'],
                                self.prior / 'project', env, self.base / 'initial-object.log', 60)
        self.assertEqual((run['terminal'], run['exit_code']), ('COMPLETED', 0))
        a.HC_OBJECTS['original/build/Fixture.olean'] = self.r.sha(artifact.read_bytes())
        collection = a._hc_exec_collection.return_value[0]; collection['output_hashes'] = dict(a.HC_OBJECTS)
        a.HC_COLLECTION_SHA256 = self.r._hc_collection_digest(collection, a)
        prior = a._hc_prior.return_value[0]
        fingerprints = {'lean': {'executable_sha256': self.r.sha(lean.read_bytes())}}
        prior['replay_evidence']['tool_fingerprints'] = fingerprints
        raw = json.dumps(prior).encode(); (self.prior / 'RECEIPT.json').write_bytes(raw)
        a.HC_PRIOR.update(receipt_sha256=self.r.sha(raw), receipt_bytes=len(raw), receipt_canonical_sha256=self.r.canonical(prior))
        a.HC_RETAINED_TREE = self.r._ac_exec_inventory(self.prior, a)[1]
        before = self.r._ac_exec_inventory(self.prior, a)
        a._verify_environment.return_value = ({'lean': lean}, fingerprints, {}, env, {})
        a.run_process.side_effect = self.r.run_process
        receipt = self.execute_fixture(data)
        self.assertEqual(receipt['outcome'], 'QUALIFIED_DECLARED_SUITE')
        self.assertEqual(a.run_process.call_count, 1)
        self.assertEqual(self.r._ac_exec_inventory(self.prior, a), before)


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


class PortableReplayIntegrationTests(unittest.TestCase):
    """Portable loader and terminal boundaries use disposable synthetic files."""
    names = ('portable_admission', 'portable_source', 'portable_collector',
             'portable_capture', 'portable_family')

    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name)

    def load(self, script=SCRIPT):
        name = 'portable_adapter_dynamic_fixture'
        self.assertNotIn(name, sys.modules)
        spec = importlib.util.spec_from_file_location(name, script)
        result = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(result)
        self.assertNotIn(name, sys.modules)
        return result

    def layout(self):
        folder = self.base / 'scripts'
        folder.mkdir()
        copy_replay_scripts(folder)
        return folder / 'replay_v5_successors.py'

    def test_portable_dynamic_file_loader_needs_no_module_registration(self):
        before = sys.path[:]
        r = self.load()
        self.assertEqual(r.portable_family.NAMES,
                         ('d06-portable-cost', 'd06-portable-runtime-literal'))
        self.assertEqual(sys.path, before)
        self.assertTrue(set(r.portable_admission.APPROVED) <= set(r.APPROVED_DECLARED_SUITES))

    def test_portable_dynamic_loader_ignores_and_restores_ambient_modules(self):
        ambient = {name: types.ModuleType(name) for name in self.names}
        with mock.patch.dict(sys.modules, ambient):
            r = self.load()
            for name in self.names:
                self.assertIs(sys.modules[name], ambient[name])
                self.assertIsNot(getattr(r, name), ambient[name])
            self.assertIs(r.portable_family.collector, r.portable_collector)
            self.assertIs(r.portable_capture.source, r.portable_source)

    def test_portable_helper_tampering_is_refused_before_execution(self):
        script = self.layout()
        path = script.with_name('portable_family.py')
        path.write_bytes(b"raise AssertionError('UNVERIFIED HELPER EXECUTED')\n" + path.read_bytes())
        with self.assertRaisesRegex(ValueError, 'Portable helper bytes changed'):
            self.load(script)

    def test_portable_missing_helper_is_refused_before_import(self):
        script = self.layout()
        script.with_name('portable_source.py').unlink()
        with self.assertRaisesRegex(ValueError, 'Portable helper is unavailable'):
            self.load(script)

    def test_portable_catalog_tampering_is_refused_before_import(self):
        script = self.layout()
        script.with_name('portable_bindings_v2.json').write_bytes(b'{}\n')
        with self.assertRaisesRegex(ValueError, 'Portable binding bytes changed'):
            self.load(script)

    def test_portable_loader_cleans_ambient_state_after_refusal(self):
        script = self.layout()
        path = script.with_name('portable_capture.py')
        path.write_bytes(path.read_bytes() + b'\n# altered\n')
        ambient = {name: types.ModuleType(name) for name in self.names}
        with mock.patch.dict(sys.modules, ambient):
            with self.assertRaises(ValueError):
                self.load(script)
            for name in self.names:
                self.assertIs(sys.modules[name], ambient[name])

    def test_portable_dispatch_passes_dynamic_adapter_api(self):
        r = self.load()
        captured = []
        def validate(api, receipt, suite, sources, root):
            captured.append(api)
            self.assertIs(api.require, r.require)
            return {'fixture': True}
        with mock.patch.object(r.portable_family, 'validate_receipt', side_effect=validate):
            result = r.validate_receipt({'replay_evidence': {'schema': r.portable_family.EVIDENCE_SCHEMA}}, {}, {}, self.base)
        self.assertEqual(result, {'fixture': True})
        self.assertEqual(len(captured), 1)

    def test_portable_dispatch_defers_malformed_outer_receipt_to_schema_gate(self):
        r = self.load()
        for receipt in (None, [], 1, 'invalid'):
            with self.subTest(receipt=receipt), self.assertRaises(ValueError):
                r.validate_receipt(receipt, {}, {}, self.base)

    def test_portable_dispatch_defers_malformed_nested_evidence_to_schema_gate(self):
        r = self.load()
        for evidence in (None, [], 1, 'invalid'):
            with self.subTest(evidence=evidence), self.assertRaises(ValueError):
                r.validate_receipt({'replay_evidence': evidence}, {}, {}, self.base)

    def test_portable_cli_dispatch_does_not_require_ambient_module(self):
        r = self.load()
        with mock.patch.object(sys, 'argv', ['fixture', '--portable-family', '--help']), \
             mock.patch.object(r.portable_family, 'command_line', return_value=0) as command:
            self.assertEqual(r.main(), 0)
        self.assertIs(command.call_args.args[0].require, r.require)
        self.assertEqual(command.call_args.args[1], ['--help'])

    def test_portable_generic_execution_refuses_before_any_output(self):
        r = self.load()
        suite = {'replay': {'drivers': [{'recipe': r.portable_admission.RECIPE}]}}
        output = self.base / 'out'
        with self.assertRaisesRegex(ValueError, 'single physical family executor'):
            r.execute_suite(suite, {}, self.base, output, {}, {})
        self.assertFalse(output.exists())

    def event(self, r, body="print('portable fixture')", timeout=1):
        path = self.base / 'tiny.py'
        path.write_text(body + '\n')
        event = {'readonly': False, 'id': 'literal/native',
                 'argv': [sys.executable, '-B', str(path)], 'cwd': str(self.base),
                 'timeout': timeout, 'source_path': str(path), 'source_sha256': r.sha(path.read_bytes()),
                 'member': 'tiny.py', 'object_path': None, 'lean_path': None, 'expected_exit': 0,
                 'original_log': 'native.log', 'timeout_marker': None}
        plan = {'events': [event], 'children': [event], 'event_plan_sha256': r.canonical([event])}
        trace = self.base / 'trace'
        trace.mkdir()
        return event, plan, trace

    def invoke(self, callback, event):
        return callback(event['argv'], cwd=self.base, stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True, timeout=event['timeout'])

    def test_portable_actual_python_capture_records_source_and_terminal(self):
        r = self.load()
        event, plan, trace = self.event(r)
        callback = r.portable_capture.capture_calls(r, subprocess.run, trace, plan, self.base / 'state.json')
        self.assertEqual(self.invoke(callback, event).returncode, 0)
        self.assertTrue(callback.finish()['complete'])
        row = r.read_json(trace / '0000.json')
        self.assertEqual(row['argv'], event['argv'])
        self.assertEqual(row['terminal'], 'COMPLETED')
        self.assertEqual(row['raw_returncode'], 0)
        self.assertEqual(row['source_sha256_before'], row['source_sha256_after'])
        self.assertEqual(row['output_hashes_after'], {})
        with self.assertRaisesRegex(ValueError, 'Extra portable original call'):
            self.invoke(callback, event)
        self.assertFalse((trace / '0001.json').exists())

    def test_portable_actual_timeout_retains_no_invented_rejection(self):
        r = self.load()
        event, plan, trace = self.event(r, 'import time; time.sleep(3)')
        callback = r.portable_capture.capture_calls(r, subprocess.run, trace, plan, self.base / 'state.json')
        with self.assertRaises(subprocess.TimeoutExpired):
            self.invoke(callback, event)
        callback.finish()
        row = r.read_json(trace / '0000.json')
        self.assertEqual(row['terminal'], 'TIMEOUT')
        self.assertIsNone(row['raw_returncode'])
        self.assertIsNone(row['exit_code'])

    def test_portable_signal_code_is_retained_without_semantic_credit(self):
        r = self.load()
        event, plan, trace = self.event(r)
        fake = lambda argv, **kwargs: subprocess.CompletedProcess(argv, -9, 'synthetic signal\n')
        callback = r.portable_capture.capture_calls(r, fake, trace, plan, self.base / 'state.json')
        self.invoke(callback, event)
        callback.finish()
        row = r.read_json(trace / '0000.json')
        self.assertEqual(row['terminal'], 'INTERRUPTED')
        self.assertEqual(row['raw_returncode'], -9)
        self.assertIsNone(row['exit_code'])

    def test_portable_capture_refuses_source_changed_during_process(self):
        r = self.load()
        event, plan, trace = self.event(r)
        def changed(argv, **kwargs):
            Path(event['source_path']).write_bytes(b'changed fixture\n')
            return subprocess.CompletedProcess(argv, 0, '')
        callback = r.portable_capture.capture_calls(r, changed, trace, plan, self.base / 'state.json')
        with self.assertRaisesRegex(ValueError, 'source changed during child'):
            self.invoke(callback, event)
        row = r.read_json(trace / '0000.json')
        self.assertNotEqual(row['source_sha256_before'], row['source_sha256_after'])

    def test_portable_cost_resource_dominates_concrete_application_mismatch(self):
        r = self.load()
        event = {'id': 'cost/ExactInheritedCostMutant', 'argv': ['lean', 'Fixture.lean'],
                 'cwd': '.', 'source_sha256': '1' * 64, 'expected_exit': 1,
                 'timeout_marker': '\nWALL_TIMEOUT_180\n'}
        text = '\n'.join(r.portable_source.MISMATCH) + '\nmaximum number of heartbeats\n'
        log = text.encode()
        captured = {'argv': event['argv'], 'cwd': '.', 'log_sha256': r.sha(log),
                    'exit_code': 1, 'terminal': 'COMPLETED'}
        original = {'source_sha256': event['source_sha256'], 'command': event['argv'],
                    'exit_code': 1, 'log_sha256': r.sha(log), 'resource_diagnostic': True}
        row = r.portable_source.classify_child(r, event, original, captured, log, log)
        self.assertTrue(row['concrete_application_mismatch'])
        self.assertTrue(row['mismatch_precedes_resource'])
        self.assertEqual(row['outcome'], 'RESOURCE_INCONCLUSIVE')
        self.assertIsNone(row['semantic_outcome'])
        self.assertFalse(row['unchanged_theorem_refuted'])

    def cache(self):
        root = self.base / 'mathlib'
        (root / '.lake/build/lib/lean').mkdir(parents=True)
        (root / '.lake/packages/Cli').mkdir(parents=True)
        plan = {'packages': {'mathlib': {'kind': 'GIT', 'path': '.'},
                             'Cli': {'kind': 'GIT', 'path': '.lake/packages/Cli'}},
                'official': {'Mathlib.Fixture': {'package': 'mathlib'}}}
        return root, plan

    def test_portable_cache_allows_only_absent_unimported_cli(self):
        r = self.load()
        root, plan = self.cache()
        r.portable_family._verify_original_libraries(r, plan, root)
        plan['official']['Cli.Fixture'] = {'package': 'Cli'}
        with self.assertRaisesRegex(r.MissingTool, 'Required imported package cache'):
            r.portable_family._verify_original_libraries(r, plan, root)

    def test_portable_cache_rejects_extra_search_root(self):
        r = self.load()
        root, plan = self.cache()
        (root / '.lake/packages/unlisted/.lake/build/lib/lean').mkdir(parents=True)
        with self.assertRaisesRegex(ValueError, 'library search differs'):
            r.portable_family._verify_original_libraries(r, plan, root)

    def test_portable_wrong_physical_recipe_cannot_be_resealed(self):
        r = self.load()
        with self.assertRaisesRegex(ValueError, 'Unknown portable physical recipe'):
            r.portable_family._physical(r, {'schema': r.portable_family.PHYSICAL_SCHEMA,
                                            'recipe': 'foreign-recipe'})

    def test_portable_parent_terminal_requires_exact_nonresource_exit(self):
        r = self.load()
        row = {'terminal': 'COMPLETED', 'exit_code': 0, 'started_at': '2026-01-01T00:00:00Z',
               'ended_at': '2026-01-01T00:00:01Z', 'log_sha256': '1' * 64}
        r.portable_family._parent_run(r, row)
        for terminal, code in [('COMPLETED', True), ('COMPLETED', -9), ('COMPLETED', 124), ('TIMEOUT', 1)]:
            with self.subTest(terminal=terminal, code=code), self.assertRaises(ValueError):
                r.portable_family._parent_run(r, {**row, 'terminal': terminal, 'exit_code': code})
        r.portable_family._parent_run(r, {**row, 'terminal': 'TIMEOUT', 'exit_code': None})

    def test_portable_audit_rejects_changed_owner_axiom_and_object_binding(self):
        r = self.load()
        target = {'target_id': 'main', 'name': 'Fixture.safe', 'module': 'Fixture'}
        plan = {'targets': {'main': target}}
        row = {'target_id': 'main', 'name': 'Fixture.safe', 'stage_id': '_target_audit',
               'log_sha256': '1' * 64, 'type_sha256': '2' * 64, 'closure_status': 'CHECKED_SAFE',
               'checked_declarations': 1, 'axioms': []}
        audit = {'run': {'terminal': 'COMPLETED', 'exit_code': 0,
                         'started_at': '2026-01-01T00:00:00Z', 'ended_at': '2026-01-01T00:00:01Z',
                         'log_sha256': '1' * 64}, 'source_sha256': r.sha(r._audit_source([target]).encode()),
                 'object_provenance_sha256': r.canonical([]), 'target_audits': [row],
                 'status': 'COMPLETE', 'resource_diagnostic': False}
        self.assertTrue(r.portable_family._audit_valid(r, {}, plan, audit, [], True))
        changes = [{'name': 'Foreign.safe'}, {'axioms': ['Foreign.axiom']},
                   {'checked_declarations': True}, {'closure_status': 'NOT_CHECKED'}]
        for change in changes:
            with self.subTest(change=change), self.assertRaises(ValueError):
                r.portable_family._audit_valid(r, {}, plan, {**audit, 'target_audits': [{**row, **change}]}, [], True)
        with self.assertRaisesRegex(ValueError, 'namespace object mapping differs'):
            r.portable_family._audit_valid(r, {}, plan, audit, [{'changed': True}], True)

    def test_portable_missing_tools_yield_two_views_without_producer(self):
        r = self.load()
        plans = {name: {} for name in r.portable_family.NAMES}
        suites = [{'id': name, 'review_ids': []} for name in r.portable_family.NAMES]
        failure = {'run_id': '1' * 64, 'physical_execution_count': 0}
        receipt = {'outcome': 'BLOCKED_TOOLCHAIN', 'proof_scope': 'NONE'}
        with mock.patch.object(r.portable_family, 'validate_family', return_value=plans), \
             mock.patch.object(r.portable_family, '_produce', return_value=(failure, {}, {})) as produce, \
             mock.patch.object(r.portable_family, 'consume_view', return_value=receipt) as consume:
            result = r.portable_family.execute_family(r, suites, {}, self.base / 'sources',
                                                     self.base / 'out', {}, {}, reviews={})
        self.assertEqual(produce.call_count, 1)
        self.assertEqual(consume.call_count, 2)
        self.assertEqual(result['physical_execution_count'], 0)
        self.assertTrue(all(row['outcome'] == 'BLOCKED_TOOLCHAIN' for row in result['views'].values()))


# P1 synthetic adapter controls: no original source, archive, driver or producer is executed.
class P1SourceBoundAdapterTests(unittest.TestCase):

    def setUp(self):
        spec = importlib.util.spec_from_file_location('p1_synthetic_adapter_under_test', SCRIPT)
        self.r = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.r)
        self.temp = tempfile.TemporaryDirectory(prefix='p1-adapter-fixture-')
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)

    def event(self, name='Positive', expected=0, finite=False):
        source = self.base / (name + '.py' if finite else name + '.lean')
        source.write_text('SYNTHETIC NONSCIENTIFIC FIXTURE\n')
        obj = None if finite else self.base / 'original/build' / (name + '.olean')
        argv = [sys.executable, '-B', str(source)] if finite else ['/fixture/lean', '-j1', '--root=' + str(self.base), '-o', str(obj), str(source)]
        return {'id': name, 'argv': argv, 'cwd': str(self.base / 'original'), 'profile': 'PYTHON_PIPE' if finite else 'LEAN_PIPE', 'source_path': str(source), 'source_sha256': self.r.sha(source.read_bytes()), 'object_path': str(obj) if obj else None, 'expected_exit': expected, 'positive_prerequisites': ['Positive'] if expected else [], 'lean_path': '/fixture/build:/fixture/cache', 'lean_bin': '/fixture', 'timeout': 180, 'finite': finite, 'axiom_count': None, 'log': str(self.base / 'original/logs' / (name + '.log')), 'required_copies': {}}

    def plan(self, events):
        return {'children': events, 'events': events, 'replacements': [(str(self.base), '$PACKET'), (str(self.base / 'original'), '$OUTPUT'), ('/fixture', '$LEAN_ROOT'), ('/cache', '$MATHLIB_ROOT'), (sys.executable, '$PYTHON')], 'derivations': {}, 'generated_bytes': {}, 'driver_sha256': self.r.p1_driver, 'plan_sha256': self.r.canonical([e['id'] for e in events]), 'preflight': None}

    def kwargs(self, event, parent=None):
        parent = parent or {'PATH': '/fixture/bin', 'KEPT': 'value'}
        env = {k: v for k, v in parent.items() if not k.startswith(('LEAN', 'LD_'))}
        env.update(LEAN_PATH=event['lean_path'], PYTHONDONTWRITEBYTECODE='1', PATH=event['lean_bin'] + os.pathsep + env.get('PATH', ''))
        return {'cwd': Path(event['cwd']), 'env': env, 'stdout': subprocess.PIPE, 'stderr': subprocess.STDOUT, 'text': True, 'timeout': 180}

    def observed(self, plan, event, raw, code=0, terminal='COMPLETED', returned=True):
        capture = {'index': 0, 'argv': event['argv'], 'cwd': event['cwd'], 'started_at': '2026-10-05T00:00:01Z', 'ended_at': '2026-10-05T00:00:02Z', 'terminal': terminal, 'exit_code': code if terminal == 'COMPLETED' else None, 'returned_exit_code': code if returned else None, 'returned': returned, 'log_sha256': self.r.sha(raw), 'source_sha256': event['source_sha256'], 'output_hashes': {}, 'input_receipt_sha256': None}
        clean = self.r.p1_neutralize(self.r, raw, plan['replacements'], terminal == 'TIMEOUT')['derived_bytes']
        row = None if not returned else {'name': event['id'], 'expectation': 'REJECT' if event['expected_exit'] else 'ACCEPT', 'exit_code': code, 'elapsed_seconds': 0.1, 'command': [self.r.p1_neutralize(self.r, x.encode(), plan['replacements'])['derived_bytes'].decode() for x in event['argv']], 'source_sha256': event['source_sha256'], 'raw_diagnostic_sha256': self.r.sha(raw), 'path_neutral_log_sha256': self.r.sha(clean), 'diagnostic_path_substitution_only': True, 'wall_limit_seconds': 180}
        return (capture, clean, row)

    def test_private_pair_refuses_unpaired_unknown_and_arbitrary(self):
        for v in [{'trace_prefix': 'x', 'pinned_trace_prefix': ''}, {'trace_prefix': 'x', 'pinned_trace_prefix': 'y'}, {'trace_prefix': '', 'pinned_trace_prefix': '', 'extra': 1}]:
            with self.assertRaises(ValueError):
                self.r.p1_private_parameters(self.r, v, self.base)

    def test_source_binding_variants_are_exact_and_typed(self):
        h = 'a' * 64
        sources = {'owner': {'original_sha256': h}, 'archive': {'original_sha256': 'b' * 64}}
        rows = [{'kind': 'ORIGINAL_SOURCE', 'source_id': 'owner', 'source_sha256': h}, {'kind': 'ARCHIVE_MEMBER', 'archive_source_id': 'archive', 'archive_sha256': 'b' * 64, 'member': 'safe/source.py', 'source_sha256': h}, {'kind': 'GENERATED_BY_ORIGINAL', 'source_id': 'owner', 'source_sha256': h, 'generated_sha256': h, 'derivation_id': 'copied-exact'}, {'kind': 'TOOL_PROBE', 'tool_name': 'python', 'executable_sha256': self.r.p1_python, 'driver_sha256': self.r.p1_driver}]
        for row in rows:
            self.assertEqual(self.r.p1_source_binding(self.r, row, sources, h), row)
            with self.assertRaises(ValueError):
                self.r.p1_source_binding(self.r, dict(row, extra=True), sources, h)

    def test_actual_capture_preserves_returned_signal_code(self):
        event = self.event()
        plan = self.plan([event])
        trace = self.base / 'trace'
        trace.mkdir()
        fn = self.r.p1_capture_run(self.r, lambda *a, **k: subprocess.CompletedProcess(a[0], -9, 'partial\n'), plan, trace, {'PATH': '/fixture/bin', 'KEPT': 'value'})
        result = fn(event['argv'], **self.kwargs(event))
        row = self.r.read_json(trace / '0000.json')
        self.assertEqual(result.returncode, -9)
        self.assertEqual(row['returned_exit_code'], -9)
        self.assertEqual(row['terminal'], 'INTERRUPTED')
        self.assertIsNone(row['exit_code'])

    def test_capture_refuses_changed_call_before_effect(self):
        event = self.event()
        trace = self.base / 'trace'
        trace.mkdir()
        calls = []
        fn = self.r.p1_capture_run(self.r, lambda *a, **k: calls.append(a), self.plan([event]), trace, {'PATH': '/fixture/bin', 'KEPT': 'value'})
        with self.assertRaises(ValueError):
            fn(event['argv'], **dict(self.kwargs(event), timeout=181))
        self.assertEqual(calls, [])
        self.assertEqual(list(trace.iterdir()), [])

    def test_timeout_capture_preserves_raw_bytes_and_raises_original_exception(self):
        event = self.event()
        trace = self.base / 'trace'
        trace.mkdir()
        error = subprocess.TimeoutExpired(event['argv'], 180, output=b'partial\xff')

        def timeout(*a, **k):
            raise error
        fn = self.r.p1_capture_run(self.r, timeout, self.plan([event]), trace, {'PATH': '/fixture/bin', 'KEPT': 'value'})
        with self.assertRaises(subprocess.TimeoutExpired) as got:
            fn(event['argv'], **self.kwargs(event))
        self.assertIs(got.exception, error)
        row = self.r.read_json(trace / '0000.json')
        self.assertFalse(row['returned'])
        self.assertEqual((trace / '0000.log').read_bytes(), b'partial\xff')
        self.assertEqual(row['terminal'], 'TIMEOUT')

    def test_dispatch_restores_process_globals_on_exception(self):
        old_run = subprocess.run
        old_argv = sys.argv
        old_path = sys.path[:]
        cwd = Path.cwd()
        driver = self.base / 'replay.py'
        driver.write_text('SYNTHETIC')

        def runner(*a, **k):
            raise RuntimeError('synthetic stop')
        with mock.patch.object(self.r, 'p1_check_driver', return_value=None, create=True):
            with self.assertRaisesRegex(RuntimeError, 'synthetic stop'):
                self.r.p1_run_original(self.r, driver, [], self.plan([]), self.base / 'trace', runner=runner)
        self.assertIs(subprocess.run, old_run)
        self.assertIs(sys.argv, old_argv)
        self.assertEqual(sys.path, old_path)
        self.assertEqual(Path.cwd(), cwd)

    def test_returned_signal_joins_original_row_without_rejection(self):
        e = self.event('Mutant', 1)
        p = self.plan([e])
        raw = b"error: tactic 'rfl' failed\n"
        cap, log, row = self.observed(p, e, raw, -9, 'INTERRUPTED')
        got = self.r.p1_classify(self.r, p, e, cap, raw, log, row, {'Positive'})
        self.assertEqual(got['outcome'], 'RESOURCE_INCONCLUSIVE')
        self.assertEqual(got['rejecting_subprocesses'], 0)

    def test_resource_diagnostic_dominates_concrete_mismatch(self):
        e = self.event('Mutant', 1)
        p = self.plan([e])
        raw = b"error: tactic 'rfl' failed\nmaximum number of heartbeats exceeded\n"
        cap, log, row = self.observed(p, e, raw, 1)
        self.assertEqual(self.r.p1_classify(self.r, p, e, cap, raw, log, row, {'Positive'})['outcome'], 'RESOURCE_INCONCLUSIVE')

    def test_rejection_requires_positives_and_absent_object(self):
        e = self.event('Mutant', 1)
        p = self.plan([e])
        raw = b"error: tactic 'rfl' failed\n"
        cap, log, row = self.observed(p, e, raw, 1)
        with self.assertRaises(ValueError):
            self.r.p1_classify(self.r, p, e, cap, raw, log, row, set())
        obj = Path(e['object_path'])
        obj.parent.mkdir(parents=True)
        obj.write_bytes(b'fixture')
        with self.assertRaises(ValueError):
            self.r.p1_classify(self.r, p, e, cap, raw, log, row, {'Positive'})

    def test_log_and_command_hash_join_rejects_mutation(self):
        e = self.event('Mutant', 1)
        p = self.plan([e])
        raw = b"error: tactic 'rfl' failed\n"
        cap, log, row = self.observed(p, e, raw, 1)
        row['raw_diagnostic_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            self.r.p1_classify(self.r, p, e, cap, raw, log, row, {'Positive'})

    def test_inventory_checks_complete_census_hashes_and_symlinks(self):
        root = self.base / 'deps'
        root.mkdir()
        (root / 'x').write_bytes(b'one')
        pin = {'roots': [''], 'entries': [{'path': 'x', 'kind': 'file', 'bytes': 3, 'sha256': self.r.sha(b'one')}]}
        result = self.r.p1_inventory(self.r, root, pin)
        self.assertEqual(result['entries'], 1)
        (root / 'extra').write_bytes(b'x')
        with self.assertRaises(ValueError):
            self.r.p1_inventory(self.r, root, pin)

    def test_audit_source_uses_fresh_namespace_and_exact_root_names(self):
        targets = [{'target_id': 'x', 'module': 'Fixture', 'name': 'Alpha.exact'}]
        text = self.r.p1_audit_source(self.r, targets)
        self.assertIn('#check @Alpha.exact', text)
        self.assertNotIn('namespace V5SuccessorCheckedAudit', text)
        self.assertIn('env.checked.get.find?', text)
        self.assertIn('info.type.getUsedConstants', text)

    def test_whole_collector_refuses_empty_success_assertion(self):
        out = self.base / 'original'
        out.mkdir()
        trace = self.base / 'trace'
        trace.mkdir()
        self.r.write_json(out / 'REPLAY_RECEIPT.json', {'status': 'PASS_PORTABLE_P1_REPLAY'})
        with self.assertRaises(ValueError):
            self.r.p1_collect(self.r, self.plan([]), out, trace, {'exit_code': 0}, b'')

    def test_views_require_all_original_children_and_safe_targets(self):
        with self.assertRaises(ValueError):
            self.r.p1_views(self.r, {'children': []}, [])

    def test_real_synthetic_python_child_is_captured_once(self):
        e = self.event('TinyPython', finite=True)
        Path(e['source_path']).write_text("print('SYNTHETIC CHILD')\n")
        e['source_sha256'] = self.r.sha(Path(e['source_path']).read_bytes())
        Path(e['cwd']).mkdir()
        trace = self.base / 'actual-trace'
        trace.mkdir()
        parent = {'PATH': os.defpath}
        call = self.r.p1_capture_run(self.r, subprocess.run, self.plan([e]), trace, parent)
        result = call(e['argv'], **self.kwargs(e, parent))
        self.assertEqual(result.returncode, 0)
        row = self.r.read_json(trace / '0000.json')
        self.assertEqual(row['returned_exit_code'], 0)
        self.assertEqual((trace / '0000.log').read_bytes(), b'SYNTHETIC CHILD\n')
        with self.assertRaises(ValueError):
            call(e['argv'], **self.kwargs(e, parent))



# Exact P1 external asset packaging checks; no scientific producer executes.
class P1PackagingTests(unittest.TestCase):

    def setUp(self):
        import shutil
        self.temp = tempfile.TemporaryDirectory(prefix='p1-packaging-fixture-')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.script = self.root / SCRIPT.name
        copy_replay_scripts(self.root)
        self.catalog = self.root / 'v5_p1_recipes.json'
        self.helper = self.root / 'v5_p1_assets/p1_recipe.py'

    def load(self):
        spec = importlib.util.spec_from_file_location('p1_packaging_fixture', self.script)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_external_assets_are_exactly_pinned(self):
        module = self.load()
        self.assertEqual(set(module.p1_asset_pins), {'v5_p1_recipes.json', 'v5_p1_assets/p1_recipe.py'})
        for name, row in module.p1_asset_pins.items():
            data = (self.root / name).read_bytes()
            self.assertEqual(row, {'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
        self.assertEqual(module.p1_meta, json.loads(self.catalog.read_bytes()))
        self.assertEqual(module.p1_recipe, 't09-p1-original-v1')
        self.assertEqual(module.p1_api().__file__, str(self.script))

    def test_missing_catalog_refused(self):
        self.catalog.unlink()
        with self.assertRaises(ValueError):
            self.load()

    def test_changed_catalog_bytes_refused(self):
        self.catalog.write_bytes(self.catalog.read_bytes() + b'\n')
        with self.assertRaises(ValueError):
            self.load()

    def test_missing_helper_refused(self):
        self.helper.unlink()
        with self.assertRaises(ValueError):
            self.load()

    def test_changed_helper_refused_before_execution(self):
        marker = self.root / 'MUST_NOT_EXIST'
        self.helper.write_text('from pathlib import Path\nPath(' + repr(str(marker)) + ').write_text("wrong")\n')
        with self.assertRaises(ValueError):
            self.load()
        self.assertFalse(marker.exists())

    def test_catalog_symlink_refused(self):
        other = self.root / 'other.json'
        self.catalog.rename(other)
        self.catalog.symlink_to(other)
        with self.assertRaises(ValueError):
            self.load()

    def test_helper_directory_symlink_refused(self):
        directory = self.helper.parent
        other = self.root / 'other-assets'
        directory.rename(other)
        directory.symlink_to(other, target_is_directory=True)
        with self.assertRaises(ValueError):
            self.load()


# Packaged selector/G1 offline boundary tests; no original science.
import ast
import shutil

class SelectorG1PackagingTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='selector-g1-packaging-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_changed_family_module_rejected_before_compile(self):
        r = self.adapter()
        path = r.selector_g1_family_path()
        path.write_bytes(path.read_bytes() + b'\nraise RuntimeError("must not execute")\n')
        with self.assertRaisesRegex(ValueError, 'Changed selector/G1 family module'):
            r.selector_g1_load_family()

    def test_missing_family_module_is_closed(self):
        r = self.adapter()
        path = r.selector_g1_family_path()
        path.rename(path.with_suffix('.held'))
        with self.assertRaises((OSError, ValueError)):
            r.selector_g1_load_family()

    def test_changed_json_is_rejected(self):
        r = self.adapter()
        f = r.selector_g1_load_family()
        p = Path(f.__file__).with_name('replay_selector_g1_catalog.json')
        p.write_bytes(p.read_bytes() + b' ')
        with self.assertRaisesRegex(ValueError, 'Changed code-owned'):
            f.selector_g1_catalog(r)

    def test_changed_helper_is_rejected_and_module_state_restored(self):
        r = self.adapter()
        f = r.selector_g1_load_family()
        name = list(f.SELECTOR_G1_HELPERS)[1]
        p = Path(f.__file__).with_name(name + '.py')
        p.write_bytes(p.read_bytes() + b'\nraise RuntimeError("must not execute")\n')
        before = {n: sys.modules.get(n) for n in f.SELECTOR_G1_HELPERS}
        with self.assertRaisesRegex(ValueError, 'Changed reviewed family helper'):
            with f.selector_g1_helpers(r):
                pass
        self.assertEqual(before, {n: sys.modules.get(n) for n in before})

    def test_preimported_poison_cannot_replace_bound_helper(self):
        r = self.adapter()
        f = r.selector_g1_load_family()
        sentinel = object()
        name = next(iter(f.SELECTOR_G1_HELPERS))
        before = sys.modules.get(name)
        sys.modules[name] = sentinel
        try:
            with f.selector_g1_helpers(r) as helpers:
                self.assertIsNot(helpers['selector'], sentinel)
            self.assertIs(sys.modules[name], sentinel)
        finally:
            if before is None:
                sys.modules.pop(name, None)
            else:
                sys.modules[name] = before

    def test_stale_bytecode_and_unreviewed_package_init_are_unused(self):
        r = self.adapter()
        p = r.selector_g1_family_path()
        (p.parent / '__init__.py').write_text('raise RuntimeError("unreviewed package init")\n')
        (p.parent / '__pycache__').mkdir()
        (p.parent / '__pycache__/replay_selector_g1.cpython-311.pyc').write_bytes(b'INVALID BYTECODE')
        self.assertEqual(r.selector_g1_load_family().SELECTOR_G1_CATALOG_SHA256, '1c04885e6a997afd24e831315a1bd313fbaef693c2d682402db0637407b55344')

    def test_symlinked_asset_is_rejected(self):
        r = self.adapter()
        p = r.selector_g1_family_path()
        held = p.with_suffix('.held')
        p.rename(held)
        try:
            p.symlink_to(held)
        except OSError as error:
            self.skipTest(str(error))
        with self.assertRaises(ValueError):
            r.selector_g1_load_family()

    def test_public_dispatch_uses_packaged_family_and_main_globals(self):
        r = self.adapter()
        f = r.selector_g1_load_family()
        cat = f.selector_g1_catalog(r)
        for definition in cat['families'].values():
            suite = definition['suite']
            for entry, hook, args in [('validate_suite', 'selector_g1_validate_suite', (suite, {}, self.root)), ('validate_receipt', 'selector_g1_validate_receipt', ({}, suite, {}, self.root)), ('execute_suite', 'selector_g1_execute', (suite, {}, self.root, self.root / 'out', {}, {}))]:
                with self.subTest(entry=entry, suite=suite['id']), mock.patch.object(r, 'selector_g1_load_family', return_value=f), mock.patch.object(f, hook, return_value='BOUND') as checked:
                    self.assertEqual(getattr(r, entry)(*args), 'BOUND')
                    self.assertIs(checked.call_args.args[0].run_process, r.run_process)
        with mock.patch.object(r, 'selector_g1_load_family', side_effect=AssertionError('legacy loaded new assets')):
            with self.assertRaises(ValueError):
                r.validate_suite({}, {}, self.root)

    def test_exact_checked_module_bytes_are_the_executed_bytes(self):
        r = self.adapter()
        p = r.selector_g1_family_path()
        original = Path.read_bytes
        reads = []

        def capture(path):
            if path == p:
                reads.append(path)
            return original(path)
        with mock.patch.object(Path, 'read_bytes', capture):
            r.selector_g1_load_family()
        self.assertEqual(reads, [p])

    def test_catalogue_and_helpers_read_each_payload_once(self):
        r = self.adapter()
        f = r.selector_g1_load_family()
        original = Path.read_bytes
        seen = []

        def capture(path):
            seen.append(path)
            return original(path)
        with mock.patch.object(Path, 'read_bytes', capture):
            f.selector_g1_catalog(r)
            with f.selector_g1_helpers(r):
                pass
        expected = [Path(f.__file__).with_name('replay_selector_g1_catalog.json'), *[Path(f.__file__).with_name(n + '.py') for n in f.SELECTOR_G1_HELPERS]]
        self.assertEqual(seen, expected)

    def adapter(self):
        (self.root / 'scripts').mkdir()
        source = SCRIPT
        copy_replay_scripts(self.root / 'scripts')
        spec = importlib.util.spec_from_file_location('selector_g1_packaging_fixture', self.root / 'scripts/replay_v5_successors.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_valid_packaging_loads_exact_catalogue_and_helpers(self):
        r = self.adapter()
        family = r.selector_g1_load_family()
        catalog = family.selector_g1_catalog(r)
        self.assertEqual(set(catalog['families']), {'selector', 'g1', 'g1-review'})
        self.assertEqual(family.SELECTOR_G1_CATALOG_SHA256, '1c04885e6a997afd24e831315a1bd313fbaef693c2d682402db0637407b55344')
        before = {name: sys.modules.get(name) for name in family.SELECTOR_G1_HELPERS}
        with family.selector_g1_helpers(r) as helpers:
            self.assertEqual(set(helpers), {'selector', 'g1', 'normalizers'})
        self.assertEqual(before, {name: sys.modules.get(name) for name in before})

class SelectorG1CacheBoundaryTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('selector_g1_public_packaged_tests', SCRIPT)
        cls.adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.adapter)
        cls.family = cls.adapter.selector_g1_load_family()
        cls.catalog = cls.family.selector_g1_catalog(cls.adapter)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='selector-g1-cache-SYNTHETIC-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        suite = self.catalog['families']['g1']['suite']
        self.suite = suite
        self.plan = {'packages': self.adapter.indexed(suite['replay']['packages'], 'name'), 'official': self.adapter.indexed(suite['replay']['official_imports'], 'module')}
        self.tools = {'lean': self.root / 'lean/bin/lean', 'mathlib': self.root / 'mathlib'}
        self.tools['lean'].parent.mkdir(parents=True)
        self.tools['lean'].write_bytes(b'SYNTHETIC NO EXECUTION')
        self.libraries = {'lean': self.root / 'lean/lib/lean'}
        self.libraries.update({name: self.adapter.path_in(self.tools['mathlib'], row['path'], dot=True) / '.lake/build/lib/lean' for name, row in self.plan['packages'].items()})
        for name, path in self.libraries.items():
            if name == 'Cli':
                continue
            path.mkdir(parents=True)
            (path / 'Synthetic.olean').write_bytes(b'NONEXECUTABLE SYNTHETIC CACHE')

    def extra(self):
        p = self.tools['mathlib'] / '.lake/packages/Undeclared/.lake/build/lib/lean'
        p.mkdir(parents=True)
        (p / 'Synthetic.olean').write_bytes(b'NONEXECUTABLE FOREIGN CACHE')
        return p

    def test_declared_available_libraries_allow_only_unimported_absent_cli(self):
        result = self.family.selector_g1_cache_measurements(self.adapter, self.plan, self.tools)
        self.assertEqual(result['Cli'], {'files': 0, 'tree_sha256': self.adapter.canonical({})})
        self.assertEqual(set(result), set(self.libraries))

    def test_new_extra_sibling_is_rejected_in_post_run_readback(self):
        self.family.selector_g1_cache_measurements(self.adapter, self.plan, self.tools)
        self.extra()
        with self.assertRaisesRegex(ValueError, 'Unreviewed extra original import cache'):
            self.family.selector_g1_cache_measurements(self.adapter, self.plan, self.tools)

    def test_imported_missing_library_is_rejected(self):
        name = next((name for name in self.plan['packages'] if name not in {'mathlib', 'Cli'}))
        self.plan['official']['SyntheticRequiredCache'] = {'package': name}
        p = self.libraries[name]
        p.rename(p.with_name('held-cache'))
        with self.assertRaises((ValueError, self.adapter.MissingTool)):
            self.family.selector_g1_cache_measurements(self.adapter, self.plan, self.tools)

    def test_missing_non_cli_is_not_silently_allowed_when_unimported(self):
        name = next((name for name in self.plan['packages'] if name not in {'mathlib', 'Cli'}))
        self.plan['official'] = {k: r for k, r in self.plan['official'].items() if r['package'] != name}
        p = self.libraries[name]
        p.rename(p.with_name('held-cache'))
        with self.assertRaises((ValueError, self.adapter.MissingTool)):
            self.family.selector_g1_cache_measurements(self.adapter, self.plan, self.tools)

    def test_imported_cli_cannot_use_absent_exception(self):
        self.plan['official']['SyntheticCli'] = {'package': 'Cli'}
        with self.assertRaises((ValueError, self.adapter.MissingTool)):
            self.family.selector_g1_cache_measurements(self.adapter, self.plan, self.tools)

    def test_present_non_directory_cli_is_rejected(self):
        p = self.libraries['Cli']
        p.parent.mkdir(parents=True)
        p.write_bytes(b'NOT A LIBRARY')
        with self.assertRaises((ValueError, self.adapter.MissingTool)):
            self.family.selector_g1_cache_measurements(self.adapter, self.plan, self.tools)

    def test_target_audit_branch_rejects_new_sibling_before_launch(self):
        self.family.selector_g1_cache_measurements(self.adapter, self.plan, self.tools)
        self.extra()
        tree = ast.parse(Path(self.family.__file__).read_text())
        fn = next((n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'selector_g1_execute'))
        tried = next((n for n in fn.body if isinstance(n, ast.Try)))
        begin = next((i for i, n in enumerate(tried.body) if isinstance(n, ast.Assign) and any((isinstance(t, ast.Name) and t.id == 'libs' for t in n.targets))))
        end = next((i for i, n in enumerate(tried.body[begin:], begin) if isinstance(n, ast.Assign) and any((isinstance(t, ast.Name) and t.id == 'audit_run' for t in n.targets))))
        branch = ast.Module(body=tried.body[begin:end + 1], type_ignores=[])
        ast.fix_missing_locations(branch)
        context = dict(self.family.__dict__)
        context.update(api=self.adapter, output=self.root / 'out', plan=self.plan, tools=self.tools, family='g1', suite=self.suite, inputs={}, resolved={'lean': self.tools['lean']}, env={}, audit=self.root / 'Audit.lean', project=self.root, logs=self.root)
        with mock.patch.object(self.adapter, 'run_process', return_value={'terminal': 'COMPLETED', 'exit_code': 0}) as launch:
            with self.assertRaisesRegex(ValueError, 'Unreviewed extra original import cache'):
                exec(compile(branch, '<exact-target-audit-branch>', 'exec'), context)
            launch.assert_not_called()

class SelectorG1OriginalContractPortableTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('selector_g1_public_packaged_tests', SCRIPT)
        cls.adapter = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.adapter)
        cls.family = cls.adapter.selector_g1_load_family()
        cls.catalog = cls.family.selector_g1_catalog(cls.adapter)

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='selector-g1-offline-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def hook(self, name):
        self.assertIsNotNone(self.family, 'Complete family integration is absent')
        self.assertTrue(callable(getattr(self.family, name, None)), name + ' is absent')
        return getattr(self.family, name)

    def test_exact_catalog_is_code_owned(self):
        self.catalog = self.hook('selector_g1_catalog')(self.adapter)
        self.assertEqual(set(self.catalog['families']), {'selector', 'g1', 'g1-review'})
        self.assertEqual([len(self.catalog['families'][f]['contract']['stages']) for f in ('selector', 'g1', 'g1-review')], [15, 120, 15])

    def test_variant_source_binding_refuses_invented_original_owner(self):
        check = self.hook('selector_g1_check_binding')
        owner = {'owner': {'original_sha256': 'a' * 64, 'public_sha256': 'a' * 64}}
        check(self.adapter, {'kind': 'ORIGINAL_SOURCE', 'source_id': 'owner', 'source_sha256': 'a' * 64}, owner)
        with self.assertRaises(ValueError):
            check(self.adapter, {'kind': 'ORIGINAL_SOURCE', 'source_id': 'invented', 'source_sha256': 'a' * 64}, owner)

    def test_variant_generated_binding_keeps_owner_and_generated_digest_separate(self):
        check = self.hook('selector_g1_check_binding')
        owner = {'owner': {'original_sha256': 'a' * 64, 'public_sha256': 'a' * 64}}
        value = {'kind': 'GENERATED_BY_ORIGINAL', 'source_id': 'owner', 'source_sha256': 'a' * 64, 'generated_sha256': 'b' * 64, 'derivation_id': 'AllReceiptsRemoved-CertificateSyntax'}
        check(self.adapter, value, owner)
        bad = dict(value, source_sha256='b' * 64)
        with self.assertRaises(ValueError):
            check(self.adapter, bad, owner)

    def test_binding_unknown_fields_fail_closed(self):
        check = self.hook('selector_g1_check_binding')
        with self.assertRaises(ValueError):
            check(self.adapter, {'kind': 'TOOL_PROBE', 'tool_name': 'lean', 'executable_sha256': 'a' * 64, 'driver_sha256': 'b' * 64, 'formal_credit': True}, {})

    def test_inherited_stdout_has_terminal_without_fabricated_child_log(self):
        capture = self.hook('selector_g1_capture_call')
        trace = self.root / 'trace'
        trace.mkdir()
        event = {'id': 'preflight', 'profile': 'INHERITED_STDOUT_CHECK', 'readonly': True, 'source_binding': {'kind': 'ORIGINAL_SOURCE', 'source_id': 'driver', 'source_sha256': 'a' * 64}}
        argv = [sys.executable, '--version']
        calls = []

        def original(given, **kw):
            calls.append((given, kw))
            return subprocess.CompletedProcess(given, 0, None, None)
        result = capture(self.adapter, original, trace, 0, event, argv, {'check': True})
        self.assertEqual(calls, [(argv, {'check': True})])
        self.assertEqual(result.returncode, 0)
        row = self.adapter.read_json(trace / '0000.json')
        self.assertEqual(row['terminal'], 'COMPLETED')
        self.assertIsNone(row['log_sha256'])
        self.assertEqual(row['capture_kind'], 'INHERITED_PARENT_STDOUT')
        self.assertFalse((trace / '0000.log').exists())

    def test_preflight_failure_is_captured_and_reraised(self):
        capture = self.hook('selector_g1_capture_call')
        trace = self.root / 'trace'
        trace.mkdir()
        event = {'id': 'preflight', 'profile': 'INHERITED_STDOUT_CHECK', 'readonly': True, 'source_binding': {'kind': 'ORIGINAL_SOURCE', 'source_id': 'driver', 'source_sha256': 'a' * 64}}

        def original(argv, **kw):
            raise subprocess.CalledProcessError(1, argv)
        with self.assertRaises(subprocess.CalledProcessError):
            capture(self.adapter, original, trace, 0, event, ['python', '--verify-only'], {'check': True})
        self.assertEqual(self.adapter.read_json(trace / '0000.json')['exit_code'], 1)
        self.assertFalse((trace / '0000.log').exists())

    def test_file_capture_preserves_original_handle_and_return(self):
        capture = self.hook('selector_g1_capture_call')
        trace = self.root / 'trace'
        trace.mkdir()
        event = {'id': 'finite', 'capture': 'FILE', 'readonly': False, 'source_binding': {'kind': 'ORIGINAL_SOURCE', 'source_id': 'finite', 'source_sha256': 'a' * 64}}
        with (self.root / 'source.log').open('w') as stream:

            def original(argv, **kw):
                self.assertIs(kw['stdout'], stream)
                stream.write('original finite output\n')
                return subprocess.CompletedProcess(argv, 0, None, None)
            result = capture(self.adapter, original, trace, 0, event, ['python', 'finite.py'], {'stdout': stream, 'stderr': subprocess.STDOUT, 'timeout': 60})
            self.assertIsNone(result.stdout)
        self.assertEqual((trace / '0000.log').read_bytes(), b'original finite output\n')

    def test_timeout_remains_inconclusive_and_partial_log_is_retained(self):
        capture = self.hook('selector_g1_capture_call')
        trace = self.root / 'trace'
        trace.mkdir()
        event = {'id': 'compile', 'profile': 'LEAN_PIPE', 'readonly': False, 'source_binding': {'kind': 'ORIGINAL_SOURCE', 'source_id': 'proof', 'source_sha256': 'a' * 64}}

        def original(argv, **kw):
            raise subprocess.TimeoutExpired(argv, 180, output=b'partial')
        with self.assertRaises(subprocess.TimeoutExpired):
            capture(self.adapter, original, trace, 0, event, ['lean', 'proof.lean'], {'stdout': subprocess.PIPE, 'stderr': subprocess.STDOUT, 'text': True, 'timeout': 180})
        row = self.adapter.read_json(trace / '0000.json')
        self.assertEqual(row['terminal'], 'TIMEOUT')
        self.assertIsNone(row['exit_code'])
        self.assertEqual((trace / '0000.log').read_bytes(), b'partial')

    def test_boolean_exit_is_not_a_successful_terminal(self):
        capture = self.hook('selector_g1_capture_call')
        trace = self.root / 'trace'
        trace.mkdir()
        event = {'id': 'compile', 'profile': 'LEAN_PIPE', 'readonly': False, 'source_binding': {'kind': 'ORIGINAL_SOURCE', 'source_id': 'proof', 'source_sha256': 'a' * 64}}

        def original(argv, **kw):
            return subprocess.CompletedProcess(argv, False, '')
        with self.assertRaises(ValueError):
            capture(self.adapter, original, trace, 0, event, ['lean'], {'stdout': subprocess.PIPE, 'text': True})

    def test_actual_synthetic_child_keeps_argv_terminal_and_raw_stdout(self):
        capture = self.hook('selector_g1_capture_call')
        trace = self.root / 'trace'
        trace.mkdir()
        event = {'id': 'fixture-child', 'profile': 'LEAN_PIPE', 'readonly': False, 'source_binding': {'kind': 'ORIGINAL_SOURCE', 'source_id': 'fixture', 'source_sha256': 'a' * 64}}
        argv = [sys.executable, '-I', '-S', '-B', '-c', 'print("synthetic real child")']
        result = capture(self.adapter, subprocess.run, trace, 0, event, argv, {'stdout': subprocess.PIPE, 'stderr': subprocess.STDOUT, 'text': True, 'timeout': 5})
        row = self.adapter.read_json(trace / '0000.json')
        self.assertEqual(result.returncode, 0)
        self.assertEqual(row['argv'], argv)
        self.assertEqual(row['exit_code'], 0)
        self.assertEqual((trace / '0000.log').read_text(), 'synthetic real child\n')

    def test_actual_inherited_stdout_child_failure_keeps_no_separate_log(self):
        capture = self.hook('selector_g1_capture_call')
        trace = self.root / 'trace'
        trace.mkdir()
        event = {'id': 'fixture-preflight', 'profile': 'INHERITED_STDOUT_CHECK', 'readonly': True, 'source_binding': {'kind': 'ORIGINAL_SOURCE', 'source_id': 'fixture', 'source_sha256': 'a' * 64}}
        argv = [sys.executable, '-I', '-S', '-B', '-c', 'raise SystemExit(7)']
        with self.assertRaises(subprocess.CalledProcessError):
            capture(self.adapter, subprocess.run, trace, 0, event, argv, {'check': True})
        self.assertEqual(self.adapter.read_json(trace / '0000.json')['exit_code'], 7)
        self.assertFalse((trace / '0000.log').exists())

    def test_audit_target_names_are_root_qualified(self):
        body = self.hook('selector_g1_audit_source')(self.adapter, [{'target_id': 't', 'module': 'M', 'name': 'OrthemicCertificate.check_sound'}])
        self.assertIn('#check @_root_.OrthemicCertificate.check_sound', body)
        self.assertIn('`OrthemicCertificate.check_sound', body)
        self.assertNotIn('`_root_.OrthemicCertificate.check_sound', body)
        self.assertIn('scheduled', body)

    def test_historical_v2_g1_cannot_satisfy_reuse_gate(self):
        gate = self.hook('selector_g1_dependency_identity')
        with self.assertRaises(ValueError):
            gate(self.adapter, 'g1-review', {'outcome': 'QUALIFIED_DECLARED_SUITE', 'replay_evidence': {'schema': 'orthemology-v5-replay-evidence-v2'}}, {}, {}, self.root)

    def test_failed_only_core_cannot_satisfy_selector_gate(self):
        gate = self.hook('selector_g1_dependency_identity')
        with self.assertRaises(ValueError):
            gate(self.adapter, 'selector', {'outcome': 'FAILED', 'replay_evidence': {}}, {}, {}, self.root)

    def test_all_three_families_have_execution_and_receipt_dispatch(self):
        for name in ('selector_g1_validate_suite', 'selector_g1_execute', 'selector_g1_validate_receipt', 'selector_g1_trace_main', 'selector_g1_collect'):
            self.hook(name)


def operational_evidence_fixture(a, packet):
    owner = a._OPERATIONAL_DATA['packets'][packet]
    suite = a._OPERATIONAL_DATA['descriptors'][owner['suite_id']]
    stages = {r['id']: copy.deepcopy(r) for r in suite['replay']['stages']}
    base = datetime(2026, 10, 5, tzinfo=timezone.utc)
    def tm(second): return (base + timedelta(seconds=second)).isoformat().replace('+00:00', 'Z')
    parent = {'terminal': 'COMPLETED', 'exit_code': 0, 'started_at': tm(100), 'ended_at': tm(1000), 'log_sha256': 'a' * 64}
    executed = {'original-driver': parent}; ledger = []; outputs = {}; observations = []
    for index, spec in enumerate(a.operational_physical_specs(packet)):
        start, end = 110 + index * 2, 111 + index * 2
        if spec['id'] == 'source-component': end = 240
        if packet == 't08-batch' and spec['parent_process_id'] is None and spec['id'] != 'source-component':
            start, end = 250 + index * 2, 251 + index * 2
        hashes = {name.removeprefix('{out}/'): a.sha(('synthetic-' + name).encode()) for name in spec['output_paths']}
        row = {'physical_id': spec['id'], 'source_binding': spec['source_binding'], 'source_argv': spec['source_argv'],
            'argv': spec['argv'], 'cwd': spec['cwd'], 'started_at': tm(start), 'ended_at': tm(end), 'terminal': 'COMPLETED',
            'exit_code': spec['expected_exit'], 'log_sha256': a.sha(('synthetic-' + spec['id']).encode()), 'output_hashes': hashes,
            'capture_sha256': a.sha(('synthetic-capture-' + spec['id']).encode()), 'log_assembly': spec['log_assembly'], 'parent_process_id': spec['parent_process_id']}
        ledger.append(row); outputs.update(hashes)
    helpers = []
    for index, hid in enumerate(owner['helper_ids']):
        hashes = {name: 'b' * 64 for name in stages[hid]['output_paths']}
        actual = {'started_at': tm(index * 2), 'ended_at': tm(index * 2 + 1), 'terminal': 'COMPLETED', 'exit_code': 0,
            'log_sha256': 'c' * 64, 'output_hashes': hashes}
        executed[hid] = actual; outputs.update(hashes)
        helpers.append({**a.operational_helper_spec(hid), **actual})
    invocation = {'parent_stage_id': 'original-driver', 'driver_sha256': owner['driver']['sha256'],
        'source_argv': stages['original-driver']['argv'], 'launch_argv': a.operational_tracer_argv(stages['original-driver'], packet),
        'launch_cwd': '{archive:source-archive}', 'runner_sha256': 'd' * 64, 'trace_sha256': 'e' * 64,
        'parent_log_sha256': parent['log_sha256'], 'child_count': len(ledger), 'physical_children': ledger,
        'helper_invocations': helpers, 'original_receipt_sha256': 'f' * 64}
    for index, (sid, stage) in enumerate(stages.items()):
        if stage['argv'][0] != '{builtin:observe-child}': continue
        row = next(r for r in ledger if r['physical_id'] == stage['argv'][2])
        executed[sid] = {'terminal': row['terminal'], 'exit_code': row['exit_code'], 'log_sha256': row['log_sha256'],
            'started_at': tm(1010 + index), 'ended_at': tm(1011 + index)}
        observations.append({'stage_id': sid, 'source_child_id': row['physical_id'], 'parent_stage_id': 'original-driver',
            'driver_sha256': owner['driver']['sha256'], 'parser_id': owner['recipe'], 'mode': 'NONEXECUTING_OBSERVATION',
            'argv_provenance': 'CAPTURED', **{k: row[k] for k in ('argv', 'cwd', 'started_at', 'ended_at', 'terminal', 'exit_code',
                'log_sha256', 'source_binding', 'output_hashes', 'log_assembly')}, 'observed_at': tm(1011 + index),
            'physical_run_sha256': 'e' * 64, 'parent_log_sha256': parent['log_sha256'], 'actual_outcome': 'ACCEPT' if row['exit_code'] == 0 else 'REJECT',
            'result_record_sha256': 'a' * 64, 'physical_record_sha256': a.canonical(row)})
    evidence = {'driver_invocations': [invocation], 'child_observations': observations, 'runner_sha256': 'd' * 64, 'output_hashes': outputs}
    return evidence, {'operational_packet': packet, 'stages': stages, 'drivers': {'original': suite['replay']['drivers'][0]}}, executed


import signal
import time
from datetime import datetime, timedelta, timezone

class SharedProcessCleanupTests(unittest.TestCase):
    """A stopped leader cannot conceal a still-running process-group child."""
    CHILD = "import json,os,pathlib,signal,sys,time; signal.signal(signal.SIGTERM,signal.SIG_IGN); pathlib.Path(sys.argv[1]).write_text(json.dumps({'pid':os.getpid(),'pgid':os.getpgrp()})); time.sleep(60)"
    LEADER = "import subprocess,sys,time; subprocess.Popen([sys.executable,'-I','-S','-B','-c',sys.argv[1],sys.argv[2]]); time.sleep(60)"
    INVOKER = '''import importlib.util,json,os,pathlib,signal,sys
def stop(signum,frame): raise KeyboardInterrupt('Synthetic outer interruption')
signal.signal(signal.SIGTERM,stop)
spec=importlib.util.spec_from_file_location('cleanup_fixture_adapter',sys.argv[1]);api=importlib.util.module_from_spec(spec);spec.loader.exec_module(api)
out=pathlib.Path(sys.argv[2])
argv=[sys.executable,'-I','-S','-B','-c',sys.argv[3],sys.argv[4],str(out/'child.json')]
result=api.run_process(argv,out,dict(os.environ),out/'stage.log',60)
(out/'result.json').write_text(json.dumps(result))
'''

    def setUp(self):
        if os.name != 'posix' or not Path('/proc').is_dir():
            self.skipTest('Actual POSIX process-group fixture requires /proc')
        self.tmp = tempfile.TemporaryDirectory(prefix='shared-cleanup-fixture-')
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        spec = importlib.util.spec_from_file_location('shared_cleanup_tests', SCRIPT)
        self.r = importlib.util.module_from_spec(spec); spec.loader.exec_module(self.r)

    def live(self, pid):
        try: value = (Path('/proc') / str(pid) / 'stat').read_text()
        except FileNotFoundError: return False
        return value[value.rfind(')') + 2:].split()[0] not in {'Z', 'X'}

    def gone(self, pid, seconds=1):
        deadline = time.monotonic() + seconds
        while self.live(pid) and time.monotonic() < deadline: time.sleep(.01)
        return not self.live(pid)

    def cleanup(self, child):
        if child is not None and self.live(child['pid']):
            try: os.killpg(child['pgid'], signal.SIGKILL)
            except ProcessLookupError: pass
            self.assertTrue(self.gone(child['pid'], 3), 'Fixture-owned cleanup failed')

    def test_timeout_stops_term_ignoring_descendant_after_leader_exits(self):
        child = None
        try:
            result = self.r.run_process([sys.executable, '-I', '-S', '-B', '-c', self.LEADER, self.CHILD, str(self.root/'child.json')], self.root, dict(os.environ), self.root/'stage.log', .6)
            child = json.loads((self.root/'child.json').read_bytes())
            self.assertEqual(result['terminal'], 'TIMEOUT'); self.assertIsNone(result['exit_code'])
            self.assertTrue(self.gone(child['pid']), 'TERM-ignoring descendant survived timeout cleanup')
        finally: self.cleanup(child)

    def test_outer_interrupt_stops_descendant_before_invoker_terminal(self):
        proc = None; child = None
        try:
            proc = subprocess.Popen([sys.executable, *(['-O'] if sys.flags.optimize else []), '-I', '-S', '-B', '-c', self.INVOKER, str(SCRIPT), str(self.root), self.LEADER, self.CHILD], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
            deadline = time.monotonic() + 8
            while not (self.root/'child.json').exists() and proc.poll() is None and time.monotonic() < deadline: time.sleep(.02)
            self.assertTrue((self.root/'child.json').exists(), 'Synthetic child did not become ready')
            child = json.loads((self.root/'child.json').read_bytes()); started = time.monotonic()
            os.killpg(proc.pid, signal.SIGTERM)
            text, _ = proc.communicate(timeout=5)
            self.assertEqual(proc.returncode, 0, text.decode(errors='replace'))
            result = json.loads((self.root/'result.json').read_bytes())
            self.assertEqual(result['terminal'], 'INTERRUPTED'); self.assertIsNone(result['exit_code'])
            self.assertLess(time.monotonic()-started, 5)
            self.assertTrue(self.gone(child['pid']), 'TERM-ignoring descendant survived invoker terminal')
        finally:
            if proc is not None and proc.poll() is None:
                os.killpg(proc.pid, signal.SIGKILL); proc.communicate(timeout=3)
            self.cleanup(child)

    def test_completed_child_keeps_real_terminal_and_output(self):
        result = self.r.run_process([sys.executable, '-I', '-S', '-B', '-c', 'print("completed fixture")'], self.root, dict(os.environ), self.root/'stage.log', 3)
        self.assertEqual(result['terminal'], 'COMPLETED'); self.assertEqual(result['exit_code'], 0)
        self.assertEqual((self.root/'stage.log').read_text(), 'completed fixture\n')

    def test_stdin_timeout_stops_term_ignoring_descendant(self):
        child = None
        stdin = self.root/'input.txt'; stdin.write_text('synthetic input\n')
        try:
            result = self.r._t15_reference_input_process([sys.executable, '-I', '-S', '-B', '-c', self.LEADER, self.CHILD, str(self.root/'child.json')], self.root, dict(os.environ), self.root/'stage.log', .6, stdin)
            child = json.loads((self.root/'child.json').read_bytes())
            self.assertEqual(result['terminal'], 'TIMEOUT'); self.assertIsNone(result['exit_code'])
            self.assertTrue(self.gone(child['pid']), 'TERM-ignoring descendant survived stdin timeout cleanup')
        finally: self.cleanup(child)

class D04NegativeProofHoleDiagnosticsTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('d04_negative_diagnostic_tests', SCRIPT)
        self.r = importlib.util.module_from_spec(spec); spec.loader.exec_module(self.r)
        self.spec = {'id':'synthetic-negative', 'argv':['lean','Control.lean'], 'cwd':'/synthetic',
            'timeout_seconds':180, 'capture':'MERGED_TEXT', 'stdin':'INHERITED_NO_INPUT',
            'outputs':[], 'expected_exit_code':1, 'required_diagnostics':['type mismatch'], 'forbidden_diagnostics':[]}
        self.log = b"error: type mismatch\n'Fixture.rejected' depends on axioms: [sorryAx]\n"
        self.parent = {'started_at':'2026-10-05T00:00:00Z','ended_at':'2026-10-05T00:00:04Z'}
        self.row = {'id':self.spec['id'], 'argv':self.spec['argv'], 'cwd':self.spec['cwd'],
            'timeout_seconds':180,'capture':'MERGED_TEXT','stdin':{'mode':'INHERITED_NO_INPUT','data_sha256':None},
            'started_at':'2026-10-05T00:00:01Z','ended_at':'2026-10-05T00:00:02Z',
            'terminal':'COMPLETED','exit_code':1,'log_sha256':self.r.sha(self.log),'output_hashes':{}}

    def assess(self, log=None):
        log = self.log if log is None else log
        self.row['log_sha256'] = self.r.sha(log)
        return self.r.d04_assess_captured_child(self.spec,self.row,log,self.parent)

    def test_failed_compiler_fixture_keeps_intended_rejection(self):
        self.assertEqual(self.assess(), {'outcome':'REJECT','rejection_credit':True})

    def test_successful_child_cannot_claim_proof_with_sorry_axiom(self):
        self.spec.update(expected_exit_code=0,required_diagnostics=[]); self.row['exit_code']=0
        with self.assertRaisesRegex(ValueError,'proof hole'): self.assess()

    def test_hole_literal_does_not_replace_required_rejection_diagnostic(self):
        with self.assertRaisesRegex(ValueError,'intended control diagnostic'): self.assess(b"'Fixture.rejected' depends on axioms: [sorryAx]\n")

    def test_negative_infrastructure_failure_is_still_refused(self):
        with self.assertRaisesRegex(ValueError,'infrastructure failure'): self.assess(self.log+b'unknown constant Fixture.missing\n')

    def test_resource_output_never_becomes_rejection(self):
        self.assertEqual(self.assess(self.log+b'out of memory\n'), {'outcome':'RESOURCE_INCONCLUSIVE','rejection_credit':False})

class RemainingDispatchBoundaryTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('remaining_dispatch_tests', SCRIPT)
        self.r = importlib.util.module_from_spec(spec); spec.loader.exec_module(self.r)

    def test_malformed_suite_is_rejected_by_schema_gate(self):
        for suite in (None, [], 1, 'invalid', {'replay':None}, {'replay':[]}, {'replay':1}):
            with self.subTest(suite=suite), self.assertRaises(ValueError):
                self.r.validate_suite(suite, {}, Path('.'))

    def test_malformed_receipt_does_not_enter_new_families(self):
        for receipt in (None, [], 1, {'replay_evidence':None}, {'replay_evidence':[]}):
            with self.subTest(receipt=receipt), self.assertRaises(ValueError):
                self.r.validate_receipt(receipt, {}, {}, Path('.'))

class OperationalProtocolTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('operational_public_controls', SCRIPT)
        cls.r = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.r)

    def test_complete_physical_plans_keep_noncredit_children(self):
        expected = {'t08-common': 48, 't08-batch': 74, 't08-shared': 48,
                    't08-controller': 40, 't09-controller': 70, 't09-transport': 38}
        for packet, count in expected.items():
            with self.subTest(packet=packet):
                rows = self.r.operational_physical_specs(packet)
                self.assertEqual(len(rows), count)
                self.assertEqual(len({r['id'] for r in rows}), count)
                self.assertTrue(any(r['source_binding']['kind'] == 'TOOL_PROBE' for r in rows))

    def test_batch_generated_audit_binds_nested_generator(self):
        rows = self.r.operational_physical_specs('t08-batch')
        row = next(r for r in rows if r['id'] == 'fresh science/AllNamedDeclarations')
        self.assertEqual(row['source_binding']['kind'], 'GENERATED_BY_ORIGINAL')
        self.assertEqual(row['source_binding']['source_sha256'], '276a9b4f7d8b304b4c553a28a029dfb006c6b0475b7a316a77467897d37b8731')
        owner = next(r for r in rows if r['id'] == 'source-component')
        self.assertEqual(owner['source_binding']['kind'], 'ARCHIVE_MEMBER')

    def test_t09_keeps_inherited_cwd_and_no_j1(self):
        rows = self.r.operational_physical_specs('t09-controller')
        for row in rows:
            self.assertNotIn('-j1', row['source_argv'])
            self.assertEqual(row['cwd'], '{archive:source-archive}')

    def test_changed_bound_source_rejected(self):
        row = copy.deepcopy(self.r.operational_physical_specs('t08-common')[1])
        row['source_binding']['source_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'binding'):
            self.r.operational_validate_source_binding('t08-common', row['id'], row['source_binding'])

    def test_helper_partial_unittest_is_rejected(self):
        config = self.r._OPERATIONAL_DATA['helpers']['t08-common-helper-1']
        text = '\n'.join(name + ' (__main__.Probe) ... ok' for name in config['unittest_names'][:-1])
        text += '\nRan 11 tests in 0.1s\n\nOK\n'
        with self.assertRaises(ValueError):
            self.r.operational_check_helper('t08-common-helper-1', text, None, None)

    def test_helper_complete_source_owned_unittest_names(self):
        config = self.r._OPERATIONAL_DATA['helpers']['t08-common-helper-1']
        text = '\n'.join(name + ' (__main__.Probe) ... ok' for name in config['unittest_names'])
        text += '\nRan 12 tests in 0.1s\n\nOK\n'
        self.r.operational_check_helper('t08-common-helper-1', text, None, None)

    def test_helper_probe_does_not_gain_mutation_credit(self):
        config = self.r._OPERATIONAL_DATA['helpers']['t08-controller-helper-1']
        self.assertEqual(config['stage']['control_ids'], [])
        self.assertEqual(config['max_compiler_processes'], 0)

class OperationalCaptureBindingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('operational_public_controls', SCRIPT)
        cls.r = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.r)

    def setUp(self):
        self.packet = 't09-controller'
        self.spec = self.r.operational_physical_specs(self.packet)[1]
        self.parent = {'started_at': '2026-10-05T01:00:00Z', 'ended_at': '2026-10-05T01:01:00Z', 'terminal': 'COMPLETED', 'exit_code': 0}
        self.row = {'physical_id': self.spec['id'], 'source_binding': self.spec['source_binding'],
            'source_argv': self.spec['source_argv'], 'argv': self.spec['argv'], 'cwd': self.spec['cwd'],
            'started_at': '2026-10-05T01:00:01Z', 'ended_at': '2026-10-05T01:00:02Z',
            'terminal': 'COMPLETED', 'exit_code': 0, 'log_sha256': self.r.sha(b''),
            'output_hashes': {p.removeprefix('{out}/'): 'a' * 64 for p in self.spec['output_paths']},
            'capture_sha256': 'b' * 64, 'log_assembly': self.spec['log_assembly'],
            'parent_process_id': self.spec['parent_process_id']}

    def test_exact_measured_child_is_accepted(self):
        self.r.operational_validate_physical_row(self.packet, self.row, self.parent, True)

    def test_fabricated_time_is_rejected(self):
        self.row['started_at'] = self.parent['ended_at']
        with self.assertRaises(ValueError): self.r.operational_validate_physical_row(self.packet, self.row, self.parent, True)

    def test_original_cwd_is_not_project_cwd(self):
        self.row['cwd'] = '{project}'
        with self.assertRaises(ValueError): self.r.operational_validate_physical_row(self.packet, self.row, self.parent, True)

    def test_missing_capture_hash_is_not_physical_evidence(self):
        self.row['capture_sha256'] = None
        with self.assertRaises(ValueError): self.r.operational_validate_physical_row(self.packet, self.row, self.parent, True)

    def test_changed_object_census_is_rejected(self):
        self.row['output_hashes'] = {}
        with self.assertRaises(ValueError): self.r.operational_validate_physical_row(self.packet, self.row, self.parent, True)

    def test_timeout_retained_but_never_completed_credit(self):
        self.row.update(terminal='TIMEOUT', exit_code=None, output_hashes={})
        self.r.operational_validate_physical_row(self.packet, self.row, self.parent, False)
        with self.assertRaises(ValueError): self.r.operational_validate_physical_row(self.packet, self.row, self.parent, True)

    def test_probe_cannot_emit_custom_object(self):
        spec = self.r.operational_physical_specs(self.packet)[0]
        self.row.update(physical_id=spec['id'], source_binding=spec['source_binding'], source_argv=spec['source_argv'], argv=spec['argv'])
        with self.assertRaises(ValueError): self.r.operational_validate_physical_row(self.packet, self.row, self.parent, True)

    def test_parent_failure_cannot_qualify_observations(self):
        self.parent['exit_code'] = 1
        with self.assertRaises(ValueError): self.r.operational_validate_physical_row(self.packet, self.row, self.parent, True)

class OperationalEvidenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec = importlib.util.spec_from_file_location('operational_public_controls', SCRIPT)
        cls.r = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cls.r)

    def test_complete_synthetic_receipt_grammar_all_six(self):
        for packet in self.r._OPERATIONAL_DATA['packets']:
            with self.subTest(packet=packet): self.r.operational_validate_child_evidence(*operational_evidence_fixture(self.r, packet), True)
    def test_missing_version_probe_rejected(self):
        e, p, s = operational_evidence_fixture(self.r, 't09-controller'); e['driver_invocations'][0]['physical_children'].pop(0); e['driver_invocations'][0]['child_count'] -= 1
        with self.assertRaises(ValueError): self.r.operational_validate_child_evidence(e, p, s, True)
    def test_helper_cannot_be_omitted(self):
        e, p, s = operational_evidence_fixture(self.r, 't08-common'); e['driver_invocations'][0]['helper_invocations'].pop()
        with self.assertRaises(ValueError): self.r.operational_validate_child_evidence(e, p, s, True)
    def test_helper_later_than_parent_rejected(self):
        e, p, s = operational_evidence_fixture(self.r, 't08-controller'); h = e['driver_invocations'][0]['helper_invocations'][0]
        h['ended_at'] = s[h['stage_id']]['ended_at'] = s['original-driver']['ended_at']
        with self.assertRaises(ValueError): self.r.operational_validate_child_evidence(e, p, s, True)
    def test_same_child_cannot_supply_two_observers(self):
        e, p, s = operational_evidence_fixture(self.r, 't08-common'); e['child_observations'][1]['source_child_id'] = e['child_observations'][0]['source_child_id']
        with self.assertRaises(ValueError): self.r.operational_validate_child_evidence(e, p, s, True)
    def test_nested_parent_is_not_an_extra_scientific_observer(self):
        e, p, s = operational_evidence_fixture(self.r, 't08-batch'); e['child_observations'][0]['source_child_id'] = 'source-component'
        with self.assertRaises(ValueError): self.r.operational_validate_child_evidence(e, p, s, True)
    def test_wrong_record_link_is_rejected(self):
        e, p, s = operational_evidence_fixture(self.r, 't08-shared'); e['child_observations'][-1]['physical_record_sha256'] = '0' * 64
        with self.assertRaises(ValueError): self.r.operational_validate_child_evidence(e, p, s, True)
    def test_old_controller_wrapper_count_cannot_be_minted(self):
        e, p, s = operational_evidence_fixture(self.r, 't08-controller'); e['driver_invocations'][0]['inherited_wrapper_tests_replayed'] = 23
        with self.assertRaises(ValueError): self.r.operational_validate_child_evidence(e, p, s, True)
    def test_serial_children_cannot_overlap(self):
        e, p, s = operational_evidence_fixture(self.r, 't09-transport'); rows = e['driver_invocations'][0]['physical_children']
        rows[1]['started_at'] = rows[0]['started_at']
        observed = next(r for r in e['child_observations'] if r['source_child_id'] == rows[1]['physical_id'])
        observed['started_at'] = rows[1]['started_at']; observed['physical_record_sha256'] = self.r.canonical(rows[1])
        with self.assertRaises(ValueError): self.r.operational_validate_child_evidence(e, p, s, True)


class RemainingReviewedDispatchTests(unittest.TestCase):
    def setUp(self):
        spec = importlib.util.spec_from_file_location('reviewed_dispatch', SCRIPT)
        self.r = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.r)

    def test_unhashable_suite_identity_reaches_schema_gate(self):
        for identity in ([], {}):
            with self.subTest(identity=identity), self.assertRaises(ValueError):
                self.r.validate_suite({'id': identity, 'replay': {}}, {}, Path('.'))

    def test_unhashable_driver_recipe_reaches_schema_gate(self):
        for recipe in ([], {}):
            with self.subTest(recipe=recipe), self.assertRaises(ValueError):
                self.r.validate_suite({'id': 'fixture', 'replay': {'drivers': [{'recipe': recipe}]}}, {}, Path('.'))

    def test_missing_operational_identity_does_not_bypass_schema_refusal(self):
        with self.assertRaises(ValueError):
            self.r.execute_suite({'replay': {'drivers': []}}, {}, Path('.'), Path('uncreated-output'), {}, {})


if __name__ == '__main__':
    unittest.main(verbosity=2)
