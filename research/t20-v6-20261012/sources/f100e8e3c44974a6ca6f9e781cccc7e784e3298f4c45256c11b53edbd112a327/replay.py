#!/usr/bin/env python3
"""Replay the exact source projection against explicit read-only dependency roots."""
from pathlib import Path
import argparse,hashlib,json,os,subprocess,time,re
ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(ok,message):
 if not ok:raise RuntimeError(message)
def write(p,x):p.write_text(json.dumps(x,indent=2)+'\n')
def pinned_tree(root,pin,exceptions={}):
 rows=pin['entries']; actual=set();expected={x['path'] for x in rows}
 for rt in pin['roots']:
  p=root/rt
  if rt:actual.add(rt)
  actual.update(str(x.relative_to(root)) for x in p.rglob('*'))
 check(actual==expected,'dependency entry inventory differs')
 accepted=[]
 for r in rows:
  p=root/r['path'];kind=r['kind']
  if kind=='directory':check(p.is_dir(),'missing directory '+r['path'])
  elif kind=='symlink':check(p.is_symlink() and str(p.readlink())==r['target'],'symlink differs '+r['path'])
  else:
   h=sha(p);size=p.stat().st_size
   if h==r['sha256'] and size==r['bytes']:continue
   e=exceptions.get(r['path'])
   check(e is not None and h==e['current_sha256'] and size==e['current_bytes'],'dependency bytes differ '+r['path'])
   accepted.append(r['path'])
 return {'entries':len(rows),'accepted_metadata_exceptions':accepted,'exact_inventory':True}
def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--lean-root',required=True,type=Path)
 p.add_argument('--mathlib-root',required=True,type=Path)
 p.add_argument('--output',required=True,type=Path)
 p.add_argument('--check-only',action='store_true')
 a=p.parse_args();out=a.output.resolve();lr=a.lean_root.resolve();mr=a.mathlib_root.resolve()
 check(not out.exists(),'output must be absent')
 check(ROOT!=out and ROOT not in out.parents,'output must be outside source package')
 check(lr!=out and lr not in out.parents and mr!=out and mr not in out.parents,'output must be outside dependency roots')
 manifest=json.loads((ROOT/'MANIFEST.json').read_text())
 expected={x['path'] for x in manifest['files']}|{'MANIFEST.json'}
 actual={str(x.relative_to(ROOT)) for x in ROOT.rglob('*') if x.is_file()}
 check(actual==expected,'package file inventory differs')
 for r in manifest['files']:
  q=ROOT/r['path'];check(sha(q)==r['sha256'] and q.stat().st_size==r['bytes'],'package hash differs '+r['path'])
 lp=json.loads((ROOT/'dependencies/LEAN_DISTRIBUTION_PIN.json').read_text())
 mp=json.loads((ROOT/'dependencies/MATHLIB_CACHE_PIN.json').read_text())
 sp=json.loads((ROOT/'dependencies/MATHLIB_SOURCE_PIN.json').read_text())
 ep=json.loads((ROOT/'dependencies/CACHE_METADATA_EXCEPTION_PINS.json').read_text())
 checks={'lean':pinned_tree(lr,lp),'cache':pinned_tree(mr,mp,{x['path']:x for x in ep['files']})}
 for r in sp['files']:
  q=mr/r['path'];check(sha(q)==r['sha256'] and q.stat().st_size==r['size'],'Mathlib source differs '+r['path'])
 checks['mathlib_source_files']=len(sp['files'])
 out.mkdir(parents=True)
 plan=json.loads((ROOT/'BUILD_PLAN.json').read_text())
 receipt={'status':'CHECK_ONLY_PASS' if a.check_only else 'RUNNING','source_manifest_sha256':sha(ROOT/'MANIFEST.json'),'freeze':json.loads((ROOT/'ORIGINAL_TO_PUBLIC.json').read_text())['original_freeze'],'external_checks':checks,'source_stages':len(plan),'stages':[],'author_objects_used':False,'jobs_per_process':1,'compile_concurrency':1,'per_process_timeout_seconds':180,'resource_limit_increases':False,'official_cache_rebuilt':False}
 write(out/'REPLAY_RECEIPT.json',receipt)
 if a.check_only:print('CHECK_ONLY_PASS',flush=True);return
 build=out/'build';build.mkdir();logs=out/'logs';logs.mkdir()
 env={k:v for k,v in os.environ.items() if not k.startswith(('LD_','LEAN_'))}
 env['PATH']=str(lr/'bin')+os.pathsep+os.defpath
 env['LEAN_PATH']=os.pathsep.join([str(build)]+[str(mr/s) for s in mp['roots']])
 def run(cmd,stage):
  start=time.monotonic();timed=False
  try:r=subprocess.run(cmd,env=env,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180);code=r.returncode;stdout=r.stdout
  except subprocess.TimeoutExpired as e:code=124;timed=True;stdout=e.stdout or '';stdout=stdout.decode() if isinstance(stdout,bytes) else stdout
  log=logs/(stage+'.log');log.write_text(stdout)
  rec={'stage':stage,'exit_code':code,'timed_out':timed,'seconds':time.monotonic()-start,'log_sha256':sha(log)}
  receipt['stages'].append(rec);write(out/'REPLAY_RECEIPT.json',receipt)
  check(code==0 and not timed,'compiler stage failed: '+stage)
  return stdout,rec
 try:
  v,_=run([str(lr/'bin/lean'),'--version'],'version');check('4.19.0' in v,'wrong Lean version')
  for n,r in enumerate(plan,1):
   f=ROOT/r['path'];check(sha(f)==r['sha256'],'source changed '+r['path'])
   stdout,rec=run([str(lr/'bin/lean'),'-j1','-o',str(build/(r['module']+'.olean')),str(f)],f'{n:03d}-{r["module"]}')
   rec.update({'module':r['module'],'source_sha256':r['sha256'],'kind':r['kind'],'olean_sha256':sha(build/(r['module']+'.olean'))})
   if r['module'] in ['AllTransportAxioms','IndependentAxiomAudit']:
    rows=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",stdout,re.S)
    free=re.findall(r"'([^']+)' does not depend on any axioms",stdout)
    names=[x[0] for x in rows]+free;expect=72 if r['module']=='AllTransportAxioms' else 20
    check(len(names)==expect and len(set(names))==expect,'axiom audit name count differs')
    if expect==72:check(set(names)=={x['name'] for x in json.loads((ROOT/'evidence/DECLARATIONS.json').read_text())},'frozen axiom declaration names differ')
    for name,axes in rows:check(set(s.strip() for s in axes.split(',') if s.strip())<={'propext','Classical.choice','Quot.sound'},'unexpected axiom '+name)
    rec['standard_only_axiom_declarations']=expect
   write(out/'REPLAY_RECEIPT.json',receipt);print(r['module'],'PASS',flush=True)
  receipt['status']='PASS';write(out/'REPLAY_RECEIPT.json',receipt)
 except Exception as e:
  receipt['status']='FAILED';receipt['error']=str(e);write(out/'REPLAY_RECEIPT.json',receipt);raise
if __name__=='__main__':main()
