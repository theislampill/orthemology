#!/usr/bin/env python3
"""Replay both control suites outside the frozen author and review packets."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

HERE = Path(__file__).resolve().parent
AUTHOR = HERE.parent / 'completion-bayes-commutation-20261010'


def verify_manifest(root):
    manifest = json.loads((root / 'MANIFEST.json').read_text())
    for row in manifest['files']:
        relative = Path(row['path'])
        if relative.is_absolute() or '..' in relative.parts:
            raise RuntimeError('Unsafe manifest path')
        data = (root / relative).read_bytes()
        if len(data) != row['bytes'] or hashlib.sha256(data).hexdigest() != row['sha256']:
            raise RuntimeError('Manifest mismatch: ' + str(root / relative))
    return len(manifest['files'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('output_dir', type=Path)
    parser.add_argument('--verify-original-inputs', type=Path)
    args = parser.parse_args()
    output = args.output_dir.resolve()
    if output.exists() or any(output == root or root in output.parents for root in (HERE, AUTHOR)):
        raise RuntimeError('Use a new output directory outside both preserved packets')
    pins = json.loads((HERE / 'AUTHOR_PINS.json').read_text())
    for name, digest in pins['sha256'].items():
        if hashlib.sha256((AUTHOR / name).read_bytes()).hexdigest() != digest:
            raise RuntimeError('Author pin mismatch: ' + name)
    review_count = verify_manifest(HERE)
    author_count = verify_manifest(AUTHOR)
    output.mkdir(parents=True)
    command = [sys.executable, str(AUTHOR / 'replay.py'), str(output / 'author')]
    if args.verify_original_inputs is not None:
        command += ['--verify-original-inputs', str(args.verify_original_inputs.resolve())]
    author = subprocess.run(command, text=True, capture_output=True)
    (output / 'author_replay_stdout.txt').write_text(author.stdout)
    (output / 'author_replay_stderr.txt').write_text(author.stderr)
    if author.returncode:
        raise RuntimeError('Author replay failed; see output logs')
    independent = subprocess.run([sys.executable, str(HERE / 'independent_controls.py'),
                                  '--output-dir', str(output / 'independent')], text=True, capture_output=True)
    (output / 'independent_verification.txt').write_text(independent.stdout)
    (output / 'independent_stderr.txt').write_text(independent.stderr)
    if independent.returncode:
        raise RuntimeError('Independent controls failed; see output logs')
    for produced, preserved in [
        (output / 'author' / 'CONTROL_RESULTS.json', HERE / 'author_replay' / 'CONTROL_RESULTS.json'),
        (output / 'author' / 'verification.txt', HERE / 'author_replay' / 'verification.txt'),
        (output / 'independent' / 'REVIEW_CONTROLS.json', HERE / 'REVIEW_CONTROLS.json'),
        (output / 'independent_verification.txt', HERE / 'independent_verification.txt'),
        (output / 'independent_stderr.txt', HERE / 'independent_stderr.txt'),
    ]:
        if produced.read_bytes() != preserved.read_bytes():
            raise RuntimeError('Replay differs: ' + str(produced))
    assert verify_manifest(HERE) == review_count
    assert verify_manifest(AUTHOR) == author_count
    author_receipt = json.loads((output / 'author' / 'REPLAY_RECEIPT.json').read_text())
    receipt = {
        'status': 'PASS',
        'scope': 'Frozen byte checks and exact author/independent control replay; not a new theorem review or programme closure.',
        'review_manifest_sha256': hashlib.sha256((HERE / 'MANIFEST.json').read_bytes()).hexdigest(),
        'review_manifest_files_verified': review_count,
        'author_manifest_sha256': pins['sha256']['MANIFEST.json'],
        'author_manifest_files_verified': author_count,
        'direct_original_inputs_verified': author_receipt['original_inputs_verified'],
        'author_assertion_groups': 24,
        'independent_assertion_groups': 15,
        'regenerated_json_and_stdout_byte_identical': True,
        'preserved_packets_unchanged': True,
    }
    (output / 'REVIEW_REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))


if __name__ == '__main__':
    main()
