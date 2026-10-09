#!/usr/bin/env python3
"""Replay the entire submitted suite without replacing its CHECK_RESULTS.json."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import unittest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))
paths = ('RESULT.md', 'compiler.py', 'verify.py', 'SOURCES.json')
before = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
spec = importlib.util.spec_from_file_location('reviewed_suite', ROOT / 'verify.py')
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)
suite = unittest.defaultTestLoader.loadTestsFromModule(module)
result = unittest.TextTestRunner(verbosity=2).run(suite)
after = {p: hashlib.sha256((ROOT / p).read_bytes()).hexdigest() for p in paths}
assert before == after, 'A reviewed source changed during replay.'
record = {
    'status': 'PASS' if result.wasSuccessful() else 'FAIL',
    'tests_run': result.testsRun,
    'failures': len(result.failures),
    'errors': len(result.errors),
    'metrics': module.METRICS,
    'source_sha256': before,
    'scope': 'Independent replay of all submitted tests, without modifying the submitted run record.'
}
(HERE / 'REPLAY_RESULTS.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
sys.exit(0 if result.wasSuccessful() else 1)
