#!/usr/bin/env python3
"""Bounded exact review controls, not an implemented analytic separator search."""
from collections import defaultdict
from datetime import datetime, timezone
from fractions import Fraction as Q
from itertools import product
from math import comb, factorial, ceil
from pathlib import Path
import hashlib
import json
import runpy
import sys
import sympy as S

ROOT = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
checks = []
def check(label, passed):
    if not passed:
        raise AssertionError(label)
    checks.append(label)

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

bindings = json.loads((ROOT/'valid-initial-escape-effectivity-20261010/INPUT_BINDINGS.json').read_text())
for item in bindings['files']:
    check('effectivity input hash: '+item['path'], digest(ROOT/item['path']) == item['sha256'])
frozen = ROOT/'valid-initial-partial-escape-20261010'
for item in json.loads((frozen/'FROZEN_MANIFEST.json').read_text())['files']:
    check('main frozen hash: '+item['path'], digest(frozen/item['path']) == item['sha256'])
check('frozen Schur copy equals actual source',
      (frozen/'inputs/countermodel.py').read_bytes() ==
      (ROOT/'full-polynomial-moment-countermodel-20261010/countermodel.py').read_bytes())

source = runpy.run_path(str(ROOT/'full-polynomial-moment-countermodel-20261010/countermodel.py'), run_name='review_readonly')
model = source['SchurMoment']().extend(15)
G = model.gram(15)
for i,j in product(range(15), repeat=2):
    check(f'exact inherited Schur inverse {i},{j}',
          sum(G[i][k]*model.B[k][j] for k in range(15)) == int(i == j))
for i,j in product(range(15), repeat=2):
    check(f'dyadic inverse entry {i},{j}',
          model.B[i][j].denominator & (model.B[i][j].denominator-1) == 0)
check('inherited witness value', model.apply(source['WITNESS']) == -1)

def idx(n):
    return [(a,n-a) for a in range(n+1)]
def moment(mu,a):
    return sum((w * x**a[0] * y**a[1] for (x,y),w in mu.items()), Q(0))
def add(mu, other, scale=Q(1)):
    for p,w in other.items():
        mu[p] += scale*w
        if mu[p] == 0:
            del mu[p]
def fd(alpha,R):
    # Repeated forward differences, independent of the inherited closed formula.
    mu = defaultdict(Q, {(0,0): Q(1)})
    for axis,times in enumerate(alpha):
        for _ in range(times):
            out = defaultdict(Q)
            for p,w in mu.items():
                shifted = list(p)
                shifted[axis] += R
                out[tuple(shifted)] += w
                out[p] -= w
            mu = out
    norm = factorial(alpha[0])*factorial(alpha[1])*R**sum(alpha)
    return {p:w/norm for p,w in mu.items() if w}
def apply(mu,p):
    return sum((c*moment(mu,a) for a,c in p.items()), Q(0))

rho = defaultdict(Q, {(0,0):Q(1)})
N = defaultdict(Q)
prefixes = {0:dict(N)}
blocks = {}
block_meta = []
last = 0
for n in range(1,9):
    residuals = {a:model.moment(*a)-moment(rho,a) for a in idx(n)}
    B = sum((abs(v)*Q(2**n, factorial(a[0])*factorial(a[1]))
             for a,v in residuals.items()), Q(0))
    R = max(1,last+1,ceil(2**n*n**(n-1)*B))
    block = defaultdict(Q)
    for a,v in residuals.items():
        add(block,fd(a,R),v)
    blocks[n] = dict(block)
    negative = {p:-w for p,w in block.items() if w<0}
    variation = sum(abs(w) for w in block.values())
    check(f'block {n} zero mass', sum(block.values()) == 0)
    check(f'block {n} half-variation negative mass', sum(negative.values()) == variation/2)
    for d in range(n):
        majorant = sum(abs(w)*(abs(p[0])+abs(p[1]))**d for p,w in block.items())
        check(f'block {n} radial majorant degree {d}',majorant <= Q(1,2**n))
    add(rho,block)
    add(N,negative)
    prefixes[n] = dict(N)
    for d in range(n+1):
        for a in idx(d):
            check(f'corrected Lambda moment after block {n}, {a}',moment(rho,a)==model.moment(*a))
    block_meta.append({'degree':n,'radius_bits':R.bit_length(),'atoms':len(block)})
    last = R

polynomials = [
    {(0,0):Q(1)},
    {(0,0):Q(-3,2),(1,0):Q(2,3),(0,2):Q(-5,7)},
    {(0,0):Q(1),(4,2):Q(1),(2,4):Q(1),(2,2):Q(-1)},
]
for pindex,p in enumerate(polynomials):
    D = max(map(sum,p))
    Bp = sum(map(abs,p.values()))
    for M in range(max(1,D),8):
        partial_tail = apply(prefixes[8],p)-apply(prefixes[M],p)
        finite_bound = Bp*sum((Q(1,2**n) for n in range(M+1,9)),Q(0))
        check(f'polynomial {pindex} finite hidden tail at {M}',abs(partial_tail)<=finite_bound)
        check(f'polynomial {pindex} geometric total tail at {M}', finite_bound < Bp*Q(1,2**M))
F = source['WITNESS']
for M in range(6,8):
    delta = apply(prefixes[8],F)-apply(prefixes[M],F)
    check(f'F increasing prefixes at {M}',delta >= 0)
    check(f'F coefficient-sum tail at {M}',delta <= 4*Q(1,2**M))
for M in range(1,8):
    delta = moment(prefixes[8],(0,0))-moment(prefixes[M],(0,0))
    finite_bound = sum((Q(1,2**(n+1)) for n in range(M+1,9)),Q(0))
    check(f'sharper negative-mass tail {M}',0<=delta<=finite_bound<Q(1,2**(M+1)))

# Exact exponent algebra supporting the analytic bounds, not numerical quadrature.
x,m,R,t,j = S.symbols('x m R t j',real=True)
check('continuous Gaussian square completion',
      S.expand(m*x-x*x/2-m*m/2+(x-m)**2/2)==0)
check('discrete Gaussian square completion',
      S.expand(m*j-j*j/2-m*m/2+(j-m)**2/2)==0)
f = S.exp(m*x-t*S.exp(2*x)-x*x/2)/S.sqrt(2*S.pi)
check('continuous derivative identity',S.simplify(S.diff(f,x)/f-(m-2*t*S.exp(2*x)-x))==0)
for mm in range(17):
    for jj in range(-160,161):
        if abs(jj)>=max(1,4*mm):
            check(f'discrete exponent domination m={mm}, j={jj}',
                  -Q(jj*jj,2)+mm*jj <= -Q(jj*jj,4))
for J in range(41):
    for n in range(41):
        check(f'discrete geometric exponent increment J={J}, n={n}',
              (J+1+n)**2 >= (J+1)**2+n*(2*J+3))
for M in range(20):
    for K in range(M+1,M+20):
        s = sum((Q(1,2**n) for n in range(M+1,K+1)),Q(0))
        check(f'exact geometric hidden tail M={M}, K={K}',s==Q(1,2**M)-Q(1,2**K))

C,lam,Nv,I,J,n0,B = S.symbols('C lam Nv I J n0 B',nonzero=True)
check('normalization cancellation', S.cancel(((lam*I+Nv*J)/C)/((I+n0*J)/C)-(lam*I+Nv*J)/(I+n0*J))==0)
check('separator normalization sign expression',S.cancel(((-I+B*J)/C)/((S.Symbol('I0')+n0*S.Symbol('J0'))/C)-(-I+B*J)/(S.Symbol('I0')+n0*S.Symbol('J0')))==0)

# An upper-negative numerator and a positive denominator interval give a
# directly checkable upper-negative normalized interval.
for wlo,whi,dlo,dhi in [(-7,-3,Q(1,17),Q(9,4)),(-1,Q(-1,128),Q(1,4096),2)]:
    wlo,whi,dlo,dhi = map(Q,(wlo,whi,dlo,dhi))
    outlo,outhi = wlo/dlo, whi/dhi
    check('negative quotient interval endpoint sign',outlo<=outhi<0)
    for numerator in [wlo,(wlo+whi)/2,whi]:
        for denominator in [dlo,(dlo+dhi)/2,dhi]:
            check('negative quotient interval containment',outlo<=numerator/denominator<=outhi)

# Scheduler control only. These rational toy values are NOT path evaluations.
toy_values = [Q(0),Q(1),Q(-1,1024),Q(-1,16)]
accepted = None
for stage in range(1,20):
    for k in range(min(stage,len(toy_values))):
        error=Q(1,2**stage)
        upper=toy_values[k]+error
        if upper<0:
            accepted=(stage,k,upper)
            break
    if accepted:
        break
check('dovetail bypasses exact-zero candidate', accepted is not None and accepted[1]>0)
check('dovetail requires strict upper-negative endpoint',accepted[2]<0)
check('zero candidate never falsely accepted',all(toy_values[0]+Q(1,2**s)>0 for s in range(1,20)))

result = {
    'status':'PASS',
    'timestamp_utc':datetime.now(timezone.utc).isoformat(),
    'check_count':len(checks),
    'scope':'Bounded exact algorithm/tail-algebra controls; no active numerical integration, separator search, witness q, or kernel proof.',
    'reviewed_addendum_hash_at_run':digest(ROOT/'valid-initial-escape-effectivity-20261010/RESULT.md'),
    'main_proof_hash':digest(frozen/'RESULT.md'),
    'signed_block_prefix':block_meta,
    'toy_scheduler_acceptance':{'stage':accepted[0],'candidate':accepted[1],'upper':str(accepted[2])},
    'checks':checks,
}
(HERE/'EXACT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
