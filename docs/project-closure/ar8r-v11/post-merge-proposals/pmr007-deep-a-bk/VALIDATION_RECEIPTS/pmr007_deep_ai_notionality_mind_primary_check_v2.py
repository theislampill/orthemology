#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path

# One structural order, one notional representation, two potential mental hosts.
VARS=['S','U','N','M0','M1','R0','R1','G0','G1','H0','H1','P0','P1']
I={v:i for i,v in enumerate(VARS)}
def v(bits,x): return bits[I[x]]

def class_models(guards=()):
    out=[]
    for b in itertools.product([False,True], repeat=len(VARS)):
        # NM-HOST: intrinsic notional representation has a mental token/host.
        if v(b,'N') and not ((v(b,'M0') and v(b,'R0')) or (v(b,'M1') and v(b,'R1'))): continue
        # Constitutive host is also a mental host representing the content.
        if v(b,'G0') and not (v(b,'M0') and v(b,'R0')): continue
        if v(b,'G1') and not (v(b,'M1') and v(b,'R1')): continue
        if 'H7a' in guards and v(b,'S') and not v(b,'N'): continue
        if 'H7b' in guards and v(b,'S') and v(b,'U') and v(b,'N') and not (v(b,'G0') or v(b,'G1')): continue
        if 'H7c' in guards:
            if v(b,'U') and v(b,'G0') and not v(b,'H0'): continue
            if v(b,'U') and v(b,'G1') and not v(b,'H1'): continue
        if 'H7d' in guards and v(b,'G0') and v(b,'G1'): continue
        out.append(b)
    return out

def eligible(ms,prem): return [m for m in ms if all(v(m,k)==val for k,val in prem.items())]
def query(ms,prem,conclusion):
    e=eligible(ms,prem); bad=[m for m in e if not conclusion(m)]
    witness={x:bool(bad[0][I[x]]) for x in VARS} if bad else None
    return {'eligible_models':len(e),'countermodels':len(bad),'first_countermodel':witness}

base=class_models()
full=class_models(('H7a','H7b','H7c','H7d'))
q={
 'notional_to_mental_host':query(base,{'N':True},lambda m:(v(m,'M0') or v(m,'M1'))),
 'structural_underived_to_mental_host':query(base,{'S':True,'U':True},lambda m:(v(m,'M0') or v(m,'M1'))),
 'notional_underived_to_constitutive_host':query(base,{'N':True,'U':True},lambda m:(v(m,'G0') or v(m,'G1'))),
 'constitutive_host_underived_without_transfer':query(class_models(('H7a','H7b','H7d')),{'S':True,'U':True},lambda m:(v(m,'H0') or v(m,'H1'))),
 'full_bridge_to_exactly_one_underived_constitutive_host':query(full,{'S':True,'U':True},lambda m:((v(m,'G0') and v(m,'H0')) ^ (v(m,'G1') and v(m,'H1')))),
 'full_bridge_to_personal_subject':query(full,{'S':True,'U':True},lambda m:(v(m,'P0') or v(m,'P1'))),
}
claims={
 'NM_HOST_entails_some_mental_host':q['notional_to_mental_host']['countermodels']==0,
 'structure_underived_does_not_entail_mental_host':q['structural_underived_to_mental_host']['countermodels']>0,
 'notional_hosting_does_not_entail_constitutive_ground':q['notional_underived_to_constitutive_host']['countermodels']>0,
 'underivability_does_not_transfer_without_H7c':q['constitutive_host_underived_without_transfer']['countermodels']>0,
 'H7a_b_c_d_entail_exactly_one_underived_constitutive_host':q['full_bridge_to_exactly_one_underived_constitutive_host']['countermodels']==0,
 'full_bridge_does_not_entail_personality':q['full_bridge_to_personal_subject']['countermodels']>0,
}
res={'schema':'PMR007_DEEP_AI_PRIMARY_CHECK_RESULTS_V2','valuations_per_class':2**len(VARS),'base_models':len(base),'full_bridge_models':len(full),'queries':q,'claims':claims,'overall':'PASS' if all(claims.values()) else 'FAIL'}
out=Path(__file__).with_name(Path(__file__).stem+'_results.json')
out.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
