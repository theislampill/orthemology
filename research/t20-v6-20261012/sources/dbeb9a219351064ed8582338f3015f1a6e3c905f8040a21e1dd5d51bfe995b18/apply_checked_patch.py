#!/usr/bin/env python3
"""Check or apply the supplied exact-base integration patch with stdlib + Git."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def require(condition, message):
    if not condition:
        raise ValueError(message)


def checksum(data):
    return hashlib.sha256(data).hexdigest()


def git(root, *args):
    result = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True)
    require(result.returncode == 0, result.stderr.strip() or 'Git command failed: ' + ' '.join(args))
    return result.stdout.strip()


def safe(root, relative):
    require(isinstance(relative, str), 'Unsafe manifest path')
    parts = relative.split('/')
    require(not any(part.rstrip(' .').casefold() == '.git' for part in parts), 'Repository metadata paths are forbidden')
    require(relative and not relative.startswith('/') and '\\' not in relative
            and ':' not in relative and all(p not in ('', '.', '..') for p in parts), 'Unsafe manifest path')
    path = root
    for part in parts:
        path = path / part
        require(not path.is_symlink(), 'Symlink at manifest path: ' + relative)
    return path


def verify_images(root, rows, phase):
    for row in rows:
        path = safe(root, row['path'])
        image = row[phase]
        if image is None:
            require(not path.exists(), 'Unexpected existing file: ' + row['path'])
        else:
            require(path.is_file(), 'Missing expected file: ' + row['path'])
            data = path.read_bytes()
            require(len(data) == image['bytes'] and checksum(data) == image['sha256'], 'Changed ' + phase + ': ' + row['path'])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, required=True)
    parser.add_argument('--apply', action='store_true', help='Apply after all checks. Without this flag, check only.')
    args = parser.parse_args()
    root = args.repository.resolve()
    package = Path(__file__).resolve().parent
    manifest = json.loads((package / 'PATCH_MANIFEST.json').read_text())
    require(manifest['schema'] == 'through-twentieth-exact-base-patch-v1', 'Unknown patch manifest')
    patch = safe(package, manifest['patch']['filename'])
    raw = patch.read_bytes()
    require(checksum(raw) == manifest['patch']['sha256'] and len(raw) == manifest['patch']['bytes'], 'Patch bytes differ from manifest')
    require(git(root, 'rev-parse', 'HEAD') == manifest['base_commit'], 'Wrong HEAD; reconcile upstream drift instead of forcing the patch')
    require(git(root, 'rev-parse', 'HEAD^{tree}') == manifest['base_tree'], 'Wrong base tree')
    require(not git(root, 'status', '--porcelain', '--untracked-files=all'), 'Worktree/index is not clean; use a fresh exact-base clone')
    branch = None
    if args.apply:
        branch = git(root, 'branch', '--show-current')
        require(bool(branch) and branch.casefold() not in {'main', 'master'},
                'Applying requires an isolated named feature branch; main/master and detached HEAD are forbidden')
    verify_images(root, manifest['changed_files'], 'before')
    git(root, 'apply', '--check', '--index', str(patch))
    if not args.apply:
        print('PASS: exact base, clean tree, patch identity, preimages and Git apply check. No changes made.')
        return
    require(git(root, 'branch', '--show-current') == branch,
            'Feature branch changed during verification; refusing to apply')
    require(git(root, 'rev-parse', 'HEAD') == manifest['base_commit'], 'HEAD changed during verification')
    require(not git(root, 'status', '--porcelain', '--untracked-files=all'), 'Tree changed during verification')
    git(root, 'apply', '--index', str(patch))
    verify_images(root, manifest['changed_files'], 'after')
    require(not git(root, 'diff', '--name-only'), 'Unexpected unstaged changes after apply')
    require(git(root, 'write-tree') == manifest['candidate_tree'], 'Applied index tree differs from reviewed candidate')
    print('PASS: patch applied to index/worktree and exact postimages/tree verified. No commit, push, PR or merge performed.')
    print('Use the supplied verification guide for local checks and the unchanged mandatory PDF/CI gate.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, json.JSONDecodeError) as error:
        print('REFUSED: ' + str(error), file=sys.stderr)
        sys.exit(1)
