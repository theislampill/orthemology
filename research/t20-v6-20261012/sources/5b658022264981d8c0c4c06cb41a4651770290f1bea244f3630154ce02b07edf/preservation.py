"""Preservation and representation-invariant production-mode controls.
A per-stage existence fact is not, by itself, a source-labelled new effect.
"""
from pathlib import Path
from itertools import product
import json,unittest
from provision_semantics import IntendedAct,execute_intentions

def uniform_realization(acts):
    events,supports,_,goals=execute_intentions(acts)
    return events,supports,{key:'realize-from-active-support' for key in supports},goals


def preserve(schedule):
    alive=False; facts=[]; proof_records=[]
    for t,(a,b) in enumerate(schedule):
        # Stage0 originates; subsequent stages preserve. No autonomous
        # unexplained background object is assumed at the starting stage.
        active=frozenset(g for g,x in [('A',a),('B',b)] if x)
        alive=bool(active) if t==0 else alive and bool(active)
        if alive:
            facts.append(('e',t,'exists'))
            proof_records.append({'stage':t,'current_support':sorted(active),
                                  'rule':'originate' if t==0 else 'preserve',
                                  'prior_state_required':t>0})
    return {'bearers':('e',) if facts else (), 'stage_facts':facts,
            'explanatory_proof_records':proof_records,
            'root_indexed_trace_if_real':[(r['stage'],g) for r in proof_records for g in r['current_support']]}


def result():
    a=IntendedAct('A','alpha',frozenset(['e']))
    b=IntendedAct('B','beta',frozenset(['e']))
    old_joint=execute_intentions([a,b]);old_solo=execute_intentions([a])
    new_joint=uniform_realization([a,b]);new_solo=uniform_realization([a])
    joint=preserve([(True,True)]*3);solo=preserve([(True,False)]*3)
    all_profiles=[]
    for schedule in product(tuple(product((False,True),repeat=2)),repeat=3):
        r=preserve(schedule)
        all_profiles.append({'schedule':schedule,'stage_facts':r['stage_facts']})
    return {'same_semantics_different_rule_names':{
        'created_and_supports_unchanged_by_reencoding':old_joint[:2]==new_joint[:2] and old_solo[:2]==new_solo[:2],
        'guarded_rule_names_change_on_suppression':old_joint[2]!=old_solo[2],
        'uniform_rule_names_change_on_suppression':new_joint[2]!=new_solo[2],
        'actual_support_changes_in_both_encodings':old_joint[1]!=old_solo[1] and new_joint[1]!=new_solo[1]},
      'preservation':{'joint':joint,'solo':solo,
                     'same_enduring_bearers':joint['bearers']==solo['bearers'],
                     'same_per_stage_existential_effects':joint['stage_facts']==solo['stage_facts'],
                     'same_root_indexed_trace_if_real':joint['root_indexed_trace_if_real']==solo['root_indexed_trace_if_real'],
                     'schedules_checked':len(all_profiles)},
      'scope':'Explanatory records are not asserted to be extra created entities; per-stage existence semantics alone does not enforce contribution-disjointness. Source original-agency adequacy remains open.'}

class PreservationTests(unittest.TestCase):
    def test_rule_name_switch_not_semantic_invariant(self):
        r=result()['same_semantics_different_rule_names']
        self.assertTrue(r['created_and_supports_unchanged_by_reencoding'])
        self.assertTrue(r['guarded_rule_names_change_on_suppression'])
        self.assertFalse(r['uniform_rule_names_change_on_suppression'])
        self.assertTrue(r['actual_support_changes_in_both_encodings'])
    def test_same_bearer_and_stage_facts_with_co_preservation(self):
        r=result()['preservation']
        self.assertTrue(r['same_enduring_bearers'])
        self.assertTrue(r['same_per_stage_existential_effects'])
        self.assertFalse(r['same_root_indexed_trace_if_real'])
    def test_preservation_is_genuinely_needed_at_every_stage(self):
        self.assertEqual(preserve([(True,False),(False,False),(True,True)])['stage_facts'],[('e',0,'exists')])
    def test_origination_not_hidden_background(self):
        self.assertEqual(preserve([(False,False),(True,True)])['stage_facts'],[])
    def test_sixty_four_profiles_examined(self):
        self.assertEqual(result()['preservation']['schedules_checked'],64)

if __name__=='__main__':
    (Path(__file__).resolve().parents[1]/'results/PRESERVATION_MODES.json').write_text(json.dumps(result(),indent=2)+'\n')
    unittest.main(verbosity=2)
