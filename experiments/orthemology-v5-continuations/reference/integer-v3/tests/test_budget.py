import sys,unittest
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from exact_budget import budget_certificate,ceil_log2_fraction,verify_certificate,BudgetResourceLimit

class BudgetTests(unittest.TestCase):
 def test_log_witness_minimal(self):
  for n in range(1,200):
   for d in range(1,35):
    x=F(n,d);k=ceil_log2_fraction(x)
    self.assertGreaterEqual(F(2)**k,x)
    if k:self.assertLess(F(2)**(k-1),x)
 def test_bound_witness(self):
  c=budget_certificate(states=2,actions=2,models=2,p_min=F(1,4),margin=F(1,16),failure_probability=F(1,20))
  self.assertTrue(verify_certificate(c));self.assertEqual(c['cutoff'],9728)
 def test_margin_clamp(self):
  a=budget_certificate(states=1,actions=1,models=1,p_min=F(1),margin=F(8),failure_probability=F(1,10))
  b=budget_certificate(states=1,actions=1,models=1,p_min=F(1),margin=F(1),failure_probability=F(1,10))
  self.assertEqual(a['tail_rate'],b['tail_rate']);self.assertTrue(verify_certificate(a))
 def test_bad_inputs(self):
  for delta in [F(0),F(1),F(-1)]:
   with self.assertRaises(ValueError):budget_certificate(states=1,actions=1,models=1,p_min=F(1),margin=F(1),failure_probability=delta)
  with self.assertRaises(ValueError):budget_certificate(states=True,actions=1,models=1,p_min=F(1),margin=F(1),failure_probability=F(1,2))
 def test_resource_limit(self):
  with self.assertRaises(BudgetResourceLimit):budget_certificate(states=100,actions=100,models=2,p_min=F(1,2),margin=F(1,10),failure_probability=F(1,10),max_power_bits=10000)
 def test_mutated_witness_rejected(self):
  c=budget_certificate(states=1,actions=1,models=1,p_min=F(1),margin=F(1,2),failure_probability=F(1,2))
  c['cutoff']=0
  self.assertFalse(verify_certificate(c))

if __name__=='__main__':unittest.main()
