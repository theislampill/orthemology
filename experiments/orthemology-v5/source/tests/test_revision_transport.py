import unittest
import operational as o
from boundaries import Rejection
from test_observation_revision import model,primitive

class RevisionTransport(unittest.TestCase):
 def test_coarsening_preserves_bound_but_rebinds_authority(self):
  e=o.Engine.standard();self.assertTrue(hasattr(e,'coarsen_probability_observation'),'explicit coarsening rule absent')
  e.set_probability_observation('x',model([0,-1]));e.require_probability('primitive:succ','x',[1,2]);old=e.admit(primitive())
  report=e.coarsen_probability_observation('x',model([0,0]));self.assertEqual(report['coarse_defect'],[0,1]);self.assertEqual(report['fine_defect'],[1,2])
  with self.assertRaises(Rejection):e.dispatch(old,2)
  new=e.revalidate(old);self.assertEqual(e.dispatch(new,2),3);self.assertNotEqual(old.ticket,new.ticket)
  self.assertEqual(e.describe(new)['probability_evidence'][0]['defect'],[0,1])
 def test_revalidation_does_not_override_revocation(self):
  e=o.Engine.standard();self.assertTrue(hasattr(e,'revalidate'),'explicit revalidation rule absent')
  old=e.admit(primitive());e.revise_rule('primitive:succ',False)
  with self.assertRaises(Rejection):e.revalidate(old)
  e.revise_rule('primitive:succ',True);new=e.revalidate(old);self.assertEqual(e.dispatch(new,0),1)
  with self.assertRaises(Rejection):e.dispatch(old,0)
 def test_malformed_native_ticket_fails_declared(self):
  e=o.Engine.standard()
  for key in [None,[],{},True,3,'x'*10000]:
   for fun in [lambda:e.dispatch(o.Licence(key),0),lambda:e.describe(o.Licence(key))]:
    with self.assertRaises(Rejection):fun()
 def test_cross_engine_ticket_not_authority(self):
  a,b=o.Engine.standard(),o.Engine.standard();ticket=a.admit(primitive())
  with self.assertRaises(Rejection):b.dispatch(ticket,0)

if __name__=='__main__':unittest.main()
