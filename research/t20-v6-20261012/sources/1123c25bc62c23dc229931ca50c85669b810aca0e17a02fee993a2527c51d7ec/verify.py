"""Exact finite controls; run from any directory with Python 3 standard library."""
from collections import deque
from itertools import product
from pathlib import Path
import hashlib, json, random
from probe import essential,closure,minimize,resets,frontier,output_for_catalogue

counts={}
def equivalent_partition(n,h,acts, witness=False):
    I=closure(n,h,acts)
    mask=sum(1<<i for i in I)
    allacts=resets(n)+tuple(acts)
    observed=minimize(h,allacts)
    expected=tuple(x&mask for x in range(1<<n))
    for x in range(1<<n):
        for y in range(x):
            assert (observed[x]==observed[y]) == (expected[x]==expected[y])
            if witness and expected[x]!=expected[y]:
                q=deque([(x,y,0)]);seen={(x,y)};found=None
                while q:
                    u,v,d=q.popleft()
                    if h[u]!=h[v]: found=d;break
                    for a in allacts:
                        pair=(a[u],a[v])
                        if pair not in seen: seen.add(pair);q.append((*pair,d+1))
                assert found is not None
                assert found <= n*n-1
                counts['independent_shortest_distinguishing_words']=counts.get('independent_shortest_distinguishing_words',0)+1
    assert len(set(observed))==1<<len(I)

# Exhaustive Boolean outputs on up to three bits, including constants and no bits.
for n in range(4):
    for h in product((0,1),repeat=1<<n):
        equivalent_partition(n,h,(),witness=n>0)
        counts['exhaustive_reset_boolean_outputs']=counts.get('exhaustive_reset_boolean_outputs',0)+1

# Every two-bit deterministic coupled action, every Boolean output.
for a in product(range(4),repeat=4):
    for h in product((0,1),repeat=4):
        equivalent_partition(2,h,(a,),witness=True)
        counts['exhaustive_two_bit_action_output_pairs']=counts.get('exhaustive_two_bit_action_output_pairs',0)+1

# General output alphabets; prices need not be Boolean.
for h in product((0,1,2),repeat=4):
    equivalent_partition(2,h,())
    counts['exhaustive_ternary_outputs']=counts.get('exhaustive_ternary_outputs',0)+1

# Diverse semantic dependency graphs, generated from randomly restricted inputs.
rng=random.Random(20261009)
for n in range(1,7):
    for case in range(250):
        def table():
            support=[i for i in range(n) if rng.randrange(2)]
            lookup=[rng.randrange(2) for _ in range(1<<len(support))]
            return tuple(lookup[sum(((x>>i)&1)<<j for j,i in enumerate(support))] for x in range(1<<n))
        h=table()
        acts=[]
        for _ in range(rng.randrange(1,5)):
            components=[table() for _ in range(n)]
            acts.append(tuple(sum(components[j][x]<<j for j in range(n)) for x in range(1<<n)))
        equivalent_partition(n,h,acts)
        counts['seeded_sparse_coupled_systems']=counts.get('seeded_sparse_coupled_systems',0)+1

# Entire families of positive catalogues: absent, zero cost, one cost on each support.
for n in range(4):
    for spec in product((None,0,1),repeat=1<<n):
        cat=tuple((s,k) for s,k in enumerate(spec) if k is not None)
        h=output_for_catalogue(n,cat)
        antichain=frontier(cat,0)
        union=0
        for s,k in antichain: union|=s
        assert essential(n,h)==frozenset(i for i in range(n) if union&(1<<i))
        assert output_for_catalogue(n,antichain)==h
        counts['exhaustive_positive_catalogues']=counts.get('exhaustive_positive_catalogues',0)+1

# Direct source-specific controls.
cat=((1,1),(2,1))
h=output_for_catalogue(2,cat)
assert frontier(cat,1)==frontier(cat,3)==((0,1),)
assert h[0]!=h[2]
assert len(set(minimize(h,(resets(2)[1],resets(2)[3]))))==2
assert len(set(minimize(h,resets(2))))==4
# Proof-availability only would incorrectly discard b's cheaper alternative.
pricecat=((0,2),(2,1));priceh=output_for_catalogue(2,pricecat)
assert essential(2,priceh)==frozenset({1})
assert essential(2,tuple(v<float('inf') for v in priceh))==frozenset()
# Hidden action dependency and a three-link propagation.
a=tuple((x&~1) if x&2 else x for x in range(4))
assert essential(2,(0,1,0,1))==frozenset({0})
assert closure(2,(0,1,0,1),(a,))==frozenset({0,1})
chain=tuple(tuple((x&~(1<<j)) if x&(1<<(j+1)) else x for x in range(16)) for j in range(3))
assert closure(4,tuple(x&1 for x in range(16)),chain)==frozenset(range(4))
# Syntactic support union over-retains b because of global dominance.
assert essential(2,output_for_catalogue(2,((1,1),(3,2))))==frozenset({0})
# A semantic signed guard cancels b.
assert essential(2,tuple(bool((x&1 and x&2) or (x&1 and not x&2)) for x in range(4)))==frozenset({0})
controls={
 'current_residual_frontier_survives_withdrawal':'REJECTED: empty versus {b} after clear a',
 'global_dominance_safe':'CONFIRMED across all catalogue valuations',
 'output_support_alone_suffices_with_coupled_guard':'REJECTED: b enters backward closure',
 'syntactic_dependency_union_is_exact':'REJECTED: globally dominated support and cancelled guard',
 'all_essential_bits_necessary_without_resets':'REJECTED: acquisition-only OR has two states',
 'availability_only_preserves_minimum_check_cost':'REJECTED: always-available expensive certificate versus optional cheaper one',
 'dependency_closure_requires_one_pass_only':'REJECTED: four-bit guard chain',
}
base=Path(__file__).resolve().parent
bindings={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in [base/'THEOREM.md',base/'probe.py',base/'verify.py',base/'tests/test_probe.py']}
result={'status':'PASS','scope':'Finite controls corroborate ordinary proofs; no Lean/kernel or actual-warrant certification.', 'counts':counts,'controls':controls,'sha256':bindings}
(base/'results/CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
