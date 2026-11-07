#!/usr/bin/env python3
"""Proposed read-only phases for a root-owned, already absent 258-copy trial.

This procedure never removes a source, modifies an index, creates a commit or
qualifies the enclosing restoration boundary. The hosted parent freezes its exact public
inputs and provides the already prepared single-checkout trial. No full protected CLI or
Lean kernel is run. The graph phase writes one public reconstruction outside it.
"""
import argparse
import contextlib
from datetime import datetime, timezone
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--repo', type=Path, required=True)
parser.add_argument('--expected-head', required=True)
parser.add_argument('--state', type=Path, required=True)
parser.add_argument('--phase', choices=['source_objects', 'legacy_suites', 'preservation',
                                     't20_graph', 'reader', 'reference'], required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
repo = args.repo.absolute()
output = args.output.absolute()
assert sys.version_info[:3] == (3, 11, 9) and __debug__
assert repo.is_dir() and not repo.is_symlink()
assert not output.exists() and not output.resolve().is_relative_to(repo.resolve())
assert subprocess.check_output(['git', '--no-replace-objects', 'rev-parse', 'HEAD'],
                               cwd=repo, text=True).strip() == args.expected_head

state = args.state.absolute()
prepared = json.loads((state / 'PREPARED.json').read_bytes())
assert prepared['repo'] == str(repo) and prepared['state'] == str(state)
assert prepared['head'] == args.expected_head
def frozen_input(relative):
    body = (state / relative).read_bytes()
    expected_input = prepared['input_files'][relative]
    assert len(body) == expected_input['bytes']
    assert hashlib.sha256(body).hexdigest() == expected_input['sha256']
    return body
guard_path = state / 'inputs/guard.py'
frozen_input('inputs/guard.py')
holds = json.loads(frozen_input('inputs/hold.json'))['held']
held_paths = {row['path'] for row in holds}
held_blobs = {row['published_metadata']['git_blob'] for row in holds}
for raw in subprocess.check_output(['git', '--no-replace-objects', 'ls-tree', '-rz', 'HEAD'], cwd=repo).split(b'\0'):
    if raw:
        metadata, path = raw.split(b'\t', 1)
        if metadata.decode().split()[2] in held_blobs:
            held_paths.add(path.decode())
spec = importlib.util.spec_from_file_location('absence_guard', guard_path)
guard_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard_module)
guard = guard_module.HeldBodyGuard()
guard.add_root(repo, sorted(held_paths))
guard.install()

sys.path.insert(0, str(repo / 'scripts'))
import resolve_t20_v6_source as source
import validate_research_continuations as legacy
import validate_t20_v6_projection as projection

classes = json.loads(frozen_input('classes.json'))
expected = {row['alias']: dict(original=row['alias'], retained=row['canonical'],
            sha256=row['sha256'], bytes=row['bytes'], git_blob=row['blob'], mode=row['mode'])
            for row in classes if row['cohort'] == '258'}
assert len(expected) == 258
assert not set(expected) & held_paths
assert not {row['retained'] for row in expected.values()} & held_paths
catalog = source._continuation_copy_catalog(repo)
assert set(catalog) == set(expected)
for path, row in expected.items():
    current = catalog[path]
    assert (current['canonical'], current['sha256'], current['bytes'], current['blob']) == (
        row['retained'], row['sha256'], row['bytes'], row['git_blob'])
    assert not os.path.lexists(repo / path), 'Root must prepare the exact absence first'
excluded = source.CONTINUATION_COPY_ROOT + source.CONTINUATION_COPY_EXCLUDED + '.lean'
assert (repo / excluded).is_file() and not (repo / excluded).is_symlink()
manifest = json.loads((repo / source.PREFIX / 'PUBLIC_PROJECTION_MANIFEST.json').read_bytes())
objects = {row['source_sha256']: row for row in manifest['objects']}
record = {'status': 'RUNNING', 'phase': args.phase, 'head': args.expected_head,
          'started_utc': datetime.now(timezone.utc).isoformat(), 'class_paths': 258,
          'source_absence_performed_by_this_procedure': False, 'kernel_execution': False}

try:
    if args.phase == 'source_objects':
        for path, row in expected.items():
            public = objects[row['sha256']]
            assert public['repository_path'] == path and public['disposition'] == 'REUSE'
            assert projection.check_object(repo, public) == []
        record['actual_public_object_checks'] = 258
    elif args.phase == 'legacy_suites':
        registry = legacy.read_json(repo / legacy.AREA / 'registry.json')
        rows = legacy.indexed(legacy.read_json(repo / registry['source_map'])['sources'], 'id')
        selected = {key: row for key, row in rows.items() if row['path'] in expected}
        assert len(selected) == 2772
        seen = set()
        for row in selected.values():
            if row['path'] not in seen:
                body = legacy.source_bytes(repo, row)
                assert hashlib.sha256(body).hexdigest() == row['sha256']
                seen.add(row['path'])
        parsed, suites = {}, []
        for name in registry['suites']:
            suite = legacy.read_json(repo / name)
            if any(module['source_id'] in selected for module in suite['modules']):
                legacy.validate_suite(suite, rows, repo, parsed)
                suites.append(suite['id'])
        assert len(suites) == 96 and len(seen) == 258
        record.update(source_ids=2772, source_paths=258, affected_suites=suites)
    elif args.phase == 'preservation':
        import validate_v5_successors as successor
        registry = successor.read_json(repo / successor.AREA / 'registry.json')
        bundle = {'registry': registry}
        for key, name in [('baseline_binding', 'BASELINE_BINDING'), ('preservation', 'PRESERVATION')]:
            bundle[key] = successor.read_json(successor.file_ref(registry['records'][name], repo))
        files = successor._preservation(bundle, repo, successor.BASELINE_ANCHOR)
        assert len(files) == 1200 and set(expected) <= set(files)
        record['original_inventory_rows_preserved'] = 1200
    elif args.phase == 't20_graph':
        graph_bytes = (repo / source.PREFIX / 'CURRENT_SOURCE_GRAPH.json').read_bytes()
        assert hashlib.sha256(graph_bytes).hexdigest() == source.CURRENT_GRAPH_SHA256
        graph = json.loads(graph_bytes)
        reads = {objects[row['source_sha256']]['repository_path'] for row in graph['nodes']}
        reads |= {objects[row['parent_sha256']]['repository_path'] for row in graph['ordinary_proof_dependencies']}
        assert not reads & held_paths
        assert source.validate_graph(repo, objects) == []
        assert projection.check_preserved_roots(repo, objects) == []
        affected = {row['sha256'] for row in expected.values()} & {row['source_sha256'] for row in graph['nodes']}
        assert len(affected) == 26
        suite = next(row for row in graph['suites'] if row['id'] == 'FamilyComputability')
        assert affected <= set(suite['modules'].values())
        destination = output.with_suffix('.export')
        prior_argv = sys.argv
        sys.argv = ['resolve_t20_v6_source.py', 'export-suite', suite['id'], str(destination)]
        try:
            with contextlib.redirect_stdout(io.StringIO()) as stream:
                source.main()
        finally:
            sys.argv = prior_argv
        exported = {}
        for module, identity in suite['modules'].items():
            body = (destination / (module.replace('.', '/') + '.lean')).read_bytes()
            assert hashlib.sha256(body).hexdigest() == identity
            exported[module] = identity
        record.update(graph_nodes=233, graph_suites=7, retained_proof_roles=26,
                      actual_export=suite['id'], exported_modules=exported,
                      export_terminal=json.loads(stream.getvalue()))
    elif args.phase == 'reader':
        import check_reader_pilot as reader
        owners = json.loads((repo / 'docs/project-closure/reader-refactor-issue-35/OWNER-MAP.json').read_bytes())
        cross = json.loads((repo / 'docs/project-closure/reader-refactor-issue-35/CROSSWALK.json').read_bytes())
        errors = reader.check(repo, owners, cross)
        errors += reader.check_reader_pages(repo, cross)
        errors += reader.check_root_navigation(repo, owners, cross)
        assert errors == [], errors
        record['reader_errors'] = []
    else:
        import validate_internal_references as references
        for path in expected:
            assert references._resolves('preserved-original-identity', path)
        assert references._resolves('preserved-original-identity', excluded)
        record['bounded_original_reference_routes'] = 258
    assert guard.denials == 0
    record['status'] = 'PASS_BOUNDED_PHASE_ONLY'
except BaseException as exc:
    record.update(status='FAIL_OR_INTERRUPTED', error=repr(exc))
    raise
finally:
    record.update(finished_utc=datetime.now(timezone.utc).isoformat(), held_denials=guard.denials)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(record, indent=2) + '\n')
