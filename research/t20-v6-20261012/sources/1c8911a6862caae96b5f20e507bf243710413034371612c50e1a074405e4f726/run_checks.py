#!/usr/bin/env python3
"""Run both interpreters and demand actual rejection of false controls."""
import hashlib,json,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
rows=[]
for optimized in (False,True):
    base=[sys.executable]+(['-O'] if optimized else [])+[str(HERE/'verify.py')]
    output=HERE/('CHECKS_OPTIMIZED.json' if optimized else 'CHECKS_NORMAL.json')
    p=subprocess.run(base+['--output',str(output)],text=True,capture_output=True)
    if p.returncode!=0:raise RuntimeError(p.stdout+p.stderr)
    parsed=json.loads(p.stdout)
    if parsed['status']!='PASS' or parsed['checks']!=13676:raise RuntimeError('Unexpected positive result')
    rows.append({'optimized':optimized,'test':'positive','returncode':p.returncode,'checks':parsed['checks']})
    for control in ('guard','scalar'):
        p=subprocess.run(base+['--negative-control',control],text=True,capture_output=True)
        if p.returncode==0 or 'ACTIVE_CHECK_FAILED' not in p.stderr:
            raise RuntimeError('Negative control did not actively fail: '+control)
        rows.append({'optimized':optimized,'test':control,'returncode':p.returncode,
                     'failure':p.stderr.splitlines()[-1]})
if (HERE/'CHECKS_NORMAL.json').read_bytes()!=(HERE/'CHECKS_OPTIMIZED.json').read_bytes():
    raise RuntimeError('Optimized and ordinary checks differ')
result={'status':'PASS','runs':rows,'verify_sha256':hashlib.sha256((HERE/'verify.py').read_bytes()).hexdigest()}
(HERE/'RUN_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
