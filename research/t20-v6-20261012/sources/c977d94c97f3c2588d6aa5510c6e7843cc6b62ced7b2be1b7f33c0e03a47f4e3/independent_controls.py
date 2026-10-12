#!/usr/bin/env python3
"""Reviewer-authored finite-fibre controls; not a proof of the measure theorem."""
import json
import random
from pathlib import Path
import mpmath as mp

mp.mp.dps = 70
rng = random.Random(119821)

def m(v):
    return mp.mpf(v)

def normalized(row):
    row = list(map(m, row))
    total = sum(row)
    return [v / total for v in row]

# Cases deliberately include zeros, disjoint support, equal endpoints,
# asymmetric overlap, and random sparse rows. These were not copied from
# the root's announced two-row control.
pairs = [
    ([1, 0, 0, 0], [0, 0, 1, 0]),
    ([2, 0, 3, 7], [2, 0, 3, 7]),
    ([1, 4, 0, 7], [0, 3, 8, 1]),
    ([1, 9, 2, 3], [8, 0, 1, 5]),
]
for _ in range(100):
    a = [rng.randrange(0, 11) for _ in range(7)]
    b = [rng.randrange(0, 11) for _ in range(7)]
    if sum(a) and sum(b):
        pairs.append((a, b))

times = list(map(m, ['0.000000000001', '0.01', '0.13', '0.5', '0.87', '0.99', '0.999999999999']))
errors = dict(mass=mp.mpf(0), source=mp.mpf(0), energy=mp.mpf(0), endpoint=mp.mpf(0))
angles = []
energies = []
for aa, bb in pairs:
    p, q = normalized(aa), normalized(bb)
    lam = [a+b for a, b in zip(p, q)]
    u = [mp.sqrt(a/l) if l else m(0) for a, l in zip(p, lam)]
    w = [mp.sqrt(b/l) if l else m(0) for b, l in zip(q, lam)]
    affinity = sum(a*b*l for a,b,l in zip(u,w,lam))
    affinity = min(m(1), max(m(0), affinity))
    theta = mp.acos(affinity)
    if all(a == b for a,b in zip(p,q)):
        theta = m(0)
    angles.append(theta)
    energies.append(4*theta**2)
    for t in times + [m(0),m(1)]:
        if not theta:
            A, B, dA, dB = 1-t, t, m(-1), m(1)
        else:
            A = mp.sin((1-t)*theta)/mp.sin(theta)
            B = mp.sin(t*theta)/mp.sin(theta)
            dA = -theta*mp.cos((1-t)*theta)/mp.sin(theta)
            dB = theta*mp.cos(t*theta)/mp.sin(theta)
        root = [A*a+B*b for a,b in zip(u,w)]
        dr = [dA*a+dB*b for a,b in zip(u,w)]
        mass = [r*r*l for r,l in zip(root,lam)]
        source = [2*r*d*l for r,d,l in zip(root,dr,lam)]
        errors['mass'] = max(errors['mass'], abs(sum(mass)-1))
        errors['source'] = max(errors['source'], abs(sum(source)))
        if t in (0,1):
            expected = p if not t else q
            errors['endpoint'] = max(errors['endpoint'], max(abs(a-b) for a,b in zip(mass,expected)))
        else:
            energy = sum(r*r/a for r,a in zip(source,mass) if a)
            errors['energy'] = max(errors['energy'], abs(energy-4*theta**2))

# Analytic Fourier leakage: 1+epsilon*sin(pi*t)*cos(2*pi*(N+1)*y)
# has mass one, matches modes 1..N, and violates mode N+1 by
# epsilon*sin(pi*t)/2. This finite, non-optimal feasible control prevents
# confusing finite constraints with the entire marginal.
N, epsilon, t = 4, m('0.3'), m('0.5')
leak = epsilon*mp.sin(mp.pi*t)/2
checks = {
    'finite_fibre_cases': len(pairs),
    'interior_time_samples_per_case': len(times),
    'max_abs_residuals': {k: str(v) for k,v in errors.items()},
    'residual_tolerance': '1e-60',
    'disjoint_support_energy': str(energies[0]),
    'pi_squared': str(mp.pi**2),
    'equal_endpoint_energy': str(energies[1]),
    'all_fibre_angles_within_zero_pi_over_two': all(0 <= a <= mp.pi/2 for a in angles),
    'all_fibre_energies_at_most_pi_squared': all(e <= mp.pi**2 + m('1e-65') for e in energies),
    'finite_fourier_modes_tested': N,
    'untested_mode_moment_error_at_half_time': str(leak),
    'limitations': 'Numerical finite-fibre identity checks and one analytic finite-test leakage example. No infinite-dimensional existence proof, optimizer, rate, or solver validation.',
}
checks['passed'] = all(v < m('1e-60') for v in errors.values()) and checks['all_fibre_angles_within_zero_pi_over_two'] and checks['all_fibre_energies_at_most_pi_squared'] and leak != 0
Path(__file__).with_name('independent_controls_results.json').write_text(json.dumps(checks, indent=2)+'\n')
print(json.dumps(checks, indent=2))
if not checks['passed']:
    raise RuntimeError('Independent control failed')
