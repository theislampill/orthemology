#!/usr/bin/env python3
"""Run unchanged frozen replay scripts in a new, isolated output workspace."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from verify_archive import safe_path, sha, verify

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out', type=Path, required=True)
args = parser.parse_args()
root = Path(__file__).resolve().parent
out = args.out.resolve()
assert not out.exists() and not out.is_relative_to(root), 'Choose a new output directory outside this archive.'
before = verify(root)
plan = json.loads((root / 'REPLAY_PLAN.json').read_text())
sources = json.loads((root / 'PRESERVED_SOURCES.json').read_text())['files']
work = out / 'workspace'
logs = out / 'logs'
work.mkdir(parents=True)
logs.mkdir()
for record in sources:
    dest = safe_path(work, record['path'])
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes((root / record['path']).read_bytes())
snapshot_count = 0
for review in plan['reviews']:
    review_root = work / review['directory']
    bindings = json.loads((review_root / 'SNAPSHOT_BINDINGS.json').read_text())
    for name, record in bindings['files'].items():
        data = (root / name).read_bytes()
        assert sha(data) == record['sha256'] and len(data) == record['bytes']
        dest = safe_path(review_root / 'snapshot', name)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data)
        snapshot_count += 1
env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONHASHSEED': '0'}
commands = []
for i, step in enumerate(plan['commands'], 1):
    command = [sys.executable] + step['arguments']
    cwd = work / step['cwd']
    start = time.monotonic()
    result = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    log = logs / (str(i).zfill(2) + '-' + step['name'] + '.log')
    log.write_text(result.stdout)
    record = {'name': step['name'], 'command': command, 'cwd': step['cwd'], 'exit_code': result.returncode,
              'seconds': round(time.monotonic()-start, 3), 'log': str(log.relative_to(out)),
              'log_sha256': sha(log.read_bytes())}
    commands.append(record)
    if result.returncode:
        (out / 'REPLAY_RECEIPT.json').write_text(json.dumps({'status': 'FAIL', 'commands': commands}, indent=2) + '\n')
        raise RuntimeError(result.stdout)
    print(step['name'], 'PASS', flush=True)
regenerated = {}
for path in plan['result_files']:
    data = (work / path).read_bytes()
    regenerated[path] = {'sha256': sha(data), 'result': json.loads(data)}
for item in plan['deterministic_outputs']:
    assert (work / item['replayed']).read_bytes() == (root / item['canonical']).read_bytes(), item
after = verify(root)
assert before == after
receipt = {'status': 'PASS_SCOPED', 'scope': plan['scope'], 'python_version': sys.version,
           'canonical_archive_hashes_preserved': True, 'preserved_original_files': before['preserved_original_files'],
           'review_snapshot_copies_materialized': snapshot_count,
           'actual_frozen_scripts_executed': True, 'commands': commands, 'regenerated_results': regenerated,
           'deterministic_outputs_byte_identical': plan['deterministic_outputs'],
           'limitations': plan['limitations']}
(out / 'REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PASS_SCOPED: all listed replay/check commands passed; canonical archived bytes unchanged.', flush=True)
