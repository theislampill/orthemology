#!/usr/bin/env python3
from decimal import Decimal as D,localcontext
from pathlib import Path
import json
rows=0;maxerr=D(0)
with localcontext() as ctx:
 ctx.prec=300;tol=D('1e-70');log2=D(2).ln()
 for s in range(1,5):
  for a in range(1,4):
   q=s*a;dim=D(s*a**s)
   for m in range(1,5):
    alpha=D(q+2*m);beta=D(q*(m-1)+2*m*m)
    for eta in map(D,['0.1','0.5','1','2']):
     c=min(eta,D(1))**2/2;A=D(2*q*s)/(1-(-c).exp());assert A>=1
     for p in map(D,['1','0.75','0.25']):
      lam=(2/(2-p**int(dim))).ln();assert lam>0
      B=dim/lam*((alpha*(1+(2*A).ln()/c)+beta)*log2+log2)
      V=dim/lam*(alpha*log2/c+1);rate=1/V;assert B>=0 and V>0 and rate>0
      for u in map(D,['0','0.001','1','3','12']):
       N=int(((2*A).ln()+u).__truediv__(c).to_integral_value(rounding='ROUND_CEILING'));assert N>=1
       J=q*(N+m-1)+2*m*(N+m);assert D(J)==alpha*N+beta
       t=B+V*u
       first=A*(-c*N).exp();second=(D(J)*log2-lam*t/dim).exp();bound=(-u).exp()
       assert first<=bound/2+tol and second<=bound/2+tol and first+second<=bound+tol
       assert (rate/2-rate).exp()<1
       rows+=1;maxerr=max(maxerr,first+second-bound)
result={'status':'PASS','decimal_precision':300,'affine_cutoff_instances':rows,'largest_positive_roundoff_excess':str(maxerr),'coverage':{'states':'1..4','actions':'1..3','models':'1..4','eta':['0.1','0.5','1','2'],'p':['1','0.75','0.25'],'u':['0','0.001','1','3','12']},'strict_rate_boundary':'At theta=1/V the geometric factor equals 1; the finite-moment certificate requires theta<1/V','scope':'Numerical checks support, but do not replace, Lean proofs'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
