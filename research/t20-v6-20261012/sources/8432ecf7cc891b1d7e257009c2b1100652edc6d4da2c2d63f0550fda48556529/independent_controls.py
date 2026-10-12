"""Independent symbolic and exact controls; no author imports. Continuum proofs are manual."""
from fractions import Fraction as Q
from itertools import product
import sympy as S
import json, sys
n=0
def require(ok,label):
 global n
 n+=1
 if not ok: raise RuntimeError(label)
t,s,c=S.symbols('t s c',real=True)
m=[S.Integer(1),S.Rational(1,2),S.Rational(1,3),t,s]
words=list(product((0,1),repeat=4))
# Inclusion-exclusion from joint-success moments, independent of author's word formula.
p={w:S.expand(sum((-1)**j*S.binomial(4-sum(w),j)*m[sum(w)+j] for j in range(5-sum(w)))) for w in words}
require(S.expand(sum(p.values()))==1,'normalization')
h=sum(p[w] for w in words if w[:2]==(1,1))
require(h==S.Rational(1,3),'history')
plans=[(False,lambda x:0),(False,lambda x:1),(True,lambda x:0),(True,lambda x:x),(True,lambda x:1-x),(True,lambda x:1)]
f=[]
for query,report in plans:
 f.append(S.expand(sum(p[w]*(int(report(w[2])!=w[3])+c*int(query)) for w in words if w[:2]==(1,1))/h))
expected=[3*t,1-3*t,c+3*t,c+6*(t-s),c+1-6*(t-s),c+1-3*t]
require(all(S.expand(x-y)==0 for x,y in zip(f,expected)),'six losses')
J=S.Matrix(f).jacobian([t,s])
require(J.rank()==2,'rank two')
require(J[[1,4],:].det()==-18,'inverse minor')
require(S.expand((1-f[1])/3)==t,'recover t')
require(S.expand(t-(c+1-f[4])/6)==s,'recover s')
L=12*t*t-4*t+S.Rational(4,9); U=-6*t*t+5*t-S.Rational(2,3)
require(S.expand(U-L+18*(t-S.Rational(2,9))*(t-S.Rational(5,18)))==0,'body gap')
mid=S.Rational(29,144); delta=S.Rational(1,1000)
require(S.Rational(1,144)>3*delta+12*delta**2,'explicit C4 interior square')
require(S.Rational(1,4)-delta>S.Rational(2,9) and S.Rational(1,4)+delta<S.Rational(5,18),'square t bounds')
# Exact rectangle is in C4: both boundary functions increase on this interval.
require(S.diff(L,t).subs(t,S.Rational(1,4)-delta)>0 and S.diff(U,t).subs(t,S.Rational(1,4)+delta)>0,'boundary monotonicity')
require(mid-delta>L.subs(t,S.Rational(1,4)+delta) and mid+delta<U.subs(t,S.Rational(1,4)-delta),'rectangle contained')
lam=[6*(t-s),4-24*t+12*s,18*t-6*s-3]
for z in lam:
 require(z.subs({t:S.Rational(1,4),s:S.Rational(7,36)})==S.Rational(1,3),'E4 interior center')
 require(S.Rational(1,3)>delta*(abs(S.diff(z,t))+abs(S.diff(z,s))),'E4 interior square')
for lo,hi in [(S.Rational(7,36),S.Rational(5,24)),(S.Rational(1,6),S.Rational(1,4))]:
 require(hi>lo,'nontrivial fixed-posterior fibre')
 require(S.expand(f[4].subs({t:S.Rational(1,4),s:hi})-f[4].subs({t:S.Rational(1,4),s:lo}))==6*(hi-lo),'fibre injection')
# Exhaust all two-tag assignments to three feasible same-posterior C4 points.
ss=[S.Rational(7,36),S.Rational(29,144),S.Rational(5,24)]
for tags in product(range(2),repeat=3):
 require(any(tags[i]==tags[j] and ss[i]!=ss[j] for i in range(3) for j in range(i)),'pigeonhole fixture')
# A one-dimensional restricted domain defeats an unqualified rank=>dimension claim.
curve=[S.expand(z.subs(s,L)) for z in f]
require(S.expand((1-curve[1])/3)==t,'one scalar suffices on lower boundary')
# A weaker policy menu has only rank one even on full domains.
require(S.Matrix(f[:2]).jacobian([t,s]).rank()==1,'skip-only countercontrol')
A=(S.Rational(1,6),0); B=(S.Rational(1,4),S.Rational(1,4)); C=(S.Rational(1,3),S.Rational(1,3))
mat=S.Matrix([[z.subs({t:x,s:y}) for z in f] for x,y in [A,B,C]])
pi=S.Matrix([0,S.Rational(4,5),0,0,S.Rational(1,5),0]); v=S.Rational(2,5)+c/5
require(mat*pi==S.Matrix([v,v,S.Rational(1,5)+c/5]),'symbolic primal')
eta=S.Matrix([ (3+4*c)/5,(2-4*c)/5,0])
gaps=[S.expand(x-v) for x in (eta.T*mat)]
require(gaps==[(1-2*c)/5,0,(1+3*c)/5,(1+8*c)/5,0,c],'dual and uniqueness gaps')
lf=[z.subs({t:S.Rational(2,9),s:S.Rational(4,27),c:S.Rational(1,10)}) for z in f]
require(min(lf)==S.Rational(1,3) and lf.count(min(lf))==1,'C4 least favorable unique skip1')
# Uniform-seed limitation is exact integrality, not inability to code rationals.
for den in [7,11,101]:
 x=Q(1,4)+Q(1,1000*den)
 y=(12*x*x-4*x+Q(4,9)-6*x*x+5*x-Q(2,3))/2
 require(Q(2,9)<x<Q(5,18),'rational unbounded-data fixtures')
 require((3*x*6).denominator!=1,'fixed D=6 cannot realize posterior')
# Unbounded Nat tuple (numerator,denominator) recovers each rational exactly.
for x in [Q(7,36),Q(5,24),Q(1234567,98765431)]:
 require(Q(x.numerator,x.denominator)==x,'unbounded rational code')
mutation=sys.argv[1] if len(sys.argv)>1 else ''
if mutation=='posterior_only': require(f[4].subs(s,ss[0])==f[4].subs(s,ss[-1]),'REJECT posterior sufficiency')
if mutation=='rank_on_curve': require(S.Matrix(curve).jacobian([t]).rank()==2,'REJECT domain-free dimension bound')
if mutation=='fixed_seed_all_rationals': require((6*Q(1,7)).denominator==1,'REJECT fixed seed all rationals')
print(json.dumps({'status':'PASS','checks':n,'scope':'symbolic identities and finite controls; topology/cardinality require written proof'}))
