#!/usr/bin/env python3
"""Bounded archive-integrity negative controls; never edit retained sources."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
TARGET = Path('fixed-marginal-correction-20261011/RESULT.md')


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def changed(copy):
    path = copy / TARGET
    data = path.read_bytes()
    path.write_bytes(bytes([data[0] ^ 1]) + data[1:])


def missing(copy):
    (copy / TARGET).unlink()


def extra(copy):
    (copy / 'UNLISTED.txt').write_text('Inventory-control payload only.\n')


def duplicate(copy):
    path = copy / 'MANIFEST.json'
    data = json.loads(path.read_text())
    data['files'].append(dict(data['files'][0]))
    path.write_text(json.dumps(data))


def unsafe(copy):
    path = copy / 'MANIFEST.json'
    data = json.loads(path.read_text())
    data['files'][0]['path'] = '../outside-evidence.txt'
    path.write_text(json.dumps(data))


def symlink(copy):
    path = copy / TARGET
    path.unlink()
    path.symlink_to('README.md')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    require(output != ROOT and ROOT not in output.parents,
            'test output must be outside the evidence tree')
    require(not output.exists(), 'test output already exists')
    cases = [('changed', changed, 'manifest byte/hash mismatch'),
             ('missing', missing, 'inventory mismatch'),
             ('extra', extra, 'inventory mismatch'),
             ('duplicate-entry', duplicate, 'duplicate manifest path'),
             ('unsafe-path', unsafe, 'unsafe or noncanonical manifest path'),
             ('symlink', symlink, 'symlinks are not permitted')]
    rows = []
    for mode in ([], ['-O']):
        original = subprocess.run([sys.executable] + mode + [str(ROOT/'replay.py'), '--inventory-only'],
                                  capture_output=True, text=True)
        require(original.returncode == 0, 'untampered inventory failed: ' + original.stderr)
        for label, mutation, expected in cases:
            with tempfile.TemporaryDirectory(prefix='fixed-marginal-inventory-') as temp:
                copy = Path(temp) / 'evidence'
                shutil.copytree(ROOT, copy)
                mutation(copy)
                result = subprocess.run([sys.executable] + mode + [str(copy/'replay.py'), '--inventory-only'],
                                        capture_output=True, text=True)
                passed = result.returncode != 0 and expected in result.stderr
                row = {'mode': 'optimized' if mode else 'normal', 'case': label,
                       'expected_failure': expected, 'returncode': result.returncode,
                       'stdout': result.stdout, 'stderr': result.stderr, 'passed': passed}
                rows.append(row)
                require(passed, 'inventory mutation was not rejected as expected: ' + repr(row))
    receipt = {'status': 'PASS', 'untampered_inventory_checks': 2,
               'rejected_mutations': len(rows), 'checks': rows,
               'scope': 'Packaging integrity only; no mathematical proof or independent review.'}
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'untampered_inventory_checks': 2,
                      'rejected_mutations': len(rows), 'output': str(output)}))


if __name__ == '__main__':
    main()
