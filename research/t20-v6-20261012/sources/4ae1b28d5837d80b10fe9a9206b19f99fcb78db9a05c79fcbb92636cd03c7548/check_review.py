#!/usr/bin/env python3
"""Portable integrity and control replay. Writes only to a fresh output directory."""
import argparse, hashlib, json, subprocess, sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser()
ap.add_argument('--output-dir',required=True,type=Path)
ap.add_argument('--original-root',type=Path)
a=ap.parse_args()
if a.output_dir.exists(): ap.error('output directory must be fresh')
a.output_dir.mkdir(parents=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_packet(root,manifest_name):
    manifest=json.loads((root/manifest_name).read_text())
    for rel,h in manifest['files'].items(): assert digest(root/rel)==h,rel
    payload=''.join(rel+'\0'+h+'\n' for rel,h in sorted(manifest['files'].items())).encode()
    assert hashlib.sha256(payload).hexdigest()==manifest['snapshot_digest']
    return manifest
review=verify_packet(BASE,'REVIEW_MANIFEST.json')
author=verify_packet(BASE/'author_snapshot','FROZEN_MANIFEST.json')
independent=subprocess.check_output([sys.executable,str(BASE/'check_independent.py')])
assert independent==(BASE/'INDEPENDENT_CONTROLS.json').read_bytes()
(a.output_dir/'INDEPENDENT_CONTROLS.json').write_bytes(independent)
subprocess.run([sys.executable,str(BASE/'author_snapshot/check_exact.py'),'--output-dir',str(a.output_dir/'portable_author')],check=True)
assert (a.output_dir/'portable_author/EXACT_CHECKS.json').read_bytes()==(BASE/'author_snapshot/portable-author-run/EXACT_CHECKS.json').read_bytes()
original_count=0
if a.original_root:
    subprocess.run([sys.executable,str(BASE/'author_snapshot/check_exact.py'),'--output-dir',str(a.output_dir/'with_originals'),'--original-root',str(a.original_root)],check=True)
    assert (a.output_dir/'with_originals/EXACT_CHECKS.json').read_bytes()==(BASE/'author_snapshot/author-run/EXACT_CHECKS.json').read_bytes()
    original_count=6
verify_packet(BASE,'REVIEW_MANIFEST.json')
verify_packet(BASE/'author_snapshot','FROZEN_MANIFEST.json')
r={'status':'PASS','review_snapshot':review['snapshot_digest'],'author_snapshot':author['snapshot_digest'],'author_portable_check_count':85,'independent_control_count':10,'original_preservation_count':original_count,'scope':'Integrity and finite exact controls; ordinary mathematics is reviewed in REVIEW.md. No formal-kernel, integration, or closure authority.'}
(a.output_dir/'REPLAY_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps(r))
