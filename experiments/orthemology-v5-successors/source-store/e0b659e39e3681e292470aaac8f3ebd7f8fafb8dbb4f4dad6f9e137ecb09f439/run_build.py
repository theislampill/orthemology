"""Run only the two retained upstream build commands, with isolated paths."""
from pathlib import Path
import argparse, datetime, hashlib, json, subprocess, time, sys
from context import isolated_environment

ROOT=Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,v): p.write_text(json.dumps(v,indent=2)+'\n')

def main():
    if sys.flags.optimize: raise ValueError('Assertions must be enabled')
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True)
    p.add_argument('stage',choices=['widget','dependencies']);a=p.parse_args()
    A=a.work.resolve();D=A/'dependencies';E=A/'evidence';env=isolated_environment(A)
    T=Path(json.loads((A/'config.json').read_text())['toolchain'])
    assert json.loads((E/'CLEAN_START.json').read_text())['status']=='CLEAN_START_VERIFIED'
    if a.stage=='widget':
        label='WIDGET_SOURCE_BUILD';cwd=D/'proofwidgets'
        assert not list(D.rglob('*.olean')) and not list(D.rglob('*.ilean'))
        cmd=[str(T/'bin/lake'),'--packages',str(A/'widget-package-overrides.json'),'--no-cache','--rehash','--verbose','build','widgetJsAll']
    else:
        label='DEPENDENCY_COLD_BUILD';cwd=A/'lake-driver'
        assert json.loads((E/'WIDGET_SOURCE_ASSETS.json').read_text())['status']=='PASS'
        assert json.loads((E/'COMPILER_PARSED_SOURCE_CLOSURE.json').read_text())['status']=='PASS'
        assert not [f for d in D.iterdir() for f in d.glob('.lake/build/lib/lean/**/*.olean')]
        assert not list((A/'lake-driver/.lake/build/lib/lean').glob('**/*.olean'))
        configs=[f.relative_to(A).as_posix() for f in D.rglob('*.olean')]
        assert configs==['dependencies/proofwidgets/.lake/lakefile.olean'],configs
        write(E/'PRE_PROOF_BUILD_CLEAN.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'third_party_proof_objects':0,'configuration_olean_paths':configs,'widget_assets_source_built':True})
        cmd=[str(T/'bin/lake'),'--no-cache','--rehash','--verbose','build']+['+'+r for r in json.loads((ROOT/'inputs/DEPENDENCY_CLOSURE.json').read_text())['roots']]
    receipt=E/(label+'.json');log=E/(label+'.log')
    if receipt.exists() or log.exists():raise ValueError('Preserve existing attempt; do not overwrite build evidence')
    start=datetime.datetime.now(datetime.timezone.utc);begin=time.monotonic()
    rec={'label':label,'cwd':str(cwd),'command':cmd,'start_utc':start.isoformat(),'environment_overrides':json.loads((A/'environment.json').read_text()),'status':'RUNNING'}
    write(receipt,rec)
    with log.open('w') as f:
        proc=subprocess.Popen(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
        while proc.poll() is None:
            write(E/'CURRENT_PROGRESS.json',{'label':label,'status':'RUNNING','pid':proc.pid,'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':round(time.monotonic()-begin,3),'fresh_dependency_objects':sum(len(list(d.glob('.lake/build/lib/lean/**/*.olean'))) for d in D.iterdir())})
            try:proc.wait(timeout=30)
            except subprocess.TimeoutExpired:pass
    rec.update(status='PASS' if proc.returncode==0 else 'FAIL',exit_code=proc.returncode,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=round(time.monotonic()-begin,3),log_sha256=sha(log))
    write(receipt,rec);write(E/'CURRENT_PROGRESS.json',rec)
    print(json.dumps(rec,indent=2));return proc.returncode

if __name__=='__main__':sys.exit(main())
