#!/usr/bin/env python3
"""PRIVATE review candidate: exact START_HERE V3 vectors in a fresh work copy.

No shell, no network, no archive permission bits, no original-source writes.
This file has not been approved to execute scientific work. Adapter admission is
required and binds its hash to the source recipe and helper hashes.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, re, signal, subprocess

ANCHOR = '066e051e6c68174e4af4726f0376040f8d8cf488a78e128510ef9338536ff320'
LEAN_SHA = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
PYTHON_SHA = 'e50d468e8b0adfb05733f5b87b3cff34829c4a8c1aea50c865aa8bdfe4bb150f'
FIXTURE_SHA = 'e4ae2e2751535e625f245a1bb2f2e4f2f4c447a55c859e1b1c94dbbf48adf359'

def require(ok,message):
    if not ok:raise ValueError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def interrupted(signum,frame):raise SystemExit(128+signum)
def write(path,value):Path(path).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n',encoding='utf-8')
def inventory(root):
    result={}
    for p in sorted(root.rglob('*')):
        require(not p.is_symlink(),'Source contains a symlink')
        if p.is_file():result[p.relative_to(root).as_posix()]={'sha256':sha(p),'bytes':p.stat().st_size}
    return result

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-root',required=True,type=Path);ap.add_argument('--output',required=True,type=Path)
    ap.add_argument('--python',required=True,type=Path);ap.add_argument('--lean',required=True,type=Path);args=ap.parse_args()
    source=args.source_root.absolute();out=args.output.absolute();python=args.python.resolve();lean=args.lean.resolve()
    require(source.is_dir() and not source.is_symlink(),'Missing original source root')
    require(not out.exists() and not out.resolve().is_relative_to(source.resolve()),'Output must be absent and outside original source')
    require(sha(source/'START_HERE.md')==ANCHOR,'Wrong source recipe')
    require(sha(lean)==LEAN_SHA and sha(python)==PYTHON_SHA,'Wrong explicitly pinned tool executable')
    require(sha(source/'sources/proper-function-and-candidate-e.md')==FIXTURE_SHA and (source/'sources/proper-function-and-candidate-e.md').stat().st_size==3013,'Wrong original criterion fixture')
    before=inventory(source);out.mkdir(parents=True);(out/'logs').mkdir();work=out/'work';work.mkdir();build=out/'build';build.mkdir()
    files=['criterion_model.py','rule_install_model.py','bounded_audit.py','shared_fixture_check.py','rule_install_audit.py',
           'CriterionTransport.lean','TypedCriterionGuard.lean','CriterionInstallation.lean','ReplayCriterionFixtures.lean','ReplayRuleInstallation.lean']
    files += [p.relative_to(source).as_posix() for folder in ['tests','sources'] for p in sorted((source/folder).rglob('*')) if p.is_file()]
    for name in files:
        dest=work/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes((source/name).read_bytes())
    (work/'evidence').mkdir()
    env={k:v for k,v in os.environ.items() if not k.startswith(('LEAN_','PYTHON','LD_')) and k not in {'DYLD_INSERT_LIBRARIES'}}
    env.update({'PYTHONDONTWRITEBYTECODE':'1','LEAN_PATH':str(build),'PATH':os.pathsep.join([str(lean.parent),str(python.parent),os.defpath])})
    stages=[]
    signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    def run(name,argv,cwd=work,budget=600):
        require(not (out/'logs'/(name+'.log')).exists(),'Child log output exists')
        row={'id':name,'argv':[str(x) for x in argv],'cwd':str(cwd),'budget_seconds':budget,'started_at':now(),'terminal':'RUNNING','exit_code':None}
        stages.append(row);write(out/'STAGES.json',stages)
        with (out/'logs'/(name+'.log')).open('xb') as log:
            # These inspected children do not launch further child processes.
            # Inherit the outer run_scientific process group for outer cleanup.
            proc=subprocess.Popen(row['argv'],cwd=cwd,env=env,stdout=log,stderr=subprocess.STDOUT,shell=False)
            try:
                code=proc.wait(timeout=budget);row['terminal']='COMPLETED' if 0<=code<124 else 'INTERRUPTED';row['exit_code']=code if row['terminal']=='COMPLETED' else None
            except subprocess.TimeoutExpired:
                row['terminal']='TIMEOUT';proc.terminate()
                try:proc.wait(timeout=2)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
            except BaseException:
                row['terminal']='INTERRUPTED'
                if proc.poll() is None:
                    proc.terminate()
                    try:proc.wait(timeout=2)
                    except subprocess.TimeoutExpired:proc.kill();proc.wait()
                raise
            finally:
                row['ended_at']=now();log.flush()
                row['log_sha256']=sha(out/'logs'/(name+'.log'));write(out/'STAGES.json',stages)
        row['log_sha256']=sha(out/'logs'/(name+'.log'));write(out/'STAGES.json',stages)
        require(row['terminal']=='COMPLETED' and row['exit_code']==0,'Child did not complete successfully: '+name)
        return (out/'logs'/(name+'.log')).read_text()
    # Original recipe lines 49-60; relocation of fresh objects and generated data
    # preserves the source bytes and uses the same explicit source/interpreter.
    run('verify-bundle',[python,'-B',source/'verify_bundle.py'],source,120)
    unittest_log=run('python-tests',[python,'-B','-m','unittest','discover','-s','tests','-v'],budget=120)
    require(re.search(r'Ran 44 tests in ',unittest_log) and re.search(r'(?m)^OK\s*$',unittest_log),'Original 44 tests did not all pass')
    run('criterion-transport',[lean,'-j1',work/'CriterionTransport.lean'],budget=180)
    run('typed-criterion',[lean,'-j1','-o',build/'TypedCriterionGuard.olean',work/'TypedCriterionGuard.lean'],budget=180)
    run('criterion-installation',[lean,'-j1','-o',build/'CriterionInstallation.olean',work/'CriterionInstallation.lean'],budget=180)
    run('bounded-audit',[python,'-B',work/'bounded_audit.py'])
    run('repair-fixtures-generate',[python,'-B',work/'shared_fixture_check.py','generate'])
    run('repair-fixtures-lean',[lean,'-j1','--run',work/'ReplayCriterionFixtures.lean'],budget=1800)
    run('repair-fixtures-compare',[python,'-B',work/'shared_fixture_check.py','compare','--label','green'])
    run('install-fixtures-generate',[python,'-B',work/'rule_install_audit.py','generate'])
    run('install-fixtures-lean',[lean,'-j1','--run',work/'ReplayRuleInstallation.lean'],budget=600)
    run('install-fixtures-compare',[python,'-B',work/'rule_install_audit.py','compare'])
    def result(name):return json.loads((work/'evidence'/name).read_text())
    bounded=result('BOUNDED_AUDIT.json');repair=result('CROSS_LANGUAGE_GREEN.json');install=result('RULE_INSTALL_CROSS_LANGUAGE.json');install_bounded=result('RULE_INSTALL_BOUNDED_AUDIT.json')
    product=bounded['execution_product']
    require(product['state_command_pairs']==393216 and product['applied']==480 and product['rejected']==392736,'Wrong bounded repair product')
    require(repair['passed'] is True and repair['compared']==393216 and repair['mismatches']==0,'Wrong repair cross-language terminal')
    require(install['passed'] is True and install['python_rows']==4096 and install['lean_rows']==4096 and install['mismatches']==0,'Wrong installation cross-language terminal')
    require(install_bounded['cases']==4096 and install_bounded['applied']==8 and install_bounded['rejected']==4088,'Wrong bounded installation product')
    require(before==inventory(source),'Original source changed during execution')
    for name in files:require(sha(work/name)==before[name]['sha256'],'Scientific work-copy source changed')
    write(out/'RECIPE_RECEIPT.json',{'status':'PASS_ORIGINAL_CRITERION_V3_VECTORS','source_recipe_sha256':ANCHOR,
          'source_before':before,'source_after':inventory(source),'stages':stages,'repair':repair,'installation':install,
          'bounded_repair_product':product,'bounded_installation':install_bounded,'source_fixture_bytes':3013,'source_fixture_sha256':FIXTURE_SHA,
          'scope':'Complete original bounded suite; not all-input Python/Lean refinement, actual-world authority, or Candidate E adoption.'})

if __name__=='__main__':main()
