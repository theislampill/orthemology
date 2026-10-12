"""Positive nonabsorption reduction and independent premise deletion controls.
Real-created-token membership is a semantic assumption, never inferred from the
existence of a derivation record or source name.
"""
from itertools import product
from pathlib import Path
import json,unittest

def subsets(n): return [frozenset(i for i in range(n) if mask & (1<<i)) for mask in range(1<<n)]

def census(n=3):
    sets=subsets(n); qualified=[]
    for ca,cb,joint in product(sets,repeat=3):
        # Solo is exactly this unchanged act's actual contribution set.
        # Both contribution sets are nonempty, source-disjoint, and retained.
        if ca and cb and not ca&cb and ca|cb <= joint:
            qualified.append((ca,cb,joint))
            assert joint-ca
            assert ca != joint
    return {'token_universe':n,'candidate_set_triples':len(sets)**3,
            'qualified_triples':len(qualified),
            'counterexamples_to_strict_total_history_growth':0}

def controls():
    return {
      'drop_nonempty_extra':{'solo':[0],'A_actual':[0],'B_actual':[],'joint':[0],'same_total':True},
      'drop_same_respect_disjointness':{'solo':[0],'A_actual':[0],'B_actual':[0],'joint':[0],'same_total':True},
      'drop_fixed_act_manifestation_locality':{'solo':[0,1],'A_actual':[0],'B_actual':[1],'joint':[0,1],'same_total':True},
      'drop_faithful_complete_retention':{'solo':[0],'A_actual':[0],'B_actual':[1],'joint':[0],'same_total':True},
      'CND_without_token_entire_attribution':{'participation_A':[0],'participation_B':[0],'entire_relation':[],
              'CND':True,'participation_disjoint':False,'point':'CND only implies disjointness after participation tokens are justified as each source entire original contribution'},
      'signed_interaction':{'solo_real_history':['ka'],'joint_real_history':['ka','kb','ki'],
              'weights':{'ka':1,'kb':1,'ki':-1},'solo_projection':1,'joint_projection':1,
              'point':'Real creation/cancellation occurrences retained; net projection equality does not imply total-history equality'},
      'background_freshness':{'background':[1],'A_actual':[0],'B_actual':[1],
              'solo':[0,1],'joint':[0,1],
              'point':'An added token must be new relative to fixed background, not only disjoint from this act current contribution'}
    }

class TraceTests(unittest.TestCase):
    def test_exhaustive_reduction(self):
        self.assertGreater(census()['qualified_triples'],0)
    def test_deleted_assumptions_each_allow_equal_total(self):
        for key,v in controls().items():
            if key.startswith('drop_'):self.assertEqual(v['solo'],v['joint'])
    def test_cnd_alone_not_disjointness(self):
        v=controls()['CND_without_token_entire_attribution']
        self.assertTrue(v['CND']);self.assertFalse(v['participation_disjoint'])
    def test_signed_projection_can_hide_real_interaction(self):
        v=controls()['signed_interaction']
        self.assertEqual(sum(v['weights'][x] for x in v['solo_real_history']),v['solo_projection'])
        self.assertEqual(sum(v['weights'][x] for x in v['joint_real_history']),v['joint_projection'])
        self.assertEqual(v['solo_projection'],v['joint_projection'])
        self.assertNotEqual(v['solo_real_history'],v['joint_real_history'])
    def test_freshness_relative_to_background(self):
        v=controls()['background_freshness']
        self.assertFalse(set(v['A_actual'])&set(v['B_actual']))
        self.assertEqual(v['solo'],v['joint'])

if __name__=='__main__':
    result={'census':census(),'controls':controls(),
            'scope':'Conditional reduction; no universal physical conservation, no claim that causal records are created tokens'}
    (Path(__file__).resolve().parents[1]/'results/TRACE_REDUCTION.json').write_text(json.dumps(result,indent=2)+'\n')
    unittest.main(verbosity=2)
