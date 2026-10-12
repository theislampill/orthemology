#!/usr/bin/env python3
"""Independent reviewer runner. No author objects reused, no source mutation."""
from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,time,importlib.util
if sys.flags.optimize:raise RuntimeError('Optimized Python refused')
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
SOURCE=ROOT/'snapshot'
LEAN=Path('private-locator:cb50f30cfa35bdf3a0cf')
MATH=Path('private-locator:18d48e051fd31eaf177f')
ARCHIVE=Path('private-locator:c8706d03ffdb12093ad5')
OUT=ROOT/'fresh-independent01'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def write(p,v):Path(p).write_text(json.dumps(v,indent=2)+'\n')

def source_check():
 assert sha(SOURCE/'SOURCE_MANIFEST.json')=='8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c'
 m=json.loads((SOURCE/'SOURCE_MANIFEST.json').read_text())
 rows={r['path']:r for r in m['sources']};assert len(rows)==len(m['sources'])==317
 assert set(rows)=={str(p.relative_to(SOURCE)) for p in SOURCE.rglob('*.lean')}
 for name,r in rows.items():
  p=SOURCE/name;assert p.is_file() and not p.is_symlink() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],name
 return m

def order(suite,target):
 root=SOURCE/suite/'src';by={str(p.relative_to(root).with_suffix('')).replace('/','.'):p for p in root.rglob('*.lean')}
 done=set();pending=set();seq=[]
 def visit(mod):
  if mod in done:return
  assert mod not in pending,'Cycle: '+mod
  pending.add(mod)
  for line in by[mod].read_text().splitlines():
   if line.startswith('import '):
    for dep in line[7:].split():
     if dep in by:visit(dep)
     else:assert dep.startswith(('Mathlib','Lean','Std','Init')),dep
  pending.remove(mod);done.add(mod);seq.append((mod,by[mod]))
 visit(target);assert set(by)==done
 return seq

def main():
 m=source_check();assert OUT.exists(),'Fresh checkpoint absent'
 previous=json.loads((OUT/'RESULT.json').read_text())
 assert previous['status']=='BLOCKED_OR_FAILED' and previous['runs'][-1]['label']=='ExactStatementReview'
 assert previous['runtime']['closure']=='PASS' and previous['runtime']['fresh_custom_modules']==167
 for rec in previous['runs'][:167]:
  assert rec['suite']=='runtime' and rec['exit_code']==0
  assert sha(ROOT/rec['source'])==rec['source_sha256']
  obj=OUT/'runtime/build'/Path(*rec['label'].split('.')).with_suffix('.olean')
  assert sha(obj)==rec['object_sha256']
 checkpoint=OUT/'BEFORE_REVIEWER_AUXILIARY_REPAIR2.json';assert not checkpoint.exists();write(checkpoint,previous)
 pins=json.loads((SOURCE/'DEPENDENCY_PINS.json').read_text())
 assert sha(LEAN)==pins['lean_binary_sha256']
 assert subprocess.check_output([str(LEAN),'--version'],text=True).strip()==pins['lean_version']
 spec=importlib.util.spec_from_file_location('dependency_verifier',SOURCE/'verify_dependency_identity.py');d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
 dep=d.verify_dependencies(MATH,ARCHIVE,pins)
 # Continue the same independently fresh source-bound replay.
 res=previous
 res.update(status='RUNNING',continuation_started_utc=now(),continuation_runner_sha256=sha(__file__),
  continued_own_exact_fresh_runtime_objects=167,reviewer_auxiliary_repair='Replaced failed decide numeral probe with transparent finite-set normalization; exact-header and all-80-declaration checks were already successful. Original failed probe and receipt retained.')
 res.pop('error',None);res.pop('finished_utc',None)
 save=lambda:write(OUT/'RESULT.json',res)
 save()
 libs=[MATH/'.lake/build/lib/lean']+sorted((MATH/'.lake/packages').glob('*/.lake/build/lib/lean'))
 def run(suite,label,src,srcroot,env,obj=None):
  cmd=[str(LEAN),'-j1','--root='+str(srcroot)]
  if obj:obj.parent.mkdir(parents=True,exist_ok=True);cmd+=['-o',str(obj)]
  cmd+=[str(src)];t=time.monotonic()
  try:
   cp=subprocess.run(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180);txt=cp.stdout;code=cp.returncode
  except subprocess.TimeoutExpired as ex:
   txt=(ex.stdout.decode() if isinstance(ex.stdout,bytes) else ex.stdout or '')+'\nWALL_TIMEOUT_180\n';code=None
  log=OUT/suite/'logs'/(label+'-continuation2.log');log.parent.mkdir(parents=True,exist_ok=True);log.write_text(txt)
  r={'suite':suite,'label':label,'source':str(src.relative_to(ROOT)),'source_sha256':sha(src),'exit_code':code,
    'elapsed_seconds':round(time.monotonic()-t,3),'command':cmd,'log':str(log.relative_to(OUT)),'log_sha256':sha(log),
    'resource_diagnostic':bool(re.search(r'timeout|maximum number of heartbeats|WALL_TIMEOUT',txt,re.I))}
  if obj and obj.exists():r['object_sha256']=sha(obj)
  res['runs'].append(r);save();print(suite,label,code,flush=True)
  return r,txt
 def clean_pass(r,txt):
  assert r['exit_code']==0 and 'error:' not in txt and not re.search(r'\b(sorry|admit)\b|declaration uses',txt),r
 def axiom_pass(r,txt,count):
  clean_pass(r,txt)
  blocks=re.findall(r"depends on axioms:\s*\[([^\]]*)\]",txt)
  none=len(re.findall(r'does not depend on any axioms',txt))
  assert len(blocks)+none==count,(len(blocks),none,count)
  for block in blocks:
   assert set(x.strip() for x in block.split(',') if x.strip())<={'propext','Classical.choice','Quot.sound'},block
  return {'count':count,'without_axioms':none,'with_only_standard_axioms':len(blocks)}
 try:
  for suite,target,count in [('runtime','ExactRuntimeCounterexample',167),('cost','ActualExponentialMoments',146)]:
   seq=order(suite,target);assert len(seq)==count
   build=OUT/suite/'build';build.mkdir(parents=True,exist_ok=(suite=='runtime'))
   env={k:v for k,v in os.environ.items() if not k.startswith('LEAN_')};env['LEAN_PATH']=':'.join(map(str,[build]+libs))
   if suite!='runtime':
    for mod,src in seq:
     r,txt=run(suite,mod,src,SOURCE/suite/'src',env,build/Path(*mod.split('.')).with_suffix('.olean'));clean_pass(r,txt)
   res[suite]={'fresh_custom_modules':count,'closure':'PASS'};save()
   if suite=='runtime':
    for label,expected in [('EveryNewAxiom',80),('ExactStatementReview',9)]:
     if label=='EveryNewAxiom' and res[suite].get(label,{}).get('count')==80:continue
     r,txt=run(suite,label,ROOT/(label+'.lean'),ROOT,env)
     res[suite][label]=axiom_pass(r,txt,expected);save()
    r,txt=run(suite,'NegativeProofIndependence',ROOT/'NegativeProofIndependence.lean',ROOT,env);clean_pass(r,txt)
    assert txt.count('PASS_NEGATIVE_PROOF_INDEPENDENCE')==6 and 'PASS_DEPENDENCY_DETECTOR_POSITIVE_CONTROL' in txt
    res[suite]['negative_proof_independence']='PASS_6_TARGETS_WITH_POSITIVE_DETECTOR_CONTROL';save()
    for label in ['WrongOldOld','WrongComputedComputed']:
     r,txt=run(suite,label,ROOT/(label+'.lean'),ROOT,env)
     assert r['exit_code']!=0 and not r['resource_diagnostic'] and ('tactic \'rfl\' failed' in txt or 'type mismatch' in txt),(label,r,txt)
     res[suite][label]='EXPECTED_CONCRETE_REJECTION';save()
   else:
    r,txt=run(suite,'CostReadback',SOURCE/'readbacks/CostReadback.lean',SOURCE/'readbacks',env)
    res[suite]['axiom_readback']=axiom_pass(r,txt,2)
    r,txt=run(suite,'ExactInheritedCostMutant',SOURCE/'cost/mutation/ActualExponentialMoments.lean',SOURCE/'cost/mutation',env)
    assert r['exit_code']!=0 and 'error: application type mismatch' in txt and 'η ≤ ε : Prop' in txt and 'η ≤ ε / 2 : Prop' in txt
    first=txt.index('error: application type mismatch');resource=re.search(r'timeout|maximum number of heartbeats|WALL_TIMEOUT',txt,re.I)
    assert resource is None or first<resource.start()
    res[suite]['mutant']={'disposition':'CONCRETE_PROOF_APPLICATION_REJECTION','rejection_precedes_resource_diagnostic':True,'additional_resource_diagnostic':r['resource_diagnostic'],'unchanged_statement_not_refuted':True};save()
  source_check()
  res.update(status='PASS_INDEPENDENT_REVIEW_CHECKS',finished_utc=now());save()
 except Exception as ex:
  res.update(status='BLOCKED_OR_FAILED',error=repr(ex),finished_utc=now());save();raise
if __name__=='__main__':main()
