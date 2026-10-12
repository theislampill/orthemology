#!/usr/bin/env python3
"""Replay declared finite checks in a fresh copy; never alters the frozen input.

Uses the installed Python standard library. Reviewed scripts are executed as code;
this is not a sandbox for arbitrary packages or a proof of universal statements.
"""
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
from verify_return import verify, safe_path, digest


def replay(root,out):
    root=Path(root).resolve();out=Path(out).resolve()
    if out.exists() or out.is_relative_to(root):raise ValueError('Output must be absent and outside the frozen input')
    identity=verify(root)
    checks=json.loads((root/'PYTHON_REPLAY.json').read_text())['checks']
    seen=set()
    for c in checks:
        if not re.fullmatch(r'[a-z][a-z0-9-]*',c['id']) or c['id'] in seen:raise ValueError('Invalid or duplicate check ID')
        seen.add(c['id'])
        p=safe_path(root,c['script'])
        if p.suffix!='.py' or not p.is_file():raise ValueError('Missing Python source')
        for key in ('expected','generated','cwd'):
            if key in c:safe_path(root,c[key])
    out.mkdir(parents=True);work=out/'work';shutil.copytree(root,work)
    receipt={'status':'RUNNING','input_manifest_sha256':identity['manifest_sha256'],
      'driver_sha256':digest(Path(__file__).read_bytes()),'python':sys.version,
      'scope':'Declared finite execution and identity checks only; no universal theorem or host attestation',
      'results':[]}
    def save():(out/'RESULT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    save()
    try:
        for c in checks:
            args=[]
            for x in c.get('args',[]):
                if '{out}' in x:x=x.replace('{out}',str(out))
                args.append(x)
            script=safe_path(work,c['script'])
            cwd=safe_path(work,c['cwd']) if 'cwd' in c else work
            start=time.monotonic()
            env={k:v for k,v in os.environ.items() if not k.startswith('PYTHON')}
            env['PYTHONDONTWRITEBYTECODE']='1'
            run=subprocess.run([sys.executable,'-E','-s','-B',str(script),*args],cwd=cwd,env=env,capture_output=True,text=True)
            log=out/(c['id']+'.log');log.write_text(run.stdout+run.stderr)
            row={'id':c['id'],'script_sha256':digest(script.read_bytes()),'exit_code':run.returncode,
                 'elapsed_seconds':time.monotonic()-start,'log':log.name,'log_sha256':digest(log.read_bytes())}
            receipt['results'].append(row)
            if run.returncode!=0:raise ValueError('Check failed: '+c['id'])
            if 'expected' in c:
                expected=safe_path(root,c['expected'])
                generated=safe_path(out,c['generated_out']) if 'generated_out' in c else safe_path(work,c['generated'])
                ignored=c.get('ignore_top_level_fields',[])
                if ignored:
                    a=json.loads(expected.read_text());b=json.loads(generated.read_text())
                    a={k:v for k,v in a.items() if k not in ignored};b={k:v for k,v in b.items() if k not in ignored}
                    equal=a==b
                else:equal=expected.read_bytes()==generated.read_bytes()
                row.update({'receipt_sha256':digest(generated.read_bytes()),'receipt_equal':equal,'ignored_runtime_fields':ignored})
                if not equal:raise ValueError('Changed scientific receipt: '+c['id'])
            if 'stdout' in c and run.stdout.strip()!=c['stdout']:raise ValueError('Unexpected checker response: '+c['id'])
            save()
        verify(root)
        receipt['status']='PASS_DECLARED_PYTHON_CHECKS';save();return receipt
    except Exception as e:
        receipt['status']='FAIL';receipt['error']=str(e);save();raise


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    p.add_argument('--out',type=Path,required=True)
    a=p.parse_args();r=replay(a.root,a.out)
    print(json.dumps({'status':r['status'],'checks':len(r['results']),'input_manifest_sha256':r['input_manifest_sha256']},indent=2))


if __name__=='__main__':main()
