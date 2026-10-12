#!/usr/bin/env python3
"""Verify archive identities and replay both final controls into new output only."""
from pathlib import Path
import argparse, hashlib, json, shutil, subprocess, sys, platform

def rec(p):
    b=p.read_bytes(); return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def verify(root, entries):
    for name, wanted in entries.items():
        assert rec(root/name)==wanted, f'Identity mismatch: {root/name}'
    return len(entries)
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
R=Path(__file__).resolve().parent
O=a.output.resolve(); assert not O.exists(), 'Fresh output directory required'; O.mkdir(parents=True)
manifest=json.loads((R/'MANIFEST.json').read_text()); n=verify(R,manifest['files'])
W=R/'evidence'; A=W/'bounded-energy-signed-continuation-20261010'
freeze=json.loads((A/'FREEZE.json').read_text())
verify(A,{e['path']:{'bytes':e['bytes'],'sha256':e['sha256']} for e in freeze['files']})
for review in ['signed-energy-independent-review-20261010','signed-energy-independent-review-v2-20261010']:
    Q=W/review; m=json.loads((Q/'REVIEW_MANIFEST.json').read_text());verify(Q,m['files'])
    bindings=json.loads((Q/'ARTIFACT_BINDINGS.json').read_text())['source_files']
    verify(Q/'frozen_workspace',bindings)
for e in json.loads((A/'INPUT_BINDINGS.json').read_text())['files']:
    expected={'bytes':e['bytes'],'sha256':e['sha256']}
    assert rec(A/e['snapshot_path'])==expected==rec(W/e['original_path'])
Q=W/'signed-energy-independent-review-v2-20261010'
assert rec(A/'RESULT.md')==rec(Q/'frozen_workspace'/A.name/'RESULT.md')
assert rec(A/'FREEZE.json')==rec(Q/'frozen_workspace'/A.name/'FREEZE.json')
commands=[]
def run(cmd, log):
    r=subprocess.run(cmd,capture_output=True,text=True); (O/log).write_text(r.stdout+r.stderr)
    commands.append({'argv':cmd,'exit_code':r.returncode,'log':log});assert r.returncode==0,r.stderr
run([sys.executable,str(A/'check_controls.py'),'--retained-root',str(W),'--output-dir',str(O/'author')],'AUTHOR_REPLAY.log')
I=O/'independent';I.mkdir();shutil.copy2(Q/'independent_controls.py',I/'independent_controls.py')
run([sys.executable,str(I/'independent_controls.py')],'INDEPENDENT_REPLAY.log')
author=json.loads((O/'author/CONTROL_RESULTS.json').read_text());ind=json.loads((I/'INDEPENDENT_CONTROLS.json').read_text())
assert author['check_count']==501 and ind['count']==111
assert rec(O/'author/CONTROL_RESULTS.json')==rec(A/'CONTROL_RESULTS.json')
assert rec(I/'INDEPENDENT_CONTROLS.json')==rec(Q/'INDEPENDENT_CONTROLS.json')
verify(R,manifest['files'])
import sympy
receipt={'status':'PASS','scope':'Intermediate ordinary mathematical evidence; not a kernel proof, integration, T20 closure, or historical duration credit.','verified_payload_files':n,'author_checks':author['check_count'],'independent_checks':ind['count'],'author_result':rec(A/'RESULT.md'),'accepted_review':rec(Q/'REVIEW.md'),'author_freeze':rec(A/'FREEZE.json'),'payload_manifest':rec(R/'MANIFEST.json'),'fresh_outputs_byte_identical':True,'archived_inputs_unchanged':True,'python':platform.python_version(),'sympy':sympy.__version__,'commands':commands,'fresh_output_files':{str(f.relative_to(O)):rec(f) for f in sorted(O.rglob('*')) if f.is_file()}}
(O/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n'); print(json.dumps(receipt,indent=2))
