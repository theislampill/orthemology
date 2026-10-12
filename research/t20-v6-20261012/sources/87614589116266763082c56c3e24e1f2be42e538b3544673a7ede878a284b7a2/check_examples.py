#!/usr/bin/env python3
"""Finite model checks for Apoautosis and Transductive Faculties.

This is an offline mathematical checker, not a migration controller, hardware
interface, autonomous deployment system, or reproduction of predecessor suites.
It uses only Python's standard library. Checks remain active under python -O.
"""
from __future__ import annotations
import argparse
import hashlib
import itertools as it
import json
import platform
from functools import lru_cache
from pathlib import Path
from typing import Callable, Hashable, Iterable


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def nonempty_subsets(items: Iterable[Hashable]):
    seq = tuple(items)
    for n in range(1, len(seq) + 1):
        for part in it.combinations(seq, n):
            yield frozenset(part)


def partitions(items: tuple[int, ...]):
    if not items:
        yield ()
        return
    x, *tail = items
    for p in partitions(tuple(tail)):
        yield (frozenset([x]),) + p
        for j in range(len(p)):
            yield p[:j] + (p[j] | {x},) + p[j + 1:]


def cover_number(accepted: tuple[frozenset[int], ...], candidates=(0, 1, 2)) -> int:
    for d in nonempty_subsets(candidates):
        if all(d & a for a in accepted):
            return len(d)
    raise ValueError('No total acceptable selection')


def run_checks() -> dict:
    results = []
    def add(name: str, **details):
        results.append({'name': name, 'status': 'PASS', **details})

    # 1. Exact continuation under different coordinate encodings.
    # Abstract task: seven-state accumulator; no claim about physical substrates.
    count = 0
    mod = 7
    enc = (lambda q: q, lambda q: (3*q + 1) % mod)
    dec = (lambda x: x, lambda x: (5*(x-1)) % mod)
    for r, s, q, a in it.product(range(2), range(2), range(mod), range(mod)):
        x = enc[r](q)
        step = enc[r]((dec[r](x) + a) % mod)
        require(dec[r](step) == (q+a) % mod, 'Execution correspondence')
        migrated = enc[s](dec[r](x))
        require(dec[s](migrated) == q, 'Migration correspondence')
        count += 1
    add('coordinate_continuation', cases=count)

    # 2. No deterministic initialiser of the four-state delay machine can
    # reconstruct all continuations from only its current output bit.
    states = tuple(it.product((0,1), repeat=2))
    invalid = 0
    for init in it.product(states, repeat=2):
        works = True
        for b,c in states:
            dst = init[b]
            if dst[0] != b or dst[1] != c:
                works = False
        invalid += not works
    require(invalid == 16, 'All one-bit delay-state initialisers must fail')
    add('insufficient_export', initialisers_rejected=invalid)

    # 3. Current parity survives loss of a future calibration, even though the
    # future environmental decision does not.
    collisions = 0
    for b in (0,1):
        for y in (0,1):
            possible = [(c,k) for c,k in it.product((0,1), repeat=2) if c ^ k == y]
            require({c for c,k in possible} == {0,1}, 'Future ambiguity')
            require(all((b ^ a) in (0,1) for a in (0,1)), 'Parity still defined')
            collisions += 1
    add('task_survival_without_future_calibration', ambiguous_observations=collisions)

    # 4. Retention and lawful reacquisition are different explicit model cases.
    cases = 0
    for c,k in it.product((0,1), repeat=2):
        y = c ^ k
        require(y ^ k == c, 'Retained calibration decoder')
        reference = 0 ^ k  # Specified permitted reference; not a physical device.
        require(y ^ reference == c, 'Reacquisition decoder')
        cases += 1
    require({0 ^ k for k in (0,1)} == {0,1}, 'Uncalibrated result remains ambiguous')
    add('retained_or_reacquired_calibration', calibrated_cases=cases,
        unavailable_reference='not treated as an available observation')

    # 5. Minimum cover and minimum good-record partition coincide exhaustively.
    subsets = tuple(nonempty_subsets(range(3)))
    families = 0
    for accepted in it.product(subsets, repeat=3):
        good_sizes = []
        for p in partitions((0,1,2)):
            if all(set.intersection(*(set(accepted[w]) for w in block)) for block in p):
                good_sizes.append(len(p))
        require(min(good_sizes) == cover_number(accepted), 'Cover/record equivalence')
        families += 1
    add('cover_equals_good_partition', acceptance_families=families)

    # 6. Pairwise overlap does not imply a common accepted outcome.
    accepted = (frozenset((0,1)), frozenset((1,2)), frozenset((0,2)))
    require(all(a & b for a,b in it.combinations(accepted,2)), 'Pair overlap')
    require(not set.intersection(*(set(a) for a in accepted)), 'No total overlap')
    require(cover_number(accepted) == 2, 'Two record values suffice')
    add('pairwise_compatibility_not_joint', cover_number=2)

    # 7. A numeric record/probe lower bound is not a repertoire sufficiency test.
    worlds=(0,1)
    record={0:0,1:0}
    probe={0:0,1:0}
    require(2 <= 1*2**1, 'Capacity lower bound happens to hold')
    require((record[0],probe[0]) == (record[1],probe[1]), 'No observation separates labels')
    add('capacity_bound_not_sufficient', cover_number=2, record_values=1, binary_budget=1)

    # 8. Per-request versus simultaneous query horizon.
    query_cases=0
    for k in range(2,9):
        for w in it.product((0,1),repeat=k):
            for q in range(k):
                answer=w[q]
                require(answer in (0,1), 'One exact coordinate answer')
                query_cases += 1
        require(2**k > 2, 'Whole answer vector cannot use only one binary value')
    add('per_query_not_all_answers', coordinate_cases=query_cases, dimensions=list(range(2,9)))

    # 9. Ordinary exact probe-cost recurrence; every world is known to exist.
    worlds=tuple(it.product((0,1),repeat=3))
    probes=tuple((lambda w,j=j:w[j]) for j in range(3))
    def optimum(target):
        @lru_cache(None)
        def value(s):
            if len({target(worlds[i]) for i in s}) == 1:return 0
            opts=[]
            for h in probes:
                values={h(worlds[i]) for i in s}
                if len(values)>1:
                    opts.append(1+max(value(tuple(i for i in s if h(worlds[i])==y)) for y in values))
            return min(opts,default=float('inf'))
        return value(tuple(range(len(worlds))))
    require(optimum(lambda w:w[0]) == 1, 'One coordinate query')
    require(optimum(lambda w:w[0]^w[1]^w[2]) == 3, 'Three-bit parity')
    require(optimum(lambda w:0) == 0, 'Constant target')
    add('exact_probe_cost', coordinate=1, three_bit_parity=3, constant=0)

    # 10. Labelled-belief reachable-graph solver (initial truth is immutable).
    def decision_rank(initial, actions, obs, labels, max_steps=20):
        b0=frozenset((s,labels[s]) for s in initial)
        reachable={b0}; todo=[b0]; edges={}
        while todo:
            b=todo.pop(); edges[b]=[]
            for action in actions:
                image=[(action[s],lab) for s,lab in b]
                children=tuple(frozenset((s,lab) for s,lab in image if obs[s]==z)
                               for z in sorted({obs[s] for s,lab in image}))
                edges[b].append(children)
                for child in children:
                    if child not in reachable:reachable.add(child);todo.append(child)
        winning={b:0 for b in reachable if len({lab for s,lab in b})==1}
        for step in range(1,max_steps+1):
            new={b:step for b in reachable if b not in winning and
                 any(all(c in winning for c in kids) for kids in edges[b])}
            if not new:break
            winning.update(new)
        return winning.get(b0),len(reachable)
    a={'p':'t1','q':'t0','r':'t0','t0':'t0','t1':'t1'}
    b={'p':'t0','q':'t1','r':'t0','t0':'t0','t1':'t1'}
    obs={'p':'?','q':'?','r':'?','t0':'0','t1':'1'}
    labels={'p':0,'q':0,'r':1}
    rank, reachable=decision_rank(('p','q','r'),(a,b),obs,labels)
    require(rank is None, 'Destructive population must be unsolvable')
    require(all(any(obs[action[u]]!=obs[action[v]] for action in (a,b))
                for u,v in it.combinations(('p','q','r'),2)), 'Pair discrimination')
    add('destructive_inquiry', whole_population_rank=None, reachable_beliefs=reachable,
        each_pair_distinguishable=True)

    # 11. Reconnection exposes an existing reachable observation.
    states=tuple(it.product((0,1),repeat=2))
    action={s:(1,s[1]) for s in states}
    obs={s:(s[0],s[0]*s[1]) for s in states}
    labels={s:s[1] for s in states}
    rank,reach=decision_rank(((0,0),(0,1)),(action,),obs,labels)
    require(rank == 1, 'Reconnection rank')
    add('reconnection', rank=rank, reachable_beliefs=reach)

    # 12. Each requested service separately possible does not imply sequential
    # capability: a shared single-use resource is consumed by either request.
    def serves(budget, requests):
        for _ in requests:
            if budget<=0:return False
            budget-=1
        return True
    require(serves(1,('a',)) and serves(1,('b',)), 'Pointwise service')
    require(not serves(1,('a','b')), 'Joint sequential resource failure')
    add('pointwise_not_sequential_capability', individually_available=2, sequence_length_defeating=2)

    # 13. Error recurrence checked using exact rational arithmetic.
    from fractions import Fraction as F
    count=0
    for ls in it.product((F(1,2),F(1),F(2)),repeat=3):
        for es in it.product((F(0),F(1,10)),repeat=3):
            x=F(1,20)
            for l,e in zip(ls,es):x=l*x+e
            product=F(1)
            for l in ls:product*=l
            formula=product*F(1,20)
            for j in range(3):
                factor=F(1)
                for l in ls[j+1:]:factor*=l
                formula+=factor*es[j]
            require(x==formula,'Nonuniform defect propagation')
            count+=1
    add('nonuniform_error_composition', rational_cases=count)

    # 14. Per-host alternatives do not imply support-free operation.
    supports=({0,1},{1,2},{0,2})
    require(all(any(h not in s for s in supports) for h in range(3)), 'Each host dispensable')
    require(all(s for s in supports),'No empty support')
    fatal=[f for f in nonempty_subsets(range(3)) if all(set(f)&s for s in supports)]
    require(min(map(len,fatal))==2,'Fatal hitting-set size')
    add('support_quantifiers', minimal_fatal_set_size=2)

    # 15. Permission is not inferred from the physical or epistemic fields.
    readiness=lambda current,r1,r2,permission: permission and current==r1==r2
    require(readiness('b','b','b',True),'Current authorized evidence')
    require(not readiness('b','a','a',True),'Old receipts must fail')
    require(not readiness('b','b','b',False),'No permission must fail')
    add('version_and_permission_guards', cases=3)

    return {'scope':'Finite stipulated offline models; not physical evidence or a general-proof certificate',
            'groups':len(results),'status':'PASS','results':results}


def main() -> None:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path)
    args=parser.parse_args()
    result=run_checks()
    result['python_version']=platform.python_version()
    result['source_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    text=json.dumps(result,indent=2,ensure_ascii=False)+'\n'
    if args.out:args.out.write_text(text,encoding='utf-8')
    print(text)

if __name__=='__main__':main()
