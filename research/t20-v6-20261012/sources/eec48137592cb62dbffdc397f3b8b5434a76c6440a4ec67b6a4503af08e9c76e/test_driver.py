"""Policy tests only: synthetic outputs never earn compiler or kernel credit."""
import sys
from pathlib import Path
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'handoff'))
from qualify_lean419 import guard_version, source_lint, GateError
from canonical_gate import parse_audit

class DriverPolicy(unittest.TestCase):
    def test_exact_version(self):guard_version('Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)\n')
    def test_wrong_version(self):
        with self.assertRaises(GateError):guard_version('Lean (version 4.32.2, commit 6caaee842e94)\n')
    def test_wrong_commit(self):
        with self.assertRaises(GateError):guard_version('Lean (version 4.19.0, commit f3b06c705)\n')
    def test_missing_compiler_text(self):
        with self.assertRaises(GateError):guard_version('not found')
    def test_proof_hole_rejected(self):
        with self.assertRaises(GateError):source_lint('theorem f : True := by sorry')
    def test_axiom_rejected(self):
        with self.assertRaises(GateError):source_lint('axiom f : False')
    def test_comment_not_proof_hole(self):source_lint('/- no sorry is permitted -/\ntheorem f : True := True.intro')
    def test_nested_comment(self):source_lint('/- a /- sorry -/ b -/\ndef x : Nat := 0')
    def test_unclosed_delimiter_rejected(self):
        with self.assertRaises(GateError):source_lint('def x := (0')
    def test_ambiguous_output_cannot_pass(self):
        with self.assertRaises(GateError):parse_audit('PASS\n',['P01.x'])
    def test_sorry_axiom_readback_rejected(self):
        text="AUDIT_BEGIN P01.x\nP01.x : True\n'P01.x' depends on axioms: [sorryAx]\nAUDIT_END P01.x\n"
        with self.assertRaises(GateError):parse_audit(text,['P01.x'])
    def test_partial_inventory_rejected(self):
        text="AUDIT_BEGIN P01.x\nP01.x : True\n'P01.x' does not depend on any axioms\nAUDIT_END P01.x\n"
        with self.assertRaises(GateError):parse_audit(text,['P01.x','P01.y'])
    def test_type_header_required(self):
        text="AUDIT_BEGIN P01.x\n'P01.x' does not depend on any axioms\nAUDIT_END P01.x\n"
        with self.assertRaises(GateError):parse_audit(text,['P01.x'])
