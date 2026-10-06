#!/usr/bin/env python3
"""Link a user-supplied prepared pinned Mathlib environment after verification."""
from pathlib import Path
import json,sys
from verify_dependencies import ROOT,verify
if len(sys.argv)!=2:raise SystemExit('usage: reuse_dependencies.py PATH_TO_PREPARED_MATHLIB')
mathlib=Path(sys.argv[1]).resolve();links=[]
for p in json.loads((ROOT/'lake-manifest.json').read_text())['packages']:
    src=mathlib if p['name']=='mathlib' else mathlib/'.lake/packages'/p['name']
    verify(src,p);dst=ROOT/'.lake/packages'/p['name']
    assert not dst.exists() or dst.resolve()==src.resolve(),f"Conflicting dependency: {p['name']}"
    links.append((src,dst))
for src,dst in links:
    dst.parent.mkdir(parents=True,exist_ok=True)
    if not dst.exists():dst.symlink_to(src,target_is_directory=True)
print('PINNED_DEPENDENCIES_LINKED: no project output reused')
