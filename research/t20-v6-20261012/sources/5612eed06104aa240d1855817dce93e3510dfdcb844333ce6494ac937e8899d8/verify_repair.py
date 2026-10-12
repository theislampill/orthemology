from pathlib import Path
from fractions import Fraction as F
from itertools import product
import json,hashlib
import sympy as s
ROOT=Path(__file__).resolve().parent
checks=[]
def check(name,condition):
 if not condition: raise AssertionError(name)
 checks.append(name)
def norm(v):
 z=sum(v);return tuple(x/z for x in v)
L=((F(1,4),F(1,2),F(3,4)),(F(3,4),F(1,2),F(1,4)))
q=(F(1,2),F(1,4),F(1,4)); p=norm(tuple(x*x for x in q))
check('inverse square readout',p==(F(2,3),F(1,6),F(1,6)))
g=sum(x*y for x,y in zip(L[0],p))
check('nonlinear outcome mass',g==F(3,8))
check('direct q probability differs',sum(x*y for x,y in zip(L[0],q))==F(7,16)!=g)
p1=norm(tuple(x*l for x,l in zip(p,L[0])))
check('parent sequence first posterior',p1==(F(4,9),F(2,9),F(1,3)))
g1=sum(x*l for x,l in zip(p1,L[0]))
check('parent sequence second predictive mass',g1==F(17,36))
check('parent sequence joint word mass',g*g1==F(17,96))
p11=norm(tuple(x*l for x,l in zip(p1,L[0])))
check('parent sequence twice posterior',p11==(F(4,17),F(4,17),F(9,17)))
q11=(F(2,7),F(2,7),F(3,7))
check('parent sequence twice inverse readout',norm(tuple(x*x for x in q11))==p11)
# A squared escort coordinate w denotes q_i=sqrt(w_i)/sum_j sqrt(w_j).
# This exact redundant representation avoids approximating irrational q.
for length in range(9):
 for word in product(range(2),repeat=length):
  w=tuple(x*x for x in q); probability=F(1)
  for o in word:
   inv=norm(w); go=sum(l*x for l,x in zip(L[o],inv))
   check('kernel normalization '+str(word)+'/'+str(o),sum(sum(l*x for l,x in zip(row,inv)) for row in L)==1)
   probability*=go
   w=tuple(x*l for x,l in zip(w,L[o]))
  direct=tuple(p[i]*s.prod(L[o][i] for o in word) for i in range(3))
  check('history mass '+str(word),probability==sum(direct))
  check('history inverse readout '+str(word),norm(w)==norm(direct))
# Actual radical q transition checked separately against the squared representation.
raw=[s.Rational(x.numerator,x.denominator)*s.sqrt(s.Rational(l.numerator,l.denominator)) for x,l in zip(q,L[0])]
out=[x/sum(raw) for x in raw]
inv=[s.simplify(x*x/sum(y*y for y in out)) for x in out]
expected=norm(tuple(x*l for x,l in zip(p,L[0])))
check('actual radical transition inverse',all(s.simplify(x-s.Rational(y.numerator,y.denominator))==0 for x,y in zip(inv,expected)))
for item in json.loads((ROOT/'REPAIR_BINDINGS.json').read_text()):
 check('unchanged '+item['path'],hashlib.sha256((ROOT.parent/item['path']).read_bytes()).hexdigest()==item['sha256'])
result={'status':'PASS','assertion_groups':len(checks),'history_count':511,'maximum_history_length':8,'scope':'Exact author controls; finite enumeration supplements general proof.'}
(ROOT/'REPAIR_CHECKS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
