"""Synthetic admission controls; these tests never remove repository sources."""
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
import hashlib
import os
import tempfile
import unittest

import source_alias_absence_population as population


def finite_fixture():
    digest = 'a' * 64
    original = ('100644', 'blob', 'b' * 40, 17)
    prefix = 'snapshots/deep/a-ap'
    retained_prefix = 'snapshots/deep/a-bk'
    rounds_prefix = 'snapshots/rounds'
    copies = {f'{prefix}/member-{i}': f'{retained_prefix}/member-{i}' for i in range(824)}
    deep = {f'member-{i}': digest for i in range(824)}
    rounds = {f'member-{i}': digest for i in range(98)}
    round_aliases = {f'{rounds_prefix}/{name}' for name in rounds}
    catalog = {f'continuations/member-{i}.lean': {'canonical': f'successors/member-{i}.lean',
        'sha256': digest, 'bytes': 17, 'blob': original[2]} for i in range(258)}
    snapshot = SimpleNamespace(PMR007_DEEP_PREFIX=prefix, PMR007_ROUNDS_PREFIX=rounds_prefix,
        PMR007_ROUNDS_CONTEXT_MEMBER='Round19.md',
        _pmr007_deep_original_members=lambda repo: deep,
        _pmr007_deep_duplicate_map=lambda members: copies,
        _pmr007_rounds_original_members=lambda repo: rounds,
        pmr007_rounds_duplicate_paths=lambda repo: round_aliases)
    source = SimpleNamespace(CONTINUATION_COPY_ROOT='continuations/', CONTINUATION_COPY_EXCLUDED='excluded',
        _continuation_copy_catalog=lambda repo: catalog)
    paths = set(copies) | set(copies.values()) | set(catalog) | {x['canonical'] for x in catalog.values()} | round_aliases
    required = {f'{rounds_prefix}/required-{i}' for i in range(31)} | {
        f'{rounds_prefix}/SHA256SUMS', f'{rounds_prefix}/Round19.md'}
    paths |= required | {'continuations/excluded.lean'}
    originals = {path: original for path in paths}
    identity = lambda repo, relative, row: {'sha256': digest, 'bytes': row[3], 'blob': row[2], 'mode': row[0]}
    return snapshot, source, copies, deep, catalog, originals, identity, required


class PopulationAdmissionControls(unittest.TestCase):
    def setUp(self):
        (self.snapshot, self.source, self.copies, self.deep, self.catalog,
         self.originals, self.identity, self.required) = finite_fixture()
        self.enterContext(patch.object(population, 'public_consumers', return_value=(self.snapshot, self.source)))
        self.enterContext(patch.object(population, 'original_tree', return_value=self.originals))
        self.enterContext(patch.object(population, 'public_identity', side_effect=self.identity))

    def test_complete_artificial_partition_and_required_population(self):
        rows = population.derive_classes(Path('/artificial-repository'))
        self.assertEqual(len(rows), 1180)
        self.assertEqual(len({r['canonical'] for r in rows}), 1082)
        self.assertEqual(population.derive_required(Path('/artificial-repository'), rows), sorted(self.required))

    def test_missing_alias_refuses_changed_population(self):
        self.copies.pop(next(iter(self.copies)))
        with self.assertRaisesRegex(ValueError, 'population differs'):
            population.derive_classes(Path('/artificial-repository'))

    def test_original_blob_mismatch_refuses_before_acceptance(self):
        alias = next(iter(self.copies))
        self.originals[alias] = ('100644', 'blob', 'c' * 40, 17)
        with self.assertRaisesRegex(ValueError, 'original tree identities differ'):
            population.derive_classes(Path('/artificial-repository'))

    def test_public_owner_digest_mismatch_refuses(self):
        self.deep['member-0'] = 'f' * 64
        with self.assertRaisesRegex(ValueError, 'Public owner digest differs'):
            population.derive_classes(Path('/artificial-repository'))

    def test_alias_cannot_be_a_retained_counterpart(self):
        aliases = list(self.copies)
        self.copies[aliases[0]] = aliases[1]
        with self.assertRaisesRegex(ValueError, 'population differs'):
            population.derive_classes(Path('/artificial-repository'))

    def test_excluded_continuation_refuses_even_with_unchanged_counts(self):
        row = self.catalog.pop(next(iter(self.catalog)))
        self.catalog['continuations/excluded.lean'] = row
        with self.assertRaisesRegex(ValueError, 'Excluded original selected'):
            population.derive_classes(Path('/artificial-repository'))

    def test_missing_required_manifest_refuses_even_with_unchanged_counts(self):
        rows = population.derive_classes(Path('/artificial-repository'))
        self.originals['snapshots/rounds/extra'] = self.originals.pop('snapshots/rounds/SHA256SUMS')
        with self.assertRaisesRegex(ValueError, 'Required manifest/context original missing'):
            population.derive_required(Path('/artificial-repository'), rows)


class PublicFileIdentityControls(unittest.TestCase):
    def setUp(self):
        self.root = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.path = self.root / 'sample.txt'
        self.body = b'finite-data\n'
        self.path.write_bytes(self.body)
        self.path.chmod(0o644)
        blob = hashlib.sha1(b'blob ' + str(len(self.body)).encode() + b'\0' + self.body).hexdigest()
        self.original = ('100644', 'blob', blob, len(self.body))

    def test_real_artificial_file_identity(self):
        value = population.public_identity(self.root, 'sample.txt', self.original)
        self.assertEqual(value['sha256'], hashlib.sha256(self.body).hexdigest())

    def test_same_size_body_change_refuses(self):
        self.path.write_bytes(b'finite-datA\n')
        with self.assertRaisesRegex(ValueError, 'Git identity differs'):
            population.public_identity(self.root, 'sample.txt', self.original)

    def test_changed_mode_refuses(self):
        self.path.chmod(0o600)
        with self.assertRaisesRegex(ValueError, 'mode/size/link differs'):
            population.public_identity(self.root, 'sample.txt', self.original)

    def test_extra_artificial_hardlink_refuses(self):
        os.link(self.path, self.root / 'alias.txt')
        with self.assertRaisesRegex(ValueError, 'mode/size/link differs'):
            population.public_identity(self.root, 'sample.txt', self.original)

    def test_symlink_and_traversal_refuse(self):
        (self.root / 'link.txt').symlink_to(self.path)
        for relative in ('link.txt', '../sample.txt', '.git/index', '/sample.txt'):
            with self.subTest(path=relative), self.assertRaises(ValueError):
                population.public_identity(self.root, relative, self.original)





class PublicFixturePopulationControls(unittest.TestCase):
    def test_native_tree_metadata_never_requests_object_sizes(self):
        import subprocess
        with tempfile.TemporaryDirectory(prefix='public123-native-tree-') as temporary:
            root = Path(temporary)
            env = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
                       GIT_CONFIG_SYSTEM=os.devnull, GIT_NO_LAZY_FETCH='1',
                       GIT_NO_REPLACE_OBJECTS='1', GIT_ALLOW_PROTOCOL='',
                       GIT_AUTHOR_NAME='Fixture', GIT_AUTHOR_EMAIL='fixture@example.invalid',
                       GIT_COMMITTER_NAME='Fixture', GIT_COMMITTER_EMAIL='fixture@example.invalid')
            def git(*args):
                return subprocess.check_output(['/usr/bin/git', '--no-replace-objects', *args], cwd=root, env=env)
            git('-c', 'init.templateDir=', 'init', '-q')
            (root / 'public.json').write_bytes(b'{"public":true}\n')
            git('add', '--', 'public.json')
            git('commit', '-qm', 'Public metadata fixture')
            revision = git('rev-parse', 'HEAD').decode().strip()
            rows = population.original_metadata_tree(root, revision)
            oid = hashlib.sha1(b'blob 16\0' + b'{"public":true}\n').hexdigest()
            self.assertEqual(rows, {'public.json': ('100644', 'blob', oid)})
            for bad in ('HEAD', revision + ':public.json', '--all', ''):
                with self.subTest(revision=bad), self.assertRaises(ValueError):
                    population.original_metadata_tree(root, bad)

    def test_complete_public_row_contract_preserves_roles_and_status_fields(self):
        body = b'public fixture\n'
        path = 'experiments/episode-reification/fixtures/E1/baseline-log.md'
        digest = hashlib.sha256(body).hexdigest()
        row = {'source_sha256': digest, 'source_action': 'include', 'source_bytes': len(body),
               'role': 'authored_argument', 'declared_eligibility_basis': 'reviewed_owner_authored',
               'required_dependencies': [], 'disposition': 'REUSE', 'repository_path': path,
               'public_sha256': digest, 'public_bytes': len(body),
               'publication_basis': 'exact_existing_public_repository_object'}
        self.assertEqual(population.public_fixture_row(path, body, row), row)
        for field, value in [('role', 'new_proof'), ('disposition', 'ADD_EXACT'),
                             ('source_action', 'exclude'), ('required_dependencies', ['new-source']),
                             ('public_bytes', len(body) + 1), ('unadmitted_field', True)]:
            with self.subTest(field=field), self.assertRaises(ValueError):
                population.public_fixture_row(path, body, dict(row, **{field: value}))

    def test_partial_duplicate_or_unbound_population_cannot_be_admitted(self):
        for rows in ([], [{'path': 'x'}], [{'path': 'x'}] * 123):
            with self.subTest(count=len(rows)), self.assertRaises((ValueError, KeyError, TypeError)):
                population.validate_public_fixture_population(rows)


if __name__ == '__main__':
    unittest.main()
