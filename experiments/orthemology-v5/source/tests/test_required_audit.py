import unittest
import build_gate as g

class RequiredAuditTests(unittest.TestCase):
 def test_transitive_gate_is_inside_every_required_block(self):
  self.assertTrue(hasattr(g,'render_required_audit'),'mandatory in-Lean audit emitter absent')
  text=g.render_required_audit([{'name':'AuditSupport','targets':['OrthemologyAudit.allowedAxiom']},{'name':'Example','targets':['Example.sound','Example.noFalse']}])
  for name in ['OrthemologyAudit.allowedAxiom','Example.sound','Example.noFalse']:
   block=text.split('AUDIT_BEGIN '+name+'"')[1].split('AUDIT_END '+name+'"')[0]
   self.assertIn('#check '+name,block);self.assertIn('#ortho_audit '+name,block);self.assertIn('#print axioms '+name,block)
  self.assertIn('import AuditSupport',text)
 def test_missing_meta_gate_module_rejected(self):
  self.assertTrue(hasattr(g,'render_required_audit'),'mandatory in-Lean audit emitter absent')
  with self.assertRaises(g.GateError):g.render_required_audit([{'name':'Example','targets':['Example.sound']}])
