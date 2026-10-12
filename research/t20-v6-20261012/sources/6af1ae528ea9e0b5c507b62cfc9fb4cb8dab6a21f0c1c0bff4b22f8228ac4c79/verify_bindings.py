#!/usr/bin/env python3
"""Verify the exact author payload reviewed here; optional live predecessors."""
import argparse, hashlib, json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--author-dir',required=True);p.add_argument('--original-root');p.add_argument('--output',required=True);a=p.parse_args()
root=Path(a.author_dir);bound=json.loads(Path(__file__).with_name('BINDINGS.json').read_text());checked=[]
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def require(ok,label):
    if not ok:raise RuntimeError('FAILED '+label)
    checked.append(label)
require(digest(root/'AUTHOR_FREEZE.json')==bound['author_freeze_sha256'],'author freeze digest')
manifest=json.loads((root/'AUTHOR_FREEZE.json').read_text())
for item in manifest['files']:
    f=root/item['path'];require(f.stat().st_size==item['bytes'] and digest(f)==item['sha256'],'author '+item['path'])
for item in json.loads((root/'INPUT_BINDINGS.json').read_text()):
    require(digest(root/item['snapshot'])==item['sha256'],'snapshot '+item['snapshot'])
    if a.original_root:require(digest(Path(a.original_root)/item['original'])==item['sha256'],'original '+item['original'])
require(digest(root/'RESULT.md')==bound['author_result_sha256'],'reviewed result identity')
require(digest(root/'gaussian_step.py')==bound['implementation_sha256'],'reviewed implementation identity')
out={'status':'PASS','count':len(checked),'checked':checked};Path(a.output).write_text(json.dumps(out,indent=2)+'\n');print(f'PASS {len(checked)} digest bindings')
