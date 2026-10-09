from pathlib import Path
from datetime import datetime,timezone
import tempfile,subprocess,shutil,os,sys,json,hashlib
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]

def run(path,cwd):
    p=subprocess.run([sys.executable,str(path)],cwd=cwd,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
    return {'path':str(path),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}

def main():
    inputs=json.loads((BASE/'SOURCE_BINDINGS.json').read_text())['files']
    unchanged=all(hashlib.sha256((ROOT/r['path']).read_bytes()).hexdigest()==r['sha256'] for r in inputs)
    local=run(BASE/'src/test_crt_calibration.py',BASE)
    (BASE/'results/FINAL_TESTS.log').write_text(local['stdout']+local['stderr'])
    exported=run(BASE/'src/export_results.py',BASE);expected=(BASE/'results/RESULTS.json').read_bytes()
    with tempfile.TemporaryDirectory(prefix='t20-crt-') as temp:
        isolated=Path(temp);(isolated/'src').mkdir();(isolated/'results').mkdir()
        for path in (BASE/'src').glob('*.py'):shutil.copy2(path,isolated/'src'/path.name)
        test=run(isolated/'src/test_crt_calibration.py',isolated)
        export=run(isolated/'src/export_results.py',isolated)
        equal=(isolated/'results/RESULTS.json').read_bytes()==expected
    record={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'local':local,'local_export':exported,'isolated':test,'isolated_export':export,
            'prior_inputs_unchanged':unchanged,'isolated_results_equal':equal,'scope':'Replay only; no new research credit.'}
    (BASE/'results/VERIFICATION.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({'tests':11,'prior_inputs_unchanged':unchanged,'isolated_results_equal':equal}))
    return 0 if unchanged and equal and all(x['exit_code']==0 for x in (local,exported,test,export)) else 1
if __name__=='__main__':raise SystemExit(main())
