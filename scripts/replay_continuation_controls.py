#!/usr/bin/env python3
"""Replay exact standard-library controls; finite checks are not general proofs."""
import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import validate_research_continuations as v


def validate_suite(suite,sources,root):
    v.keys(suite,{'schema','id','steps'})
    v.require(suite['schema']=='orthemology-native-controls-v1','Unknown native suite')
    v.require(re.fullmatch('[a-z0-9][a-z0-9-]*',suite['id']),'Unsafe native suite ID')
    steps=v.indexed(suite['steps'],'id');v.require(bool(steps),'Empty native suite')
    for step in steps.values():
        v.keys(step,{'id','files','entry','outputs','args'})
        v.require(re.fullmatch('[a-z0-9][a-z0-9-]*',step['id']),'Unsafe control ID')
        files=v.indexed(step['files'],'path')
        v.require(step['entry'] in files and step['entry'].endswith('.py'),'Missing Python control entry')
        v.require(isinstance(step['args'],list) and all(isinstance(x,str) for x in step['args']),'Invalid control arguments')
        v.require(isinstance(step['outputs'],list) and len(step['outputs'])==len(set(step['outputs'])),'Duplicate control output')
        for path in step['outputs']:v.safe_relative(path)
        v.require(not set(step['outputs'])&set(files),'Output would replace original input')
        for row in files.values():
            v.keys(row,{'path','source_id'});v.safe_relative(row['path'])
            v.require(row['source_id'] in sources,'Unknown native source')
            source=sources[row['source_id']]
            v.require(source['projection']=='EXACT' and source['path'] is not None,'Native controls need exact public source bytes')
            p=v.path_in(root,source['path'])
            v.require(v.sha(p)==source['sha256'],'Changed native source')


def replay(root,suite,sources,out,timeout=600):
    root=Path(root).resolve();out=Path(out).resolve()
    v.require(sys.version_info[:3]==(3,11,9),'Native replay requires exact Python 3.11.9')
    v.require(not out.exists() and not out.is_relative_to(root),'Output must be absent and outside repository')
    validate_suite(suite,sources,root)
    out.mkdir(parents=True)
    receipt={'status':'RUNNING','suite_id':suite['id'],'python':sys.version.split()[0],
             'steps':[],'scope':'Exact finite Python controls; no kernel, continuum-proof or world-warrant credit.'}
    def save():(out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    save()
    try:
        for step in suite['steps']:
            work=out/step['id'];work.mkdir()
            hashes={}
            for row in step['files']:
                source=sources[row['source_id']];p=work/row['path'];p.parent.mkdir(parents=True,exist_ok=True)
                raw=v.path_in(root,source['path']).read_bytes()
                import hashlib
                v.require(hashlib.sha256(raw).hexdigest()==source['sha256'],'Source changed during staging')
                p.write_bytes(raw);hashes[row['path']]=v.sha(p)
            env={k:value for k,value in os.environ.items() if k not in {'PYTHONOPTIMIZE','PYTHONPATH','PYTHONHOME'}}
            # -E ignores inherited interpreter flags; -B prevents source pollution.
            proc=subprocess.run([sys.executable,'-E','-B',step['entry'],*step['args']],cwd=work,env=env,
                                capture_output=True,timeout=timeout)
            log=out/(step['id']+'.log');log.write_bytes(proc.stdout+b'\n'+proc.stderr)
            row={'id':step['id'],'exit_code':proc.returncode,'source_hashes':hashes,'log_sha256':v.sha(log)}
            receipt['steps'].append(row);save()
            v.require(proc.returncode==0,'Native control failed: '+step['id'])
            for name,h in hashes.items():v.require(v.sha(v.path_in(work,name))==h,'Control changed its input')
            actual={p.relative_to(work).as_posix() for p in work.rglob('*') if p.is_file() or p.is_symlink()}
            v.require(actual==set(hashes)|set(step['outputs']),'Unexpected or missing control output')
            row['output_hashes']={name:v.sha(v.path_in(work,name)) for name in step['outputs']}
        validate_suite(suite,sources,root)
        receipt['status']='PASS_NATIVE_CONTROLS';save();return receipt
    except (ValueError,OSError,subprocess.TimeoutExpired) as exc:
        receipt['status']='FAILED';receipt['error']=str(exc);save();raise ValueError('Native replay failed; see external receipt') from exc


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    ap.add_argument('--suite',required=True);ap.add_argument('--out',type=Path,required=True)
    args=ap.parse_args();root=args.root.resolve();v.validate(root)
    registry=v.read_json(root/v.AREA/'registry.json')
    suites={v.read_json(root/p)['id']:v.read_json(root/p) for p in registry.get('native_suites',[])}
    v.require(args.suite in suites,'Unknown native suite')
    sources=v.indexed(v.read_json(root/registry['source_map'])['sources'],'id')
    result=replay(root,suites[args.suite],sources,args.out)
    print(json.dumps({'status':result['status'],'suite_id':result['suite_id'],'steps':len(result['steps'])}))


if __name__=='__main__':
    try:main()
    except ValueError as exc:raise SystemExit(str(exc))
