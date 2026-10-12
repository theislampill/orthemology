#!/usr/bin/env python3
"""Independent additive review against only this reviewer's fresh core objects."""
from pathlib import Path
import ast,datetime,hashlib,importlib.util,json,os,re,subprocess,sys,time
if sys.flags.optimize:raise RuntimeError('Optimized Python refused')
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent;SOURCE=ROOT/'literal-snapshot';CORE=ROOT/'snapshot';COREOUT=ROOT/'fresh-independent01';OUT=ROOT/'literal-independent01'
LEAN=Path('${LEAN_BIN}/lean');MATH=Path('${MATHLIB}')
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest();utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
write=lambda p,x:Path(p).write_text(json.dumps(x,indent=2)+'\n')
def main():
 assert sha(SOURCE/'SOURCE_MANIFEST.json')=='81d7bec2f6bf584d62f5cac7aa32773870dcff4ca33d8d53d5c84cec765f63e4'
 assert sha(CORE/'SOURCE_MANIFEST.json')=='8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c'
 lm=json.loads((SOURCE/'SOURCE_MANIFEST.json').read_text());cm=json.loads((CORE/'SOURCE_MANIFEST.json').read_text())
 for r in lm['files']:
  p=SOURCE/r['path'];assert p.is_file() and not p.is_symlink() and sha(p)==r['sha256'] and p.stat().st_size==r['bytes']
 assert {str(p.relative_to(SOURCE)) for p in SOURCE.rglob('*.lean')}=={r['path'] for r in lm['files'] if r['path'].endswith('.lean')}
 cr=json.loads((COREOUT/'RESULT.json').read_text());assert cr['status'] in ['PASS_CORE_WITH_EXPLICIT_AUXILIARY_LIMITATIONS','PASS_INDEPENDENT_REVIEW_CHECKS']
 assert cr['runtime']['closure']=='PASS' and cr['cost']['closure']=='PASS'
 sources={r['path'][12:-5].replace('/','.'):r['sha256'] for r in cm['sources'] if r['path'].startswith('runtime/src/')}
 verified=[]
 for r in cr['runs'][:167]:
  assert r['suite']=='runtime' and r['exit_code']==0 and r['source_sha256']==sources[r['label']]
  p=COREOUT/'runtime/build'/Path(*r['label'].split('.')).with_suffix('.olean');assert sha(p)==r['object_sha256']
  verified.append({'module':r['label'],'source_sha256':r['source_sha256'],'object_sha256':r['object_sha256']})
 assert len(verified)==167 and {x['module'] for x in verified}==set(sources)
 pins=json.loads((CORE/'DEPENDENCY_PINS.json').read_text());assert sha(LEAN)==pins['lean_binary_sha256']
 spec=importlib.util.spec_from_file_location('depverify',CORE/'verify_dependency_identity.py');d=importlib.util.module_from_spec(spec);spec.loader.exec_module(d)
 dependency=d.verify_dependencies(MATH,ARCHIVE,pins)
 assert not OUT.exists();OUT.mkdir();build=OUT/'build';build.mkdir();(OUT/'logs').mkdir()
 write(OUT/'OWN_FRESH_CORE_BINDINGS.json',verified)
 res={'status':'RUNNING','started_utc':utc(),'source_manifest_sha256':sha(SOURCE/'SOURCE_MANIFEST.json'),'core_source_manifest_sha256':sha(CORE/'SOURCE_MANIFEST.json'),'core_receipt_sha256':sha(COREOUT/'RESULT.json'),'own_core_objects_verified':167,'core_bindings_sha256':sha(OUT/'OWN_FRESH_CORE_BINDINGS.json'),'author_custom_objects_reused':False,'literal_objects_reused':False,'runner_sha256':sha(__file__),'dependency_identity':dependency,'heartbeat_flags_added':False,'parallel_lean_processes':1,'runs':[]}
 save=lambda:write(OUT/'RESULT.json',res);save()
 libs=[MATH/'.lake/build/lib/lean']+sorted((MATH/'.lake/packages').glob('*/.lake/build/lib/lean'))
 env={k:v for k,v in os.environ.items() if not k.startswith('LEAN_')};env['LEAN_PATH']=':'.join(map(str,[build,COREOUT/'runtime/build']+libs))
 def run(label,src,root,obj=None,limit=180):
  cmd=[str(LEAN),'-j1','--root='+str(root)]
  if obj:cmd+=['-o',str(obj)]
  cmd+=[str(src)];t=time.monotonic()
  try:p=subprocess.run(cmd,cwd=ROOT,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=limit);txt=p.stdout;code=p.returncode
  except subprocess.TimeoutExpired as e:txt=(e.stdout.decode() if isinstance(e.stdout,bytes) else e.stdout or '')+'\nRESOURCE_LIMIT\n';code=None
  log=OUT/'logs'/(label+'.log');log.write_text(txt)
  r={'label':label,'source_sha256':sha(src),'exit_code':code,'elapsed_seconds':round(time.monotonic()-t,3),'command':cmd,'log':str(log.relative_to(OUT)),'log_sha256':sha(log)}
  if obj and obj.exists():r['object_sha256']=sha(obj)
  res['runs'].append(r);save();print(label,code,flush=True)
  assert code==0 and 'error:' not in txt and not re.search(r'\b(sorry|admit)\b|declaration uses',txt),(label,txt)
  return txt
 def audit(txt,count):
  blocks=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',txt);none=len(re.findall('does not depend on any axioms',txt))
  assert len(blocks)+none==count,(len(blocks),none,count)
  for b in blocks:assert set(x.strip() for x in b.split(',') if x.strip())<={'propext','Classical.choice','Quot.sound'}
  return {'count':count,'empty':none,'standard_only':len(blocks)}
 try:
  for label in ['LiteralSelectorObstruction','LiteralSelectorFamily','LiteralRuntimeCounterexample']:
   run(label,SOURCE/'src'/(label+'.lean'),SOURCE/'src',build/(label+'.olean'))
  res['all_new_axioms']=audit(run('EveryLiteralAxiom',ROOT/'EveryLiteralAxiom.lean',ROOT),56);save()
  res['endpoint_correspondence']=audit(run('LiteralEndpointReview',ROOT/'LiteralEndpointReview.lean',ROOT),2);save()
  numerals=run('SelectorNumeralReadback',SOURCE/'readbacks/SelectorNumeralReadback.lean',SOURCE/'readbacks',limit=30)
  assert '44812' in numerals and '24332' in numerals and numerals.count('428783445879334172098560')==2 and numerals.count('64080')==2
  code=run('LiteralCodeReadback',SOURCE/'readbacks/LiteralCodeReadback.lean',SOURCE/'readbacks',limit=120)
  values={line.split('=',1)[0]:line.split('=',1)[1] for line in code.splitlines() if '_BYTES=' in line}
  expected={'OLD_FALSE':'40f25f3bd087bfb672d9a390913e6959bd399d6bfa90889d4c4d935f91c4eb40','OLD_TRUE':'1bc2df93721979bb9806940d69d03a331d87964b61fb35e1de15fafcc3314424','COMPUTED_FALSE':'08ed35c82f63c180f1c5ea4778efbbebc70521cec514bf9870ab91c558eb7908','COMPUTED_TRUE':'d1a9ed7903def5a682f334d816ab3615bd2f8ef9b350149442404ca1fcd4712f'}
  (OUT/'programs').mkdir();res['programs']=[]
  for name,h in expected.items():
   b=bytes(ast.literal_eval(values[name+'_BYTES']));assert len(b)==48389 and hashlib.sha256(b).hexdigest()==h
   (OUT/'programs'/(name+'.bin')).write_bytes(b);res['programs'].append({'name':name,'bytes':len(b),'sha256':h})
  save()
  cmd=[sys.executable,str(SOURCE/'check_literal_native.py'),'--readback',str(OUT/'logs/LiteralCodeReadback.log'),'--codec',str(SOURCE/'prcodec.py'),'--out',str(OUT/'NATIVE_RESULT.json')]
  cp=subprocess.run(cmd,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=90);log=OUT/'logs/native.log';log.write_text(cp.stdout)
  assert cp.returncode==0,cp.stdout
  nr=json.loads((OUT/'NATIVE_RESULT.json').read_text());assert nr['status']=='PASS_BOUNDED_LITERAL_PARSED_CODE' and nr['history_cases']==340 and nr['zero_resource_guard_passed'] and nr['all_results_match_independent_reference']
  assert len(nr['cases'])==340 and all(x['actual']==x['expected'] for x in nr['cases'])
  res.update(status='PASS_INDEPENDENT_LITERAL_ADDENDUM',finished_utc=utc(),native_command=cmd,native_receipt_sha256=sha(OUT/'NATIVE_RESULT.json'),native_log_sha256=sha(log),claim='At least one of two explicit literal Configs certifies every inherited hypothesis and has positive-measure exact mixed-decoder failure. No evaluated retained orientation; parsed finite execution is separate corroboration, not direct Lean denotation or infinite-horizon proof.')
  save()
 except Exception as e:res.update(status='BLOCKED_OR_FAILED',error=repr(e),finished_utc=utc());save();raise
if __name__=='__main__':main()
