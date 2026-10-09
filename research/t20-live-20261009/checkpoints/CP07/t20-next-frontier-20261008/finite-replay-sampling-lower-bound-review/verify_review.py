#!/usr/bin/env python3
"""Verify this bounded review's exact source and payload hashes; no file writes."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent
BASE=HERE.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((HERE/'MANIFEST.json').read_text())
r=json.loads((HERE/'REVIEW_RECEIPT.json').read_text())
checked=[]
for obj in m['files']:
    p=HERE/obj['path']
    assert p.is_file(),str(p)
    assert p.stat().st_size==obj['bytes'],str(p)
    assert sha(p)==obj['sha256'],str(p)
    checked.append('review:'+obj['path'])
for obj in r['author_artifacts']:
    p=BASE/obj['path']
    assert p.stat().st_size==obj['bytes'] and sha(p)==obj['sha256'],str(p)
    snap=HERE/obj['snapshot']
    assert snap.read_bytes()==p.read_bytes(),str(snap)
    checked.append('author:'+obj['path'])
for obj in r['prerequisite_sources']:
    p=BASE/obj['path']
    assert sha(p)==obj['sha256'],str(p)
    checked.append('prerequisite:'+obj['path'])
p=json.loads((HERE/'PREFREEZE_DERIVATION_RECEIPT.json').read_text())
assert p['author_result_read'] is False
assert sha(HERE/p['file'])==p['sha256']
c=json.loads((HERE/'INDEPENDENT_CONTROLS.json').read_text())
assert c['status']=='PASS' and c['check_count']==4922
assert len(c['certified_Joe_examples'])==36
assert len(c['adaptive_rational_proxy_prefixes'])==5
assert r['verdict']=='PASS' and not r['blocking_findings']
print(json.dumps({'status':'PASS','bound_files':len(checked),'checks':checked,'independent_control_assertions':c['check_count'],'scope':r['scope']},indent=2))
