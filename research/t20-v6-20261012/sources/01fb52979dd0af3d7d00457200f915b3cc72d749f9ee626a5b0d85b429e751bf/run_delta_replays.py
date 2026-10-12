import concurrent.futures,hashlib,json,os,shutil,subprocess,sys,tempfile,time
from pathlib import Path
D=Path(__file__).resolve().parent;R=D.parents[1];P=R/'t20-consolidation-20261011/projection/package-v3'
SUITES=['finite-contracts-reconstructed','audit-refinement','restricted-controls','depth-independent','foundational-scope','pro-exact-controls','contract-downstream']
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
records=[]
with tempfile.TemporaryDirectory(prefix='independent-v3-projection-review-') as tmp:
 work=Path(tmp)/'package';shutil.copytree(P,work)
 def run(label,args):
  start=time.monotonic();p=subprocess.run([sys.executable,'-B',*args],cwd=work,env=env,text=True,capture_output=True,timeout=600)
  (D/(label+'.stdout')).write_text(p.stdout);(D/(label+'.stderr')).write_text(p.stderr)
  row={'label':label,'arguments':args,'exit_code':p.returncode,'seconds':round(time.monotonic()-start,3),'stdout_sha256':hashlib.sha256(p.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr.encode()).hexdigest()}
  if label in SUITES and p.returncode==0:
   j=json.loads(p.stdout);row.update(status=j['status'],suite=j['suite'],subprocess_runs=len(j['results']),scope=j['scope'])
  return row
 records.append(run('validator',['validate_package.py']))
 records.append(run('tool-tests',['-m','unittest','discover','-s','tool-tests','-v']))
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
  futures={ex.submit(run,s,['replay_selected.py','--suite',s,'--timeout','600']):s for s in SUITES}
  for f in concurrent.futures.as_completed(futures):
   row=f.result();records.append(row);print(row['label'],row['exit_code'],row['seconds'],flush=True)
result={'status':'PASS' if all(x['exit_code']==0 for x in records) else 'FAIL','scope':'Independent executions of new selected replay targets and delivery-tool tests, in disposable copied package; unchanged historical suites not rerun.','records':records}
(D/'REPLAY_RUNS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));sys.exit(result['status']!='PASS')
