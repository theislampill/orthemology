#!/usr/bin/env python3
"""Verify the private launch's retained inputs. Standard library; no Git/network/writes."""
import hashlib
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parent.parent

def require(condition, message):
    if not condition:
        raise ValueError(message)

def checked_path(relative):
    require(isinstance(relative, str), 'Input path must be text')
    parts = relative.split('/')
    require(parts and parts[0] == 'inputs' and '\\' not in relative and ':' not in relative
            and all(p not in ('', '.', '..') and p.rstrip(' .').casefold() != '.git' for p in parts),
            'Unsafe input path: ' + relative)
    path = ROOT
    for part in parts:
        path = path / part
        require(not path.is_symlink(), 'Symlink input path: ' + relative)
    require(path.is_file(), 'Missing input: ' + relative)
    return path

def main():
    manifest_path = ROOT / 'INPUTS.json'
    require(not manifest_path.is_symlink(), 'Symlink manifest refused')
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    inputs = manifest['inputs']
    require(isinstance(inputs, list) and inputs, 'Empty or invalid input inventory')
    seen = set()
    for entry in inputs:
        relative = entry['path']
        path = checked_path(relative)
        require(relative.casefold() not in seen, 'Duplicate input: ' + relative)
        seen.add(relative.casefold())
        require(type(entry['bytes']) is int and entry['bytes'] >= 0, 'Invalid byte count')
        with path.open('rb') as source:
            digest = hashlib.file_digest(source, 'sha256').hexdigest()
        require(path.stat().st_size == entry['bytes'] and digest == entry['sha256'], 'MISMATCH ' + relative)
        if path.suffix.lower() == '.zip':
            with zipfile.ZipFile(path) as archive:
                require(archive.testzip() is None, 'CRC failure: ' + relative)
        print('PASS', relative, entry['bytes'])
    print('PASS_ALL_INPUTS', len(inputs))

if __name__ == '__main__':
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile) as error:
        print('REFUSED:', error, file=sys.stderr)
        sys.exit(1)
