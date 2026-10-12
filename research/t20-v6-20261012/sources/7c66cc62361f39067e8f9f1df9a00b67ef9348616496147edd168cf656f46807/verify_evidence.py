"""Replay local and isolated extraction layouts; record hashes and exit codes."""
from pathlib import Path
from datetime import datetime,timezone
import os,sys,json,hashlib,subprocess,tempfile,shutil,re
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def execute(cmd,cwd):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
    p=subprocess.run(cmd,cwd=cwd,env=env,text=True,capture_output=True)
    return {'command':cmd,'cwd':str(cwd),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}

def main():
    bindings=json.loads((BASE/'SOURCE_BINDINGS.json').read_text())
    before={r['path']:digest(ROOT/r['path']) for r in bindings['files']}
    mismatch=[r['path'] for r in bindings['files'] if before[r['path']]!=r['sha256']]
    if mismatch:raise RuntimeError('Bound input mismatch: '+repr(mismatch))
    test=execute([sys.executable,str(BASE/'src/test_production_contract.py')],ROOT)
    (BASE/'results/FINAL_TESTS.log').write_text(test['stdout']+test['stderr'])
    export=execute([sys.executable,str(BASE/'src/export_results.py')],ROOT)
    expected_results=(BASE/'results/RESULTS.json').read_bytes()
    deps=json.loads((BASE/'DELIVERY_DEPENDENCIES.json').read_text())
    with tempfile.TemporaryDirectory(prefix='t20-effect-production-') as temp:
        iso=Path(temp);rel=BASE.relative_to(ROOT)
        for path in (BASE/'src').glob('*.py'):
            dest=iso/path.relative_to(ROOT);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,dest)
        (iso/rel/'results').mkdir(parents=True,exist_ok=True)
        for record in deps['runtime_dependencies']:
            dest=iso/record['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/record['path'],dest)
        code="import sys;from pathlib import Path;sys.path.insert(0,str(Path('t20-continuation-20261008/effect-production/src').resolve()));import production_contract as p;assert p.ROOT==Path.cwd();assert Path(p.inherited.__file__).is_relative_to(p.ROOT);assert Path(p.reactive.__file__).is_relative_to(p.ROOT);print(p.ROOT);print(p.inherited.__file__);print(p.reactive.__file__)"
        imports=execute([sys.executable,'-c',code],iso)
        isolated=execute([sys.executable,str(iso/rel/'src/test_production_contract.py')],iso)
        isoexport=execute([sys.executable,str(iso/rel/'src/export_results.py')],iso)
        exact_results=(iso/rel/'results/RESULTS.json').read_bytes()==expected_results
    after={r['path']:digest(ROOT/r['path']) for r in bindings['files']}
    evidence={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'local_tests':test,'local_export':export,
              'isolated_import_paths':imports,'isolated_tests':isolated,'isolated_export':isoexport,
              'isolated_results_exact_match':exact_results,'bound_inputs_unchanged':before==after,
              'bound_input_count':len(before),'runtime_dependencies_copied':len(deps['runtime_dependencies']),
              'test_count':int(re.search(r'Ran (\d+) tests',test['stderr']).group(1)),
              'scope':'Replay and extraction verification, not additional scientific credit.'}
    (BASE/'results/VERIFICATION.json').write_text(json.dumps(evidence,indent=2)+'\n')
    success=all(x['exit_code']==0 for x in (test,export,imports,isolated,isoexport)) and exact_results and before==after
    print(json.dumps({k:evidence[k] for k in ('test_count','bound_input_count','bound_inputs_unchanged','isolated_results_exact_match')}))
    return 0 if success else 1

if __name__=='__main__':raise SystemExit(main())
