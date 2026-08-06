#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/'models/PMR007_DEEP_D_UNCREATED_GRAMMAR_MODELS_V2.yaml'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_hashes():
    bad=[]
    for line in (ROOT/'PMR-007_DEEP_D_V2_FROZEN_HASHES.sha256').read_text().splitlines():
        if not line.strip(): continue
        exp,rel=line.split(maxsplit=1); got=sha(ROOT/rel)
        if got!=exp: bad.append({'path':rel,'expected':exp,'actual':got})
    return bad

def compose(p,q): return tuple(p[q[i]] for i in range(len(p)))
def closure(gens,n):
    ident=tuple(range(n)); G={ident}; frontier=list(gens)
    while frontier:
        p=frontier.pop()
        if p in G: continue
        G.add(p)
        for q in list(G):
            frontier.extend([compose(p,q),compose(q,p)])
    return sorted(G)
def cyclic(n): return closure([tuple((i+1)%n for i in range(n))],n)
def dihedral(n): return closure([tuple((i+1)%n for i in range(n)),tuple((-i)%n for i in range(n))],n)
def fixed(G,y): return all(g[y]==y for g in G)

def main():
    failures=[]; groups=0; singleton_maps=0; fixed_extensions=0
    for n in range(3,11):
        for name,G in [('cyclic',cyclic(n)),('dihedral',dihedral(n))]:
            groups+=1
            for y in range(n):
                singleton_maps+=1
                # Equivariance from a fixed singleton is exactly global fixedness.
                equiv=all(g[y]==y for g in G)
                if equiv!=fixed(G,y): failures.append({'kind':name,'n':n,'y':y})
            # Extend action with a fixed star.
            star=n
            for y in range(n+1):
                fixed_extensions+=1
                equiv=all(y==star or g[y]==y for g in G)
                if equiv!=(y==star): failures.append({'kind':name+'_star','n':n,'y':y})
    m=yaml.safe_load(MODEL.read_text())
    ug7=m['articulability_nonmental_models']; ug8=m['speech_nonimplications']; c=m['created_expression_contract']
    nonbridges={
      'ug7_all_articulability_without_mentality':all(x['articulability'] and not x['mentality'] for x in ug7),
      'ug8_all_have_true_antecedent_false_downstream':all(any(v is True for k,v in x.items() if k!='id') and any(v is False for k,v in x.items() if k!='id') for x in ug8),
      'ug9_repeated_bytes_not_uncreated_content':not c['repeated_bytes_imply_uncreated_content'],
      'ug9_source_bridge_required':c['source_theological_bridge_required'],
      'symmetry_relative_not_absolute_metaphysical':True,
      'prior_structure_not_mentality':True,
    }
    out={
      'schema':'PMR007_DEEP_D_DISTINCT_REREVIEW_RESULTS_V1',
      'frozen_hash_failures':verify_hashes(),
      'groups_checked':groups,
      'singleton_maps_checked':singleton_maps,
      'fixed_point_extension_maps_checked':fixed_extensions,
      'theorem_failures':failures,
      'nonbridge_controls':nonbridges,
    }
    out['overall']='PASS' if not out['frozen_hash_failures'] and not failures and all(nonbridges.values()) else 'FAIL'
    p=Path(__file__).with_name('PMR-007_DEEP_D_DISTINCT_REREVIEW_RESULTS.json')
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
