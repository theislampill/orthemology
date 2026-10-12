#!/usr/bin/env python3
"""Reconstruct a NEW isolated source directory from this checkpoint.
Never modifies an existing repository or claims canonical adoption.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import zipfile

INPUT_SHA = '050aac77db52ad70e0155bbeb76f903a4dae65a36977a4159c8dcaf5634bcab0'
PREFIX = 'source-main/experiments/orthemology-v5/source/'

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--mode', choices=('baseline', 'proposal'), required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    dest = args.out.expanduser().absolute()
    if dest.exists():
        raise SystemExit(f'Refusing existing destination: {dest}')
    data = (root/'inputs/Orthemology_Pro_P03_Engine_Refinement.zip').read_bytes()
    if digest(data) != INPUT_SHA:
        raise SystemExit('Original input SHA-256 mismatch')
    # Validate everything before creating the new directory.
    source: dict[str, bytes] = {}
    with zipfile.ZipFile(root/'inputs/Orthemology_Pro_P03_Engine_Refinement.zip') as z:
        if z.testzip() is not None:
            raise SystemExit('Input CRC failure')
        names = z.namelist()
        if len(names) != len(set(names)):
            raise SystemExit('Duplicate input members')
        for name in names:
            if name.startswith(PREFIX) and not name.endswith('/'):
                rel = name[len(PREFIX):]
                p = PurePosixPath(rel)
                if p.is_absolute() or '..' in p.parts or '\\' in rel:
                    raise SystemExit('Unsafe source path')
                source[rel] = z.read(name)
    if len(source) != 70:
        raise SystemExit(f'Unexpected source population: {len(source)}')
    changes = []
    if args.mode == 'proposal':
        mapping = json.loads((root/'proposal/PATCH_MAP.json').read_text())
        for repo_path, row in mapping.items():
            rel = repo_path.removeprefix('experiments/orthemology-v5/source/')
            if rel not in source or digest(source[rel]) != row['preimage_sha256']:
                raise SystemExit(f'Preimage mismatch: {repo_path}')
            pre = (root/'proposal/preimages'/rel).read_bytes()
            post = (root/'proposal/postimages'/rel).read_bytes()
            if pre != source[rel] or digest(post) != row['postimage_sha256']:
                raise SystemExit(f'Proposal identity mismatch: {repo_path}')
            source[rel] = post
            changes.append(repo_path)
    dest.mkdir(parents=True, exist_ok=False)
    for rel, content in sorted(source.items()):
        p = dest/rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(content)
    print(json.dumps({'status':'ISOLATED_SOURCE_PREPARED', 'mode':args.mode,
        'destination':str(dest), 'source_files':len(source), 'changed_paths':changes,
        'input_sha256':INPUT_SHA, 'canonical_mutation':False,
        'files':{p:digest(b) for p,b in sorted(source.items())}}, indent=2))

if __name__ == '__main__':
    main()
