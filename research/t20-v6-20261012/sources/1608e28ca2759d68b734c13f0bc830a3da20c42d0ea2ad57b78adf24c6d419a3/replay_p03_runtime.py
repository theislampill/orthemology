#!/usr/bin/env python3
"""Run the preserved P03 reference/proposal tests and 188 native strict-JSON cases."""
from pathlib import Path
import argparse,datetime,json,os,subprocess,sys
from portable_core import extract_zip,sha,write_json,verify_manifest
from verify import verify

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--package-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();root=a.package_root.resolve();out=a.out.resolve()
 if out.exists() or out.is_relative_to(root):raise SystemExit('Fresh output outside immutable package required')
 before=verify(root);out.mkdir(parents=True);payload=extract_zip(root/'archives/P03_Qualified_Native_Refinement_20260930.zip',out/'payload')
 rec={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_sha256':before['manifest_sha256'],'commands':[],'scope':'Finite actual reference/proposal executions only; not universal runtime equivalence or kernel certification of Python'}
 def save():write_json(out/'P03_RUNTIME_RESULT.json',rec)
 def run(label,args,cwd,extra={}):
  env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(cwd),**extra};p=subprocess.run([sys.executable,'-B']+args,cwd=cwd,env=env,capture_output=True,text=True,timeout=900)
  (out/(label+'.stdout')).write_text(p.stdout);(out/(label+'.stderr')).write_text(p.stderr);rec['commands'].append({'label':label,'argv':args,'cwd':str(cwd.relative_to(out)),'exit_code':p.returncode,'stdout_sha256':sha(out/(label+'.stdout')),'stderr_sha256':sha(out/(label+'.stderr'))});save()
  if p.returncode:raise ValueError('P03 finite replay failure: '+label)
 try:
  for name in ['source','canonical']:
   base=payload/'python-bases'/name
   for mode,opts in [('normal',[]),('optimized',['-O'])]:
    run(name+'-base-'+mode,opts+['-m','unittest','discover','-s','tests','-v'],base)
    run(name+'-proposal-'+mode,opts+[str(payload/'shadow/tools/test_new_frontier.py')],payload/'shadow',{'P03_BASE':str(base),'P03_HISTORY_OUT':str(out/(name+'-'+mode+'-histories.json'))})
  casecode='''import json,hashlib,os
from pathlib import Path
from collections import Counter
import reference
from boundaries import Rejection
root=Path(os.environ['P03_CASES']); rows=json.loads((root/'CASES.json').read_text());counts=Counter()
for row in rows:
 raw=(root/(row['name']+'.json')).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=row['raw_sha256']:raise ValueError('Raw case hash changed')
 try:result=reference.check_json(raw,row['depth']);outcome='accept'
 except Rejection:result=None;outcome='refuse'
 if outcome!=row['outcome']:raise ValueError('Outcome mismatch '+row['name'])
 if outcome=='accept' and json.loads(json.dumps(result))!=row['output']:raise ValueError('Accepted output mismatch '+row['name'])
 if not row['duplicate_field_wire']:
  try:native=reference.check(json.loads(raw),row['depth']);native_outcome='accept'
  except Rejection:native=None;native_outcome='refuse'
  if native_outcome!=outcome or native!=result:raise ValueError('Native/strict-JSON mismatch '+row['name'])
 elif outcome!='refuse':raise ValueError('Duplicate wire accepted')
 counts[outcome]+=1
if len(rows)!=188 or dict(counts)!={'accept':54,'refuse':134}:raise ValueError('Case census changed')
print(json.dumps({'status':'PASS','cases':len(rows),'outcomes':dict(counts)}))
'''
  run('native-json-188',['-c',casecode],payload/'python-bases/source',{'P03_CASES':str(payload/'constructor-square/native-cross-language-final')})
  verify_manifest(root,before['manifest_sha256']);rec['status']='PASS';rec['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
 except Exception as ex:rec['status']='FAIL_CLOSED';rec['error']=repr(ex);save();raise
 print(json.dumps({'status':rec['status'],'receipt':str(out/'P03_RUNTIME_RESULT.json'),'sha256':sha(out/'P03_RUNTIME_RESULT.json')}))
if __name__=='__main__':main()
