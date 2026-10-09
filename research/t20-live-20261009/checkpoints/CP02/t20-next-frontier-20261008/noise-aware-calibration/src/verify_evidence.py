from pathlib import Path
from datetime import datetime,timezone
import tempfile,subprocess,shutil,os,sys,json,hashlib
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]

def run(path,cwd):
    p=subprocess.run([sys.executable,str(path)],cwd=cwd,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
    return {'path':str(path),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}

def main():
    records=json.loads((BASE/'SOURCE_BINDINGS.json').read_text())['files']
    before={r['path']:hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest() for r in records}
    assert all(before[r['path']]==r['sha256'] for r in records)
    local=run(BASE/'src/test_robust_masks.py',BASE)
    (BASE/'results/FINAL_TESTS.log').write_text(local['stdout']+local['stderr'])
    exported=run(BASE/'src/export_results.py',BASE);expected=(BASE/'results/RESULTS.json').read_bytes()
    with tempfile.TemporaryDirectory(prefix='t20-robust-masks-') as temp:
        isolated=Path(temp);(isolated/'src').mkdir();(isolated/'results').mkdir()
        for path in (BASE/'src').glob('*.py'):shutil.copy2(path,isolated/'src'/path.name)
        isolated_test=run(isolated/'src/test_robust_masks.py',isolated)
        isolated_export=run(isolated/'src/export_results.py',isolated)
        equal=(isolated/'results/RESULTS.json').read_bytes()==expected
    after={r['path']:hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest() for r in records}
    result={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'local_tests':local,'local_export':exported,
            'isolated_tests':isolated_test,'isolated_export':isolated_export,'exports_byte_equal':equal,
            'bound_inputs_unchanged':before==after,'bound_input_count':len(records),'test_groups':11,
            'scope':'Administrative replay only, not empirical trials, new discoveries or kernel verification.'}
    (BASE/'results/VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('test_groups','exports_byte_equal','bound_inputs_unchanged','bound_input_count')}))
    return 0 if equal and before==after and all(x['exit_code']==0 for x in (local,exported,isolated_test,isolated_export)) else 1
if __name__=='__main__':raise SystemExit(main())
