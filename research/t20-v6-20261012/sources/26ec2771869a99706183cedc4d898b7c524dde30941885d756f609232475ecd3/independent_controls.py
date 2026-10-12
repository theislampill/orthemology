#!/usr/bin/env python3
"""Independent exact review: solve atom constraints, then test the channel.

Does not import or execute author code. The atom vector is recovered by exact
Gaussian elimination from the moment matrix, not the author's cell formula.
"""
from fractions import Fraction as Q
from itertools import product, combinations, permutations
from pathlib import Path
from hashlib import sha256
import json
import argparse

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--mathematics-only', action='store_true', help='Run standalone exact mathematics without upstream custody reads.')
args = parser.parse_args()

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUTHOR = ROOT / 'pairwise-corroboration-bound-20261011'
BITS = list(product((0, 1), repeat=3))
SUBSETS = [s for n in range(4) for s in combinations(range(3), n)]
checks = 0

def expect(value):
    global checks
    assert value
    checks += 1

def prod(values):
    result = Q(1)
    for value in values:
        result *= value
    return result

def rref(matrix):
    a = [[Q(v) for v in row] for row in matrix]
    row = 0
    pivots = []
    for col in range(len(a[0])):
        pivot = next((i for i in range(row, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[row], a[pivot] = a[pivot], a[row]
        divisor = a[row][col]
        a[row] = [v / divisor for v in a[row]]
        for i in range(len(a)):
            if i != row:
                factor = a[i][col]
                a[i] = [v - factor*w for v, w in zip(a[i], a[row])]
        pivots.append(col)
        row += 1
        if row == len(a):
            break
    return a, pivots

MATRIX = [[prod(c[i] for i in s) for c in BITS] for s in SUBSETS]
reduced, pivots = rref(MATRIX[:-1])
expect(len(pivots) == 7)
expect(7 not in pivots)
null = [-reduced[i][7] for i in range(7)] + [Q(1)]
expect(null == [Q((-1)**(3-sum(c))) for c in BITS])
expect(all(sum(a*b for a, b in zip(row, null)) == 0 for row in MATRIX[:-1]))

inverse_augmented, pivots = rref([row + [int(i == j) for j in range(8)] for i, row in enumerate(MATRIX)])
expect(pivots == list(range(8)))
INVERSE = [row[8:] for row in inverse_augmented]

def atoms(p, triple):
    moments = [Q(1)] + [p]*3 + [p*p]*3 + [triple]
    values = [sum(a*b for a, b in zip(row, moments)) for row in INVERSE]
    return dict(zip(BITS, values))

def joint(p, t0, t1, prior):
    result = {}
    for truth, t in ((0, t0), (1, t1)):
        for c, probability in atoms(p, t).items():
            reports = tuple(truth if bit else 1-truth for bit in c)
            result[(truth,) + reports] = probability * (prior if truth else 1-prior)
    return result

def marginal(law, indices):
    result = {}
    for state, probability in law.items():
        key = tuple(state[i] for i in indices)
        result[key] = result.get(key, Q(0)) + probability
    return result

def posterior(law):
    likelihood_mass = law[(0, 1, 1, 1)] + law[(1, 1, 1, 1)]
    if not likelihood_mass:
        return None
    return law[(1, 1, 1, 1)] / likelihood_mass

def inspect_atoms(p, t):
    law = atoms(p, t)
    expect(sum(law.values()) == 1)
    expect(min(law.values()) >= 0)
    for permutation in permutations(range(3)):
        expect(all(law[c] == law[tuple(c[i] for i in permutation)] for c in BITS))
    for size in (1, 2):
        for indices in combinations(range(3), size):
            actual = marginal(law, indices)
            for bits, probability in actual.items():
                expect(probability == prod(p if bit else 1-p for bit in bits))
    return law

ps = sorted({Q(n, d) for d in range(1, 16) for n in range(d+1)})
models = 0
for p in ps:
    lower = max(Q(0), 2*p*p-p)
    upper = min(p*p, 1-3*p+3*p*p)
    for weight in (Q(0), Q(1, 7), Q(1, 2), Q(6, 7), Q(1)):
        t = lower + weight*(upper-lower)
        atom_law = inspect_atoms(p, t)
        models += 1
        if Q(1, 2) < p < 1:
            K = 1-3*p+3*p*p
            L = p*(2*p-1)
            expect((lower, upper) == (L, K))
            expect(K-L == (1-p)**2)
            for prior in (Q(1, 5), Q(1, 2), Q(2, 3), Q(4, 5)):
                law = joint(p, t, t, prior)
                post = posterior(law)
                expect(post == prior*t/(prior*t + (1-prior)*(K-t)))
                expect((post >= prior) == (2*t >= K))
                minimum = prior*L/(prior*L + (1-prior)*(1-p)**2)
                expect(minimum <= post <= 1)
                raw = marginal(law, (1, 2, 3))
                expect(raw[(1, 1, 1)] == (1-prior)*K + (2*prior-1)*t)
                if prior != Q(1, 2):
                    expect((raw[(1,1,1)]-(1-prior)*K)/(2*prior-1) == t)
                else:
                    expect(raw == {c: K/2 if sum(c) in (0,3) else p*(1-p)/2 for c in BITS})
                    tau = sum(m*prod(2*x-1 for x in state) for state,m in law.items())
                    expect(tau == 8*t-12*p*p+6*p-1)
                    expect((tau+12*p*p-6*p+1)/8 == t)
            expect((L/(1-p)**2 >= 1) == (p*p+p-1 >= 0))
            if 0 < weight < 1:
                expect(min(atom_law.values()) > 0)

# Bound sharpness without assuming truth symmetry: independent conditional laws.
asymmetric_models = 0
for p in (Q(3,5), Q(2,3), Q(9,10)):
    L = p*(2*p-1)
    K = 1-3*p+3*p*p
    values = [L, (L+K)/2, K]
    for prior in (Q(1,5), Q(1,2), Q(2,3)):
        minimum = prior*L/(prior*L+(1-prior)*(1-p)**2)
        for t0,t1 in product(values, repeat=2):
            law = joint(p,t0,t1,prior)
            expect(minimum <= posterior(law) <= 1)
            asymmetric_models += 1
        expect(posterior(joint(p,L,L,prior)) == minimum)
        expect(posterior(joint(p,K,L,prior)) == 1)

p = Q(3,5)
ts = [Q(3,25), Q(13,100), Q(1,5), Q(27,125), Q(7,25)]
laws = [joint(p,t,t,Q(1,2)) for t in ts]
expect([posterior(j) for j in laws] == [Q(3,7),Q(13,28),Q(5,7),Q(27,35),Q(1)])
for size in range(4):
    for indices in combinations(range(4), size):
        expect(all(marginal(laws[0],indices) == marginal(j,indices) for j in laws[1:]))
expect(all(min(laws[i].values()) > 0 for i in (1,2,3)))
expect(posterior(laws[1]) < Q(1,2) < posterior(laws[2]))
independent = atoms(p,p**3)
expect(all(independent[c] == prod(p if bit else 1-p for bit in c) for c in BITS))

# Sample-law collision holds for all finite products by multiplicativity;
# explicitly check every ordered two-observation sample (64 outcomes).
raw0 = marginal(laws[0], (1,2,3))
raw1 = marginal(laws[3], (1,2,3))
expect(all(raw0[a]*raw0[b] == raw1[a]*raw1[b] for a,b in product(BITS, repeat=2)))

# Known unequal prior identifies the author's common t, but not two separate t_x.
a = Q(2,3)
asym0 = joint(p,Q(1,5),Q(1,5),a)
asym1 = joint(p,Q(11,50),Q(21,100),a)
expect(min(asym0.values()) > 0 and min(asym1.values()) > 0)
expect(posterior(asym0) == Q(5,6))
expect(posterior(asym1) == Q(7,8))
for size in range(4):
    for indices in combinations(range(4),size):
        expect(marginal(asym0,indices) == marginal(asym1,indices))

# Deliberately excluded endpoint regimes and impossible-event guards.
expect(posterior(joint(Q(1,2),Q(0),Q(0),Q(1,2))) == 0)
expect(posterior(joint(Q(1,2),Q(1,4),Q(1,4),Q(1,2))) == 1)
expect(posterior(joint(Q(1),Q(1),Q(1),Q(1,2))) == 1)
expect(posterior(joint(p,Q(3,25),Q(3,25),Q(0))) == 0)
expect(posterior(joint(p,Q(7,25),Q(7,25),Q(0))) is None)
expect(posterior(joint(p,Q(3,25),Q(3,25),Q(1))) == 1)
expect(posterior(joint(Q(1),Q(1),Q(1),Q(0))) is None)
expect(posterior(joint(Q(1,2),Q(0),Q(0),Q(1))) is None)

binding_records = []
verified = []
manifest = {'files': []}
if not args.mathematics_only:
    bindings = json.loads((AUTHOR/'INPUT_BINDINGS.json').read_text())
    binding_records = bindings['attachments'] + bindings['bound_prior_inputs']
    for record in binding_records:
        data = (ROOT/record['path']).read_bytes()
        expect(len(data) == record['bytes'])
        expect(sha256(data).hexdigest() == record['sha256'])
        verified.append(record['path'])
    manifest = json.loads((AUTHOR/'MANIFEST.json').read_text())
    for record in manifest['files']:
        data = (AUTHOR/record['path']).read_bytes()
        expect(len(data) == record['bytes'])
        expect(sha256(data).hexdigest() == record['sha256'])
    expect(sha256((AUTHOR/'RESULT.md').read_bytes()).hexdigest() == 'a86cced3f856527cbfab677458c2792e36bab1a89dc0684f3c5a0447c8ef0eb2')

result = {
    'status': 'PASS',
    'exact_assertions': checks,
    'moment_constraint_rank': 7,
    'general_accuracy_models': models,
    'asymmetric_truth_models': asymmetric_models,
    'parameter_grid_includes_p_zero_half_one': True,
    'prior_endpoint_impossible_events_guarded': True,
    'author_manifest_entries_verified': len(manifest['files']),
    'binding_records_verified': len(binding_records),
    'unique_bound_files_verified': len(set(verified)),
    'mathematics_only': args.mathematics_only,
    'asymmetric_unequal_prior_countercontrol_posteriors': ['5/6','7/8'],
    'scope': ('Independent finite exact mathematics only; upstream custody checks explicitly skipped. No formal-kernel, historical, novelty-search, release, or audit-closure claim.' if args.mathematics_only else 'Independent finite exact controls and custody checks; no formal-kernel, historical, novelty-search, release, or audit-closure claim.')
}
output = 'MATHEMATICS_ONLY_RESULTS.json' if args.mathematics_only else 'INDEPENDENT_RESULTS.json'
(HERE/output).write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
