#!/usr/bin/env python3
"""Replay the additive literal family after an exact verified core build."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,subprocess,sys,time
if sys.flags.optimize:raise RuntimeError('Optimized Python is refused')
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
PIN='81d7bec2f6bf584d62f5cac7aa32773870dcff4ca33d8d53d5c84cec765f63e4';CORE_PIN='8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--core-packet',type=Path,required=True);p.add_argument('--out',type=Path);p.add_argument('--lean-bin',type=Path);p.add_argument('--mathlib',type=Path);p.add_argument('--mathlib-archive',type=Path);p.add_argument('--existing-core-output',type=Path,help='Explicit reuse only: validate every object of a completed core runtime replay');p.add_argument('--verify-only',action='store_true');a=p.parse_args()
 core=a.core_packet.resolve();assert sha(ROOT/'SOURCE_MANIFEST.json')==PIN and sha(core/'SOURCE_MANIFEST.json')==CORE_PIN
 manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
 for r in manifest['files']:
  f=ROOT/r['path'];assert f.is_file() and not f.is_symlink() and sha(f)==r['sha256'] and f.stat().st_size==r['bytes'],r['path']
 expected={r['path'] for r in manifest['files'] if r['path'].endswith('.lean')}
 assert {str(f.relative_to(ROOT)) for f in ROOT.rglob('*.lean')}==expected
 q=subprocess.run([sys.executable,str(core/'replay.py'),'--verify-only'],capture_output=True,text=True);assert q.returncode==0,q.stdout+q.stderr
 if a.verify_only:print('PASS_LITERAL_AND_CORE_SOURCE_FREEZES');return
 if any(v is None for v in [a.out,a.lean_bin,a.mathlib]):p.error('--out, --lean-bin and --mathlib are required')
 out=a.out.resolve();lean=(a.lean_bin/'lean').resolve();math=a.mathlib.resolve();assert not out.exists()
 for protected in [ROOT,core,lean.parent.parent,math]:assert not out.is_relative_to(protected)
 pins=json.loads((core/'DEPENDENCY_PINS.json').read_text());assert sha(lean)==pins['lean_binary_sha256'];assert subprocess.check_output([str(lean),'--version'],text=True).strip()==pins['lean_version']
 sys.path.insert(0,str(core));from verify_dependency_identity import verify_dependencies
 identity=verify_dependencies(math,a.mathlib_archive,pins)
 out.mkdir(parents=True)
 if a.existing_core_output is None:
  coreout=out/'core';cmd=[sys.executable,str(core/'replay.py'),'--lean-bin',str(a.lean_bin),'--mathlib',str(math),'--out',str(coreout),'--mode','runtime']
  if a.mathlib_archive:cmd+=['--mathlib-archive',str(a.mathlib_archive)]
  q=subprocess.run(cmd,capture_output=True,text=True);(out/'core-driver.log').write_text(q.stdout+q.stderr);assert q.returncode==0
 else:coreout=a.existing_core_output.resolve()
 cr=json.loads((coreout/'RESULT.json').read_text());assert cr['status']=='COMPLETED_FRESH_REPLAY' and cr['source_manifest_sha256']==CORE_PIN
 assert cr['runtime']['custom_modules']==167 and cr['runtime']['axiom_readbacks']==13
 expected_sources={r['path'][12:-5].replace('/','.'):r['sha256'] for r in json.loads((core/'SOURCE_MANIFEST.json').read_text())['sources'] if r['path'].startswith('runtime/src/')}
 seen=set()
 for r in cr['runs']:
  if r['suite']!='runtime' or r['module']=='RuntimeReadback':continue
  assert r['exit_code']==0 and r['source_sha256']==expected_sources[r['module']]
  obj=coreout/'runtime/build'/Path(*r['module'].split('.')).with_suffix('.olean');assert sha(obj)==r['object_sha256'];seen.add(r['module'])
 assert seen==set(expected_sources)
 build=out/'build';build.mkdir();(out/'logs').mkdir();libs=[math/'.lake/build/lib/lean']+sorted((math/'.lake/packages').glob('*/.lake/build/lib/lean'))
 env=dict(os.environ);env.pop('LEAN_SRC_PATH',None);env['LEAN_PATH']=':'.join(map(str,[build,coreout/'runtime/build']+libs))
 result={'status':'RUNNING','started_utc':utc(),'source_manifest_sha256':PIN,'core_source_manifest_sha256':CORE_PIN,'core_receipt_sha256':sha(coreout/'RESULT.json'),'core_objects':'EXPLICIT_COMPLETED_EIGHTH_CORE_REPLAY_REUSE' if a.existing_core_output else 'FRESH_IN_THIS_INVOCATION','literal_objects_reused':False,'core_object_hashes_verified':len(seen),'dependency_identity':identity,'heartbeat_flags_added':False,'parallel_processes':1,'runs':[]}
 save=lambda:(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 def run(n,src,root,obj=None,timeout=180):
  cmd=[str(lean),'-j1','--root='+str(root)]
  if obj:cmd+=['-o',str(obj)]
  cmd+=[str(src)];t=time.monotonic()
  try:q=subprocess.run(cmd,env=env,capture_output=True,text=True,timeout=timeout);txt=q.stdout+q.stderr;code=q.returncode
  except subprocess.TimeoutExpired as ex:txt=(ex.stdout.decode() if isinstance(ex.stdout,bytes) else ex.stdout or '')+'\nWALL_CLOCK_LIMIT\n';code=None
  log=out/'logs'/(n+'.log');log.write_text(txt);row={'module':n,'source_sha256':sha(src),'exit_code':code,'elapsed_seconds':round(time.monotonic()-t,3),'command':cmd,'log':str(log.relative_to(out)),'log_sha256':sha(log),'has_resource_diagnostic':bool(re.search('timeout|WALL_CLOCK_LIMIT',txt))}
  if obj and obj.exists():row['object_sha256']=sha(obj)
  result['runs'].append(row);save();print(n,code,flush=True);assert code==0 and 'error:' not in txt and "declaration uses 'sorry'" not in txt,txt
  return txt
 save()
 try:
  for n in ['LiteralSelectorObstruction','LiteralSelectorFamily','LiteralRuntimeCounterexample']:run(n,ROOT/'src'/(n+'.lean'),ROOT/'src',build/(n+'.olean'))
  txt=run('LiteralAxiomReadback',ROOT/'readbacks/LiteralAxiomReadback.lean',ROOT/'readbacks')
  audits=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',txt);assert len(audits)==7
  for block in audits:assert set(x.strip() for x in block.split(','))<= {'propext','Classical.choice','Quot.sound'}
  run('SelectorNumeralReadback',ROOT/'readbacks/SelectorNumeralReadback.lean',ROOT/'readbacks',timeout=30)
  run('LiteralCodeReadback',ROOT/'readbacks/LiteralCodeReadback.lean',ROOT/'readbacks',timeout=120)
  cmd=[sys.executable,str(ROOT/'check_literal_native.py'),'--readback',str(out/'logs/LiteralCodeReadback.log'),'--codec',str(ROOT/'prcodec.py'),'--out',str(out/'NATIVE_RESULT.json')]
  q=subprocess.run(cmd,capture_output=True,text=True,timeout=90);(out/'logs/native-check.log').write_text(q.stdout+q.stderr);assert q.returncode==0,q.stdout+q.stderr
  native=json.loads((out/'NATIVE_RESULT.json').read_text());assert native['history_cases']==340 and native['all_results_match_independent_reference'] and native['zero_resource_guard_passed']
  result.update(status='PASS_FRESH_LITERAL_MODULES_AXIOM_AND_NATIVE_CHECKS',finished_utc=utc(),axiom_readbacks=7,native_receipt_sha256=sha(out/'NATIVE_RESULT.json'),scope='At least one of two explicit literal Configs is fully certified and refutes the exact mixed target; no evaluated retained-orientation selection; finite native tests are corroboration only');save()
 except Exception as ex:result.update(status='FAILED_CLOSED',error=str(ex),finished_utc=utc());save();raise
if __name__=='__main__':main()
