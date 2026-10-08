"""Synthetic-only, independently derived exact controls. No archive I/O."""
from fractions import Fraction as Q
from functools import lru_cache
from itertools import product
from math import prod

GAMMAS = tuple(map(Q, ['1', '1.1', '1.25', '1.5', '2', '3', '5', '10']))


def exp_negative_enclosure(x, bits=512):
    """Enclose exp(-x) via positive Taylor bounds, reciprocal, dyadic squaring.

    For y=x/2**k <= 1, T_n <= exp(y) <= T_n + next/(1-y/(n+2)).
    The upper remainder follows by domination of all subsequent term ratios.
    Reciprocal reverses endpoints; each squaring uses outward integer rounding.
    """
    x = Q(x)
    assert x >= 0 and bits >= 256
    if x == 0:
        return Q(1), Q(1)
    k = 0
    y = x
    while y > 1:
        y /= 2
        k += 1
    total = term = Q(1)
    n = 0
    tolerance = Q(1, 2 ** (bits + 16))
    while True:
        nxt = term * y / (n + 1)
        remainder = nxt / (1 - y / (n + 2))
        if remainder <= tolerance:
            break
        total += nxt
        term = nxt
        n += 1
    scale = 2 ** bits
    lowq = 1 / (total + remainder)
    highq = 1 / total
    low = (lowq.numerator * scale) // lowq.denominator
    high = -((-highq.numerator * scale) // highq.denominator)
    for _ in range(k):
        low = (low * low) // scale
        high = -((-high * high) // scale)
    return Q(low, scale), Q(high, scale)


def closed_enclosure(t, total_abs, variance, gamma, bits=512):
    t, total_abs, variance, gamma = map(Q, (t, total_abs, variance, gamma))
    assert t >= 0 and total_abs >= 0 and variance >= 0 and gamma >= 1
    if not variance or not t:
        return Q(1), Q(1)
    drift = (gamma - 1) * total_abs / (gamma + 1)
    x = max(Q(0), t - drift) ** 2 / (2 * variance)
    lo, hi = exp_negative_enclosure(x, bits)
    return min(Q(1), 2 * lo), min(Q(1), 2 * hi)


def adaptive_tail(weights, threshold, gamma, directed=0):
    """Exact whole-tree Bellman oracle for tiny synthetic vectors only."""
    weights = tuple(map(Q, weights))
    threshold, gamma = Q(threshold), Q(gamma)
    low, high = 1 / (1 + gamma), gamma / (1 + gamma)

    @lru_cache(None)
    def val(i, total):
        if i == len(weights):
            event = abs(total) >= threshold if not directed else directed * total >= threshold
            return Q(int(event))
        minus = val(i + 1, total - weights[i])
        plus = val(i + 1, total + weights[i])
        return max((1 - q) * minus + q * plus for q in (low, high))
    return val(0, Q(0))


def exhaustive_adaptive(weights, threshold, gamma):
    """Enumerate every endpoint policy, independently of Bellman merging."""
    weights, threshold, gamma = tuple(map(Q, weights)), Q(threshold), Q(gamma)
    assert len(weights) <= 3
    histories = [h for i in range(len(weights)) for h in product((0, 1), repeat=i)]
    low, high = 1 / (1 + gamma), gamma / (1 + gamma)
    best = Q(0)
    for parameters in product((low, high), repeat=len(histories)):
        policy = dict(zip(histories, parameters))
        mass = Q(0)
        for z in product((0, 1), repeat=len(weights)):
            total = sum((a * (2 * b - 1) for a, b in zip(weights, z)), Q(0))
            if abs(total) >= threshold:
                mass += prod(policy[z[:i]] if bit else 1 - policy[z[:i]] for i, bit in enumerate(z))
        best = max(best, mass)
    return best


def product_tail_max(weights, threshold, gamma, directed=0):
    weights, threshold, gamma = tuple(map(Q, weights)), Q(threshold), Q(gamma)
    low, high = 1 / (1 + gamma), gamma / (1 + gamma)
    best = Q(0)
    for probabilities in product((low, high), repeat=len(weights)):
        mass = Q(0)
        for z in product((0, 1), repeat=len(weights)):
            total = sum((a * (2 * b - 1) for a, b in zip(weights, z)), Q(0))
            event = abs(total) >= threshold if not directed else directed * total >= threshold
            if event:
                mass += prod(p if bit else 1 - p for p, bit in zip(probabilities, z))
        best = max(best, mass)
    return best


def fixture():
    """Semantic records only, unrelated to the archive's serialization."""
    records = []
    for game, members in [('game-A', ['p1']), ('game-B', ['p1', 'p2'])]:
        for p in members:
            for r in range(48):
                records.append(dict(game=game, player=p, round=r,
                    truth=True, local_correct=True,
                    global_correct=(game == 'game-A' and r >= 24),
                    local_left=(game == 'game-A' or r < 36), forecast=Q(100)))
    return records


def descriptive_oracle(records):
    rosters = {}
    for row in records:
        rosters.setdefault(row['game'], set()).add(row['player'])
    keys = {(r['game'], r['player'], r['round']) for r in records}
    assert len(keys) == len(records)
    assert keys == {(g, p, r) for g, ps in rosters.items() for p in ps for r in range(48)}
    out = dict(S=Q(0), H=Q(0), total_abs=Q(0), V=Q(0),
               Q_plus=Q(0), Q_minus=Q(0), M_plus=Q(0), M_minus=Q(0),
               V_plus=Q(0), V_minus=Q(0), present=0, absent=0, midpoint=0,
               eligible=0, eligible_present=0, eligible_absent=0, eligible_midpoint=0)
    game_weights = {g: Q(0) for g in rosters}
    for row in records:
        w = Q(1, len(rosters) * len(rosters[row['game']]) * 48)
        game_weights[row['game']] += w
        L = row['truth'] if row['local_correct'] else not row['truth']
        J = row['truth'] if row['global_correct'] else not row['truth']
        E = L != J
        F = row['forecast']
        R = F is not None
        out['present' if R else 'absent'] += 1
        out['midpoint'] += int(R and F == 50)
        if E:
            out['eligible'] += 1
            out['eligible_present' if R else 'eligible_absent'] += 1
            out['eligible_midpoint'] += int(R and F == 50)
        c = w * E
        y = (2 * int(L) - 1) * (F / 50 - 1) if R else Q(0)
        a = c * y
        side = 'plus' if row['local_left'] else 'minus'
        out['S'] += a * (1 if row['local_left'] else -1)
        out['H'] += c
        out['total_abs'] += abs(a)
        out['V'] += a * a
        out['Q_' + side] += a
        out['M_' + side] += c
        out['V_' + side] += c * R
    out['game_weights'] = game_weights
    out['T'] = abs(out['S'])
    return out
