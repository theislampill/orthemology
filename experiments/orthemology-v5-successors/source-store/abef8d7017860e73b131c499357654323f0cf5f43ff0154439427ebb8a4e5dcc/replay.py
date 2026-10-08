#!/usr/bin/env python3
"""Fresh source-only Eighth semantic-control replay; no downloads or heartbeat changes."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,subprocess,sys,time
if sys.flags.optimize: raise RuntimeError('Optimized Python is refused')
sys.dont_write_bytecode=True
from verify_dependency_identity import verify_dependencies
ROOT=Path(__file__).resolve().parent
SOURCE_MANIFEST_SHA256='8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n')
def sources():
 assert sha(ROOT/'SOURCE_MANIFEST.json')==SOURCE_MANIFEST_SHA256,'Unexpected source manifest'
 m=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
 actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*.lean')}
 assert actual=={r['path'] for r in m['sources']},'Lean source census mismatch'
 for r in m['sources']:
  p=ROOT/r['path'];assert p.is_file() and not p.is_symlink() and sha(p)==r['sha256'] and p.stat().st_size==r['bytes'],r['path']
 def closure(suite,target):
  root=ROOT/suite/'src';by={str(p.relative_to(root))[:-5].replace('/','.'):p for p in root.rglob('*.lean')};order=[];states={}
  def visit(n):
   if states.get(n)==2:return
   assert states.get(n)!=1,'Cyclic import'
   states[n]=1
   for line in by[n].read_text().splitlines():
    if line.startswith('import '):
     for dep in line[7:].split():
      if dep in by:visit(dep)
      else:assert dep.startswith(('Mathlib','Lean','Std','Init')),dep
   states[n]=2;order.append(n)
  visit(target);assert set(order)==set(by),'Unreachable custom source in closure'
  return [(n,by[n]) for n in order]
 c=closure('cost','ActualExponentialMoments');r=closure('runtime','ExactRuntimeCounterexample')
 assert len(c)==146 and len(r)==167
 original=(ROOT/'cost/src/ActualExponentialMoments.lean').read_bytes();mut=(ROOT/'cost/mutation/ActualExponentialMoments.lean').read_bytes()
 before='fallback fallbackAction ε\n    bad hpriority hs₀ σ hσ η hηpos hη hSep'.encode();after=before.replace(' ε\n'.encode(),' (ε/2)\n'.encode())
 assert original.count(before)==1 and original.replace(before,after)==mut
 assert sha(ROOT/'cost/mutation/ActualExponentialMoments.lean')==m['cost_mutant_sha256']
 orig=(ROOT/'runtime/src/FullControllerCanonicalLaw.lean').read_bytes();mut=(ROOT/'runtime/inherited-mutation/FullControllerCanonicalLaw.lean').read_bytes()
 before='(decodedHistory (policyProgram (withComputedTolerance c)) (sourcePolicy (withComputedTolerance c)) σ x)) := by'.encode();after=before.replace('(policyProgram (withComputedTolerance c))'.encode(),'(policyProgram c)'.encode())
 assert orig.count(before)==1 and orig.replace(before,after)==mut
 assert sha(ROOT/'runtime/inherited-mutation/FullControllerCanonicalLaw.lean')==m['runtime_inherited_mutant_sha256']
 return {'cost':c,'runtime':r}

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--verify-only',action='store_true');p.add_argument('--lean-bin',type=Path);p.add_argument('--mathlib',type=Path);p.add_argument('--mathlib-archive',type=Path);p.add_argument('--out',type=Path);p.add_argument('--mode',choices=['all','cost','runtime'],default='all');a=p.parse_args()
 order=sources()
 if a.verify_only:print('PASS_SOURCE_FREEZE: 146 cost modules, 167 runtime modules, two exact mutation derivations; no proof replay.');return
 if any(v is None for v in [a.lean_bin,a.mathlib,a.out]):p.error('--lean-bin, --mathlib and --out are required')
 lean=(a.lean_bin/'lean').resolve();math=a.mathlib.resolve();out=a.out.resolve()
 assert not out.exists(),'Output must be absent'
 for protected in [ROOT,math,lean.parent.parent]:assert not out.is_relative_to(protected),'Output is inside a protected root'
 pins=json.loads((ROOT/'DEPENDENCY_PINS.json').read_text())
 assert sha(lean)==pins['lean_binary_sha256'];assert subprocess.check_output([str(lean),'--version'],text=True).strip()==pins['lean_version']
 identity=verify_dependencies(math,a.mathlib_archive,pins)
 libs=[math/'.lake/build/lib/lean']+sorted((math/'.lake/packages').glob('*/.lake/build/lib/lean'))
 assert (libs[0]/'Mathlib.olean').is_file(),'Official dependency cache required'
 out.mkdir(parents=True)
 result={'status':'RUNNING','started_utc':utc(),'mode':a.mode,'source_manifest_sha256':SOURCE_MANIFEST_SHA256,'dependency_identity':identity,'official_dependency_cache_trusted':True,'custom_objects_reused':False,'heartbeat_flags_added':False,'parallel_processes':1,'wall_clock_per_module_seconds':180,'original_runtime_mutant_retried':False,'historical_statuses_unchanged':True,'runs':[]}
 save=lambda:write(out/'RESULT.json',result)
 def run(suite,label,source,root,env,object_path=None):
  cmd=[str(lean),'-j1','--root='+str(root)]
  if object_path:object_path.parent.mkdir(parents=True,exist_ok=True);cmd+=['-o',str(object_path)]
  cmd+=[str(source)];t=time.monotonic()
  try:
   proc=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180);txt=proc.stdout;code=proc.returncode
  except subprocess.TimeoutExpired as ex:
   txt=(ex.stdout.decode() if isinstance(ex.stdout,bytes) else ex.stdout or '')+'\nWALL_CLOCK_LIMIT_180_SECONDS\n';code=None
  log=out/suite/'logs'/(label+'.log');log.parent.mkdir(parents=True,exist_ok=True);log.write_text(txt)
  rec={'suite':suite,'module':label,'source_sha256':sha(source),'exit_code':code,'elapsed_seconds':round(time.monotonic()-t,3),'command':cmd,'log':str(log.relative_to(out)),'log_sha256':sha(log),'has_resource_diagnostic':bool(re.search(r'timeout|maximum number of heartbeats|WALL_CLOCK_LIMIT',txt))}
  if object_path and object_path.exists():rec['object_sha256']=sha(object_path)
  result['runs'].append(rec);save();print(suite,label,code,flush=True);return rec,txt
 save()
 try:
  for suite in ['cost','runtime']:
   if a.mode not in ['all',suite]:continue
   build=out/suite/'build';build.mkdir(parents=True);env=dict(os.environ);env.pop('LEAN_SRC_PATH',None);env['LEAN_PATH']=':'.join(map(str,[build]+libs))
   for mod,src in order[suite]:
    rec,txt=run(suite,mod,src,ROOT/suite/'src',env,build/Path(*mod.split('.')).with_suffix('.olean'))
    if rec['exit_code']!=0 or 'error:' in txt or re.search(r'\b(sorry|admit)\b|declaration uses',txt):
     result.update(status='POSITIVE_CLOSURE_BLOCKED',blocked_suite=suite,finished_utc=utc());save();return
   rb='CostReadback' if suite=='cost' else 'RuntimeReadback'
   rec,txt=run(suite,rb,ROOT/'readbacks'/(rb+'.lean'),ROOT/'readbacks',env)
   audits=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',txt)
   assert rec['exit_code']==0 and len(audits)==(2 if suite=='cost' else 13),'Missing or failed axiom audit'
   for block in audits:assert set(x.strip() for x in block.split(','))<= {'propext','Classical.choice','Quot.sound'},block
   result[suite]={'status':'FRESH_EXACT_CLOSURE_AND_AXIOM_READBACK_PASS','custom_modules':len(order[suite]),'axiom_readbacks':len(audits)};save()
   if suite=='cost':
    rec,txt=run(suite,'exact-cost-mutant',ROOT/'cost/mutation/ActualExponentialMoments.lean',ROOT/'cost/mutation',env)
    concrete='error: application type mismatch' in txt and 'η ≤ ε / 2 : Prop' in txt and 'η ≤ ε : Prop' in txt
    before_resource=concrete and (not rec['has_resource_diagnostic'] or txt.index('error: application type mismatch')<txt.index('timeout'))
    result['cost']['mutant']={'concrete_application_rejection':concrete,'concrete_before_resource':before_resource,'additional_resource_diagnostic':rec['has_resource_diagnostic'],'does_not_refute_unchanged_positive_theorem':True}
    if not concrete:result['cost']['mutant']['status']='INCONCLUSIVE_RESOURCE' if rec['has_resource_diagnostic'] else 'UNREVIEWED_NONRESOURCE_OUTCOME'
    else:result['cost']['mutant']['status']='CONCRETE_PROOF_APPLICATION_REJECTION'
   else:
    result['runtime']['semantic_result']='EXACT_MUTATED_UNIVERSAL_STATEMENT_FALSE_BY_POSITIVE_MEASURE_COUNTEREXAMPLE'
    result['runtime']['selector_kind']='KERNEL_CERTIFIED_CLASSICAL_EXISTENTIAL_NOT_EVALUATED_NATIVE_NUMERALS'
   save()
  result.update(status='COMPLETED_FRESH_REPLAY',finished_utc=utc());save()
 except Exception as ex:
  result.update(status='FAILED_CLOSED',error=str(ex),finished_utc=utc());save();raise
if __name__=='__main__':main()
