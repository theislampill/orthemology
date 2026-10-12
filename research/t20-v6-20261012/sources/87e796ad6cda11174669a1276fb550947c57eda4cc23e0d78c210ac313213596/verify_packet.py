#!/usr/bin/env python3
"""Read-only verification of an Orthemology handoff directory or ZIP.

Python 3.10+; standard library only. No extraction, research-code execution,
network access, package installation or source modification. Safety checks do
not use assert and remain effective under python -O. A separately trusted ZIP
hash is still required for authenticity beyond this self-contained manifest.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import zipfile

MAX_FILES = 100_000
MAX_BYTES = 1_000_000_000
SPECIAL = {'MANIFEST.json', 'MANIFEST.sha256'}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def safe_path(text: str) -> str:
    require(isinstance(text, str) and bool(text), 'Empty/non-string path')
    p = PurePosixPath(text)
    require(str(p) == text and not p.is_absolute() and '..' not in p.parts
            and '\\' not in text and ':' not in text and '\x00' not in text,
            'Unsafe or noncanonical path: '+repr(text))
    return text


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def strict_json(data: bytes) -> dict:
    def pairs(items: list[tuple[str, object]]) -> dict:
        result = {}
        for k, value in items:
            require(k not in result, 'Duplicate JSON key: '+k)
            result[k] = value
        return result
    def nonfinite(value: str) -> None:
        raise ValueError('Non-finite JSON number: '+value)
    result = json.loads(data.decode('utf-8'), object_pairs_hook=pairs,
                        parse_constant=nonfinite)
    require(isinstance(result, dict), 'Expected a JSON object')
    return result


def load(path: Path) -> tuple[dict[str, bytes], dict[str, int]]:
    require(not path.is_symlink(), 'Input must not be a symlink')
    data: dict[str, bytes] = {}
    modes: dict[str, int] = {}
    if path.is_dir():
        total = 0
        for p in sorted(path.rglob('*')):
            require(not p.is_symlink(), 'Symlink forbidden: '+str(p))
            if p.is_dir():
                continue
            require(p.is_file(), 'Nonregular entry: '+str(p))
            name = safe_path(p.relative_to(path).as_posix())
            total += p.stat().st_size
            require(len(data) < MAX_FILES and total <= MAX_BYTES, 'Package size limit')
            data[name] = p.read_bytes()
            modes[name] = p.stat().st_mode
    else:
        require(path.is_file(), 'Input does not exist')
        with zipfile.ZipFile(path) as archive:
            infos = archive.infolist()
            names = [i.filename for i in infos]
            require(len(names) <= MAX_FILES and len(set(names)) == len(names),
                    'Too many or duplicate ZIP members')
            require(sum(i.file_size for i in infos) <= MAX_BYTES, 'ZIP expansion limit')
            for i in infos:
                name = i.filename[:-1] if i.is_dir() else i.filename
                safe_path(name)
                mode = i.external_attr >> 16
                require(not i.flag_bits & 1, 'Encrypted member forbidden')
                require(not stat.S_ISLNK(mode), 'ZIP symlink forbidden')
                require(stat.S_IFMT(mode) in (0, stat.S_IFREG, stat.S_IFDIR),
                        'ZIP special file forbidden')
                if i.is_dir():
                    continue
                data[name] = archive.read(i)  # zipfile verifies each member CRC
                modes[name] = mode
        if 'MANIFEST.json' not in data:
            roots = {PurePosixPath(n).parts[0] for n in data}
            require(len(roots) == 1 and all(len(PurePosixPath(n).parts) > 1 for n in data),
                    'Expected a single packet root')
            prefix = next(iter(roots))+'/'
            data = {n[len(prefix):]: b for n, b in data.items()}
            modes = {n[len(prefix):]: m for n, m in modes.items()}
    return data, modes


def git_oid(kind: str, content: bytes) -> str:
    header = kind.encode('ascii')+b' '+str(len(content)).encode('ascii')+b'\0'
    return hashlib.sha1(header+content).hexdigest()


def git_tree(flat: dict[str, bytes]) -> str:
    nested: dict = {}
    for path, content in flat.items():
        parts = PurePosixPath(safe_path(path)).parts
        current = nested
        for component in parts[:-1]:
            require(not isinstance(current.get(component), bytes), 'Tree path collision')
            current = current.setdefault(component, {})
        require(parts[-1] not in current, 'Tree path collision')
        current[parts[-1]] = content
    def encode(node: dict) -> str:
        entries = []
        for name, value in node.items():
            encoded = name.encode('utf-8')
            if isinstance(value, dict):
                sort_key = encoded+b'/'
                entry = b'40000 '+encoded+b'\0'+bytes.fromhex(encode(value))
            else:
                sort_key = encoded
                entry = b'100644 '+encoded+b'\0'+bytes.fromhex(git_oid('blob', value))
            entries.append((sort_key, entry))
        return git_oid('tree', b''.join(entry for _, entry in sorted(entries)))
    return encode(nested)


def verify(path: Path) -> dict:
    data, modes = load(Path(path))
    require(SPECIAL <= data.keys(), 'Packet manifest/checksum missing')
    expected_checksum = digest(data['MANIFEST.json'])+'  MANIFEST.json\n'
    require(data['MANIFEST.sha256'].decode('ascii') == expected_checksum,
            'Manifest checksum mismatch')
    manifest = strict_json(data['MANIFEST.json'])
    require(manifest.get('schema') == 'orthemology-continuity-packet-v1', 'Unknown schema')
    rows = manifest.get('files')
    require(isinstance(rows, list), 'Manifest file list missing')
    require(manifest.get('file_count') == len(rows), 'Manifest file count mismatch')
    seen = set()
    for row in rows:
        require(isinstance(row, dict), 'Invalid manifest row')
        name = safe_path(row['path'])
        require(name not in seen and name not in SPECIAL, 'Duplicate/reserved manifest path')
        seen.add(name)
        require(name in data, 'Missing payload: '+name)
        require(isinstance(row.get('bytes'), int) and row['bytes'] == len(data[name]),
                'Size mismatch: '+name)
        require(isinstance(row.get('sha256'), str) and
                re.fullmatch(r'[0-9a-f]{64}', row['sha256']) is not None,
                'Malformed SHA-256: '+name)
        require(digest(data[name]) == row['sha256'], 'Hash mismatch: '+name)
    require(set(data) == seen | SPECIAL, 'Unexpected payload files')
    input_count = 0
    if 'inventory/INPUT_IDENTITIES.json' in data:
        for row in strict_json(data['inventory/INPUT_IDENTITIES.json'])['files']:
            name = safe_path(row['path'])
            require(name in data and len(data[name]) == row['bytes'] and
                    digest(data[name]) == row['sha256'], 'Input identity mismatch: '+name)
            input_count += 1
    publication = manifest.get('publication')
    publication_receipt = None
    if publication is not None:
        prefix = safe_path(publication['prefix'])+'/'
        selected = {n[len(prefix):]: b for n, b in data.items() if n.startswith(prefix)}
        require(len(selected) == publication['file_count'], 'Publication count mismatch')
        for name in selected:
            require(not modes[prefix+name] & 0o111, 'Unexpected executable publication mode')
        computed = git_tree(selected)
        require(computed == publication['git_tree'], 'Publication Git-tree mismatch')
        publication_receipt = {'files': len(selected), 'git_tree': computed,
                               'declared_file_git_mode': '100644'}
    return {'status': 'PASS', 'payload_files': len(rows), 'total_files': len(data),
            'payload_bytes': sum(len(data[n]) for n in seen),
            'original_input_identities_checked': input_count,
            'manifest_sha256': digest(data['MANIFEST.json']),
            'publication': publication_receipt,
            'research_code_executed': False, 'source_files_modified': False,
            'network_access': False, 'lean_replay': False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet', type=Path, nargs='?', default=Path('.'))
    args = parser.parse_args()
    try:
        print(json.dumps(verify(args.packet), indent=2))
        return 0
    except (ValueError, OSError, KeyError, TypeError, UnicodeError,
            json.JSONDecodeError, zipfile.BadZipFile) as error:
        print('FAIL: '+str(error), file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
