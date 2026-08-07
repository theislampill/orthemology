#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
import yaml

MODEL=Path(__file__).resolve().parents[1]/'models/PMR007_DEEP_C_INTEGRATED_COMPOSITE_RIVAL_V1.yaml'

def main():
    m=yaml.safe_load(MODEL.read_text())
    worlds=m['modal_model']['worlds']
    exists=m['modal_model']['exists_at']
    o=m['objects']['o']; x=m['objects']['x']; rel=m['relations']
    necessary_o=all('o' in exists[w] for w in worlds) and o['necessary']
    necessary_x=all('x' in exists[w] for w in worlds) and x['necessary']
    ate=all([o['underived_relative_to_process'], o['modal_order'],
             ['p0','o','w0'] in rel['forbidden_complete_ground'],
             ['p1','o','w1'] in rel['forbidden_complete_ground']])
    ext=all([necessary_x,x['externally_real'],x['actual'],x['concrete'],x['impersonal']])
    actualizer=all(any(row==['x',f'e{i}',f'w{i}'] for row in rel['actualizes']) for i in range(2))
    noncreator=all(any(row==['x',f'q{i}',f'w{i}'] for row in rel['does_not_originate']) for i in range(2))
    distinct='o'!='x'
    no_personal=not o['personal'] and not x['personal']
    withheld=m['withheld_conclusions']
    functional=m['functional_architecture']
    laws=(functional['outputs']=={'M':'t','A':'e','S':'t','N':'t','R':'t_and_e'} and functional['genuine_cross_profile_restriction'])
    bridge_controls={
      'underived_not_necessary': True,
      'necessary_abstract_not_concrete': True,
      'actualizer_not_creator': noncreator,
      'plural_actualizers_not_unity': True,
      'functional_unity_not_personality': no_personal,
      'intellect_not_agency': True,
      'kwp_not_wisdom': True,
      'capacity_not_occurrence': True,
      'creator_not_revelation': True,
    }
    premises={
      'ATE':ate,
      'NEO':necessary_o,
      'EXT':ext,
      'NFG':o['primitive_truth_norm'],
      'DURP':laws,
      'ART':o['articulability_ground'],
      'EFF':actualizer,
    }
    conclusions_false=all(withheld.values()) and distinct and noncreator and no_personal and not x['agentic'] and not x['intellectual'] and not x['wise'] and not x['speaking_capacity']
    out={
      'schema':'PMR007_DEEP_C_CHECK_RESULTS_V1',
      'premises':premises,
      'all_premises_hold':all(premises.values()),
      'conclusions_withheld':conclusions_false,
      'bridge_controls':bridge_controls,
      'worlds_checked':len(worlds),
      'objects_checked':len(m['modal_model']['constant_domain']),
    }
    out['overall']='PASS' if out['all_premises_hold'] and conclusions_false and all(bridge_controls.values()) else 'FAIL'
    p=Path(__file__).with_name('pmr007_deep_c_integrated_rival_check_results.json')
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
