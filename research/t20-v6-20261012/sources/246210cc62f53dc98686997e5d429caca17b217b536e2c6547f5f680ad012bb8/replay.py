#!/usr/bin/env python3
"""Relocation-safe bounded replay. Never builds/updates external dependencies."""
from pathlib import Path
import argparse,hashlib,json,os,re,shutil,subprocess,sys,time,platform
R=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__)
ap.add_argument('--lean-home',type=Path,required=True,help='Lean 4.19.0 distribution root, containing bin/lean, lib/lean and src/lean')
ap.add_argument('--packages-dir',type=Path,required=True,help='Directory containing the pinned Mathlib and peer package checkouts with retained .lake/build/lib/lean objects')
ap.add_argument('--output',type=Path,required=True,help='New, nonexistent replay-output directory outside this packet')
a=ap.parse_args(); out=a.output.resolve(); leanhome=a.lean_home.resolve(); packages=a.packages_dir.resolve()
assert not out.exists(),'Refusing to reuse a possibly stale output directory'
assert out!=R and R not in out.parents,'Output must be outside the immutable packet'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def write(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def check_manifest():
 m=read(R/'MANIFEST.json')
 for row in m['files']:
  p=R/row['path'];assert p.is_file() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'],('packet integrity',row['path'])
 return len(m['files'])
packet_count=check_manifest();out.mkdir(parents=True); logs=out/'logs';logs.mkdir();lib=out/'lib';lib.mkdir()
record={'status':'RUNNING','packet_manifest_sha256':sha(R/'MANIFEST.json'),'packet_files_verified':packet_count,'python':sys.version,'platform':platform.platform(),'trust':0,'external_dependencies_rebuilt':False,'modules':[],'negative_controls':[],'symbolic_checks':[]}
write(out/'REPLAY_RECEIPT.json',record)
try:
 pins=read(R/'prerequisites/RUNTIME_PINS.json');lean=leanhome/'bin/lean'
 assert sha(lean)==pins['lean_executable_sha256'],'Lean executable identity differs'
 for runtime in pins['lean_runtime_shared_libraries']:
  assert sha(leanhome/runtime['path'])==runtime['sha256'],('Lean runtime identity differs',runtime['path'])
 version=subprocess.check_output([str(lean),'--version'],text=True).strip();assert version==pins['lean_version'],version
 import sympy,mpmath
 assert sympy.__version__==pins['sympy'] and mpmath.__version__==pins['mpmath'],'Use the pinned symbolic runtime'
 record.update(lean_version=version,lean_executable_sha256=sha(lean),sympy=sympy.__version__,mpmath=mpmath.__version__)
 roots={'lean_home':leanhome,'packages':packages}; depdata=read(R/'prerequisites/EXTERNAL_DEPENDENCIES.json');external={}
 for row in depdata['entries']:
  for kind in ['source','object']:
   spec=row[kind];p=roots[spec['root']]/spec['path'];assert p.is_file() and sha(p)==spec['sha256'],('dependency identity',row['module'],kind,str(p))
   if kind=='object':external[str(p.resolve())]=spec['sha256']
 assert len(external)==2447
 record['external_source_object_pairs_verified']=len(external)
 write(out/'DEPENDENCY_CHECK.json',{'status':'PASS','source_object_pairs_verified':len(external),'objects_rebuilt':False,'source_graph_manifest_sha256':sha(R/'prerequisites/EXTERNAL_DEPENDENCIES.json'),'resolved_roots':{k:str(v) for k,v in roots.items()}})
 src=R/'sources/lean-truncated-moment-obstruction-20261010'; review=R/'sources/polynomial-moment-certificate-independent-review-20261010'
 order=['TruncatedMoment','ScalarPositivity','DegreeBridge','Certificate','Controls','MomentValues','Verify']
 needed_packages={r['object']['path'].split('/')[0] for r in depdata['entries'] if r['object']['root']=='packages'}
 search=[lib]+[packages/p/'.lake/build/lib/lean' for p in pins['package_search_order'] if p in needed_packages]
 assert all(p.is_dir() for p in search),search
 env=dict(os.environ,LEAN_PATH=':'.join(map(str,search)),PYTHONDONTWRITEBYTECODE='1')
 # Do not retain inherited Lean search overrides that could redirect the toolchain.
 env.pop('LEAN_SYSROOT',None)
 record['lean_path']=list(map(str,search));own={}; direct={}
 original_objects={r['module']:r['object_sha256'] for r in read(src/'REPLAY_RECEIPT.json')['module_results']}
 axiom_counts={'Verify':16,'IndependentProbes':2,'AllAxiomClosures':72}
 all_axioms={}
 for mod in order+['IndependentProbes','AllAxiomClosures']:
  source=(src if mod in order else review)/(mod+'.lean');dest=lib/(mod+'.olean');start=time.monotonic()
  assert not re.search(r'\b(sorry|admit|axiom|native_decide|implemented_by)\b',source.read_text()),('forbidden proof token',mod)
  command=[str(lean),'--trust=0','-o',str(dest),str(source)]
  p=subprocess.run(command,cwd=source.parent,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=logs/(mod+'.log');log.write_text(p.stdout)
  assert p.returncode==0 and not any(x in p.stdout for x in ['error:','sorryAx']), (mod,p.stdout)
  digest=sha(dest);own[str(dest.resolve())]=digest
  if mod in original_objects:assert digest==original_objects[mod],('production object mismatch',mod)
  if mod in axiom_counts:
   closures=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",p.stdout)
   assert len(closures)==axiom_counts[mod],(mod,len(closures))
   for name,deps in closures:assert {x.strip() for x in deps.split(',') if x.strip()}<={'propext','Classical.choice','Quot.sound'},(name,deps)
   all_axioms[mod]=closures
  q=subprocess.run([str(lean),'--deps',str(source)],cwd=source.parent,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  assert q.returncode==0,(mod,q.stdout)
  resolved=[]
  for name in q.stdout.splitlines():
   path=Path(name).resolve();key=str(path);assert key in own or key in external,('unrecorded import',mod,key)
   digest=sha(path);assert digest==(own|external)[key]
   resolved.append({'path':key,'sha256':digest,'fresh_local':key in own})
  direct[mod]=resolved
  record['modules'].append({'module':mod,'command':command,'returncode':p.returncode,'source_sha256':sha(source),'object_sha256':sha(dest),'log_sha256':sha(log),'seconds':round(time.monotonic()-start,3),'production_hash_matches_author':mod in original_objects})
  print('PASS Lean',mod,flush=True);write(out/'REPLAY_RECEIPT.json',record)
 controls=sorted((src/'negative-controls').glob('*.lean'));assert len(controls)==5
 for source in controls:
  p=subprocess.run([str(lean),'--trust=0',str(source)],cwd=src,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=logs/source.with_suffix('.log').name;log.write_text(p.stdout)
  assert p.returncode!=0 and 'unsolved goals' in p.stdout and 'False' in p.stdout and not any(x in p.stdout for x in ['unknown module','does not exist','unknown identifier']),(source.name,p.stdout)
  record['negative_controls'].append({'name':source.stem,'returncode':p.returncode,'expected_logical_rejection':True,'source_sha256':sha(source),'log_sha256':sha(log)})
  print('PASS expected rejection',source.stem,flush=True)
 write(out/'DIRECT_IMPORTS.json',direct);write(out/'AXIOM_CLOSURES.json',all_axioms)
 symbolic=[('transport',R/'sources/polynomial-transport-continuation-20261010','check_exact.py','EXACT_RESULTS.json'),('rational_diagnostic',R/'inherited/heat-truncated-certificate-diagnostic-20261010','check_exact.py','EXACT_RESULTS.json'),('independent_math',review/'evidence','independent_math_checks.py','independent_math_checks.json'),('inherited_V',R/'inherited/time-varying-square-positivity-20261010','check_controls.py','CONTROL_RESULTS.json')]
 for name,source,script,result in symbolic:
  work=out/'symbolic'/name;work.mkdir(parents=True)
  shutil.copyfile(source/script,work/script)
  if name=='inherited_V':shutil.copyfile(source/'INPUT_BINDINGS.json',work/'INPUT_BINDINGS.json');shutil.copytree(source/'inputs',work/'inputs')
  p=subprocess.run([sys.executable,str(work/script)],cwd=work,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=logs/(name+'.log');log.write_text(p.stdout);assert p.returncode==0,(name,p.stdout)
  assert sha(work/result)==sha(source/result),('symbolic result bytes differ',name)
  got=read(work/result)
  if name=='transport':assert got['algebraic_checks']==36
  if name=='rational_diagnostic':assert got['concrete_witness_value']=='-3797/2500' and got['moment_basis_size']==35
  if name=='independent_math':assert got['degree_3_square_counterexample']=='-96'
  if name=='inherited_V':assert got['total_exact_checks']==23
  record['symbolic_checks'].append({'name':name,'returncode':p.returncode,'result_sha256':sha(work/result),'byte_identical_to_preserved_result':True,'log_sha256':sha(log)})
  print('PASS exact symbolic',name,flush=True)
 assert check_manifest()==packet_count
 record.update(status='PASS_SCOPED_FRESH_REPLAY',production_modules=7,independent_probe_modules=2,all_production_axiom_closures=72,additional_probe_axiom_closures=2,selected_author_axiom_closures=16,negative_controls_rejected=5,transport_symbolic_controls=36,standard_axioms_only=['propext','Classical.choice','Quot.sound'],degree_3_counterexample='Lambda((x^3-x)^2)=-96',formal_MeasureTheory_claim=False,formal_heat_claim=False,T20_closure=False)
 write(out/'REPLAY_RECEIPT.json',record)
 print(json.dumps({k:record[k] for k in ['status','production_modules','all_production_axiom_closures','negative_controls_rejected','transport_symbolic_controls','external_source_object_pairs_verified','external_dependencies_rebuilt']},indent=2))
except Exception as e:
 record.update(status='FAIL',error=repr(e));write(out/'REPLAY_RECEIPT.json',record);raise
