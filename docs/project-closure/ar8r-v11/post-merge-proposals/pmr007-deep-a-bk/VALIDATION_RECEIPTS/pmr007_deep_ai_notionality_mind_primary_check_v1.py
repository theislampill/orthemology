#!/usr/bin/env python3
from __future__ import annotations
import itertools,json
from pathlib import Path

# One order/content object and two potential mind hosts.
VARS=['S','U','N','M0','M1','R0','R1','G0','G1','H0','H1','P0','P1']
idx={v:i for i,v in enumerate(VARS)}
def val(bits,v): return bits[idx[v]]
def models(extra=()):
    out=[]
    for bits in itertools.product([False,True], repeat=len(VARS)):
        # NM-HOST: N -> some mind representing.
        if val(bits,'N') and not ((val(bits,'M0') and val(bits,'R0')) or (val(bits,'M1') and val(bits,'R1'))): continue
        # Ground implies mind and representation.
        if val(bits,'G0') and not (val(bits,'M0') and val(bits,'R0')): continue
        if val(bits,'G1') and not (val(bits,'M1') and val(bits,'R1')): continue
        # Underivability transfer if requested.
        if 'TRANSFER' in extra:
            if val(bits,'U') and val(bits,'G0') and not val(bits,'H0'): continue
            if val(bits,'U') and val(bits,'G1') and not val(bits,'H1'): continue
        # Structure-to-notion if requested.
        if 'S_TO_N' in extra and val(bits,'S') and not val(bits,'N'): continue
        # Constitutive-host existence for underived notional structure.
        if 'CONSTITUTIVE' in extra and val(bits,'S') and val(bits,'U') and val(bits,'N') and not (val(bits,'G0') or val(bits,'G1')): continue
        # Unique constitutive host.
        if 'UNIQUE' in extra and val(bits,'G0') and val(bits,'G1'): continue
        out.append(bits)
    return out

def entails(ms,premises,conclusion):
    relevant=[m for m in ms if all(val(m,p)==want for p,want in premises.items())]
    bad=[m for m in relevant if not conclusion(m)]
    return len(relevant),len(bad),bad[0] if bad else None

base=models()
full=models(('S_TO_N','CONSTITUTIVE','TRANSFER','UNIQUE'))
queries={}
queries['structural_underived_to_mind']=entails(base,{'S':True,'U':True},lambda m:(val(m,'M0') or val(m,'M1')))
queries['notional_to_mind']=entails(base,{'N':True},lambda m:(val(m,'M0') or val(m,'M1')))
queries['notional_underived_to_ground']=entails(base,{'N':True,'U':True},lambda m:(val(m,'G0') or val(m,'G1')))
queries['full_bridge_to_underived_intellect']=entails(full,{'S':True,'U':True},lambda m:(val(m,'H0') or val(m,'H1')))
queries['full_bridge_to_unique_ground']=entails(full,{'S':True,'U':True},lambda m:not (val(m,'G0') and val(m,'G1')) and (val(m,'G0') or val(m,'G1')))
queries['full_bridge_to_personality']=entails(full,{'S':True,'U':True},lambda m:(val(m,'P0') or val(m,'P1')))

# Convert witnesses to named dictionaries.
def pack(q):
    n,b,w=q
    return {'eligible_models':n,'countermodels':b,'first_countermodel':({v:bool(w[idx[v]]) for v in VARS} if w else None)}
res={k:pack(v) for k,v in queries.items()}
claims={
 'NM_HOST_entails_mind':res['notional_to_mind']['countermodels']==0,
 'structure_underived_does_not_entail_mind':res['structural_underived_to_mind']['countermodels']>0,
 'representation_hosting_does_not_entail_ground':res['notional_underived_to_ground']['countermodels']>0,
 'H7a_b_c_plus_unique_entails_one_underived_intellect_role':res['full_bridge_to_underived_intellect']['countermodels']==0 and res['full_bridge_to_unique_ground']['countermodels']==0,
 'full_bridge_does_not_entail_personality':res['full_bridge_to_personality']['countermodels']>0,
}
result={
 'schema':'PMR007_DEEP_AI_PRIMARY_CHECK_RESULTS_V1',
 'valuations_checked_per_class':2**len(VARS),
 'base_models':len(base),
 'full_bridge_models':len(full),
 'queries':res,
 'claims':claims,
 'overall':'PASS' if all(claims.values()) else 'FAIL'
}
out=Path(__file__).with_name(Path(__file__).stem+'_results.json')
out.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
print(json.dumps(result,indent=2,sort_keys=True))
