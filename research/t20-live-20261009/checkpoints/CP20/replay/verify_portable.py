#!/usr/bin/env python3
"""Verify checkpoint20 bytes and replay unchanged checkers in a new directory.

Python standard library only. This is syntactic/matrix checking, not Lean.
The package and selected original inputs are never written by this program.
"""
import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def canonical_review(value):
    value = copy.deepcopy(value)
    key = 'variable_sharing_cross_values'
    value[key] = sorted(value[key], key=lambda row: (row['a'], row['b'], row['value']))
    return value


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path,
                        help='New, nonexisting output directory outside the package')
    args = parser.parse_args()
    package = Path(__file__).resolve().parent.parent
    output = args.output.resolve()
    if output == package or package in output.parents:
        raise SystemExit('Output must be outside the package.')
    if output.exists():
        raise SystemExit('Refusing to overwrite an existing output directory.')
    manifest = json.loads((package / 'MANIFEST.json').read_text())
    files = manifest['files']
    checked = []
    for item in files:
        relative = PurePosixPath(item['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        path = package / relative
        assert path.is_file() and not path.is_symlink()
        assert path.stat().st_size == item['bytes'], item['path']
        assert digest(path) == item['sha256'], item['path']
        if path.suffix == '.json':
            json.loads(path.read_text())
        checked.append(item['path'])
    expected = set(checked) | {'MANIFEST.json', 'MANIFEST.sha256'}
    actual = {p.relative_to(package).as_posix() for p in package.rglob('*') if p.is_file()}
    assert actual == expected, (actual - expected, expected - actual)
    checksum_rows = {}
    for line in (package / 'MANIFEST.sha256').read_text().splitlines():
        sha, name = line.split('  ', 1)
        assert name not in checksum_rows
        checksum_rows[name] = sha
    assert set(checksum_rows) == set(checked) | {'MANIFEST.json'}
    assert all(digest(package / name) == sha for name, sha in checksum_rows.items())
    package_hashes_before = {name: digest(package / name) for name in sorted(actual)}
    inherited = 'necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md'
    assert digest(package / inherited) == '3ccb73001c99c976e728817ca9fca75ab128e6538578068f51333e5321f41b5b'
    output.mkdir(parents=True, exist_ok=False)
    replay = output / 'isolated'
    replay.mkdir()
    for dirname in ('compound-ground-necessity-20261009', 'compound-ground-review-20261009',
                    'necessary-truth-operative-basing-20261009'):
        shutil.copytree(package / dirname, replay / dirname)
    author = replay / 'compound-ground-necessity-20261009'
    review = replay / 'compound-ground-review-20261009'
    original_author = package / author.name
    original_review = package / review.name
    run_records = []

    def run(script, label, seed):
        env = dict(os.environ, PYTHONHASHSEED=str(seed), PYTHONDONTWRITEBYTECODE='1')
        proc = subprocess.run([sys.executable, str(script)], cwd=replay, env=env,
                              capture_output=True, text=True, timeout=300)
        (output / (label + '.stdout.txt')).write_text(proc.stdout)
        (output / (label + '.stderr.txt')).write_text(proc.stderr)
        record = {'label': label, 'python_hash_seed': seed, 'returncode': proc.returncode,
                  'script': script.relative_to(replay).as_posix(), 'script_sha256': digest(script)}
        run_records.append(record)
        assert proc.returncode == 0, record
        return record

    author_run = run(author / 'check_compound_ground.py', 'author', 0)
    author_comparisons = []
    for name in ('CHECK_RESULTS.json', 'VARIABLE_SHARING_REDUCTION.md'):
        same = (author / name).read_bytes() == (original_author / name).read_bytes()
        author_comparisons.append({'path': author.name + '/' + name,
                                   'byte_identical': same, 'replay_sha256': digest(author / name)})
        assert same, name
    baseline = json.loads((original_review / 'INDEPENDENT_RESULTS.json').read_text())
    independent_comparisons = []
    for seed in (0, 1):
        label = 'independent-seed-' + str(seed)
        run(review / 'independent_checks.py', label, seed)
        generated = review / 'INDEPENDENT_RESULTS.json'
        value = json.loads(generated.read_text())
        equal = canonical_review(value) == canonical_review(baseline)
        differences = sorted(k for k in set(value) | set(baseline) if value.get(k) != baseline.get(k))
        assert equal and set(differences) <= {'variable_sharing_cross_values'}
        assert len(value['variable_sharing_cross_values']) == 4
        assert len({tuple(sorted(r.items())) for r in value['variable_sharing_cross_values']}) == 4
        target = output / (label + '.INDEPENDENT_RESULTS.json')
        shutil.copyfile(generated, target)
        independent_comparisons.append({
            'python_hash_seed': seed,
            'byte_identical': generated.read_bytes() == (original_review / generated.name).read_bytes(),
            'canonical_equal': equal, 'different_fields': differences,
            'canonicalization': 'Only sort variable_sharing_cross_values by (a,b,value); preserve all other arrays, keys and values.',
            'replay_sha256': digest(generated)})
    # Changes inside the isolated copy are expected only for generated checker outputs.
    allowed = {author.name + '/CHECK_RESULTS.json', author.name + '/VARIABLE_SHARING_REDUCTION.md',
               review.name + '/INDEPENDENT_RESULTS.json'}
    nonoutput_checks = []
    for p in replay.rglob('*'):
        if p.is_file():
            rel = p.relative_to(replay).as_posix()
            if rel not in allowed:
                assert digest(p) == digest(package / rel), rel
                nonoutput_checks.append(rel)
    package_hashes_after = {name: digest(package / name) for name in sorted(actual)}
    assert package_hashes_before == package_hashes_after
    receipt = {
        'status': 'PASS', 'qualification': 'Python matrix and syntactic proof checks; no Lean or philosophical certification',
        'python': sys.version, 'manifest_files_checked': len(checked),
        'manifest_sha256': digest(package / 'MANIFEST.json'),
        'all_package_files_unchanged': True,
        'inherited_dependency_sha256': digest(package / inherited),
        'runs': run_records, 'author_comparisons': author_comparisons,
        'independent_comparisons': independent_comparisons,
        'nonoutput_copy_files_hash_verified': nonoutput_checks,
        'checks': {
            'axiom_assignments_per_checker': baseline['axiom_assignment_total'],
            'modus_ponens_pairs': baseline['modus_ponens_pairs'],
            'adjunction_pairs': baseline['adjunction_pairs'],
            'conditional_proof_lines': len(baseline['conditional_derivation']),
            'inherited_positive_proof_lines': len(baseline['positive_relevant_derivation']),
            'material_actual_assignments': baseline['material_actual_assignments'],
            'material_actual_sensitivity_failures': baseline['material_actual_sensitivity_failures'],
            'hypothesis_removal_rejected': baseline['conditional_derivation_rejected_without_H'],
            'wrong_consequent_rejected': baseline['wrong_final_consequent_rejected'],
            'corrupt_table_rejected': baseline['corrupt_table_entry_rejected_by_recomputed_A1']}}
    (output / 'REPLAY_RECEIPT.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(receipt, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
