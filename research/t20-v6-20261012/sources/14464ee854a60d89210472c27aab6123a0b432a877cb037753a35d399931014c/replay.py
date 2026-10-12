#!/usr/bin/env python3
"""Replay this exact review without live original sources or network."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
AUTHOR_MANIFEST_SHA256='ec678fb09461e8ea32a2826ee736919e3b7e780084fff9d491049f5715343dff'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def require(ok, message):
    if not ok: raise RuntimeError(message)

def run(out):
    out=out.resolve()
    require(out!=ROOT and ROOT not in out.parents,'Output directory must be outside the frozen review packet.')
    m=json.loads((ROOT/'REVIEW_MANIFEST.json').read_text())
    for e in m['files']:
        path=(ROOT/e['path']).resolve()
        require(ROOT in path.parents,'Unsafe manifest path: '+e['path'])
        require(path.stat().st_size==e['bytes'] and sha(path)==e['sha256'],'Review payload mismatch: '+e['path'])
    candidate=ROOT/'candidate_snapshot'
    require(sha(candidate/'FROZEN_MANIFEST.json')==AUTHOR_MANIFEST_SHA256,'Author manifest digest mismatch')
    am=json.loads((candidate/'FROZEN_MANIFEST.json').read_text())
    for e in am['files']:
        p=candidate/e['path']
        require(p.stat().st_size==e['bytes'] and sha(p)==e['sha256'],'Author payload mismatch: '+e['path'])
    out.mkdir(parents=True,exist_ok=True)
    subprocess.run([sys.executable,str(candidate/'verify.py'),'--output-dir',str(out/'author')],check=True,cwd=out)
    for f in ['CONTROL_RESULTS.json','verification.txt']:
        require((out/'author'/f).read_bytes()==(candidate/'author-run'/f).read_bytes(),'Author replay differs: '+f)
    subprocess.run([sys.executable,str(ROOT/'independent_controls.py'),'--output',str(out/'INDEPENDENT_RESULTS.json')],check=True,cwd=out)
    independent=json.loads((out/'INDEPENDENT_RESULTS.json').read_text())
    retained=json.loads((ROOT/'INDEPENDENT_RESULTS.json').read_text())
    require(independent==retained,'Independent replay differs from retained exact result')
    receipt={'status':'PASS','bound_review_files':len(m['files']),'bound_author_files':len(am['files']),'author_manifest_sha256':AUTHOR_MANIFEST_SHA256,'author_checks':json.loads((out/'author/CONTROL_RESULTS.json').read_text())['check_count'],'independent_checks':independent['control_count'],'author_outputs_byte_identical':True,'independent_output_identical':True,'scope':'Portable byte integrity and executable replay only; mathematical and quantifier review is in REVIEW.md.'}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt))

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--output-dir',type=Path,required=True)
    run(ap.parse_args().output_dir)
