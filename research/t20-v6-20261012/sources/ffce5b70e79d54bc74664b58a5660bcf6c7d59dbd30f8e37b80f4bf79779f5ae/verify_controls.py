#!/usr/bin/env python3
"""Run two rejected semantic mutations against the frozen general proof.
These controls are not additional proofs, and an expected rejection is not a successful build.
"""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

root = Path(__file__).resolve().parent
lean = shutil.which('lean')
if lean is None:
    raise SystemExit('Lean executable missing from PATH')
source = (root / 'ResetContinuation.lean').read_text()
mutants = [
    ('remove_backward_dependency',
     'Essential (fun x => T a x j) i → Closure h T i',
     'Essential (fun x => T a x j) i → Closure h T j'),
    ('make_resets_noops',
     'fun j => if j = i then b else x j',
     'fun j => x j'),
]
records = []
for name, old, new in mutants:
    if source.count(old) != 1:
        raise SystemExit(f'{name}: mutation target is not unique')
    mutated = source.replace(old, new)
    with tempfile.TemporaryDirectory(prefix='reset-lean-control-') as temp:
        path = Path(temp) / f'{name}.lean'
        path.write_text(mutated)
        result = subprocess.run([lean, '-DwarningAsError=true', str(path)],
                                capture_output=True, text=True, cwd=root)
    log = root / 'logs' / f'control-{name}.log'
    log.write_text(result.stdout + result.stderr)
    proof_failure = any(marker in result.stdout + result.stderr for marker in
                        ['unsolved goals', 'application type mismatch'])
    records.append({'name': name, 'exit_code': result.returncode,
                    'expected': 'rejected', 'passed': result.returncode != 0 and proof_failure,
                    'proof_failure_diagnostic': proof_failure,
                    'mutated_source_sha256': hashlib.sha256(mutated.encode()).hexdigest(),
                    'log': str(log.relative_to(root))})
    if result.returncode == 0 or not proof_failure:
        raise SystemExit(f'ERROR: semantic mutation {name} did not have the expected proof failure')
report = {'source_sha256': hashlib.sha256(source.encode()).hexdigest(), 'controls': records}
(root / 'CONTROL_RESULTS.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
