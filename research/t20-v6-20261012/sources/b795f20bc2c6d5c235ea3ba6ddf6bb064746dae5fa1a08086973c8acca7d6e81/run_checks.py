#!/usr/bin/env python3
"""Run the author controls in normal and optimized modes and require rejections."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent.parent
records=[]
positive=[]
for optimize in (False,True):
    mode='optimized' if optimize else 'normal'
    base=[sys.executable]+(['-O'] if optimize else [])+[str(HERE/'check_exact.py')]
    result=subprocess.run(base,cwd=ROOT,capture_output=True,text=True)
    (HERE/f'positive-{mode}.stdout').write_text(result.stdout)
    (HERE/f'positive-{mode}.stderr').write_text(result.stderr)
    records.append({'mode':mode,'case':'positive','returncode':result.returncode})
    if result.returncode:
        raise RuntimeError(f'{mode} positive controls failed: {result.stderr}')
    parsed=json.loads(result.stdout)
    if parsed['status']!='PASS':raise RuntimeError('missing explicit successful status')
    positive.append(result.stdout)
    (HERE/f'EXACT_{mode.upper()}.json').write_text(result.stdout)
    for name in ('guard','iid_equals_exchangeable','scalar_pruning','horizon_closed'):
        result=subprocess.run(base+['--negative',name],cwd=ROOT,capture_output=True,text=True)
        (HERE/f'negative-{name}-{mode}.stdout').write_text(result.stdout)
        (HERE/f'negative-{name}-{mode}.stderr').write_text(result.stderr)
        records.append({'mode':mode,'case':name,'returncode':result.returncode})
        if result.returncode==0 or 'CONTROL FAILED: required false claim '+name not in result.stderr:
            raise RuntimeError(f'{mode} {name} did not reject actively')
if positive[0]!=positive[1]:raise RuntimeError('normal and optimized positive results differ')
report={'status':'PASS','positive_runs':2,'required_negative_rejections':8,'identical_positive_outputs':True,
        'checks_per_positive_run':json.loads(positive[0])['active_exact_checks'],'runs':records,
        'bound_author_sha256':{name:hashlib.sha256((HERE/name).read_bytes()).hexdigest() for name in ('RESULT.md','check_exact.py','READ_LEDGER.json')}}
(HERE/'RUN_RECEIPT.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
