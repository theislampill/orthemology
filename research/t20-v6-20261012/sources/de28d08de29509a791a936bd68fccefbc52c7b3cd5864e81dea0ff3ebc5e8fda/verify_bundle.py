#!/usr/bin/env python3
"""Offline integrity and safe extraction only; never executes packaged source.

Trust the separately supplied outer archive SHA-256 before trusting this script or
its manifest. Hash agreement is identity evidence, not mathematical verification.
"""
import argparse
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile
import unicodedata

MAX_MEMBER = 32 * 1024 * 1024
MAX_TOTAL = 128 * 1024 * 1024
MAX_FILES = 5000


def fail(message):
    raise ValueError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe_name(name):
    if not isinstance(name, str) or not name or name.startswith('/') or '\\' in name or ':' in name or any(ord(c) < 32 or ord(c) == 127 for c in name):
        fail('unsafe archive path')
    parts = name.split('/')
    if any(p in ('', '.', '..') for p in parts) or str(PurePosixPath(name)) != name:
        fail('unsafe archive path')
    devices = {'CON','PRN','AUX','NUL'} | {'COM'+str(n) for n in range(1,10)} | {'LPT'+str(n) for n in range(1,10)}
    if any(p.endswith(('.', ' ')) or p.split('.')[0].upper() in devices or any(c in p for c in '<>"|?*') for p in parts):
        fail('unsafe archive path for portable extraction')
    return parts


def load_json(data):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                fail('duplicate JSON key')
            result[key] = value
        return result
    return json.loads(data, object_pairs_hook=unique)


def read_zip(data):
    result, folded, normalized, total = {}, set(), set(), 0
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        entries = archive.infolist()
        if len(entries) > MAX_FILES:
            fail('archive entry limit exceeded')
        for item in entries:
            safe_name(item.filename)
            if item.filename in result:
                fail('duplicate archive member')
            if item.filename.casefold() in folded:
                fail('archive case collision')
            canon = unicodedata.normalize('NFC', item.filename).casefold()
            if canon in normalized:
                fail('archive Unicode normalization collision')
            normalized.add(canon)
            folded.add(item.filename.casefold())
            mode = item.external_attr >> 16
            if item.is_dir() or stat.S_IFMT(mode) not in (0, stat.S_IFREG):
                fail('non-regular archive member')
            if item.flag_bits & 1 or item.compress_type not in (zipfile.ZIP_STORED, zipfile.ZIP_DEFLATED):
                fail('unsupported or encrypted archive member')
            if item.file_size > MAX_MEMBER:
                fail('archive member size limit exceeded')
            total += item.file_size
            if total > MAX_TOTAL:
                fail('archive expanded size limit exceeded')
            payload = archive.read(item)
            if len(payload) != item.file_size:
                fail('archive member size mismatch')
            result[item.filename] = payload
    # Forbid file/directory prefix collisions before any output is created.
    for name in result:
        parts = name.split('/')
        if any('/'.join(parts[:i]).casefold() in folded for i in range(1, len(parts))):
            fail('archive file/directory collision')
    return result


def no_symlink_ancestors(path):
    path = Path(os.path.abspath(path))
    for node in (path, *path.parents):
        if node.is_symlink():
            fail('symlink path is not allowed')
    return path


def read_directory(path):
    root = no_symlink_ancestors(path)
    if not root.is_dir():
        fail('bundle directory is missing')
    result = {}
    total = 0
    for base, dirs, files in os.walk(root, followlinks=False):
        for name in dirs + files:
            p = Path(base) / name
            if p.is_symlink():
                fail('bundle symlink is not allowed')
        for name in files:
            p = Path(base) / name
            if not p.is_file():
                fail('non-regular bundle file')
            size = p.stat().st_size
            total += size
            if size > MAX_MEMBER or total > MAX_TOTAL or len(result) >= MAX_FILES:
                fail('bundle size or entry limit exceeded')
            relative = p.relative_to(root).as_posix()
            safe_name(relative)
            result[relative] = p.read_bytes()
    return result


def verify_payload(files):
    if 'BUNDLE_MANIFEST.json' not in files:
        fail('bundle manifest is missing')
    manifest = load_json(files['BUNDLE_MANIFEST.json'])
    if manifest.get('format') != 1 or not isinstance(manifest.get('files'), list) or not isinstance(manifest.get('archives'), list):
        fail('unsupported manifest format')
    expected = {}
    folded = set()
    for row in manifest['files']:
        name = row['path']; safe_name(name)
        if name == 'BUNDLE_MANIFEST.json' or name in expected or unicodedata.normalize('NFC', name).casefold() in folded:
            fail('duplicate manifest path or self-hash')
        if not isinstance(row.get('bytes'), int) or row['bytes'] < 0 or not re.fullmatch('[0-9a-f]{64}', row.get('sha256', '')):
            fail('malformed file identity')
        expected[name] = row; folded.add(unicodedata.normalize('NFC', name).casefold())
    if set(files) != set(expected) | {'BUNDLE_MANIFEST.json'}:
        fail('bundle file census mismatch')
    for name, row in expected.items():
        if len(files[name]) != row['bytes'] or sha(files[name]) != row['sha256']:
            fail('bundle file digest or size mismatch: ' + name)
    nested, ids, seen_archives = {}, set(), set()
    for row in manifest['archives']:
        name = row['path']; safe_name(name)
        ident = row['extraction_id']; safe_name(ident)
        if '/' in ident or ident.casefold() in ids or name in seen_archives or name not in files:
            fail('duplicate or invalid archive inventory')
        ids.add(ident.casefold()); seen_archives.add(name)
        contents = read_zip(files[name])
        if len(contents) != row['members'] or sum(map(len, contents.values())) != row['uncompressed_bytes']:
            fail('nested archive inventory mismatch')
        nested[ident] = contents
    if {n for n in files if n.lower().endswith('.zip')} != seen_archives:
        fail('unlisted nested archive')
    return manifest, nested


def check_new_target(path):
    path = no_symlink_ancestors(path)
    if path.exists():
        fail('extraction target already exists')
    if not path.parent.is_dir():
        fail('extraction parent must already exist')
    return path


def extract_files(files, target):
    # Validation must be complete before this routine. Fresh directory and
    # exclusive creation prevent overwriting any pre-existing payload.
    target.mkdir(mode=0o700)
    for name, payload in sorted(files.items()):
        destination = target.joinpath(*safe_name(name))
        destination.parent.mkdir(parents=True, exist_ok=True)
        no_symlink_ancestors(destination.parent)
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, 'O_NOFOLLOW', 0)
        fd = os.open(destination, flags, 0o600)
        with os.fdopen(fd, 'wb') as stream:
            stream.write(payload)


def main():
    if not __debug__ or os.environ.get('PYTHONOPTIMIZE'):
        fail('optimized Python is not allowed')
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group()
    source.add_argument('--archive', type=Path)
    source.add_argument('--directory', type=Path)
    parser.add_argument('--expected-sha256')
    parser.add_argument('--extract-to', type=Path, help='new outer-archive extraction directory')
    parser.add_argument('--extract-packages-to', type=Path, help='new directory for verified nested source/evidence archives')
    args = parser.parse_args()
    outer_sha, outer_files = None, None
    if args.archive:
        if not args.expected_sha256 or not re.fullmatch('[0-9a-f]{64}', args.expected_sha256):
            fail('--archive requires --expected-sha256 from an independent trusted delivery receipt')
        archive_path = no_symlink_ancestors(args.archive)
        if archive_path.stat().st_size > MAX_TOTAL:
            fail('archive size limit exceeded')
        raw = archive_path.read_bytes(); outer_sha = sha(raw)
        if outer_sha != args.expected_sha256:
            fail('outer archive SHA-256 mismatch')
        outer_files = read_zip(raw)
        roots = {safe_name(n)[0] for n in outer_files}
        if len(roots) != 1 or any('/' not in n for n in outer_files):
            fail('outer archive must have one root directory')
        root = next(iter(roots)) + '/'
        files = {n[len(root):]: d for n, d in outer_files.items()}
    else:
        if args.expected_sha256 or args.extract_to:
            fail('--expected-sha256 and --extract-to require --archive')
        files = read_directory(args.directory or Path(__file__).resolve().parent)
    manifest, nested = verify_payload(files)
    target = check_new_target(args.extract_to) if args.extract_to else None
    packages = check_new_target(args.extract_packages_to) if args.extract_packages_to else None
    if target and packages and (target == packages or target in packages.parents or packages in target.parents):
        fail('extraction targets must be disjoint')
    if target:
        extract_files(outer_files, target)
    if packages:
        flattened = {ident+'/'+n: d for ident, rows in nested.items() for n,d in rows.items()}
        extract_files(flattened, packages)
    print(json.dumps({'status':'PASS_INTEGRITY_AND_SAFE_EXTRACTION_ONLY','outer_sha256':outer_sha,'manifest_sha256':sha(files['BUNDLE_MANIFEST.json']),'files_verified':len(files)-1,'nested_archives_verified':len(nested),'nested_files_verified':sum(map(len,nested.values())),'outer_extracted':bool(target),'nested_packages_extracted':bool(packages),'proof_replay_performed':False,'empirical_replay_performed':False,'network_access_performed':False},indent=2))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError, zipfile.BadZipFile, RuntimeError) as exc:
        print('VERIFICATION FAILED: ' + str(exc), file=sys.stderr)
        sys.exit(1)
