#!/usr/bin/env python3
"""Require intended type errors, rejecting failed imports or other accidental errors."""
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent.parent
controls = sorted((ROOT/'verification/negative-controls').glob('*.lean'))
assert len(controls) == 9, 'Unexpected negative-control inventory'
for control in controls:
    name = str(control.relative_to(ROOT))
    result = subprocess.run(['lake', 'env', 'lean', name], cwd=ROOT,
                            stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    errors = [line for line in result.stdout.splitlines() if ': error:' in line]
    expected = (result.returncode == 1 and len(errors) == 1
                and re.search(r': error: (?:application )?type mismatch', errors[0]))
    if not expected:
        print(result.stdout)
        raise SystemExit(f'UNEXPECTED CONTROL RESULT: {name}; exit={result.returncode}; errors={errors}')
    print(f'EXPECTED TYPE REJECTION: {name}')
print('NEGATIVE_CONTROLS_PASS: 9 intended type errors; these are interface controls, not logical independence proofs.')
