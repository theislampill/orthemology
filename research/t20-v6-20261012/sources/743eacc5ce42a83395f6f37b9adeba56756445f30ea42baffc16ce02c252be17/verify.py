#!/usr/bin/env python3
"""Exact finite controls, not a proof of the universal claims."""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import json
import sympy as s

ROOT = Path(__file__).resolve().parent
checks = []
def record(name, detail):
    checks.append({'name': name, 'status': 'PASS', 'detail': detail})
def bayes(p, L):
    z = sum(a*b for a,b in zip(p,L))
    if z == 0:
        raise ValueError('undefined conditioning: zero evidence mass')
    return tuple(a*b/z for a,b in zip(p,L))
def had(a,b): return tuple(x*y for x,y in zip(a,b))
def block_project(p, blocks, weights):
    out = [F(0)]*len(p)
    for block,w in zip(blocks,weights):
        z=sum(p[i] for i in block)
        assert z>0
        for i in block: out[i]=w*p[i]/z
    return tuple(out)
def half_brier_div(p,q): return sum((a-b)**2 for a,b in zip(p,q))/2
def entropy_brier(p): return (1-sum(x*x for x in p))/2

def exact_vertices(H):
    n=H.cols
    E=s.ones(1,n).col_join(H)
    target=s.Matrix([1]+[0]*H.rows)
    vertices=set()
    for k in range(1,min(n,E.rank())+1):
        for I in combinations(range(n),k):
            EI=E[:,list(I)]
            if EI.rank()!=k or EI.row_join(target).rank()!=k: continue
            sol=tuple(EI.gauss_jordan_solve(target)[0])
            if any(x<0 for x in sol): continue
            p=[s.S(0)]*n
            for i,x in zip(I,sol): p[i]=x
            vertices.add(tuple(p))
    return sorted(vertices)
def rank_accept(H,L,S):
    HS=H[:,S]; D=s.diag(*[L[i] for i in S])
    return HS.col_join(HS*D).rank()==HS.rank()
def graph_accept(H,L,S):
    HS=H[:,S]; R,piv=HS.rref(); free=[j for j in range(len(S)) if j not in piv]
    return all(R[r,j]==0 or L[S[j]]==L[S[p]] for r,p in enumerate(piv) for j in free)

# Full support-orbit witness, including lower-dimensional support.
p=(F(1,4),F(0),F(3,4),F(0)); q=(F(2,5),F(0),F(3,5),F(0))
L=tuple(qi/pi if pi else F(1) for pi,qi in zip(p,q))
assert bayes(p,L)==q
assert bayes(bayes(p,L),tuple(1/x for x in L))==p
record('positive orbit and inverse',{'p':str(p),'q':str(q),'L':str(L)})

# Enumerate every nonempty support family on 4 labels.
n=4; supports=range(1,1<<n); both=[]; family_count=0
for bits in range(1,1<<len(supports)):
    family={m for m in supports if bits & (1<<(m-1))}; family_count+=1
    down=all(t in family for m in family for t in supports if t&m==t)
    union=all((a|b) in family for a in family for b in family)
    principal=any(family=={t for t in supports if t&m==t} for m in supports)
    assert (down and union)==principal
    if down and union: both.append(sorted(family))
assert len(both)==15
record('support-family face classification',{'nonempty_families':family_count,'closed_convex_invariant_families':len(both)})

# Exact affine tests: vertices independently certify every finite instance.
matrices=[s.Matrix([row]) for row in product((-1,0,1),repeat=3)]
matrices += [s.Matrix([[1,-1,0],[0,1,-1]]),s.Matrix([[0,1,1],[0,2,2]]),s.zeros(0,3)]
instances=accepted=0; feasible_families=0
for H in matrices:
    vertices=exact_vertices(H)
    if not vertices: continue
    feasible_families+=1
    S=[i for i in range(H.cols) if any(p[i]>0 for p in vertices)]
    positive=s.Matrix([sum(p[i] for p in vertices)/len(vertices) for i in S])
    assert all(x>0 for x in positive) and H[:,S]*positive==s.zeros(H.rows,1)
    for L in product((s.S(1),s.S(2),s.S(3)),repeat=H.cols):
        vertex_accept=all(H*s.Matrix(bayes(p,L))==s.zeros(H.rows,1) for p in vertices)
        assert vertex_accept==rank_accept(H,L,S)==graph_accept(H,L,S)
        if vertex_accept:
            inverse=tuple(1/x for x in L)
            assert all(H*s.Matrix(bayes(p,inverse))==s.zeros(H.rows,1) for p in vertices)
            accepted+=1
        instances+=1
record('affine rank, RREF graph, vertex and inverse agreement',{'feasible_families':feasible_families,'likelihood_instances':instances,'accepted':accepted})

# Omitting actual support is a false negative.
H=s.Matrix([[0,1,1]]); L=(1,2,3)
assert exact_vertices(H)==[(s.S(1),s.S(0),s.S(0))]
assert rank_accept(H,L,[0]) and not rank_accept(H,L,[0,1,2])
record('actual-support omission control','C={e1}: all positive L preserve it; unrestricted kernel test incorrectly rejects (1,2,3).')

# Positive model: p1=p2, observations distinguish its shared block from state 3.
H=s.Matrix([[1,-1,0]]); p=(F(1,4),F(1,4),F(1,2))
Lp=(F(3,4),F(3,4),F(1,4)); Lm=tuple(1-x for x in Lp)
assert rank_accept(H,Lp,[0,1,2]) and rank_accept(H,Lm,[0,1,2])
assert bayes(p,Lp)==(F(3,8),F(3,8),F(1,4))
assert bayes(p,Lm)==(F(1,8),F(1,8),F(3,4))
assert bayes(bayes(p,Lp),Lp)==(F(9,20),F(9,20),F(1,10))
record('informative invariant affine model',{'plus':str(bayes(p,Lp)),'minus':str(bayes(p,Lm)),'plus_plus':str(bayes(bayes(p,Lp),Lp))})

# Symbolic projected update composition on two blocks.
p=s.symbols('p0:4',positive=True); L=s.symbols('l0:4',positive=True); M=s.symbols('m0:4',positive=True)
w=s.symbols('w',positive=True); blocks=((0,1),(2,3)); weights=(w,1-w)
def symbolic_U(p,L):
    out=[0]*4
    for I,wt in zip(blocks,weights):
        z=sum(p[i]*L[i] for i in I)
        for i in I: out[i]=wt*p[i]*L[i]/z
    return out
left=symbolic_U(symbolic_U(p,M),L); right=symbolic_U(p,had(L,M))
assert all(s.cancel(a-b)==0 for a,b in zip(left,right))
c=s.symbols('c',positive=True)
assert all(s.cancel(a-b)==0 for a,b in zip(symbolic_U(p,tuple(c*x for x in L)),symbolic_U(p,L)))
record('symbolic block update composition and scalar neutrality','Identities hold on positive inputs; fixed weights require 0<w<1.')

# Legitimate positive binary channel where block-KL repair erases all evidence.
p=(F(1,2),F(1,4),F(1,4)); blocks=((0,),(1,2)); weights=(F(1,2),F(1,2))
Lp=(F(3,4),F(1,4),F(1,4)); Lm=tuple(1-x for x in Lp)
Qp=bayes(p,Lp); Qm=bayes(p,Lm)
assert Qp==(F(3,4),F(1,8),F(1,8)) and Qm==(F(1,4),F(3,8),F(3,8))
assert block_project(Qp,blocks,weights)==p==block_project(Qm,blocks,weights)
assert sum(pi*li for pi,li in zip(p,Lp))==F(1,2)==sum(pi*li for pi,li in zip(p,Lm))
assert half_brier_div(Qp,p)==F(3,64)==half_brier_div(Qm,p)
assert entropy_brier(p)==F(5,16)
assert (entropy_brier(Qp)+entropy_brier(Qm))/2==F(17,64)
assert entropy_brier(p)-(entropy_brier(Qp)+entropy_brier(Qm))/2==F(3,64)
Qpp=bayes(Qp,Lp)
assert Qpp==(F(9,10),F(1,20),F(1,20))
assert block_project(bayes(block_project(Qp,blocks,weights),Lp),blocks,weights)==p
H=s.Matrix([[F(1,2),-F(1,2),-F(1,2)]])
assert not rank_accept(H,Lp,[0,1,2])
record('positive-channel block projection information erasure',{'prior':str(p),'plus':str(Qp),'minus':str(Qm),'plus_plus':str(Qpp),'expected_half_Brier_regret':'3/64','true_expected_posterior_risk':'17/64','constrained_expected_risk':'5/16'})

# A specified likelihood can preserve one prior but not the entire family.
p4=(F(1,4),)*4; L4=(F(1),F(3),F(2),F(2))
assert sum(bayes(p4,L4)[:2])==F(1,2)
p4b=(F(1,8),F(3,8),F(1,4),F(1,4))
assert sum(bayes(p4b,L4)[:2])!=F(1,2)
record('single-prior versus family quantifier','Same L preserves block masses at one prior and fails at another.')

# Both outcomes preserve the actual current state but not all future feasible states.
p=(F(1,2),F(1,4),F(1,4)); Lp=(F(1,2),F(1,4),F(3,4)); Lm=tuple(1-x for x in Lp)
H=s.Matrix([[F(1,2),-F(1,2),-F(1,2)]])
Qp=bayes(p,Lp); Qm=bayes(p,Lm)
assert Qp==(F(1,2),F(1,8),F(3,8)) and Qm==(F(1,2),F(3,8),F(1,8))
assert not rank_accept(H,Lp,[0,1,2]) and not rank_accept(H,Lm,[0,1,2])
assert bayes(Qp,Lp)==(F(4,9),F(1,18),F(1,2))
record('legitimate current-state-only positive channel',{'plus':str(Qp),'minus':str(Qm),'second_plus_leaves_C':str(bayes(Qp,Lp))})

# Closure / convexity and nonnegative-likelihood boundaries.
assert bayes((F(1,2),F(1,2)),(F(1),F(0)))==(F(1),F(0))
try:
    bayes((F(1),F(0)),(F(0),F(1)))
    raise AssertionError('zero denominator should fail')
except ValueError:
    pass
# Affine inclusion need not be equality after a singular update.
assert bayes((F(1,2),F(1,2)),(F(1),F(0)))==(F(1),F(0))
# Closed convex inequality family can have strict forward inclusion for positive L.
assert bayes((F(1,2),F(1,2)),(F(2),F(1)))==(F(2,3),F(1,3))
record('zero-likelihood and inequality boundaries','Support may shrink; zero mass is undefined; positive forward invariance of p1>=1/2 need not be equality.')

result={'status':'PASS','method':'Exact rational, symbolic, and finite exhaustive controls. Not formal-kernel certification.','control_groups':len(checks),'checks':checks}
(ROOT/'CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
