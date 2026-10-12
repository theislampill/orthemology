"""Synthetic final-handoff controls. Retained sentinel sources are never executed."""
import ast
import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
import plan_selection as p
import materialise_selection as m


def load(name):
    path = HERE / (name + '.py')
    if not path.exists():
        raise AssertionError(name + ' is not implemented')
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class HandoffControls(unittest.TestCase):
    def setUp(self):
        self.v = load('verify_handoff')
        self.b = load('prepare_handoff')
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.sources = self.root / 'sources'; self.sources.mkdir()
        self.data = b'raise RuntimeError("retained source must never execute")\n'
        self.h = p.digest(self.data)
        self.tool = (HERE / 'verify_handoff.py').read_bytes()
        self.th = p.digest(self.tool)
        self.original = 'e' * 64
        self.received = b'received public body\n'; self.rh = p.digest(self.received)
        self.qualification = {'schema': 't20-received-public-qualification-v1',
            'public_sha256': self.rh, 'original_sha256': self.original,
            'repository': 'theislampill/orthemology', 'commit': '7' * 40,
            'repository_path': 'research/source.md',
            'source_reading': {'ledger_sha256': '9' * 64, 'pointer': '$/records/5', 'scope': 'complete_body'},
            'equivalence_to_original': 'unverified_original_unavailable'}
        self.qdata = p.canonical(self.qualification); self.qh = p.digest(self.qdata)
        self.bodies = {self.h: self.data, self.th: self.tool, self.rh: self.received, self.qh: self.qdata}
        views = {self.h: ['research/sentinel.py', 'START_HERE.md'], self.th: ['tools/verify_handoff.py'],
                 self.rh: ['research/received.md'], self.qh: ['metadata/qualification.json']}
        rows = []; lookup = {}
        for h, data in self.bodies.items():
            (self.sources / h).write_bytes(data)
            lookup[h] = {'sha256': h, 'bytes': len(data), 'source_path': 'sources/' + h,
                'source_hash_verified': True, 'reviewed_digest': h, 'current_path_digest': h,
                'prior_exclusion_reasons': [], 'sensitive_screen_flags': []}
            rows.append({'sha256': h, 'action': 'include', 'scope_status': 'source-only',
                'eligibility': {'basis': 'reviewed_owner_authored', 'decision_reference': 'reviewed-selection',
                    'content_reviewed_for_distribution': True, 'resolved_historical_role_filters': []},
                'role': 'authored_code', 'required_dependencies': [],
                'views': [{'packet': 'fixture', 'path': path} for path in views[h]]})
        # Planner requires packet/member views. Final curated paths must exactly match plan views.
        rows[0]['views'] = [{'packet': 'research', 'path': 'sentinel.py'}, {'packet': 'reader', 'path': 'START_HERE.md'}]
        for row in rows:
            if row['sha256'] == self.th: row['views'] = [{'packet': 'tools', 'path': 'verify_handoff.py'}]
            if row['sha256'] == self.rh:
                row.update(original_sha256=self.original, received_public_qualification_sha256=self.qh)
                row['eligibility']['basis'] = 'reviewed_received_public_version'
            if row['sha256'] == self.qh: row['role'] = 'qualified_metadata'
        rows.append({'sha256': self.original, 'action': 'identity_only', 'scope_status': 'unavailable'})
        lookup[self.original] = {'sha256': self.original, 'source_hash_verified': False, 'current_path_digest': None}
        selection = {'schema': p.SCHEMA, 'assembly_authorized': False, 'audience': 'owner_private_handoff',
            'decision_reference': 'reviewed-selection', 'destination': 'handoff-v6',
            'baseline_policy': 'separate_unchanged_owner_checkpoint', 'lookup_sha256': 'b'*64,
            'v5_index_sha256': 'c'*64, 'exclusions_sha256': 'd'*64, 'v5_archive_sha256': 'a'*64, 'objects': rows}
        self.result = p.build_plan(selection, lookup, {'zip_sha256': 'a'*64, 'members': []}, {}, self.root)
        self.source = self.root / 'materialised'; m.materialise(self.result, self.source, [self.sources], self.root)
        self.entries = [{'path': 'START_HERE.md', 'source_view': 'reader/START_HERE.md', 'sha256': self.h},
                        {'path': 'tools/verify_handoff.py', 'source_view': 'tools/verify_handoff.py', 'sha256': self.th}]
        self.declaration = {'schema': 't20-v6-curated-entry-declaration-v1', 'entries': copy.deepcopy(self.entries)}
        self.out = self.root / 'handoff'

    def prepare(self):
        return self.b.prepare(self.source, self.declaration, self.out)

    def manifest(self):
        return p.parse((self.out / 'PACKAGE_MANIFEST.json').read_bytes())

    def rewrite_manifest(self, manifest):
        (self.out / 'PACKAGE_MANIFEST.json').write_bytes(p.canonical(manifest))

    def refresh_inventory(self):
        manifest = self.manifest()
        for row in manifest['files']:
            raw = (self.out / row['path']).read_bytes()
            row.update(sha256=p.digest(raw), bytes=len(raw))
        self.rewrite_manifest(manifest)

    def reject(self):
        with self.assertRaises(ValueError): self.v.verify(self.out)

    def test_complete_finite_manifest_and_exact_preserved_inputs(self):
        before = {str(f.relative_to(self.source)): f.read_bytes() for f in self.source.rglob('*') if f.is_file()}
        original_before = {f.name: f.read_bytes() for f in self.sources.iterdir()}
        result = self.prepare(); report = self.v.verify(self.out)
        self.assertEqual(result['manifest_sha256'], report['manifest_sha256'])
        self.assertEqual(report['state'], 'VERIFIED_SOURCE_ONLY_HANDOFF')
        self.assertFalse(report['source_execution_selected'])
        for name, raw in before.items():
            self.assertEqual((self.source / name).read_bytes(), raw)
            self.assertEqual((self.out / name).read_bytes(), raw)
        self.assertEqual({f.name: f.read_bytes() for f in self.sources.iterdir()}, original_before)
        self.assertEqual((self.out / 'START_HERE.md').read_bytes(), self.data)
        self.assertFalse((self.out / 'research').exists())
        self.assertEqual(len(list((self.out / 'authored_objects').glob('*/*'))), 4)
        self.assertEqual(self.manifest()['excluded_files'], ['PACKAGE_MANIFEST.json'])

    def test_deterministic_builder(self):
        self.prepare(); second = self.root / 'second'
        self.b.prepare(self.source, self.declaration, second)
        self.assertEqual((self.out / 'PACKAGE_MANIFEST.json').read_bytes(), (second / 'PACKAGE_MANIFEST.json').read_bytes())

    def test_cli_is_read_only_with_exact_expected_manifest_hash(self):
        self.prepare()
        before = sorted(str(f.relative_to(self.out)) for f in self.out.rglob('*'))
        expected = p.digest((self.out / 'PACKAGE_MANIFEST.json').read_bytes())
        for flag in ([], ['-O']):
            result = subprocess.run([sys.executable, *flag, 'tools/verify_handoff.py', '.', '--expected-manifest-sha256', expected],
                cwd=self.out, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)['manifest_sha256'], expected)
        self.assertEqual(sorted(str(f.relative_to(self.out)) for f in self.out.rglob('*')), before)

    def test_expected_manifest_hash_mismatch(self):
        self.prepare()
        with self.assertRaises(ValueError): self.v.verify(self.out, 'f'*64)

    def test_tampered_cas_even_with_rehashed_inventory(self):
        self.prepare(); (self.out / m.object_path(self.h)).write_bytes(b'tampered')
        self.refresh_inventory(); self.reject()

    def test_tampered_curated_copy_even_with_rehashed_inventory(self):
        self.prepare(); (self.out / 'START_HERE.md').write_bytes(b'tampered')
        self.refresh_inventory(); self.reject()

    def test_tampered_view_map_even_with_rehashed_inventory(self):
        self.prepare(); path = self.out / 'VIEW_MAP.json'; value = p.parse(path.read_bytes())
        value['views'][0]['path'] = 'wrong/file.py'; path.write_bytes(p.canonical(value))
        self.refresh_inventory(); self.reject()

    def test_tampered_materialisation_even_with_rehashed_inventory(self):
        self.prepare(); path = self.out / 'MATERIALISATION.json'; value = p.parse(path.read_bytes())
        value['object_count'] = True; path.write_bytes(p.canonical(value))
        self.refresh_inventory(); self.reject()

    def test_extra_file(self):
        self.prepare(); (self.out / 'extra').write_bytes(b'unlisted'); self.reject()

    def test_extra_empty_directory(self):
        self.prepare(); (self.out / 'extra').mkdir(); self.reject()

    def test_declared_extra_file_is_rejected(self):
        self.prepare(); (self.out / 'extra').write_bytes(b'extra')
        manifest = self.manifest(); manifest['files'].append({'path': 'extra', 'sha256': p.digest(b'extra'), 'bytes': 5})
        manifest['files'].sort(key=lambda row: row['path']); self.rewrite_manifest(manifest); self.reject()

    def test_missing_source(self):
        self.prepare(); (self.out / m.object_path(self.h)).unlink(); self.reject()

    def test_symlink_source(self):
        self.prepare(); path = self.out / m.object_path(self.h); path.unlink(); path.symlink_to(self.sources / self.h); self.reject()

    def test_symlink_directory(self):
        self.prepare(); (self.out / 'extra').symlink_to(self.sources, target_is_directory=True); self.reject()

    def test_fifo_payload_rejected_without_reading(self):
        self.prepare(); path = self.out / 'START_HERE.md'; path.unlink(); os.mkfifo(path); self.reject()

    def test_manifest_traversal(self):
        self.prepare(); manifest = self.manifest(); manifest['files'][0]['path'] = '../escape'; self.rewrite_manifest(manifest); self.reject()

    def test_duplicate_json_key(self):
        self.prepare(); path = self.out / 'PACKAGE_MANIFEST.json'; path.write_bytes(b'{"schema":"a","schema":"b"}'); self.reject()

    def test_nonfinite_json(self):
        self.prepare(); path = self.out / 'PACKAGE_MANIFEST.json'; path.write_bytes(b'{"schema":NaN}'); self.reject()

    def test_manifest_noncanonical_bytes(self):
        self.prepare(); path = self.out / 'PACKAGE_MANIFEST.json'; path.write_bytes(path.read_bytes() + b' '); self.reject()

    def test_wrong_received_public_receipt_with_all_hashes_rebound(self):
        self.prepare(); wrong = dict(self.qualification, public_sha256='f'*64); raw = p.canonical(wrong); new = p.digest(raw)
        plan = p.parse((self.out / 'PUBLIC_PLAN.json').read_bytes())
        for obj in plan['objects']:
            if obj['sha256'] == self.qh:
                obj.update(sha256=new, reviewed_digest=new, current_path_digest=new, bytes=len(raw)); obj['provider']['path'] = m.object_path(new)
            if obj['sha256'] == self.rh: obj['received_public_qualification_sha256'] = new
        for view in plan['views']:
            if view['sha256'] == self.qh: view['sha256'] = new
        oldpath = self.out / m.object_path(self.qh); oldpath.unlink()
        if not list(oldpath.parent.iterdir()): oldpath.parent.rmdir()
        newpath = self.out / m.object_path(new); newpath.parent.mkdir(exist_ok=True); newpath.write_bytes(raw)
        included = m.validate_plan(plan); ph = p.digest(p.canonical(plan)); vm = m.make_map(plan, ph, included); receipt = m.make_receipt(ph, vm)
        for name, value in [('PUBLIC_PLAN.json', plan), ('VIEW_MAP.json', vm), ('MATERIALISATION.json', receipt)]:
            (self.out / name).write_bytes(p.canonical(value))
        # Rebind every outer inventory field so only the receipt's semantics fail.
        manifest = self.manifest()
        manifest['files'] = [{'path': f.relative_to(self.out).as_posix(), 'sha256': p.digest(f.read_bytes()), 'bytes': f.stat().st_size}
                             for f in sorted(self.out.rglob('*')) if f.is_file() and f.name != 'PACKAGE_MANIFEST.json']
        manifest['directories'] = sorted(f.relative_to(self.out).as_posix() for f in self.out.rglob('*') if f.is_dir())
        for field, name in [('plan_sha256', 'PUBLIC_PLAN.json'), ('view_map_sha256', 'VIEW_MAP.json'),
                            ('materialisation_sha256', 'MATERIALISATION.json')]:
            manifest[field] = p.digest((self.out / name).read_bytes())
        self.rewrite_manifest(manifest)
        with self.assertRaisesRegex(ValueError, 'received-public identity mismatch'):
            self.v.verify(self.out)

    def test_existing_destination_untouched(self):
        self.out.mkdir(); (self.out / 'keep').write_bytes(b'keep')
        with self.assertRaises(ValueError): self.prepare()
        self.assertEqual((self.out / 'keep').read_bytes(), b'keep')

    def test_source_destination_overlap(self):
        for target in [self.source / 'nested', self.sources / 'nested']:
            with self.subTest(target=target), self.assertRaises(ValueError):
                self.b.prepare(self.source, self.declaration, target, protected_roots=[self.sources])
            self.assertFalse(target.exists())

    def test_destination_ancestor_overlap(self):
        target = self.root / 'new'
        with self.assertRaises(ValueError): self.b.prepare(self.source, self.declaration, target, protected_roots=[target / 'preserved'])
        self.assertFalse(target.exists())

    def test_symlink_destination_parent(self):
        (self.root / 'link').symlink_to(self.root, target_is_directory=True)
        with self.assertRaises(ValueError): self.b.prepare(self.source, self.declaration, self.root / 'link/new')
        self.assertFalse((self.root / 'new').exists())

    def test_undeclared_input_package_path_prevents_writes(self):
        (self.source / 'extra').write_bytes(b'unknown')
        with self.assertRaises(ValueError): self.prepare()
        self.assertFalse(self.out.exists())

    def test_alias_must_match_selected_view(self):
        self.declaration['entries'][0]['source_view'] = 'other/unselected.md'
        with self.assertRaises(ValueError): self.prepare()
        self.assertFalse(self.out.exists())

    def test_wrong_alias_source_identity(self):
        self.declaration['entries'][0]['sha256'] = self.th
        with self.assertRaises(ValueError): self.prepare()
        self.assertFalse(self.out.exists())

    def test_alias_unsafe_paths(self):
        for name in ['../escape', '/absolute', 'reader/CON', 'reader/COM¹', 'reader/a\\b', 'reader/a.']:
            with self.subTest(name=name):
                self.declaration['entries'][0]['path'] = name
                with self.assertRaises(ValueError): self.prepare()
                self.assertFalse(self.out.exists())

    def test_reserved_and_prefix_alias_collisions(self):
        for path in ['PACKAGE_MANIFEST.json', 'PUBLIC_PLAN.json', 'VIEW_MAP.json', 'MATERIALISATION.json',
                     'authored_objects/other', 'AUTHORED_OBJECTS/other', 'tools', 'Tools/other.py']:
            with self.subTest(path=path):
                self.declaration['entries'][0]['path'] = path
                self.declaration['entries'].sort(key=lambda row: row['path'])
                with self.assertRaises(ValueError): self.prepare()
                self.assertFalse(self.out.exists())
                self.declaration['entries'] = copy.deepcopy(self.entries)

    def test_alias_declaration_duplicate_unsorted_or_extra_field(self):
        good = copy.deepcopy(self.declaration)
        for bad in [dict(good, entries=good['entries'] * 2), dict(good, entries=list(reversed(good['entries']))),
                    dict(good, extra='unknown')]:
            self.declaration = bad
            with self.assertRaises(ValueError): self.prepare()
            self.assertFalse(self.out.exists())

    def test_no_nonstandard_module_import_from_package_tools(self):
        self.prepare()
        # An unlisted adjacent stdlib-shadowing module must not execute before inventory rejection.
        (self.out / 'tools/json.py').write_text('raise RuntimeError("UNTRUSTED_IMPORT")\n')
        proc = subprocess.run([sys.executable, 'tools/verify_handoff.py', '.'], cwd=self.out, capture_output=True, text=True)
        self.assertNotEqual(proc.returncode, 0)
        self.assertNotIn('UNTRUSTED_IMPORT', proc.stderr + proc.stdout)
        self.assertFalse((self.out / 'tools/__pycache__').exists())

    def test_builder_only_loads_intended_verifier_tool(self):
        toolroot = self.root / 'preparation-tools'; toolroot.mkdir()
        for name in ('verify_handoff.py', 'prepare_handoff.py'):
            shutil.copyfile(HERE / name, toolroot / name)
        for name in ('__future__.py', 'json.py', 'argparse.py'):
            (toolroot / name).write_text('raise RuntimeError("UNTRUSTED_BUILDER_IMPORT")\n')
        declaration = self.root / 'curated.json'; declaration.write_bytes(p.canonical(self.declaration))
        for index, flags in enumerate(([], ['-O'])):
            destination = self.root / ('cli-handoff-' + str(index))
            proc = subprocess.run([sys.executable, *flags, str(toolroot / 'prepare_handoff.py'),
                '--source-package', str(self.source), '--curated', str(declaration), '--destination', str(destination)],
                capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertEqual(json.loads(proc.stdout)['state'], 'VERIFIED_SOURCE_ONLY_HANDOFF')
        self.assertFalse((toolroot / '__pycache__').exists())

    def test_no_future_import_before_read_only_bootstrap(self):
        self.prepare()
        (self.out / 'tools/__future__.py').write_text('raise RuntimeError("UNTRUSTED_FUTURE_IMPORT")\n')
        for flags in ([], ['-O']):
            proc = subprocess.run([sys.executable, *flags, 'tools/verify_handoff.py', '.'],
                                  cwd=self.out, capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertNotIn('UNTRUSTED_FUTURE_IMPORT', proc.stdout + proc.stderr)
            self.assertEqual(json.loads(proc.stdout)['state'], 'INVALID_HANDOFF')
        self.assertFalse((self.out / 'tools/__pycache__').exists())

    def test_no_retained_import_beneath_interpreter_prefix_or_pythonpath(self):
        self.prepare()
        stdlib = Path(sys._stdlib_dir)
        version = f'python{sys.version_info.major}.{sys.version_info.minor}'
        library = self.root / 'lib'; library.mkdir()
        (library / version).symlink_to(stdlib, target_is_directory=True)
        (self.out / 'tools/json.py').write_text('raise RuntimeError("UNTRUSTED_PREFIX_IMPORT")\n')
        env = dict(os.environ, PYTHONHOME=str(self.root), PYTHONPATH=str(self.out / 'tools'))
        for flags in ([], ['-O']):
            proc = subprocess.run([sys.executable, *flags, 'tools/verify_handoff.py', '.'],
                                  cwd=self.out, env=env, capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertNotIn('UNTRUSTED_PREFIX_IMPORT', proc.stdout + proc.stderr)
            self.assertEqual(json.loads(proc.stdout)['state'], 'INVALID_HANDOFF')
        self.assertFalse((self.out / 'tools/__pycache__').exists())

    def test_static_contract_matches_reviewed_helpers_exactly(self):
        # Comparing ASTs catches accidental changes in copied validation semantics.
        class Unqualify(ast.NodeTransformer):
            def visit_Attribute(self, node):
                if isinstance(node.value, ast.Name) and node.value.id == 'p':
                    return ast.copy_location(ast.Name(id=node.attr, ctx=node.ctx), node)
                return self.generic_visit(node)
        compiled = {n.name: n for n in ast.parse((HERE / 'verify_handoff.py').read_text()).body if isinstance(n, ast.FunctionDef)}
        functions = {'plan_selection.py': ['require', 'digest', 'canonical', 'unique_pairs', 'parse', 'sha', 'identifier',
                     'relative', 'checked_read', 'validate_received_public_receipt'],
                     'materialise_selection.py': ['keys', 'object_path', 'local_path', 'overlap', 'fresh_destination',
                     'validate_plan', 'make_map', 'make_receipt', 'validate_received_public_bodies', 'read_metadata']}
        for filename, names in functions.items():
            original = {n.name: n for n in ast.parse((HERE.parent / filename).read_text()).body if isinstance(n, ast.FunctionDef)}
            for name in names:
                source = original[name]
                if filename == 'materialise_selection.py': source = Unqualify().visit(source)
                with self.subTest(function=name): self.assertEqual(ast.dump(source), ast.dump(compiled[name]))
        plan = self.result['public_plan']; included = m.validate_plan(plan); plan_hash = p.digest(p.canonical(plan))
        self.assertEqual(self.v.make_map(plan, plan_hash, included), m.make_map(plan, plan_hash, included))
        self.assertEqual(self.v.make_receipt(plan_hash, self.v.make_map(plan, plan_hash, included)),
                         m.make_receipt(plan_hash, m.make_map(plan, plan_hash, included)))

    def test_dependency_disposition_contract_stays_exact(self):
        plan = copy.deepcopy(self.result['public_plan'])
        source = next(row for row in plan['objects'] if row['sha256'] == self.h)
        source['role'] = 'licensed_dependency'; source['eligibility_basis'] = 'reviewed_licensed_dependency'
        source['required_dependencies'] = [self.original]
        with self.assertRaises(ValueError): self.v.validate_plan(plan)
        plan['replay_blockers'] = [{'consumer': self.h, 'dependency': self.original, 'reason': 'required_dependency_not_delivered'}]
        self.assertEqual(self.v.validate_plan(plan), m.validate_plan(plan))


if __name__ == '__main__': unittest.main()
