#!/usr/bin/env python3
"""Replay all nine inherited interface rejections without changing their bytes."""
from pathlib import Path
import re,subprocess
ROOT=Path(__file__).resolve().parent.parent
controls=sorted((ROOT/'verification/inherited/negative-controls').glob('*.lean'))
assert len(controls)==9
for p in controls:
    r=subprocess.run(['lake','env','lean',str(p.relative_to(ROOT))],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    errors=[x for x in r.stdout.splitlines() if ': error:' in x]
    if not (r.returncode==1 and len(errors)==1 and re.search(r': error: (?:application )?type mismatch',errors[0])):
        print(r.stdout);raise SystemExit(f'Unexpected inherited negative-control outcome: {p.name}')
    print(f'EXPECTED_INHERITED_REJECTION: {p.name}')
print('INHERITED_NEGATIVE_CONTROLS_PASS: nine intended type errors; interface tests, not independence proofs')
