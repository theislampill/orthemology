#!/usr/bin/env python3
"""Exact rational controls for the explicit t=1 monomial separator.
The all-integer tail argument and inherited ordinary theorems are in RESULT.md.
No numerical quadrature, finite PSD inference, or witness search is used.
"""
from fractions import Fraction as Q
from pathlib import Path
import hashlib,json,runpy,time
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
started=time.perf_counter()
bindings=json.loads((HERE/'INPUT_BINDINGS.json').read_text())
for relative,expected in bindings.items():
 assert hashlib.sha256((ROOT/relative).read_bytes()).hexdigest()==expected, 'Input hash mismatch: '+relative
runpy.run_path(str(HERE/'compute_hidden_bound.py'),run_name='__main__')
hidden=json.loads((HERE/'HIDDEN_BOUND.json').read_text())
checks=[]
def check(name,condition):
 if not condition: raise AssertionError(name)
 checks.append(name)
def exp_bounds(x,n):
 x=Q(x); term=Q(1); total=term
 for k in range(1,n+1):
  term*=x/k; total+=term
 nxt=term*x/(n+1)
 ratio=x/(n+2)
 assert 0<=ratio<1
 return total,total+nxt/(1-ratio)
constants=[]
for x,n,lower,upper in [(1,12,2,3),(2,20,7,9),(5,30,60,149),(6,40,400,404),(7,50,1096,1097),(8,60,2980,2981)]:
 lo,hi=exp_bounds(x,n)
 check(f'exp({x})>{lower}',lo>lower)
 check(f'exp({x})<{upper}',hi<upper)
 constants.append({'x':x,'taylor_order':n,'strict_lower':lower,'strict_upper':upper,'rational_lower':str(lo),'rational_upper':str(hi)})
B=Q(hidden['N_F_upper'])
check('hidden exact prefix plus proved tail below 2^171',B<2**171)
check('only Schur indices through 10',hidden['schur_maximum_index']==10)
check('active interval length 1/20',Q(7,2)-Q(69,20)==Q(1,20))
a=2048*Q(69,20)-1097-Q(49,8)
check('continuous integral exponent exceeds 5962',a>5962)
check('j=3 exponent below 5740',2048*3-Q(9,2)-400<5740)
check('j=4 exponent below 5204',2048*4-8-2980==5204)
check('j>=4 discrete exponent decrement below -1',2048-Q(9,2)-6*2980<-1)
check('low-tail exponent 4096 below 5204',4096<5204)
check('four-times-tail absorbed with e>2',5740-5204>=2)
check('B J exponent at most 5912',171+5741==5912)
check('I lower exponent after e^5>60',5962-5==5957)
check('I exponent advantage exceeds 1',5957-5912>1)
check('full polynomial total degree 2054',2*1024+6==2054)
check('normalizer at most 3/2 and W<-2 imply L<-4/3',Q(-2)/Q(3,2)==Q(-4,3))
check('unweighted active moment exponent',2048**2//2==2097152)
check('rational lower endpoint exponent',2097152+9==2097161)
result={'status':'PASS','t':'1','q':{'coefficient':'1','z_exponent':1024},'H':{'formula':'z^2048 * (1+u^4*v^2+u^2*v^4-u^2*v^2)','total_degree':2054,'nonzero_monomials':4},'hidden_upper_bound':'2^171','unnormalized_W_strict_upper':'-2','normalized_L_strict_upper':'-4/3','normalized_interval':{'lower':{'sign':-1,'base':3,'exponent':2097161},'upper':'-4/3'},'continuous_lower':'exp(5962)/60','discrete_upper':'exp(5741)','exact_checks':checks,'elementary_exponential_certificates':constants,'elapsed_seconds':time.perf_counter()-started,'evidence_scope':'Exact finite arithmetic and rational Taylor bounds, with the explicit all-integer lattice-tail proof in RESULT.md and inherited ordinary construction. Not a Lean kernel proof.'}
(HERE/'CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ['exact_checks','elementary_exponential_certificates']},indent=2))
print('Exact checks:',len(checks))
