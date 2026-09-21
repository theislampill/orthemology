import importlib.util,itertools,unittest
from fractions import Fraction
import operational as o
from boundaries import Rejection
from test_reference import PT,PF,BOOL
import reference as r

class GuardedSourceTests(unittest.TestCase):
 def setUp(self):
  self.assertIsNotNone(importlib.util.find_spec('guarded_sampler'),'guarded source absent')
  import guarded_sampler
  self.g=guarded_sampler
 def spec(self,n=8):return {'kind':'quadratic','left':PT,'right':PF,'max_bits':n}
 def test_transition_counter_contract(self):
  z=self.g.advance(self.g.initial(),0)
  self.assertEqual(z['work']['shifts'],5)
  self.assertEqual(z['work']['additions'],6)
 def test_source_mass_certificate(self):
  p=self.g.check(self.spec());d=self.g.certificate(p)
  self.assertEqual(sum(Fraction(*d[k]) for k in ('left_mass','right_mass','pending_mass')),1)
  self.assertEqual(d['pending_mass'],[1,256]);self.assertEqual(Fraction(*d['expected_bits']),Fraction(255,128))
  self.assertEqual(d['assumptions'],['independent fair input bits','declared quadratic threshold'])
 def test_step_matches_prefix_all_branches(self):
  p=self.g.check(self.spec(10));e=o.Engine.standard();old=e.admit({'op':'sampler','left':PT,'right':PF})
  for n in range(9):
   for bits in itertools.product((0,1),repeat=n):
    result=self.g.run(p,list(bits));self.assertEqual(result['output'],e.dispatch(old,list(bits)))
    self.assertEqual(result['work']['multiplications'],3*result['output']['bits'])
    self.assertLessEqual(result['work']['comparisons'],2*result['output']['bits'])
 def test_done_leaf_type_and_pending_not_proof(self):
  p=self.g.check(self.spec());q=self.g.run(p,[0,0])['output'];self.assertEqual(r.check(q['proof'])[1],BOOL)
  q=self.g.run(p,[])['output'];self.assertNotIn('proof',q)
 def test_forged_state_rejected(self):
  for state in [None,{},self.g.State(-1,0),self.g.State(3,7)]:
   with self.assertRaises(Rejection):self.g.advance(state,0)
 def test_cap_and_bad_source(self):
  p=self.g.check(self.spec(2))
  with self.assertRaises(Rejection):self.g.run(p,[0,1,0])
  with self.assertRaises(Rejection):self.g.check({**self.spec(),'max_bits':True})
  with self.assertRaises(Rejection):self.g.check({**self.spec(),'claimed_mass':1})
 def test_finite_budget_is_not_full_termination(self):
  p=self.g.check(self.spec(8));state=self.g.initial()
  for _ in range(8):
   choices=[self.g.advance(state,b) for b in (0,1)];pending=[x for x in choices if x['branch']=='pending']
   self.assertEqual(len(pending),1);state=pending[0]['next']
  self.assertEqual(state.bits,8);self.assertEqual(self.g.certificate(p)['pending_mass'],[1,256])
 def test_operational_budget_admission_and_revision(self):
  e=o.Engine.standard();spec=self.spec(8);c={'op':'sampler_budgeted','source':spec,'max_pending':[1,256]}
  lic=e.admit(c);out=e.dispatch(lic,[0,0]);self.assertEqual(r.check(out['proof'])[1],BOOL)
  with self.assertRaises(Rejection):e.admit({**c,'max_pending':[1,512]})
  e.revise_rule('sampler',False)
  with self.assertRaises(Rejection):e.dispatch(lic,[0,0])

if __name__=='__main__':unittest.main()
