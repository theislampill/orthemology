from pathlib import Path
from datetime import datetime,timezone
import os,sys,subprocess,tempfile,shutil,json,hashlib,re
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def run(path,cwd):
    p=subprocess.run([sys.executable,str(path)],cwd=cwd,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),text=True,capture_output=True)
    return {'path':str(path),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}

def main():
    bindings=json.loads((BASE/'SOURCE_BINDINGS.json').read_text());inputs=bindings['files']
    before={r['path']:sha(ROOT/r['path']) for r in inputs}
    assert all(before[r['path']]==r['sha256'] for r in inputs)
    tests=(Path('src/test_identifiability.py'),Path('general-roots/src/test_design_rank.py'))
    local=[run(BASE/p,ROOT) for p in tests]
    for index,result in enumerate(local):(BASE/'results'/f'FINAL_TESTS_{index+1}.log').write_text(result['stdout']+result['stderr'])
    export=run(BASE/'src/export_results.py',ROOT);expected=(BASE/'results/RESULTS.json').read_bytes()
    with tempfile.TemporaryDirectory(prefix='t20-identification-') as temp:
        isolated=Path(temp);relative=BASE.relative_to(ROOT)
        for path in BASE.rglob('*.py'):
            destination=isolated/path.relative_to(ROOT);destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(path,destination)
        (isolated/relative/'results').mkdir(parents=True,exist_ok=True)
        for record in inputs:
            if record['kind']=='runtime':
                destination=isolated/record['path'];destination.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/record['path'],destination)
        isolated_tests=[run(isolated/relative/p,isolated) for p in tests]
        isolated_export=run(isolated/relative/'src/export_results.py',isolated)
        equal=(isolated/relative/'results/RESULTS.json').read_bytes()==expected
    after={r['path']:sha(ROOT/r['path']) for r in inputs}
    result={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'local_tests':local,'export':export,'isolated_tests':isolated_tests,
            'isolated_export':isolated_export,'results_byte_equal':equal,'bound_inputs_unchanged':before==after,'input_count':len(inputs),
            'test_counts':[int(re.search(r'Ran (\d+) tests',r['stderr']).group(1)) for r in local],
            'scope':'Evidence replay only; no additional research credit or kernel certification.'}
    (BASE/'results/VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('test_counts','results_byte_equal','bound_inputs_unchanged','input_count')}))
    return 0 if all(r['exit_code']==0 for r in local+isolated_tests+[export,isolated_export]) and equal and before==after else 1
if __name__=='__main__':raise SystemExit(main())
