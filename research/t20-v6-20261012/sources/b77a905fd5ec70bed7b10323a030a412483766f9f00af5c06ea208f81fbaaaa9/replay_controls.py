#!/usr/bin/env python3
"""Replay only portable controls into external outputs. No network or writes to payloads."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
CASES = [
    {'name': 'matrix-author', 'packet': 'matrix-rank-gaussian-entrance-20261011',
     'script': 'verify.py', 'option': '--output', 'expected': 31,
     'exact': 27, 'numerical': 0, 'bindings': 4, 'style': 'matrix-author'},
    {'name': 'matrix-independent', 'packet': 'matrix-rank-independent-review-20261011',
     'script': 'independent_controls.py', 'option': '--output', 'expected': 51,
     'exact': 42, 'numerical': 0, 'bindings': 9, 'style': 'matrix-review'},
    {'name': 'matrix-root-isotropic', 'packet': 'matrix-rank-root-controls-20261011',
     'script': 'check_isotropic.py', 'option': None, 'expected': 15,
     'exact': 15, 'numerical': 0, 'bindings': 0, 'style': 'root'},
    {'name': 'conditional-author', 'packet': 'conditional-entropy-control-20261011',
     'script': 'verify.py', 'option': '--output-dir', 'expected': 42,
     'exact': 28, 'numerical': 9, 'bindings': 5, 'style': 'conditional-author'},
    {'name': 'conditional-independent', 'packet': 'conditional-entropy-independent-review-20261011',
     'script': 'check.py', 'option': '--output', 'expected': 30,
     'exact': 30, 'numerical': 0, 'bindings': 0, 'style': 'conditional-review'},
    {'name': 'conditional-root', 'packet': 'conditional-entropy-root-controls-20261011',
     'script': 'check.py', 'option': None, 'expected': 9,
     'exact': 9, 'numerical': 0, 'bindings': 0, 'style': 'root'},
]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command, log_base, env):
    p = subprocess.run(command, cwd=log_base.parent, env=env,
                       text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    log_base.with_suffix('.stdout.txt').write_text(p.stdout)
    log_base.with_suffix('.stderr.txt').write_text(p.stderr)
    if p.returncode:
        raise RuntimeError(f'Command failed ({p.returncode}): {command}; see {log_base}')
    return p


def classified(data, case):
    count = data.get('count', data.get('check_count'))
    if count != case['expected']:
        raise RuntimeError(f"Unexpected count for {case['name']}: {count}")
    if case['style'] == 'root':
        if len(data['checks']) != case['expected'] or not all(v is True for v in data['checks'].values()):
            raise RuntimeError('Failed root controls: ' + case['name'])
        return case['exact'], 0, 0
    if data.get('status', '').lower() != 'pass':
        raise RuntimeError('Nonpassing result: ' + case['name'])
    if case['style'] == 'matrix-author':
        items = data['exact_controls']
        bindings = sum(name.startswith('input ') for name in items)
        return len(items) - bindings, 0, bindings
    if case['style'] == 'matrix-review':
        items = data['controls']
        bindings = sum(name.startswith(('author freeze ', 'predecessor snapshot ')) for name in items)
        return len(items) - bindings, 0, bindings
    if case['style'] == 'conditional-author':
        items = data['checks']
        if not all(item['passed'] for item in items):
            raise RuntimeError('Nonpassing conditional author control')
        return (sum(item['kind'] == 'exact' for item in items),
                sum(item['kind'] == 'numerical high precision' for item in items),
                sum(item['kind'] == 'integrity' for item in items))
    # The independent conditional checker's 30 controls contain no input bindings.
    if len(data['checks']) != case['expected'] or not all(item['pass'] for item in data['checks']):
        raise RuntimeError('Nonpassing conditional independent control')
    return case['exact'], 0, 0


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output-dir', required=True, type=Path)
    args = p.parse_args()
    out = args.output_dir.resolve()
    if out == ROOT or ROOT in out.parents:
        raise RuntimeError('Output directory must be outside the frozen archive tree')
    out.mkdir(parents=True, exist_ok=False)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    initial = [sys.executable, '-B', str(ROOT / 'verify_archive.py'), '--output', str(out / 'manifest-before.json')]
    run(initial, out / 'verify-before', env)
    results = []
    for case in CASES:
        modes = []
        for mode, flag in [('normal', []), ('optimized', ['-O'])]:
            target = out / case['name'] / mode
            target.mkdir(parents=True)
            source = ROOT / case['packet'] / case['script']
            output = target / 'CHECKS.json'
            if case['option'] is None:
                # The unmodified root checker writes CHECKS.json beside itself.
                script = target / case['script']
                shutil.copy2(source, script)
                if sha(script) != sha(source):
                    raise RuntimeError('External script copy mismatch')
                command = [sys.executable, '-B', *flag, str(script)]
            else:
                value = str(target if case['option'] == '--output-dir' else output)
                command = [sys.executable, '-B', *flag, str(source), case['option'], value]
            run(command, target / 'command', env)
            data = json.loads(output.read_text())
            counts = classified(data, case)
            expected = (case['exact'], case['numerical'], case['bindings'])
            if counts != expected:
                raise RuntimeError(f"Unexpected classification for {case['name']}: {counts} != {expected}")
            modes.append({'mode': mode, 'command': command, 'exit_code': 0,
                          'output': str(output), 'sha256': sha(output), 'checks': case['expected'],
                          'author_labelled_exact_mathematical_controls': counts[0],
                          'high_precision_numerical_controls': counts[1], 'source_bindings': counts[2]})
        equal = modes[0]['sha256'] == modes[1]['sha256']
        if not equal:
            raise RuntimeError('Normal/optimized JSON differs: ' + case['name'])
        results.append({'case': case['name'], 'normal_optimized_outputs_equal': equal, 'runs': modes})
        print(f"{case['name']}: {case['expected']} checks pass in both modes; identical outputs", flush=True)
    final = [sys.executable, '-B', str(ROOT / 'verify_archive.py'), '--output', str(out / 'manifest-after.json')]
    run(final, out / 'verify-after', env)
    if (out / 'manifest-before.json').read_bytes() != (out / 'manifest-after.json').read_bytes():
        raise RuntimeError('Manifest verification changed during replay')
    import sympy, mpmath
    receipt = {'status': 'pass', 'python': sys.version, 'sympy': sympy.__version__, 'mpmath': mpmath.__version__,
               'archive_root': str(ROOT), 'payload_unchanged': True, 'cases': results,
               'excluded_from_fresh_replay': [
                   'Five conditional-author --original-root bindings: external predecessor paths are intentionally not required.',
                   'Inherited archived replays are preserved evidence, not rerun or counted as independent fresh mathematical tests.',
                   'Cumulative-warrant private source bodies and visual reading: omitted; only the shareable manifest can be authenticated.',
                   'Three conditional-author primary-source bodies are intentionally omitted; the preserved author manifest is historical evidence, not a claim that every listed source body is delivered.',
                   'Source interpretation, analytic proof validity, formal proof, general PDE existence/uniqueness, and programme closure are not certified by these finite controls.'],
               'counting_note': 'Normal and optimized runs are repetitions. Math controls, numerical checks, integrity bindings and independent evidence are not interchangeable; overlap is not a novelty measure.'}
    (out / 'REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(str(out / 'REPLAY_RECEIPT.json'))


if __name__ == '__main__':
    main()
