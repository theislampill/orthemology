#!/usr/bin/env python3
"""Finite exact-rational review controls; no simulated/physical observations."""
from fractions import Fraction as F
from itertools import product
from math import factorial
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
LABELS = ('A', 'B', 'OR', 'AND')
CODES = ((1,0), (0,1), (1,1), (0,0))
RESULTS = {}


def response(a, b):
    return (a, b, 1-(1-a)*(1-b), a*b)


def joint(p, q, t):
    return {(1,1):t, (1,0):p-t, (0,1):q-t, (0,0):1-p-q+t}


def determinant(matrix):
    m = [list(row) for row in matrix]
    d = F(1)
    for i in range(len(m)):
        if m[i][i] == 0:
            k = next((k for k in range(i+1,len(m)) if m[k][i]), None)
            if k is None:
                return F(0)
            m[i], m[k] = m[k], m[i]
            d = -d
        pivot = m[i][i]
        d *= pivot
        for j in range(i+1,len(m)):
            ratio = m[j][i]/pivot
            for k in range(i,len(m)):
                m[j][k] -= ratio*m[i][k]
    return d


def exp_bounds(x, n=40):
    """Exact enclosing Taylor sum and positive geometric bound on tail."""
    assert x >= 0 and x < n+2
    lower = sum((x**k/F(factorial(k)) for k in range(n+1)), F(0))
    first = x**(n+1)/F(factorial(n+1))
    upper = lower + first/(1-x/F(n+2))
    return lower, upper


# 1. Exact deterministic code map; order matters.
p0, p1 = response(F(1),F(0)), response(F(0),F(1))
assert tuple(zip(p0,p1)) == CODES
matrix = [[F(code == CODES[j]) for j in range(4)] for code in CODES]
assert determinant(matrix) == 1
assert sum(CODES[0]) == sum(CODES[1])  # collapsing to counts loses A versus B
RESULTS['deterministic_code_map'] = dict(zip(LABELS, ['10','01','11','00']))

# 2. All-profile mixture identity on a finite rational grid.
count = 0
for ai, bi in product(range(13), repeat=2):
    r = response(F(ai,12), F(bi,12))
    assert r[0]+r[1] == r[2]+r[3]
    count += 1
RESULTS['one_trial_identity_grid'] = count

# 3. Transcript equality for one explicit genuinely adaptive strategy.
def profile(history):
    s, k = sum(history), len(history)
    return F(s+1,k+2), F(k-s+1,k+3)

histories = {(): (F(1),F(1))}
compared = 0
for depth in range(7):
    nxt = {}
    for h, (left,right) in histories.items():
        assert left == right
        compared += 1
        r = response(*profile(h))
        p, q = (r[0]+r[1])/2, (r[2]+r[3])/2
        assert p == q
        for bit in (0,1):
            nxt[h+(bit,)] = (left*(p if bit else 1-p), right*(q if bit else 1-q))
    histories = nxt
RESULTS['adaptive_history_nodes_checked'] = compared

# 4. Shared versus fresh labels at crossed corners.
left_shared = {c:F(c in (CODES[0],CODES[1]),2) for c in CODES}
right_shared = {c:F(c in (CODES[2],CODES[3]),2) for c in CODES}
assert sum(min(left_shared[c],right_shared[c]) for c in CODES) == 0
fresh = joint(F(1,2),F(1,2),F(1,4))
assert set(fresh.values()) == {F(1,4)}
RESULTS['crossed_shared_labels_total_variation'] = '1'
RESULTS['crossed_fresh_labels_common_cell_probability'] = '1/4'

# 5. Frechet endpoints exhaust extremal couplings for fixed Bernoulli marginals.
checks = 0
for eta in (F(0),F(1,1000),F(1,48),F(1,16)):
    for d1,e1,d2,e2 in product((F(0),eta/2,eta), repeat=4):
        r = response(1-d1,e1)
        s = response(d2,1-e2)
        for j in range(4):
            first_error = 1-r[j] if CODES[j][0] else r[j]
            second_error = 1-s[j] if CODES[j][1] else s[j]
            assert 0 <= first_error <= eta and 0 <= second_error <= eta
            for t in (max(F(0),r[j]+s[j]-1), min(r[j],s[j])):
                law = joint(r[j],s[j],t)
                assert min(law.values()) >= 0 and sum(law.values()) == 1
                assert law[CODES[j]] >= 1-2*eta
                checks += 1
    sharp = joint(1-eta,eta,eta)
    assert sharp[(1,0)] == 1-2*eta
RESULTS['frechet_endpoint_checks'] = checks
RESULTS['union_bound_sharp_on_tested_etas'] = True

# 6. Floor separation and conservative exponent constants, including w=1.
weights = (F(1),F(1,2),F(1,3),F(1,4),F(1,8),F(1,1000))
for w in weights:
    for beta in (F(0),w/16,w/8):
        assert beta <= w/8
        assert (1-beta)*w >= 7*w/8 > w/2 > beta
    p, threshold = 7*w/8,w/2
    exponent = (p-threshold)**2/(2*p)
    assert exponent == 9*w/112 > w/16
    # ln 2 >= 1/2 gives the claimed absent-label exponent.
    assert w/8-threshold*F(1,2) == -w/8
RESULTS['floor_and_exponent_weight_cases'] = len(weights)

# 7. Exact enclosure of logs needed for ceil(48 log 80)=211.
assert exp_bounds(F(210,48))[1] < 80
assert exp_bounds(F(211,48))[0] > 80
assert F(2)*F(1,48) == F(1,24) == F(1,3)/8
RESULTS['numerical_design'] = {'w':'1/3','delta':'1/20','eta_max':'1/48',
                             'groups':211,'endpoints':422,
                             'ceil_proof':'exp(210/48) < 80 < exp(211/48), exact Taylor bounds'}

# 8. Oracle overlap/TV, and the stronger simultaneous-error criterion.
oracle_checks = 0
for w in (F(1,2),F(1,3),F(1,8)):
    for n in range(0,9):
        alt = {bits:w**sum(bits)*(1-w)**(n-sum(bits)) for bits in product((0,1), repeat=n)}
        assert sum(alt.values()) == 1
        all_a = (0,)*n
        overlap = alt[all_a]
        assert overlap == (1-w)**n
        error = overlap/(1+overlap)
        # Test says H1 with probability error on the common all-A event.
        assert (1-error)*overlap == error
        oracle_checks += 1
assert F(2,3)**5 > F(1,10) >= F(2,3)**6
assert F(2,3)**7 > F(1,19) >= F(2,3)**8
RESULTS['oracle_enumeration_cases'] = oracle_checks
RESULTS['oracle_example_lower_bound_groups'] = {'stated_2delta_bound':6,'sharp_simultaneous_two_point_bound':8}

# 9. Independently recompute every supplied corner-control row.
corner_path = HERE/'frozen'/'CORNER_SIGNATURE_CONTROL.json'
corner = json.loads(corner_path.read_text())
for row in corner['rows']:
    a,b = F(row['a']),F(row['b'])
    A,AA,A_AB = a, 1-(1-a)**2, 1-(1-a)*(1-a*b)
    assert (A,AA,A_AB) == tuple(F(row[k]) for k in ('A','AA','A_AB'))
    assert AA-A == a*(1-a)
    assert A_AB-A == a*b*(1-a)
    if a in (0,1) and b in (0,1):
        assert A == AA == A_AB
assert (F(1,2),F(3,4),F(5,8)) == (F(1,2),1-(1-F(1,2))**2,1-(1-F(1,2))*(1-F(1,4)))
RESULTS['corner_control_rows_recomputed'] = len(corner['rows'])

# 10. One fixed two-repeat panel has rank <=3; multiple panels can recover rank4.
r = response(F(1,4),F(1,2))
s = response(F(1,2),F(1,4))
ordered = [[(1-v)**2 for v in r],[(1-v)*v for v in r],
           [v*(1-v) for v in r],[v*v for v in r]]
assert ordered[1] == ordered[2] and determinant(ordered) == 0
multi = [[F(1)]*4,list(r),[v*v for v in r],list(s)]
assert determinant(multi) == F(-3,256)
RESULTS['fixed_panel_determinant'] = '0'
RESULTS['multiple_panel_augmented_determinant'] = '-3/256'

# 11. Correct per-label marginals do not alone give the adaptive kernel premise.
# A single uniform U, independent of all fresh labels, is shared across groups.
# At a=b=1/2: A,B succeed below U=1/2; OR below 3/4; AND below 1/4.
left_cross_group = {(1,1):F(1,2),(1,0):F(0),(0,1):F(0),(0,0):F(1,2)}
right_cross_group = {(1,1):F(3,8),(1,0):F(1,8),(0,1):F(1,8),(0,0):F(3,8)}
assert sum(left_cross_group.values()) == sum(right_cross_group.values()) == 1
for law in (left_cross_group,right_cross_group):
    assert sum(v for (x,y),v in law.items() if x) == F(1,2)
    assert sum(v for (x,y),v in law.items() if y) == F(1,2)
assert left_cross_group != right_cross_group
RESULTS['cross_group_coupling_counterexample'] = {
    'left_order_11_10_01_00':['1/2','0','0','1/2'],
    'right_order_11_10_01_00':['3/8','1/8','1/8','3/8']}

# 12. Swapped-profile interior determinant in the author's stated row/column order.
checks = 0
for ai,bi in product(range(17),repeat=2):
    a,b = F(ai,16),F(bi,16)
    r,s = response(a,b),response(b,a)
    channel = [[(1-p)*(1-q),(1-p)*q,p*(1-q),p*q] for p,q in zip(r,s)]
    actual = determinant(channel)
    claimed = (a-b)*(a+b-2*a*b)*((a-b)**2+2*a*b*(1-a)*(1-b))
    assert actual == claimed
    assert (actual == 0) == (a == b)
    # Count compression of product Bernoulli A/B rows agrees despite unequal ordered laws.
    counts_a = [channel[0][0],channel[0][1]+channel[0][2],channel[0][3]]
    counts_b = [channel[1][0],channel[1][1]+channel[1][2],channel[1][3]]
    assert counts_a == counts_b == [(1-a)*(1-b),a+b-2*a*b,a*b]
    assert (channel[0] == channel[1]) == (a == b)
    checks += 1
RESULTS['interior_determinant_exact_grid_checks'] = checks

print(json.dumps({'status':'PASS','families':12,'results':RESULTS}, indent=2))
