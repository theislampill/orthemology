"""Finite research control, not a metaphysical admissibility interpreter.

Read the retained model, enumerate full-signature transports, and verify the
conditional exchange-invariant means claim. No recovered file is modified.
"""
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from itertools import permutations, product
from pathlib import Path
import json
import sys


ROOT = Path('[OMITTED_PRIVATE_MACHINE_PATH]')
SOURCE = ROOT / ('recovery-t20/addendum/tranche20/research-frontier-continuation/'
                 'sovereignty-choice-semantics/reactive-context-extension/src/'
                 'reactive_context.py')
EXPECTED = 'f73cee9c0271dd2a80843a3994534e1119fca33386e59a483f3175d69880a6cc'
assert sha256(SOURCE.read_bytes()).hexdigest() == EXPECTED
spec = spec_from_file_location('retained_reactive_transport_review', SOURCE)
m = module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)
c = m.Catalogue(('x', 'y'))
assert c.n == 3
codes = tuple(range(c.n))
options = (None,) + codes
perms = tuple(permutations(codes))
identity = codes


def image(perm, value):
    return None if value is None else perm[value]


def preserves(alpha, beta, gamma, domain):
    return all(c.combine(image(alpha, a), image(beta, b)) ==
               image(gamma, c.combine(a, b))
               for a, b in domain)


triples = tuple(product(perms, repeat=3))
coactive = tuple(t for t in triples if preserves(*t, product(codes, repeat=2)))
full = tuple(t for t in triples if preserves(*t, product(options, repeat=2)))
assert len(triples) == 216
assert len(coactive) == 18
assert len(full) == 6
assert set(full) == {(p, p, p) for p in perms}
fixed_output_coactive = tuple(t for t in coactive if t[2] == identity)
fixed_output_full = tuple(t for t in full if t[2] == identity)
assert len(fixed_output_coactive) == 3
assert fixed_output_full == ((identity, identity, identity),)

q_results = []
for q in codes:
    # Inverse planning query under the known law; all nine profiles stay in
    # the operational domain. Goal-achievement is not original-agent eligibility.
    profiles = tuple(product(codes, repeat=2))
    fitting = tuple(p for p in profiles if c.combine(*p) == q)
    exchange_fixed = tuple((a, b) for a, b in fitting if a == b)
    assert len(fitting) == 3
    assert exchange_fixed == ((q, q),)
    # Conservative de re target group: identity on all target codes, plus
    # optional exchange of structurally equivalent unpointed bearer roles.
    assert all(c.combine(a, b) == c.combine(b, a) for a, b in profiles)
    # Larger algebraic group permits common operation-preserving relabelings.
    stabilizer = tuple((p, swap) for p in perms for swap in (False, True)
                       if p[q] == q)
    def transported(pair, transformation):
        perm, swap = transformation
        a, b = pair
        return (perm[b], perm[a]) if swap else (perm[a], perm[b])
    common_fixed = tuple(pair for pair in fitting
                         if all(transported(pair, t) == pair for t in stabilizer))
    assert len(stabilizer) == 4
    assert common_fixed == ((q, q),)
    # Local policies take q, not an actual peer exercise or a selected profile.
    a = m.own_policy(m.Original('A'), q)
    b = m.own_policy(m.Original('B'), q)
    assert (a.setting, b.setting) == (q, q)
    actual = m.execute(c, a, b)
    assert actual['events'] == c.targets[q]
    assert all(actual['intentions'].values())
    assert all(roots == frozenset(('A', 'B')) for roots in actual['supports'].values())
    assert all(not owners for owners in actual['entire'].values())
    q_results.append({'q': q, 'active_operational_profiles': len(profiles),
                      'goal_achieving_profiles': fitting,
                      'exchange_fixed': exchange_fixed,
                      'full_algebraic_stabilizer_size': len(stabilizer),
                      'common_fixed': common_fixed,
                      'local_policy_settings': (a.setting, b.setting),
                      'individual_entire_providers': 0})

rejected = []
for shift in (1, 2):
    alpha = tuple((a + shift) % 3 for a in codes)
    beta = tuple((b - shift) % 3 for b in codes)
    assert preserves(alpha, beta, identity, product(codes, repeat=2))
    assert not preserves(alpha, beta, identity, product(options, repeat=2))
    failures = tuple((a, b) for a, b in product(options, repeat=2)
                     if c.combine(image(alpha, a), image(beta, b)) != c.combine(a, b))
    assert len(failures) == 6
    assert all((a is None) != (b is None) for a, b in failures)
    rejected.append({'shift': shift, 'coactive_law_preserved': True,
                     'full_law_preserved': False, 'failed_solo_cases': failures})

# A genuinely symmetric abstract reason fibre has an obstruction: the three
# candidates rotate freely under C3 while the reason record stays fixed.
rotations = tuple(tuple((a + shift) % 3 for a in codes) for shift in codes)
abstract_common_fixed = tuple(a for a in codes if all(p[a] == a for p in rotations))
assert abstract_common_fixed == ()
# A context augmented with selected-token w has only transformations fixing w.
# Projection-equivariance is proved in the report, not counted as a code test.
selected_token_stabilizers = tuple(sum(p[w] == w for p in rotations) for w in codes)
assert selected_token_stabilizers == (1, 1, 1)

# General odd cyclic law: exchange fixedness + success selects only q.
# Exhaustive finite checks supplement the proof; no inference uses extrapolation.
odd_n_checks = []
for n in (1, 3, 5, 7, 9, 11):
    half = (n + 1) // 2
    for q in range(n):
        solutions = tuple((a, b) for a, b in product(range(n), repeat=2)
                          if half * (a + b) % n == q)
        assert len(solutions) == n
        assert tuple((a, b) for a, b in solutions if a == b) == ((q, q),)
    odd_n_checks.append(n)

result = {
    'status': 'all finite controls passed',
    'retained_source': str(SOURCE.relative_to(ROOT)),
    'retained_sha256': EXPECTED,
    'independent_setting_output_permutation_triples_checked': len(triples),
    'coactive_preserving_triples': len(coactive),
    'full_idle_including_preserving_triples': len(full),
    'fixed_output_coactive_preserving_triples': len(fixed_output_coactive),
    'fixed_output_full_preserving_triples': len(fixed_output_full),
    'contexts': q_results,
    'rejected_anti_diagonal_shifts': rejected,
    'abstract_C3_fibre_common_fixed_choices': abstract_common_fixed,
    'selected_token_stabilizer_sizes': selected_token_stabilizers,
    'odd_cyclic_sizes_checked': odd_n_checks,
    'scope': ('Conditional structural selection and local execution only; no '
              'normative sufficiency, knowledge, original-agent eligibility, '
              'or individual whole actual efficacy is established.')}
print(json.dumps(result, indent=2))
