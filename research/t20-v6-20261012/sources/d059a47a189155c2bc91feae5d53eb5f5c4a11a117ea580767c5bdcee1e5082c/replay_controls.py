#!/usr/bin/env python3
"""Replay only four reviewed finite scripts, using copies outside this archive.

No network, installs, protected writes, original-file writes, or ancestor campaigns.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.metadata
import json
import os
import platform
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, help='A new directory outside the archive')
    args = parser.parse_args()
    out = Path(args.output).resolve()
    assert not out.exists(), 'Output directory must not already exist'
    assert out != ROOT and ROOT not in out.parents, 'Output must be outside the archive'
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    integrity = subprocess.run([sys.executable, '-B', str(ROOT/'verify_preservation.py')],
                               capture_output=True, text=True, check=True, env=env)
    version = importlib.metadata.version('sympy')
    assert version == '1.14.0', 'Pinned replay requires SymPy 1.14.0; no install is performed'
    before = {str(p.relative_to(ROOT)):sha(p) for p in ROOT.rglob('*') if p.is_file()}
    out.mkdir(parents=True)
    work = out/'workspace'
    shutil.copytree(ROOT/'workspace', work)
    specs = [
        ('finite-author', 'bayes-feasibility-compatibility-20261010/verify.py',
         'CHECK_RESULTS.json', 10, 'exact_bytes'),
        ('finite-independent-review', 'bayes-feasibility-review-20261010/independent_controls.py',
         'INDEPENDENT_CHECK_RESULTS.json', 9, 'semantic_without_runtime'),
        ('fixed-prior-author', 'constrained-learning-possibility-20261010/verify.py',
         'CHECK_RESULTS.json', 12, 'exact_bytes'),
        ('fixed-prior-independent-review', 'constrained-learning-review-20261010/independent_controls.py',
         'INDEPENDENT_CONTROL_RESULTS.json', 4, 'exact_bytes'),
    ]
    records = []
    for label, rel, result_name, groups, comparison in specs:
        script = work/rel
        expected_script = ROOT/'workspace'/rel
        assert script.read_bytes() == expected_script.read_bytes()
        result = script.with_name(result_name)
        original_result = expected_script.with_name(result_name)
        start = time.monotonic()
        run = subprocess.run([sys.executable, '-B', str(script)], cwd=work,
                             capture_output=True, text=True, timeout=600, env=env)
        (out/(label+'.stdout.txt')).write_text(run.stdout)
        (out/(label+'.stderr.txt')).write_text(run.stderr)
        assert run.returncode == 0, (label,run.returncode,run.stderr)
        observed = json.loads(result.read_text())
        expected = json.loads(original_result.read_text())
        assert observed['status'] == 'PASS' and observed['control_groups'] == groups
        if comparison == 'exact_bytes':
            assert result.read_bytes() == original_result.read_bytes(), label
        else:
            observed.pop('runtime', None)
            expected.pop('runtime', None)
            assert observed == expected, label
        records.append({'label':label,'script':rel,'script_sha256':sha(expected_script),
                        'status':'PASS','control_groups':groups,
                        'output_comparison':comparison,'output_sha256':sha(result),
                        'seconds':round(time.monotonic()-start,3)})
    after = {str(p.relative_to(ROOT)):sha(p) for p in ROOT.rglob('*') if p.is_file()}
    assert before == after, 'Archive changed during replay'
    receipt = {'status':'PASS','scope':'35 exact finite control groups from four copied scripts. No measure theorem checker, ancestor campaign, formal-kernel certificate or new mathematical review.',
               'python':sys.version,'platform':platform.platform(),'sympy':version,
               'integrity':json.loads(integrity.stdout),'controls':records,
               'archive_unchanged':True,'total_control_groups':sum(r['control_groups'] for r in records)}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':'PASS','control_groups':35,'receipt':str(out/'REPLAY_RECEIPT.json')},sort_keys=True))

if __name__ == '__main__':
    main()
