#!/usr/bin/env python3
"""Isolated portable replay; Python standard library plus official Lean 4.19.0."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parent
INPUTS=['verify_attribution.py','UnknownRootAttribution.lean',
        'dependencies/DynamicInterlock.lean','dependencies/CoveringCore.lean']


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--lean',required=True,help='Official Lean 4.19.0 executable')
    parser.add_argument('--output-dir',default=str(ROOT/'verification-replay'))
    args=parser.parse_args()
    lean=str(Path(args.lean).resolve())
    version=subprocess.check_output([lean,'--version'],text=True).strip()
    if 'version 4.19.0,' not in version:raise SystemExit('Wrong pinned Lean compiler: '+version)
    out=Path(args.output_dir).resolve()
    if out==ROOT:raise SystemExit('Output directory must be separate from frozen source payload.')
    out.mkdir(parents=True,exist_ok=True)
    for item in json.loads((ROOT/'DEPENDENCY_BINDING.json').read_text())['formal_dependency_copies']:
        assert digest(ROOT/item['path'])==item['sha256']
    steps=[]
    with tempfile.TemporaryDirectory(prefix='root-attribution-replay-') as raw:
        work=Path(raw);(work/'dependencies').mkdir();(work/'build').mkdir()
        for name in INPUTS:shutil.copyfile(ROOT/name,work/name)
        commands=[
            ('finite',[os.sys.executable,'verify_attribution.py'],{}),
            ('core_lean',[lean,'-o','build/DynamicInterlock.olean','dependencies/DynamicInterlock.lean'],{}),
            ('cover_lean',[lean,'-o','build/CoveringCore.olean','dependencies/CoveringCore.lean'],{'LEAN_PATH':str(work/'build')}),
            ('attribution_lean',[lean,'UnknownRootAttribution.lean'],{'LEAN_PATH':str(work/'build')}),
        ]
        for name,command,extra in commands:
            result=subprocess.run(command,cwd=work,env={**os.environ,**extra},text=True,
                                  stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
            log=out/(name+'.log');log.write_text(result.stdout)
            if result.returncode or 'sorryAx' in result.stdout:
                raise SystemExit(f'Failed {name}, exit {result.returncode}; inspect {log}')
            steps.append({'step':name,'exit_code':result.returncode,'log':log.name,'sha256':digest(log)})
        for name in ['ATTRIBUTION_CHECK_RESULTS.json','ATTRIBUTION_COUNTEREXAMPLES.json']:
            shutil.copyfile(work/name,out/name)
    receipt={
        'status':'PASS_AUTHOR_ISOLATED_REPLAY',
        'independent_review':'External additive review binding is separate from this executable verification.',
        'lean_version':version,'steps':steps,
        'source_sha256':{name:digest(ROOT/name) for name in INPUTS},
        'formal_scope':['tainted-label bound B+c-1','sound overlap and cancellation witnesses',
                        'pointwise maximal-label-fault realization','exact actual-root cardinality of that realization',
                        'minimum actual-root arithmetic'],
        'ordinary_only_scope':['sharp cross-image iff and forced-bridge corner',
                               'arbitrary fixed-family impossibility','covering/binomial search lower bound'],
        'not_claimed':['arbitrary adaptive alias-discovery impossibility','label failure independence',
                       'actual map oracle','physical implementation certification','fixed R5 defeat'],
        'finite_results':json.loads((out/'ATTRIBUTION_CHECK_RESULTS.json').read_text()),
    }
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
