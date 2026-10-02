import sys,unittest
from pathlib import Path
from fractions import Fraction as F
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from exact_budget import budget_certificate,verify_certificate

class GridTests(unittest.TestCase):
 def test_exact_grid_and_mutations(self):
  count=0
  for s in range(1,4):
   for a in range(1,4):
    for m in range(1,4):
     for p in [F(1,2),F(3,4),F(1)]:
      for eta in [F(1,100),F(1,8),F(2)]:
       previous=None
       for delta in [F(1,2),F(1,10),F(1,100)]:
        c=budget_certificate(states=s,actions=a,models=m,p_min=p,margin=eta,failure_probability=delta)
        self.assertTrue(verify_certificate(c))
        if previous is not None:self.assertGreaterEqual(c['bad_count_budget'],previous)
        previous=c['bad_count_budget']
        d=c.copy();d['bad_count_budget']=0;self.assertFalse(verify_certificate(d))
        d=c.copy();d['cutoff_log_witness']-=1;self.assertFalse(verify_certificate(d))
        count+=1
  self.assertEqual(count,729)
 def test_float_rejected(self):
  with self.assertRaises(TypeError):budget_certificate(states=1,actions=1,models=1,p_min=.5,margin=F(1,4),failure_probability=F(1,10))

if __name__=='__main__':unittest.main()
