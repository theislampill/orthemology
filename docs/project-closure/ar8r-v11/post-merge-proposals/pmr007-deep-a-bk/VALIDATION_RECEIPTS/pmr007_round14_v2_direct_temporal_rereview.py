#!/usr/bin/env python3
"""Distinct direct-temporal rereview for PMR-007 Round 14 V2.

This implementation does not import the original checker. It uses Python sets,
explicit outer/inner approximants, Tarjan SCCs for direct co-Buchi semantics,
and an extracted rank strategy. It verifies frozen hashes before running.
"""
from __future__ import annotations
from itertools import combinations, product
from pathlib import Path
import hashlib, json, random, time

BASE = Path(__file__).resolve().parents[1]
EXPECTED = {
    "PMR-007_FRONTIER_ROUND14_LOCAL_PROTOCOL_REACH_AND_STAY_FIXED_POINT_V2.md": "e3db880891dc6baf7ba48f166951ecd4ef3b66ca5afe57e5a77a00c31919505b",
    "checks/pmr007_round14_v2_cobuchi_check.py": "b7b72e676f474e3f8dc3f0e870e67454c04612380e658d1fda944f1e9dda2d9d",
    "checks/pmr007_round14_v2_cobuchi_check_results.json": "9789cf7cc81cd6d5a9d3bf12c8958034743017321bd9db2dfa78993794715905",
    "audits/PMR-007_FRONTIER_ROUND14_V2_COLD_AUDIT.md": "bd5c08bf7fc65890cac4b06c724a66b2dfaf9f8572e1daf3a40b4bae5291c1a7",
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def all_antichains(n: int):
    universe = [frozenset(i for i in range(n) if mask & (1 << i)) for mask in range(1, 1 << n)]
    ans = []
    for r in range(1, len(universe) + 1):
        for c in combinations(universe, r):
            if all(not (a <= b or b <= a) for i, a in enumerate(c) for b in c[i+1:]):
                ans.append(tuple(c))
    return ans


def pre(menus, X: frozenset[int], Safe: frozenset[int]) -> frozenset[int]:
    return frozenset(q for q in Safe if any(succ <= X for succ in menus[q]))


def fixed_point_with_approximants(menus, Target, Safe):
    Bad = Safe - Target
    outer = [frozenset()]
    while True:
        Z = outer[-1]
        X = Safe
        while True:
            X2 = (Target & pre(menus, X, Safe)) | (Bad & pre(menus, Z, Safe))
            if X2 == X:
                break
            X = X2
        if X == Z:
            return X, outer
        outer.append(X)


def core_region(menus, Target, Safe):
    K = Target
    while True:
        K2 = Target & pre(menus, K, Safe)
        if K2 == K:
            break
        K = K2
    W = K
    while True:
        W2 = W | pre(menus, W, Safe)
        if W2 == W:
            return K, W
        W = W2


def extract_rank_strategy(menus, Target, Safe, W, outer):
    ranks = {}
    for q in W:
        ranks[q] = next(i for i, Zi in enumerate(outer) if i > 0 and q in Zi)
    strategy = {}
    for q in W:
        r = ranks[q]
        bound = outer[r] if q in Target else outer[r-1]
        witnesses = [succ for succ in menus[q] if succ <= bound]
        if not witnesses:
            raise AssertionError(("no rank witness", q, r, bound, menus[q]))
        # deterministic canonical choice
        strategy[q] = min(witnesses, key=lambda s: (len(s), tuple(sorted(s))))
    # arbitrary choices outside W; they cannot be reached by W under the selected witnesses
    for q in range(len(menus)):
        if q not in strategy:
            strategy[q] = min(menus[q], key=lambda s: (len(s), tuple(sorted(s))))
    return strategy, ranks


def tarjan_scc(adjacency: dict[int, frozenset[int]]):
    index = 0
    stack = []
    onstack = set()
    indices = {}
    low = {}
    out = []
    def visit(v):
        nonlocal index
        indices[v] = low[v] = index
        index += 1
        stack.append(v); onstack.add(v)
        for w in adjacency[v]:
            if w not in indices:
                visit(w); low[v] = min(low[v], low[w])
            elif w in onstack:
                low[v] = min(low[v], indices[w])
        if low[v] == indices[v]:
            comp = set()
            while True:
                w = stack.pop(); onstack.remove(w); comp.add(w)
                if w == v: break
            out.append(frozenset(comp))
    for v in adjacency:
        if v not in indices: visit(v)
    return out


def reachable(adjacency, start):
    seen = {start}; todo = [start]
    while todo:
        v = todo.pop()
        for w in adjacency[v]:
            if w not in seen:
                seen.add(w); todo.append(w)
    return frozenset(seen)


def winning_for_strategy(strategy, Target, Safe):
    adjacency = dict(strategy)
    sccs = tarjan_scc(adjacency)
    bad = Safe - Target
    bad_cycle_nodes = set()
    for comp in sccs:
        cyclic = len(comp) > 1 or any(v in adjacency[v] for v in comp)
        if cyclic and comp & bad:
            bad_cycle_nodes |= set(comp & bad)
    winning = set()
    for q in range(len(strategy)):
        R = reachable(adjacency, q)
        if q not in Safe or not R <= Safe:
            continue
        # A reachable bad cycle exists iff some bad-cycle member is reachable.
        if R & bad_cycle_nodes:
            continue
        winning.add(q)
    return frozenset(winning)


def direct_union(menus, Target, Safe):
    win = frozenset(); count = 0
    for choices in product(*menus):
        count += 1
        strategy = {q: choices[q] for q in range(len(menus))}
        win = win | winning_for_strategy(strategy, Target, Safe)
    return win, count


def run_exhaustive():
    totals = {"labelled_games": 0, "strategies": 0, "formula_direct_mismatch": 0, "extracted_strategy_failure": 0, "core_subset_failure": 0, "strict_cases": 0}
    per_size=[]
    for n in (1,2,3):
        menu_pool = all_antichains(n)
        row = {"n":n,"menu_pool":len(menu_pool),"menu_tuples":0,"labelled_games":0,"strategies":0,"strict_cases":0}
        for menus in product(menu_pool, repeat=n):
            row["menu_tuples"] += 1
            for labels in product((0,1,2), repeat=n):
                Safe=frozenset(i for i,x in enumerate(labels) if x>=1)
                Target=frozenset(i for i,x in enumerate(labels) if x==2)
                W, outer=fixed_point_with_approximants(menus,Target,Safe)
                direct,sc=direct_union(menus,Target,Safe)
                K,core=core_region(menus,Target,Safe)
                row["labelled_games"]+=1; row["strategies"]+=sc
                if W != direct:
                    totals["formula_direct_mismatch"]+=1
                    return totals,per_size+[row],{"kind":"formula_direct","n":n,"labels":labels,"W":sorted(W),"direct":sorted(direct)}
                if not core <= W:
                    totals["core_subset_failure"]+=1
                    return totals,per_size+[row],{"kind":"core_subset","n":n}
                if core != W: row["strict_cases"]+=1
                strategy,ranks=extract_rank_strategy(menus,Target,Safe,W,outer)
                extracted_win=winning_for_strategy(strategy,Target,Safe)
                if not W <= extracted_win:
                    totals["extracted_strategy_failure"]+=1
                    return totals,per_size+[row],{"kind":"rank_strategy","n":n,"W":sorted(W),"extracted":sorted(extracted_win),"ranks":ranks}
        per_size.append(row)
        totals["labelled_games"]+=row["labelled_games"]
        totals["strategies"]+=row["strategies"]
        totals["strict_cases"]+=row["strict_cases"]
    return totals,per_size,None


def random_challenge(seed=1414, cases=3000):
    rng=random.Random(seed)
    totals={"seed":seed,"cases":0,"strategies":0,"mismatches":0,"rank_strategy_failures":0}
    for n in (4,5):
        subsets=[frozenset(i for i in range(n) if mask&(1<<i)) for mask in range(1,1<<n)]
        for _ in range(cases):
            menus=[]
            for q in range(n):
                rng.shuffle(subsets)
                chosen=[]
                goal=rng.randint(1,3)
                for s in subsets:
                    if any(s<=t or t<=s for t in chosen): continue
                    chosen.append(s)
                    if len(chosen)>=goal: break
                menus.append(tuple(chosen))
            menus=tuple(menus)
            labels=[rng.randrange(3) for _ in range(n)]
            Safe=frozenset(i for i,x in enumerate(labels) if x>=1)
            Target=frozenset(i for i,x in enumerate(labels) if x==2)
            W,outer=fixed_point_with_approximants(menus,Target,Safe)
            direct,sc=direct_union(menus,Target,Safe)
            totals["cases"]+=1; totals["strategies"]+=sc
            if W!=direct:
                totals["mismatches"]+=1; return totals,{"n":n,"W":sorted(W),"direct":sorted(direct)}
            strategy,_=extract_rank_strategy(menus,Target,Safe,W,outer)
            if not W <= winning_for_strategy(strategy,Target,Safe):
                totals["rank_strategy_failures"]+=1; return totals,{"n":n,"kind":"rank"}
    return totals,None


def main():
    t0=time.perf_counter()
    hashes={rel:{"expected":exp,"actual":digest(BASE/rel),"pass":digest(BASE/rel)==exp} for rel,exp in EXPECTED.items()}
    totals,per_size,failure=run_exhaustive()
    random_totals,random_failure=random_challenge()
    # Mandatory regression under this independent implementation.
    menus=((frozenset({0}),),(frozenset({0}),),(frozenset({0,1,2}),))
    Safe=frozenset({0,1,2}); Target=frozenset({0,2})
    W,outer=fixed_point_with_approximants(menus,Target,Safe)
    K,core=core_region(menus,Target,Safe)
    regression={"K":sorted(K),"W_core":sorted(core),"W_coB":sorted(W),"pass":K==frozenset({0}) and core==frozenset({0,1}) and W==frozenset({0,1,2})}
    overall=all(v["pass"] for v in hashes.values()) and failure is None and random_failure is None and regression["pass"]
    result={
        "review":"PMR-007 Round 14 V2 distinct direct-temporal rereview",
        "method":"set-valued mu/nu approximants + independently implemented Tarjan SCC semantics + rank-strategy extraction",
        "frozen_hashes":hashes,
        "exhaustive":{ "totals":totals,"per_size":per_size,"first_failure":failure},
        "larger_random":{ "totals":random_totals,"first_failure":random_failure},
        "r14_f01":regression,
        "elapsed_seconds":time.perf_counter()-t0,
        "overall":"PASS" if overall else "FAIL"
    }
    out=Path(__file__).with_name('PMR-007_FRONTIER_ROUND14_V2_FRESH_REREVIEW_RESULTS.json')
    out.write_text(json.dumps(result,indent=2)+"\n",encoding='utf-8')
    print(json.dumps(result,indent=2))
    return 0 if overall else 1

if __name__=='__main__':
    raise SystemExit(main())
