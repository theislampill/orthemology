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
