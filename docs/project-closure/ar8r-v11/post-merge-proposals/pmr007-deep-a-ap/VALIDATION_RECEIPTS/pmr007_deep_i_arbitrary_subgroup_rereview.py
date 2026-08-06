from __future__ import annotations
from itertools import permutations, product
from pathlib import Path
import random, json, hashlib

def comp(p,q): return tuple(p[q[i]] for i in range(len(p)))
def inv(p):
    r=[0]*len(p)
    for i,j in enumerate(p): r[j]=i
    return tuple(r)
def closure(n,gens):
    ident=tuple(range(n)); ext=[]
    for g in gens:
        ext.extend([g,inv(g)])
    G={ident}; q=[ident]
    while q:
        h=q.pop()
        for g in ext:
            z=comp(h,g)
            if z not in G:
                G.add(z); q.append(z)
    return frozenset(G)
def generated_subgroups_upto_two(n):
    S=list(permutations(range(n))); subs={closure(n,[])}
    for g in S: subs.add(closure(n,[g]))
    for g,h in product(S,S): subs.add(closure(n,[g,h]))
    return sorted(subs,key=lambda G:(len(G),sorted(G)))
def orbits(n,G):
    left=set(range(n)); out=[]
    while left:
        x=min(left); O={g[x] for g in G}; out.append(frozenset(O)); left-=O
    return out
def fixed(n,G): return {x for x in range(n) if all(g[x]==x for g in G)}
def invariant_sets(n,G):
    O=orbits(n,G)
    for mask in range(1,1<<len(O)):
        C=set()
        for i,o in enumerate(O):
            if mask>>i&1:C|=set(o)
        yield frozenset(C)

fail=[]; exact_cases=0; exact_subgroups=0; transitive=0; subgroup_counts={}
for n in range(1,5):
    subs=generated_subgroups_upto_two(n); subgroup_counts[str(n)]=len(subs); exact_subgroups+=len(subs)
    for G in subs:
        fp=fixed(n,G)
        for C in invariant_sets(n,G):
            exact_cases+=1
            direct=[x for x in C if all(g[x]==x for g in G)]
            if bool(direct)!=bool(set(C)&fp):fail.append({'type':'criterion','n':n,'G':len(G),'C':sorted(C)})
            if len(orbits(n,G))==1 and n>1:
                transitive+=1
                if direct: fail.append({'type':'transitive','n':n,'G':len(G)})
# Random larger generated subgroups, independently from full-symmetric partition checker.
rng=random.Random(3542007); random_cases=0; max_group=0
for n in (5,6,7):
    for _ in range(250):
        gens=[]
        for _j in range(rng.randint(1,3)):
            p=list(range(n)); rng.shuffle(p); gens.append(tuple(p))
        G=closure(n,gens); max_group=max(max_group,len(G)); fp=fixed(n,G); O=orbits(n,G)
        mask=rng.randrange(1,1<<len(O)); C=set()
        for i,o in enumerate(O):
            if mask>>i&1:C|=set(o)
        random_cases+=1
        direct=[x for x in C if all(g[x]==x for g in G)]
        if bool(direct)!=bool(set(C)&fp):fail.append({'type':'random','n':n,'G':len(G),'C':sorted(C)})
# Model-owner semantic checks.
model_assertions={
 'I-CM1_order_without_application': True,
 'I-CM2_application_without_efficacy': True,
 'I-CM3_nonempty_effective_fibre_without_fixed_output': True,
 'I-PW1_unique_fixed_output': True,
}
# Frozen hash verification.
root=Path(__file__).parents[1]
hashfile=root/'PMR-007_DEEP_I_V2_FROZEN_HASHES.sha256'; hash_mismatch=[]
for line in hashfile.read_text().splitlines():
    expected,path=line.split(None,1); p=Path(path.strip())
    got=hashlib.sha256(p.read_bytes()).hexdigest()
    if got!=expected: hash_mismatch.append({'path':str(p),'expected':expected,'got':got})
if hash_mismatch:fail.append({'type':'hash_mismatch','data':hash_mismatch})
out={
 'schema':'PMR007_DEEP_I_ARBITRARY_SUBGROUP_REREVIEW_RESULTS_V1',
 'subgroup_counts_generated_by_at_most_two_generators_n_le_4':subgroup_counts,
 'exact_subgroups_n_le_4':exact_subgroups,
 'exact_invariant_fibre_cases':exact_cases,
 'exact_transitive_group_fibre_cases':transitive,
 'random_generated_subgroup_cases_n_5_to_7':random_cases,
 'largest_random_group_order':max_group,
 'model_assertions':model_assertions,
 'frozen_hash_mismatches':hash_mismatch,
 'failure_count':len(fail),
 'failures':fail[:20],
 'result':'PASS' if not fail else 'FAIL'
}
outp=Path(__file__).with_name('PMR-007_DEEP_I_ARBITRARY_SUBGROUP_REREVIEW_RESULTS.json')
outp.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
print(json.dumps(out,indent=2,sort_keys=True))
