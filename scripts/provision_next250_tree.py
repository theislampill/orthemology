#!/usr/bin/env python3
"""Restore one authenticated, metadata-only provisional Git tree for CI.

No source blobs, refs, index, or worktree files are created or changed.
The resolver's original tree/qualification checks remain mandatory.
"""
import ast
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess


def safe_path(path):
    if (not isinstance(path, str) or not path or '\\' in path
            or any(ord(c) < 32 or ord(c) == 127 for c in path)
            or str(PurePosixPath(path)) != path
            or PurePosixPath(path).is_absolute() or '..' in PurePosixPath(path).parts):
        raise ValueError('unsafe metadata path')
    return path


def read_metadata(root, path):
    path = safe_path(path)
    target = root
    for part in path.split('/'):
        target = target / part
        if target.is_symlink():
            raise ValueError('metadata symlink forbidden')
    if not target.is_file():
        raise ValueError('metadata file missing')
    return target.read_bytes()


def binding_from_source(body):
    matches = [n.value for n in ast.parse(body).body if isinstance(n, ast.Assign)
               and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
               and n.targets[0].id == 'NEXT250_BINDING']
    if len(matches) != 1:
        raise ValueError('unique literal NEXT250 binding required')
    return ast.literal_eval(matches[0])


def git(root, *args, data=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith('GIT_')}
    env.update(GIT_NO_REPLACE_OBJECTS='1', GIT_NO_LAZY_FETCH='1', GIT_OPTIONAL_LOCKS='0',
               GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL=os.devnull,
               GIT_CONFIG_SYSTEM=os.devnull, GIT_ALLOW_PROTOCOL='', GIT_TERMINAL_PROMPT='0')
    return subprocess.check_output(['/usr/bin/git', '--no-replace-objects', '--literal-pathspecs',
                                    '-c', 'core.fsmonitor=false', *args], cwd=root, env=env, input=data)


def entry(text, path):
    if text == '':
        return None
    match = re.fullmatch(r'(100644|100755|120000) blob ([0-9a-f]{40})\t([^\0]+)\0', text)
    if match is None or match[3] != path:
        raise ValueError('qualified entry malformed')
    return match[1], 'blob', match[2]


def reconstruct(flat, changes):
    entries = {}
    for line in flat.split(b'\0'):
        if line:
            meta, path = line.decode().split('\t')
            safe_path(path)
            if path in entries:
                raise ValueError('duplicate base path')
            entries[path] = tuple(meta.split())
    paths = [safe_path(row['path']) for row in changes]
    if paths != sorted(set(paths)):
        raise ValueError('qualified change domain malformed')
    for row in changes:
        if set(row) != {'path', 'before_entry', 'after_entry'}:
            raise ValueError('qualified change shape differs')
        path = row['path']
        if entry(row['before_entry'], path) != entries.get(path):
            raise ValueError('qualified before entry differs')
        after = entry(row['after_entry'], path)
        if after is None:
            entries.pop(path, None)
        else:
            entries[path] = after
    root = {}
    for path, val in entries.items():
        node = root
        for part in path.split('/')[:-1]:
            node = node.setdefault(part, {})
            if not isinstance(node, dict):
                raise ValueError('file/directory collision')
        if path.split('/')[-1] in node:
            raise ValueError('file/directory collision')
        node[path.split('/')[-1]] = val
    objects = {}
    def tree(node):
        body = b''
        for name, val in sorted(node.items(), key=lambda x: (x[0] + ('/' if isinstance(x[1], dict) else '')).encode()):
            if isinstance(val, dict):
                mode, oid = '40000', tree(val)
            else:
                mode, kind, oid = val
                if kind not in ('blob', 'commit') or not re.fullmatch('[0-9a-f]{40}', oid):
                    raise ValueError('base entry malformed')
            body += mode.encode() + b' ' + name.encode() + b'\0' + bytes.fromhex(oid)
        oid = hashlib.sha1(b'tree ' + str(len(body)).encode() + b'\0' + body).hexdigest()
        objects[oid] = body
        return oid
    return tree(root), objects


def provision(root):
    root = Path(root).resolve()
    binding = binding_from_source(read_metadata(root, 'scripts/resolve_t20_v6_source.py'))
    base, provisional = binding['published_base'], binding['provisional_input']
    spec = provisional['qualification']
    if (spec['path'] != 'docs/provenance/r0002-next250-receiver/PROVISIONAL-QUALIFICATION.json'
            or spec['role'] != 'provisional_qualification' or spec['origin'] != 'reviewed_receipt'):
        raise ValueError('qualification metadata owner differs')
    body = read_metadata(root, spec['path'])
    identity = [hashlib.sha1(b'blob ' + str(len(body)).encode() + b'\0' + body).hexdigest(),
                hashlib.sha256(body).hexdigest(), len(body)]
    if identity != spec['identity']:
        raise ValueError('qualification metadata identity differs')
    qualification = json.loads(body)
    if (qualification != provisional['expected_document']
            or qualification['verdict'] != 'QUALIFIED_PROVISIONAL_INPUT'
            or qualification['published_base'] != base or qualification['tree'] != provisional['tree']):
        raise ValueError('qualification document differs')
    if git(root, 'rev-parse', '--verify', base['commit'] + '^{tree}').decode().strip() != base['tree']:
        raise ValueError('published base tree differs')
    git(root, 'merge-base', '--is-ancestor', base['commit'], 'HEAD')
    flat = git(root, 'ls-tree', '-r', '-z', base['tree'])
    expected, objects = reconstruct(flat, qualification['permitted_changes'])
    if expected != provisional['tree']:
        raise ValueError('reconstructed provisional tree differs')
    existing = {base['tree']}
    for line in git(root, 'ls-tree', '-r', '-t', '-z', base['tree']).split(b'\0'):
        if line:
            mode, kind, oid = line.split(b'\t', 1)[0].decode().split()
            if kind == 'tree':
                existing.add(oid)
    written = 0
    for oid, tree_body in objects.items():
        if oid not in existing:
            actual = git(root, 'hash-object', '-w', '-t', 'tree', '--stdin', data=tree_body).decode().strip()
            if actual != oid:
                raise ValueError('written tree identity differs')
            written += 1
    if git(root, 'rev-parse', '--verify', expected + '^{tree}').decode().strip() != expected:
        raise ValueError('provisional tree readback differs')
    return {'provisional_tree': expected, 'tree_object_write_attempts': written, 'source_bodies_read': 0}


if __name__ == '__main__':
    print(json.dumps(provision(Path(__file__).resolve().parents[1]), sort_keys=True))
