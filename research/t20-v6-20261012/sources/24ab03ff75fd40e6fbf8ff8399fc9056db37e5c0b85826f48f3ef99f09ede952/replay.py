from pathlib import Path
import json,hashlib,shutil,tempfile,subprocess,sys,difflib
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(c,m):
 if not c:raise RuntimeError(m)
def verify():
 for x in json.loads((R/'MANIFEST.json').read_text()):
  p=R/x['path'];check(p.is_file(),'Missing delivered file '+x['path']);check(sha(p)==x['sha256'] and p.stat().st_size==x['bytes'],'Manifest mismatch '+x['path'])
 for x in json.loads((R/'PRESERVATION_MAP.json').read_text()):check(sha(R/x['preserved'])==x['sha256'],'Original preservation mismatch '+x['source'])
 omitted={x['path']:x for x in json.loads((R/'OMISSION_LEDGER.json').read_text())}
 for x in json.loads((R/'BOUND_INPUT_STATUS.json').read_text()):
  if x['status']=='included':check(sha(R/x['preserved'])==x['sha256'],'Bound input mismatch '+x['path'])
  else:check(x['status']=='omitted-source-body' and omitted[x['path']]['sha256']==x['sha256'],'Undisclosed omission '+x['path'])
 pred=R/'payload/predictive-understanding-transfer-20261011'
 for name,h in json.loads((pred/'CURRENT_BINDINGS.json').read_text())['current_after_correction'].items():check(sha(pred/name)==h,'Current binding mismatch '+name)
 diff=''.join(''.join(difflib.unified_diff((pred/'pre-correction'/name).read_text().splitlines(True),(pred/name).read_text().splitlines(True),fromfile='pre-correction/'+name,tofile=name)) for name in ['REPORT.md','verify.py'])
 check(diff==(pred/'CORRECTION.diff').read_text(),'Exact correction diff mismatch')
def replay():
 verify();runs=[]
 with tempfile.TemporaryDirectory(prefix='moment-predictive-') as tmp:
  work=Path(tmp)/'payload';shutil.copytree(R/'payload',work)
  for opt in [False,True]:
   prefix=[sys.executable]+(['-O'] if opt else [])
   for folder,script in [('fixed-calibration-moment-repair-20261011','check.py'),('fixed-calibration-moment-independent-review-20261011','check_independent.py'),('predictive-understanding-root-review-20261011','check.py')]:
    p=subprocess.run(prefix+[str(work/folder/script)],cwd=work,text=True,capture_output=True)
    check(p.returncode==0,folder+' failed '+p.stderr);runs.append({'packet':folder,'optimized':opt,'status':'PASS','stdout':p.stdout})
   script=work/'predictive-understanding-transfer-20261011/verify.py';name='PORTABLE_OPTIMIZED.json' if opt else 'PORTABLE_NORMAL.json'
   p=subprocess.run(prefix+[str(R/'portable_predictive_adapter.py'),str(script),'--output',name],cwd=work,text=True,capture_output=True)
   check(p.returncode==0,'Predictive adapted replay failed '+p.stderr);result=json.loads(p.stdout)
   check(result['explicit_checks_executed']==1406,'Portable count must exclude exactly two source-body checks')
   original=json.loads((script.parent/('OPTIMIZED_CONTROL_RESULTS.json' if opt else 'CONTROL_RESULTS.json')).read_text())
   for key,value in original.items():
    if key not in ['explicit_checks_executed','input_bindings_reverified']:check(result[key]==value,'Original numerical result differs '+key)
   check(result['input_bindings_reverified'] is False and result['portable_replay']['primary_source_body_checks_replayed'] is False,'Missing source limitation disclosure')
   runs.append({'packet':'predictive-understanding-transfer-20261011','optimized':opt,'status':'PASS with explicit source omissions','result':result})
   negatives=[([str(work/'fixed-calibration-moment-independent-review-20261011/check_independent.py'),'--negative'],'ACTIVE_MOMENT_REVIEW_FAILURE'),([str(R/'portable_predictive_adapter.py'),str(script),'--false-check-control'],'deliberate active false-check control')]
   for args,token in negatives:
    p=subprocess.run(prefix+args,cwd=work,text=True,capture_output=True)
    check(p.returncode!=0 and token in p.stderr,'False control failed to reject '+token)
    runs.append({'optimized':opt,'kind':'deliberate failure','token':token,'returncode':p.returncode,'last_error':p.stderr.splitlines()[-1]})
 verify();print(json.dumps({'status':'PASS','python':sys.version,'runs':runs,'primary_source_body_replay':False,'mathematical_checks_and_inherited_bindings_active':True,'raw_historical_optimized_replay_credit':False},indent=2))
if __name__=='__main__':
 if '--verify-only' in sys.argv:verify();print('PASS: manifest, originals, bound statuses, current bindings, exact correction diff')
 else:replay()
