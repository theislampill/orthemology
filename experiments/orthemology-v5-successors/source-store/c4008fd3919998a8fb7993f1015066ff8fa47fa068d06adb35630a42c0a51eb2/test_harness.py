#!/usr/bin/env python3
"""Byte-preservation and fresh-output regression tests on disposable copies."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

p = argparse.ArgumentParser()
p.add_argument('--source', type=Path, required=True)
p.add_argument('--lean', type=Path, required=True)
p.add_argument('--record', type=Path, required=True)
a = p.parse_args()
source = a.source.resolve()
lean = a.lean.resolve()
record = a.record.resolve()
if record.exists():
    raise SystemExit('Refusing to overwrite an existing test record')
if record == source or source in record.parents:
    raise SystemExit('Test record must be outside the sealed source tree')

payload = ['ModalUnion.lean', 'FiniteControls.lean', 'AxiomAudit.lean',
           'negative-controls/RejectedClaims.lean', 'replay.sh',
           'README.txt', 'STATEMENT_CONTRACT.txt', 'AXIOM_AUDIT.txt']
if (source / 'test_harness.py').is_file():
    payload.append('test_harness.py')

def snapshot(root):
    found = {}
    for q in sorted(root.rglob('*')):
        key = str(q.relative_to(root))
        if q.is_symlink():
            found[key] = ['symlink', os.readlink(q)]
        elif q.is_file():
            found[key] = ['file', hashlib.sha256(q.read_bytes()).hexdigest()]
        elif q.is_dir():
            found[key] = ['directory']
    return found

results = []
with tempfile.TemporaryDirectory(prefix='modal-union-guard-test-') as tmp:
    tmp = Path(tmp)
    for case in ['existing_output', 'source_descendant', 'source_equal',
                 'source_symlink_alias', 'normal_fresh']:
        case_root = tmp / case
        sealed = case_root / 'input'
        sealed.mkdir(parents=True)
        for name in payload:
            dest = sealed / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source / name, dest)
        (sealed / 'source-sentinel.txt').write_bytes(b'sealed source sentinel\n')
        if case == 'existing_output':
            out = case_root / 'existing-output'
            out.mkdir()
            (out / 'core.log').write_bytes(b'historical core log sentinel\n')
            (out / 'sentinel.bin').write_bytes(b'\x00historical output\xff')
        elif case == 'source_descendant':
            out = sealed / 'forbidden-output'
        elif case == 'source_equal':
            out = sealed
        elif case == 'source_symlink_alias':
            alias = case_root / 'input-alias'
            alias.symlink_to(sealed, target_is_directory=True)
            out = alias / 'forbidden-output'
        else:
            out = case_root / 'fresh-output'
        before_source = snapshot(sealed)
        before_output = snapshot(out) if out.is_dir() else None
        run = subprocess.run(['bash', str(sealed / 'replay.sh'), str(out)],
                             cwd=case_root, env=dict(os.environ, LEAN_BIN=str(lean)),
                             text=True, capture_output=True)
        unchanged_source = snapshot(sealed) == before_source
        unchanged_output = before_output is None or snapshot(out) == before_output
        if case == 'normal_fresh':
            passed = run.returncode == 0 and unchanged_source and (out / 'RESULT.txt').exists()
        else:
            passed = run.returncode != 0 and unchanged_source and unchanged_output
            if before_output is None:
                passed = passed and not out.exists()
        results.append({'case': case, 'passed': passed, 'exit_code': run.returncode,
                        'source_bytes_and_paths_unchanged': unchanged_source,
                        'existing_output_bytes_and_paths_unchanged': unchanged_output,
                        'stdout': run.stdout, 'stderr': run.stderr})
record.write_text(json.dumps({'source': str(source), 'cases': results,
                              'all_passed': all(r['passed'] for r in results)}, indent=2) + '\n')
for r in results:
    print(r['case'], 'PASS' if r['passed'] else 'FAIL', 'exit', r['exit_code'])
raise SystemExit(0 if all(r['passed'] for r in results) else 1)
