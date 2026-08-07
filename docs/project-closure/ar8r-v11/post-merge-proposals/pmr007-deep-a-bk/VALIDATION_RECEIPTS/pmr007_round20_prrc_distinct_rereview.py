#!/usr/bin/env python3
from pathlib import Path
from itertools import product
import hashlib,json,yaml,random
ROOT=Path(__file__).resolve().parents[1]
HASHES=ROOT/'PMR-007_FRONTIER_ROUND20_V2_FROZEN_HASHES.sha256'
MODEL=ROOT/'models/PMR007_ROUND20_PROVENANCE_RESILIENT_RESTORATIVE_CUTSETS_V2.yaml'
OUT=Path(__file__).with_name('PMR-007_FRONTIER_ROUND20_V2_DISTINCT_REREVIEW_RESULTS.json')

def pop(x): return x.bit_count()
def edge_masks(n): return list(range(1,1<<n))
def tau_masks(H,n):
    if not H:return 0
    return min(pop(c) for c in range(1<<n) if all(c&e for e in H))
def failure_margin(pathHs,n):
    # least corruption mask that uncovers at least one path
    for size in range(n+1):
        for c in range(1<<n):
            if pop(c)!=size: continue
            if any(all(c&e for e in H) for H in pathHs): return size
    raise AssertionError
def check_hashes():
    bad=[];count=0
    for line in HASHES.read_text().splitlines():
        if not line.strip(): continue
        h,rel=line.split(None,1); rel=rel.strip(); count+=1
        got=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()
        if got!=h: bad.append({'path':rel,'expected':h,'got':got})
    return count,bad

def exhaustive_single():
    fams=cases=fail=0
    for n in range(1,5):
        es=edge_masks(n)
        for fm in range(1<<len(es)):
            H=[es[i] for i in range(len(es)) if fm>>i&1]
            fams+=1
            a=tau_masks(H,n); b=failure_margin([H],n); cases+=1
            if a!=b: fail+=1
    return fams,cases,fail

def exhaustive_two_path_n3():
    n=3; es=edge_masks(n)
    hs=[]
    for fm in range(1<<len(es)):
        hs.append([es[i] for i in range(len(es)) if fm>>i&1])
    count=fail=0
    for H1 in hs:
        for H2 in hs:
            count+=1
            k=min(tau_masks(H1,n),tau_masks(H2,n))
            d=failure_margin([H1,H2],n)
            if k!=d: fail+=1
    return count,fail

def contraction_exhaustive():
    cases=fail=0
    for n in range(1,5):
        es=edge_masks(n)
        # sample all families for n<=3; deterministic 5000 for n=4
        fam_masks=range(1<<len(es)) if n<=3 else range(0,1<<len(es),7)
        for fm in fam_masks:
            H=[es[i] for i in range(len(es)) if fm>>i&1]
            base=tau_masks(H,n)
            for k in range(1,n+1):
                for q in product(range(k),repeat=n):
                    Hq=[]
                    for e in H:
                        me=0
                        for r in range(n):
                            if e>>r&1: me|=1<<q[r]
                        Hq.append(me)
                    got=tau_masks(Hq,k); cases+=1
                    if got>base: fail+=1
    return cases,fail

def independent_controls(model):
    cms={c['id']:c for c in model['countermodels']}; out={}
    # Incompatibility: enumerate selections directly from YAML
    c=cms['R20-CM3']; bs=c['blockers']; ids=[a['id'] for a in bs]
    found=False
    for mask in range(1<<len(ids)):
        chosen={ids[i] for i in range(len(ids)) if mask>>i&1}
        if any(set(pair)<=chosen for pair in c['incompatibilities']): continue
        if all(any(a['id'] in chosen and a['path']==p for a in bs) for p in c['paths']): found=True
    out['incompatible_cover_absent']=not found
    # Dynamic update from YAML
    c=cms['R20-CM4']; active=set(c['registered_paths'])
    for a in c['blockers']:
        active.discard(a['path']); active.add(a['creates_path'])
    out['dynamic_new_path_survives']=active==set(c['omitted_created_paths'])
    # Adaptive commitment: every blocker has a <=1 corruption that intersects dep
    c=cms['R20-CM5']; out['adaptive_defeats_every_commitment']=all(len(a['dep'])>0 for a in c['blockers'])
    # Partial registry direct actual family
    c=cms['R20-CM7']; out['omitted_path_has_no_blocker']=all(not any(a['path']==p for a in c['blockers']) for p in c['omitted_paths'])
    # Alias
    c=cms['R20-CM6']; out['alias_collapses_two_to_one']=len(set(c['display_to_actual'].values()))==1 and len(c['displayed_roots'])==2
    # Positive direct corruption enumeration
    c=cms['R20-CM8']; roots=c['roots']; rid={r:i for i,r in enumerate(roots)}; pathHs=[]
    for p in c['paths']:
        H=[]
        for a in c['blockers']:
            if a['path']==p:
                m=0
                for r in a['dep']:m|=1<<rid[r]
                H.append(m)
        pathHs.append(H)
    out['positive_margin']=failure_margin(pathHs,len(roots))==3
    return out

def random_multimodel():
    rng=random.Random(770020); cases=fail=0
    for _ in range(50000):
        n=rng.randint(1,9); es=edge_masks(n); pathHs=[]
        for _p in range(rng.randint(1,6)):
            H=[rng.choice(es) for _ in range(rng.randint(0,10))]
            pathHs.append(H)
        k=min(tau_masks(H,n) for H in pathHs); d=failure_margin(pathHs,n); cases+=1
        if k!=d:fail+=1
    return cases,fail

def main():
    hc,hbad=check_hashes(); model=yaml.safe_load(MODEL.read_text())
    sf,sc,sfail=exhaustive_single(); tp,tpf=exhaustive_two_path_n3(); cc,cf=contraction_exhaustive(); rc,rf=random_multimodel(); controls=independent_controls(model)
    result={'schema':'PMR007_ROUND20_DISTINCT_REREVIEW_RESULTS_V1','frozen_files_checked':hc,'hash_mismatches':hbad,
      'single_path_families':sf,'single_path_cases':sc,'single_path_failures':sfail,
      'two_path_three_root_systems':tp,'two_path_failures':tpf,
      'root_contraction_cases':cc,'root_contraction_failures':cf,
      'random_multi_path_cases':rc,'random_multi_path_failures':rf,
      'independent_stronger_reading_controls':controls}
    result['overall']='PASS' if not hbad and not(sfail or tpf or cf or rf) and all(controls.values()) else 'FAIL'
    OUT.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n'); print(json.dumps(result,indent=2,sort_keys=True))
    raise SystemExit(result['overall']!='PASS')
if __name__=='__main__':main()
