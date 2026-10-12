#!/usr/bin/env python3
"""Read-only path, hash and ZIP safety primitives; no scientific execution."""
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import struct
import unicodedata
import zipfile
EPOCH = 315532800

def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical_json(value):
    return (json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n').encode('utf-8')


def safe_relative(name):
    require(isinstance(name, str) and bool(name), 'Empty or non-text path')
    require('\\' not in name and not name.startswith('/'), 'Absolute/backslash path: ' + name)
    parts = name.split('/')
    require(all(p not in ('', '.', '..') for p in parts), 'Unsafe path segment: ' + name)
    for part in parts:
        require(not any(ord(c) < 32 or ord(c) == 127 or c in '<>:"|?*' for c in part), 'Windows-unsafe path: ' + name)
        require(not part.endswith((' ', '.')), 'Windows-trimmed alias: ' + name)
        stem = part.split('.')[0].upper()
        require(stem not in {'CON', 'PRN', 'AUX', 'NUL', 'CLOCK$'} and
                re.fullmatch(r'(?:COM|LPT)[1-9¹²³]', stem) is None, 'Windows device path: ' + name)
    require(not PurePosixPath(name).is_absolute(), 'Absolute path: ' + name)
    return name


def check_names(files, directories=()):
    """Reject file duplicates, file/directory shadows, NFC and casefold aliases."""
    files, directories = list(files), list(directories)
    require(len(files) == len(set(files)), 'Duplicate file name')
    require(len(directories) == len(set(directories)), 'Duplicate directory entry')
    require(not set(files) & set(directories), 'File/directory name collision')
    nodes = {}
    for name in files + directories:
        safe_relative(name)
        parts = name.split('/')
        for length in range(1, len(parts) + 1):
            prefix = '/'.join(parts[:length])
            key = unicodedata.normalize('NFC', prefix).casefold()
            require(key not in nodes or nodes[key] == prefix, 'Windows/Unicode name collision: ' + prefix)
            nodes[key] = prefix
        for length in range(1, len(parts)):
            require('/'.join(parts[:length]) not in files, 'File shadows directory: ' + name)
    return {'files': len(files), 'directories': len(nodes) - len(files),
            'windows_case_and_unicode_collisions': 0,
            'long_relative_paths_over_240': sorted(x for x in files if len(x) > 240)}


def no_symlink_path(path):
    path = Path(os.path.abspath(path))
    for item in [path, *path.parents]:
        require(not item.is_symlink(), 'Symlink path is not supported: ' + str(item))
    return path


def source_path(root, relative):
    safe_relative(relative)
    root = no_symlink_path(root)
    p = no_symlink_path(root / relative)
    require(p.is_relative_to(root), 'Source escaped input root')
    require(p.is_file() and stat.S_ISREG(p.stat().st_mode), 'Not a regular source: ' + relative)
    return p


def checked_bytes(path, row):
    data = Path(path).read_bytes()
    require(len(data) == row['bytes'], 'Length mismatch: ' + str(path))
    require(digest(data) == row['sha256'], 'SHA-256 mismatch: ' + str(path))
    return data


def inspect_zip(data, label, depth=0, budget=None):
    """Check archives without extracting. Includes recursively nested .zip files."""
    require(depth <= 8, 'Nested archive depth exceeds safe bound')
    if budget is None:
        budget = [0]
    try:
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            entries = archive.infolist()
            files = [i.filename for i in entries if not i.is_dir()]
            dirs = [i.filename[:-1] for i in entries if i.is_dir()]
            safety = check_names(files, dirs)
            records, nested = [], []
            for item in entries:
                # All authorised input containers have empty extra fields. Refuse
                # alternate filename/ownership semantics rather than normalise them.
                require(item.orig_filename == item.filename, 'ZIP filename was silently normalised or truncated')
                safe_relative(item.orig_filename.rstrip('/') if item.is_dir() else item.orig_filename)
                require(not item.extra, 'ZIP extra metadata is unsupported: ' + item.filename)
                offset = item.header_offset
                require(offset >= 0 and offset + 30 <= len(data), 'Invalid local ZIP header offset')
                fields = struct.unpack_from('<4s5H3L2H', data, offset)
                require(fields[0] == b'PK\x03\x04', 'Invalid local ZIP header signature')
                require(fields[10] == 0, 'Local ZIP extra metadata is unsupported: ' + item.filename)
                kind = stat.S_IFMT(item.external_attr >> 16)
                require(kind in ((0, stat.S_IFDIR) if item.is_dir() else (0, stat.S_IFREG)), 'ZIP member type disagrees with its name: ' + item.filename)
                require(not ((item.external_attr >> 16) & 0o7000), 'Privileged ZIP permission bits are unsupported')
                require(not (item.flag_bits & 1), 'Encrypted ZIP member unsupported')
                require(item.file_size <= 128 * 1024 * 1024, 'ZIP member exceeds size bound')
                budget[0] += item.file_size
                require(budget[0] <= 512 * 1024 * 1024, 'Nested ZIP expansion exceeds size bound')
                body = archive.read(item)  # Also verifies CRC.
                require(len(body) == item.file_size, 'ZIP member length mismatch')
                if item.is_dir():
                    require(not body, 'Directory member has payload')
                    continue
                records.append({'path': item.filename, 'bytes': len(body), 'sha256': digest(body)})
                if item.filename.lower().endswith('.zip'):
                    nested.append(inspect_zip(body, label + '!/' + item.filename, depth + 1, budget))
            return {'archive': label, 'bytes': len(data), 'sha256': digest(data),
                    'crc': 'PASS', 'path_safety': safety, 'files': records, 'nested': nested,
                    'archive_count': 1 + sum(n['archive_count'] for n in nested),
                    'regular_member_count': len(records) + sum(n['regular_member_count'] for n in nested)}
    except (zipfile.BadZipFile, RuntimeError, OSError, NotImplementedError) as exc:
        raise ValueError('ZIP integrity failure: ' + label + ': ' + str(exc)) from exc


def check_archive_equivalence(data, prefix, expected):
    if prefix:
        safe_relative(prefix.rstrip('/'))
        require(prefix.endswith('/'), 'Package prefix must end with slash')
    inventory = inspect_zip(data, 'source-package')
    require(not inventory['nested'], 'Source-only ZIP must not contain nested ZIPs')
    records = []
    for row in inventory['files']:
        require(row['path'].startswith(prefix), 'Source ZIP member outside declared root')
        records.append({'logical_path': row['path'][len(prefix):], 'sha256': row['sha256'], 'bytes': row['bytes']})
    check_names(r['logical_path'] for r in records)
    identity = lambda r: (r['logical_path'], r['bytes'], r['sha256'])
    require(sorted(map(identity, records)) == sorted(map(identity, expected)), 'Source ZIP finite reconstruction differs')
    return {'matched_members': len(records), 'archive_sha256': digest(data), 'prefix': prefix,
            'status': 'EXACT_MEMBER_LAYOUT_EQUIVALENCE', 'container_copied': False}


def check_package(root, rows):
    check_names(r['path'] for r in rows)
    for row in rows:
        checked_bytes(source_path(root, row['path']), row)
    return len(rows)


def read_nested_identity(data, members):
    for name in members:
        safe_relative(name)
        with zipfile.ZipFile(io.BytesIO(data)) as archive:
            require(archive.namelist().count(name) == 1, 'Nested member not uniquely resolved: ' + name)
            data = archive.read(name)
    return data


