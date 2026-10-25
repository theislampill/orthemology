#!/usr/bin/env python3
"""Resolve preserved source identities and reconstruct a qualified isolated suite.

This tool copies verified sources; it does not execute historical wrappers or
certify scientific acceptance. Same-named historical variants stay separate.
"""
from __future__ import annotations
import argparse
import collections
import hashlib
import json
import pathlib
import re
import stat
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[1]
PREFIX = 'research/t20-v6-20261012'
PUBLIC = {'ADD_EXACT', 'PROJECT', 'REUSE'}
CURRENT_GRAPH_SHA256 = 'ce15fabe3966d210aadbbf51b0d1213c45d6f9397a3dfebbaa66257afc32b5ff'


# Exactly reviewed historical-only prose, not a suffix/directory exemption.
# Ordinary reading uses the existing recognition chapter; original identities
# and the duplicate CP20 proof occurrence remain independently authenticated.
HISTORICAL_PROSE_REVISION = '7efc6217c090b92d65f2c4cb8b011c18eb96bf7c'
HISTORICAL_PROSE = {
    'research/t20-live-20261009/checkpoints/CP19/necessary-truth-operative-basing-20261009/REPORT.md':
        ('15e864dd9b9a31a5203f31fe9b080261afc7de4e',
         '4bd8f0e5bcac178bf9eb890544fcba9fd60f6a1d08cdf2e0cc12bb6d2c4b4c1c', 15381),
    'research/t20-live-20261009/checkpoints/CP19/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md':
        ('18b3ceb2bcca924387899a9d51f3fd035967eac7',
         '3ccb73001c99c976e728817ca9fca75ab128e6538578068f51333e5321f41b5b', 1939),
    'research/t20-live-20261009/checkpoints/CP20/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md':
        ('18b3ceb2bcca924387899a9d51f3fd035967eac7',
         '3ccb73001c99c976e728817ca9fca75ab128e6538578068f51333e5321f41b5b', 1939),
    'research/t20-live-20261009/checkpoints/CP20/compound-ground-necessity-20261009/VARIABLE_SHARING_REDUCTION.md':
        ('512266ec363346b6302292f69dafad32f1e067a9',
         '9420d38627e0dea98af9e8838485fb68ab08feb184ae254953f08585cfe2e71d', 1587),
    'research/t20-live-20261009/checkpoints/CP20/compound-ground-necessity-20261009/REPORT.md':
        ('cf657a78f972b7f98190139b2275a3381d288b66',
         '52631c602c1c8fede28dbe6da34480094caf6f441c1aec0293229cdfdf28a0be', 15839),
}
# The inherited duplicate is a path obligation, not an extra manifest object.
HISTORICAL_PROSE_PUBLIC_PATHS = tuple(
    path for path in HISTORICAL_PROSE
    if path != 'research/t20-live-20261009/checkpoints/CP20/necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md')


def historical_source_bytes(root, path, revision, git_blob):
    """Authenticate one finite original and reject any unsafe or wrong copy.

    Missing physical prose may use the pinned original Git object. A present
    copy must still match. No source is written, no fallback follows a failed
    read, and these checks do not qualify custody or historical execution.
    """
    binding = HISTORICAL_PROSE.get(path)
    if not binding or revision != HISTORICAL_PROSE_REVISION or git_blob != binding[0]:
        raise ValueError('unqualified historical prose binding')
    root = pathlib.Path(root)
    blob, identity, size = binding

    def git(*args):
        result = subprocess.run(
            ['git', '--no-replace-objects', '--literal-pathspecs', *args],
            cwd=root, capture_output=True, check=False)
        if result.returncode:
            raise ValueError('required historical Git objects unavailable')
        return result.stdout

    if git('cat-file', '-t', revision) != b'commit\n':
        raise ValueError('historical revision is not the pinned commit')
    expected_entry = ('100644 blob ' + blob + '\t' + path + '\0').encode()
    if git('ls-tree', '-z', revision, '--', path) != expected_entry:
        raise ValueError('historical path, blob or mode differs')
    body = git('cat-file', 'blob', blob)
    raw = b'blob ' + str(len(body)).encode() + b'\0' + body
    if (len(body), digest(body), hashlib.sha1(raw).hexdigest()) != (size, identity, blob):
        raise ValueError('historical source bytes differ')

    # A combined baseline/worktree diff can show D while the index contains a
    # wrong blob, mode or unresolved merge. Bind the actual staged original too.
    indexed = git('ls-files', '--stage', '-z', '--', path)
    expected_index = ('100644 ' + blob + ' 0\t' + path + '\0').encode()
    if indexed not in (b'', expected_index):
        raise ValueError('historical source index is conflicted or differs from its pinned original')

    target, entry = root, None
    parts = path.split('/')
    for index, part in enumerate(parts):
        target = target / part
        try:
            entry = target.lstat()
        except FileNotFoundError:
            entry = None
            continue
        if stat.S_ISLNK(entry.st_mode):
            raise ValueError('historical source path contains a symlink')
        if index < len(parts) - 1 and not stat.S_ISDIR(entry.st_mode):
            raise ValueError('historical source ancestor is not a directory')
    if entry is not None:
        if not stat.S_ISREG(entry.st_mode) or entry.st_mode & 0o111:
            raise ValueError('historical source is not a regular nonexecutable file')
        if target.read_bytes() != body:
            raise ValueError('present historical source differs from its pinned edition')
    return body


def digest(body):
    return hashlib.sha256(body).hexdigest()


def source_bytes(root, row):
    path = pathlib.PurePosixPath(row['repository_path'])
    if path.is_absolute() or '..' in path.parts or '\\' in str(path):
        raise ValueError('unsafe source path')
    if str(path) in HISTORICAL_PROSE:
        blob, identity, size = HISTORICAL_PROSE[str(path)]
        if (row['repository_path'] != str(path) or str(path) not in HISTORICAL_PROSE_PUBLIC_PATHS
                or row.get('disposition') != 'REUSE'
                or row.get('source_sha256') != identity or row.get('source_bytes') != size):
            raise ValueError('historical public source owner differs')
        body = historical_source_bytes(root, str(path), row.get('repository_revision'), row.get('git_blob'))
    elif row.get('repository_revision'):
        if row['repository_revision'] != HISTORICAL_PROSE_REVISION:
            raise ValueError('invalid pinned historical reuse')
        body = subprocess.check_output(['git', 'show', row['repository_revision'] + ':' + str(path)], cwd=root)
    else:
        target = root / path
        if target.is_symlink() or not target.resolve().is_relative_to(root.resolve()):
            raise ValueError('unsafe source target')
        body = target.read_bytes()
    if digest(body) != row['public_sha256'] or len(body) != row['public_bytes']:
        raise ValueError('source identity differs: ' + row['source_sha256'])
    return body


def lean_imports(text):
    """Read import commands, masking nested Lean comments and strings."""
    out = list(text)
    i, depth, quoted = 0, 0, False
    while i < len(text):
        if depth:
            if text.startswith('/-', i):
                depth += 1
                out[i:i+2] = '  '
                i += 2
            elif text.startswith('-/', i):
                depth -= 1
                out[i:i+2] = '  '
                i += 2
            else:
                if text[i] != '\n':
                    out[i] = ' '
                i += 1
        elif quoted:
            if text[i] == '\\' and i + 1 < len(text):
                out[i:i+2] = '  '
                i += 2
            else:
                quoted = text[i] != '"'
                if text[i] != '\n':
                    out[i] = ' '
                i += 1
        elif text.startswith('/-', i):
            depth = 1
            out[i:i+2] = '  '
            i += 2
        elif text.startswith('--', i):
            end = text.find('\n', i)
            end = len(text) if end < 0 else end
            out[i:end] = ' ' * (end-i)
            i = end
        elif text[i] == '"':
            quoted = True
            out[i] = ' '
            i += 1
        else:
            i += 1
    imports = []
    for line_number, line in enumerate(''.join(out).splitlines(), 1):
        match = re.match(r'^\s*import\s+(.+)$', line)
        if match:
            for module in match[1].split():
                if not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_.]*', module):
                    raise ValueError('unsupported Lean import syntax')
                imports.append((line_number, module))
    return imports


def closure(graph, root_hash):
    edges = collections.defaultdict(list)
    for edge in graph['edges']:
        edges[edge['parent_sha256']].append(edge['target_sha256'])
    seen, active, ordered = set(), set(), []

    def visit(identity):
        if identity in active:
            raise ValueError('cyclic custom import graph')
        if identity in seen:
            return
        active.add(identity)
        for child in edges[identity]:
            visit(child)
        active.remove(identity)
        seen.add(identity)
        ordered.append(identity)

    visit(root_hash)
    return ordered


def validate_graph(root, objects):
    errors = []
    graph_bytes = (root / PREFIX / 'CURRENT_SOURCE_GRAPH.json').read_bytes()
    graph = json.loads(graph_bytes)
    if digest(graph_bytes) != CURRENT_GRAPH_SHA256:
        errors.append('qualified current source graph differs')
    nodes = {n['source_sha256']: n for n in graph['nodes']}
    if len(nodes) != len(graph['nodes']):
        errors.append('duplicate current source node')
    declarations = collections.defaultdict(list)
    for edge in graph['edges']:
        parent, target = edge['parent_sha256'], edge['target_sha256']
        declarations[parent].append((edge['line'], edge['module']))
        if target not in nodes or edge['module'] not in nodes[target]['modules']:
            errors.append('custom import module binding differs: ' + parent)
        if objects.get(target, {}).get('disposition') not in PUBLIC:
            errors.append('required current source unavailable: ' + target)
    for edge in graph['official_import_edges']:
        declarations[edge['parent_sha256']].append((edge['line'], edge['module']))
        if edge['module'].split('.')[0] not in ('Init', 'Lean', 'Std', 'Mathlib'):
            errors.append('unqualified official import')
    for identity in nodes:
        row = objects.get(identity, {})
        if row.get('disposition') not in PUBLIC:
            errors.append('required current source unavailable: ' + identity)
            continue
        try:
            body = source_bytes(root, row)
            if digest(body) != identity:
                errors.append('current formal source must retain exact original bytes: ' + identity)
            actual = lean_imports(body.decode('utf-8'))
            if collections.Counter(actual) != collections.Counter(declarations[identity]):
                errors.append('actual import declarations differ: ' + identity)
        except (OSError, ValueError, KeyError, subprocess.CalledProcessError):
            errors.append('missing or changed current source: ' + identity)
    if set(declarations) - set(nodes):
        errors.append('import parent absent from source graph')
    reached = set()
    for suite in graph['suites']:
        ordered = closure(graph, suite['root_sha256'])
        reached.update(ordered)
        mapping = suite['modules']
        if any(not re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z_][A-Za-z0-9_]*)*', module) for module in mapping):
            errors.append('unsafe suite module name: ' + suite['id'])
        if set(mapping.values()) != set(ordered) or len(mapping) != len(ordered):
            errors.append('isolated suite coverage differs: ' + suite['id'])
        if any(module not in nodes.get(identity, {}).get('modules', []) for module, identity in mapping.items()):
            errors.append('isolated suite module binding differs: ' + suite['id'])
        for edge in graph['edges']:
            if edge['parent_sha256'] in ordered and mapping.get(edge['module']) != edge['target_sha256']:
                errors.append('isolated suite imports a different variant: ' + suite['id'])
    if reached != set(nodes):
        errors.append('current source graph contains missing or unrooted nodes')
    for edge in graph['ordinary_proof_dependencies']:
        for key in ('parent_sha256', 'target_sha256'):
            if objects.get(edge[key], {}).get('disposition') not in PUBLIC:
                errors.append('ordinary proof support unavailable: ' + edge[key])
        try:
            body = source_bytes(root, objects[edge['parent_sha256']]).decode('utf-8')
            if edge['evidence_text'] not in body:
                errors.append('ordinary proof evidence binding differs: ' + edge['parent_sha256'])
        except (OSError, ValueError, KeyError):
            errors.append('ordinary proof parent unavailable: ' + edge['parent_sha256'])
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('find').add_argument('query')
    sub.add_parser('resolve').add_argument('source_sha256')
    export = sub.add_parser('export-suite')
    export.add_argument('suite')
    export.add_argument('destination', type=pathlib.Path)
    args = parser.parse_args()
    document = json.loads((ROOT / PREFIX / 'PUBLIC_PROJECTION_MANIFEST.json').read_bytes())
    objects = {r['source_sha256']: r for r in document['objects']}
    if args.command == 'find':
        query = args.query.casefold()
        for row in objects.values():
            if query in ' '.join([row['source_sha256'], row.get('repository_path', ''), *row.get('source_names', [])]).casefold():
                print(json.dumps(row, ensure_ascii=False))
    elif args.command == 'resolve':
        row = objects[args.source_sha256.removeprefix('source-sha256:')]
        if row['disposition'] in PUBLIC:
            source_bytes(ROOT, row)
        print(json.dumps(row, ensure_ascii=False, indent=2))
    else:
        errors = validate_graph(ROOT, objects)
        if errors:
            raise SystemExit('\n'.join(errors))
        graph = json.loads((ROOT / PREFIX / 'CURRENT_SOURCE_GRAPH.json').read_bytes())
        suite = next(s for s in graph['suites'] if s['id'] == args.suite)
        destination = args.destination.resolve()
        if destination.is_relative_to(ROOT):
            raise SystemExit('Reconstruct outside the repository in a fresh directory')
        # Verify all bytes before creating the fresh destination.
        modules = {identity: module for module, identity in suite['modules'].items()}
        plan = [(modules[h], source_bytes(ROOT, objects[h])) for h in closure(graph, suite['root_sha256'])]
        destination.mkdir(parents=True, exist_ok=False)
        for module, body in plan:
            path = destination / (module.replace('.', '/') + '.lean')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(body)
        (destination / 'REPLAY_ORDER.txt').write_text('\n'.join(m.replace('.', '/') for m, _ in plan) + '\n')
        (destination / 'RECONSTRUCTION.json').write_text(json.dumps(suite, indent=2) + '\n')
        print(json.dumps({'suite': suite['id'], 'verified_sources': len(plan), 'executed': False}))


if __name__ == '__main__':
    main()
