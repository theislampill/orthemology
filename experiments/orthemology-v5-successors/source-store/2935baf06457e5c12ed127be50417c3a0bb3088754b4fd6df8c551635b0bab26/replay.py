#!/usr/bin/env python3
"""Source-only signed-controller replay. No downloads and no project object reuse."""
from pathlib import Path, PurePosixPath
import argparse, datetime, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, time
sys.dont_write_bytecode=True
if sys.flags.optimize: raise RuntimeError('Optimized Python is refused, including --verify-only')
ROOT=Path(__file__).resolve().parent
MANIFEST_SHA256='768ed23d656626cca7e0c8a15708d0ac0b7d572b47ee2ac6f1f0f74afac83b2b'
CONTROLLER=['OrderedCycle','StageFamily','SubmittedFamily','DirectController','DirectMemoryTransitions','DirectSafety','DirectRun','DirectDynamics','DirectCycling','DirectStability','DirectParity','DirectActualLaw','RationalTest','DirectEndpoint']
NEGATIVE=['Refutation','FiniteLists','IndexedCoverage','FiniteEnumeration','PositiveFormula','SignedService','SignedControllerService']
CONTROLS=['OrderedCycleControls','DirectInterfaceControls','NativeControllerControls','ControllerDependencies']
ALLOWED_AXIOMS={'propext','Classical.choice','Quot.sound'}

def require(condition,message):
 if not condition: raise RuntimeError(message)

def sha(path):
 h=hashlib.sha256()
 with Path(path).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()

def verify_package(root,manifest_sha):
 root=Path(root)
 manifest=root/'PACKAGE_MANIFEST.json'
 require(manifest.is_file() and not manifest.is_symlink(),'Package manifest missing or symlink')
 require(sha(manifest)==manifest_sha,'Package manifest identity changed')
 data=json.loads(manifest.read_text());require(data.get('format')==1,'Unsupported manifest format')
 rows=data['files'];expected={}
 for row in rows:
  name=row['path'];p=PurePosixPath(name)
  require(not p.is_absolute() and '..' not in p.parts and name==str(p) and name not in ('','.','PACKAGE_MANIFEST.json','replay.py') and '\\' not in name,'Unsafe manifest path '+name)
  require(name not in expected,'Manifest duplicate path '+name);expected[name]=row
 actual=set()
 for directory,dirs,files in os.walk(root,followlinks=False):
  for name in dirs+files:
   p=Path(directory)/name;require(not p.is_symlink(),'Package symlink refused: '+str(p))
  for name in files:
   p=Path(directory)/name;require(p.is_file(),'Non-regular package entry');actual.add(str(p.relative_to(root)))
 require(actual==set(expected)|{'PACKAGE_MANIFEST.json','replay.py'},'Package file census mismatch: '+repr(sorted(actual^(set(expected)|{'PACKAGE_MANIFEST.json','replay.py'}))))
 for name,row in expected.items():
  p=root/name;require(p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],'Package source changed: '+name)
 return data

def validate_output(out,protected):
 raw=Path(out);out=raw.resolve()
 require(not raw.exists() and not raw.is_symlink(),'Output directory must be absent')
 for root in protected:require(not out.is_relative_to(Path(root).resolve()),'Output is inside protected input')
 return out

def clean_env(libs,environ=None):
 env=dict(os.environ if environ is None else environ)
 for key in ['LEAN_PATH','LEAN_SRC_PATH','LEAN_SYSROOT','LEAN_OPTS','PYTHONPATH','PYTHONHOME','PYTHONSTARTUP']:env.pop(key,None)
 env['LEAN_PATH']=os.pathsep.join(map(str,libs));env['LEAN_NUM_THREADS']='1';env['PYTHONDONTWRITEBYTECODE']='1'
 return env

def check_outcome(code,expected,txt):
 require(code is not None,'Module wall-clock limit exceeded')
 require(code==expected,'Unexpected compiler exit: '+str(code))
 require("uses 'sorry'" not in txt,'Forbidden sorry declaration')
 if expected==0:require('error:' not in txt,'Compiler error despite zero exit')
 else:
  require(expected==1,'Unsupported failure contract')
  require(txt.count('error:')==1 and txt.count('did not evaluate to `true`')==1 and re.search(r'error: expression\s',txt) is not None,'Failure was not the single intended native guard')
  require(not any(x in txt for x in ['unknown identifier','unknown module','failed to synthesize','ambiguous','unexpected token','invalid field','object file','declaration uses']), 'Infrastructure/type error is not mutation detection')
 for block in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',txt):
  require({x.strip() for x in block.split(',') if x.strip()}<=ALLOWED_AXIOMS,'Unexpected axiom')

def import_verified(path,name):
 spec=importlib.util.spec_from_file_location(name,path);mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def dependency_state(math,lean,archive,project_modules):
 pins=json.loads((ROOT/'ninth/DEPENDENCY_PINS.json').read_text())
 require(sha(lean)==pins['lean_binary_sha256'],'Lean binary digest mismatch')
 require(subprocess.check_output([str(lean),'--version'],text=True,env=clean_env([])).strip()==pins['lean_version'],'Lean version mismatch')
 pkg_names={p['name'] for p in pins['packages'] if p['name']!='mathlib'}
 pkgroot=math/'.lake/packages'
 require({p.name for p in pkgroot.iterdir()}==pkg_names,'Unexpected dependency package census')
 verifier=import_verified(ROOT/'ninth/verify_dependency_identity.py','ninth_dependency_identity')
 identity=verifier.verify_dependencies(math,archive,pins)
 roots={'mathlib':math,**{name:(pkgroot/name).resolve() for name in sorted(pkg_names)}}
 libs=[math/'.lake/build/lib/lean']+sorted(pkgroot.glob('*/.lake/build/lib/lean'))
 require((libs[0]/'Mathlib.olean').is_file(),'Official Mathlib object cache required')
 for lib in libs:
  for mod in project_modules:require(not (lib/Path(*mod.split('.')).with_suffix('.olean')).exists(),'Project object is present in dependency library: '+mod)
 inventory=json.loads((ROOT/'DEPENDENCY_OBJECTS.json').read_text());observed=[]
 for row in inventory['files']:
  path=roots[row['package']]/'.lake/build/lib/lean'/row['path']
  require(path.is_file() and not path.is_symlink() and path.stat().st_size==row['bytes'] and sha(path)==row['sha256'],'Dependency object changed or missing: '+row['package']+'/'+row['path'])
  observed.append(row)
 expected={(r['package'],r['path']) for r in observed}
 actual={(name,str(p.relative_to(root/'.lake/build/lib/lean'))) for name,root in roots.items() for p in (root/'.lake/build/lib/lean').rglob('*.olean')}
 require(actual==expected,'Dependency object census changed')
 return {'identity':identity,'lean_sha256':sha(lean),'dependency_object_manifest_sha256':sha(ROOT/'DEPENDENCY_OBJECTS.json'),'objects_verified':len(observed)},libs,list(roots.values())

def derive_negative_mutants(out):
 source=ROOT/'service/negative/src/IndexedCoverage.lean';base=source.read_text();base=base[:base.index('/-- Acceptance forces')]
 contract=json.loads((ROOT/'MUTATION_CONTRACT.json').read_text());rows=[]
 for item in contract['source_derived_negative']:
  require(sha(source)==item['source_sha256'],'Mutant derivation source changed')
  require(base.count(item['anchor'])==1,'Mutant derivation anchor mismatch')
  body=base.replace(item['anchor'],item['replacement'])
  body=body.replace('namespace OrthemicCertificate.Signed','namespace OrthemicCertificate.'+item['namespace']+'\nopen OrthemicCertificate.Signed')
  body+='\n'+item['guard']+'\nend OrthemicCertificate.'+item['namespace']+'\n'
  path=out/(item['name']+'.lean');path.write_text(body)
  require(sha(path)==item['derived_sha256'],'Derived negative mutant bytes changed');rows.append(path)
 return rows

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--verify-only',action='store_true');ap.add_argument('--lean-bin',type=Path);ap.add_argument('--mathlib',type=Path);ap.add_argument('--mathlib-archive',type=Path);ap.add_argument('--out',type=Path)
 a=ap.parse_args();verify_package(ROOT,MANIFEST_SHA256);wrapper_before=sha(ROOT/'replay.py')
 if a.verify_only:
  print('PASS_EXACT_PACKAGE_CENSUS_AND_HASHES. No proof replay performed.');return
 if any(v is None for v in [a.lean_bin,a.mathlib,a.out]):ap.error('--lean-bin, --mathlib and --out are required')
 math=a.mathlib.resolve();lean=(a.lean_bin/'lean').resolve()
 pins=json.loads((ROOT/'ninth/DEPENDENCY_PINS.json').read_text())
 dep_roots=[math]+[(math/'.lake/packages'/p['name']).resolve() for p in pins['packages'] if p['name']!='mathlib']
 out=validate_output(a.out,[ROOT,lean.parent.parent,*dep_roots])
 nm=json.loads((ROOT/'ninth/SOURCE_MANIFEST.json').read_text())
 modules=[r['module'] for r in nm['sources']]+CONTROLLER+NEGATIVE+CONTROLS+['SmallFixtures','IndependentControls','DeclarationAudit']
 pre,libs,_=dependency_state(math,lean,a.mathlib_archive,modules)
 out.mkdir(parents=True);(out/'logs').mkdir();new=out/'service';new.mkdir();build=new/'build';build.mkdir();cg=new/'codegen';cg.mkdir();logs=new/'logs';logs.mkdir()
 result={'format':1,'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_sha256':MANIFEST_SHA256,'wrapper_sha256':wrapper_before,'dependency_before':pre,'project_objects_reused':False,'ninth_modules':95,'new_modules':21,'distinct_project_production_modules':116,'separate_sixteenth_core_included':False,'jobs':1,'module_wall_seconds':180,'new_production_heartbeats':'unchanged default','audit_only_unlimited_heartbeats':['DeclarationAudit'],'linked_binary_parser_physical_or_practical_complexity_claim':False,'runs':[]}
 def save():(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 def run(label,src,expected=0,obj=None,cfile=None):
  cmd=[str(lean),'-j1','--root='+str(src.parent)]
  if obj:cmd+=['-o',str(obj)]
  if cfile:cmd+=['-c',str(cfile)]
  cmd+=[str(src)];started=time.monotonic();txt='';rc=None
  try:
   p=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180);txt=p.stdout;rc=p.returncode
  except subprocess.TimeoutExpired as ex:txt=(ex.stdout.decode() if isinstance(ex.stdout,bytes) else ex.stdout or '')+'\nWALL_CLOCK_LIMIT_180\n'
  log=logs/(label+'.log');log.write_text(txt)
  rec={'label':label,'source_sha256':sha(src),'exit_code':rc,'expected_exit':expected,'elapsed_seconds':round(time.monotonic()-started,3),'log':str(log.relative_to(out)),'log_sha256':sha(log)}
  if obj and rc==0:rec['object_sha256']=sha(obj)
  if cfile and cfile.exists():rec.update(c_sha256=sha(cfile),c_bytes=cfile.stat().st_size)
  result['runs'].append(rec);save();print(label,rc,flush=True);check_outcome(rc,expected,txt)
 save()
 try:
  # The unchanged predecessor wrapper builds all 95 production modules and its complete controls.
  cmd=[sys.executable,'-B',str(ROOT/'ninth/replay.py'),'--lean-bin',str(lean.parent),'--mathlib',str(math),'--out',str(out/'ninth')]
  if a.mathlib_archive:cmd+=['--mathlib-archive',str(a.mathlib_archive.resolve())]
  with (out/'logs/ninth-console.log').open('w') as f:rc=subprocess.run(cmd,env=clean_env(libs),stdout=f,stderr=subprocess.STDOUT).returncode
  require(rc==0,'Fresh unchanged Ninth replay failed; retained logs/ninth-console.log')
  prior=json.loads((out/'ninth/RESULT.json').read_text())
  require(prior['status']=='PASS_FRESH_CLOSURE_CONTROLS_AXIOMS_AUDIT_CODEGEN_AND_MUTATIONS','Ninth replay did not pass')
  require(len(prior['runs'])==120,'Ninth run census changed')
  for rec in prior['runs']:
   check_outcome(rec['exit_code'],rec['expected_exit'],(out/'ninth'/rec['log']).read_text())
  result['ninth_result_sha256']=sha(out/'ninth/RESULT.json');result['ninth_runs']=120;save();print('NINTH_FRESH_95_PASS',flush=True)
  env=clean_env([build,out/'ninth/build',*libs])
  for family,order in [('controller',CONTROLLER),('negative',NEGATIVE)]:
   for mod in order:run(mod,ROOT/'service'/family/'src'/(mod+'.lean'),obj=build/(mod+'.olean'),cfile=cg/(mod+'.c'))
  for mod in CONTROLS:run(mod,ROOT/'service/controller/tests'/(mod+'.lean'),obj=build/(mod+'.olean'))
  run('SmallFixtures',ROOT/'service/negative/tests/SmallFixtures.lean',obj=build/'SmallFixtures.olean')
  for src in sorted((ROOT/'service/negative/tests').glob('*.lean')):
   if src.stem!='SmallFixtures':run(src.stem,src,obj=build/(src.stem+'.olean'))
  for mod in ['IndependentControls','DeclarationAudit']:run(mod,ROOT/'review'/(mod+'.lean'),obj=build/(mod+'.olean'))
  # Rebuild source-derived controller probes in scratch and compare frozen generated bytes.
  derived=out/'derived-controller';derived.mkdir();(derived/'src').mkdir()
  for mod in ['DirectEndpoint','DirectController','RationalTest']:shutil.copyfile(ROOT/'service/controller/src'/(mod+'.lean'),derived/'src'/(mod+'.lean'))
  shutil.copyfile(ROOT/'service/controller/derive_mutations.py',derived/'derive_mutations.py')
  p=subprocess.run([sys.executable,'-B',str(derived/'derive_mutations.py')],env=clean_env([]),capture_output=True,text=True)
  (out/'logs/mutation-derivation.log').write_text(p.stdout+p.stderr);require(p.returncode==0,'Controller derivation failed')
  for generated in sorted((derived/'mutations').iterdir()):require(sha(generated)==sha(ROOT/'service/controller/mutations'/generated.name),'Controller mutation derivation mismatch')
  for family in ['controller','negative']:
   for src in sorted((ROOT/'service'/family/'mutations').glob('*.lean')):run('Mutation-'+src.stem,src,expected=1)
  nd=out/'derived-negative';nd.mkdir()
  for src in derive_negative_mutants(nd):run('Mutation-'+src.stem,src,expected=1)
  require(len(result['runs'])==52,'New-lane run census changed')
  verify_package(ROOT,MANIFEST_SHA256);require(sha(ROOT/'replay.py')==wrapper_before,'Wrapper changed during replay')
  post,_,_=dependency_state(math,lean,a.mathlib_archive,modules);require(pre==post,'Dependency identity changed during replay')
  result.update(status='PASS_FRESH_95_PLUS_21_SOURCE_CONTROLS_AUDITS_CODEGEN_MUTATIONS',finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),dependency_after=post,new_runs=52,total_runs=172,positive_new_runs=44,expected_fail_new_runs=8,source_unchanged_after=True);save()
 except Exception as ex:
  result.update(status='FAILED_CLOSED',error=str(ex),finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());save();raise

if __name__=='__main__':main()
