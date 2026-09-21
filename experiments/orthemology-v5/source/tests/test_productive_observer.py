import importlib.util,unittest
from boundaries import Rejection
import operational

def machine(rows):return {'kind':'binary-tape-observer','transitions':rows}
LOOP=machine([[[0,0,1],[0,0,1]]])
HALT=machine([[[-1,0,1],[-1,0,1]]])
LATER=machine([[[1,0,1],[1,0,1]],[[-1,0,1],[-1,0,1]]])

class ProductiveObserverTests(unittest.TestCase):
 def setUp(self):
  self.assertIsNotNone(importlib.util.find_spec('productive_observer'),'productive observation source absent')
  import productive_observer
  self.p=productive_observer
 def test_total_finite_prefix_not_infinite_decision(self):
  out=self.p.prefix(LOOP,[1,0,1,1]);self.assertEqual(out['output'],[0,0,0,0]);self.assertEqual(out['full_stream_defect'],'UNKNOWN')
  out=self.p.prefix(HALT,[1,0,1]);self.assertEqual(out['output'],[1,0,1]);self.assertEqual(out['full_stream_defect'],[1,1])
  out=self.p.prefix(LATER,[1,1,0,1]);self.assertEqual(out['output'],[0,1,0,1]);self.assertEqual(out['halt_step'],2)
 def test_closed_control_invariant_proves_constant(self):
  cert=self.p.certify_constant(LOOP,[0]);self.assertEqual(cert['full_stream_defect'],[0,1]);self.assertEqual(cert['status'],'FINITE_INVARIANT_CHECKED')
  with self.assertRaises(Rejection):self.p.certify_constant(HALT,[0])
  with self.assertRaises(Rejection):self.p.certify_constant(LATER,[0])
 def test_unreachable_halt_does_not_spoil_valid_invariant(self):
  source=machine([[[0,0,1],[0,1,-1]],[[-1,0,1],[-1,0,1]]])
  self.assertEqual(self.p.certify_constant(source,[0])['full_stream_defect'],[0,1])
  with self.assertRaises(Rejection):self.p.certify_constant(source,[0,1])
 def test_no_raw_claimed_proof_and_bad_bit(self):
  with self.assertRaises(Rejection):self.p.prefix({**LOOP,'proved':True},[])
  with self.assertRaises(Rejection):self.p.prefix(LOOP,[True])
  with self.assertRaises(Rejection):self.p.certify_constant(LOOP,[])
 def test_executable_context_admits_nonidentity_and_revokes(self):
  e=operational.Engine.standard();c={'op':'observer','source':LOOP,'invariant':[0]}
  ticket=e.admit(c);self.assertEqual(e.dispatch(ticket,[1,0,1]),[0,0,0])
  e.revise_rule('observer',False)
  with self.assertRaises(Rejection):e.dispatch(ticket,[1])
  with self.assertRaises(Rejection):e.admit(c)
 def test_negative_certificate_is_not_a_positive_licence(self):
  e=operational.Engine.standard()
  with self.assertRaises(Rejection):e.admit({'op':'observer','source':HALT,'invariant':[0]})
