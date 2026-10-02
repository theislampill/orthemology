import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from exact_budget import budget_certificate,verify_certificate
from fractions import Fraction as F

class CertificateTypes(unittest.TestCase):
 def setUp(self):
  self.c=budget_certificate(states=1,actions=1,models=1,p_min=F(1),margin=F(1),failure_probability=F(1,2))
 def test_float_derived_fields_rejected(self):
  for key in ['bad_count_budget','tail_rate','block_success_lower','rotor_size_bound','cutoff','charged_interval_bound']:
   with self.subTest(key=key):
    c=self.c.copy();c[key]=float(c[key]);self.assertFalse(verify_certificate(c))
 def test_rational_fields_remain_fraction(self):
  for key in ['p_min','margin','block_success_lower']:
   with self.subTest(key=key):
    c=self.c.copy();c[key]=int(c[key]);self.assertFalse(verify_certificate(c))
 def test_integer_fields_reject_bool_and_fraction(self):
  for value in [True,F(1)]:
   c=self.c.copy();c['states']=value;self.assertFalse(verify_certificate(c))
 def test_plain_dict_required(self):
  class Subdict(dict): pass
  self.assertFalse(verify_certificate(Subdict(self.c)))
 def test_legitimate_certificate_accepted(self):self.assertTrue(verify_certificate(self.c))
if __name__=='__main__':unittest.main()
