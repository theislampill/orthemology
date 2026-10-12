#!/usr/bin/env python3
"""Exact finite controls; RESULT.md supplies the universal ordinary proof."""
from pathlib import Path
from fractions import Fraction as Q
from math import comb, factorial, ceil
from itertools import product
from datetime import datetime, timezone
import hashlib, json, os, platform, runpy, sys
import sympy as S

HERE = Path(__file__).resolve().parent
ROOT = Path(os.environ.get('ESCAPE_SOURCE_ROOT', str(HERE.parent))).resolve()
checks = []

def check(name, ok):
    if not ok:
        raise AssertionError(name)
    checks.append({'name': name, 'passed': True})

def indices(d, n):
    return [a for a in product(range(n + 1), repeat=d) if sum(a) == n]

def moment(measure, alpha):
    return sum((w * product_number(x ** a for x, a in zip(point, alpha))
                for point, w in measure.items()), Q(0))

def product_number(values):
    out = 1
    for value in values:
        out *= value
    return out

def add(target, source, scale=Q(1)):
    for point, w in source.items():
        target[point] = target.get(point, Q(0)) + scale * w
        if target[point] == 0:
            del target[point]

def difference(alpha, radius):
    n = sum(alpha)
    denominator = radius ** n * product_number(factorial(a) for a in alpha)
    return {tuple(radius * j for j in point):
            Q((-1) ** (n - sum(point)) *
              product_number(comb(a, j) for a, j in zip(alpha, point)), denominator)
            for point in product(*(range(a + 1) for a in alpha))}

bindings = json.loads((HERE / 'INPUT_BINDINGS.json').read_text())
for item in bindings['files']:
    check('original hash: ' + item['original'],
          hashlib.sha256((ROOT / item['original']).read_bytes()).hexdigest() == item['sha256'])
    if item.get('copy'):
        check('frozen copy hash: ' + item['copy'],
              hashlib.sha256((HERE / item['copy']).read_bytes()).hexdigest() == item['sha256'])

# Multi-index finite differences are checked without floating point.
for d in [1, 2, 3]:
    for n in range(1, 6):
        for alpha in indices(d, n):
            for radius in [1, 2, 7]:
                block = difference(alpha, radius)
                for degree in range(n + 1):
                    for beta in indices(d, degree):
                        check(f'difference d={d} alpha={alpha} R={radius} beta={beta}',
                              moment(block, beta) == Q(int(alpha == beta)))
                for m in range(n):
                    # The exact l1 norm majorizes the Euclidean norm in the proof.
                    absolute = sum(abs(w) * sum(point) ** m for point, w in block.items())
                    bound = Q(2 ** n * n ** m,
                              product_number(factorial(a) for a in alpha) * radius ** (n - m))
                    check(f'variation bound d={d} alpha={alpha} R={radius} m={m}',
                          absolute <= bound)

source = runpy.run_path(str(HERE / 'inputs/countermodel.py'), run_name='escape_control_import')
model = source['SchurMoment']()
check('inherited witness Lambda(F)=-1', model.apply(source['WITNESS']) == -1)

# Execute the actual signed-measure construction through degree six, including
# all moments in the separating polynomial. Future blocks are justified by the
# written induction and tail argument, not by this finite computation.
rho = {(0, 0): Q(1)}
positive = {(0, 0): Q(1)}
negative = {}
previous_radius = 0
block_info = []
for n in range(1, 7):
    residuals = {alpha: model.moment(*alpha) - moment(rho, alpha)
                 for alpha in indices(2, n)}
    B = sum(abs(v) * Q(2 ** n, product_number(factorial(a) for a in alpha))
            for alpha, v in residuals.items())
    radius = max(1, previous_radius + 1, ceil(2 ** n * n ** (n - 1) * B))
    block = {}
    for alpha, residual in residuals.items():
        add(block, difference(alpha, radius), residual)
    check(f'degree {n}: zero mass', moment(block, (0, 0)) == 0)
    for m in range(n):
        absolute = sum(abs(w) * sum(point) ** m for point, w in block.items())
        check(f'degree {n}: summable absolute moment m={m}', absolute <= Q(1, 2 ** n))
    add(rho, block)
    add(positive, {point: w for point, w in block.items() if w > 0})
    add(negative, {point: -w for point, w in block.items() if w < 0})
    for degree in range(n + 1):
        for alpha in indices(2, degree):
            check(f'degree {n}: exact corrected moment {alpha}',
                  moment(rho, alpha) == model.moment(*alpha))
    check(f'degree {n}: P-N identity', all(
        rho.get(point, Q(0)) == positive.get(point, Q(0)) - negative.get(point, Q(0))
        for point in set(rho) | set(positive) | set(negative)))
    massP = moment(positive, (0, 0))
    massN = moment(negative, (0, 0))
    check(f'degree {n}: exact mass identity', massP == 1 + massN)
    check(f'degree {n}: negative mass at most one half', massN <= Q(1, 2))
    block_info.append({'degree': n, 'radius_bit_length': radius.bit_length(),
                       'block_atom_count': len(block), 'total_atom_count': len(rho)})
    previous_radius = radius

def apply_measure(measure, polynomial):
    return sum((c * moment(measure, alpha) for alpha, c in polynomial.items()), Q(0))

check('signed prefix realizes actual separating polynomial', apply_measure(rho, source['WITNESS']) == -1)
check('positive prefix witness is nonnegative', apply_measure(positive, source['WITNESS']) >= 0)
check('negative prefix witness is nonnegative', apply_measure(negative, source['WITNESS']) >= 0)
check('witness decomposition is exact',
      apply_measure(positive, source['WITNESS']) - apply_measure(negative, source['WITNESS']) == -1)
for point in set(positive) | set(negative):
    u, v = point
    check(f'actual block atom has positive witness {point[0].bit_length()},{point[1].bit_length()}',
          1 + u ** 4 * v ** 2 + u ** 2 * v ** 4 - u ** 2 * v ** 2 >= Q(3, 4))

# Algebraic controls of the classical active pair and the normalized hierarchy.
j, m = S.symbols('j m', integer=True)
check('lognormal lattice square completion', S.expand(m*j-j*j/2-m*m/2+(j-m)**2/2) == 0)
C, n0, lam, N, active = S.symbols('C n0 lam N active')
check('initial same-moment mixture gives genuine P', S.expand(active*lam+active*N-active*(lam+N)) == 0)
check('initial mass is one', S.simplify((1+n0)/(1+n0)-1) == 0)
Ap, Agp, A1, Ag = S.symbols('Ap Agp A1 Ag', nonzero=True)
quotient_derivative = (-Agp*A1 + Ap*Ag)/A1**2
hierarchy = -Agp/A1 + (Ag/A1)*(Ap/A1)
check('normalized hierarchy quotient identity', S.simplify(quotient_derivative-hierarchy) == 0)
t, z = S.symbols('t z', nonnegative=True)
K = t*z**4 + t**3*z*z/3
g = z**4+t*t*z*z
check('higher-degree schedule primitive', S.expand(S.diff(K,t)-g) == 0)
check('higher-degree cumulative SOS remainder', S.expand(K-t**3*z*z/3-t*z**4) == 0)

result = {'status': 'PASS', 'timestamp_utc': datetime.now(timezone.utc).isoformat(),
          'check_count': len(checks), 'python': platform.python_version(),
          'sympy': S.__version__, 'signed_prefix_blocks': block_info,
          'scope': 'Exact finite controls only. Infinite signed representation, full strict PSD, all-time nonrepresentability, and signed Fourier uniqueness are proved in RESULT.md, not inferred from these checks.',
          'checks': checks}
(HERE/'CONTROL_RESULTS.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'checks'}, indent=2))
