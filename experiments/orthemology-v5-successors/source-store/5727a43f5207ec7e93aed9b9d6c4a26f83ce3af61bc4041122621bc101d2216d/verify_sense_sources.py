#!/usr/bin/env python3
"""Verify nine supplemental source identities without printing source content.

Standard library only. No source parsing, application imports, network,
subprocesses or source writes. This adds no occurrence-data or linguistic tests.
"""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import sys


def verify(source):
    if not source.is_dir():
        raise ValueError('source directory is missing or is not a directory')
    lock_path = Path(__file__).resolve().with_name('sense-source-lock.json')
    try:
        lock = json.loads(lock_path.read_text(encoding='utf-8'))
        files = lock['files']
    except (OSError, ValueError, KeyError, TypeError):
        raise ValueError('sense-source-lock.json is missing or malformed') from None
    if not isinstance(files, list) or len(files) != 9:
        raise ValueError('supplemental lock must contain exactly nine source bindings')
    checks = []
    seen = set()
    for row in files:
        relative = PurePosixPath(row['path'])
        if (relative.is_absolute() or '..' in relative.parts or
                relative.as_posix() != row['path'] or row['path'] in seen):
            raise ValueError('supplemental lock has an invalid relative path')
        seen.add(row['path'])
        try:
            data = source.joinpath(*relative.parts).read_bytes()
        except OSError:
            raise ValueError('missing or unreadable locked file: ' + row['path']) from None
        digest = hashlib.sha256(data).hexdigest()
        blob_id = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
        if len(data) != row['bytes'] or digest != row['sha256'] or blob_id != row['blob_sha1']:
            raise ValueError('source identity mismatch: ' + row['path'])
        checks.append({'path': row['path'], 'pass': True})
    return {
        'status': 'PASS',
        'scope': 'Supplemental source identity only; no occurrence-data or linguistic checks',
        'commit': lock['commit'],
        'tree': lock['tree'],
        'source_files_checked': len(checks),
        'occurrence_data_checks': 0,
        'checks': checks,
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source_dir', type=Path,
                        help='separately obtained pinned source root containing the nine locked files')
    args = parser.parse_args()
    try:
        result = verify(args.source_dir)
    except (KeyError, TypeError):
        print(json.dumps({'status': 'FAIL', 'reason': 'malformed supplemental lock'}, sort_keys=True))
        return 1
    except ValueError as exc:
        print(json.dumps({'status': 'FAIL', 'reason': str(exc)}, sort_keys=True))
        return 1
    sys.stdout.write(json.dumps(result, indent=2, sort_keys=True) + '\n')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
