#!/usr/bin/env python3
"""Verify the explicit public projection, not the complete original packet."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

def sha256(data):
    return hashlib.sha256(data).hexdigest()

def safe_path(root, relative):
    parsed=PurePosixPath(relative)
    if parsed.is_absolute() or '..' in parsed.parts or str(parsed)!=relative:
        raise ValueError(f'noncanonical manifest path: {relative}')
    return root.joinpath(*parsed.parts)

def verify_tree(root):
    root=Path(root)
    manifest=json.loads((root/'PROJECTION_MANIFEST.json').read_text())
    seen=set()
    counts={}
    for group in ('retained','independent_review','added'):
        entries=manifest[group]
        for item in entries:
            name=item['public_path']
            if name in seen: raise ValueError(f'duplicate public path: {name}')
            seen.add(name)
            data=safe_path(root,name).read_bytes()
            if len(data)!=item['bytes'] or sha256(data)!=item['sha256']:
                raise ValueError(f'public bytes differ: {name}')
            if group=='retained' and item.get('original_sha256',item['sha256'])!=item['sha256']:
                raise ValueError(f'retained scientific source was transformed: {name}')
        counts[group]=len(entries)
    for item in manifest['excluded']:
        if safe_path(root,item['original_path']).exists():
            raise ValueError(f'excluded process/full-manifest file present: {item["original_path"]}')
    counts['excluded']=len(manifest['excluded'])
    return counts

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source-freeze',type=Path,help='Optional unchanged original v2 freeze for direct comparison')
    args=parser.parse_args()
    root=Path(__file__).resolve().parent
    counts=verify_tree(root)
    manifest=json.loads((root/'PROJECTION_MANIFEST.json').read_text())
    if args.source_freeze:
        data=(args.source_freeze/'PACKAGE_MANIFEST.json').read_bytes()
        if sha256(data)!=manifest['original_v2_manifest_sha256']:
            raise ValueError('original v2 manifest identity differs')
        for item in manifest['retained']+manifest['excluded']:
            data=safe_path(args.source_freeze,item['original_path']).read_bytes()
            if len(data)!=item['bytes'] or sha256(data)!=item.get('original_sha256',item['sha256']):
                raise ValueError(f'original source changed: {item["original_path"]}')
    print(json.dumps({'status':'PASS','scope':'Explicit public projection; no claim of full original-packet inclusion',**counts},indent=2))

if __name__=='__main__':main()
