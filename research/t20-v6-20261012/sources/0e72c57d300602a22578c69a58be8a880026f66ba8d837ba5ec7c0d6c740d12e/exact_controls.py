#!/usr/bin/env python3
"""Exact finite rational controls; analytic limit conclusions are explained in REPORT.md."""
from fractions import Fraction as Q
import json
from pathlib import Path
r=Path(__file__).resolve().parent
half=lambda k:Q(1,2**k)
# For fair Cantor, every n-cylinder weighs 2^-n.
Hfair=lambda k,n:Q(int(n<=k))
# For sum_{j>=0} 2^(-j-1) delta_{e_j}, e_j has its sole 1 at coordinate j.
def geometric_cell_masses(n):return [half(j+1) for j in range(n)]+[half(n)]
def geometric_heavy(k,n):return sum((x for x in geometric_cell_masses(n) if half(k)<=x),Q(0))
# At the all-zero branch of half delta_0 plus half fair, cylinder mass is half+2^(-n-1).
tied=lambda n:Q(1,2)+half(n+1)
checks=0
for k in range(30):
 for n in range(30):
  assert Hfair(k,n)==int(half(k)<=half(n));checks+=1
  assert geometric_heavy(k,n)==(Q(1) if n<=k else 1-half(k));checks+=1
  assert sum(geometric_cell_masses(n))==1;checks+=1
  assert geometric_heavy(k,n+1)<=geometric_heavy(k,n);checks+=1
  assert geometric_heavy(k,n)<=geometric_heavy(k+1,n);checks+=1
 assert Hfair(k,k)==1 and Hfair(k,k+1)==0;checks+=1
 assert geometric_heavy(k,k+1)<1;checks+=1
 assert tied(k)>Q(1,2);checks+=1
for d in range(2,70):
 for num in range(d):
  q=Q(num,d);k=0
  while 1-half(k)<q:k+=1
  assert all(q<=geometric_heavy(k,n) for n in range(2*k+4));checks+=1
result={'status':'PASS','exact_checks':checks,'controls':[
 {'name':'swapped_depth_threshold','facts':'H_fair(k,n)=1 iff n<=k; fixed-k inf=0, fixed-n sup=1'},
 {'name':'strict_threshold_tie','facts':'half-Dirac/half-fair zero-cylinder mass=1/2+2^(-n-1)>1/2, but its singleton mass=1/2'},
 {'name':'q_equals_one','facts':'geometric atom law has H(k,n)=1 for n<=k, else 1-2^-k; atomic mass=1 but no fixed threshold captures mass 1'},
 {'name':'finite_horizon_false_positive','facts':'fair Cantor passes any finite depth window by choosing threshold index at least its last depth'}
]}
(r/'EXACT_CONTROLS_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
