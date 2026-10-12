from fractions import Fraction as Q
from pathlib import Path
from itertools import product
import json
from polynomial_oracle import params,polynomial_coefficients,baseline,candidate,bary,losses,TRUTHS
R=Path(__file__).resolve().parents[1]
def components(s,z,w,h):
 m,e,r,T,g,b,theta=params(s,z,w,h);h1,h2,hz,hw=h
 GH=[e-2*(s-v[0])*b+(v[2]+v[3]-T)*g for v in TRUTHS]
 FH=[r*e+(s-v[0])*(96*s*e-2*r*b)+100*(v[2]+v[3]-T)*g for v in TRUTHS]
 GC=[-b*(h1+h2)-g*(hz+hw),-(b*b+g*g)]
 FC=[polynomial_coefficients(s,h,b,g,v[0]) for v in TRUTHS]
 B0=[1+s-z-w,z-s,w-s,s];B1=[m-hz-hw,hz-m,hw-m,m];B2=[b-2*g,g-b,g-b,b]
 P=[s,s,z,w];heads=GH+FH+B0+P+[1-x for x in P]
 budgets=[sum(map(abs,GC))]*4+[sum(map(abs,c)) for c in FC]+[abs(x)+abs(y) for x,y in zip(B1,B2)]+list(map(abs,h))+list(map(abs,h))
 def rem(ep):
  val=lambda c:sum(a*ep**i for i,a in enumerate(c))
  return [val(GC)]*4+[val(c) for c in FC]+[x+ep*y for x,y in zip(B1,B2)]+list(h)+[-x for x in h]
 delta=1/(1+sum(2*(B+1)/H for H,B in zip(heads,budgets)))
 return heads,budgets,rem,delta

def main():
 contexts=[]
 for weights in product([1,2,4],repeat=4):
  a=[Q(x,sum(weights)) for x in weights];contexts.append((a[3],a[1]+a[3],a[2]+a[3]))
 for k in [3,6,12]:
  for small in range(4):
   a=[Q(1)]*4;a[small]=Q(1,10**k);a=[x/sum(a) for x in a];contexts.append((a[3],a[1]+a[3],a[2]+a[3]))
 dirs=[(1,0,0,0),(-1,0,0,0),(0,1,3,-2),(100,99,-100,120),(1,-1,1000,-1000),(Q(1,1000),0,1,-1)]
 records=[]
 for s,z,w in contexts:
  for raw in dirs:
   h=tuple(map(Q,raw));H,B,rem,d=components(s,z,w,h);assert len(H)==len(B)==20
   assert min(H)>0 and min(B)>=0 and 0<d<=1
   assert all(d<hh/(2*(bb+1)) for hh,bb in zip(H,B))
   for ep in [Q(0),d/2,d*Q(999,1000),Q(1)]:assert all(abs(rr)<=bb for rr,bb in zip(rem(ep),B))
   ep=d*Q(999,1000);rawconstraints=[hh+ep*rr for hh,rr in zip(H,rem(ep))];assert min(rawconstraints)>0
   I=baseline(s,z,w,h,ep);O=candidate(s,z,w,h,ep);assert all(0<x<1 for x in I+O)
   actual=[(losses(v,I)[0]-losses(v,O)[0])/ep**2 for v in TRUTHS]+[(losses(v,I)[1]-losses(v,O)[1])/ep**2 for v in TRUTHS]+list(bary(O))+list(I)+[1-x for x in I]
   assert actual==rawconstraints
   records.append({'context':list(map(str,(s,z,w))),'direction':list(map(str,h)),'delta':str(d),'epsilon':str(ep),'minimum_constraint':str(min(actual))})
 sample=components(Q(1,4),Q(1,2),Q(1,2),(Q(1),Q(0),Q(0),Q(0)))
 # Meaningful universal-budget controls.
 assert abs(Q(1)+Q(-1)*Q(0))>sum([Q(1),Q(-1)])
 H=[Q(1,100)];B=[Q(1)];wrong=1/(1+sum(2*(b+1)*h for h,b in zip(H,B)));ep=wrong/2
 assert H[0]+ep*(-B[0])<0
 out={'status':'PASS','case_count':len(records),'constraint_count_per_case':20,'exact_constraint_identities':20*len(records),'all_remainder_bound_tests':80*len(records),'cases':records,'sample_delta':str(sample[3]),'controls':{'dropping_absolute_coefficient_values_fails':True,'multiplying_by_head_in_radius_fails':True},'scope':'Exact-rational evaluation of the newly defined 20-constraint radius; universal claim separately kernel checked.'}
 (R/'evidence/SCALE_CHECKS.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='cases'},indent=2))
if __name__=='__main__':main()
