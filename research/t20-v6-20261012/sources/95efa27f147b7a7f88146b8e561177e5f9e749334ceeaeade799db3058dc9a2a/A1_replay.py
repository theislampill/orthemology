#!/usr/bin/env python3
"""Fresh additive A1 check after explicit exact-source core verification; no native probes."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,subprocess,sys,time
if sys.flags.optimize:raise RuntimeError('Optimized Python refused')
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
CORE='8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c'
LITERAL='81d7bec2f6bf584d62f5cac7aa32773870dcff4ca33d8d53d5c84cec765f63e4'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
p=argparse.ArgumentParser(description=__doc__)
for x in ['core-packet','literal-packet','core-output','lean-bin','mathlib','out']:p.add_argument('--'+x,type=Path,required=True)
p.add_argument('--mathlib-archive',type=Path);p.add_argument('--expected-manifest-sha256',required=True)
a=p.parse_args();core=a.core_packet.resolve();literal=a.literal_packet.resolve();co=a.core_output.resolve();out=a.out.resolve();lean=(a.lean_bin/'lean').resolve();math=a.mathlib.resolve()
assert sha(ROOT/'SOURCE_MANIFEST.json')==a.expected_manifest_sha256
manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
for r in manifest['files']:
 f=ROOT/r['path'];assert f.is_file() and not f.is_symlink() and sha(f)==r['sha256'] and f.stat().st_size==r['bytes']
assert not out.exists()
for protected in [ROOT,core,literal,co,math,lean.parent.parent]:assert not out.is_relative_to(protected)
assert sha(core/'SOURCE_MANIFEST.json')==CORE and sha(literal/'SOURCE_MANIFEST.json')==LITERAL
pins=json.loads((core/'DEPENDENCY_PINS.json').read_text());assert sha(lean)==pins['lean_binary_sha256'];assert subprocess.check_output([str(lean),'--version'],text=True).strip()==pins['lean_version']
sys.path.insert(0,str(core));from verify_dependency_identity import verify_dependencies
identity=verify_dependencies(math,a.mathlib_archive,pins)
cm=json.loads((core/'SOURCE_MANIFEST.json').read_text());expected={r['path'][12:-5].replace('/','.'):r for r in cm['sources'] if r['path'].startswith('runtime/src/')}
for r in expected.values():assert sha(core/r['path'])==r['sha256'] and (core/r['path']).stat().st_size==r['bytes']
cr=json.loads((co/'RESULT.json').read_text());assert cr['status']=='COMPLETED_FRESH_REPLAY' and cr['source_manifest_sha256']==CORE
seen=set()
for r in cr['runs']:
 if r['suite']!='runtime' or r['module']=='RuntimeReadback':continue
 assert r['exit_code']==0 and r['source_sha256']==expected[r['module']]['sha256']
 obj=co/'runtime/build'/Path(*r['module'].split('.')).with_suffix('.olean');assert obj.is_file() and sha(obj)==r['object_sha256'];seen.add(r['module'])
assert seen==set(expected) and len(seen)==167
lm={r['path']:r for r in json.loads((literal/'SOURCE_MANIFEST.json').read_text())['files']}
build=out/'build';build.mkdir(parents=True);(out/'logs').mkdir()
libs=[math/'.lake/build/lib/lean']+sorted((math/'.lake/packages').glob('*/.lake/build/lib/lean'))
env=dict(os.environ);env.pop('LEAN_SRC_PATH',None);env['LEAN_PATH']=':'.join(map(str,[build,co/'runtime/build']+libs))
result={'status':'RUNNING','started_utc':utc(),'source_manifest_sha256':sha(ROOT/'SOURCE_MANIFEST.json'),'driver_sha256':sha(__file__),'dependency_identity':identity,'core_receipt_sha256':sha(co/'RESULT.json'),'core_source_object_pairs_verified':len(seen),'additive_objects_reused':False,'native_probes_run':False,'historical_probes_retried':False,'heartbeat_flags_added':False,'wall_clock_per_module_seconds':180,'runs':[]}
save=lambda:(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
def run(name,src,root):
 obj=build/(name+'.olean');cmd=[str(lean),'-j1','--root='+str(root),'-o',str(obj),str(src)];t=time.monotonic()
 try:q=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180);txt=q.stdout;code=q.returncode
 except subprocess.TimeoutExpired as ex:txt=(ex.stdout.decode() if isinstance(ex.stdout,bytes) else ex.stdout or '')+'\nWALL_CLOCK_LIMIT_180_SECONDS\n';code=None
 log=out/'logs'/(name+'.log');log.write_text(txt);r={'module':name,'source_sha256':sha(src),'exit_code':code,'elapsed_seconds':time.monotonic()-t,'command':cmd,'log':str(log.relative_to(out)),'log_sha256':sha(log)}
 if obj.exists():r['object_sha256']=sha(obj)
 result['runs'].append(r);save();print(name,code,flush=True)
 assert code==0 and 'error:' not in txt and "declaration uses 'sorry'" not in txt,txt
 return txt
save()
try:
 for name in ['LiteralSelectorObstruction','LiteralSelectorFamily']:
  src=literal/'src'/(name+'.lean');r=lm['src/'+name+'.lean'];assert sha(src)==r['sha256'] and src.stat().st_size==r['bytes'];run(name,src,literal/'src')
 for name in ['FiniteRadixNormalForm','SelectorTableNormalForm']:run(name,ROOT/'src'/(name+'.lean'),ROOT/'src')
 txt=run('A1AxiomReadback',ROOT/'src/A1AxiomReadback.lean',ROOT/'src')
 audits=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",txt)
 expected_names={r['name'] for r in manifest['declarations']};assert {n for n,_ in audits}==expected_names and len(audits)==len(expected_names)==49
 for n,block in audits:assert set(x.strip() for x in block.split(','))<= {'propext','Classical.choice','Quot.sound'},(n,block)
 result.update(status='PASS_FRESH_A1_PROOFS_AND_ALL_DECLARATION_AXIOMS',finished_utc=utc(),axiom_declarations=49,definitions=7,theorems=42);save()
except Exception as ex:result.update(status='FAILED_CLOSED',error=str(ex),finished_utc=utc());save();raise
