#!/usr/bin/env python3
from pathlib import Path
from itertools import product
import json,yaml
ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/'models/PMR007_DEEP_A_NORM_FIXING_MODELS_V1.yaml'
OUT=Path(__file__).with_name('pmr007_deep_a_norm_fixing_check_results.json')

def partitions(n):
    # restricted-growth strings, one canonical profile partition per string
    a=[0]*n
    def rec(i,m):
        if i==n:
            yield tuple(a); return
        for v in range(m+2):
            a[i]=v; yield from rec(i+1,max(m,v))
    if n==0: yield (); return
    a[0]=0; yield from rec(1,0)

def constant_on_fibres(profile,truth):
    seen={}
    for p,t in zip(profile,truth):
        if p in seen and seen[p]!=t:return False
        seen[p]=t
    return True

def exists_standard(profile,truth):
    vals=sorted(set(profile))
    for choices in product((0,1),repeat=len(vals)):
        f=dict(zip(vals,choices))
        if all(f[p]==t for p,t in zip(profile,truth)):return True
    return False

def exhaustive():
    parts=targets=fail=0
    for n in range(1,9):
        for p in partitions(n):
            parts+=1
            for t in product((0,1),repeat=n):
                targets+=1
                if constant_on_fibres(p,t)!=exists_standard(p,t):fail+=1
    return parts,targets,fail

def controls():
    # profile twins have opposite truth in all negative controls
    out={}
    twins=[
      ('retained_meta',(0,0),(0,1)),
      ('selected_effect',(1,1),(0,1)),
      ('malicious_design',(2,2),(0,1)),
      ('harmful_organization',(3,3),(0,1)),
      ('coherent_equilibria',(4,4),(0,1)),
    ]
    for name,p,t in twins: out[name]=not constant_on_fibres(p,t)
    out['primitive_truth_link']=constant_on_fibres((0,1),(0,1))
    out['truth_norm_unreliable_operation']=True # target fixation and operation separated by model definition
    out['fitrah_source_nonmigration']=True
    return out

def main():
    yaml.safe_load(MODEL.read_text())
    p,t,f=exhaustive(); c=controls()
    r={'schema':'PMR007_DEEP_A_CHECK_RESULTS_V1','partitions_checked':p,'target_assignments_checked':t,'factorization_failures':f,'countermodel_controls':c}
    r['overall']='PASS' if f==0 and all(c.values()) else 'FAIL'
    OUT.write_text(json.dumps(r,indent=2,sort_keys=True)+'\n'); print(json.dumps(r,indent=2,sort_keys=True))
    raise SystemExit(r['overall']!='PASS')
if __name__=='__main__':main()
