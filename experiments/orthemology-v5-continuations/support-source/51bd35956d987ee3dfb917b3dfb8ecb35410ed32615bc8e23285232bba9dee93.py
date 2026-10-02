#!/usr/bin/env python3
"""Reviewer-written exact checks. Finite controls, NOT a continuum proof.

No third-party imports and no floating-point arithmetic. The proof assessment is
in INDEPENDENT_REVIEW.md. This file does not import the author's checker.
"""
from fractions import Fraction as Q
from itertools import combinations, permutations, product
import hashlib
import json
import random


def require(condition, explanation):
    if not condition:
        raise AssertionError(explanation)


def ceiling(q):
    return (q.numerator + q.denominator - 1) // q.denominator


def blocks(u, b):
    """Direct minimax over integral corruption allocations (no quota formula)."""
    values = []
    for s in range(1, u):
        feasible = [min(Q(a, s), Q(b-a, u-s))
                    for a in range(b+1) if a <= s and b-a <= u-s]
        values.append((max(feasible), s))
    return min(values)


def dual_block_value(u, b):
    """Independent floor-threshold allocation with N=b-1, reversing extrema."""
    return min(max(Q(a, s), Q(b-1-a, u-s))
               for s in range(1, u) for a in range(b))


def prefixes(order):
    masks, current = [0], 0
    for i in order:
        current |= 1 << i
        masks.append(current)
    return masks


def independent(mask, pref, cap):
    return all((mask & p).bit_count() <= c for p, c in zip(pref, cap))


def formula_rank(mask, pref, cap):
    return min((mask & ~p).bit_count()+c for p, c in zip(pref, cap))


def brute_ranks(n, pref, cap):
    """Subset-DP from actual independence, not the claimed rank formula."""
    rank = [0]*(1 << n)
    for mask in range(1, 1 << n):
        if independent(mask, pref, cap):
            rank[mask] = mask.bit_count()
        else:
            bits = mask
            while bits:
                bit = bits & -bits
                rank[mask] = max(rank[mask], rank[mask ^ bit])
                bits ^= bit
    return rank


def matroid_intersection(n, first, second, cap):
    """Shortest augmenting paths, independent implementation of standard oracle algorithm."""
    chosen = 0
    while True:
        inside = [x for x in range(n) if chosen >> x & 1]
        outside = [x for x in range(n) if not chosen >> x & 1]
        sources = [x for x in outside if independent(chosen | (1 << x), first, cap)]
        sinks = {x for x in outside if independent(chosen | (1 << x), second, cap)}
        predecessor = {x: None for x in sources}
        queue = list(sources)
        endpoint = None
        for x in queue:
            if x in sinks:
                endpoint = x
                break
            if chosen >> x & 1:
                candidates = [y for y in outside
                              if independent(chosen ^ (1 << x) ^ (1 << y), first, cap)]
            else:
                candidates = [y for y in inside
                              if independent(chosen ^ (1 << x) ^ (1 << y), second, cap)]
            for y in candidates:
                if y not in predecessor:
                    predecessor[y] = x
                    queue.append(y)
        if endpoint is None:
            return chosen
        old_size = chosen.bit_count()
        while endpoint is not None:
            chosen ^= 1 << endpoint
            endpoint = predecessor[endpoint]
        require(chosen.bit_count() == old_size+1, "invalid augmentation cardinality")
        require(independent(chosen, first, cap), "augmentation violates first matroid")
        require(independent(chosen, second, cap), "augmentation violates second matroid")


def run():
    counts = {}
    # Every breakpoint and every intervening open cell is represented. This
    # checks the right-hand jump which breakpoint-only enumeration would miss.
    threshold_checks = 0
    bound_checks = 0
    examples = []
    for u in range(2, 26):
        breakpoints = sorted({Q(a, d) for d in range(1, u+1) for a in range(d+1)})
        probes = breakpoints + [(a+b)/2 for a, b in zip(breakpoints, breakpoints[1:])]
        for b in range(1, u):
            value, s = blocks(u, b)
            require(value == dual_block_value(u, b), ("reversed-extrema identity", u, b))
            require(value < 1, ("forbidden t=1", u, b))
            require((value == 0) == (b == 1), ("zero boundary", u, b))
            for t in probes:
                quota_cost = max(ceiling(t*k)+ceiling(t*(u-k)) for k in range(u+1))
                require((quota_cost <= b) == (t <= value), ("closed interval", u, b, t))
                threshold_checks += 1
            if (u, b) in [(2,1), (7,3), (11,5), (8,3), (9,4), (6,5)]:
                examples.append({"u":u, "b":b, "B":str(value), "attaining_block_sizes":[s,u-s]})
            bound_checks += 1
    counts["partition_and_independent_floor_dual"] = bound_checks
    counts["all_threshold_breakpoints_and_open_cells"] = threshold_checks

    # Stronger than the floor(alpha*k) subfamily: all integral monotone
    # 1-Lipschitz capacities, including all loops and the free matroid.
    rank_checks = exchange_checks = scalar_checks = 0
    for n in range(1, 9):
        pref = prefixes(range(n))
        for increments in product((0,1), repeat=n):
            cap = [0]
            for a in increments:
                cap.append(cap[-1]+a)
            rank = brute_ranks(n, pref, cap)
            for mask, value in enumerate(rank):
                require(value == formula_rank(mask, pref, cap), ("chain rank", n, cap, mask))
                rank_checks += 1
            g = min(cap[s]+cap[n-s] for s in range(n+1))
            h = min(cap[k]+cap[l]+max(0,n-k-l) for k in range(n+1) for l in range(n+1))
            require(g == h, ("min-min scalar equality", n, cap))
            scalar_checks += 1
            if n <= 6:
                inds = [mask for mask in range(1 << n) if rank[mask] == mask.bit_count()]
                for first in inds:
                    for second in inds:
                        if first.bit_count() >= second.bit_count():
                            continue
                        require(any(independent(first | (1 << x), pref, cap)
                                    for x in range(n) if second >> x & 1 and not first >> x & 1),
                                ("exchange axiom", n, cap, first, second))
                        exchange_checks += 1
    counts["all_binary_capacity_rank_subsets"] = rank_checks
    counts["all_binary_capacity_exchange_pairs_through_6"] = exchange_checks
    counts["all_binary_capacity_min_min_equalities"] = scalar_checks

    intersection_checks = algorithm_checks = reverse_checks = 0
    for n in range(1, 7):
        full = (1 << n)-1
        pref1 = prefixes(range(n))
        perms = list(permutations(range(n)))
        for increments in product((0,1), repeat=n):
            cap = [0]
            for a in increments:
                cap.append(cap[-1]+a)
            rank1 = brute_ranks(n, pref1, cap)
            common_candidates = [m for m in range(1 << n) if rank1[m] == m.bit_count()]
            g = min(cap[s]+cap[n-s] for s in range(n+1))
            for ix, order in enumerate(perms):
                pref2 = prefixes(order)
                # Directly enumerate common independent sets and independently
                # evaluate the rank sum. This is not a row probability grid.
                actual = max(m.bit_count() for m in common_candidates if independent(m, pref2, cap))
                rank2 = [formula_rank(mask, pref2, cap) for mask in range(1 << n)]
                formula = min(rank1[a]+rank2[full ^ a] for a in range(1 << n))
                require(actual == formula and actual >= g, ("two-matroid rank sum", n, cap, order))
                intersection_checks += 1
                if order == tuple(reversed(range(n))):
                    require(actual == g, ("reverse-order sharpness", n, cap))
                    reverse_checks += 1
                if ix in {0,len(perms)//2,len(perms)-1}:
                    found = matroid_intersection(n, pref1, pref2, cap)
                    require(found.bit_count() == actual, ("algorithm vs brute", n, cap, order))
                    algorithm_checks += 1
    counts["all_permutations_all_binary_capacities_through_6"] = intersection_checks
    counts["reverse_order_attains_scalar_bound"] = reverse_checks
    counts["augmenting_algorithm_vs_brute_instances"] = algorithm_checks

    # Higher-dimensional rational witnesses, including ties, zeros, point
    # masses, coincident and reverse rankings, and very unequal denominators.
    rng = random.Random(930274691)
    witness_digest = hashlib.sha256()
    row_checks = 0
    for u in (2,3,7,11,17,24,32):
        for b in sorted({1,2,u//2,u-1} & set(range(1,u))):
            t, _ = blocks(u,b)
            cap = [((1-t)*k).__floor__() for k in range(u+1)]
            for trial in range(6):
                raw = [[Q(rng.randrange(11),rng.randrange(1,100)) for _ in range(u)] for _ in range(2)]
                if trial == 0:
                    raw = [[Q(int(i==j)) for i in range(u)] for j in range(2)]
                elif trial == 1:
                    raw[1] = raw[0][:]
                elif trial == 2:
                    raw = [[Q(i+1) for i in range(u)], [Q(u-i) for i in range(u)]]
                elif trial == 3:
                    raw = [[Q((i+j)%3) for i in range(u)] for j in range(2)]
                elif trial == 4:
                    raw[0] = [Q(1,10**(i+1)) for i in range(u)]
                rows = [[x/sum(row) for x in row] for row in raw]
                order = [sorted(range(u),key=lambda x:(-row[x],x)) for row in rows]
                pref = [prefixes(o) for o in order]
                d = matroid_intersection(u,pref[0],pref[1],cap)
                require(d.bit_count() >= u-b, ("insufficient common rank",u,b,trial))
                while d.bit_count() > u-b:
                    d ^= d & -d
                c = ((1 << u)-1) ^ d
                require(c.bit_count() == b, "complement has wrong cardinality")
                for row, o, p in zip(rows,order,pref):
                    a = [(c & mask).bit_count() for mask in p]
                    require(all(a[k] >= ceiling(t*k) for k in range(u+1)), "quota witness fails")
                    mass = sum(row[i] for i in range(u) if c >> i & 1)
                    sorted_row = [row[i] for i in o]+[Q(0)]
                    abel = sum((sorted_row[k-1]-sorted_row[k])*a[k] for k in range(1,u+1))
                    require(mass == abel and mass >= t, "summation by parts or probability witness fails")
                witness_digest.update(repr((u,b,trial,t,rows,c)).encode())
                row_checks += 1
    counts["rational_codebooks_with_algorithmic_witnesses"] = row_checks

    # Deliberately invalid scope/step modifications, each rejected by a witness.
    require(max((Q(1,2)*s).__floor__()+(Q(1,2)*(7-s)).__floor__()
                for s in range(8)) <= 3 and Q(3,7)<Q(1,2), "floor mutant not rejected")
    n=3; t=Q(1,2); c=0b011; row=[Q(0),Q(0),Q(1)]
    require(all((c & p).bit_count() >= ceiling(t*k)
                for k,p in enumerate(prefixes(range(n)))) and sum(row[:2])<t,
            "unsorted-row mutant not rejected")
    # Three partition matroids on a triangle have common rank 1 while the
    # proposed three-way rank-partition minimum is 2.
    pairs = [0b011,0b110,0b101]
    def rank3(mask,pair):
        return (mask & ~pair).bit_count()+min(1,(mask & pair).bit_count())
    actual3=max(mask.bit_count() for mask in range(8)
                if all(rank3(mask,p)==mask.bit_count() for p in pairs))
    false_formula3=min(sum(rank3(sum(1 << x for x in range(3) if assignment[x]==j),pairs[j])
                           for j in range(3)) for assignment in product(range(3),repeat=3))
    require((actual3,false_formula3)==(1,2), "three-matroid false formula control")
    orders=[(0,5,6,7,8,1,2,3,4),(1,3,4,7,8,0,2,5,6),(2,3,4,5,6,0,1,7,8)]
    no_quota=True
    for chosen in combinations(range(9),4):
        mask=sum(1 << x for x in chosen)
        if all((mask & p).bit_count() >= ceiling(Q(k,4))
               for o in orders for k,p in enumerate(prefixes(o))):
            no_quota=False
    require(no_quota,"three-ordering obstruction did not reproduce")
    fixed=blocks(8,3)[0]
    public=Q(sum(set(pair)<=set(range(3)) for pair in combinations(range(8),2)),28)
    require((fixed,public)==(Q(1,4),Q(3,28)),"private/public separation")
    # At reciprocal thresholds, the exact ceiling cost agrees with the known
    # Suksompong size bound. This is arithmetic, not a literature novelty test.
    reciprocal_checks=0
    for u in range(2,31):
        for k in range(2,16):
            actual=max(ceiling(Q(s,k))+ceiling(Q(u-s,k)) for s in range(u+1))
            require(actual==ceiling(Q(u+k-1,k)),("reciprocal source matching",u,k))
            reciprocal_checks+=1
    counts["reciprocal_size_bound_matches_ceiling_cost"] = reciprocal_checks
    return {"status":"PASS", "scope":"Finite structural regressions supporting a separately inspected general proof; not a formalization or probability-grid proof", "counts":counts,
            "examples":examples,"witness_sha256":witness_digest.hexdigest(),
            "negative_controls":{"ceiling_to_floor":"rejected by uniform rows at (7,3), t=1/2", "omit_sorting":"rejected by point mass", "three_matroid_rank_partition_formula":{"actual":actual3,"false_formula":false_formula3},"three_ordering_ordinal_extension":"rejected at (9,4,1/4)","merge_private_and_public_resources":{"fixed":str(fixed),"public":str(public)}}}


if __name__ == "__main__":
    print(json.dumps(run(),indent=2,sort_keys=True))
