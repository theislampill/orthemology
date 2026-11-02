"""Artificial hosted-coordinate and protected-metadata refusal controls."""
from pathlib import Path
from unittest.mock import patch
import os
import pathlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
import ast
import re
import shutil
import types

import source_alias_absence_boundary as boundary
import check_source_alias_absence as runner


class HostedCoordinatesControls(unittest.TestCase):
    def setUp(self):
        self.area = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.repo = self.area / 'checkout'; self.repo.mkdir()
        (self.repo / '.git').mkdir()
        self.temporary = self.area / 'runner-temp'; self.temporary.mkdir()
        self.state = self.temporary / 'r0002-source-alias-absence'
        self.head = 'a' * 40
        self.env = {'GITHUB_ACTIONS': 'true', 'GITHUB_REPOSITORY': 'theislampill/orthemology',
                    'GITHUB_WORKSPACE': str(self.repo), 'RUNNER_TEMP': str(self.temporary),
                    'GITHUB_SHA': self.head, 'GITHUB_RUN_ID': '123', 'GITHUB_RUN_ATTEMPT': '1',
                    'GITHUB_EVENT_NAME': 'pull_request', 'RUNNER_OS': 'Linux'}

    def admit(self, **changes):
        env = dict(self.env, **changes)
        return boundary.validate_hosted_coordinates(self.repo, self.state, env,
                                                     self.head, self.repo, fresh=True)

    def test_exact_artificial_hosted_coordinates(self):
        result = self.admit()
        self.assertEqual(result['head'], self.head)
        self.assertEqual(result['state'], str(self.state))

    def test_local_or_other_repository_refuses(self):
        for change in ({'GITHUB_ACTIONS': 'false'}, {'GITHUB_REPOSITORY': 'other/repo'},
                       {'GITHUB_EVENT_NAME': 'workflow_dispatch'}, {'RUNNER_OS': 'Windows'}):
            with self.subTest(change=change), self.assertRaises(RuntimeError):
                self.admit(**change)

    def test_commit_and_workspace_mismatch_refuse(self):
        for change in ({'GITHUB_SHA': 'b' * 40}, {'GITHUB_WORKSPACE': str(self.temporary)},
                       {'GITHUB_RUN_ID': ''}, {'GITHUB_RUN_ATTEMPT': '0'}):
            with self.subTest(change=change), self.assertRaises(RuntimeError):
                self.admit(**change)

    def test_existing_state_refuses_new_run(self):
        self.state.mkdir()
        with self.assertRaises(RuntimeError): self.admit()

    def test_output_inside_checkout_or_symlink_refuses(self):
        self.state = self.repo / 'r0002-source-alias-absence'
        with self.assertRaises(RuntimeError): self.admit(RUNNER_TEMP=str(self.repo))
        link = self.area / 'temp-link'; link.symlink_to(self.temporary, target_is_directory=True)
        self.state = link / 'r0002-source-alias-absence'
        with self.assertRaises(RuntimeError): self.admit(RUNNER_TEMP=str(link))


class ProtectedMetadataControls(unittest.TestCase):
    def setUp(self):
        self.repo = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.originals, self.stage, self.manifest = {}, {}, {}
        for n, relative in enumerate(boundary.PROTECTED_PATHS):
            path = self.repo / relative; path.parent.mkdir(parents=True)
            path.write_bytes(b'artificial-held-fixture'); path.chmod(0o644)
            oid = f'{n + 1:040x}'
            self.originals[relative] = ('100644', 'blob', oid, path.stat().st_size)
            self.stage[relative] = ('100644', oid)
            self.manifest[relative] = Path(relative).parent.name

    def derive(self):
        return boundary.derive_held_metadata(self.repo, self.originals, self.stage, self.manifest)

    def test_metadata_only_one_checkout_population(self):
        with patch.object(Path, 'read_bytes', side_effect=AssertionError('Body read is forbidden')):
            rows = self.derive()
        self.assertEqual(len(rows), 5)
        self.assertEqual({r['path'] for r in rows}, set(boundary.PROTECTED_PATHS))
        self.assertEqual({r['sha256'] for r in rows}, set(self.manifest.values()))

    def test_manifest_or_staged_identity_mismatch_refuses(self):
        path = boundary.PROTECTED_PATHS[0]
        self.manifest[path] = 'f' * 64
        with self.assertRaises(RuntimeError): self.derive()
        self.manifest[path] = Path(path).parent.name
        self.stage[path] = ('100644', 'f' * 40)
        with self.assertRaises(RuntimeError): self.derive()

    def test_unexcluded_stage_alias_refuses(self):
        self.stage['unexpected-alias'] = self.stage[boundary.PROTECTED_PATHS[0]]
        with self.assertRaises(RuntimeError): self.derive()

    def test_second_link_or_symlink_refuses(self):
        original = self.repo / boundary.PROTECTED_PATHS[0]
        os.link(original, self.repo / 'extra-link')
        with self.assertRaises(RuntimeError): self.derive()
        (self.repo / 'extra-link').unlink()
        original.unlink(); original.symlink_to(self.repo / boundary.PROTECTED_PATHS[1])
        with self.assertRaises(RuntimeError): self.derive()


class AuthenticatedHelperControls(unittest.TestCase):
    def setUp(self):
        self.area = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.repo = self.area / 'checkout'; self.repo.mkdir()
        self.relative = runner.PUBLIC_HELPERS['boundary.py']
        self.helper = self.repo / self.relative
        self.helper.parent.mkdir(parents=True)
        self.helper.write_text('VALUE = 7\n'); self.helper.chmod(0o644)
        self.marker = self.area / 'unexecuted-marker'
        self.git('init', '-q')
        self.git('add', '--', self.relative)
        self.git('-c', 'user.name=Artificial Fixture', '-c', 'user.email=fixture@example.invalid',
                 'commit', '-qm', 'Synthetic authenticated helper')

    def git(self, *args):
        return subprocess.check_output(['git', '-c', 'core.hooksPath=/dev/null', *args],
                                       cwd=self.repo, stderr=subprocess.DEVNULL,
                                       env=dict(os.environ, GIT_OPTIONAL_LOCKS='0'))

    def changed_body(self):
        return ('from pathlib import Path\nPath(' + repr(str(self.marker)) +
                ').write_text("unexpected")\nVALUE = 8\n').encode()

    def test_public_helper_identity_precedes_execution(self):
        good = runner.checkout_module(self.repo, 'boundary.py', 'synthetic_public_boundary')
        self.assertEqual(good.VALUE, 7)
        self.helper.write_bytes(self.changed_body())
        with self.assertRaisesRegex(RuntimeError, 'checkout'):
            runner.checkout_module(self.repo, 'boundary.py', 'synthetic_changed_boundary')
        self.assertFalse(self.marker.exists())

    def test_staged_but_uncommitted_helper_is_not_admitted(self):
        self.helper.write_bytes(self.changed_body())
        self.git('add', '--', self.relative)
        with self.assertRaisesRegex(RuntimeError, 'checkout'):
            runner.checkout_module(self.repo, 'boundary.py', 'synthetic_staged_boundary')
        self.assertFalse(self.marker.exists())

    def saved_inputs(self, body, name='saved-state'):
        state = self.area / name; (state / 'inputs').mkdir(parents=True)
        (state / 'inputs/boundary.py').write_bytes(body)
        identities = {'boundary.py': runner.identity(body)}
        identity_body = runner.json_bytes(identities)
        (state / 'inputs/SOURCE-IDENTITIES.json').write_bytes(identity_body)
        prepared = {'input_files': {'inputs/SOURCE-IDENTITIES.json': runner.identity(identity_body),
                                   'inputs/boundary.py': runner.identity(body)}}
        (state / 'PREPARED.json').write_bytes(runner.json_bytes(prepared))
        return state

    def test_saved_identity_map_is_pinned_before_helper_execution(self):
        state = self.saved_inputs(b'VALUE = 7\n')
        good = runner.helper_module(state, 'boundary.py', 'synthetic_saved_boundary')
        self.assertEqual(good.VALUE, 7)
        changed = self.changed_body()
        (state / 'inputs/boundary.py').write_bytes(changed)
        (state / 'inputs/SOURCE-IDENTITIES.json').write_bytes(
            runner.json_bytes({'boundary.py': runner.identity(changed)}))
        with self.assertRaisesRegex(RuntimeError, 'Prepared helper identity map'):
            runner.helper_module(state, 'boundary.py', 'synthetic_changed_saved_boundary')
        self.assertFalse(self.marker.exists())

    def test_saved_helper_metadata_aliases_refuse_before_loading(self):
        state = self.saved_inputs(b'VALUE = 7\n')
        manifest = state / 'inputs/SOURCE-IDENTITIES.json'
        body = manifest.read_bytes()
        outside = self.area / 'outside-metadata.json'
        for kind in ('hardlink', 'symlink'):
            with self.subTest(kind=kind):
                if kind == 'hardlink':
                    os.link(manifest, outside)
                else:
                    outside.write_bytes(body)
                    manifest.unlink(); manifest.symlink_to(outside)
                with self.assertRaisesRegex(RuntimeError, 'unaliased ordinary file'):
                    runner.helper_module(state, 'boundary.py', 'synthetic_aliased_metadata')
                manifest.unlink(); outside.unlink(); manifest.write_bytes(body)

    def test_local_preparation_refuses_before_population_import(self):
        fake = self.area / 'ambient'; fake.mkdir()
        (fake / 'source_alias_absence_population.py').write_bytes(self.changed_body())
        code = '''import importlib.util, pathlib, sys
spec = importlib.util.spec_from_file_location('cold_runner', sys.argv[1])
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
sys.path.insert(0, sys.argv[2])
module.prepare(pathlib.Path(sys.argv[3]), pathlib.Path(sys.argv[4]))
'''
        state = self.area / 'must-remain-absent'
        result = subprocess.run([sys.executable, '-B', '-c', code, runner.__file__, str(fake),
                                 str(self.repo), str(state)], capture_output=True, text=True,
                                env=dict(os.environ, GITHUB_ACTIONS='false', PYTHONDONTWRITEBYTECODE='1'))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Actual hosted execution is required', result.stderr)
        self.assertFalse(self.marker.exists())
        self.assertFalse(state.exists())

    def test_saved_boundary_admission_has_no_ambient_product_import(self):
        state = self.saved_inputs(Path(boundary.__file__).read_bytes())
        temporary = self.area / 'runner-temp'; temporary.mkdir()
        expected_state = temporary / 'r0002-source-alias-absence'
        state.rename(expected_state); state = expected_state
        (state / 'inputs/harness.py').write_bytes(Path(runner.__file__).read_bytes())
        head = self.git('rev-parse', 'HEAD').decode().strip()
        environment = dict(os.environ, GITHUB_ACTIONS='true', GITHUB_REPOSITORY='theislampill/orthemology',
            GITHUB_WORKSPACE=str(self.repo), RUNNER_TEMP=str(temporary), GITHUB_SHA=head,
            GITHUB_RUN_ID='123', GITHUB_RUN_ATTEMPT='1', GITHUB_EVENT_NAME='pull_request', RUNNER_OS='Linux',
            PYTHONPATH='', PYTHONDONTWRITEBYTECODE='1')
        code = '''import importlib.util, json, pathlib, sys
spec = importlib.util.spec_from_file_location('saved_runner', sys.argv[1])
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
result = module.admit_hosted_checkout(pathlib.Path(sys.argv[2]), pathlib.Path(sys.argv[3]), fresh=False, saved=True)
print(json.dumps(result, sort_keys=True))
'''
        result = subprocess.run([sys.executable, '-B', '-c', code, str(state / 'inputs/harness.py'),
                                 str(self.repo), str(state)], cwd=self.area, env=environment,
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)['head'], head)
        self.assertFalse((state / 'OPERATION.lock').exists())

    def test_authentication_closure_rejects_aliases_before_target_reads(self):
        # Artificial identity records exercise read ordering only. Hosted admission
        # and runtime are substituted; no actual preparation or restoration runs.
        def fixture(name):
            state = self.saved_inputs(b'VALUE = 7\n', name)
            body = b'artificial public recovery preimage\n'
            digest = runner.identity(body)
            relative = 'bodies/' + digest['sha256']
            (state / 'bodies').mkdir(); (state / relative).write_bytes(body)
            preimages = runner.json_bytes([dict(digest, path='alias.txt', mode=0o644)])
            (state / 'preimages.json').write_bytes(preimages)
            index = b'artificial index identity fixture\n'
            (state / 'original-index').write_bytes(index)
            before = runner.json_bytes({'artificial_fixture': True})
            (state / 'before.json').write_bytes(before)
            prepared = json.loads((state / 'PREPARED.json').read_bytes())
            info = self.repo.stat()
            prepared.update(repo=str(self.repo), state=str(state), repo_inode=[info.st_dev, info.st_ino],
                harness=runner.identity(Path(runner.__file__).read_bytes()), before=runner.identity(before),
                preimages=runner.identity(preimages), raw_index=runner.identity(index), admission={}, runtime={})
            (state / 'PREPARED.json').write_bytes(runner.json_bytes(prepared))
            return state, relative
        with patch.object(runner, 'admit_hosted_checkout', return_value={}), patch.object(runner, 'runtime', return_value={}):
            valid, body_path = fixture('valid-authentication')
            _, before = runner.authenticate_state(self.repo, valid)
            self.assertEqual(before, {'artificial_fixture': True})
            selected = ['PREPARED.json', 'inputs/SOURCE-IDENTITIES.json', 'inputs/boundary.py',
                        'before.json', 'preimages.json', 'original-index', body_path]
            read_bytes = Path.read_bytes
            for number, (relative, kind) in enumerate((r, k) for r in selected for k in ('symlink', 'hardlink')):
                with self.subTest(relative=relative, kind=kind):
                    state, _ = fixture('aliased-authentication-' + str(number))
                    target = state / relative
                    outside = self.area / ('outside-authentication-' + str(number))
                    if kind == 'symlink':
                        target.rename(outside); target.symlink_to(outside)
                    else:
                        os.link(target, outside)
                    interceptions = []
                    def guarded_read(path):
                        if path == target:
                            interceptions.append(str(path))
                            raise RuntimeError('ALIAS_READ_INTERCEPTED_BEFORE_BODY_OPEN')
                        return read_bytes(path)
                    with patch.object(Path, 'read_bytes', guarded_read):
                        with self.assertRaisesRegex(RuntimeError, 'unaliased ordinary file'):
                            runner.authenticate_state(self.repo, state)
                    self.assertEqual(interceptions, [])
            corrupt, body_path = fixture('corrupt-authentication')
            (corrupt / body_path).write_bytes(b'artificial corrupt backup\n')
            with self.assertRaisesRegex(RuntimeError, 'Preimage body changed'):
                runner.authenticate_state(self.repo, corrupt)





class PublicFixtureNativeControls(unittest.TestCase):
    """Small real native fixtures; no123 campaign or hosted-success simulation."""
    def setUp(self):
        area = Path(self.enterContext(tempfile.TemporaryDirectory(prefix='public123-native-control-')))
        self.repo = area / 'repo'; self.repo.mkdir()
        self.state = area / 'state'; self.state.mkdir()
        self.env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
        self.env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_CONFIG_SYSTEM=os.devnull, GIT_NO_LAZY_FETCH='1',
                        GIT_NO_REPLACE_OBJECTS='1', GIT_ALLOW_PROTOCOL='',
                        GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                        GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
        self.git('-c', 'init.templateDir=', 'init', '-q')
        self.bodies = {'one.json': b'{"one":1}\n', 'two.txt': b'two\n', 'provider.py': b'VALUE = 3\n'}
        for name, body in self.bodies.items():
            (self.repo / name).write_bytes(body)
        self.git('add', '--', *self.bodies)
        self.git('commit', '-qm', 'Small native restore contract fixture')
        self.members = ['one.json', 'two.txt']

    def git(self, *args, data=None):
        return subprocess.check_output(['/usr/bin/git', '--no-replace-objects', '--literal-pathspecs', *args],
                                       cwd=self.repo, env=self.env, input=data)

    def prepare_small(self):
        self.before = runner.capture_public_fixture_sources(self.repo, self.bodies)
        raw = (self.repo / '.git/index').read_bytes()
        (self.state / 'original-index').write_bytes(raw)
        (self.state / 'expected-index').write_bytes(raw)
        (self.state / 'index-mode.json').write_text(json.dumps({'mode': stat.S_IMODE((self.repo/'.git/index').stat().st_mode)}))
        (self.state / 'before.json').write_text(json.dumps(self.before))
        (self.state / 'before-namespace.json').write_text(json.dumps(runner.public_fixture_namespace(self.repo)))
        self.raw = raw
        return self.before

    def park_and_stage(self):
        self.prepare_small()
        runner.park_public_fixture_members(self.repo, self.state, self.before, self.members)
        runner.public_fixture_git(self.repo, self.state, 'update-index', '--force-remove', '--', *self.members)
        (self.state / 'expected-index').write_bytes((self.repo / '.git/index').read_bytes())

    def test_local_execution_cannot_obtain_actual_hosted_admission(self):
        with self.assertRaises(RuntimeError):
            boundary.validate_public_fixture_coordinates(self.repo, self.state, {}, 'a' * 40,
                                                          self.repo, fresh=True)

    def test_native_staged_absence_restores_original_inodes_and_raw_index(self):
        self.park_and_stage()
        self.assertTrue(all(not os.path.lexists(self.repo / path) for path in self.members))
        remaining = self.git('ls-files', '-z').split(b'\0')
        self.assertEqual([x for x in remaining if x], [b'provider.py'])
        result = runner.restore_public_fixture_members(self.repo, self.state, self.before, self.members)
        self.assertEqual(result['status'], 'PASS_FIXTURE_MEMBERS_AND_INDEX_RESTORATION_ONLY')
        self.assertEqual(runner.capture_public_fixture_sources(self.repo, self.bodies), self.before)
        self.assertEqual((self.repo / '.git/index').read_bytes(), self.raw)

    def test_reappearance_stops_before_any_file_or_index_restore(self):
        self.park_and_stage()
        (self.repo / self.members[0]).write_bytes(self.bodies[self.members[0]])
        reappeared = runner.public_fixture_file(self.repo, self.members[0])
        index = (self.repo / '.git/index').read_bytes()
        with self.assertRaisesRegex(RuntimeError, 'reappeared'):
            runner.restore_public_fixture_members(self.repo, self.state, self.before, self.members)
        self.assertEqual(runner.public_fixture_file(self.repo, self.members[0]), reappeared)
        self.assertFalse(os.path.lexists(self.repo / self.members[1]))
        self.assertTrue(all((self.state / 'park' / p).exists() for p in self.members))
        self.assertEqual((self.repo / '.git/index').read_bytes(), index)

    def test_provider_divergence_stops_before_original_or_index_restore(self):
        self.park_and_stage()
        (self.repo / 'provider.py').write_bytes(b'changed provider\n')
        index = (self.repo / '.git/index').read_bytes()
        with self.assertRaisesRegex(RuntimeError, 'source'):
            runner.restore_public_fixture_members(self.repo, self.state, self.before, self.members)
        self.assertTrue(all(not os.path.lexists(self.repo / path) for path in self.members))
        self.assertEqual((self.repo / '.git/index').read_bytes(), index)

    def test_unexplained_index_divergence_is_not_reset(self):
        self.park_and_stage()
        self.git('update-index', '--chmod=+x', '--', 'provider.py')
        changed = (self.repo / '.git/index').read_bytes()
        with self.assertRaisesRegex(RuntimeError, 'index'):
            runner.restore_public_fixture_members(self.repo, self.state, self.before, self.members)
        self.assertEqual((self.repo / '.git/index').read_bytes(), changed)
        self.assertTrue(all(not os.path.lexists(self.repo / path) for path in self.members))

    def test_park_corruption_or_alias_is_not_overwritten(self):
        self.park_and_stage()
        (self.state / 'park' / self.members[0]).write_bytes(b'corrupt parked body')
        with self.assertRaisesRegex(RuntimeError, '[Pp]ark'):
            runner.restore_public_fixture_members(self.repo, self.state, self.before, self.members)
        self.assertTrue(all(not os.path.lexists(self.repo / path) for path in self.members))

    def test_native_guard_rejects_size_queries_and_transports_before_execution(self):
        for args in [('ls-tree', '-l', 'HEAD'), ('cat-file', '-s', '0' * 40), ('fetch', 'origin')]:
            with self.subTest(args=args), self.assertRaises(RuntimeError):
                runner.public_fixture_git(self.repo, self.state, *args)
        self.assertEqual(runner.public_fixture_git(self.repo, self.state, 'ls-files', '-z'),
                         self.git('ls-files', '-z'))
        rows = list((self.state / 'native-commands').glob('*.json'))
        self.assertEqual(len(rows), 1)
        record = json.loads(rows[0].read_bytes())
        self.assertEqual(record['exit_code'], 0)
        self.assertTrue(record['stdout']['sha256'])

    def test_atomic_move_refuses_a_destination_without_overwriting_either_inode(self):
        first = runner.public_fixture_file(self.repo, 'one.json')
        second = runner.public_fixture_file(self.repo, 'two.txt')
        with self.assertRaises(OSError):
            runner._public_fixture_rename_noreplace(self.repo/'one.json', self.repo/'two.txt')
        self.assertEqual(runner.public_fixture_file(self.repo, 'one.json'), first)
        self.assertEqual(runner.public_fixture_file(self.repo, 'two.txt'), second)

    def test_native_conflict_stage_is_refused_before_consumer_execution(self):
        _, original = runner.public_fixture_stage_map(self.repo, self.state)
        oid = original['one.json'][1]
        self.git('update-index', '--force-remove', '--', 'one.json')
        self.git('update-index', '-z', '--index-info', data=('100644 '+oid+' 2\tone.json\0').encode())
        with self.assertRaisesRegex(RuntimeError, 'ordinary unconflicted'):
            runner.public_fixture_stage_map(self.repo, self.state)

    def test_untracked_namespace_change_is_visible_without_body_reads(self):
        before = runner.public_fixture_namespace(self.repo)
        (self.state/'before-namespace.json').write_text(json.dumps(before))
        self.assertEqual(runner.check_public_fixture_namespace(self.repo, self.state, set()), before)
        (self.repo/'untracked.txt').write_bytes(b'new public test file\n')
        with self.assertRaisesRegex(RuntimeError, 'namespace'):
            runner.check_public_fixture_namespace(self.repo, self.state, set())

    def test_unexplained_index_drift_is_refused_before_owned_native_mutation(self):
        self.prepare_small()
        runner.park_public_fixture_members(self.repo, self.state, self.before, self.members)
        self.git('update-index', '--chmod=+x', '--', 'provider.py')
        drift = (self.repo/'.git/index').read_bytes()
        failure = None
        try:
            runner.public_fixture_git(self.repo, self.state, 'update-index', '--force-remove', '--', *self.members)
        except RuntimeError as error:
            failure = str(error)
        after = (self.repo/'.git/index').read_bytes()
        self.assertIsNotNone(failure, 'Unexplained raw-index drift admitted; further mutation='+str(after != drift))
        self.assertIn('before controlled native mutation', failure)
        self.assertEqual(after, drift)
        self.assertEqual((self.state/'expected-index').read_bytes(), self.raw)
        self.assertFalse((self.state/'native-index-mutations').exists())
        self.assertTrue(all((self.state/'park'/path).exists() for path in self.members))

    def test_unexplained_provider_drift_is_refused_before_owned_control_write(self):
        from types import SimpleNamespace
        self.prepare_small()
        provider = self.before['provider.py']
        (self.state/'provider-bodies').mkdir()
        (self.state/'provider-bodies'/provider['sha256']).write_bytes(self.bodies['provider.py'])
        (self.repo/'provider.py').write_bytes(b'foreign public provider change\n')
        drift = runner.public_fixture_file(self.repo, 'provider.py')
        failure = None
        try:
            runner.public_fixture_controls(self.repo, self.state,
                {'records': [{'path': 'one.json'}], 'providers': [dict(provider, path='provider.py')]},
                self.before, SimpleNamespace(members=set(self.members)))
        except RuntimeError as error:
            failure = str(error)
        self.assertEqual(runner.public_fixture_file(self.repo, 'provider.py'), drift,
                         'An unexplained provider change was overwritten by a control')
        self.assertIsNotNone(failure)
        self.assertIn('before controlled provider mutation', failure)
        self.assertEqual((self.repo/'.git/index').read_bytes(), self.raw)


import hashlib
import stat

class PublicFixtureMutationRevisionTests(unittest.TestCase):
    """Declared tiny native fault fixtures; never a public123 campaign."""
    def setUp(self):
        self.area = Path(os.environ['PUBLIC123_REVISION_RESOURCES']) / self.id()
        if self.area.exists():
            raise RuntimeError('Finite fault resource is single-use')
        self.area.mkdir()
        self.repo = self.area/'repo'; self.repo.mkdir()
        self.state = self.area/'state'; self.state.mkdir()
        self.env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
        self.env.update(GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                        GIT_CONFIG_SYSTEM=os.devnull, GIT_NO_LAZY_FETCH='1',
                        GIT_NO_REPLACE_OBJECTS='1', GIT_ALLOW_PROTOCOL='', GIT_OPTIONAL_LOCKS='0',
                        GIT_AUTHOR_NAME='Finite public fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                        GIT_COMMITTER_NAME='Finite public fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
        self.git('-c', 'init.templateDir=', 'init', '-q')
        self.bodies = {'one.json': b'{"one":1}\n', 'two.txt': b'two\n', 'provider.py': b'VALUE = 3\n'}
        for name, body in self.bodies.items():
            (self.repo/name).write_bytes(body)
        self.git('add', '--', *self.bodies)
        self.git('commit', '-qm', 'Declared tiny public mutation-boundary fixture')
        self.members = {'one.json', 'two.txt'}
        self.before = runner.capture_public_fixture_sources(self.repo, self.bodies)
        self.raw = runner.public_fixture_index(self.repo)
        self.mode = stat.S_IMODE((self.repo/'.git/index').stat().st_mode)
        for name in ('original-index', 'expected-index'):
            (self.state/name).write_bytes(self.raw)
        (self.state/'index-mode.json').write_text(json.dumps({'mode': self.mode}))
        (self.state/'before.json').write_text(json.dumps(self.before))
        (self.state/'before-namespace.json').write_text(json.dumps(runner.public_fixture_namespace(self.repo)))
        self.source = self.before['provider.py']
        (self.state/'provider-bodies').mkdir()
        (self.state/'provider-bodies'/self.source['sha256']).write_bytes(self.bodies['provider.py'])

    def git(self, *args, data=None):
        result = subprocess.run(['/usr/bin/git', '--no-replace-objects', '--literal-pathspecs', *args],
                                cwd=self.repo, env=self.env, input=data, capture_output=True, check=True)
        return result.stdout

    def park(self):
        runner.park_public_fixture_members(self.repo, self.state, self.before, self.members)

    def controls(self):
        value = {'records': [{'path': 'one.json'}],
                 'providers': [dict(self.source, path='provider.py')]}
        audit = runner.PublicFixtureAudit(self.repo, self.state, self.members)
        return runner.public_fixture_controls(self.repo, self.state, value, self.before, audit)

    def save_observation(self, name, value):
        (self.area/(name+'.json')).write_text(json.dumps(value, indent=2)+'\n')

    def test_saved_index_mode_is_required_before_any_parking(self):
        os.chmod(self.repo/'.git/index', 0o600)
        failure = None
        try:
            self.park()
        except RuntimeError as error:
            failure = str(error)
        presence = {path: os.path.lexists(self.repo/path) for path in self.members}
        self.save_observation('mode-before-parking', {'failure': failure, 'presence': presence,
            'park_exists': os.path.lexists(self.state/'park'),
            'parking_start_exists': (self.state/'PARKING-START.json').exists(),
            'index_mode': stat.S_IMODE((self.repo/'.git/index').stat().st_mode),
            'raw_index_unchanged': runner.public_fixture_index(self.repo) == self.raw})
        self.assertTrue(all(presence.values()), 'Index mode drift was followed by original parking')
        self.assertFalse(os.path.lexists(self.state/'park'))
        self.assertFalse((self.state/'PARKING-START.json').exists())
        self.assertIsNotNone(failure)
        self.assertEqual(stat.S_IMODE((self.repo/'.git/index').stat().st_mode), 0o600)
        self.assertEqual(runner.capture_public_fixture_sources(self.repo, self.bodies), self.before)

    def test_valid_stat_only_index_drift_prevents_all_provider_writes(self):
        self.park()
        stage = self.git('ls-files', '--stage', '-z')
        altered = bytearray(self.raw)
        self.assertEqual(int.from_bytes(altered[4:8], 'big'), 2)
        altered[12:16] = ((int.from_bytes(altered[12:16], 'big')+1) % (2**32)).to_bytes(4, 'big')
        altered[-20:] = hashlib.sha1(altered[:-20]).digest()
        (self.repo/'.git/index').write_bytes(altered)
        self.assertEqual(self.git('ls-files', '--stage', '-z'), stage)
        provider = runner.public_fixture_file(self.repo, 'provider.py')
        writes, active = [], [True]
        def record_write(event, args):
            if (active[0] and event == 'open' and isinstance(args[0], (str, bytes, os.PathLike))
                    and Path(os.fsdecode(args[0])).absolute() == self.repo/'provider.py'
                    and isinstance(args[2], int) and args[2] & (os.O_WRONLY | os.O_RDWR)):
                writes.append({'flags': args[2]})
        sys.addaudithook(record_write)
        failure = None
        try:
            self.controls()
        except RuntimeError as error:
            failure = str(error)
        finally:
            active[0] = False
        after = runner.public_fixture_file(self.repo, 'provider.py')
        self.save_observation('stat-index-before-controls', {'failure': failure, 'observed_provider_writes': writes,
            'provider_before': provider, 'provider_after': after,
            'drifted_raw_index_unchanged': runner.public_fixture_index(self.repo) == bytes(altered)})
        self.assertEqual(writes, [], 'Unexpected raw-index drift was followed by provider-body writes')
        self.assertIsNotNone(failure)
        self.assertEqual(after, provider)
        self.assertEqual(runner.public_fixture_index(self.repo), bytes(altered))

    def cleanup_fault(self, kind):
        from unittest.mock import patch
        self.park()
        real_run = subprocess.run
        observed = {}
        def actual_native_then_fault(command, *args, **kwargs):
            result = real_run(command, *args, **kwargs)
            if 'update-index' in command and '--cacheinfo' in command and not observed:
                observed['controlled'] = runner.public_fixture_index(self.repo)
                if kind == 'mode':
                    os.chmod(self.repo/'.git/index', 0o600)
                else:
                    (self.repo/'.git/index.lock').write_bytes(b'foreign public test lock\n')
            return result
        failure = None
        with patch.object(subprocess, 'run', side_effect=actual_native_then_fault):
            try:
                self.controls()
            except (RuntimeError, KeyError) as error:
                # This finite fixture intentionally stops at the controlled
                # index boundary. The old implementation may proceed into the
                # omitted later public-row stimulus after incorrectly resetting
                # the index; preserve that diagnostic, then test the state.
                failure = type(error).__name__+': '+str(error)
        self.assertIn('controlled', observed)
        after = runner.public_fixture_index(self.repo)
        mode = stat.S_IMODE((self.repo/'.git/index').stat().st_mode)
        lock = self.repo/'.git/index.lock'
        self.save_observation('controlled-index-'+kind, {'failure': failure,
            'controlled_raw': runner.identity(observed['controlled']), 'actual_raw': runner.identity(after),
            'actual_mode': mode, 'foreign_lock_present': lock.exists()})
        self.assertEqual(after, observed['controlled'], 'Controlled cleanup erased unexplained index drift')
        self.assertIsNotNone(failure)
        if kind == 'mode':
            self.assertEqual(mode, 0o600)
        else:
            self.assertEqual(lock.read_bytes(), b'foreign public test lock\n')

    def test_control_cleanup_refuses_foreign_index_mode(self):
        self.cleanup_fault('mode')

    def test_control_cleanup_refuses_foreign_index_lock(self):
        self.cleanup_fault('lock')

    def test_valid_control_cleanup_restores_exact_owned_index(self):
        self.park()
        self.git('update-index', '--cacheinfo', '100755,'+self.source['git_blob']+',provider.py')
        changed = runner.public_fixture_index(self.repo)
        runner.restore_public_fixture_control_index(self.repo, self.state, self.before, self.members,
                                                    self.raw, changed, self.mode)
        self.assertEqual(runner.public_fixture_index(self.repo), self.raw)
        self.assertEqual(stat.S_IMODE((self.repo/'.git/index').stat().st_mode), self.mode)
        self.assertTrue(all(not os.path.lexists(self.repo/path) for path in self.members))



class PublicFixtureFailureExportRevisionTests(unittest.TestCase):
    """Real tiny native source authentication; no hosted-context simulation."""
    def setUp(self):
        self.root = Path(os.environ['PUBLIC123_REVISION_RESOURCES'])/self.id()
        self.repo, self.state = self.root/'repo', self.root/'state'
        self.repo.mkdir(parents=True); self.state.mkdir()
        self.env = dict(runner.public_fixture_environment(), GIT_AUTHOR_NAME='Finite Fixture',
                        GIT_AUTHOR_EMAIL='fixture@example.invalid', GIT_COMMITTER_NAME='Finite Fixture',
                        GIT_COMMITTER_EMAIL='fixture@example.invalid')
        self.git('-c', 'init.templateDir=', 'init', '-q')
        helpers, inputs = {}, {}
        paths = dict(runner.PUBLIC_HELPERS, **{'harness.py': 'scripts/check_source_alias_absence.py'})
        for name, relative in paths.items():
            body = (Path(runner.__file__).parent.parent/relative).read_bytes()
            target = self.repo/relative; target.parent.mkdir(parents=True, exist_ok=True); target.write_bytes(body)
            saved = self.state/'inputs'/name; saved.parent.mkdir(parents=True, exist_ok=True); saved.write_bytes(body)
            inputs['inputs/'+name] = runner.identity(body)
            if name != 'harness.py': helpers[name] = dict(runner.identity(body), source_path=relative)
        runner.save(self.state/'inputs/SOURCE-IDENTITIES.json', helpers)
        inputs['inputs/SOURCE-IDENTITIES.json'] = runner.identity((self.state/'inputs/SOURCE-IDENTITIES.json').read_bytes())
        self.git('add', '--', *paths.values())
        self.git('commit', '-qm', 'Declared finite public exporter source fixture')
        self.prepared = {'profile': runner.PUBLIC_FIXTURE_PROFILE, 'repo': str(self.repo), 'state': str(self.state),
            'repo_inode': [self.repo.stat().st_dev, self.repo.stat().st_ino],
            'head': self.git('rev-parse', 'HEAD').decode().strip(), 'tree': self.git('rev-parse', 'HEAD^{tree}').decode().strip(),
            'harness': inputs['inputs/harness.py'], 'input_files': inputs}
        runner.save(self.state/'PREPARED.json', self.prepared)
        self.raw = (self.repo/'.git/index').read_bytes()
        runner.atomic_bytes(self.state/'expected-index', self.raw)
        runner.save(self.state/'index-mode.json', {'mode': stat.S_IMODE((self.repo/'.git/index').stat().st_mode)})

    def git(self, *args):
        return subprocess.run(['/usr/bin/git', '--no-replace-objects', '--literal-pathspecs', *args],
            cwd=self.repo, env=self.env, capture_output=True, check=True).stdout

    def test_corrupt_live_index_does_not_block_public_source_receiving_or_get_repaired(self):
        corrupt = b'INTENTIONALLY_CORRUPT_FINITE_INDEX\n'
        (self.repo/'.git/index').write_bytes(corrupt)
        before = {str(p.relative_to(self.state)): p.read_bytes() for p in self.state.rglob('*') if p.is_file()}
        received = runner.authenticate_public_fixture_export_sources(self.repo, self.state)
        self.assertEqual(len(received['public_sources']), 9)
        self.assertFalse(received['live_index_required_for_authentication'])
        observation = runner.public_fixture_export_index_observation(self.repo, self.state)
        self.assertFalse(observation['exact'])
        self.assertFalse(observation['restoration_performed'])
        self.assertEqual((self.repo/'.git/index').read_bytes(), corrupt)
        self.assertEqual(before, {str(p.relative_to(self.state)): p.read_bytes() for p in self.state.rglob('*') if p.is_file()})
        runner.save(self.root/'corrupt-index-source-receiving.json', {'received': received, 'live_index': observation,
            'actual_hosted_execution': False, 'qualification': 'SOURCE_AUTHENTICATION_ONLY'})

    def test_wrong_public_code_head_and_root_are_refused(self):
        for field, value in [('head', '0'*40), ('repo', str(self.root))]:
            changed = dict(self.prepared, **{field: value})
            runner.save(self.state/'PREPARED.json', changed, replace=True)
            with self.subTest(field=field), self.assertRaises(RuntimeError):
                runner.authenticate_public_fixture_export_sources(self.repo, self.state)
        runner.save(self.state/'PREPARED.json', self.prepared, replace=True)
        target = self.repo/'scripts/source_alias_absence_boundary.py'
        target.write_bytes(target.read_bytes()+b'\n# wrong live code\n')
        with self.assertRaises(RuntimeError):
            runner.authenticate_public_fixture_export_sources(self.repo, self.state)
        self.assertEqual((self.repo/'.git/index').read_bytes(), self.raw)



class PublicFixtureChildLifetimeRevisionTests(unittest.TestCase):
    """Actual tiny fault children: startup/lease custody, no consumer campaign."""
    def setUp(self):
        self.root = Path(os.environ['PUBLIC123_REVISION_RESOURCES'])/self.id()
        self.root.mkdir(parents=True)
        self.repo, self.state = self.root/'repo', self.root/'state'
        self.repo.mkdir(); self.state.mkdir()
        self.out = self.state/'phases/fixtures123-present'
        self.out.mkdir(parents=True)
        self.token = 'a'*32

    def child(self, mode, *, group_save_failure=False):
        from unittest import mock
        script = self.root/'fault_child.py'
        code = ("import json,os,sys\n"
                "sys.path.insert(0, "+repr(str(Path(runner.__file__).parent))+ ")\n"
                "import check_source_alias_absence as harness\n"
                "mode=sys.argv[1]\nfd=int(sys.argv[sys.argv.index('--identity-fd')+1])\n"
                "if mode=='silent': sys.stdin.readline()\n"
                "with os.fdopen(fd,'wb') as stream:\n"
                "    if mode=='good': stream.write(json.dumps(harness.group_record()).encode()+b'\\n')\n"
                "    elif mode=='malformed': stream.write(b'{\\n')\n"
                "    elif mode=='invalid-shape': stream.write(b'{}\\n')\n"
                "    stream.flush()\n"
                "lease=sys.stdin.readline().rstrip('\\n')\n"
                "if lease: print('actual narrow lease received',flush=True)\n")
        prefix = [sys.executable, '-B', str(script), mode]
        runner.save(self.root/'CHILD-DECLARATION.json', {'command_prefix': prefix,
            'script_sha256': hashlib.sha256(code.encode()).hexdigest(), 'scope': 'Actual finite fault child only',
            'declared_before_script_creation': True, 'actual_hosted_execution': False})
        script.write_text(code)
        lease_checks = []
        real_save = runner.save
        def save_with_one_transport_fault(path, *args, **kwargs):
            if group_save_failure and Path(path) == self.state/'groups'/(self.token+'.json'):
                raise OSError('Declared exact group-record persistence fault')
            return real_save(path, *args, **kwargs)
        with mock.patch.object(runner, 'save', save_with_one_transport_fault):
            if mode == 'good' and not group_save_failure:
                result = runner.public_fixture_child_custody(self.repo, self.state, self.out,
                    'fixtures123-present', self.token, prefix, lambda: lease_checks.append(True), handshake_timeout=3)
                self.assertEqual(result['exit_code'], 0)
                self.assertTrue(result['lease_sent'])
                self.assertTrue(result['quiescent'])
            else:
                with self.assertRaises((RuntimeError, ValueError, OSError)) as failure:
                    runner.public_fixture_child_custody(self.repo, self.state, self.out,
                        'fixtures123-present', self.token, prefix, lambda: lease_checks.append(True),
                        handshake_timeout=0.2 if mode=='silent' else 3)
                self.assertEqual(lease_checks, [])
                if mode=='silent': self.assertIn('timed out', str(failure.exception))
        record = json.loads((self.state/'children'/(self.token+'.json')).read_bytes())
        self.assertEqual(record['status'], 'TERMINAL_RECEIVED')
        self.assertIs(type(record['exit_code']), int)
        with self.assertRaises(ChildProcessError): os.waitpid(record['pid'], os.WNOHANG)
        quiet = runner.public_fixture_quiescence(self.state)
        self.assertEqual(quiet['quiescent'], mode == 'good' and not group_save_failure)
        if mode != 'good' or group_save_failure:
            self.assertFalse(record['lease_sent'])
            self.assertFalse(record['quiescent'])
        runner.save(self.root/'ACTUAL-CHILD-OUTCOME.json', {'record': record, 'received_quiescence': quiet,
            'reaped_by_owned_parent': True, 'actual_hosted_execution': False})

    def test_malformed_handshake_child_is_reaped_and_restoration_stays_blocked(self):
        self.child('malformed')

    def test_missing_handshake_child_is_reaped_and_restoration_stays_blocked(self):
        self.child('missing')

    def test_invalid_group_shape_child_is_reaped_without_trusting_its_fields(self):
        self.child('invalid-shape')

    def test_group_save_failure_is_contained_before_any_lease(self):
        self.child('good', group_save_failure=True)

    def test_actual_finite_child_lease_wait_and_quiescence_are_bound(self):
        self.child('good')

    def test_silent_open_handshake_times_out_reaps_owned_child_and_blocks_restoration(self):
        self.child('silent')


import copy

class PublicFixtureNativeOutcomeRevisionTests(unittest.TestCase):
    """New actual native outcome/journal bindings on a three-file ordinary fixture."""
    setUp = PublicFixtureMutationRevisionTests.setUp
    git = PublicFixtureMutationRevisionTests.git
    park = PublicFixtureMutationRevisionTests.park

    def test_actual_native_outcomes_and_hash_bound_references_reject_missing_or_changed_evidence(self):
        import source_alias_absence_evidence as evidence
        with runner.PublicFixtureNativeRecorder(self.repo, self.state) as recorder:
            runner.public_fixture_git(self.repo, self.state, 'rev-parse', 'HEAD')
            result = subprocess.run(['/usr/bin/git', '--no-replace-objects', 'config', '--type=bool', '--get', 'core.splitIndex'],
                cwd=self.repo, env=self.env, capture_output=True)
            self.assertEqual(result.returncode, 1)
            refs = recorder.snapshot()
        rows, identities = evidence.public_fixture_category(self.state, 'native-executions')
        self.assertEqual(len(rows), 2)
        for row in rows.values():
            self.assertEqual(evidence.public_fixture_native_record(row, str(self.repo), set())['scope'],
                             'CONSISTENT_NATIVE_OUTCOME_ONLY')
        process = next(iter(rows.values()))['process']
        self.assertEqual(evidence.public_fixture_native_refs(refs, rows, identities, process), set(rows))
        for change in ({'status': 'STARTED_NOT_TERMINAL'}, {'exit_code': None}, {'exit_code': True},
                       {'observed_cwd': '/wrong/native/root'}, {'resolved_executable': '/fake/git'},
                       {'stdout': {}}):
            bad = dict(next(iter(rows.values())), **change)
            with self.subTest(change=change), self.assertRaises((RuntimeError, TypeError, KeyError)):
                evidence.public_fixture_native_record(bad, str(self.repo), set())
        bad_refs = copy.deepcopy(refs); bad_refs[0]['identity']['sha256'] = '0'*64
        with self.assertRaises(RuntimeError): evidence.public_fixture_native_refs(bad_refs, rows, identities, process)
        with self.assertRaises(RuntimeError): evidence.public_fixture_native_refs(refs+refs[:1], rows, identities, process)
        with self.assertRaises(RuntimeError): evidence.public_fixture_native_refs(refs, {}, {}, process)
        runner.save(self.area/'NATIVE-OUTCOME-CONTRACT.json', {'native_records': len(rows), 'negative_variants': 9,
            'actual_native_execution': True, 'actual123_or_hosted_execution': False, 'raw_index_unchanged': runner.public_fixture_index(self.repo)==self.raw})

    def test_actual_native_control_journal_binds_before_after_process_and_owned_cleanup(self):
        import source_alias_absence_evidence as evidence
        self.park()
        with runner.PublicFixtureNativeRecorder(self.repo, self.state) as recorder:
            runner.public_fixture_git(self.repo, self.state, 'update-index', '--cacheinfo',
                                      '100755,'+self.source['git_blob']+',provider.py')
            changed = runner.public_fixture_index(self.repo)
            cleanup = runner.restore_public_fixture_control_index(self.repo, self.state, self.before, self.members,
                                                                  self.raw, changed, self.mode)
            refs = recorder.snapshot()
        commands, command_ids = evidence.public_fixture_category(self.state, 'native-commands')
        native, native_ids = evidence.public_fixture_category(self.state, 'native-executions')
        mutations, _ = evidence.public_fixture_category(self.state, 'native-index-mutations')
        self.assertEqual(len(commands), 1); self.assertEqual(len(native), 1); self.assertEqual(len(mutations), 1)
        mutation = next(iter(mutations.values())); command = commands[mutation['command_record']]
        self.assertEqual(mutation['command_identity'], command_ids[mutation['command_record']])
        self.assertEqual(mutation['native_record'], command['native_record'])
        actual = native[mutation['native_record']]
        self.assertEqual(mutation['process'], actual['process'])
        self.assertEqual(mutation['command'], actual['observed_argv'])
        self.assertEqual(mutation['before']['raw_index'], runner.identity(self.raw))
        self.assertEqual(mutation['after'], runner.identity(changed))
        self.assertEqual(mutation['status'], 'TERMINAL'); self.assertEqual(mutation['exit_code'], 0)
        self.assertEqual(cleanup['before'], mutation['after']); self.assertEqual(cleanup['after'], runner.identity(self.raw))
        self.assertEqual(json.loads((self.state/cleanup['write_record']).read_bytes())['body'], runner.identity(self.raw))
        self.assertEqual(evidence.public_fixture_native_refs(refs, native, native_ids, actual['process']), set(native))
        self.assertEqual(runner.public_fixture_index(self.repo), self.raw)
        runner.save(self.area/'NATIVE-CONTROL-JOIN.json', {'mutation': mutation, 'cleanup': cleanup,
            'actual_native_execution': True, 'actual123_or_hosted_execution': False})


class PublicFixtureAuthenticatedCurrentnessControls(unittest.TestCase):
    """The actual caller and validators, with finite artificial Git identities.

    No generated fixture or research programme is executed. Empty public-object
    records intentionally cannot earn a complete public123 consumer verdict.
    """
    def setUp(self):
        import hashlib
        import importlib
        from types import SimpleNamespace
        self.hashlib = hashlib
        self.audit = SimpleNamespace(absent=False)
        self.area = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.repo = self.area/'checkout'; self.repo.mkdir()
        self.state = self.area/'state'; (self.state/'inputs').mkdir(parents=True)
        self.script_root = self.repo/'scripts'; self.script_root.mkdir()
        names = {Path(path).name for path in runner.PUBLIC_FIXTURE_SOURCE_PATHS}
        names |= {'source_alias_absence_boundary.py', 'source_alias_absence_reader.py'}
        source_root = Path(runner.__file__).resolve().parent
        for name in names:
            (self.script_root/name).write_bytes((source_root/name).read_bytes())
        module_names = {Path(name).stem for name in names}
        old_modules = {name: sys.modules.get(name) for name in module_names}
        old_path = list(sys.path)
        def restore_imports():
            sys.path[:] = old_path
            for name, value in old_modules.items():
                if value is None: sys.modules.pop(name, None)
                else: sys.modules[name] = value
        self.addCleanup(restore_imports)
        for name in module_names: sys.modules.pop(name, None)
        sys.path.insert(0, str(self.script_root))
        self.reader = importlib.import_module('check_reader_pilot')
        self.adapter = importlib.import_module('source_alias_absence_reader')
        self.source = importlib.import_module('resolve_t20_v6_source')
        self.enterContext(patch.object(runner, 'helper_module', return_value=self.adapter))
        self.enterContext(patch.dict(os.environ, {'GITHUB_WORKSPACE': str(self.repo),
            'GIT_NO_LAZY_FETCH': '1', 'GIT_NO_REPLACE_OBJECTS': '1', 'GIT_ALLOW_PROTOCOL': '',
            'GIT_AUTHOR_NAME': 'Artificial fixture', 'GIT_AUTHOR_EMAIL': 'fixture@example.invalid',
            'GIT_COMMITTER_NAME': 'Artificial fixture', 'GIT_COMMITTER_EMAIL': 'fixture@example.invalid'}))
        self.git('init', '-q')
        self.held = []
        for n, path in enumerate(boundary.PROTECTED_PATHS):
            body = ('artificial held stand-in '+str(n)+'\n').encode()
            self.write(path, body)
            self.held.append({'path': path, 'bytes': len(body), 'published_metadata': {
                'mode': '100644', 'git_blob': runner.identity(body)['git_blob']}})
        self.original, self.current = {}, {}
        fixture_paths = set(self.reader.FIXTURE_CONSUMER_ORIGINAL)
        continuation_paths = set(self.reader.CONTINUATION_OWNER_PATHS)
        for n, path in enumerate(sorted(fixture_paths | continuation_paths)):
            old, new = ('original owner '+str(n)+'\n').encode(), ('current owner '+str(n)+'\n').encode()
            self.write(path, old)
            self.original[path], self.current[path] = self.edition(old), self.edition(new)
        self.base_path = str(Path('docs')/'context-base.md')
        self.write(self.base_path, b'An artificial original public source.\n')
        self.git('add', '--all')
        tree = self.git('write-tree').decode().strip()
        self.baseline = self.git('commit-tree', tree, input=b'Artificial currentness baseline\n').decode().strip()
        rows = []
        for raw in self.git('ls-tree', '-r', '-z', self.baseline).split(b'\0'):
            if not raw: continue
            head, path = raw.split(b'\t'); mode, kind, oid = head.decode().split()
            path = path.decode()
            rows.append({'path': path, 'mode': mode, 'kind': kind, 'git_oid': oid,
                         'bytes': (self.repo/path).stat().st_size})
        rows.sort(key=lambda row: row['path'])
        digest = hashlib.sha256(json.dumps(rows, sort_keys=True, ensure_ascii=False,
            separators=(',', ':')).encode()).hexdigest()
        self.owner = {'schema': 'orthemology-reader-owner-map-v1', 'baseline': {
            'commit': self.baseline, 'tree': tree}, 'entries_sha256': digest,
            'external_body_admissions': [], 'historical_source_bindings': [],
            'baseline_work_population': {'count': 0,
                'keys_sha256': hashlib.sha256(b'[]').hexdigest()}}
        self.census = {'schema': 'orthemology-reader-census-v1',
            'baseline': dict(self.owner['baseline']), 'entries_sha256': digest,
            'external_body_admissions': [], 'population': {'tracked_entries': len(rows)}}
        self.cross = {'schema': 'orthemology-reader-crosswalk-v1', 'coverage_stage': 'reader-candidate',
            'works': [], 'sources': {}}
        for path in self.original:
            n = sorted(self.original).index(path)
            self.write(path, ('current owner '+str(n)+'\n').encode())
        for name, values in [('FIXTURE_CONSUMER_ORIGINAL', self.original),
                             ('FIXTURE_CONSUMER_CURRENT', self.current)]:
            self.enterContext(patch.object(self.reader, name, {p: values[p] for p in fixture_paths}))
        for name, values in [('CONTINUATION_OWNER_ORIGINAL', self.original),
                             ('CONTINUATION_OWNER_CURRENT', self.current),
                             ('CONTINUATION_OWNER_SPARSE_PRIOR', self.current)]:
            self.enterContext(patch.object(self.reader, name, {p: values[p] for p in continuation_paths}))
        self.enterContext(patch.object(self.reader, 'FIXTURE_CONSUMER_REVISION', self.baseline))
        self.work_path = str(Path('docs')/'context-work.md')
        review_path = str(Path('docs')/'context-review.md')
        work = b'# Artificial admitted work\n\nFinite consumer test only.\n'
        self.write(self.work_path, work)
        review = ('| Work | SHA-256 | Bytes |\n|---|---|---|\n| [Work](context-work.md) | `'
                  +hashlib.sha256(work).hexdigest()+'` | '+str(len(work))+' |\n').encode()
        self.write(review_path, review)
        self.owner['source_additions'] = []
        for key, path, body, role, supports in [('work', self.work_path, work, 'work-source', ['review']),
                                              ('review', review_path, review, 'review', [])]:
            identity = runner.identity(body)
            self.owner['source_additions'].append({'key': key, 'path': path, 'mode': '100644',
                'git_oid': identity['git_blob'], 'bytes': identity['bytes'], 'sha256': identity['sha256'],
                'role': role, 'work_keys': ['artificial-work'], 'supporting_source_keys': supports})
            self.cross['sources'][key] = {'path': path, 'sha256': identity['sha256'],
                'read_scope': 'Finite artificial caller control'}
        self.cross['works'] = [{'key': 'artificial-work', 'role': 'synthesis', 'source_keys': ['work'],
            'supporting_source_keys': ['review'],
            'reading_forms': [{'source': 'work', 'relationship': 'authored-synthesis'}]}]
        self.metadata_root = Path(runner.PUBLIC_FIXTURE_OWNER).parent
        self.sync_metadata()
        (self.state/'inputs/hold.json').write_text(json.dumps({'held': self.held}))
        self.git('add', '--all')

    def git(self, *args, input=None):
        return subprocess.run(['git', '--no-replace-objects', *args], cwd=self.repo,
            input=input, capture_output=True, check=True).stdout

    def write(self, path, body):
        node = self.repo/path; node.parent.mkdir(parents=True, exist_ok=True); node.write_bytes(body)

    def edition(self, body):
        value = runner.identity(body)
        return value['git_blob'], value['sha256'], value['bytes']

    def sync_metadata(self):
        for name, value in [('OWNER-MAP.json', self.owner), ('CROSSWALK.json', self.cross),
                            ('CENSUS.json', self.census)]:
            self.write(str(self.metadata_root/name), runner.json_bytes(value))

    def consume(self):
        original = self.source.readonly_git_diff
        native_run = subprocess.run
        self.native_commands = []
        def observe(command, *args, **kwargs):
            self.native_commands.append(list(command))
            return native_run(command, *args, **kwargs)
        pins = {'BASELINE': self.baseline,
            'OWNER_MAP_SHA256': runner.identity((self.repo/runner.PUBLIC_FIXTURE_OWNER).read_bytes())['sha256'],
            'READER_SHA256': runner.identity((self.script_root/'check_reader_pilot.py').read_bytes())['sha256'],
            'RESOLVER_SHA256': runner.identity((self.script_root/'resolve_t20_v6_source.py').read_bytes())['sha256'],
            'CENSUS_SHA256': runner.identity((self.repo/self.metadata_root/'CENSUS.json').read_bytes())['sha256']}
        with patch.multiple(self.adapter, create=True, **pins), patch.object(subprocess, 'run', side_effect=observe):
            try:
                return runner.public_fixture_consumers(self.repo, self.state, {'records': []}, self.audit)
            finally:
                self.source.readonly_git_diff = original
                self.reader.readonly_git_diff = original

    def test_actual_caller_accepts_authenticated_contexts_and_keeps_held_exclusions(self):
        import io
        held_paths = {self.repo/row['path'] for row in self.held}
        actual_open, actual_os_open = io.open, os.open
        def guarded_open(file, *args, **kwargs):
            if not isinstance(file, int) and Path(file).absolute() in held_paths:
                raise AssertionError('Held stand-in body open is forbidden')
            return actual_open(file, *args, **kwargs)
        def guarded_os_open(file, *args, **kwargs):
            if not isinstance(file, int) and Path(file).absolute() in held_paths:
                raise AssertionError('Held stand-in descriptor open is forbidden')
            return actual_os_open(file, *args, **kwargs)
        with patch.object(io, 'open', side_effect=guarded_open), patch.object(os, 'open', side_effect=guarded_os_open):
            result = self.consume()
        self.assertEqual(result['currentness_errors'], [])
        metadata_queries = [argv for argv in self.native_commands if 'ls-tree' in argv]
        self.assertTrue(metadata_queries)
        self.assertTrue(all('-l' not in argv and '--long' not in argv for argv in metadata_queries))
        self.assertFalse(result['passed'])  # Empty objects never claim a public123 pass.
        events = result['reader_boundary']['events']
        self.assertEqual([r['surface'] for r in events], ['index', 'public_worktree'])
        self.assertEqual([r['held_worktree_exclusions'] for r in events], [0, 5])
        self.assertEqual(sum(arg.startswith(':(top,literal,exclude)')
            for arg in events[1]['executed_command']), 5)

    def test_unknown_added_source_is_still_rejected(self):
        path = str(Path('docs')/'context-unadmitted.md')
        self.write(path, b'No source admission.\n'); self.git('add', '--', path)
        result = self.consume()
        self.assertTrue(any(path in error for error in result['currentness_errors']))

    def test_unstaged_original_change_is_still_rejected(self):
        self.write(self.base_path, b'Changed only in the worktree.\n')
        result = self.consume()
        self.assertTrue(any(self.base_path in error for error in result['currentness_errors']))

    def test_corrupt_admission_error_reaches_actual_consumer(self):
        self.owner['source_additions'][0]['sha256'] = '0'*64
        self.sync_metadata(); self.git('add', '--all')
        result = self.consume()
        self.assertTrue(any(error.startswith('source-addition:') for error in result['currentness_errors']))

    def test_incorrect_fixture_owner_edition_reaches_actual_consumer(self):
        path = sorted(self.reader.FIXTURE_CONSUMER_ORIGINAL)[0]
        self.write(path, b'Unadmitted owner edition.\n'); self.git('add', '--', path)
        result = self.consume()
        self.assertTrue(any(error.startswith('fixture-consumer:') for error in result['currentness_errors']))

    def test_incorrect_continuation_owner_edition_reaches_actual_consumer(self):
        path = self.reader.CONTINUATION_OWNER_PATHS[0]
        self.write(path, b'Unadmitted continuation edition.\n'); self.git('add', '--', path)
        result = self.consume()
        self.assertTrue(any(error.startswith('continuation-owner:') for error in result['currentness_errors']))

    def test_census_cannot_select_another_baseline_tree(self):
        self.census['baseline']['tree'] = '0'*40
        self.sync_metadata(); self.git('add', '--all')
        with self.assertRaisesRegex(RuntimeError, 'census|baseline'):
            self.consume()

    def test_owner_body_changed_after_adapter_admission_is_rejected(self):
        install = self.adapter.install
        def changed_after_admission(*args):
            result = install(*args)
            self.owner['unexpected'] = True
            self.write(runner.PUBLIC_FIXTURE_OWNER, runner.json_bytes(self.owner))
            return result
        with patch.object(self.adapter, 'install', side_effect=changed_after_admission):
            with self.assertRaisesRegex(RuntimeError, 'owner map changed'):
                self.consume()

    def test_published_size_metadata_cannot_admit_a_held_identity(self):
        held = self.held[0]
        bad = dict(self.reader.HISTORICAL_PROSE)
        bad[held['path']] = (held['published_metadata']['git_blob'], '0'*64, held['bytes'])
        with patch.object(self.reader, 'HISTORICAL_PROSE', bad):
            with self.assertRaisesRegex(RuntimeError, 'Held'):
                self.consume()


class ProductionReaderSourcePinControls(unittest.TestCase):
    def test_unpatched_adapter_pins_equal_exact_composed_source_bytes(self):
        import ast
        import hashlib
        scripts = Path(__file__).resolve().parents[1] / 'scripts'
        source = (scripts / 'source_alias_absence_reader.py').read_bytes()
        constants = {node.targets[0].id: ast.literal_eval(node.value)
                     for node in ast.parse(source).body
                     if isinstance(node, ast.Assign) and len(node.targets) == 1
                     and isinstance(node.targets[0], ast.Name)
                     and node.targets[0].id in {'RESOLVER_SHA256', 'READER_SHA256'}}
        for name, filename in [('RESOLVER_SHA256', 'resolve_t20_v6_source.py'),
                               ('READER_SHA256', 'check_reader_pilot.py')]:
            with self.subTest(pin=name):
                self.assertEqual(constants[name], hashlib.sha256((scripts / filename).read_bytes()).hexdigest())


class PublicFixtureReconciliationCommandControls(unittest.TestCase):
    """Exercise exact operational functions through the unchanged public audit.

    No repository is initialized and no native command or scientific source is
    executed. The dispatcher supplies finite synthetic native metadata/bodies
    only after the actual PublicFixtureAudit accepts the requested command.
    """
    SOURCE_PATH = Path(__file__).resolve().parents[1] / 'scripts/validate_ar8r_reconciliation.py'
    AUDIT_PATH = Path(__file__).resolve().parents[1] / 'scripts/check_source_alias_absence.py'
    OBSERVATIONS = []

    @staticmethod
    def _operational_functions(source_path, audit_path):
        constants = {
            'PMR007_DEEP_PREFIX', 'PMR007_DEEP_HISTORY', 'PMR007_DEEP_MANIFEST_SHA256',
            'PMR007_DEEP_DISTINCT_MEMBERS', 'PMR007_ROUNDS_PREFIX', 'PMR007_ROUNDS_HISTORY',
            'PMR007_ROUNDS_MANIFEST_SHA256', 'PMR007_ROUNDS_CONTEXT_MEMBER',
            'PMR007_ROUNDS_FORMALIZATION', 'PMR007_ROUNDS_FORMALIZATION_SHA256',
        }
        functions = {
            '_pmr007_deep_regular_file', '_pmr007_deep_member_bytes',
            '_pmr007_deep_original_members',
            '_pmr007_deep_duplicate_map', 'pmr007_deep_duplicate_paths',
            '_pmr007_rounds_original_members', 'pmr007_rounds_duplicate_paths',
            'pmr007_rounds_formalization_navigation',
        }
        selected, found = [], set()
        for node in ast.parse(source_path.read_bytes(), filename=str(source_path)).body:
            if isinstance(node, ast.FunctionDef) and node.name in functions:
                selected.append(node); found.add(node.name)
            elif (isinstance(node, ast.Assign) and len(node.targets) == 1
                  and isinstance(node.targets[0], ast.Name) and node.targets[0].id in constants):
                selected.append(node); found.add(node.targets[0].id)
        if found != constants | functions:
            raise AssertionError('Exact operational extraction population changed')
        namespace = {'ROOT': Path('/unused-synthetic-default'), 'Path': Path,
                     'hashlib': hashlib, 're': re, 'os': os,
                     'subprocess': types.SimpleNamespace()}
        # The current member getter uses the actual finite custody provider.
        # Load its entire operational dependency closure, never a permissive
        # path read or an empty catalogue. No resolver module is imported.
        resolver_path = source_path.with_name('resolve_t20_v6_source.py')
        resolver_constants = {'DIGEST_RECORD_BASE', 'DIGEST_RECORD_TREE_SHA256',
                              'DIGEST_RECORD_GROUPS', 'DIGEST_RECORD_PATHS'}
        resolver_functions = {
            'digest', '_administrative_git', '_binding_record_root',
            '_binding_record_present', '_binding_record_current_state',
            '_digest_record_root', '_digest_record_state',
            '_digest_record_current_bytes', '_digest_record_bound_bytes',
            '_digest_record_read', '_digest_record_catalog',
            '_digest_record_view_binding', 'digest_record_view_bytes',
        }
        resolver_selected, resolver_found = [], set()
        for node in ast.parse(resolver_path.read_bytes(), filename=str(resolver_path)).body:
            if isinstance(node, ast.FunctionDef) and node.name in resolver_functions:
                resolver_selected.append(node); resolver_found.add(node.name)
            elif (isinstance(node, ast.Assign) and len(node.targets) == 1
                  and isinstance(node.targets[0], ast.Name)
                  and node.targets[0].id in resolver_constants):
                resolver_selected.append(node); resolver_found.add(node.targets[0].id)
        if resolver_found != resolver_constants | resolver_functions:
            raise AssertionError('Exact digest custody dependency population changed')
        resolver_namespace = {'pathlib': pathlib, 'hashlib': hashlib, 're': re,
                              'os': os, 'stat': stat, 'subprocess': types.SimpleNamespace()}
        exec(compile(ast.Module(body=resolver_selected, type_ignores=[]),
                     str(resolver_path), 'exec'), resolver_namespace)
        namespace['DIGEST_RECORD_PATHS'] = resolver_namespace['DIGEST_RECORD_PATHS']
        namespace['digest_record_view_bytes'] = resolver_namespace['digest_record_view_bytes']
        exec(compile(ast.Module(body=selected, type_ignores=[]), str(source_path), 'exec'), namespace)
        audit_nodes = [node for node in ast.parse(audit_path.read_bytes(), filename=str(audit_path)).body
                       if isinstance(node, (ast.FunctionDef, ast.ClassDef))
                       and node.name in {'require', 'PublicFixtureAudit'}]
        if {node.name for node in audit_nodes} != {'require', 'PublicFixtureAudit'}:
            raise AssertionError('Exact public audit extraction population changed')
        audit_namespace = {'Path': Path, 'os': os, 'json': json, 'sys': sys, 'shutil': shutil,
                           '__file__': str(audit_path), '_PUBLIC_FIXTURE_NATIVE': None}
        exec(compile(ast.Module(body=audit_nodes, type_ignores=[]), str(audit_path), 'exec'), audit_namespace)
        return namespace, audit_namespace['PublicFixtureAudit']

    @staticmethod
    def _oid(body):
        return hashlib.sha1(b'blob ' + str(len(body)).encode('ascii') + b'\0' + body).hexdigest()

    def setUp(self):
        resources = Path(os.environ['PUBLIC123_REVISION_RESOURCES'])
        self.area = Path(self.enterContext(tempfile.TemporaryDirectory(prefix='reconciliation-', dir=resources)))
        self.cases = []
        self.addCleanup(self._record_cases)

    def _record_cases(self):
        self.OBSERVATIONS.append({'test': self.id(), 'cases': self.cases})

    def _write(self, relative, body, mode=0o644):
        path = self.repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body); path.chmod(mode)
        return path

    def _make(self, kind, *, aliases_present=True):
        self.namespace, audit_class = self._operational_functions(self.SOURCE_PATH, self.AUDIT_PATH)
        self.repo = self.area / ('case-' + str(len(self.cases)))
        self.repo.mkdir()
        state = self.repo / 'audit-state'; state.mkdir()
        self.audit = audit_class(self.repo, state)
        self.case = {'kind': kind, 'attempts': [], 'admitted': []}
        self.cases.append(self.case)
        self.kind = kind
        self.prefix = self.namespace['PMR007_' + kind.upper() + '_PREFIX']
        self.canonical_prefix = self.prefix.replace('pmr007-rounds11-20', 'pmr007-deep-a-bk').replace('a-ap', 'a-bk')
        self.history = self.namespace['PMR007_' + kind.upper() + '_HISTORY']
        if kind == 'deep':
            duplicate_relatives = ['SYNTHETIC_MEMBERS/member_%04d.txt' % i for i in range(824)]
            relatives = duplicate_relatives + sorted(self.namespace['PMR007_DEEP_DISTINCT_MEMBERS'])
        else:
            duplicate_relatives = (['PROPOSED_THEOREM_FILES/member_%02d.txt' % i for i in range(9)]
                                   + ['SYNTHETIC_MEMBERS/member_%03d.txt' % i for i in range(89)])
            duplicate_relatives.append(self.namespace['PMR007_ROUNDS_CONTEXT_MEMBER'])
            relatives = duplicate_relatives + ['SYNTHETIC_DISTINCT/member_%02d.txt' % i for i in range(31)]
        self.members, self.tree_rows, self.responses = {}, {}, {}
        self.duplicates = {}
        for number, relative in enumerate(relatives):
            body = ('inert public fixture group %02d\n' % (number % 7)).encode('ascii')
            oid = self._oid(body)
            self.members[relative] = hashlib.sha256(body).hexdigest()
            self.responses[oid] = (0, body)
            alias, canonical = self.prefix + '/' + relative, self.canonical_prefix + '/' + relative
            self.tree_rows[alias] = ('100644', 'blob', oid)
            if relative in duplicate_relatives:
                self.tree_rows[canonical] = self.tree_rows[alias]
                self._write(canonical, body)
                if aliases_present: self._write(alias, body)
                self.duplicates[alias] = canonical
        if kind == 'rounds':
            del self.duplicates[self.prefix + '/' + self.namespace['PMR007_ROUNDS_CONTEXT_MEMBER']]
        self._manifest(self.members)
        self.ls_tree_result = None
        self.index_result = None
        self.namespace['subprocess'].run = self._run
        self.digest_namespace = self.namespace['digest_record_view_bytes'].__globals__
        self.digest_namespace['subprocess'].run = self._digest_run
        self.original_navigation = None
        if kind == 'rounds':
            theorem_paths = [name for name in sorted(self.duplicates) if '/PROPOSED_THEOREM_FILES/' in name]
            original = b'schema: synthetic-operational-only\nstatus: UNADOPTED\n'
            original += b''.join(('source_path: ' + name.removeprefix('docs/project-closure/ar8r-v11/') + '\n').encode()
                                 for name in theorem_paths)
            original += b'controls: retain-every-field\n'
            self._navigation(original)
        self.case['manifest_rows'] = len(self.members)
        self.case['qualified_aliases'] = len(self.duplicates)
        return self

    def _manifest(self, members):
        body = ''.join(digest + '  ' + relative + '\n' for relative, digest in sorted(members.items())).encode()
        self._write(self.prefix + '/SHA256SUMS', body)
        # Only synthetic fixture identities are substituted. Production counts,
        # modes, paths, pinned revision, equality predicates and audit stay exact.
        self.namespace['PMR007_' + self.kind.upper() + '_MANIFEST_SHA256'] = hashlib.sha256(body).hexdigest()

    def _navigation(self, original):
        self.original_navigation = original
        self.namespace['PMR007_ROUNDS_FORMALIZATION_SHA256'] = hashlib.sha256(original).hexdigest()
        self.navigation_path = self.namespace['PMR007_ROUNDS_FORMALIZATION']
        self.navigation_selector = self.history + ':' + self.navigation_path
        self.responses[self.navigation_selector] = (0, original)
        expected = original
        for alias in sorted(self.duplicates):
            if '/PROPOSED_THEOREM_FILES/' in alias:
                old = ('source_path: ' + alias.removeprefix('docs/project-closure/ar8r-v11/')).encode()
                expected = expected.replace(old, old.replace(b'pmr007-rounds11-20/', b'pmr007-deep-a-bk/'))
        self.current_navigation = expected
        self._write(self.navigation_path, expected)

    def _tree_bytes(self):
        return b''.join((' '.join(metadata) + '\t' + path + '\0').encode()
                        for path, metadata in sorted(self.tree_rows.items()))

    def _run(self, argv, *, cwd, capture_output, check, env, **kwargs):
        self.case['attempts'].append(list(argv[4:7]))
        self.audit.audit('subprocess.Popen', (argv[0], argv, str(cwd), env))
        self.case['admitted'].append(list(argv[4:7]))
        self.assertEqual(argv[:4], ['git', '--no-replace-objects', '-c', 'core.fsmonitor=false'])
        self.assertEqual(Path(cwd), self.repo)
        self.assertTrue(capture_output); self.assertFalse(check)
        self.assertEqual(env['GIT_NO_LAZY_FETCH'], '1')
        self.assertEqual(env['GIT_TERMINAL_PROMPT'], '0')
        self.assertEqual(kwargs, {})
        command = argv[4:]
        if command[0] == 'ls-tree':
            paths = (sorted(set(self.duplicates) | set(self.duplicates.values())) if self.kind == 'deep'
                     else [self.prefix, self.canonical_prefix])
            self.assertEqual(command, ['ls-tree', '-r', '-z', '--full-tree', self.history, '--', *paths])
            code, body = self.ls_tree_result if self.ls_tree_result is not None else (0, self._tree_bytes())
        elif command[0] == 'cat-file':
            self.assertEqual(command[:2], ['cat-file', 'blob'])
            self.assertEqual(len(command), 3)
            self.assertIn(command[2], self.responses)
            code, body = self.responses[command[2]]
        elif command[0] == 'ls-files':
            self.assertEqual(command, ['ls-files', '--stage', '-z', '--', self.navigation_path])
            required = ('100644 ' + self._oid(self.current_navigation) + ' 0\t' + self.navigation_path + '\0').encode()
            code, body = self.index_result if self.index_result is not None else (0, required)
        else:
            self.fail('Unexpected synthetic native command: ' + repr(command))
        return subprocess.CompletedProcess(argv, code, body, b'')

    def _digest_run(self, argv, *, cwd, capture_output, check, env):
        """An unavailable synthetic history still passes through the real audit."""
        command = ['git', '--no-replace-objects', '--literal-pathspecs',
                   'cat-file', 'commit', self.digest_namespace['DIGEST_RECORD_BASE']]
        self.case.setdefault('digest_attempts', []).append(list(argv))
        self.audit.audit('subprocess.Popen', (argv[0], argv, str(cwd), env))
        self.assertEqual(argv, command)
        self.assertEqual(Path(cwd), self.repo)
        self.assertTrue(capture_output); self.assertFalse(check)
        for key, value in {'GIT_NO_LAZY_FETCH': '1', 'GIT_NO_REPLACE_OBJECTS': '1',
                           'GIT_ALLOW_PROTOCOL': '', 'GIT_OPTIONAL_LOCKS': '0',
                           'GIT_TERMINAL_PROMPT': '0'}.items():
            self.assertEqual(env[key], value)
        return subprocess.CompletedProcess(argv, 1, b'', b'synthetic history unavailable')

    def _qualify(self):
        return self.namespace['pmr007_' + self.kind + '_duplicate_paths'](self.repo)

    def _navigate(self, *, indexed=True):
        return self.namespace['pmr007_rounds_formalization_navigation'](self.repo, indexed=indexed)

    def _object_queries(self):
        return [event['argv'][6] for event in self.audit.events if event['argv'][4:6] == ['cat-file', 'blob']]

    def test_deep_exact_objects_pass_actual_audit(self):
        self._make('deep')
        self.assertEqual(self._qualify(), set(self.duplicates))
        self.assertEqual(len(self.duplicates), 824)
        expected = sorted({self.tree_rows[name][2] for name in self.duplicates})
        self.assertEqual(self._object_queries(), expected)
        self.assertEqual(len(self.audit.events), 1 + len(expected))

    def test_rounds_exact_objects_pass_actual_audit(self):
        self._make('rounds')
        self.assertEqual(self._qualify(), set(self.duplicates))
        self.assertEqual(len(self.duplicates), 98)
        expected = sorted({self.tree_rows[name][2] for name in self.duplicates})
        self.assertEqual(self._object_queries(), expected)
        self.assertNotIn(self.prefix + '/' + self.namespace['PMR007_ROUNDS_CONTEXT_MEMBER'], self._qualify())

    def test_absent_synthetic_aliases_keep_finite_qualification(self):
        for kind in ('deep', 'rounds'):
            with self.subTest(kind=kind):
                self._make(kind, aliases_present=False)
                self.assertEqual(self._qualify(), set(self.duplicates))
                self.assertTrue(all(not (self.repo / name).exists() for name in self.duplicates))

    def test_navigation_and_index_pass_actual_audit(self):
        self._make('rounds')
        for indexed in (True, False):
            with self.subTest(indexed=indexed):
                self.assertEqual(self._navigate(indexed=indexed), self.navigation_path)
        self.assertEqual((self.repo / self.navigation_path).read_bytes(), self.current_navigation)
        self.assertEqual(self.current_navigation.count(b'source_path: '), 9)
        self.assertEqual(self._object_queries().count(self.navigation_selector), 2)

    def test_navigation_original_read_passes_actual_audit(self):
        self._make('rounds')
        # Isolate the downstream read from duplicate qualification to expose the
        # old `show` failure independently of the old `--batch` failure. The
        # preceding test executes both actual functions without this test seam.
        self.namespace['pmr007_rounds_duplicate_paths'] = lambda repo: set(self.duplicates)
        self.assertEqual(self._navigate(), self.navigation_path)
        self.assertEqual(self._object_queries(), [self.navigation_selector])

    def test_object_failure_length_and_digest_guards(self):
        for kind in ('deep', 'rounds'):
            for corruption in ('failed', 'short', 'trailing', 'same-length'):
                with self.subTest(kind=kind, corruption=corruption):
                    self._make(kind)
                    oid = sorted({self.tree_rows[name][2] for name in self.duplicates})[0]
                    body = self.responses[oid][1]
                    self.responses[oid] = {
                        'failed': (1, body), 'short': (0, body[:-1]),
                        'trailing': (0, body + b'\n'), 'same-length': (0, b'X' * len(body)),
                    }[corruption]
                    with self.assertRaisesRegex(ValueError, 'original-git-(objects-unavailable|.*content-mismatch)'):
                        self._qualify()

    def test_native_blob_oid_still_authenticates_body(self):
        for kind in ('deep', 'rounds'):
            with self.subTest(kind=kind):
                self._make(kind)
                old = self.tree_rows[sorted(self.duplicates)[0]][2]
                different_oid = self._oid(b'other synthetic native object\n')
                for name, metadata in list(self.tree_rows.items()):
                    if metadata[2] == old: self.tree_rows[name] = (*metadata[:2], different_oid)
                self.responses[different_oid] = self.responses[old]
                # Length and expected SHA-256 still match; native SHA-1 must fail.
                with self.assertRaisesRegex(ValueError, 'content-mismatch'): self._qualify()

    def test_expected_sha256_still_authenticates_body(self):
        for kind in ('deep', 'rounds'):
            with self.subTest(kind=kind):
                self._make(kind)
                old = self.tree_rows[sorted(self.duplicates)[0]][2]
                different_body = b'X' * len(self.responses[old][1])
                different_oid = self._oid(different_body)
                for name, metadata in list(self.tree_rows.items()):
                    if metadata[2] == old: self.tree_rows[name] = (*metadata[:2], different_oid)
                self.responses[different_oid] = (0, different_body)
                # Length and native SHA-1 match; the original SHA-256 must fail.
                with self.assertRaisesRegex(ValueError, 'content-mismatch'): self._qualify()

    def test_pinned_history_and_equal_native_identity_are_required(self):
        for kind in ('deep', 'rounds'):
            for corruption in ('unavailable', 'malformed', 'missing', 'mode', 'type', 'unequal'):
                with self.subTest(kind=kind, corruption=corruption):
                    self._make(kind)
                    alias = sorted(self.duplicates)[0]
                    canonical = self.duplicates[alias]
                    original = self.tree_rows[alias]
                    if corruption == 'unavailable': self.ls_tree_result = (1, b'')
                    elif corruption == 'malformed': self.ls_tree_result = (0, b'malformed-native-record\0')
                    elif corruption == 'missing': del self.tree_rows[alias]
                    elif corruption == 'mode': self.tree_rows[alias] = ('100755', *original[1:])
                    elif corruption == 'type': self.tree_rows[alias] = (original[0], 'tree', original[2])
                    else: self.tree_rows[canonical] = (*original[:2], self._oid(b'other synthetic identity'))
                    with self.assertRaises(ValueError): self._qualify()

    def test_current_canonical_and_present_alias_guards(self):
        for kind in ('deep', 'rounds'):
            for target_kind in ('canonical', 'alias'):
                for corruption in ('bytes', 'executable', 'symlink', 'missing-parent'):
                    with self.subTest(kind=kind, target=target_kind, corruption=corruption):
                        self._make(kind)
                        alias = sorted(self.duplicates)[0]
                        target = self.repo / (self.duplicates[alias] if target_kind == 'canonical' else alias)
                        if corruption == 'bytes': target.write_bytes(b'corrupt synthetic public body\n')
                        elif corruption == 'executable': target.chmod(0o755)
                        elif corruption == 'symlink':
                            target.unlink(); target.symlink_to(self.repo / 'absent-synthetic-target')
                        else:
                            # A symlink component must fail even when it leads to
                            # the same regular inert bytes inside this fixture.
                            parent = target.parent
                            relocated = parent.with_name(parent.name + '-moved')
                            parent.rename(relocated); parent.symlink_to(relocated, target_is_directory=True)
                        with self.assertRaises(ValueError): self._qualify()

    def test_digest_manifest_retains_current_inode_witness(self):
        # Clearing the finite set or substituting an ordinary read loses this
        # descriptor witness and must fail this consumer-facing control.
        for kind in ('deep', 'rounds'):
            with self.subTest(kind=kind):
                self._make(kind)
                relative = self.prefix + '/SHA256SUMS'
                target = self.repo / relative
                original = target.read_bytes()
                native_open, replacements = os.open, []
                def replace_before_open(name, flags, *args, **kwargs):
                    if not isinstance(name, int) and Path(name) == target:
                        self.assertFalse(replacements)
                        target.rename(target.with_name('parked-inert-manifest'))
                        target.write_bytes(original)
                        replacements.append(relative)
                    return native_open(name, flags, *args, **kwargs)
                with patch.object(os, 'open', side_effect=replace_before_open):
                    with self.assertRaisesRegex(ValueError, 'current descriptor changed'):
                        self.namespace['_pmr007_deep_member_bytes'](self.repo, relative)
                self.assertEqual(replacements, [relative])

    def test_missing_digest_manifest_keeps_history_failure_closed(self):
        for kind in ('deep', 'rounds'):
            with self.subTest(kind=kind):
                self._make(kind)
                relative = self.prefix + '/SHA256SUMS'
                (self.repo / relative).unlink()
                with self.assertRaisesRegex(OSError, 'historical digest is unavailable'):
                    self.namespace['_pmr007_deep_member_bytes'](self.repo, relative)
                self.assertFalse((self.repo / relative).exists())
                self.assertEqual(len(self.case['digest_attempts']), 1)
                self.assertEqual(self.audit.private_denials, [])

    def test_manifest_and_original_source_count_guards(self):
        for kind in ('deep', 'rounds'):
            for corruption in ('identity', 'count', 'duplicate-row', 'invalid-digest'):
                with self.subTest(kind=kind, corruption=corruption):
                    self._make(kind)
                    path = self.repo / self.prefix / 'SHA256SUMS'
                    if corruption == 'identity': path.write_bytes(path.read_bytes() + b'changed\n')
                    elif corruption == 'count':
                        members = dict(self.members); members.pop(sorted(self.duplicates)[0].removeprefix(self.prefix + '/'))
                        self._manifest(members)
                    else:
                        lines = path.read_bytes().splitlines(keepends=True)
                        body = b''.join(lines + [lines[0]]) if corruption == 'duplicate-row' else b'g' * 64 + lines[0][64:] + b''.join(lines[1:])
                        path.write_bytes(body)
                        self.namespace['PMR007_' + kind.upper() + '_MANIFEST_SHA256'] = hashlib.sha256(body).hexdigest()
                    with self.assertRaisesRegex(ValueError, 'original-manifest-'): self._qualify()

    def test_rounds_context_and_exact_equality_count(self):
        for corruption in ('context', 'too-many', 'too-few'):
            with self.subTest(corruption=corruption):
                self._make('rounds')
                if corruption == 'context':
                    relative = self.namespace['PMR007_ROUNDS_CONTEXT_MEMBER']
                    del self.tree_rows[self.canonical_prefix + '/' + relative]
                elif corruption == 'too-many':
                    relative = 'SYNTHETIC_DISTINCT/member_00.txt'
                    self.tree_rows[self.canonical_prefix + '/' + relative] = self.tree_rows[self.prefix + '/' + relative]
                else: del self.tree_rows[sorted(self.duplicates)[0]]
                with self.assertRaisesRegex(ValueError, 'original-equality-class-mismatch'): self._qualify()

    def test_deep_distinct_member_names_are_retained(self):
        self._make('deep')
        members = dict(self.members)
        distinct = sorted(self.namespace['PMR007_DEEP_DISTINCT_MEMBERS'])[0]
        members['UNEXPECTED_SYNTHETIC_MEMBER.txt'] = members.pop(distinct)
        self._manifest(members)
        with self.assertRaisesRegex(ValueError, 'distinct-member-set-mismatch'): self._qualify()

    def test_navigation_original_pin_and_exact_nine_changes(self):
        for corruption in ('unavailable', 'pin', 'eight', 'ten'):
            with self.subTest(corruption=corruption):
                self._make('rounds')
                if corruption == 'unavailable': self.responses[self.navigation_selector] = (1, self.original_navigation)
                elif corruption == 'pin': self.responses[self.navigation_selector] = (0, self.original_navigation + b'changed\n')
                else:
                    lines = self.original_navigation.splitlines(keepends=True)
                    route = next(line for line in lines if line.startswith(b'source_path: '))
                    original = self.original_navigation.replace(route, b'', 1) if corruption == 'eight' else self.original_navigation + route
                    self._navigation(original)
                with self.assertRaisesRegex(ValueError, 'original-formalization-unavailable|formalization-navigation-mismatch'):
                    self._navigate()

    def test_navigation_current_regular_bytes_and_mode(self):
        for corruption in ('bytes', 'executable', 'symlink', 'parent-symlink'):
            with self.subTest(corruption=corruption):
                self._make('rounds')
                path = self.repo / self.navigation_path
                if corruption == 'bytes': path.write_bytes(self.current_navigation + b'changed\n')
                elif corruption == 'executable': path.chmod(0o755)
                elif corruption == 'symlink':
                    path.unlink(); path.symlink_to(self.repo / 'absent-synthetic-target')
                else:
                    parent = path.parent; relocated = parent.with_name(parent.name + '-moved')
                    parent.rename(relocated); parent.symlink_to(relocated, target_is_directory=True)
                with self.assertRaises(ValueError): self._navigate()

    def test_navigation_exact_index_entry_guards(self):
        for corruption in ('unavailable', 'oid', 'mode', 'stage', 'extra'):
            with self.subTest(corruption=corruption):
                self._make('rounds')
                entry = ('100644 ' + self._oid(self.current_navigation) + ' 0\t' + self.navigation_path + '\0').encode()
                if corruption == 'unavailable': self.index_result = (1, entry)
                elif corruption == 'oid': self.index_result = (0, entry.replace(self._oid(self.current_navigation).encode(), self._oid(b'other synthetic index').encode()))
                elif corruption == 'mode': self.index_result = (0, entry.replace(b'100644 ', b'100755 ', 1))
                elif corruption == 'stage': self.index_result = (0, entry.replace(b' 0\t', b' 1\t', 1))
                else: self.index_result = (0, entry + entry)
                with self.assertRaisesRegex(ValueError, 'indexed-formalization-navigation-mismatch'): self._navigate()

    def test_actual_audit_refuses_forbidden_command_shapes(self):
        self._make('rounds')
        oid = self._oid(b'only synthetic native data')
        for command in (['cat-file', '--batch'], ['cat-file', '--batch-check'], ['cat-file', '-s', oid],
                        ['show', self.navigation_selector], ['fetch'], ['ls-tree', '-l', self.history],
                        ['ls-tree', '--long', self.history]):
            with self.subTest(command=command):
                argv = ['git', '--no-replace-objects', '-c', 'core.fsmonitor=false', *command]
                with self.assertRaises(RuntimeError):
                    self.audit.audit('subprocess.Popen', ('git', argv, str(self.repo), {}))
        self.assertEqual(self.audit.events, [])

    def test_actual_audit_refuses_synthetic_hold_coordinates(self):
        self._make('rounds')
        held_oid = self._oid(b'synthetic held object, never requested from native Git')
        held_path = 'SYNTHETIC_HELD/member.txt'
        self.audit.held_coordinates = {held_oid, held_path}
        for selector in (held_oid, self.history + ':' + held_path):
            with self.subTest(selector=selector):
                argv = ['git', '--no-replace-objects', '-c', 'core.fsmonitor=false', 'cat-file', 'blob', selector]
                with self.assertRaises(PermissionError):
                    self.audit.audit('subprocess.Popen', ('git', argv, str(self.repo), {}))
        self.assertEqual(len(self.audit.private_denials), 2)
        self.assertEqual(self.audit.events, [])

    def test_actual_audit_refuses_other_roots_and_index_mutation(self):
        self._make('rounds')
        for command, cwd in ((['cat-file', 'blob', self.navigation_selector], self.area),
                             (['update-index', '--remove', 'SYNTHETIC_MEMBER.txt'], self.repo)):
            with self.subTest(command=command):
                argv = ['git', '--no-replace-objects', '-c', 'core.fsmonitor=false', *command]
                with self.assertRaises(RuntimeError):
                    self.audit.audit('subprocess.Popen', ('git', argv, str(cwd), {}))
        self.assertEqual(self.audit.events, [])



if __name__ == '__main__': unittest.main()
