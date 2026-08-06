#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path
import yaml
MODEL=Path(__file__).resolve().parents[1]/'models/PMR007_DEEP_C_INTEGRATED_COMPOSITE_RIVAL_V2.yaml'

def main():
    m=yaml.safe_load(MODEL.read_text())
    W=m['modal_model']['worlds']; ex=m['modal_model']['exists_at']; P=m['predicate_extensions']; R=m['relations']
    necessary=lambda z: z in P['necessary'] and all(z in ex[w] for w in W)
    ate=(all(p in P['determinate_process'] for p in ('p0','p1')) and
         all(row in R['constitutive_condition'] for row in [['o','p0','w0'],['o','p1','w1']]) and
         all(row in R['forbidden_complete_ground'] for row in [['p0','o','w0'],['p1','o','w1']]))
    creator_candidates=[]
    for z in m['modal_model']['constant_domain']:
        if z not in P['agentic'] or z not in P['nonborrowed_efficacy']:
            continue
        ok=True
        for w in W:
            for c in m['contingent_particulars'][w]:
                if [z,c,w] not in R['originates']:
                    ok=False
        if ok: creator_candidates.append(z)
    table=m['functional_architecture']['profile_table']
    image={tuple(row[k] for k in ['M','A','S','N','R']) for row in table}
    marg=[{x[i] for x in image} for i in range(5)]
    product=set(itertools.product(*map(sorted,marg)))
    laws=all(row['M']==row['S']==row['N'] and row['R']==(row['A'] & row['N']) for row in table)
    common=set(P['modal_order']) & set(P['semantic_order']) & set(P['primitive_truth_norm']) & set(P['articulability_ground']) & set(P['concrete_actualizer'])
    premises={
      'ATE':ate,
      'NEO':necessary('o') and 'o' in P['underived_relative_to_process'],
      'EXT':necessary('x') and all('x' in P[k] for k in ['externally_real','actual','concrete','concrete_actualizer']),
      'NFG':'o' in P['primitive_truth_norm'],
      'DURP':laws and len(image)==4 and len(product)==32,
      'ART':'o' in P['articulability_ground'],
      'EFF':all(['x',f'e{i}',f'w{i}'] in R['actualizes'] for i in range(2)),
    }
    conclusions={
      'one_common_bearer':bool(common),
      'creatorhood':bool(creator_candidates) or bool(P['creator']),
      'intellect':bool(P['intellectual']),
      'personality':bool(P['personal']),
      'agency':bool(P['agentic']),
      'wisdom':bool(P['wise']),
      'speech_capacity':bool(P['speech_capable']),
      'actual_speech':bool(P['speaks']),
      'revelational_identification':bool(P['revelation_identified']),
    }
    bridge=[]
    for name,b in m['bridge_models'].items():
        vals=list(b.values())
        bridge.append({'id':name,'typed':all(isinstance(v,bool) for v in vals),'has_true_antecedent':any(vals),'has_false_withheld':any(v is False for v in vals)})
    out={
      'schema':'PMR007_DEEP_C_CHECK_RESULTS_V2',
      'premises':premises,
      'all_premises_hold':all(premises.values()),
      'conclusions':conclusions,
      'all_target_conclusions_false':not any(conclusions.values()),
      'creator_candidates':creator_candidates,
      'common_bearers':sorted(common),
      'functional_image_count':len(image),
      'functional_product_count':len(product),
      'functional_excluded_count':len(product-image),
      'bridge_model_controls':bridge,
      'bridge_controls_pass':all(x['typed'] and x['has_true_antecedent'] and x['has_false_withheld'] for x in bridge),
    }
    out['overall']='PASS' if out['all_premises_hold'] and out['all_target_conclusions_false'] and out['bridge_controls_pass'] else 'FAIL'
    p=Path(__file__).with_name('pmr007_deep_c_integrated_rival_check_v2_results.json')
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
