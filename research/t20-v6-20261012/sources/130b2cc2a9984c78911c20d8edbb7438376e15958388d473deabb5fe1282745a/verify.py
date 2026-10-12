#!/usr/bin/env python3
"""Complete deterministic submitted/reviewer regression replay and input binding."""
from datetime import datetime,timezone
from pathlib import Path
import hashlib
import json
import sys
import unittest

BASE=Path(__file__).resolve().parent
ROOT=BASE.parent
sys.path.insert(0,str(BASE))
sys.path.insert(0,str(BASE/'review'))
import test_guarded_compiler as main_tests
import test_submitted_guarded_compiler as review_tests
from mutation_controls import run as mutations

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    started=datetime.now(timezone.utc).isoformat()
    loader=unittest.TestLoader()
    suite=unittest.TestSuite((loader.loadTestsFromModule(main_tests),
                             loader.loadTestsFromModule(review_tests)))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():
        return 1
    rejected=mutations()
    originals=json.loads((BASE/'INPUT_HASHES.json').read_text())
    for row in json.loads((BASE/'source-review/SOURCE_BINDINGS.json').read_text())['sources']:
        if row['path'] in originals:
            assert originals[row['path']]==row['sha256']
        originals[row['path']]=row['sha256']
    unchanged={p:sha(ROOT/p)==digest for p,digest in originals.items()}
    assert all(unchanged.values()),unchanged
    (BASE/'INPUT_UNCHANGED.json').write_text(json.dumps(unchanged,indent=2)+'\n')
    bound=('RESULT.md','guarded_compiler.py','test_guarded_compiler.py','mutation_controls.py','verify.py',
           'review/test_submitted_guarded_compiler.py','review/GUARDED_TREE_REVIEW.md',
           'source-review/RETAINED_SOURCE_FINDING.md','source-review/SOURCE_BINDINGS.json')
    output={'status':'PASS','started_utc':started,'finished_utc':datetime.now(timezone.utc).isoformat(),
            'tests_run':result.testsRun,'main_tests':9,'independent_internal_ai_tests':5,
            'metrics':main_tests.METRICS,'mutations':rejected,
            'unchanged_input_files':len(unchanged),
            'sha256':{p:sha(BASE/p) for p in bound},
            'boundary':'Finite structural tree checks. No kernel proof, source validation, integration, closure, or active-duration credit.'}
    (BASE/'CHECK_RESULTS.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output,indent=2))
    return 0

if __name__=='__main__':
    raise SystemExit(main())
