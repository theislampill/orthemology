#!/usr/bin/env python3
"""Fail closed on any changed bound artifact, then replay review-only controls."""
from hashlib import sha256
from pathlib import Path
import json
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
receipt_path=ROOT/'REVIEW_RECEIPT.json'
receipt=json.loads(receipt_path.read_text())
assert receipt['verdict']=='PASS'

def digest(p):
    return sha256(p.read_bytes()).hexdigest()

def verify_artifacts():
    count=0
    for section in ['reviewed_artifacts','predecessor_bindings','review_artifacts']:
        for item in receipt[section]:
            path=ROOT/item['path']
            assert path.is_file(), f'Missing {path}'
            actual=digest(path)
            assert actual==item['sha256'], f'Digest changed: {path}: {actual}'
            count+=1
    return count

before=verify_artifacts()
subprocess.run([sys.executable,str(ROOT/'independent_controls.py')],cwd=ROOT,check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
if receipt.get('author_replay'):
    replay=receipt['author_replay']
    subprocess.run([sys.executable,str(ROOT/replay['script'])],cwd=ROOT/replay['cwd'],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
after=verify_artifacts()
print(json.dumps({
    'status':'PASS',
    'receipt_sha256':digest(receipt_path),
    'verified_artifacts_before':before,
    'verified_artifacts_after':after,
    'independent_assertions':receipt['independent_controls']['assertions_passed'],
    'scope':'These exact bound bytes and finite replay results only; no release or closure authority.'
},indent=2,sort_keys=True))
