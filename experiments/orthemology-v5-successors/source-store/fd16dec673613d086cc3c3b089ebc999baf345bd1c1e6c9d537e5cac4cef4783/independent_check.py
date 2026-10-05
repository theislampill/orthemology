#!/usr/bin/env python3
"""Independent finite audit; no imports from the author's checker.
This is mathematical testing, not normative or metaphysical validation.
"""
import hashlib, itertools, json
from pathlib import Path
P = Path(__file__).resolve().parent

def strict_pareto(x, y):
    return x != y and x & y == x

def check_binary_spaces(n):
    U = range(2**n)
    count = {"contexts": n, "profile_sets": 0, "actual_assignments": 0,
             "R_P_sets": 0, "R_P_and_N_applications": 0,
             "violations": 0, "local_plus_N_bad_actual": 0}
    full = 2**n - 1
    for selection in range(1, 2**(2**n)):
        K = [x for x in U if selection >> x & 1]
        # Completely expanded target and profile quantifiers, separate from top test.
        R = all(any((y >> c & 1) and strict_pareto(x,y) for y in K)
                for x in K for c in range(n) if not (x >> c & 1))
        assert R == (full in K)
        local = all(any(x >> c & 1 for x in K) for c in range(n))
        count['profile_sets'] += 1
        count['R_P_sets'] += R
        for a in K:
            N = not any(strict_pareto(a,y) for y in K)
            good = a == full
            count['actual_assignments'] += 1
            count['R_P_and_N_applications'] += R and N
            count['violations'] += R and N and not good
            count['local_plus_N_bad_actual'] += local and N and not good
    return count

rows = [check_binary_spaces(n) for n in range(1,5)]
assert sum(r['profile_sets'] for r in rows) == 65808
assert sum(r['actual_assignments'] for r in rows) == 525348
assert sum(r['violations'] for r in rows) == 0

# More general relations over the four two-context profiles. In particular,
# unlike the author check, generic repair is not defined by Pareto dominance.
U=range(4)
edges=[(x,y) for x in U for y in U if x != y]
generic={'irreflexive_relations':0,'strict_partial_orders':0,
         'space_relation_pairs':0,'actual_assignments':0,
         'R_G_and_N_applications':0,'violations':0,
         'weaker_bad_profile_has_successor_and_N_violations':0}
for mask in range(1<<len(edges)):
    E={edge for j,edge in enumerate(edges) if mask>>j&1}
    is_transitive=all((x,z) in E for x,y in E for yy,z in E if y==yy)
    generic['irreflexive_relations']+=1
    generic['strict_partial_orders']+=is_transitive
    for selection in range(1,16):
        K=[x for x in U if selection>>x&1]
        Rg=all(any(y>>c&1 and (x,y) in E for y in K)
               for x in K for c in range(2) if not(x>>c&1))
        Rb=all(any((x,y) in E for y in K) for x in K if x!=3)
        assert not Rg or Rb
        generic['space_relation_pairs']+=1
        for a in K:
            N=not any((a,y) in E for y in K)
            generic['actual_assignments']+=1
            generic['R_G_and_N_applications']+=Rg and N
            generic['violations']+=Rg and N and a!=3
            generic['weaker_bad_profile_has_successor_and_N_violations']+=Rb and N and a!=3
assert generic['strict_partial_orders']==219
assert generic['violations']==0
assert generic['weaker_bad_profile_has_successor_and_N_violations']==0

# Genuine strict-comparison repair may incur a lesser loss. The two respects
# are fidelity and another stipulated pure good; this tests inference only.
K=[(0,1),(1,0)]
score=lambda p:2*p[0]+p[1]
Rg=all(any(y[0] and score(y)>score(x) for y in K) for x in K if not x[0])
Rp=all(any(y[0] and all(v>=u for u,v in zip(x,y)) and x!=y for y in K)
       for x in K if not x[0])
assert Rg and not Rp

# R and N are world-indexed: actual-world premises supply no other-world N.
worlds=[{'K':[(1,)],'actual':(1,)},{'K':[(0,),(1,)],'actual':(0,)}]
assert all(all(any(y[0] and y[0]>x[0] for y in w['K']) for x in w['K'] if not x[0]) for w in worlds)
assert not any(y[0]>1 for y in worlds[0]['K'])
assert any(y[0]>0 for y in worlds[1]['K'])

# Illustrations, not finite proof of the infinite assertion: repair S at i is
# S union {i}. It is finite, strictly contains S, and leaves old truths intact.
for bound in range(1,10):
    for k in range(bound+1):
        S=frozenset(range(k))
        i=bound
        assert i not in S
        T=S|{i}
        assert len(T)==len(S)+1 and S<T

result={'scope':'Mathematical controls only; no normative truth or metaphysical possibility inference',
        'binary_rows':rows,'generic_relation_check':generic,
        'R_G_without_R_P':{'profiles':K,'score':'2 * fidelity + lesser_good',
                           'R_G':Rg,'R_P':Rp,'nondominated_actual':[1,0]},
        'actual_not_essential_control':worlds,
        'infinite_argument':'For every finite S subset of N choose i outside S; S union {i} is an eligible strict successor. No finite S is maximal; no all-truthful profile exists.',
        'generic_proof_observation':'The contradiction needs only a strict eligible successor for each defective profile, not target repair or transitivity.',
        'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(P/'INDEPENDENT_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
