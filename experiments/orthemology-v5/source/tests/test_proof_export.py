import importlib.util,unittest
from test_reference import PID,PF,PT,ID,BOOL,ae
import reference as r
from boundaries import dump_json,Rejection

class ProofExportTests(unittest.TestCase):
 def setUp(self):
  self.assertIsNotNone(importlib.util.find_spec('proof_export'),'proof export bridge absent')
  import proof_export
  self.e=proof_export
 def test_internal_self_application_exports_actual_check(self):
  p={'rule':'app','function':ae(PID,ID),'argument':PID};text=self.e.export('identitySelf',dump_json(p))
  self.assertIn('check 0 identitySelfCertificate',text);self.assertIn('Cert.allE',text);self.assertIn('identitySelf_erasure',text)
  self.assertIn('by decide',text);self.assertNotIn('sorry',text);self.assertNotIn('axiom ',text)
 def test_reduction_trace_exports_steps(self):
  p={'rule':'app','function':ae(PID,ID),'argument':PID};t,_=r.check(p);_,tr=r.normalize(t)
  source=self.e.export('reduced',dump_json({'rule':'reduce','proof':p,'trace':tr}))
  self.assertEqual(source.count('Cert.step'),len(tr)-1)
 def test_duplicate_unknown_and_bad_trace_rejected(self):
  for raw in [b'{"rule":"i","rule":"i","A":["bottom"]}',dump_json({'rule':'trust','valid':True}),dump_json({'rule':'reduce','proof':PID,'trace':[['k']]})]:
   with self.assertRaises(Rejection):self.e.export('x',raw)
 def test_module_names_not_an_injection_channel(self):
  for name in ['x\naxiom false : False','', 'A.B','x;by','a'*81]:
   with self.assertRaises(Rejection):self.e.export(name,dump_json(PID))
 def test_deterministic_emission_and_schema(self):
  self.assertEqual(self.e.export('selector',dump_json(PT)),self.e.export('selector',dump_json(PT)))
  text=self.e.module([('trueSelector',dump_json(PT)),('falseSelector',dump_json(PF))])
  self.assertIn('import FiniteBridge',text);self.assertIn('namespace OrthemologyV4Exports',text)
  with self.assertRaises(Rejection):self.e.module([('x',dump_json(PT)),('x',dump_json(PF))])

if __name__=='__main__':unittest.main()
