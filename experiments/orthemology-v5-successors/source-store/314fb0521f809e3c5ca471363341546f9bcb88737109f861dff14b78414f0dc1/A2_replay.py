#!/usr/bin/env python3
"""Fresh A2 proof checks with exact source/object censuses for verified A1/core reuse."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,subprocess,sys,time
if sys.flags.optimize:raise RuntimeError('Optimized Python refused')
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
CORE='8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c'
LITERAL='81d7bec2f6bf584d62f5cac7aa32773870dcff4ca33d8d53d5c84cec765f63e4'
A1='923206fcb0d870806b6e77ca259f99e0604876ac872d97c0bf70c100fb460bd3'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
utc=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
p=argparse.ArgumentParser(description=__doc__)
for x in ['core-packet','literal-packet','core-output','a1-packet','a1-output','lean-bin','mathlib','out']:p.add_argument('--'+x,type=Path,required=True)
p.add_argument('--mathlib-archive',type=Path);p.add_argument('--expected-manifest-sha256',required=True)
a=p.parse_args();core=a.core_packet.resolve();literal=a.literal_packet.resolve();co=a.core_output.resolve();a1=a.a1_packet.resolve();ao=a.a1_output.resolve();out=a.out.resolve();lean=(a.lean_bin/'lean').resolve();math=a.mathlib.resolve()
assert sha(ROOT/'SOURCE_MANIFEST.json')==a.expected_manifest_sha256,'A2 manifest mismatch'
manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
for r in manifest['files']:
 f=ROOT/r['path'];assert f.is_file() and not f.is_symlink() and sha(f)==r['sha256'] and f.stat().st_size==r['bytes'],r['path']
assert {str(x.relative_to(ROOT)) for x in (ROOT/'src').rglob('*.lean')}=={x['path'] for x in manifest['files'] if x['path'].endswith('.lean')},'Unexpected A2 source'
assert not list(ROOT.rglob('*.olean')),'A2 source packet contains compiled objects'
assert not out.exists(),'Output must be absent'
for protected in [ROOT,core,literal,co,a1,ao,math,lean.parent.parent]:assert not out.is_relative_to(protected),'Output inside protected input'
assert sha(core/'SOURCE_MANIFEST.json')==CORE and sha(literal/'SOURCE_MANIFEST.json')==LITERAL and sha(a1/'SOURCE_MANIFEST.json')==A1,'Dependency source-manifest mismatch'
pins=json.loads((core/'DEPENDENCY_PINS.json').read_text());assert sha(lean)==pins['lean_binary_sha256'];assert subprocess.check_output([str(lean),'--version'],text=True).strip()==pins['lean_version']
sys.path.insert(0,str(core));from verify_dependency_identity import verify_dependencies
identity=verify_dependencies(math,a.mathlib_archive,pins)
cm=json.loads((core/'SOURCE_MANIFEST.json').read_text());expected_core={r['path'][12:-5].replace('/','.'):r for r in cm['sources'] if r['path'].startswith('runtime/src/')}
for r in expected_core.values():
 f=core/r['path'];assert f.is_file() and not f.is_symlink() and sha(f)==r['sha256'] and f.stat().st_size==r['bytes']
cr=json.loads((co/'RESULT.json').read_text());assert cr['status']=='COMPLETED_FRESH_REPLAY' and cr['source_manifest_sha256']==CORE
core_runs={r['module']:r for r in cr['runs'] if r['suite']=='runtime' and r['module']!='RuntimeReadback'}
assert len(core_runs)==len(expected_core)==167 and set(core_runs)==set(expected_core)
def check_object_census(build,runs,sources):
 actual={str(x.relative_to(build)) for x in build.rglob('*.olean')}
 expected={str(Path(*name.split('.')).with_suffix('.olean')) for name in runs}
 assert actual==expected,'Unexpected or missing custom object: '+repr(sorted(actual^expected))
 for f in build.rglob('*'):assert not f.is_symlink(),'Custom object tree has symlink: '+str(f)
 for name,r in runs.items():
  assert r['exit_code']==0 and r['source_sha256']==sources[name]
  obj=build/Path(*name.split('.')).with_suffix('.olean');assert obj.is_file() and sha(obj)==r['object_sha256'],name
 return len(actual)
core_count=check_object_census(co/'runtime/build',core_runs,{n:r['sha256'] for n,r in expected_core.items()})
a1m=json.loads((a1/'SOURCE_MANIFEST.json').read_text())
for r in a1m['files']:
 f=a1/r['path'];assert f.is_file() and not f.is_symlink() and sha(f)==r['sha256'] and f.stat().st_size==r['bytes']
lm={r['path']:r for r in json.loads((literal/'SOURCE_MANIFEST.json').read_text())['files']}
a1_sources={r['path'][4:-5]:r['sha256'] for r in a1m['files'] if r['path'].startswith('src/') and r['path'].endswith('.lean')}
for n in ['LiteralSelectorObstruction','LiteralSelectorFamily']:
 r=lm['src/'+n+'.lean'];f=literal/r['path'];assert f.is_file() and not f.is_symlink() and sha(f)==r['sha256'] and f.stat().st_size==r['bytes'];a1_sources[n]=r['sha256']
ar=json.loads((ao/'RESULT.json').read_text());assert ar['status']=='PASS_FRESH_A1_PROOFS_AND_ALL_DECLARATION_AXIOMS' and ar['source_manifest_sha256']==A1
assert ar['core_receipt_sha256']==sha(co/'RESULT.json'),'A1/core output lineage mismatch'
a1_runs={r['module']:r for r in ar['runs']};assert len(a1_runs)==len(a1_sources)==5 and set(a1_runs)==set(a1_sources)
a1_count=check_object_census(ao/'build',a1_runs,a1_sources)
build=out/'build';build.mkdir(parents=True);(out/'logs').mkdir()
libs=[math/'.lake/build/lib/lean']+sorted((math/'.lake/packages').glob('*/.lake/build/lib/lean'))
env=dict(os.environ);env.pop('LEAN_SRC_PATH',None);env['LEAN_PATH']=':'.join(map(str,[build,ao/'build',co/'runtime/build']+libs))
result={'status':'RUNNING','started_utc':utc(),'source_manifest_sha256':sha(ROOT/'SOURCE_MANIFEST.json'),'driver_sha256':sha(__file__),'dependency_identity':identity,'core_receipt_sha256':sha(co/'RESULT.json'),'a1_receipt_sha256':sha(ao/'RESULT.json'),'core_source_object_pairs_verified':core_count,'a1_source_object_pairs_verified':a1_count,'exact_custom_object_censuses':True,'custom_object_symlinks':False,'additive_objects_reused':False,'native_probes_run':False,'historical_probes_retried':False,'heartbeat_flags_added':False,'wall_clock_per_module_seconds':180,'runs':[]}
save=lambda:(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
def run(name):
 src=ROOT/'src'/(name+'.lean');obj=build/(name+'.olean');cmd=[str(lean),'-j1','--root='+str(ROOT/'src'),'-o',str(obj),str(src)];t=time.monotonic()
 try:q=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180);txt=q.stdout;code=q.returncode
 except subprocess.TimeoutExpired as ex:txt=(ex.stdout.decode() if isinstance(ex.stdout,bytes) else ex.stdout or '')+'\nWALL_CLOCK_LIMIT_180_SECONDS\n';code=None
 log=out/'logs'/(name+'.log');log.write_text(txt);r={'module':name,'source_sha256':sha(src),'exit_code':code,'elapsed_seconds':time.monotonic()-t,'command':cmd,'log':str(log.relative_to(out)),'log_sha256':sha(log)}
 if obj.exists():r['object_sha256']=sha(obj)
 result['runs'].append(r);save();print(name,code,flush=True)
 assert code==0 and 'error:' not in txt and "declaration uses 'sorry'" not in txt,txt
 return txt
save()
try:
 for name in ['SelectorCallDomains','SelectorSemanticTransport']:run(name)
 txt=run('A2AxiomReadback')
 audits=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",txt)
 audits += [(n, "") for n in re.findall(r"'([^']+)' does not depend on any axioms",txt)]
 expected_names={r['name'] for r in manifest['declarations']};assert {n for n,_ in audits}==expected_names and len(audits)==len(expected_names)==72
 for n,block in audits:assert set(x.strip() for x in block.split(',') if x.strip())<= {'propext','Classical.choice','Quot.sound'},(n,block)
 result.update(status='PASS_FRESH_A2_DOMAINS_TRANSPORT_AND_ALL_AXIOMS',finished_utc=utc(),axiom_declarations=72,definitions=11,theorems=61);save()
except Exception as ex:result.update(status='FAILED_CLOSED',error=str(ex),finished_utc=utc());save();raise
