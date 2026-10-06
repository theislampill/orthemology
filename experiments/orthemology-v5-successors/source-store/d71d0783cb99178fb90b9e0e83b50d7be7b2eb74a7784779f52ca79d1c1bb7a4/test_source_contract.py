#!/usr/bin/env python3
"""Identity and bounded branch-sensitivity controls, not universal proof credit."""
from pathlib import Path
import ast, hashlib, importlib.util, sys, unittest
sys.dont_write_bytecode = True
ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'source/prcodec.py'

class SourceContractTests(unittest.TestCase):
    def test_validator_exists(self):
        self.assertTrue((ROOT/'source_contract.py').is_file(), 'missing source-shape validator')
    def test_source_shape_pins_and_mutation_controls(self):
        path=ROOT/'source_contract.py'
        self.assertTrue(path.is_file(), 'missing source-shape validator')
        spec=importlib.util.spec_from_file_location('source_contract',path)
        v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
        text=SOURCE.read_text(); self.assertEqual(v.validate(text)['status'],'PASS_EXACT_SOURCE_SHAPE')
        mutations={
            'swap_operands':('b=vals.pop();a=vals.pop()','a=vals.pop();b=vals.pop()'),
            'skip_ready_ticks':('t,ready=stack.pop();meter.tick();k=t[0]','t,ready=stack.pop();k=t[0]'),
            'check_registers':('vals.append(regs.get(t[1],0))','vals.append(meter.check(regs.get(t[1],0)))'),
            'off_by_one_pow_guard':('a+1>meter.max_bits','a>meter.max_bits'),
            'wrong_missing_default':('regs.get(t[1],0)','regs.get(t[1],1)'),
        }
        for label,(old,new) in mutations.items():
            self.assertEqual(text.count(old),1,label)
            with self.assertRaises(ValueError,msg=label): v.validate(text.replace(old,new))

if __name__=='__main__': unittest.main()
