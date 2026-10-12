#!/usr/bin/env python3
"""Portable frozen-payload replay, writing all new results outside this delivery."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from datetime import datetime, timezone
sys.dont_write_bytecode = True
from verify_delivery import verify

ROOT = Path(__file__).resolve().parent
p = argparse.ArgumentParser()
p.add_argument('--output-dir', required=True, help='New directory outside this delivery')
args = p.parse_args()
out = Path(args.output_dir).resolve()
if out == ROOT or ROOT in out.parents:
    raise RuntimeError('Replay output must be outside the frozen delivery')
if out.exists():
    raise RuntimeError('Replay output directory must not already exist')
pre = verify()
out.mkdir(parents=True)
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
author = ROOT/'fibrewise-split-correction-20261011'
review = ROOT/'fibrewise-split-independent-review-20261011'
root = ROOT/'fibrewise-split-root-controls-20261011'
commands = []


def run(label, cmd, cwd):
    result = subprocess.run(cmd, cwd=cwd, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    log = out/(label+'.log')
    log.write_text(result.stdout)
    commands.append({'label':label, 'argv':cmd, 'cwd':str(cwd), 'exit_code':result.returncode, 'log':str(log.relative_to(out)), 'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
    if result.returncode:
        (out/'FAILED_COMMANDS.json').write_text(json.dumps(commands,indent=2)+'\n')
        raise RuntimeError(label + ' failed; see ' + str(log))
    print(label + ': PASS', flush=True)


for mode in ['normal','optimized']:
    python = [sys.executable, '-B'] + (['-O'] if mode == 'optimized' else [])
    run('author-unit-'+mode, python+['-m','unittest','discover','-s',str(author),'-p','test_*.py','-v'], out)
    run('author-controls-'+mode, python+[str(author/'verify.py'),'--output-dir',str(out/('author-'+mode))], out)
    run('review-controls-'+mode, python+[str(review/'check.py'),'--output',str(out/('review-'+mode+'.json'))], out)
    run('review-implementation-'+mode, python+[str(review/'implementation_controls.py'),'--author-dir',str(author),'--output',str(out/('implementation-'+mode+'.json'))], out)
    rootcopy = out/('root-'+mode)
    rootcopy.mkdir()
    shutil.copyfile(root/'check.py',rootcopy/'check.py')
    run('root-controls-'+mode, python+[str(rootcopy/'check.py')], rootcopy)

post = verify()
classes = {}
for mode in ['normal','optimized']:
    a = json.loads((out/('author-'+mode)/'CHECKS.json').read_text())['checks']
    r = json.loads((out/('review-'+mode+'.json')).read_text())['checks']
    im = json.loads((out/('implementation-'+mode+'.json')).read_text())['checks']
    rc = json.loads((out/('root-'+mode)/'CHECKS.json').read_text())['checks']
    author_classes = {'symbolic_or_rational':0,'numerical_high_precision':0,'numerical_floating_point':0,'snapshot_integrity':0}
    for check in a:
        if check['name'].startswith(('snapshot hash ','original unchanged ')):
            key='snapshot_integrity'
        elif check.get('kind') == 'numerical high precision':
            key='numerical_high_precision'
        elif check.get('kind') == 'numerical floating point':
            key='numerical_floating_point'
        elif check.get('kind') == 'exact':
            key='symbolic_or_rational'
        else:
            raise RuntimeError('Unknown author check class: '+repr(check))
        author_classes[key] += 1
    numerical_start = next(i for i,c in enumerate(r) if c['name']=='atomic_mixture_KL_below_kernel_bound')
    impl_gates = sum(c['name'].startswith('reject_') for c in im)
    classes[mode] = {'author_controls':author_classes,'review_controls':{'symbolic_or_rational':numerical_start,'numerical':len(r)-numerical_start},'review_implementation':{'input_validation_regressions':impl_gates,'numerical_fixture_oracles':len(im)-impl_gates},'root_controls':{'symbolic_or_rational':len(rc)},'author_unit_suite':'13 test methods: implementation fixtures and input validation, including complex-input regressions; see unit log'}

receipt = {'status':'PASS','finished_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'dependencies':{name:importlib.metadata.version(name) for name in ['numpy','sympy','mpmath','scipy']},'pre_integrity':pre,'post_integrity':post,'commands':commands,'evidence_classification':classes,'limits':['Normal and optimized modes rerun the same evidence; they are not independent witnesses.','Root algebra shares the author fixture; repeated fixtures are not independent mathematical proof.','The reviewer scripts are separately written but still finite controls, not proofs of general law-level claims.','Numerical and implementation checks have no certified error guarantee for all inputs.','Integrity checks establish byte identity, not mathematical correctness.','No source bodies, downloads, original workspace paths, or external predecessor files are required.','No general all-law PDE existence, unique Trotter limit, finite-mixture reaction closure, or programme closure is established.']}
(out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: normal and optimized replay; frozen delivery remains byte-identical')
print(out/'REPLAY_RECEIPT.json')
