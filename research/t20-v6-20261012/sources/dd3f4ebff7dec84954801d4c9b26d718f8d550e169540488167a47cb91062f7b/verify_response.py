#!/usr/bin/env python3
"""Verify this response's bytes and replay its bounded unchanged controls.

This is packaging/replay machinery, not another scientific validation layer.
No network access or external original workspace is needed. Source controls
run in a temporary isolated directory and cannot rewrite package evidence.
"""
from pathlib import Path
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[1]


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def checked_relative(name):
    path = Path(name)
    require(not path.is_absolute() and '..' not in path.parts,
            'Unsafe manifest path: ' + name)
    return path


def verify_inventory():
    manifest = json.loads((ROOT / 'MANIFEST.json').read_text())
    expected = set()
    for row in manifest['files']:
        name = row['path']
        require(name not in expected, 'Duplicate manifest entry: ' + name)
        expected.add(name)
        path = ROOT / checked_relative(name)
        require(path.is_file() and not path.is_symlink(), 'Missing or linked file: ' + name)
        require(path.stat().st_size == row['bytes'] and digest(path) == row['sha256'],
                'Package byte mismatch: ' + name)
    entries = list(ROOT.rglob('*'))
    require(not any(p.is_symlink() for p in entries), 'Symbolic links are not package evidence')
    actual = {str(p.relative_to(ROOT)) for p in entries if p.is_file()}
    require(actual == expected | {'MANIFEST.json'}, 'Package inventory has missing or extra files')
    return len(expected)


def verify_local_custody():
    custody = json.loads((ROOT / 'INPUT_CUSTODY.json').read_text())
    for row in custody['copied_artifacts']:
        path = ROOT / checked_relative(row['package_path'])
        require(path.stat().st_size == row['bytes'] and digest(path) == row['sha256'],
                'Copied artifact differs from recorded source: ' + row['package_path'])
    snapshots = []
    omitted = []
    for row in custody['existing_comparison_inputs']:
        if 'package_snapshot' in row:
            path = ROOT / checked_relative(row['package_snapshot'])
            require(path.stat().st_size == row['bytes'] and digest(path) == row['sha256'],
                    'Included input snapshot mismatch: ' + row['path'])
            snapshots.append(row['package_snapshot'])
        else:
            omitted.append(row['path'])
    return {'included_comparison_snapshots_checked': len(snapshots),
            'omitted_comparison_inputs_not_reopened': len(omitted)}


def run(command, cwd):
    result = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    require(result.returncode == 0,
            'Control failed: ' + ' '.join(command) + '\n' + result.stdout + result.stderr)
    return result.stdout


def main():
    require(len(sys.argv) == 1, 'This verifier takes no arguments')
    count = verify_inventory()
    custody = verify_local_custody()
    flags = ['-B'] + (['-O'] if sys.flags.optimize else [])
    with tempfile.TemporaryDirectory(prefix='synthesis-response-controls-') as temporary:
        work = Path(temporary)
        support_name = 'synthesis-warrant-scope-20261011'
        support = work / support_name
        support.mkdir()
        shutil.copyfile(ROOT / support_name / 'support_scope_check.py', support / 'support_scope_check.py')
        source_dir = Path('intrinsic-necessity-bridge-20261009/sources')
        shutil.copytree(ROOT / source_dir, work / source_dir)
        support_stdout = run([sys.executable, *flags, str(support / 'support_scope_check.py')], work)
        support_result = json.loads((support / 'CHECK_RESULTS.json').read_text())
        prior_support = json.loads((ROOT / support_name / 'CHECK_RESULTS.json').read_text())
        require(support_result == prior_support, 'Support output changed from the preserved worker receipt')
        require(support_result['status'] == 'PASS' and support_result['check_count'] == 33,
                'Unexpected support-scope check result')

        timing_name = 'synthesis-hybrid-timing-review-20261011'
        timing = work / timing_name
        shutil.copytree(ROOT / timing_name, timing)
        timing_stdout = run([sys.executable, *flags, str(timing / 'checks.py')], work)
        timing_result = json.loads(timing_stdout)
        prior_file = 'CHECKS_OPTIMISED.json' if sys.flags.optimize else 'CHECKS.json'
        prior_timing = json.loads((ROOT / timing_name / prior_file).read_text())
        # The original run checked workspace originals. A portable replay checks
        # the same hashed snapshots, without pretending those originals exist.
        prior_timing['original_sources_checked'] = False
        require(timing_result == prior_timing, 'Timing output differs beyond the declared custody mode')
        require(timing_result['status'] == 'PASS' and timing_result['control_groups'] == 8,
                'Unexpected timed-control result')
    require(verify_inventory() == count, 'Control replay changed the package')
    result = {
        'status': 'PASS',
        'mode': 'optimized' if sys.flags.optimize else 'normal',
        'scope': 'Package byte integrity and bounded response controls; scoped internal comparison only',
        'manifest_files_checked': count,
        'custody': custody,
        'support_scope_checks': support_result['check_count'],
        'timing_control_groups': timing_result['control_groups'],
        'timing_original_workspace_sources_checked': False,
        'source_pdf_bytes_or_images_checked': False,
        'original_26_test_corpus_rerun': False,
        'lean_replay': False,
        'package_unchanged_after_replay': True,
        'support_stdout': support_stdout.strip(),
        'timing_checks': timing_result['checks'],
    }
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
