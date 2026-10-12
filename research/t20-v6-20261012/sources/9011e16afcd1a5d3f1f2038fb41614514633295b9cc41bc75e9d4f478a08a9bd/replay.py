#!/usr/bin/env python3
"""Fresh, relocation-safe replay; retained dependencies are read-only, never rebuilt."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,platform,re,shutil,subprocess,sys,time
R=Path(__file__).resolve().parent
A='full-polynomial-moment-countermodel-20261010'; AR='full-polynomial-moment-independent-review-20261010'; L='full-functional-lean-20261010'; LR='full-functional-lean-independent-review-20261010'
MODULES=['ScalarSupport','Indexing','Schur','Recurrence','Moment','PolynomialBridge','Countermodel']
ALLOWED={'propext','Classical.choice','Quot.sound'}
def require(ok,msg):
 if not ok:raise ValueError(msg)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def dump(p,j):p.write_text(json.dumps(j,indent=2)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def check(p,row):
 require(p.is_file() and not p.is_symlink(),'Missing or symlink file: '+str(p))
 require(p.stat().st_size==row.get('bytes',p.stat().st_size),'Size mismatch: '+str(p))
 require(sha(p)==row['sha256'],'SHA-256 mismatch: '+str(p))
def main():
 if not __debug__:raise SystemExit('Do not disable Python assertions for preserved programs.')
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--lean-home',type=Path,help='Exact retained Lean 4.19.0 distribution root')
 ap.add_argument('--packages-dir',type=Path,help='Exact retained Mathlib and peer package roots')
 ap.add_argument('--output-dir',type=Path,required=True,help='New directory outside this packet and external prerequisites')
 a=ap.parse_args();out=a.output_dir.resolve()
 require(out!=R and R not in out.parents,'Output must be outside the immutable packet.')
 require(not out.exists(),'Refusing to reuse an existing output directory.')
 roots={'lean_home':a.lean_home.resolve() if a.lean_home else None,'packages':a.packages_dir.resolve() if a.packages_dir else None}
 for root in roots.values():
  if root:require(out!=root and root not in out.parents and out not in root.parents,'Output must be separate from external prerequisites.')
 out.mkdir(parents=True)
 receipt={'status':'STARTED','started_utc':now(),'runs':[],'scope':'Fresh local proof compilation and finite exact controls from preserved sources. No fresh independent mathematical review, dependency rebuild, or research-time credit.','T20_status':'ACTIVE','closure':False,'integration':False,'dependency_rebuild':False}
 def save():dump(out/'REPLAY_RECEIPT.json',receipt)
 try:
  m=read(R/'MANIFEST.json')['files']
  require(not any(p.is_symlink() for p in R.rglob('*')),'Symlink in immutable packet')
  require({str(p.relative_to(R)) for p in R.rglob('*') if p.is_file()}=={x['path'] for x in m}|{'MANIFEST.json'},'Unexpected or missing packet payload')
  for row in m:
   require(not Path(row['path']).is_absolute() and '..' not in Path(row['path']).parts,'Unsafe manifest path')
   check(R/row['path'],row)
  receipt['packet_manifest_sha256']=sha(R/'MANIFEST.json');receipt['packet_files_verified']=len(m)
  for row in read(R/'COPY_MANIFEST.json')['files']:check(R/row['archive_path'],row)
  anchors=read(R/'ACCEPTANCE_BINDINGS.json')
  for p,h in anchors['anchors'].items():check(R/'evidence'/p,{'sha256':h})
  require(anchors['independent_lean_verdict']=='PASS_INDEPENDENT_FULL_FUNCTIONAL_LEAN_REVIEW','Unexpected accepted Lean verdict')
  require(read(R/'evidence'/LR/'FROZEN_REVIEW_MANIFEST.json')['status']=='PASS_INDEPENDENT_FULL_FUNCTIONAL_LEAN_REVIEW','Independent Lean freeze is not PASS')
  require(read(R/'evidence'/AR/'REVIEW_MANIFEST.json')['verdict']=='PASS_UNIVERSAL_MATHEMATICAL_CONSTRUCTION_WITH_BOUNDED_REPLAYS','Ordinary review verdict differs')
  require(read(R/'evidence'/L/'LEAN_RECEIPT.json')['status']=='PASS_FULL_POLYNOMIAL_COUNTERMODEL_LEAN','Author Lean status differs')
  E=R/'evidence'
  # Check each historical object against the receipt for that exact path. A
  # different build's matching source is not a substitute for object identity.
  identities=read(R/'HISTORICAL_OBJECT_NOTE.json')
  require(identities['status']=='PASS_SEPARATE_OBJECT_RECEIPT_BINDINGS' and identities['historical_receipt_object_mismatch'] is False,'Contradictory scalar identity summary')
  require(len(identities['bindings'])==3,'Expected three separate scalar receipt bindings')
  for row in identities['bindings']:
   value=read(E/row['receipt_path'])
   for key in row['receipt_selector']:value=value[key]
   require(value==row['expected_sha256']==row['actual_sha256'] and row['match'] is True,'Scalar object/receipt binding differs: '+row['object_path'])
   check(E/row['object_path'],{'bytes':row['bytes'],'sha256':value})
  check(E/AR/'frozen-target/lean-support/ScalarSupport.olean',{'sha256':identities['ordinary_review_frozen_object_sha256']})
  require(identities['ordinary_review_frozen_object_sha256']==identities['bindings'][0]['actual_sha256'],'Ordinary frozen object differs')
  receipt['scalar_object_receipt_bindings_verified']=3
  receipt['historical_scalar_receipt_object_mismatch']=False
  receipt['provenance_correction_sha256']=sha(R/'PROVENANCE_CORRECTION.json')
  # Verify each historical freeze as originally written. All referenced local objects
  # are preserved but must never enter this fresh replay's Lean import search path.
  for directory,filename in [(A,'FROZEN_MANIFEST.json'),(AR,'REVIEW_MANIFEST.json'),(L,'FROZEN_MANIFEST.json'),(LR,'FROZEN_REVIEW_MANIFEST.json')]:
   data=read(E/directory/filename); rows=data['files']
   if isinstance(rows,dict):rows=[{'path':k,'sha256':v} for k,v in rows.items()]
   for row in rows:check(E/directory/row['path'],row)
  for mod in MODULES:
   name=mod+'.lean';digest=read(E/L/'SOURCE_FREEZE.json')['sources'][name]
   check(E/L/name,{'sha256':digest});check(E/LR/'frozen-target'/name,{'sha256':digest})
  require(sha(E/L/'ScalarSupport.lean')==sha(E/A/'lean-support/ScalarSupport.lean'),'Historical scalar source differs')
  if any(x is None or not x.is_dir() for x in roots.values()):
   receipt.update(status='BLOCKED_MISSING_EXTERNAL_PREREQUISITES',finished_utc=now());save();print('BLOCKED: provide exact retained Lean and package directories. No proof or control executed.');return 2
  pins=read(R/'prerequisites/RUNTIME_PINS.json')
  require(platform.python_version()==pins['python_version'] and platform.python_implementation()==pins['python_implementation'],'Pinned Python runtime differs')
  def resolve(spec):
   require(spec['root'] in roots and not Path(spec['path']).is_absolute() and '..' not in Path(spec['path']).parts,'Unsafe prerequisite path')
   return roots[spec['root']]/spec['path']
  external=read(R/'prerequisites/EXTERNAL_DEPENDENCIES.json')
  missing=[str(resolve(x)) for x in pins['binaries'] if not resolve(x).is_file()]
  missing += [str(resolve(row[k])) for row in external['entries'] for k in ['source','object'] if not resolve(row[k]).is_file()]
  if missing:
   receipt.update(status='BLOCKED_MISSING_EXTERNAL_PREREQUISITES',missing=missing,finished_utc=now());save();print('BLOCKED: exact external prerequisite bytes are missing. No proof or control executed.');return 2
  for x in pins['binaries']:check(resolve(x),x)
  objects={};by_module={}
  for row in external['entries']:
   for k in ['source','object']:check(resolve(row[k]),row[k])
   p=resolve(row['object']).resolve();objects[str(p)]=row['object']['sha256'];by_module[row['module']]=row
  receipt['external_source_object_pairs_verified']=len(external['entries'])
  lean=roots['lean_home']/'bin/lean'
  clean=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
  for name in ['LEAN_PATH','LEAN_SYSROOT','LEAN_SRC_PATH','LD_LIBRARY_PATH','LD_PRELOAD','PYTHONOPTIMIZE','PYTHONPATH']:clean.pop(name,None)
  ver=subprocess.check_output([str(lean),'--version'],text=True,env=clean).strip()
  require(ver==pins['lean_version'],'Lean version differs');receipt['lean_version']=ver
  work=out/'work';lib=work/'lean';lib.mkdir(parents=True);logs=out/'logs';logs.mkdir()
  used_packages={row['object']['path'].split('/')[0] for row in external['entries'] if row['object']['root']=='packages'}
  search=[lib]+[roots['packages']/p/'.lake/build/lib/lean' for p in pins['package_search_order'] if p in used_packages]
  require(all(p.is_dir() for p in search),'Missing retained import search directory')
  env=dict(clean,LEAN_PATH=':'.join(map(str,search)))
  receipt['lean_path']=list(map(str,search));receipt['no_historical_local_objects_imported']=True
  save();fresh={};direct={};axioms={}
  def run(name,cmd,cwd,success=True):
   start=time.monotonic();p=subprocess.run(cmd,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
   log=logs/(name+'.log');log.write_text(p.stdout)
   row={'name':name,'command':cmd,'exit_status':p.returncode,'log':str(log.relative_to(out)),'log_sha256':sha(log),'seconds':round(time.monotonic()-start,3),'expected_success':success}
   receipt['runs'].append(row);save()
   require((p.returncode==0)==success,'Unexpected exit status: '+name+'\n'+p.stdout)
   if success:require('error:' not in p.stdout and 'warning:' not in p.stdout,'Diagnostic in successful run: '+name)
   else:
    require('error:' in p.stdout and any(x in p.stdout for x in ['unsolved goals','type mismatch','tactic','failed to find a contradiction']),'Not a mathematical rejection: '+name)
    require(not any(x in p.stdout for x in ['does not exist','unknown module','unknown identifier','unexpected token']),'Infrastructure failure is not a mathematical rejection: '+name)
   print(('PASS ' if success else 'EXPECTED_REJECTION ')+name,flush=True)
   return p.stdout
  def imports_for(source,name):
   p=subprocess.run([str(lean),'--deps',str(source)],cwd=lib,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
   require(p.returncode==0,'Cannot resolve direct imports: '+name);rows=[]
   for val in p.stdout.splitlines():
    q=Path(val).resolve();key=str(q)
    require(key in objects or key in fresh,'Unbound or historical import: '+key)
    h=sha(q);require(h==(objects|fresh)[key],'Import bytes changed: '+key)
    rows.append({'path':key,'sha256':h,'fresh_local':key in fresh})
   direct[name]=rows
  def compile_source(source,name,expected_axioms=None):
   dest=lib/(name+'.lean');shutil.copyfile(source,dest)
   require(not re.search(r'\b(sorry|admit|axiom|native_decide|implemented_by|unsafe)\b',dest.read_text()),'Forbidden production proof token: '+name)
   imports_for(dest,name)
   output=run(name,[str(lean),'--trust=0','-o',str(lib/(name+'.olean')),str(dest)],lib)
   closures=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",output)
   if expected_axioms is not None:require(len(closures)==expected_axioms,'Axiom audit count differs: '+name)
   for thm,dep in closures:require({x.strip() for x in dep.split(',') if x.strip()}<=ALLOWED,'Unexpected axiom: '+thm)
   axioms[name]=closures;fresh[str((lib/(name+'.olean')).resolve())]=sha(lib/(name+'.olean'))
   return output
  for mod in MODULES:compile_source(E/L/(mod+'.lean'),mod)
  require(sum(map(len,axioms.values()))==22,'Expected 22 author axiom audits')
  require(any(n=='FullPolynomialCountermodel.full_polynomial_countermodel' for n,d in axioms['Countermodel']),'Missing final theorem audit')
  positive=compile_source(E/LR/'controls/PositiveChecks.lean','PositiveChecks',4)
  imports=re.findall(r'^REVIEW_IMPORT (.+)$',positive,re.M)
  require(len(imports)==len(set(imports)),'Duplicate actual imported module')
  expected={x['module'] for x in read(E/LR/'IMPORT_CLOSURE.json')}
  require(set(imports)==expected,'Actual imported environment differs from independent freeze')
  require(set(imports)<=set(by_module)|set(MODULES),'Unbound transitive imported module')
  receipt['actual_import_modules_verified']=len(imports)
  # The old support source is the exact ScalarSupport already rebuilt above.
  compile_source(E/A/'lean-support/RetainedMatrixProbe.lean','RetainedMatrixProbe',0)
  controls=[('author-'+p.stem,p) for p in sorted((E/L/'negative-controls').glob('*.lean'))]
  controls += [('independent-'+p.stem,p) for p in sorted((E/LR/'controls').glob('False*.lean'))]
  controls += [('historical-'+n,E/A/'lean-support'/(n+'.lean')) for n in ['wrong_origin_value','wrong_seed_value']]
  require(len(controls)==12,'Expected 3 author, 7 independent, and 2 historical false controls')
  for name,src in controls:
   dest=work/'negative-controls'/name/(src.name);dest.parent.mkdir(parents=True);shutil.copyfile(src,dest)
   imports_for(dest,name);run(name,[str(lean),'--trust=0',str(dest)],lib,False)
  # Exact arithmetic programs are unchanged and run only in disposable output.
  ordinary=work/A;ordinary.mkdir()
  for name in ['check_exact.py','countermodel.py','PROOF.md']:shutil.copyfile(E/A/name,ordinary/name)
  run('ordinary-author-exact',[sys.executable,'-B',str(ordinary/'check_exact.py')],ordinary)
  exact=read(ordinary/'EXACT_CHECK_RECEIPT.json');require(exact['checks_passed']==37588,'Author finite count differs')
  require(sha(ordinary/'PREFIX_25.json')==sha(E/A/'PREFIX_25.json'),'Exact prefix bytes differ')
  for k in ['status','universal_claim_basis','checks_passed','prefix_length','independent_recurrence','positivity_verification','bounded_midpoint_pairs_checked','exceptional_pairs','Lambda_F','negative_controls','source_sha256','prefix_sha256']:
   require(exact[k]==read(E/A/'EXACT_CHECK_RECEIPT.json')[k],'Author finite receipt differs except timing: '+k)
  review=work/AR;review.mkdir();shutil.copyfile(E/AR/'check_independent.py',review/'check_independent.py')
  run('ordinary-independent-exact',[sys.executable,'-B',str(review/'check_independent.py'),'--target',str(ordinary)],review)
  independent=read(review/'INDEPENDENT_RECEIPT.json');historical=read(E/AR/'INDEPENDENT_RECEIPT.json')
  require(independent['checks']==44637,'Independent finite count differs')
  require({k:v for k,v in independent.items() if k!='elapsed_seconds'}=={k:v for k,v in historical.items() if k!='elapsed_seconds'},'Independent finite receipt differs except timing')
  dump(out/'DIRECT_IMPORTS.json',direct);dump(out/'AXIOM_AUDITS.json',axioms)
  for row in m:check(R/row['path'],row)
  for x in pins['binaries']:check(resolve(x),x)
  for row in external['entries']:
   for k in ['source','object']:check(resolve(row[k]),row[k])
  receipt.update(status='PASS_FRESH_FULL_FUNCTIONAL_REPLAY',finished_utc=now(),trust=0,production_modules=7,independent_positive_modules=1,historical_availability_probes=1,author_axiom_audits=22,independent_axiom_audits=4,mathematical_negative_controls={'author':3,'independent':7,'historical_scalar':2},finite_exact_checks={'author':37588,'independent':44637},finite_checks_are_universal_proof=False,packet_and_external_inputs_unchanged=True,formal_measure_integral_corollary=False,formal_dyadic_executable_correspondence=False,formal_determinant_invariant=False,formal_explicit_inverse_algorithm=False)
  save();print(json.dumps({k:receipt[k] for k in ['status','production_modules','external_source_object_pairs_verified','actual_import_modules_verified','mathematical_negative_controls','finite_exact_checks']},indent=2));return 0
 except BaseException as exc:
  receipt.update(status='FAIL',error=str(exc),finished_utc=now());save();raise
if __name__=='__main__':sys.exit(main())
