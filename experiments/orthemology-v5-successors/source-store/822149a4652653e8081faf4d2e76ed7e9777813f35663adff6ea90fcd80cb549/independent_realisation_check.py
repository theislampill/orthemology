#!/usr/bin/env python3
"""Explicit-realisation audit, independent of the author's semantic reduction.
No state, world or power interpretation is asserted metaphysically possible.
"""
from pathlib import Path
from itertools import product
import hashlib,json
P=Path(__file__).resolve().parent
counts={'frames_and_states':0,'faithful_realisation_interpretations':0,
        'pointwise_equivalence_checks':0,'pointwise_violations':0,
        'coverage_equivalence_checks':0,'coverage_equivalence_violations':0,
        'object_local_composition_applications':0,'object_violations':0}

def mat(mask,n):return [[bool(mask & 1<<(i*n+j)) for j in range(n)] for i in range(n)]
def evaluate(R,S,A):
    n=len(S);exists=[s!=0 for s in S];U=[s==1 for s in S];received=[s==2 for s in S]
    possU=[any(R[v][u] and U[u] for u in range(n)) for v in range(n)]
    possE=[any(R[v][u] and exists[u] for u in range(n)) for v in range(n)]
    # A is an available productive manifestation witness, not a causal arrow
    # between worlds. It is explicit rather than substituted with implication.
    faithful=all(exists[v] or not A[v][u] or received[u] for v in range(n) for u in range(n))
    F=[exists[v] or not possU[v] or any(A[v][u] and U[u] for u in range(n)) for v in range(n)]
    reduced=[not possU[v] or exists[v] for v in range(n)]
    relevant=[v for v in range(n) if R[0][v]]
    coverage=all(exists[v] or possU[v] for v in relevant)
    necessity=all(exists[v] for v in relevant)
    reverse=all(R[v][0] for v in relevant)
    local_unreceivable=all(not received[v] for v in relevant)
    # Object premise explicitly requires accessible realisation of same g.
    O=all(exists[v] or not possE[v] or any(R[v][u] and A[v][u] and exists[u] for u in range(n)) for v in relevant)
    closure=all(not(R[0][v] and R[v][u]) or R[0][u] for v in range(n) for u in range(n))
    return locals()

for n in range(1,4):
    for tail in product(range(3),repeat=n-1):
        S=[1,*tail]
        # Enumerate every realisation relation satisfying causal fidelity.
        allowed=[(v,u) for v in range(n) for u in range(n) if S[v]!=0 or S[u]==2]
        realisations=[]
        for mask in range(1<<len(allowed)):
            A=[[False]*n for _ in range(n)]
            for k,(v,u) in enumerate(allowed): A[v][u]=bool(mask>>k&1)
            realisations.append(A)
        for rmask in range(1<<(n*n)):
            R=mat(rmask,n);counts['frames_and_states']+=1
            for A in realisations:
                x=evaluate(R,S,A);assert x['faithful']
                counts['faithful_realisation_interpretations']+=1
                counts['pointwise_equivalence_checks']+=n
                counts['pointwise_violations']+=sum(a!=b for a,b in zip(x['F'],x['reduced']))
                if x['coverage']:
                    counts['coverage_equivalence_checks']+=1
                    counts['coverage_equivalence_violations']+=all(x['F'][v] for v in x['relevant'])!=x['necessity']
                if x['reverse'] and x['O'] and x['local_unreceivable'] and x['closure']:
                    counts['object_local_composition_applications']+=1
                    counts['object_violations']+=not x['necessity']
assert counts['frames_and_states']==4658
assert not counts['pointwise_violations']
assert not counts['coverage_equivalence_violations']
assert not counts['object_violations']

# Deletion of causal-content fidelity breaks the exact-fact implication.
R=[[True,True],[True,True]];S=[1,0];A=[[False,False],[True,False]]
x=evaluate(R,S,A)
assert all(x['F']) and x['coverage'] and not x['necessity'] and not x['faithful']
fidelity_deletion={'R':R,'state':S,'realisation':A,'exact_fact_completeness':all(x['F']),
                   'possibility_coverage':x['coverage'],'causal_fidelity':x['faithful'],'necessity_g':x['necessity']}
# Delete possibility coverage, keeping fidelity and exact-fact completeness.
R=[[True,True],[False,True]];S=[1,0];A=[[False]*2 for _ in range(2)]
x=evaluate(R,S,A)
assert all(x['F']) and x['faithful'] and not x['necessity'] and not x['coverage']
coverage_deletion={'R':R,'state':S,'realisation':A,'exact_fact_completeness':all(x['F']),
                   'causal_fidelity':x['faithful'],'possibility_coverage':x['coverage'],'necessity_g':x['necessity']}
# Necessary existence from the exact-fact route does not make originlessness
# essential. The absent-bearer conditional is vacuous in both worlds here.
R=[[True,True],[True,True]];S=[1,2];A=[[False]*2 for _ in range(2)]
x=evaluate(R,S,A)
assert all(x['F']) and x['faithful'] and x['necessity'] and not x['local_unreceivable']
existence_not_origin={'R':R,'state':S,'necessity_g':True,'essential_unreceivability':False,'exact_fact_completeness':True}
# One invariant modal content and each-world unique ground: identity cannot be omitted.
contents={'a':{'q'},'b':{'q'}};E={'a':{'g'},'b':{'h'}};G={'a':{'q':'g'},'b':{'q':'h'}}
assert all('q' in contents[w] and G[w]['q'] in E[w] for w in contents)
assert not all('g' in E[w] for w in E)
# Distributed grounds can satisfy invariant content + fixed identity pointwise.
E2={'a':{'g','h'},'b':{'g','h'}};G2={w:{'q':'g','r':'h'} for w in E2}
assert all(G2[w][q] in E2[w] for w in E2 for q in ['q','r'])
assert not any(all(G2[w][q]==g for q in ['q','r']) for w in E2 for g in ['g','h'])
result={'scope':'Explicit finite semantic controls; no metaphysical realization claim',
 'counts':counts,'fidelity_deleted':fidelity_deletion,'coverage_deleted':coverage_deletion,'existence_not_essential_origin':existence_not_origin,
 'ground_identity_deleted':{'contents':{k:list(v) for k,v in contents.items()},'existence':{k:list(v) for k,v in E.items()},'ground_map':G},
 'distributed_grounds':G2,'result':'PASS','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(P/'INDEPENDENT_REALISATION_CHECK.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
