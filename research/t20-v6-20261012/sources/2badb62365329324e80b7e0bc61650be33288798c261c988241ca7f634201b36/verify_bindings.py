#!/usr/bin/env python3
"""Verify the complete review packet and frozen author snapshot without mutation."""
import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--original-root',type=Path);p.add_argument('--output-dir',type=Path);a=p.parse_args()
r=Path(__file__).resolve().parent
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,condition):
    if not condition:raise RuntimeError(name)
    checks.append(name)
bind=json.loads((r/'REVIEW_BINDINGS.json').read_text())
copy=r/'author-snapshot'
actual={str(p.relative_to(copy)):h(p) for p in sorted(copy.rglob('*')) if p.is_file()}
check('snapshot exact inventory and hashes',actual==bind['snapshot_hashes'])
check('author unchanged during review',bind['author_before']==bind['author_after'])
check('snapshot equals reviewed author',actual==bind['author_before'])
for row in json.loads((copy/'MANIFEST.json').read_text())['files']:
    f=copy/row['path'];check('author manifest '+row['path'],h(f)==row['sha256'] and f.stat().st_size==row['bytes'])
check('author review replay normal equals optimized',(r/'author-replay-normal/CHECKS.json').read_bytes()==(r/'author-replay-optimized/CHECKS.json').read_bytes())
check('author review replay equals frozen original',(r/'author-replay-normal/CHECKS.json').read_bytes()==(copy/'author-run/CHECKS.json').read_bytes())
check('independent normal equals optimized',(r/'independent-normal/CHECKS.json').read_bytes()==(r/'independent-optimized/CHECKS.json').read_bytes())
for row in json.loads((r/'MANIFEST.json').read_text())['files']:
    f=r/row['path'];check('review manifest '+row['path'],h(f)==row['sha256'] and f.stat().st_size==row['bytes'])
freeze=json.loads((r/'REVIEW_FREEZE.json').read_text())
check('review frozen digest',h(r/'REVIEW.md')==freeze['review_sha256'])
check('review manifest frozen digest',h(r/'MANIFEST.json')==freeze['manifest_sha256'])
if a.original_root:
    src=a.original_root/bind['author_path']
    check('live original author exact inventory and hashes',{str(p.relative_to(src)):h(p) for p in sorted(src.rglob('*')) if p.is_file()}==bind['author_before'])
out={'status':'PASS','count':len(checks),'checks':checks}
if a.output_dir:
    a.output_dir.mkdir(parents=True,exist_ok=True);(a.output_dir/'BINDING_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':'PASS','count':len(checks)}))
