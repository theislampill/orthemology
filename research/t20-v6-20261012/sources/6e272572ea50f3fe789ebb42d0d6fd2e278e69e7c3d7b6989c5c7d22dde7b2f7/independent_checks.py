#!/usr/bin/env python3
"""Independent exact review controls; does not import either author's checker."""
from collections import deque
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import sympy as sp

ROOT = Path(__file__).resolve().parent
ONE = sp.Integer(1)

def all_words(alphabet_size, horizon):
    for length in range(horizon + 1):
        yield from product(range(alphabet_size), repeat=length)

def evolved(matrices, word, state):
    for symbol in word:
        state = matrices[symbol] * state
    return state

def output(C, state):
    mass = sum(state)
    return None if mass == 0 else tuple(C * state / mass)

def tensor_basis(C, matrices):
    n = C.cols
    unit = sp.ones(1, n)
    generators = [sp.kronecker_product(C.row(i), unit) -
                  sp.kronecker_product(unit, C.row(i)) for i in range(C.rows)]
    lifts = [sp.kronecker_product(M, M) for M in matrices]
    basis = sp.Matrix.vstack(*generators).rowspace()
    dimensions = [len(basis)]
    while basis:
        proposed = sp.Matrix.vstack(*basis, *(v * T for v in basis for T in lifts)).rowspace()
        if len(proposed) == len(basis):
            break
        basis = proposed
        dimensions.append(len(basis))
    assert len(basis) <= n * (n - 1) // 2
    for v in basis:
        assert all(v[i*n+j] == -v[j*n+i] for i in range(n) for j in range(n))
    return basis, dimensions

def tensor_pass(basis, r, s):
    pair = sp.kronecker_product(r, s)
    return all((v * pair)[0] == 0 for v in basis)

def boolean_product(A, B):
    n = len(A)
    return tuple(tuple(any(A[i][k] and B[k][j] for k in range(n))
                       for j in range(n)) for i in range(n))

def boolean_semigroup(matrices):
    """Independent oracle: enumerate support relations, not pairs of belief supports."""
    n = matrices[0].rows
    generators = [tuple(tuple(M[i,j] > 0 for j in range(n)) for i in range(n))
                  for M in matrices]
    identity = tuple(tuple(i == j for j in range(n)) for i in range(n))
    found = {identity: ()}
    queue = deque([identity])
    while queue:
        relation = queue.popleft()
        for symbol, generator in enumerate(generators):
            successor = boolean_product(generator, relation)
            if successor not in found:
                found[successor] = found[relation] + (symbol,)
                queue.append(successor)
    return found

def same_feasibility(relations, r, s):
    n = len(r)
    for relation, word in relations.items():
        live_r = any(relation[i][j] and r[j] > 0 for i in range(n) for j in range(n))
        live_s = any(relation[i][j] and s[j] > 0 for i in range(n) for j in range(n))
        if live_r != live_s:
            return False, word
    return True, None

results = {}

# The two-observation family is jointly column stochastic and the target nontrivial.
C3 = sp.Matrix([[1,1,0],[0,0,1]])
selectors = [sp.diag(1,0,1), sp.diag(0,1,0)]
r = sp.Matrix([1,0,0])
s = sp.Matrix([0,1,0])
basis, dimensions = tensor_basis(C3, selectors)
assert tensor_pass(basis, r, s)
guard, witness = same_feasibility(boolean_semigroup(selectors), r, s)
assert not guard and witness == (0,)
assert output(C3, evolved(selectors, witness, r)) == (1,0)
assert output(C3, evolved(selectors, witness, s)) is None
results['missing_feasibility_false_positive'] = {
    'tensor_passes': True, 'feasibility_passes': False,
    'shortest_witness': witness, 'tensor_dimensions': dimensions}

# Explicit noncommuting convention control: chronological (0,1) applies M1 M0.
M0 = sp.Matrix([[0,1,0],[1,0,0],[0,0,1]]) / 2
M1 = sp.Matrix([[1,0,0],[0,0,1],[0,1,0]]) / 2
assert M1*M0 != M0*M1
state = sp.Matrix([sp.Rational(1,2),sp.Rational(1,3),sp.Rational(1,6)])
assert evolved([M0,M1], (0,1), state) == M1*M0*state
assert evolved([M0,M1], (0,1), state) != M0*M1*state
unit = sp.ones(1,3)
O = sp.kronecker_product(C3.row(1),unit)-sp.kronecker_product(unit,C3.row(1))
pair = sp.kronecker_product(r, state)
correct = (O*sp.kronecker_product(M1,M1)*sp.kronecker_product(M0,M0)*pair)[0]
rr, ss = evolved([M0,M1], (0,1), r), evolved([M0,M1], (0,1), state)
assert correct == (C3.row(1)*rr)[0]*sum(ss)-sum(rr)*(C3.row(1)*ss)[0]
results['chronological_noncommuting_control'] = 'PASS'

# Random rational instruments. The oracle enumerates every chronological word
# through the universal antisymmetric dimension bound, independently of span closure.
rng = random.Random(107031)
model_count = pair_count = word_count = identity_count = 0
for n in (2,3,4):
    for trial in range(8):
        raw = [[[rng.randrange(3) for _ in range(n)] for _ in range(n)] for _ in range(2)]
        denominators = [sum(raw[a][i][j] for a in range(2) for i in range(n)) for j in range(n)]
        for j in range(n):
            if denominators[j] == 0:
                raw[0][0][j] = denominators[j] = 1
        matrices = [sp.Matrix(n,n,lambda i,j: sp.Rational(raw[a][i][j],denominators[j])) for a in range(2)]
        C = sp.Matrix([[int(i == n-1) for i in range(n)], [int(i != n-1) for i in range(n)]])
        B, _ = tensor_basis(C, matrices)
        relations = boolean_semigroup(matrices)
        states = []
        for _ in range(4):
            weights = [rng.randrange(4) for _ in range(n)]
            if not sum(weights): weights[0] = 1
            states.append(sp.Matrix([sp.Rational(x,sum(weights)) for x in weights]))
        states.append(sp.ones(n,1)/n)
        # Include a full-support pair with matching present target but different hidden nuisance.
        if n > 2:
            p = sp.ones(n,1)/n
            p[0] += sp.Rational(1,2*n)
            p[1] -= sp.Rational(1,2*n)
            states.append(p)
        horizon = n*(n-1)//2
        words = list(all_words(2,horizon))
        evolutions = [[evolved(matrices,w,p) for w in words] for p in states]
        outs = [[output(C,p) for p in paths] for paths in evolutions]
        for i,j in product(range(len(states)),repeat=2):
            x,y = states[i],states[j]
            feasible, _ = same_feasibility(relations,x,y)
            lifted = tensor_pass(B,x,y)
            direct_cross = all((C*xx)*sum(yy)==(C*yy)*sum(xx)
                               for xx,yy in zip(evolutions[i],evolutions[j]))
            assert lifted == direct_cross
            # Direct output equality plus separately certified full support-language equality.
            assert (feasible and lifted) == (feasible and outs[i] == outs[j])
            if {k for k,v in enumerate(x) if v>0} == {k for k,v in enumerate(y) if v>0}:
                assert feasible
                for xx,yy in zip(evolutions[i],evolutions[j]):
                    assert {k for k,v in enumerate(xx) if v>0} == {k for k,v in enumerate(yy) if v>0}
            pair_count += 1
            word_count += len(words)
        for paths in evolutions:
            for w, xx in zip(words, paths):
                product_matrix = sp.eye(n)
                for a in w: product_matrix = matrices[a]*product_matrix
                assert xx == product_matrix*states[evolutions.index(paths)]
                identity_count += 1
        model_count += 1
results['generic_exact_controls'] = {'models':model_count,'pairs':pair_count,
    'pair_word_comparisons':word_count,'chronological_identities':identity_count}

# Complete bounded grid includes zero cells but requires both audit outcomes live.
states = {tuple(Q(x,sum(xs)) for x in xs) for xs in product(range(4),repeat=4)
          if xs[0]+xs[2]>0 and xs[1]+xs[3]>0}
def signature(p):
    return p[2]+p[3], p[2]/(p[0]+p[2]), p[3]/(p[1]+p[3])
signatures = {}
dependent = independent = 0
for p in states:
    q,q0,q1 = signature(p)
    signatures.setdefault((q,q0,q1),[]).append(p)
    if q0 != q1:
        t = (q-q0)/(q1-q0)
        assert ((1-t)*(1-q0),t*(1-q1),(1-t)*q0,t*q1) == p
        dependent += 1
    else:
        assert q == q0 == q1
        assert p[0]*p[3] == p[1]*p[2]
        independent += 1
for sig, group in signatures.items():
    q,q0,q1 = sig
    assert q0 == q1 or len(group) == 1
for p,r in product(states,repeat=2):
    ps,rs = signature(p),signature(r)
    assert (ps==rs) == (p==r or (ps[1]==ps[2] and rs[1]==rs[2] and ps[0]==rs[0]))
results['binary_audit_boundary_grid'] = {'joint_laws':len(states),'pair_checks':len(states)**2,
    'dependent_laws':dependent,'independent_laws':independent,'zero_cells_included':True}

results['status'] = 'PASS'
results['review_script_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
destination = ROOT/'INDEPENDENT_RESULTS.json'
destination.write_text(json.dumps(results,indent=2)+'\n')
print(destination.read_text())
