"""Artificial hosted-coordinate and protected-metadata refusal controls."""
from pathlib import Path
from unittest.mock import patch
import os
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest

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


if __name__ == '__main__': unittest.main()
