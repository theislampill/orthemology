"""Independent typing and modal-admissibility controls, not original-source models.
No constructive script here certifies metaphysical possibility.
"""
from dataclasses import dataclass, replace
from itertools import product
from pathlib import Path
import importlib.util
import json
import time

@dataclass(frozen=True)
class State:
    a: int
    b: int
    e: int
    knowledge_b: int
    knowledge_e: int

def factive(s):
    return s.knowledge_b == s.b and s.knowledge_e == s.e

def independent_state(a,b):
    return State(a,b,a,b,a)

def controls():
    actual = independent_state(1,1)
    frozen_peer_change = replace(actual,b=0)
    updated_peer_knowledge = replace(frozen_peer_change,knowledge_b=0)
    # Same command, efficacy equation, capacity and outcome, different relational
    # knowledge content. This does not establish unreceived intrinsic knowledge.
    assert not factive(frozen_peer_change)
    assert factive(updated_peer_knowledge)
    assert (actual.a,actual.e)==(updated_peer_knowledge.a,updated_peer_knowledge.e)
    # Exactly the same problem appears without any rival original producer.
    single_actual={'command':1,'effect':1,'knowledge_effect':1}
    single_alternative={'command':0,'effect':0,'knowledge_effect':1}
    single_repaired={**single_alternative,'knowledge_effect':0}
    assert single_alternative['knowledge_effect'] != single_alternative['effect']
    assert single_repaired['knowledge_effect'] == single_repaired['effect']
    # A passive observer's fixed true content also entails an outcome, despite
    # zero productive input. Thus entailment over factive fixed-content states
    # cannot define original productive sufficiency.
    observer_states=[{'producer':p,'observer_knowledge':p,'effect':p} for p in (0,1)]
    knowing_e=[s for s in observer_states if s['observer_knowledge']==1]
    assert knowing_e and all(s['effect']==1 for s in knowing_e)
    # Two intrinsic acts and two causal contributions can inhabit one external
    # created product. This is a typing control: it does not make them originals.
    intrinsic_acts={'act_A','act_B'}
    contribution_to_product={'contribution_A':'e','contribution_B':'e'}
    assert len(intrinsic_acts)==2
    assert len(contribution_to_product)==2
    assert len(set(contribution_to_product.values()))==1
    # Distribution over a source-neutral end does not select an allocation.
    admissible=[(a,b) for a,b in product(range(3),repeat=2) if a+b==2]
    assert len(admissible)==3
    # Unique output with complete knowledge in every world remains three worlds.
    omniscient=[{'a':a,'b':b,'knows_a':a,'knows_b':b,'e':a+b} for a,b in admissible]
    assert len(omniscient)==3 and {w['e'] for w in omniscient}=={2}
    return {
      'peer_suppression_frozen_knowledge_factive':factive(frozen_peer_change),
      'peer_suppression_updated_relational_content_factive':factive(updated_peer_knowledge),
      'operative_command_and_result_unchanged':True,
      'single_source_frozen_knowledge_alternative_factive':False,
      'single_source_updated_knowledge_alternative_factive':True,
      'passive_knower_content_entails_effect_without_productive_input':True,
      'distinct_intrinsic_acts':len(intrinsic_acts),
      'distinct_contributions':len(contribution_to_product),
      'external_created_products':len(set(contribution_to_product.values())),
      'fully_factive_allocation_worlds':omniscient,
      'scope':'Finite logical controls. No constitutive nonreceipt, unrestricted ability, original-source possibility or whole-front closure is established.'
    }

def replay_causal_abstraction():
    p=Path(__file__).resolve().parents[1]/'causal-abstraction'/'causal_transfer.py'
    spec=importlib.util.spec_from_file_location('causal_transfer_review',p)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    r=module.run()
    assert r['all_three_output_tables_equal']
    ci=r['concordant_identification']
    assert ci['compatible_with_concordant_data']==4
    assert ci['minimal_identifying_extra_query_sets']==[[[0,1],[1,0]]]
    assert not r['conjunctive_negative_control_equal']
    assert r['modified_hp_root_causes']['parallel']==[('A','B')]
    assert r['modified_hp_root_causes']['left']==[('A',)]
    assert r['modified_hp_root_causes']['right']==[('B',)]
    full_states=[tuple(sorted(s.items())) for s in r['actual_fine_states'].values()]
    assert len(set(full_states))==3
    return {'independent_replay_passed':True,
            'root_output_comparisons':r['root_output_intervention_comparisons'],
            'full_fine_state_equality':False,
            'concordant_four_law_control_passed':True,
            'two_offdiagonal_queries_needed_for_all_four':True,
            'parallel_A_and_B_each_part_of_modified_HP_cause':True,
            'scope':'Methodological coarse/fine distinction; not a full-created-process equivalence or source-proof.'}

if __name__=='__main__':
    start=time.perf_counter()
    result={'controls':controls(),'causal_abstraction':replay_causal_abstraction()}
    result['measured_execution_seconds']=time.perf_counter()-start
    out=Path(__file__).with_name('INDEPENDENT_CONTROL_RESULTS.json')
    out.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
