from itertools import product, combinations
from fractions import Fraction
from pathlib import Path
import json


def value(table, p):
    total = Fraction(0)
    for s, w in table.items():
        pr = Fraction(1)
        for i, a in enumerate(s):
            pr *= p[i] if a == 1 else 1-p[i]
        total += pr*w
    return total


def rectangles(table, n):
    for i, j in combinations(range(n), 2):
        others = [k for k in range(n) if k not in (i, j)]
        for fixed in product((0, 1), repeat=len(others)):
            corners = {}
            for a, b in product((0, 1), repeat=2):
                s = [0]*n
                for k, z in zip(others, fixed):
                    s[k] = z
                s[i], s[j] = a, b
                corners[a, b] = tuple(s)
            delta = (table[corners[0, 0]] + table[corners[1, 1]]
                     - table[corners[0, 1]] - table[corners[1, 0]])
            yield i, j, corners, delta


def check(n):
    profiles = list(product((0, 1), repeat=n))
    counts = {'tables': 0, 'additive_tables': 0, 'nonadditive_tables': 0,
              'verified_concavity_violations': 0, 'verified_convexity_violations': 0}
    for vals in product((-1, 0, 1), repeat=len(profiles)):
        table = dict(zip(profiles, vals))
        counts['tables'] += 1
        rs = list(rectangles(table, n))
        additive = all(d == 0 for _, _, _, d in rs)
        zero = (0,)*n
        def decomp(s):
            return table[zero] + sum(table[tuple(a if k == i else 0 for k,a in enumerate(s))]
                                    - table[zero] for i in range(n))
        assert additive == all(table[s] == decomp(s) for s in profiles)
        if additive:
            counts['additive_tables'] += 1
            continue
        counts['nonadditive_tables'] += 1
        i,j,c,d = next(r for r in rs if r[3])
        mid = [Fraction(a) for a in c[0,0]]
        mid[i] = mid[j] = Fraction(1,2)
        wm = value(table, mid)
        diag = Fraction(table[c[0,0]] + table[c[1,1]],2)
        off = Fraction(table[c[0,1]] + table[c[1,0]],2)
        assert min(diag, off) < wm < max(diag,off)
        counts['verified_concavity_violations'] += 1
        counts['verified_convexity_violations'] += 1
    return counts


if __name__ == '__main__':
    report = {
        'two_players_two_responses': check(2),
        'three_players_two_responses': check(3),
        'coordination_control': {
            'payoff': {'00': 2, '01': 0, '10': 0, '11': 1},
            'product_half_marginals': '3/4',
            'correlated_half_diagonals_same_marginals': '3/2',
            'unrestricted_product_optimum': 2,
            'unrestricted_joint_optimum': 2,
        },
        'scope': 'Finite exact arithmetic checks support the analytic theorem; not an exhaustive test over arbitrary real tables.',
    }
    Path(__file__).with_name('team_concavity_results.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))
