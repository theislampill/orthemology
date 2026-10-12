"""Synthetic gate tests, NOT Lean execution or declaration evidence."""
import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'handoff'))
from execute_formal import require_version,parse_axioms

class FormalGateTests(unittest.TestCase):
    def test_exact_versions(self):
        require_version('Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)',
                        'Lake version 5.0.0-6caaee8 (Lean version 4.19.0)')
    def test_wrong_missing_versions_refused(self):
        for lean,lake in [('Lean version 4.32.2','Lake version 5.0.0-6caaee8'),
                          ('Lean version 4.19.0','Lake version 5.0.0-6caaee8'),
                          ('Lean version 4.19.0 6caaee8','Lake version 5.0.0-other'),('', '')]:
            with self.assertRaises(ValueError):require_version(lean,lake)
    def test_matching_type_and_axioms(self):
        text="P02A2.test : True\n'P02A2.test' depends on axioms: [propext, Classical.choice, Quot.sound]\n"
        self.assertEqual(parse_axioms(text,'P02A2.test'),['propext','Classical.choice','Quot.sound'])
    def test_empty_axioms_accepted_only_with_readback(self):
        self.assertEqual(parse_axioms("P02A2.test : True\n'P02A2.test' does not depend on any axioms\n",'P02A2.test'),[])
        with self.assertRaises(ValueError):parse_axioms("'P02A2.test' does not depend on any axioms",'P02A2.test')
    def test_wrong_name_duplicate_and_missing_refused(self):
        for text in ["P02A2.test : True\n'Other.test' depends on axioms: []",
                     "P02A2.test : True\n'P02A2.test' depends on axioms: []\n'P02A2.test' depends on axioms: []",
                     'P02A2.test : True','']:
            with self.assertRaises(ValueError):parse_axioms(text,'P02A2.test')
    def test_sorry_error_and_new_axiom_refused(self):
        for body in ["'P02A2.test' depends on axioms: [sorryAx]",
                     "'P02A2.test' depends on axioms: [unreviewedAx]",
                     "error: elaboration failed\n'P02A2.test' depends on axioms: []"]:
            with self.assertRaises(ValueError):parse_axioms('P02A2.test : True\n'+body,'P02A2.test')
if __name__=='__main__':unittest.main(verbosity=2)
