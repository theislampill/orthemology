#!/usr/bin/env python3
"""Small exact symbolic/rational controls; not an analytic/topological proof."""
from pathlib import Path
import hashlib
import json
from math import factorial
import sympy as s

HERE = Path(__file__).resolve().parent
p = s.symbols('p1:7')
r = p[0]-1
Q = [p[0]]
for j in range(4):
    Q.append(s.expand(sum(s.diff(Q[-1],p[k-1])*k*r*(p[k]-p[k-1]) for k in range(1,j+2))))
counts = {}

def record(group):
    counts[group] = counts.get(group,0)+1

def equal(a,b,group):
    assert s.cancel(a-b) == 0, (group,a,b)
    record(group)

for j in range(1,5):
    equal(s.diff(Q[j],p[j]),factorial(j)*r**j,'triangular_leading_coefficients')
    assert not s.expand(Q[j]-factorial(j)*r**j*p[j]).has(p[j])
    record('triangular_remainders')

for n in range(1,5):
    b=s.symbols(f'b1:{n+1}')
    z=sum(b)
    F=[-(z-1)*bi*(1-bi) for bi in b]
    powers={p[k-1]:sum(bi**k for bi in b) for k in range(1,7)}
    def lie(q):
        return s.expand(sum(s.diff(q,bi)*fi for bi,fi in zip(b,F)))
    for k in range(1,5):
        equal(lie(powers[p[k-1]]),-k*(z-1)*(powers[p[k-1]]-powers[p[k]]),'moment_recurrence')
    q=z
    for j in range(n):
        equal(q,Q[j].subs(powers,simultaneous=True),'independent_lie_jets')
        q=lie(q)
    S=sum(bi*(1-bi) for bi in b)
    equal(sum(F)/S,-(z-1),'normalized_output')
    P=s.Matrix([powers[p[k]] for k in range(n)])
    vand=s.prod(b[j]-b[i] for i in range(n) for j in range(i+1,n))
    equal(P.jacobian(b).det(),factorial(n)*vand,'moment_jacobian')
    equal(s.Matrix(Q[:n]).jacobian(p[:n]).det(),s.prod(factorial(j) for j in range(n))*r**(n*(n-1)//2),'jet_moment_jacobian')
    if n<=3:
        J=s.Matrix([qj.subs(powers,simultaneous=True) for qj in Q[:n]])
        expected=s.prod(factorial(k) for k in range(1,n+1))*(z-1)**(n*(n-1)//2)*vand
        equal(J.jacobian(b).det(),expected,'direct_observability_determinant')

def moments(b):
    return [sum(x**k for x in b) for k in range(1,len(b)+1)]

def jets(b):
    ps={p[k-1]:sum(x**k for x in b) for k in range(1,7)}
    return [s.factor(q.subs(ps)) for q in Q[:len(b)]]

def recover_moments(js):
    got=[js[0]]
    for j in range(1,len(js)):
        known=dict(zip(p,got))
        remainder=Q[j].subs(p[j],0).subs(known)
        got.append(s.cancel((js[j]-remainder)/(factorial(j)*(got[0]-1)**j)))
    return got

def newton_polynomial(ps):
    es=[s.Integer(1)]
    for k in range(1,len(ps)+1):
        es.append(s.cancel(sum((-1)**(i-1)*es[k-i]*ps[i-1] for i in range(1,k+1))/k))
    X=s.Symbol('X')
    return s.expand(sum((-1)**k*es[k]*X**(len(ps)-k) for k in range(len(ps)+1)))

A=[s.Rational(1,10),s.Rational(1,2),s.Rational(3,5)]
B=[s.Rational(1,5),s.Rational(3,10),s.Rational(7,10)]
fixtures=[
    [s.Rational(2,5)],
    [s.Rational(1,5),s.Rational(2,5)],
    A,B,
    [s.Rational(1,9),s.Rational(2,9),s.Rational(5,9),s.Rational(7,9)],
]
for b in fixtures:
    got=recover_moments(jets(b))
    assert got==moments(b)
    record('rational_jet_reconstruction')
    X=s.Symbol('X')
    equal(newton_polynomial(got),s.prod(X-x for x in b),'rational_newton_reconstruction')
    assert jets(b)==jets(list(reversed(b)))
    record('permutation_control')

ja,jb=jets(A),jets(B)
assert ja[:2]==jb[:2] and ja[2]!=jb[2]
assert ja==[s.Rational(6,5),s.Rational(-29,250),s.Rational(853,12500)]
assert jb==[s.Rational(6,5),s.Rational(-29,250),s.Rational(889,12500)]
record('equal_sum_equal_S_second_jet_separator')

C=[s.Rational(1,10),s.Rational(3,10),s.Rational(3,5)]
D=[s.Rational(1,5),s.Rational(7,20),s.Rational(9,20)]
assert C!=D and sum(C)==sum(D)==1
assert jets(C)==jets(D)==[1,0,0]
assert all(-(sum(v)-1)*x*(1-x)==0 for v in [C,D] for x in v)
record('coherent_stationary_collapse')

result={
 'status':'PASS',
 'scope':'Finite exact symbolic/rational identity and counterexample controls only; analytic ODE, Newton uniqueness, arbitrary-n triangular induction, and invariance-of-domain claims rely on the written proofs.',
 'counts':counts,
 'total_assertion_groups':sum(counts.values()),
 'symbolic_jet_polynomials':[str(q) for q in Q[:4]],
 'second_jet_separator':{'a':[str(x) for x in A],'b':[str(x) for x in B], 'a_jets':[str(x) for x in ja], 'b_jets':[str(x) for x in jb], 'S':'29/50','p3_a':'171/500','p3_b':'189/500'},
 'coherent_control':{'c':[str(x) for x in C], 'd':[str(x) for x in D], 'jets':['1','0','0']},
 'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'sympy_version':s.__version__,
}
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
