from fractions import Fraction as F
from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent
cases=0;thresholds=0;undefined=0
for pi in range(1,10):
 p=F(pi,10)
 for ai in range(11):
  a=F(ai,10)
  for bi in range(11):
   b=F(bi,10);D=p*a+(1-p)*b
   if D==0:
    undefined+=1;continue
   q=p*a/D
   assert q-p==p*(1-p)*(a-b)/D
   assert (q<p)==(a<b)
   assert (q==p)==(a==b)
   assert (q>p)==(a>b)
   if b>0:assert q/(1-q)==(p/(1-p))*(a/b)
   for ti in range(1,10):
    t=F(ti,10)
    assert (q<=t)==(p*a*(1-t)<=t*(1-p)*b)
    thresholds+=1
   cases+=1
examples=[]
for p,a,b in [(F(1,2),F(1,100),F(99,100)),(F(9,10),F(1,100),F(9,10)),(F(1,2),F(1,4),F(3,4)),(F(1,100),F(3,4),F(1,4)),(F(4,5),F(1,2),F(1,2))]:
 q=p*a/(p*a+(1-p)*b)
 examples.append({'p':str(p),'a':str(a),'b':str(b),'q':str(q)})
assert examples[0]['q']=='1/100' and examples[1]['q']=='1/11'
out={'status':'PASS','grid_valid_binary_models':cases,'threshold_checks':thresholds,'zero_evidence_probability_cases_excluded':undefined,'examples':examples,'scope':'Exact rational controls only. Identities are algebraically derived in review. No empirical/theological assignments, no equal-prior prescription, no runtime routing test.'}
(R/'INDEPENDENT_CONTROLS.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
