import json,unittest
from pathlib import Path
from plurality_model import *

class BridgeChecks(unittest.TestCase):
    def test_two_bearers_distinct_own_tokens(self):
        m=model()
        self.assertEqual(m.relations['Bearer'],frozenset({('A',),('B',)}))
        self.assertIn(('PA','A'),m.relations['Inheres']);self.assertIn(('PB','B'),m.relations['Inheres'])
        self.assertNotIn(('PA','B'),m.relations['Inheres']);self.assertNotIn(('PB','A'),m.relations['Inheres'])
        self.assertNotEqual('AA','AB')
    def test_full_signature_swap_is_automorphism(self):
        self.assertTrue(automorphism(model(),SWAP))
        self.assertNotEqual(SWAP['A'],'A')
    def test_nontrivial_parameter_free_questions_agree(self):
        for f in formulas().values():
            self.assertEqual(truth(model(),f,{'x':'A'}),truth(model(),f,{'x':'B'}))
    def test_individual_constants_do_distinguish(self):
        m=model();f=EQ(V('x'),K('A'))
        self.assertTrue(truth(m,f,{'x':'A'}));self.assertFalse(truth(m,f,{'x':'B'}))
        f=R('Inheres',K('PA'),V('x'))
        self.assertTrue(truth(m,f,{'x':'A'}));self.assertFalse(truth(m,f,{'x':'B'}))
    def test_weak_relational_distinction_is_present(self):
        m=model()
        self.assertIn(('A','B'),m.relations['OtherBearer'])
        self.assertNotIn(('A','A'),m.relations['OtherBearer'])
        self.assertIn(('B','A'),m.relations['OtherBearer'])
    def test_added_qualitative_feature_breaks_symmetry_without_adding_parts(self):
        m=with_feature(model())
        self.assertFalse(automorphism(m,SWAP))
        self.assertNotEqual(('A',) in m.relations['DistinguishingFeature'],('B',) in m.relations['DistinguishingFeature'])
        self.assertFalse(m.relations['SeparableProperPart'])
        self.assertFalse(m.relations['ForeignEfficientReceipt'])
    def test_own_prerequisite_not_foreign_receipt(self):
        m=model()
        self.assertTrue(m.relations['OwnAttributePrerequisite'])
        self.assertFalse(m.relations['ForeignEfficientReceipt'])
        self.assertNotEqual(m.relations['OwnAttributePrerequisite'],m.relations['ForeignEfficientReceipt'])

    def test_current_joined_reactive_qualitative_reducts_have_swap(self):
        for r in reactive_reducts():
            self.assertTrue(r['is_automorphism'])
            self.assertNotEqual(r['act_tokens']['A'],r['act_tokens']['B'])
            self.assertEqual(r['structure'].relations['SatisfiedIntention'],frozenset({('A',),('B',)}))
            self.assertEqual(r['structure'].relations['SatisfiedOwnEnd'],frozenset({('A',),('B',)}))
            # Its known lack of individual entire production stays visible.
            self.assertFalse(r['structure'].relations['EntireProvider'])

if __name__=='__main__':
    out=report();out['reactive_reducts']=[{'context':r['context'],'domain':r['structure'].domain,'relations':{k:sorted(v) for k,v in r['structure'].relations.items()},'swap':r['swap'],'is_automorphism':r['is_automorphism']} for r in reactive_reducts()]
    (Path(__file__).resolve().parents[1]/'results/MODEL.json').write_text(json.dumps(out,indent=2)+'\n')
    unittest.main(verbosity=2)
