"""Adversarial boundaries for the source-bound successor replay interface."""
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
