#!/usr/bin/env python3
"""Bounded exact replay from immutable evidence with explicit external source bytes."""
from pathlib import Path
import argparse,datetime,difflib,hashlib,json,os,platform,shutil,subprocess,sys,time
HERE=Path(__file__).resolve().parent
A='cumulative-square-positivity-20261010'; AR='cumulative-square-positivity-independent-review-20261010'
B='partial-quadratic-rank-classification-20261010'; BR='partial-quadratic-rank-independent-review-20261010'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def dump(p,j):p.write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(ok,message):
 if not ok:raise ValueError(message)
def check(p,row):
 require(p.is_file() and not p.is_symlink(),'Missing or symlink file: '+str(p))
 require('bytes' not in row or p.stat().st_size==row['bytes'],'Size mismatch: '+str(p))
 require(sha(p)==row['sha256'],'SHA-256 mismatch: '+str(p))
def main():
 if not __debug__:raise SystemExit('Do not disable Python assertions for preserved control programs.')
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--external-root',type=Path,help='Read-only directory containing the three exact source artifacts at EXTERNAL_PREREQUISITES.json paths. No automatic retrieval.')
 ap.add_argument('--output-dir',type=Path,required=True,help='New nonexistent directory outside this immutable packet.')
 args=ap.parse_args();out=args.output_dir.resolve()
 require(out!=HERE and HERE not in out.parents,'Output must be outside the immutable packet.')
 require(not out.exists(),'Refusing to reuse an existing output directory.')
 out.mkdir(parents=True)
 external=args.external_root.resolve() if args.external_root else None
 receipt={'schema':'directional-coverage-replay-v1','started_utc':now(),'status':'STARTED','python':sys.version,'external_root':str(external) if external else None,'script_runs':[],'integrity_checks':{},'scope':'Fresh execution of four finite current control programs plus one integrity verifier. No new independent proof review, classical source reading, or research-time credit.','T20_status':'ACTIVE','formal_kernel_verification':False,'dependency_rebuild':False,'integration':False,'closure':False}
 def save():dump(out/'REPLAY_RECEIPT.json',receipt)
 try:
  manifest=read(HERE/'MANIFEST.json')['files']
  require(not any(p.is_symlink() for p in HERE.rglob('*')),'Symlink in packet')
  actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file()}
  require(actual=={r['path'] for r in manifest}|{'MANIFEST.json'},'Unexpected or missing packet payload')
  for row in manifest:check(HERE/row['path'],row)
  receipt['packet_manifest_sha256']=sha(HERE/'MANIFEST.json')
  receipt['integrity_checks']['payload_files']=len(manifest)
  for r in read(HERE/'COPY_MANIFEST.json')['files']:check(HERE/r['archive_path'],r)
  receipt['integrity_checks']['unchanged_original_copies']=len(read(HERE/'COPY_MANIFEST.json')['files'])
  for rel,h in read(HERE/'ACCEPTANCE_BINDINGS.json')['anchors'].items():check(HERE/'evidence'/rel,{'sha256':h})
  ext=read(HERE/'EXTERNAL_PREREQUISITES.json')['sources'];aliases={alias:r for r in ext for alias in r['aliases']}
  missing=[]
  for row in ext:
   p=external/row['path'] if external else None
   if p is None or not p.is_file():missing.append(row['path'])
   else:check(p,row)
  if missing:
   receipt.update(status='BLOCKED_MISSING_EXTERNAL_PREREQUISITES',missing_external_artifacts=missing,finished_utc=now());save()
   print('BLOCKED: exact external source artifacts required; no control program executed.');return 2
  receipt['integrity_checks']['external_unique_source_artifacts']=len(ext)
  pins=read(HERE/'prerequisites/RUNTIME_PINS.json')
  require(platform.python_version()==pins['python_version'] and platform.python_implementation()==pins['python_implementation'],'Use pinned Python implementation/version.')
  try:import sympy,mpmath
  except ImportError as e:
   receipt.update(status='BLOCKED_MISSING_RUNTIME_PREREQUISITES',error=str(e),finished_utc=now());save();return 2
  require(sympy.__version__==pins['sympy_version'] and mpmath.__version__==pins['mpmath_version'],'Use pinned SymPy/mpmath versions.')
  for name,mod in [('sympy',sympy),('mpmath',mpmath)]:check(Path(mod.__file__),{'sha256':pins['entrypoint_hashes'][name]})
  receipt['runtime']={'python':platform.python_version(),'sympy':sympy.__version__,'mpmath':mpmath.__version__,'entrypoint_hashes_verified':True,'entire_distributions_byte_verified':False}
  def original(rel):
   p=HERE/'evidence'/rel
   if p.is_file():return p
   require(rel in aliases,'Undeclared missing canonical evidence: '+rel)
   return external/aliases[rel]['path']
  checked=0;omitted=[]
  for rec in read(HERE/'HISTORICAL_RECEIPT_REFERENCES.json')['receipts']:
   require(sha(HERE/rec['receipt'])==sha(HERE/rec['canonical_receipt']),'Copied receipt origin mismatch')
   for row in rec['references']:
    if row['disposition']=='historical_reference_not_bundled_or_replayed':omitted.append({'receipt':rec['receipt'],**row})
    else:check(original(row['path']),row);checked+=1
  receipt['integrity_checks']['historical_receipt_member_bindings']=checked
  receipt['historical_references_not_bundled_or_replayed']=omitted
  ca=read(original(A+'/AUTHOR_RECEIPT.json'));cr=read(original(AR+'/REVIEW_RECEIPT.json'))
  ra=read(original(B+'/AUTHOR_RECEIPT.json'));rr=read(original(BR+'/REVIEW_RECEIPT.json'))
  require(ca['total_exact_checks']==118 and ca['category_counts']=={'algebra':89,'input_integrity':14,'receipt_integrity':15},'Cumulative author scope')
  require(cr['status']=='PASS_EXACT_HYPOTHESES' and cr['independent_exact_controls']==55 and cr['unresolved_defects']==[],'Cumulative review scope')
  require(cr['final_candidate_sha256']==sha(original(A+'/RESULT.md')),'Cumulative accepted target')
  require(cr['initial_candidate_sha256']==sha(original(AR+'/inputs/candidate-RESULT.md')),'Cumulative draft binding')
  cb=read(original(AR+'/INPUT_BINDINGS.json'))
  require(cb['final_author_receipt_sha256']==sha(original(A+'/AUTHOR_RECEIPT.json')),'Cumulative final author receipt binding')
  for row in cb['inputs']:check(original(AR+'/'+row['copy']),row)
  before=original(AR+'/inputs/candidate-RESULT.md').read_text().splitlines(keepends=True)
  after=original(A+'/RESULT.md').read_text().splitlines(keepends=True)
  delta=''.join(difflib.unified_diff(before,after,fromfile='initial-candidate-468dac5c',tofile='final-candidate-a530a534'))
  require(delta==original(AR+'/FINAL_DELTA.patch').read_text(),'Cumulative exact draft-to-final delta')
  receipt['integrity_checks']['cumulative_draft_and_exact_correction_patch']=True
  require(ra['controls']['total_exact_checks']==1232 and rr['status']=='PASS_NO_BLOCKING_FINDINGS' and rr['independent_exact_checks']==1605,'Rank acceptance scope')
  require(rr['author_result_sha256']==sha(original(B+'/RESULT.md')) and rr['author_receipt_sha256']==sha(original(B+'/AUTHOR_RECEIPT.json')) and rr['review_report_sha256']==sha(original(BR+'/REVIEW.md')),'Rank accepted target or receipt binding')
  inputs=0
  for folder in [A,B]:
   for row in read(original(folder+'/INPUT_BINDINGS.json')):
    check(original(folder+'/'+row['copy']),row);check(original(row['source']),row);inputs+=2
  for row in read(original(BR+'/AUTHOR_SNAPSHOT_BINDINGS.json')):
   check(original(row['author']),row);check(original(BR+'/'+row['snapshot']),row);inputs+=2
  for row in read(original(BR+'/HISTORICAL_EXCLUSION_BINDINGS.json')):check(original(BR+'/'+row['copy']),row);inputs+=1
  for row in read(original(B+'/SOURCE_MANIFEST.json'))['local_files']:check(original(B+'/'+row['file']),row);inputs+=1
  receipt['integrity_checks']['current_input_snapshot_and_exclusion_bindings']=inputs
  work=out/'work';shutil.copytree(HERE/'evidence',work)
  for row in ext:
   for alias in row['aliases']:
    dest=work/alias;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(external/row['path'],dest)
  receipt['external_copies_only_in_disposable_replay_workspace']=sum(len(r['aliases']) for r in ext)
  execution=read(HERE/'EXECUTION_SCOPE.json')['scripts']
  require(sorted(str(p.relative_to(work)) for p in work.rglob('*.py'))==sorted(r['path'] for r in execution),'Execution-scope enumeration differs')
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0');env.pop('PYTHONOPTIMIZE',None)
  logs=out/'logs';logs.mkdir()
  for row in execution:
   if row['execution']!='run':continue
   script=row['path'];check(work/script,row);start=time.monotonic()
   command=[sys.executable,'-I','-B',str(work/script)]
   p=subprocess.run(command,cwd=work,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
   log=logs/(script.replace('/','__')+'.log');log.write_text(p.stdout)
   entry={'script':script,'script_sha256':sha(work/script),'exit_code':p.returncode,'log':str(log.relative_to(out)),'log_sha256':sha(log),'seconds':round(time.monotonic()-start,3),'kind':row['kind']};receipt['script_runs'].append(entry);save()
   require(p.returncode==0,'Control program failed: '+script)
   if row['result']:
    result=work/row['result'];require(sha(result)==sha(original(row['result'])),'Fresh result is not byte-identical: '+row['result'])
    obj=read(result);count=obj.get('total_exact_checks',obj.get('count',obj.get('exact_checks')))
    require(count==row['expected_check_count'],'Wrong exact check count: '+script)
    entry.update(result=row['result'],result_sha256=sha(result),byte_identical=True,count=count)
   else:
    obj=json.loads(p.stdout);require(obj['status']=='PASS' and obj['unchanged_live_author_files']==14,'Rank receipt verifier did not cover all current author files');entry['integrity_result']=obj
   print('PASS',script,flush=True)
  receipt['controls']={'cumulative_author':{'historical_total':118,'algebra':89,'integrity':29},'cumulative_independent':{'historical_total':55,'algebra':54,'integrity':1},'rank_author':{'historical_total':1232,'algebra':1223,'integrity':9},'rank_independent':{'historical_total':1605,'algebra':1591,'integrity':14,'gaussian_recursion_cases':1309}}
  # Confirm category distinctions against the regenerated records, not just prose counts.
  require(read(work/A/'CONTROL_RESULTS.json')['category_counts']==ca['category_counts'],'Cumulative categories changed')
  rank=read(work/B/'CONTROL_RESULTS.json');require(rank['categories']['input_sha256']+rank['categories']['primary_source_sha256']==9,'Rank integrity category count')
  independ=read(work/BR/'INDEPENDENT_RESULTS.json');require(sum(x.startswith('snapshot-integrity-') for x in independ['checks'])==14 and independ['gaussian_recursion_cases']==1309,'Rank independent integrity/recursion count')
  for row in manifest:check(HERE/row['path'],row)
  for row in ext:check(external/row['path'],row)
  receipt.update(status='PASS_FRESH_EXTRACTION_REPLAY_WITH_EXPLICIT_PREREQUISITES',byte_identical_regenerated_results=4,preserved_payload_and_external_inputs_unchanged=True,finished_utc=now());save()
  print(json.dumps({'status':receipt['status'],'controls':receipt['controls'],'byte_identical_results':4,'external_unique_artifacts':3},indent=2));return 0
 except BaseException as e:
  receipt.update(status='FAIL',error=str(e),finished_utc=now());save();raise
if __name__=='__main__':sys.exit(main())
