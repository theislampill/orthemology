from fractions import Fraction as F
import json
count=0
for qn in range(9):
 for qd in range(1,9):
  q=F(qn,qd)
  for a in range(17):
   for b in range(17):
    r=F(a,b) if b else F(0)
    assert (r<q)==(0<q.numerator and (b==0 or a*q.denominator<q.numerator*b))
    assert (q<r)==(b!=0 and q.numerator*b<a*q.denominator)
    # True membership above 1 cannot become a strict lower-cut witness.
    if r>=1: assert not(q<r and r<1)
    count+=1
# Ordinary supremum attainment guard: atom j has mass 2^-j, j>=1.
for k in range(1,101):
 assert sum((F(1,2**j) for j in range(1,k+1)),F(0))==1-F(1,2**k)<1
print(json.dumps({'rational_comparison_cases':count,'supremum_finite_controls':100,'result':'PASS','scope':'Exact Python Fraction controls, not Lean kernel theorems or general classification'}))
count=0
for a in range(13):
 for b in range(13):
  r=F(a,b) if b else F(0)
  complement=F(max(b-a,0),b) if b else F(1)
  assert complement==max(F(1)-r,F(0))
  for c in range(13):
   for d in range(13):
    s=F(c,d) if d else F(0)
    assert (r<s)==(d!=0 and c>0 and (b==0 or a*d<c*b))
    count+=1
print(json.dumps({'joint_code_comparison_cases':count,'complement_cases':169,'result':'PASS'}))
