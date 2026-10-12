#!/usr/bin/env python3
"""Check by default; explicitly apply only this additive proposed research subtree."""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess

HERE = Path(__file__).resolve().parent
_spec = importlib.util.spec_from_file_location('package_validation', HERE / 'validate_package.py')
validation = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validation)


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True, check=False)
    if result.returncode:
        raise ValueError('Git precondition failed: ' + result.stderr.strip())
    return result.stdout.strip()


def check_repository(root, pins):
    root = Path(root).resolve()
    if Path(git(root, 'rev-parse', '--show-toplevel')).resolve() != root:
        raise ValueError('target must be the repository root')
    if git(root, 'rev-parse', 'HEAD') != pins['commit']:
        raise ValueError('baseline commit drift; stop and obtain a reviewed rebase')
    if git(root, 'rev-parse', 'HEAD^{tree}') != pins['tree']:
        raise ValueError('baseline tree drift')
    if git(root, 'status', '--porcelain=v1', '--untracked-files=all'):
        raise ValueError('target checkout is not clean')
    if any(record and record[0] != 'H' for record in git(root, 'ls-files', '-v', '-z').split('\0')):
        raise ValueError('index flags hide worktree state; use a fully checked clean checkout')
    for row in pins['preimages']:
        rel = str(validation.safe_path(row['path']))
        if git(root, 'rev-parse', 'HEAD:' + rel) != row['git_blob_sha1']:
            raise ValueError('preimage drift: ' + rel)
        path = root / rel
        if path.is_symlink() or any(parent.is_symlink() for parent in path.parents if parent != root):
            raise ValueError('symlink in preimage')
        raw = path.read_bytes()
        if len(raw) != row['bytes'] or hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise ValueError('worktree preimage drift: ' + rel)
    destination = root / str(validation.safe_path(pins['destination']))
    for path in [destination, *destination.parents]:
        if path == root:
            break
        if path.is_symlink():
            raise ValueError('symlink in destination path')
    if destination.exists():
        raise ValueError('destination exists; additive tool never overwrites')
    return destination


def copy_additive(source, destination):
    source, destination = Path(source), Path(destination)
    for path in source.rglob('*'):
        if path.is_symlink():
            raise ValueError('symlink in source')
    destination.parent.mkdir(parents=True, exist_ok=True)
    # copytree creates the root exclusively. Existing files are never overwritten.
    shutil.copytree(source, destination, dirs_exist_ok=False, copy_function=shutil.copyfile)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checkout', type=Path)
    parser.add_argument('--apply', action='store_true', help='Requires separate integration authority; copies only the new subtree.')
    args = parser.parse_args()
    validation.verify_files(HERE)
    validation.verify_projection(HERE)
    pins = validation.read_json(HERE / 'INTEGRATION_PINS.json')
    root = args.checkout.resolve()
    if root == HERE or root in HERE.parents:
        raise ValueError('keep the package outside the target checkout')
    destination = check_repository(root, pins)
    if not args.apply:
        print(json.dumps({'status':'PRECONDITIONS_PASS','writes':False,'destination':pins['destination']}))
        return
    copy_additive(HERE, destination)
    validation.verify_files(destination)
    validation.verify_projection(destination)
    print(json.dumps({'status':'ADDITIVE_COPY_VERIFIED','destination':pins['destination'],
                      'next':'Run established repository checks and derived-state workflow under integration authority; nothing staged, committed, pushed, merged, or adopted.'}))


if __name__ == '__main__':
    main()
