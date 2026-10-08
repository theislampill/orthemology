"""Replay previous 26 controls with efficient synthesis and negative checking."""
import importlib.util
from pathlib import Path
import sys
import unittest
HERE=Path(__file__).resolve().parent
PRIOR=HERE.parent/'hidden-change-reference'
ROOT=HERE.parents[2]
REFERENCE=ROOT/'tranche18/research/hidden-change/reference-v1'
EFFICIENT=ROOT/'tranche18/research/hidden-change/efficient-v1'
sys.path[:0]=[str(EFFICIENT),str(REFERENCE)]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec);sys.modules[name]=module;spec.loader.exec_module(module)
    return module
load('oracle',PRIOR/'oracle.py')
previous=load('previous_adversarial',PRIOR/'test_reference_independent.py')
import efficient,negative
previous.solve=efficient.solve
previous.known_operator=efficient.known_operator
previous.uncertain_operator=efficient.uncertain_operator
previous.check_negative=negative.check_negative
if __name__=='__main__':
    outcome=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromModule(previous))
    raise SystemExit(not outcome.wasSuccessful())
