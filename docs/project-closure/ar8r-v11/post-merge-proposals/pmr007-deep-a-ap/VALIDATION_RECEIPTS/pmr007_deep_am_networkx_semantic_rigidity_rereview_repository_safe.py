#!/usr/bin/env python3
"""Repository-safe semantic-rigidity rereview core.

Source-custody hashes and locators are supplied separately by the proposal
manifest; this file contains only the finite automorphism/orbit verification.
"""
from __future__ import annotations
import itertools, json, random
from pathlib import Path
import networkx as nx

def graph(n,mask):
    G=nx.Graph(); G.add_nodes_from(range(n)); pairs=list(itertools.combinations(range(n),2))
    G.add_edges_from(e for j,e in enumerate(pairs) if (mask>>j)&1); return G

def auts(G):
    gm=nx.algorithms.isomorphism.GraphMatcher(G,G)
    return [tuple(m[i] for i in range(len(G))) for m in gm.isomorphisms_iter()]

def orbits(n,A):
    left=set(range(n)); out=[]
    while left:
        x=min(left); o={p[x] for p in A}; out.append(o); left-=o
    return out

def fixed(i,A): return all(all(i[p[x]]==i[x] for x in range(len(i))) for p in A)
def orbit_constant(i,O): return all(len({i[x] for x in o})==1 for o in O)
counts={'graphs':0,'interpretations':0,'mismatches':0,'random_cases':0,'random_mismatches':0}
for mask in range(1<<6):
    G=graph(4,mask); A=auts(G); O=orbits(4,A); counts['graphs']+=1
    for i in itertools.product(range(3),repeat=4):
        counts['interpretations']+=1
        counts['mismatches']+=fixed(i,A)!=orbit_constant(i,O)
rng=random.Random(20260805)
for _ in range(20000):
    G=graph(5,rng.randrange(1<<10)); A=auts(G); O=orbits(5,A); i=tuple(rng.randrange(4) for _ in range(5))
    counts['random_cases']+=1; counts['random_mismatches']+=fixed(i,A)!=orbit_constant(i,O)
res={'schema':'PMR007_DEEP_AM_REPOSITORY_SAFE_REREVIEW','counts':counts,'overall':'PASS' if counts['mismatches']==counts['random_mismatches']==0 else 'FAIL'}
Path(__file__).with_name(Path(__file__).stem+'_results.json').write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
