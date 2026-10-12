#!/usr/bin/env python3
"""Replay unchanged fifth-checkpoint controls in a disposable copy."""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[1]
P = 't20-next-frontier-20261008/'
COMMANDS = [
    ('grouped-author', 'grouped-calibration-invariants/exact_controls.py', ['grouped-calibration-invariants/results/exact_controls.json'], None),
    ('grouped-review', 'grouped-calibration-invariants-review/independent_controls.py', ['grouped-calibration-invariants-review/results/independent_controls.json'], 'grouped-calibration-invariants-review/results/independent_controls.json'),
    ('stable-author', 'stable-grouped-invariants/exact_controls.py', ['stable-grouped-invariants/results/exact_controls.json', 'stable-grouped-invariants/results/GRID_WITNESS.json'], None),
    ('stable-review', 'stable-grouped-invariants-review/exact_checks.py', [], 'stable-grouped-invariants-review/exact_checks.json'),
    ('interaction-author', 'interaction-calibration-anchor/exact_controls.py', ['interaction-calibration-anchor/results/exact_controls.json'], 'interaction-calibration-anchor/results/exact_controls.json'),
    ('interaction-panel', 'interaction-calibration-anchor/panel_controls.py', ['interaction-calibration-anchor/results/panel_controls.json'], 'interaction-calibration-anchor/results/panel_controls.json'),
    ('interaction-review', 'interaction-calibration-anchor-review/independent_controls.py', [], 'interaction-calibration-anchor-review/INDEPENDENT_CONTROLS.json'),
    ('interaction-panel-review', 'interaction-calibration-anchor-review/independent_panel_controls.py', ['interaction-calibration-anchor-review/INDEPENDENT_PANEL_CONTROLS.json'], 'interaction-calibration-anchor-review/INDEPENDENT_PANEL_CONTROLS.json'),
    ('absence-author', 'interaction-absence-obstruction/exact_controls.py', ['interaction-absence-obstruction/results/exact_controls.json'], 'interaction-absence-obstruction/results/exact_controls.json'),
    ('absence-review', 'interaction-absence-obstruction-review/independent_controls.py', ['interaction-absence-obstruction-review/INDEPENDENT_CONTROLS.json'], 'interaction-absence-obstruction-review/INDEPENDENT_CONTROLS.json'),
    ('transport-author', 'historical-mathematical-transport/exact_controls.py', [], 'historical-mathematical-transport/CONTROL_RESULTS.json'),
    ('transport-review', 'historical-mathematical-transport-review/independent_controls.py', [], 'historical-mathematical-transport-review/CONTROL_RESULTS.json'),
]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(): return {p.relative_to(ROOT).as_posix(): sha(p) for p in ROOT.rglob('*') if p.is_file()}

parser = argparse.ArgumentParser()
parser.add_argument('--output', required=True)
args = parser.parse_args()
out = Path(args.output).resolve()
assert out != ROOT and ROOT not in out.parents, 'Replay results must stay outside frozen checkpoint'
out.mkdir(parents=True, exist_ok=True)
before = snapshot()
checks = []
with tempfile.TemporaryDirectory(prefix='t20-fifth-controls-') as temp:
    work = Path(temp) / 'copy'
    shutil.copytree(ROOT, work)
    for name, script, generated, stdout_target in COMMANDS:
        for output in generated:
            (work/(P+output)).unlink(missing_ok=True)
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', PYTHONOPTIMIZE='0')
        proc = subprocess.run([sys.executable, P+script], cwd=work, env=env,
                              capture_output=True, timeout=900)
        (out/(name+'.stdout.log')).write_bytes(proc.stdout)
        (out/(name+'.stderr.log')).write_bytes(proc.stderr)
        row = {'name': name, 'command': ['python3', P+script], 'script_sha256': sha(ROOT/(P+script)),
               'exit_code': proc.returncode, 'generated_outputs': []}
        for output in generated:
            expected, actual = ROOT/(P+output), work/(P+output)
            row['generated_outputs'].append({'path': P+output, 'expected_sha256': sha(expected),
                 'actual_sha256': sha(actual) if actual.exists() else None,
                 'byte_match': actual.is_file() and actual.read_bytes()==expected.read_bytes()})
        if stdout_target:
            expected = ROOT/(P+stdout_target)
            row.update({'stdout_target': P+stdout_target, 'expected_stdout_sha256': sha(expected),
                        'actual_stdout_sha256': hashlib.sha256(proc.stdout).hexdigest(),
                        'stdout_byte_match': proc.stdout==expected.read_bytes()})
        row['status'] = 'PASS' if proc.returncode==0 and all(x['byte_match'] for x in row['generated_outputs']) and row.get('stdout_byte_match', True) else 'FAIL'
        checks.append(row)
        print(name, row['status'], flush=True)

unchanged = before == snapshot()
receipt = {'created_utc': datetime.now(timezone.utc).isoformat(),
           'classification': 'DELIVERY_ASSURANCE_ONLY_NO_ACTIVE_RESEARCH_CREDIT',
           'python': sys.version, 'dependencies': 'Python standard library only; no additional packages',
           'checks': checks, 'checkpoint_bytes_unchanged': unchanged,
           'fresh_Lean_replay_performed': False, 'historical_research_reintegration': False,
           'status': 'PASS' if unchanged and all(x['status']=='PASS' for x in checks) else 'FAIL'}
(out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
assert receipt['status']=='PASS', receipt
