#!/usr/bin/env python3
"""Run only explicitly scoped finite controls in a disposable copy, never source files in place."""
import argparse
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
from validate_package import verify_files, verify_projection

ROOT = Path(__file__).resolve().parent
SUITES = {
    'finite-contracts': {'directory':'finite-contracts','commands':[
        ['-B','-m','unittest','discover','-s','.','-p','test_contracts.py','-v'],
        ['-O','-B','-m','unittest','discover','-s','.','-p','test_contracts.py','-v'],
        ['-B','exhaustive_oracle.py']], 'dependencies':[],
        'scope':'26 finite contract tests (normal and optimized) plus finite exhaustive oracle; not universal proof or archive inventory verification.'},
    'grouped-author': {'directory':'grouped-source-audit-gradient-20261011','commands':[['-B','check_exact.py'],['-O','-B','check_exact.py']], 'dependencies':['sympy'],
        'scope':'Exact finite/symbolic author controls; public wrapper binds included original-byte snapshots only. No private workspace check or formal kernel proof.'},
    'grouped-independent': {'directory':'grouped-audit-independent-review','commands':[['-B','check_grouped_covariance.py']], 'dependencies':['sympy'],
        'scope':'Independent symbolic grouped covariance and singleton failure controls; assertions preserved, no optimized-mode assertion claim.'},
    'high-order-author': {'directory':'positive-high-order-correction-20261011','commands':[['-B','check.py']], 'dependencies':['sympy','mpmath'],
        'scope':'Finite exact/symbolic controls plus explicitly numerical diagnostics; not universal measure proof or formal verification.'},
    'high-order-independent': {'directory':'high-order-law-independent-review-20261011','commands':[['-B','check_independent.py']], 'dependencies':['sympy','mpmath'],
        'scope':'Independent finite and numerical controls; not kernel proof.'},
}


# Separately dated consolidation-depth reassessment targets.
SUITES.update({'finite-contracts-reconstructed': {'directory': 'finite-contracts-reconstructed',
                                    'commands': [['-B',
                                                  '-m',
                                                  'unittest',
                                                  'discover',
                                                  '-s',
                                                  '.',
                                                  '-p',
                                                  'test_*.py',
                                                  '-v'],
                                                 ['-O',
                                                  '-B',
                                                  '-m',
                                                  'unittest',
                                                  'discover',
                                                  '-s',
                                                  '.',
                                                  '-p',
                                                  'test_*.py',
                                                  '-v'],
                                                 ['-B', 'exhaustive_oracle.py'],
                                                 ['-O', '-B', 'exhaustive_oracle.py']],
                                    'dependencies': [],
                                    'scope': '30 tests: 26 inherited plus four reconstructed '
                                             'input-boundary regressions, normal/optimized; '
                                             'unchanged finite exhaustive oracle both modes. '
                                             'Separate successor candidate, not R3, not the '
                                             '52-to-55 line or general Iterable support.'},
 'audit-refinement': {'directory': 'audit-refinement',
                      'commands': [['-B', 'run_portable.py'], ['-O', '-B', 'run_portable.py']],
                      'dependencies': ['sympy'],
                      'scope': 'Exact mathematical author checker, 14 groups/3054 counted controls '
                               'and public fixture checks, normal/optimized. Derived '
                               'public-fixture binding replaces private assembly-location '
                               'verification; universal theorem rests on written proof.'},
 'restricted-controls': {'directory': 'restricted-controls',
                         'commands': [['-B', 'verify.py'], ['-O', '-B', 'verify.py']],
                         'dependencies': ['sympy'],
                         'scope': '31 exact restricted-control fixtures, normal/optimized. '
                                  'Ordinary universal proof and domain guards separate.'},
 'depth-independent': {'directory': 'depth-independent',
                       'commands': [['-B', 'check_independent.py'],
                                    ['-O', '-B', 'check_independent.py']],
                       'dependencies': ['sympy'],
                       'scope': '62 independent exact checks, normal/optimized; not a formal '
                                'kernel proof. Reviewer contributed tagged-instrument corollary '
                                'proof; review is not independent corroboration of that '
                                'contribution.'},
 'foundational-scope': {'directory': 'foundational-scope',
                        'commands': [['-B',
                                      'synthesis-warrant-scope-20261011/support_scope_check.py'],
                                     ['-O',
                                      '-B',
                                      'synthesis-warrant-scope-20261011/support_scope_check.py']],
                        'dependencies': [],
                        'scope': '33 inherited source/dependency checks with exact owner inputs, '
                                 'normal/optimized; not new theorem, human-warrant classification '
                                 'or Lean build.'},
 'pro-exact-controls': {'directory': 'pro-exact-controls',
                        'commands': [['-B', 'independent_exact_controls.py']],
                        'dependencies': [],
                        'scope': 'New supplied exact-rational finite validation, normal Python '
                                 'only because bare assertions would be removed by optimization; '
                                 'independent formulas do not replay actual later integrator.'},
 'contract-downstream': {'directory': 'contract-downstream',
                         'commands': [['-B', 'run_probe.py']],
                         'dependencies': [],
                         'scope': 'New explicit old/repaired Python dependency comparison; 162 '
                                  'checks/125 rows in both modes with byte-identical caller '
                                  'outputs, original single dependency pin rejects new bytes. No '
                                  'historical rebind, whole 3097-pin verifier, Lean build or all '
                                  'Python-observable equivalence.'}})

SUITES.update({'depth-joint-correction': {'directory': 'depth-joint-correction', 'commands': [['-B', 'check_joint.py', '--output', 'REPLAY.json'], ['-O', '-B', 'check_joint.py', '--output', 'REPLAY_OPTIMIZED.json']], 'dependencies': ['sympy', 'mpmath'], 'scope': 'Exact author mathematical program and portable exact source fixtures; finite controls and high-precision diagnostics, not universal proof or R3 comparison.'}, 'depth-semantic-geometry': {'directory': 'depth-semantic-geometry', 'commands': [['-B', 'check_controls.py'], ['-O', '-B', 'check_controls.py']], 'dependencies': ['sympy'], 'scope': 'Exact author symbolic and finite controls using portable source fixtures; not an enumeration proof of uncountable semantic claims.'}, 'depth-proof-inquiry': {'directory': 'depth-proof-inquiry', 'commands': [['-B', '-m', 'unittest', 'discover', '-s', '.', '-p', 'test_*.py', '-v'], ['-O', '-B', '-m', 'unittest', 'discover', '-s', '.', '-p', 'test_*.py', '-v']], 'dependencies': [], 'scope': '19 portable cache/policy tests with three exact inherited modules. Original workspace preservation verifier is retained as source, not advertised as portable.'}, 'depth-uncertainty-inquiry': {'directory': 'depth-uncertainty-inquiry', 'commands': [['-B', 'check_exact.py'], ['-O', '-B', 'check_exact.py']], 'dependencies': [], 'scope': 'Exact rational finite controls with fourteen exact read-ledger fixtures, normal and optimized. Written continuum and minimax proofs remain separate.'}, 'depth-grounding-provenance': {'directory': 'depth-grounding-provenance', 'commands': [['-B', 'run_portable.py']], 'dependencies': [], 'scope': 'Exact author finite relation controls and unchanged engine. Normal only: bare assertions make optimized execution non-evidence. Derived driver changes only catalogue ROOT.'}, 'depth-decision-representation': {'directory': 'depth-decision-representation', 'commands': [['-B', 'check_exact.py'], ['-O', '-B', 'check_exact.py']], 'dependencies': [], 'scope': 'Exact finite loss/profile certificates. Not a continuum proof by enumeration or fresh Lean build.'}, 'depth-collective-continuation': {'directory': 'depth-collective-continuation', 'commands': [['-B', 'CONTROL_CHECKS.py'], ['-O', '-B', 'CONTROL_CHECKS.py']], 'dependencies': [], 'scope': 'Exact finite linked-signal Bayes risk, recalibration, rank and migration controls; not empirical or infinite-continuation proof replay.'}, 'depth-occurrence-warrant': {'directory': 'depth-occurrence-warrant', 'commands': [['-B', 'controls/contract_check.py'], ['-O', '-B', 'controls/contract_check.py'], ['-B', 'controls/verify_boundaries.py'], ['-O', '-B', 'controls/verify_boundaries.py'], ['-B', 'controls/inherited_t16/check.py']], 'dependencies': [], 'scope': 'Exact frozen seven-record source-view controls, deliberate boundary mutations, and inherited T16 checker normal-only. No Arabic authentication or human-warrant inference.'}})

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--list',action='store_true')
    parser.add_argument('--suite',choices=sorted(SUITES),default='finite-contracts')
    parser.add_argument('--timeout',type=int,default=300)
    args=parser.parse_args()
    if args.list:
        print(json.dumps(SUITES,indent=2));return
    verify_files(ROOT);verify_projection(ROOT)
    spec=SUITES[args.suite]
    dependencies={name:importlib.metadata.version(name) for name in spec['dependencies']}
    results=[]
    with tempfile.TemporaryDirectory(prefix='t20-selected-replay-') as temporary:
        work=Path(temporary)/'suite'
        shutil.copytree(ROOT/'replay'/spec['directory'],work)
        for flags in spec['commands']:
            start=time.monotonic()
            result=subprocess.run([sys.executable,*flags],cwd=work,capture_output=True,text=True,timeout=args.timeout,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
            output=result.stdout+result.stderr
            results.append({'python_arguments':flags,'exit_code':result.returncode,'seconds':round(time.monotonic()-start,3),'output_sha256':hashlib.sha256(output.encode()).hexdigest(),'output':output})
            if result.returncode:
                print(json.dumps({'status':'FAIL','suite':args.suite,'results':results},indent=2));raise SystemExit(result.returncode)
    print(json.dumps({'status':'PASS','suite':args.suite,'python_version':sys.version.split()[0],'dependencies':dependencies,'scope':spec['scope'],'results':results},indent=2))


if __name__=='__main__':main()
