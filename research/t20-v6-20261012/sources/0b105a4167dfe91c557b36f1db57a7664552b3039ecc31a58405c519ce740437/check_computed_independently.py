#!/usr/bin/env python3
"""Independent exact cross-checks for the t=1 certificate; no witness search."""
from pathlib import Path
from fractions import Fraction as Q
from math import factorial
from datetime import datetime, timezone
import contextlib, hashlib, io, json, runpy

HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
captured=io.StringIO()
with contextlib.redirect_stdout(captured):
    independent=runpy.run_path(str(HERE/'check_effectivity.py'))
(HERE/'exact_controls.log').write_text(captured.getvalue())
SOURCE=HERE/'computed-author-frozen-copy'
checks=[]
def check(label,ok):
    if not ok: raise AssertionError(label)
    checks.append(label)
for name,expected in json.loads((SOURCE/'FROZEN_MANIFEST.json').read_text())['files'].items():
    check('frozen computed source '+name,hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()==expected)
hidden=json.loads((SOURCE/'HIDDEN_BOUND.json').read_text())
certificate=json.loads((SOURCE/'CERTIFICATE.json').read_text())
nf=independent['apply'](independent['prefixes'][6],independent['F'])
check('independent hidden prefix exactly equals author fraction',nf==Q(hidden['N_F_prefix']))
check('independent rigorous hidden upper exactly equals author fraction',nf+Q(1,16)==Q(hidden['N_F_upper']))
check('independent hidden upper below 2^171',nf+Q(1,16)<2**171)
check('hidden numerator bit length 2058',nf.numerator.bit_length()==2058)
check('hidden denominator bit length 1887',nf.denominator.bit_length()==1887)
for row in certificate['elementary_exponential_certificates']:
    x,n=Q(row['x']),row['taylor_order']
    # Direct powers/factorials rather than the author's incremental recurrence.
    lo=sum((x**k/factorial(k) for k in range(n+1)),Q(0))
    hi=lo+(x**(n+1)/factorial(n+1))/(1-x/Q(n+2))
    check(f'exp({x}) exact lower endpoint',lo==Q(row['rational_lower']))
    check(f'exp({x}) exact upper endpoint',hi==Q(row['rational_upper']))
    check(f'exp({x}) strict lower threshold',lo>row['strict_lower'])
    check(f'exp({x}) strict upper threshold',hi<row['strict_upper'])
    check(f'exp({x}) tail ratio below one',0<x/Q(n+2)<1)
check('rational strip length',Q(7,2)-Q(69,20)==Q(1,20))
check('strip minimum exponent arithmetic',2048*Q(69,20)-1097-Q(49,8)==Q(238499,40)>5962)
check('j=3 whole-term bound',6144-Q(9,2)-400==Q(11479,2)<5740)
check('j=4 whole-term bound threshold',8192-8-2980==5204)
check('all j>=4 decrement majorant',2048-4-Q(1,2)-6*2980<-1)
check('continuous exponent exceeds discrete-plus-hidden exponent',5962-5>5741+171+1)
check('normalization quotient strict upper threshold',Q(-2)/Q(3,2)==Q(-4,3))
check('rational lower endpoint exponent',2048**2//2+9==2097161)
check('reported rational upper endpoint',certificate['normalized_interval']['upper']=='-4/3')
check('reported exact compact integer endpoint',certificate['normalized_interval']['lower']=={'sign':-1,'base':3,'exponent':2097161})
check('sparse separator total degree',certificate['H']['total_degree']==2048+6==2054)
result={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','check_count':len(checks),'independent_effectivity_check_count':len(independent['checks']),'computed_proof_sha256':hashlib.sha256((SOURCE/'RESULT.md').read_bytes()).hexdigest(),'scope':'Independent rational prefix equality and exact Taylor endpoint/threshold checks, plus ordinary all-integer-tail proof review. No numerical integration or generic witness search.','checks':checks}
(HERE/'COMPUTED_INDEPENDENT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
