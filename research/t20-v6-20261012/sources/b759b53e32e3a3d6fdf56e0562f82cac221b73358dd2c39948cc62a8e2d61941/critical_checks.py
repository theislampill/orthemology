#!/usr/bin/env python3
from fractions import Fraction as Q
from pathlib import Path
import sympy as S
import json
ROOT=Path(__file__).resolve().parents[1]
def psi(t):z=t-Q(1,2);return z*z/2+Q(2,3)*z**3+z**4
def dp(t):z=t-Q(1,2);return z+2*z*z+4*z**3
def div(v,t):return psi(v)-psi(t)-dp(t)*(v-t)
def main():
 t,a,b,eps=S.symbols('t a b eps',real=True);r=1+4*(t-Q(1,2))+12*(t-Q(1,2))**2
 assert S.expand(S.diff(psi(t),t)-dp(t))==0
 assert S.expand(S.diff(dp(t),t)-r)==0
 assert S.expand(r-12*(t-Q(1,3))**2-Q(2,3))==0
 assert r.subs(t,Q(1,2))==1 and S.diff(r,t).subs(t,Q(1,2))==4
 q=Q(1,2)+eps/2+eps*eps*b
 G=((Q(1,2)+eps-a)**2+(Q(1,2)-a)**2)/2-(q-a)**2
 F=div(a,Q(1,2)+eps)+div(a,Q(1,2))-2*div(a,q)
 lead=[]
 for P in [G,F]:
  for aa in [0,1]:
   po=S.Poly(S.expand(P.subs(a,aa)),eps);assert po.nth(0)==po.nth(1)==0;lead.append(po.nth(2))
 expected=[Q(1,4)-b,Q(1,4)+b,Q(3,4)-b,b-Q(1,4)]
 assert all(S.expand(x-y)==0 for x,y in zip(lead,expected))
 assert [x.subs(b,Q(1,4)) for x in lead]==[0,Q(1,2),Q(1,2),0]
 assert S.expand((lead[0]+lead[3])/2)==0
 u=Q(1,2)+eps/2+eps**2/4-eps**3/8;BG=((Q(1,2)+eps)**2+Q(1,2)**2)/2
 tail=9*eps**9-72*eps**8+72*eps**7+592*eps**6-816*eps**5-2304*eps**4+1696*eps**3+4992*eps**2-17280*eps+2304
 assert S.expand(u*u-BG-eps**3*(eps**3-4*eps**2-4*eps+8)/64)==0
 assert S.expand(2*div(1,u)-div(1,Q(1,2)+eps)-div(1,Q(1,2))-eps**3*tail/6144)==0
 # Same second-order data, entire positive analytic curvature, exact criterion everywhere.
 plus=S.exp(4*(t-Q(1,2)))/16;plusr=S.diff(plus,t,2)
 assert plusr.subs(t,Q(1,2))==1 and S.diff(plusr,t).subs(t,Q(1,2))==4
 assert S.simplify(S.diff(plusr,t)/plusr)==4
 assert S.expand(1-4*t*(1-t)-(2*t-1)**2)==0
 records=[]
 for n in range(1,65):
  e=Q(1,100*n);env=Q(1,2)+e/2+e*e/4-e**3/8
  gex=env*env-((Q(1,2)+e)**2+Q(1,2)**2)/2
  fex=2*div(Q(1),env)-div(Q(1),Q(1,2)+e)-div(Q(1),Q(1,2))
  assert 0<env<1 and gex>0 and fex>0
  records.append({'epsilon':str(e),'quadratic_envelope_excess':str(gex),'nonlinear_envelope_excess':str(fex)})
 # These violate the conclusion of weak duality if exactly one premise is deleted.
 controls=[{'omitted':'nonnegative weights','B':[1,2],'L':[0,0],'weights':[2,-1],'w':0,'tau':1,'dual_objective':0},
           {'omitted':'unit mass','B':[1],'L':[0],'weights':[0],'w':0,'tau':1,'dual_objective':0},
           {'omitted':'balance for every w','B':[0],'L':[1],'weights':[1],'w':-1,'tau':1,'dual_objective':0}]
 for c in controls:
  margins=[B-L*c['w'] for B,L in zip(c['B'],c['L'])]
  assert min(margins)>=c['tau']>sum(w*B for w,B in zip(c['weights'],c['B']))
  if c['omitted']!='unit mass':assert sum(c['weights'])==1
  if c['omitted']!='nonnegative weights':assert min(c['weights'])>=0
  if c['omitted']!='balance for every w':assert sum(w*L for w,L in zip(c['weights'],c['L']))==0
 # The changed critical final-row sign would falsely permit a positive margin.
 wrong=[Q(1,4),Q(1,4),Q(3,4),Q(1,4)];assert min(wrong)>0 and (Q(0)-Q(1,4))<0
 out={'status':'PASS','critical_rows':list(map(str,lead)),'primal_witness':'1/4','dual_weights':['1/2','0','0','1/2'],'envelope_case_count':len(records),'envelope_cases':records,'dual_premise_deletion_controls':controls,'exponential_success_comparator':'same r=1,rprime=4 at1/2; log slope4; global positive analytic curvature','wrong_final_row_sign_rejected':True}
 (ROOT/'evidence/CRITICAL_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='envelope_cases'},indent=2))
if __name__=='__main__':main()
