#!/usr/bin/env python3
from __future__ import annotations
from itertools import combinations
from random import Random
from pathlib import Path
import json,yaml

ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/'models/PMR007_ROUND20_PROVENANCE_RESILIENT_RESTORATIVE_CUTSETS_V2.yaml'
OUT=Path(__file__).with_name('pmr007_round20_prrc_primary_check_v2_results.json')

def subsets(xs):
    xs=tuple(xs)
    for r in range(len(xs)+1):
        for c in combinations(xs,r): yield frozenset(c)

def tau(edges, roots):
    es={frozenset(e) for e in edges}
    if not es: return 0
    return min(len(c) for c in subsets(roots) if all(c&e for e in es))

def kappa(path_edges, roots): return min(tau(h,roots) for h in path_edges)
def robust(path_edges,roots,f):
    return all(all(any(not(c&e) for e in h) for h in path_edges)
               for c in subsets(roots) if len(c)<=f)

def compatible_cover(paths, blockers, incompatibilities):
    ids=[a['id'] for a in blockers]
    bad={frozenset(x) for x in incompatibilities}
    byid={a['id']:a for a in blockers}
    for chosen in subsets(ids):
        if any(pair<=chosen for pair in bad): continue
        if all(any(byid[i].get('path')==p for i in chosen) for p in paths): return True
    return False

def dynamic_after(actions, initial_paths):
    active=set(initial_paths)
    for a in actions:
        if a.get('path') in active: active.remove(a['path'])
        if a.get('creates_path'): active.add(a['creates_path'])
    return active

def commit_then_adversary(blockers,roots,f):
    # robust only if some commitment survives every allowed corruption
    for a in blockers:
        dep=set(a['dep'])
        if all(not(dep & set(c)) for c in subsets(roots) if len(c)<=f): return True
    return False

def hypergraph_exhaustion():
    systems=cases=fail=0
    for n in range(1,5):
        roots=tuple(range(n)); edges=[s for s in subsets(roots) if s]
        for mask in range(1<<len(edges)):
            H=[edges[i] for i in range(len(edges)) if mask>>i&1]
            systems+=1; kval=kappa([H],roots)
            for f in range(n+1):
                cases+=1
                if robust([H],roots,f)!=(kval>f): fail+=1
    return systems,cases,fail

def random_multi_and_monotone():
    rng=Random(20072026); systems=criteria=0; fail=[]
    mono={k:0 for k in ('duplicate','add','delete','contract')}
    for _ in range(40000):
        n=rng.randint(1,7); roots=tuple(range(n)); pes=[]
        for _p in range(rng.randint(1,5)):
            H=[]
            for _a in range(rng.randint(0,8)):
                e=frozenset(r for r in roots if rng.random()<.4)
                H.append(e or frozenset([rng.choice(roots)]))
            pes.append(H)
        kval=kappa(pes,roots); systems+=1
        for f in range(n+1):
            criteria+=1
            if robust(pes,roots,f)!=(kval>f): fail.append('criterion')
        pi=rng.randrange(len(pes)); H=pes[pi]
        if H:
            base=tau(H,roots); e=rng.choice(H)
            if tau(H+[e],roots)!=base: fail.append('duplicate')
            mono['duplicate']+=1
            all_edges=[x for x in subsets(roots) if x]
            add=rng.choice(all_edges)
            if tau(H+[add],roots)<base: fail.append('add')
            mono['add']+=1
            j=rng.randrange(len(H)); hd=H[:j]+H[j+1:]
            if tau(hd,roots)>base: fail.append('delete')
            mono['delete']+=1
            size=rng.randint(1,n)
            q={r:rng.randrange(size) for r in roots}
            hq=[frozenset(q[x] for x in e) for e in H]
            rq=tuple(sorted(set(q.values())))
            if tau(hq,rq)>base: fail.append('contract')
            mono['contract']+=1
    return systems,criteria,mono,fail[:20]

def controls(model):
    cms={c['id']:c for c in model['countermodels']}; out={}
    def pk(c):
        ps=c.get('paths') or c.get('registered_paths'); roots=c.get('roots'); bs=c.get('blockers',[])
        return kappa([[frozenset(a['dep']) for a in bs if a.get('path')==p] for p in ps],roots)
    for cid in ('R20-CM1','R20-CM2','R20-CM3','R20-CM4','R20-CM5','R20-CM7','R20-CM8'):
        c=cms[cid]; got=pk(c); exp=c.get('expected_kappa',c.get('expected_registered_kappa'))
        out[cid]={'got':got,'expected':exp,'pass':got==exp}
    c=cms['R20-CM3']
    out['incompatible_execution']={'support_robust':robust([[frozenset(['r1'])],[frozenset(['r2'])]],['r1','r2'],0),
        'compatible_cover':compatible_cover(c['paths'],c['blockers'],c['incompatibilities'])}
    out['incompatible_execution']['pass']=out['incompatible_execution']=={'support_robust':True,'compatible_cover':False}
    c=cms['R20-CM4']; remaining=dynamic_after(c['blockers'],c['registered_paths'])
    out['dynamic_rerouting']={'remaining_paths':sorted(remaining),'pass':remaining=={'p1'}}
    c=cms['R20-CM5']; static=robust([[frozenset(a['dep']) for a in c['blockers']]],c['roots'],1)
    adapt=commit_then_adversary(c['blockers'],c['roots'],1)
    out['adaptive_after_commitment']={'static':static,'commit_robust':adapt,'pass':static and not adapt}
    c=cms['R20-CM6']; apparent=tau(map(frozenset,c['displayed_supports']),c['displayed_roots'])
    actual=[frozenset(c['display_to_actual'][x] for x in s) for s in c['displayed_supports']]
    actualk=tau(actual,c['actual_roots'])
    out['unauthenticated_alias']={'apparent':apparent,'actual':actualk,'pass':apparent==2 and actualk==1}
    c=cms['R20-CM7']; reg=robust([[frozenset(a['dep']) for a in c['blockers']]],c['roots'],1)
    actual_paths=c['registered_paths']+c['omitted_paths']; pes=[]
    for p in actual_paths: pes.append([frozenset(a['dep']) for a in c['blockers'] if a['path']==p])
    actual_ok=robust(pes,c['roots'],1)
    out['partial_registry']={'registered':reg,'operative':actual_ok,'pass':reg and not actual_ok}
    c=cms['R20-CM8']; pes=[]
    for p in c['paths']: pes.append([frozenset(a['dep']) for a in c['blockers'] if a['path']==p])
    pos=robust(pes,c['roots'],c['corruption_budget'])
    out['positive_construction']={'kappa':kappa(pes,c['roots']),'robust':pos,'pass':pos and kappa(pes,c['roots'])==3}
    return out

def main():
    model=yaml.safe_load(MODEL.read_text())
    s,c,f=hypergraph_exhaustion(); rs,rc,mono,mfail=random_multi_and_monotone(); ctr=controls(model)
    result={'schema':'PMR007_ROUND20_PRRC_PRIMARY_CHECK_RESULTS_V2','model':MODEL.name,
      'exhaustive_single_path_hypergraphs':s,'exhaustive_criterion_cases':c,'exhaustive_failures':f,
      'random_multi_path_systems':rs,'random_multi_path_criterion_cases':rc,
      'monotonicity_cases':mono,'random_or_monotonicity_failures':mfail,'stronger_reading_controls':ctr}
    result['overall']='PASS' if f==0 and not mfail and all(v['pass'] for v in ctr.values()) else 'FAIL'
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(result['overall']!='PASS')
if __name__=='__main__': main()
