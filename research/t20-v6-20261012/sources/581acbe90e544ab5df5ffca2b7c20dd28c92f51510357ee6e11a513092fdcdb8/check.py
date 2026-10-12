#!/usr/bin/env python3
"""Replay only the reviewed module and independent controls; retain dependencies."""
from pathlib import Path
import argparse, hashlib, json, os, subprocess
parser = argparse.ArgumentParser()
parser.add_argument('--workspace', type=Path, required=True, help='Retained toolchain and dependency workspace')
parser.add_argument('--output', type=Path, required=True, help='Fresh, previously nonexistent replay directory')
args = parser.parse_args()
root = Path(__file__).resolve().parent
workspace = args.workspace.resolve()
out = args.output.resolve()
out.mkdir(parents=True, exist_ok=False)
lib = out / 'fresh-lib'
lib.mkdir()
old_workspace = Path(root.joinpath('lean_path.txt').read_text().strip().split(':')[1]).parent.parent
paths = root.joinpath('lean_path.txt').read_text().strip().split(':')[1:]
paths = [str(workspace / Path(path).relative_to(old_workspace)) for path in paths]
env = os.environ.copy()
env['LEAN_PATH'] = ':'.join([str(lib), *paths])
lean = workspace / '.toolchains/lean-4.19.0-linux/bin/lean'
results = {}
for name, expected in [('InductionRigidityConverse', 0), ('PositiveControls', 0)] + [(p.stem, 1) for p in sorted(root.glob('Negative*.lean'))]:
    command = [str(lean), '--trust=0']
    if expected == 0:
        command += ['-o', str(lib / (name + '.olean'))]
    command += [str(root / (name + '.lean'))]
    run = subprocess.run(command, env=env, capture_output=True, text=True)
    log = run.stdout + run.stderr
    (out / (name + '.log')).write_text(log)
    passed = (run.returncode == 0) if expected == 0 else (run.returncode != 0 and 'error:' in log)
    results[name] = {'exit_code': run.returncode, 'expected_exit': expected, 'pass': passed}
    print(name, run.returncode, 'PASS' if passed else 'FAIL')
(out / 'REPLAY.json').write_text(json.dumps(results, indent=2) + '\n')
raise SystemExit(0 if all(r['pass'] for r in results.values()) else 1)
