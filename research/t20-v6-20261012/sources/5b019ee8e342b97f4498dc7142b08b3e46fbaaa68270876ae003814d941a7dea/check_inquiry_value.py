#!/usr/bin/env python3
"""Exact independent controls for posterior-only state versus inquiry value."""
from fractions import Fraction as F
from itertools import product
from pathlib import Path
import hashlib,json,random
import sympy as s

ROOT=Path(__file__).resolve().parent
Q=s.Matrix([[1,s.Rational(1,2),0],[0,s.Rational(1,2),1]])
def half_brier_risk(p):
    return (1-sum(x*x for x in p))/2
def posterior(joint,word):
    if not word:
        return tuple(joint*s.ones(joint.cols,1))
    if any(d!=word[0] for d in word):return None
    col=joint[:,word[0]]
    z=sum(col)
    return None if z==0 else tuple(col/z)

as_=[s.Rational(1,4),s.Rational(1,8)]
laws=[];values=[]
h=s.Matrix([half_brier_risk(Q[:,i]) for i in range(Q.cols)])
assert tuple(h)==(0,s.Rational(1,4),0)
for a in as_:
    t=s.Matrix([a,1-2*a,a])
    law=Q*s.diag(*t)
    assert tuple(Q*t)==(s.Rational(1,2),)*2
    assert all(x>0 for x in t)
    expected=(h.T*t)[0]
    gain=half_brier_risk(Q*t)-expected
    assert gain==a/2
    laws.append(law)
    values.append((a,expected,gain,gain-s.Rational(3,32)))
word_count=0
for length in range(8):
    for word in product(range(3),repeat=length):
        assert posterior(laws[0],word)==posterior(laws[1],word)
        word_count+=1
assert values[0][3]==s.Rational(1,32) and values[1][3]==-s.Rational(1,32)
assert Q.rank()==2 and Q.col_join(h.T).rank()==3
kernel=Q.nullspace()
assert len(kernel)==1 and Q*kernel[0]==s.zeros(2,1)
assert (h.T*kernel[0])[0]!=0

# Strictly positive-cell ternary control.
Qinterior=s.Matrix([[s.Rational(3,4),s.Rational(1,2),s.Rational(1,4)],
                    [s.Rational(1,4),s.Rational(1,2),s.Rational(3,4)]])
interior_values=[]
for a in as_:
    t=s.Matrix([a,1-2*a,a]);law=Qinterior*s.diag(*t)
    assert all(x>0 for x in law)
    gain=half_brier_risk(Qinterior*t)-sum(t[i]*half_brier_risk(Qinterior[:,i]) for i in range(3))
    assert gain==a/8
    interior_values.append((a,gain,gain-s.Rational(3,128)))
assert interior_values[0][2]==s.Rational(1,128)
assert interior_values[1][2]==-s.Rational(1,128)

# Binary fixed-audit theorem: complete bounded grid, including zero marginals.
# Compare arbitrary finite functions of the posterior as well as Brier risk.
binary_laws={tuple(F(x,sum(v)) for x in v) for v in product(range(4),repeat=4) if sum(v)>0}
groups={}
for cells in binary_laws:
    # Cell order: (theta0,D0),(theta0,D1),(theta1,D0),(theta1,D1).
    masses=(cells[0]+cells[2],cells[1]+cells[3])
    qs=tuple(None if masses[d]==0 else cells[2+d]/masses[d] for d in range(2))
    sig=(cells[2]+cells[3],)+qs
    expectations=[]
    for fun in (lambda p:p*(1-p),lambda p:p*p+p**7,lambda p:F(int(p>F(2,5)))):
        expectations.append(sum(masses[d]*fun(qs[d]) for d in range(2) if masses[d]))
    groups.setdefault(sig,[]).append((cells,tuple(expectations)))
binary_collisions=0
for sig,group in groups.items():
    assert len({e for cells,e in group})==1
    if len(group)>1:
        assert sig[0]==sig[1]==sig[2]
        binary_collisions+=len(group)*(len(group)-1)
# An outcome-dependent cost distinguishes independence fibers, as excluded.
assert F(1,4)!=F(3,4)

# Generic exact null-direction witnesses test both directions of the row-span rule.
rng=random.Random(10432026)
cases=witnesses=constant_controls=0
for m in (2,3):
    for k in (2,3,4,5):
        for _ in range(8):
            columns=[]
            for j in range(k):
                raw=[rng.randrange(5) for _ in range(m)]
                if not sum(raw):raw[0]=1
                columns.append(s.Matrix([s.Rational(x,sum(raw)) for x in raw]))
            A=s.Matrix.hstack(*columns)
            raw=[rng.randrange(1,5) for _ in range(k)]
            t0=s.Matrix([s.Rational(x,sum(raw)) for x in raw]);q=A*t0
            bayes=s.Matrix([half_brier_risk(A[:,i]) for i in range(k)])
            null=A.nullspace()
            row_member=A.col_join(bayes.T).rank()==A.rank()
            assert row_member==all((bayes.T*v)[0]==0 for v in null)
            for v in null:
                eps=min(t0[i]/(2*abs(v[i])) for i in range(k) if v[i]!=0)
                lo,hi=t0-eps*v,t0+eps*v
                assert all(x>0 for x in lo) and all(x>0 for x in hi)
                assert A*lo==A*hi==q and sum(lo)==sum(hi)==1
                delta=(bayes.T*(hi-lo))[0]
                assert delta==2*eps*(bayes.T*v)[0]
                if delta!=0:witnesses+=1
                lam=s.Matrix([[s.Rational(i+1,m+1) for i in range(m)]])
                affine=lam*A
                assert (affine*lo)[0]==(affine*hi)[0]==(lam*q)[0]
                constant_controls+=1
            cases+=1

# Boundary caveat with the same proper loss, not an arbitrary impossible h.
boundary=s.Matrix([0,0,1])
assert Q*boundary==s.Matrix([0,1])
# Nonnegative t with target probability one forces t0=t1=0, hence this singleton.
assert all(Q[0,i]>0 for i in (0,1)) and Q[0,2]==0
assert (h.T*boundary)[0]==0
assert Q.col_join(h.T).rank()>Q.rank()

# Symbolic symmetric family and finite-risk generalization.
a,H0,Hmid,H1=s.symbols('a H0 Hmid H1')
gain=s.expand(Hmid-(a*H0+(1-2*a)*Hmid+a*H1))
assert s.expand(gain-a*(2*Hmid-H0-H1))==0

def enc(v):
    if isinstance(v,(tuple,list)):return [enc(x) for x in v]
    if isinstance(v,dict):return {k:enc(x) for k,x in v.items()}
    if isinstance(v,s.Basic):return str(v)
    return v
results={'status':'PASS','ternary_half_brier_rows':values,
 'interior_ternary_rows':interior_values,
 'identical_status_and_posterior_words_through_length_7':word_count,
 'posterior_matrix_rank':2,'rank_with_risk_row':3,
 'exact_rational_models':cases,'nonconstant_positive_fiber_witnesses':witnesses,
 'row_span_constant_direction_controls':constant_controls,
 'boundary_counterexample_to_unqualified_iff':True,
 'binary_laws_including_zero_marginals':len(binary_laws),
 'binary_posterior_classes':len(groups),
 'binary_distinct_equivalent_ordered_pairs':binary_collisions,
 'binary_expectation_test_functions':3,
 'general_symmetric_gain':str(gain),
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
out=json.dumps(enc(results),indent=2)+'\n'
(ROOT/'RESULTS.json').write_text(out)
print(out)
