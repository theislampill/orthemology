#!/usr/bin/env python3
"""Recheck bounded source preservation and final exact review targets."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

HERE=Path(__file__).resolve().parent
WORKSPACE=HERE.parent.parent

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

targets=json.loads((HERE/'REVIEW_TARGETS.json').read_text())
checked=[]
for target in targets:
    source=WORKSPACE/target['source']; snapshot=WORKSPACE/target['snapshot']
    actual=digest(source); copied=digest(snapshot)
    if actual != target['sha256'] or copied != actual:
        raise RuntimeError(('target currentness',target['source'],actual,copied,target['sha256']))
    checked.append({'path':target['source'],'sha256':actual,'snapshot_matches':True})
source_results=[]
for source in json.loads((HERE/'SOURCE_BINDINGS.json').read_text())['sources']:
    actual=digest(WORKSPACE/source['path'])
    if actual != source['sha256']:
        raise RuntimeError(('source changed',source['path'],actual,source['sha256']))
    source_results.append({'path':source['path'],'sha256':actual,'matches':True})
for mode in ['NORMAL','OPTIMIZED']:
    controls=json.loads((HERE/f'CONTROL_{mode}.json').read_text())
    if controls['status']!='PASS' or controls['check_count']!=62 or controls['script_sha256']!=digest(HERE/'check_independent.py'):
        raise RuntimeError('independent checks failed or stale')
    audit=json.loads((HERE/'author_snapshots/audit_symmetries'/f'REPLAY_{mode}.json').read_text())
    if audit['status']!='passed' or audit['control_groups']!=14 or audit['control_count']!=3054 or audit['script_sha256']!=digest(HERE/'author_snapshots/audit_symmetries/check_exact.py') or audit['report_sha256']!=digest(HERE/'author_snapshots/audit_symmetries/RESULT.md'):
        raise RuntimeError('audit replay failed or stale')
    restricted=json.loads((HERE/'author_snapshots/restricted_controls'/f'REPLAY_{mode}.json').read_text())
    if restricted['status']!='PASS' or restricted['count']!=31:
        raise RuntimeError('restricted replay failed')
if (HERE/'CONTROL_NORMAL.json').read_bytes()!=(HERE/'CONTROL_OPTIMIZED.json').read_bytes():
    raise RuntimeError('independent normal/optimized outputs differ')
result={'status':'PASS','checked_utc':datetime.now(timezone.utc).isoformat(),'targets':checked,'sources':source_results,'independent_checks':62,'audit_author_groups':14,'audit_author_count':3054,'restricted_author_controls':31,'review_sha256':digest(HERE/'REVIEW.md'),'scope':'Bounded exact target/source currentness; no global repository or kernel certification.'}
(HERE/'FINAL_CURRENTNESS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['targets','sources']},indent=2))
