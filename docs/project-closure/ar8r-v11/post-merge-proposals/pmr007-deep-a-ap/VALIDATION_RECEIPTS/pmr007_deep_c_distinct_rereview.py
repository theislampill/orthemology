#!/usr/bin/env python3
from __future__ import annotations
import hashlib, itertools, json
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/'models/PMR007_DEEP_C_INTEGRATED_COMPOSITE_RIVAL_V2.yaml'

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def hashes():
    bad=[]
    for line in (ROOT/'PMR-007_DEEP_C_V2_FROZEN_HASHES.sha256').read_text().splitlines():
        if not line.strip(): continue
        exp,rel=line.split(maxsplit=1); got=sha(ROOT/rel)
        if exp!=got: bad.append({'path':rel,'expected':exp,'actual':got})
    return bad

def main():
    m=yaml.safe_load(MODEL.read_text())
    W=m['modal_model']['worlds']; A=m['modal_model']['accessibility']; E=m['modal_model']['exists_at']; P=m['predicate_extensions']; R=m['relations']
    # Generic Kripke necessity: exists at every world accessible from every world.
    universal_access=all(set(A[w])==set(W) for w in W)
    necessary_eval={z:(z in P['necessary'] and all(z in E[v] for w in W for v in A[w])) for z in m['modal_model']['constant_domain']}
    # Generic scoped creator evaluator from the declared definition.
    creators=[]
    for z in m['modal_model']['constant_domain']:
        guard=(z in P['agentic'] and z in P['nonborrowed_efficacy'])
        complete=all([z,c,w] in R['originates'] for w in W for c in m['contingent_particulars'][w])
        if guard and complete: creators.append(z)
    # Generic common-bearer query over the five declared role extensions.
    roles=['modal_order','semantic_order','primitive_truth_norm','articulability_ground','concrete_actualizer']
    common=set(m['modal_model']['constant_domain'])
    for role in roles: common &= set(P[role])
    # Rebuild outputs from primitive table, not from primary result.
    table=m['functional_architecture']['profile_table']
    image=set()
    table_errors=[]
    for row in table:
        predicted=(row['t'],row['e'],row['t'],row['t'],row['t'] & row['e'])
        observed=tuple(row[k] for k in ['M','A','S','N','R'])
        if observed!=predicted: table_errors.append({'row':row,'predicted':predicted})
        image.add(observed)
    marginals=[sorted({x[i] for x in image}) for i in range(5)]
    product=set(itertools.product(*marginals))
    target_roles=['personal','intellectual','agentic','wise','speech_capable','speaks','revelation_identified','creator','unified_common_bearer']
    empty_targets={r:(len(P[r])==0) for r in target_roles}
    out={
      'schema':'PMR007_DEEP_C_DISTINCT_REREVIEW_RESULTS_V1',
      'frozen_hash_failures':hashes(),
      'universal_accessibility':universal_access,
      'necessary_o':necessary_eval['o'],
      'necessary_x':necessary_eval['x'],
      'creator_candidates':creators,
      'common_bearers':sorted(common),
      'target_extensions_empty':empty_targets,
      'profile_table_errors':table_errors,
      'image_count':len(image),
      'product_count':len(product),
      'excluded_count':len(product-image),
      'model_relative_necessity_only':True,
      'formal_satisfiability_not_world_truth':True,
      'source_claim_not_made':True,
    }
    out['overall']='PASS' if (not out['frozen_hash_failures'] and universal_access and necessary_eval['o'] and necessary_eval['x'] and not creators and not common and all(empty_targets.values()) and not table_errors and len(image)==4 and len(product)==32 and all(out[k] for k in ['model_relative_necessity_only','formal_satisfiability_not_world_truth','source_claim_not_made'])) else 'FAIL'
    p=Path(__file__).with_name('PMR-007_DEEP_C_DISTINCT_REREVIEW_RESULTS.json')
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
