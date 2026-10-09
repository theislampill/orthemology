from pathlib import Path
from datetime import datetime,timezone
import tempfile,subprocess,shutil,os,sys,json,hashlib,re
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[1]

def run(path,cwd):
    p=subprocess.run([sys.executable,str(path)],cwd=cwd,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True,text=True)
    return {'path':str(path),'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    records=json.loads((BASE/'SOURCE_BINDINGS.json').read_text())['files']
    before={r['path']:digest(ROOT/r['path']) for r in records}
    assert all(before[r['path']]==r['sha256'] for r in records)
    primary=[]
    for source in json.loads((BASE/'sources/SOURCE_READS.json').read_text())['sources']:
        path=BASE/'sources'/source['file']
        if path.exists():
            match=digest(path)==source['sha256'];assert match
            primary.append({'file':source['file'],'status':'hash verified'})
        else:
            assert source['delivery'].startswith('inspection-only')
            primary.append({'file':source['file'],'status':'link-and-hash source; full modern article intentionally not packaged'})
    names=('test_countable_support.py','test_gcd_decoder.py','test_oracle_boundaries.py')
    local=[run(BASE/'src'/name,BASE) for name in names]
    for name,result in zip(names,local):(BASE/'results'/('FINAL_'+name+'.log')).write_text(result['stdout']+result['stderr'])
    exported=run(BASE/'src/export_results.py',BASE);expected=(BASE/'results/RESULTS.json').read_bytes()
    with tempfile.TemporaryDirectory(prefix='t20-countable-') as temp:
        isolated=Path(temp);(isolated/'src').mkdir();(isolated/'results').mkdir()
        for path in (BASE/'src').glob('*.py'):shutil.copy2(path,isolated/'src'/path.name)
        isolated_tests=[run(isolated/'src'/name,isolated) for name in names]
        isolated_export=run(isolated/'src/export_results.py',isolated)
        equal=(isolated/'results/RESULTS.json').read_bytes()==expected
    after={r['path']:digest(ROOT/r['path']) for r in records}
    result={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'local_tests':local,'local_export':exported,
            'isolated_tests':isolated_tests,'isolated_export':isolated_export,'exports_byte_equal':equal,
            'bound_inputs_unchanged':before==after,'primary_source_checks':primary,
            'test_counts':[int(re.search(r'Ran (\d+) tests',r['stderr']).group(1)) for r in local],
            'scope':'Evidence replay only, not new research credit, a new primitive-divisor proof, or source-world authentication.'}
    (BASE/'results/VERIFICATION.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ('test_counts','exports_byte_equal','bound_inputs_unchanged')}))
    return 0 if equal and before==after and all(x['exit_code']==0 for x in local+isolated_tests+[exported,isolated_export]) else 1
if __name__=='__main__':raise SystemExit(main())
