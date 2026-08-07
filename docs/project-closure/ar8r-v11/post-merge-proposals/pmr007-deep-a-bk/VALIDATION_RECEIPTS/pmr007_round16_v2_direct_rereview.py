#!/usr/bin/env python3
"""Distinct direct rereview for PMR-007 Round 16 V2."""
from __future__ import annotations
from copy import deepcopy
from itertools import combinations, product
from pathlib import Path
from typing import Any
import hashlib, json, time, yaml

BASE=Path(__file__).resolve().parents[1]
MODEL=BASE/'models/PMR007_ROUND16_VERSION_CUSTODY_AND_ELIGIBILITY_V2.yaml'
OUT=Path(__file__).with_name('PMR-007_FRONTIER_ROUND16_V2_FRESH_REREVIEW_RESULTS.json')
EXPECTED={
'PMR-007_FRONTIER_ROUND16_VERSION_CUSTODY_TRANSPORT_AND_TEMPORAL_ELIGIBILITY_V2.md':'599e9dd9595e26ae857a9a1e7c8a07306a2ec13f25c0c5a0500da544bc45f3ba',
'models/PMR007_ROUND16_VERSION_CUSTODY_AND_ELIGIBILITY_V2.yaml':'0f29fc7d081898901fd78af1ba1aaf379264988bd844b6cf13258551cfd13eef',
'checks/pmr007_round16_version_custody_check_v2.py':'739e8a918b403161249375b2159ce9a858676e9fda6df024252a0671abc4fd0f',
'checks/pmr007_round16_version_custody_check_v2_results.json':'3e2c5c67bf6d81ff9df2239a1e78629e2b820ff4aaa50ddb4986063ba6c5b96a',
'audits/PMR-007_FRONTIER_ROUND16_V1_COLD_AUDIT.md':'575d1199348bbf1d774be2a255f73cade458733100c5f8e4a2c7d85814d611e2',
'repairs/PMR-007_FRONTIER_ROUND16_REPAIR_LOG.md':'7e3b6c2de058a44f36001bb0c485dc2541eb4c332184d7fe01706a758f9f677e',
}
EVIDENCE={
'PRIVATE_EVIDENCE_REFERENCE:AR8R_AR2_AR3_COLLECTIVE_BACKBONE_RECONCILIATION.md':'fb22d822c53259cac6045df41ede3addcfd6089e5196dae885394ece49e0d7d7',
'PRIVATE_EVIDENCE_REFERENCE:PMR_AGCOM_01_CANDIDATE.md':'d2a4d6a7a20cf32546da0b683266e7c3497aaecaa320f301b934018c3fd907a7',
'PRIVATE_EVIDENCE_REFERENCE:PMR_AGCOM_02_CANDIDATE_V2.md':'98b451468eaa225b1f23427c70007bd7a92ceab4fa1440afce0637248d833a9e',
'PRIVATE_EVIDENCE_REFERENCE:PMR_AGCOM_06_CANDIDATE_V2.md':'5b8d1b411c7a5aea03e0bd0f836d0d68f9f698f3429125cd5e82fd01c8163a7c',
'PRIVATE_EVIDENCE_REFERENCE:PMR_LANG_01_CANDIDATE_V2.md':'f9d6820ef93ef276a45dc3d8176fae70b659063b6f8e8d6d9021ee2917984232',
'PRIVATE_EVIDENCE_REFERENCE:PMR_LANG_02_CANDIDATE_V2.md':'236d570a5bc1a149008cd20ae8493d53afd609a8585e01ffb46ae4df863b3af2',
}

def digest(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def direct_path(path):
    c=path['initial_certificate']; state=(c['version'],c['claim'],c['root'],frozenset(c['nodes']),frozenset(map(tuple,c['dependency_edges'])),frozenset(c['discharged_obligations']))
    prev_redelegable=True; trace=[]
    for i,e in enumerate(path['edges']):
        version,claim,root,nodes,deps,discharged=state
        if (e['input_version'],e['input_claim'],e['input_root'])!=(version,claim,root): return False,'boundary-mismatch',trace
        if i and not prev_redelegable: return False,'nonredelegable-authority',trace
        if frozenset(e['node_map'])!=nodes or frozenset(map(tuple,e['input_dependency_edges']))!=deps: return False,'reason-dag-boundary-mismatch',trace
        mapped=frozenset((e['node_map'][a],e['node_map'][b]) for a,b in deps); outdeps=frozenset(map(tuple,e['output_dependency_edges'])); outnodes=frozenset(e['node_map'].values())
        if not mapped<=outdeps or any(a not in outnodes or b not in outnodes for a,b in outdeps): return False,'dependency-output-failure',trace
        preserved=frozenset(e['preserved_obligations'])
        if not preserved<=discharged: return False,'preserved-obligation-not-discharged',trace
        newdis=preserved|frozenset(e['revalidated_obligations'])
        if not frozenset(e['target_required_obligations'])<=newdis: return False,'target-obligation-open',trace
        if not e['semantic_square_commutes'] or not e['authority_delegation_valid'] or e['invalidators_open'] or e['input_root']!=e['output_root']: return False,'semantic-authority-root-or-invalidator-failure',trace
        state=(e['output_version'],e['output_claim'],e['output_root'],outnodes,outdeps,newdis); prev_redelegable=e['delegation_redelegable']; trace.append(e['edge_id'])
    ex=path['expected_final']; ok=state[0]==ex['version'] and state[1]==ex['claim'] and state[2]==ex['root'] and frozenset(ex['required_obligations'])<=state[5]
    return ok,None if ok else 'final-contract-failure',trace

def mutate(obj:Any,path:str,value:Any):
    cur=obj; ps=path.split('.')
    for p in ps[:-1]: cur=cur[int(p)] if isinstance(cur,list) else cur[p]
    if isinstance(cur,list): cur[int(ps[-1])]=value
    else: cur[ps[-1]]=value

def all_strategies(menus):
    states=sorted(menus)
    for choice in product(*(menus[q] for q in states)):
        yield {q:frozenset(a['successors']) for q,a in zip(states,choice)}

def reach(adj,start):
    seen={start}; todo=[start]
    while todo:
        q=todo.pop()
        for r in adj[q]:
            if r not in seen: seen.add(r); todo.append(r)
    return seen

def sccs(adj):
    idx=0; stack=[]; on=set(); ind={}; low={}; out=[]
    def visit(v):
        nonlocal idx
        ind[v]=low[v]=idx; idx+=1; stack.append(v); on.add(v)
        for w in adj[v]:
            if w not in ind: visit(w); low[v]=min(low[v],low[w])
            elif w in on: low[v]=min(low[v],ind[w])
        if low[v]==ind[v]:
            c=set()
            while True:
                w=stack.pop(); on.remove(w); c.add(w)
                if w==v: break
            out.append(c)
    for v in adj:
        if v not in ind: visit(v)
    return out

def direct_regions(menus,Safe,Target):
    K=set(); strategies=list(all_strategies(menus))
    for adj in strategies:
        for q in Target:
            if reach(adj,q)<=Target: K.add(q)
    Wc=set(); Wb=set(); Bad=Safe-Target
    for adj in strategies:
        cyc=set()
        badcyc=set()
        for c in sccs(adj):
            cyclic=len(c)>1 or any(v in adj[v] for v in c)
            if cyclic: cyc|=c
            if cyclic and c&Bad: badcyc|=(c&Bad)
        for q in adj:
            R=reach(adj,q)
            if q not in Safe or not R<=Safe: continue
            if not ((R&cyc)-K) and all(not (k in R) or adj[k]<=K for k in K): Wc.add(q)
            if not R&badcyc: Wb.add(q)
    return K,Wc,Wb,len(strategies)

def menu_pool(n):
    succ=[frozenset(i for i in range(n) if m&(1<<i)) for m in range(1,1<<n)]; out=[]
    for r in range(1,len(succ)+1):
        for c in combinations(succ,r): out.append([{'action_id':f'a{i}','successors':sorted(s)} for i,s in enumerate(c)])
    return out

def submenus(menu):
    return [[menu[i] for i in range(len(menu)) if m&(1<<i)] for m in range(1,1<<len(menu))]

def direct_monotonicity():
    totals={'games':0,'pairs':0,'strategy_enumerations':0,'failures':0}; first=None
    for n in (1,2):
        pool=menu_pool(n)
        for ft in product(pool,repeat=n):
            full={q:ft[q] for q in range(n)}; subs=[submenus(ft[q]) for q in range(n)]
            for labels in product((0,1,2),repeat=n):
                Safe={q for q,x in enumerate(labels) if x>=1}; Target={q for q,x in enumerate(labels) if x==2}; K,Wc,Wb,sc=direct_regions(full,Safe,Target); totals['games']+=1; totals['strategy_enumerations']+=sc
                for rt in product(*subs):
                    r={q:rt[q] for q in range(n)}; K2,Wc2,Wb2,sc2=direct_regions(r,Safe,Target); totals['pairs']+=1; totals['strategy_enumerations']+=sc2
                    if not(K2<=K and Wc2<=Wc and Wb2<=Wb): totals['failures']+=1; first={'n':n,'labels':labels}; return totals,first
    return totals,first

def temporal(doc):
    x=doc['temporal_eligibility_witness']; full={**x['common_actions'],**x['version_v1_actions']}; restricted={**x['common_actions'],**x['version_v2_actions']}; Safe=set(x['safe_states']); Target=set(x['target_states']); _,c1,b1,_=direct_regions(full,Safe,Target); _,c2,b2,_=direct_regions(restricted,Safe,Target)
    return {'v1':{'W_core':sorted(c1),'W_coB':sorted(b1)},'v2':{'W_core':sorted(c2),'W_coB':sorted(b2)},'pass':sorted(c1)==x['expected']['v1']['W_core'] and sorted(b1)==x['expected']['v1']['W_coB'] and sorted(c2)==x['expected']['v2']['W_core'] and sorted(b2)==x['expected']['v2']['W_coB']}

def main():
    t=time.perf_counter(); hashes={r:{'expected':h,'actual':digest(BASE/r),'pass':digest(BASE/r)==h} for r,h in EXPECTED.items()}; evidence={p:{'expected':h,'actual':digest(p),'pass':digest(p)==h} for p,h in EVIDENCE.items()}; doc=yaml.safe_load(MODEL.read_text()); pos=direct_path(doc['positive_transport_path']); fixtures={}
    for f in doc['transport_path_negative_fixtures']:
        d=deepcopy(doc)
        for p,v in f['mutation'].items(): mutate(d,p,v)
        got=direct_path(d['positive_transport_path']); fixtures[f['fixture_id']]={'reason':got[1],'expected':f['expected_error'],'pass':got[0] is False and got[1]==f['expected_error']}
    mono,fail=direct_monotonicity(); tw=temporal(doc); primary=json.loads((BASE/'checks/pmr007_round16_version_custody_check_v2_results.json').read_text())
    overall=all(x['pass'] for x in hashes.values()) and all(x['pass'] for x in evidence.values()) and pos[0] and all(x['pass'] for x in fixtures.values()) and fail is None and tw['pass'] and primary['overall']=='PASS'
    result={'review':'PMR-007 Round 16 V2 distinct direct-semantic rereview','review_relation':'same-model procedural rereview with separate implementation; not external human or independent model-lineage review','frozen_hashes':hashes,'evidence_hashes':evidence,'positive_path':{'valid':pos[0],'reason':pos[1],'edge_trace':pos[2]},'repair_regressions':fixtures,'direct_strategy_monotonicity':{'totals':mono,'first_failure':fail},'temporal_reopening':tw,'primary_frozen_result':primary['overall'],'authority_ceiling':'post-merge scoped integration/application; original RP-T2/RP-T40 bytes unavailable here; no source truth, runtime completeness, general novelty, or adoption','elapsed_seconds':time.perf_counter()-t,'overall':'PASS' if overall else 'FAIL'}; OUT.write_text(json.dumps(result,indent=2)+'\n'); print(json.dumps(result,indent=2)); return 0 if overall else 1
if __name__=='__main__': raise SystemExit(main())
