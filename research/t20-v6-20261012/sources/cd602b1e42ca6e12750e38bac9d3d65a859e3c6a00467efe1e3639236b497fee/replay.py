#!/usr/bin/env python3
"""Replay only the packaged heat controls. Fail closed on external prerequisites."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,v): p.write_text(json.dumps(v,indent=2)+'\n')
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--external-root',type=Path,help='Root containing exact omitted source artifacts at manifest-relative paths; no network retrieval is performed.')
 ap.add_argument('--output-dir',type=Path,required=True,help='Fresh directory outside the package for receipts and replay workspace.')
 args=ap.parse_args()
 out=args.output_dir.resolve(); out.mkdir(parents=True,exist_ok=False)
 if out==HERE or HERE in out.parents: raise SystemExit('Output directory must be outside preserved package.')
 receipt={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'STARTED','scope':'Fresh contained mathematical Python plus exact input and package integrity; ordinary proof evidence only.','python':sys.version,'external_root':str(args.external_root.resolve()) if args.external_root else None,'portable_source_verification':'Requires retrieval/provision of exact omitted sources and derivatives; this run does not retrieve or re-read primary literature.','algebraic_controls':{},'integrity_checks':{},'script_runs':[],'historical_count_policy':'Inherited G/V and predecessor control counts are historical and are not included in fresh totals. Two identical diagnostic copies are rerun for preservation and are not two independent mathematical datasets.','T20_closure':False,'Lean_verification':False}
 def record(): dump(out/'REPLAY_RECEIPT.json',receipt)
 try:
  manifest=json.loads((HERE/'MANIFEST.json').read_text())['files']
  for r in manifest:
   p=HERE/r['path']; assert p.is_file(),r['path']; assert p.stat().st_size==r['bytes'],r['path']; assert sha(p)==r['sha256'],r['path']
  receipt['integrity_checks']['archive_manifest_files']=len(manifest)
  copy_manifest=json.loads((HERE/'COPY_MANIFEST.json').read_text())['files']
  for r in copy_manifest:
   assert sha(HERE/r['archive_path'])==r['sha256'],r['path']
  receipt['integrity_checks']['byte_preserved_original_copies']=len(copy_manifest)
  external=json.loads((HERE/'EXTERNAL_PREREQUISITES.json').read_text())['sources']
  missing=[]
  for r in external:
   p=args.external_root/r['path'] if args.external_root else None
   if p is None or not p.is_file(): missing.append(r['path'])
   elif p.stat().st_size!=r['bytes'] or sha(p)!=r['sha256']: raise AssertionError('External source hash mismatch: '+r['path'])
  if missing:
   receipt['status']='BLOCKED_MISSING_EXTERNAL_PREREQUISITES';receipt['missing_external_artifacts']=missing;record()
   print('BLOCKED: exact external artifacts are required; no full replay is claimed.');return 2
  receipt['integrity_checks']['omitted_external_source_artifacts']=len(external)
  source_manifest=json.loads((HERE/'evidence/moment-evolution-source-comparison-20261010/SOURCE_MANIFEST.json').read_text())['sources']
  for r in source_manifest:
   source=args.external_root/'moment-evolution-source-comparison-20261010'/r['file']
   assert source.stat().st_size==r['bytes'] and sha(source)==r['sha256'],r['file']
  receipt['integrity_checks']['original_source_manifest_bindings']=len(source_manifest)
  receipt['external_source_verification']='PASS using explicitly provided retained/retrieved external artifacts; primary source retrieval is still a prerequisite for portability.'
  work=out/'work'; shutil.copytree(HERE/'evidence',work)
  # The historical script expects these external inputs as siblings. Copy only
  # the two necessary files into the new replay sandbox, never into the archive.
  required=[r for r in external if r['required_by_original_heat_control_script']]
  for r in required:
   dest=work/r['path']; dest.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(args.external_root/r['path'],dest)
  # Original review input bindings: classify rather than aggregate with algebra.
  review='heat-transport-obstruction-independent-review-20261010'
  bind=json.loads((work/review/'INPUT_BINDINGS.json').read_text())['inputs']
  assert len(bind)==11
  for r in bind: assert sha(work/r['path'])==r['sha256'],r['path']
  receipt['integrity_checks']['original_review_bound_inputs']=len(bind)
  primary='moment-evolution-source-comparison-20261010'
  cb=json.loads((work/primary/'INPUT_BINDINGS.json').read_text())['read_only_inputs']
  for r in cb: assert sha(work/r['path'])==r['sha256'],r['path']
  receipt['integrity_checks']['comparison_bound_inputs']=len(cb)
  diag='heat-truncated-certificate-diagnostic-20261010'
  clar=json.loads((work/diag/'FILTERED_LINEARITY_CLARIFICATION.json').read_text())
  assert sha(work/diag/'FILTERED_OPERATOR_NOTE.md')==clar['current_sha256']
  assert sha(work/diag/'FILTERED_OPERATOR_NOTE.before-explicit-linearity.md')==clar['prior_sha256']
  prior=(work/diag/'FILTERED_OPERATOR_NOTE.before-explicit-linearity.md').read_text()
  final=(work/diag/'FILTERED_OPERATOR_NOTE.md').read_text()
  assert final==prior.replace('**Claim.** If T=mI+N','**Claim.** Let T:V→V be linear. If T=mI+N',1)
  receipt['integrity_checks']['linearity_clarification_hash_and_exact_delta']=3
  rr=json.loads((work/review/'REVIEW_RECEIPT.json').read_text())
  for path,digest in rr['files'].items():
   p=work/review/path
   if not p.is_file(): p=args.external_root/review/path
   assert sha(p)==digest,path
  receipt['integrity_checks']['heat_review_receipt_file_bindings']=len(rr['files'])
  fr=json.loads((work/review/'FILTERED_OPERATOR_REVIEW_RECEIPT.json').read_text())
  assert sha(work/fr['source'])==fr['source_sha256']
  assert sha(work/review/fr['review'])==fr['review_sha256']
  assert sha(work/review/'REVIEW_RECEIPT.json')==fr['prior_review_receipt_sha256']
  assert clar['prior_sha256']==fr['prior_source_sha256']
  receipt['integrity_checks']['filtered_operator_receipt_bindings']=4
  ar=json.loads((work/diag/'AUTHOR_RECEIPT.json').read_text())
  assert ar['status']=='AUTHOR_EXACT_CONTROLS_PASS_INDEPENDENT_REVIEW_PENDING'
  for path,digest in ar['files'].items(): assert sha(work/diag/path)==digest,path
  for path,digest in ar['inputs'].items(): assert sha(work/path)==digest,path
  receipt['integrity_checks']['historical_pending_author_receipt_status_and_bindings']=1+len(ar['files'])+len(ar['inputs'])
  # References of omitted inherited historical campaigns remain visibly outside
  # this new replay scope; all included referenced artifacts are checked.
  h=json.loads((HERE/'HISTORICAL_RECEIPT_REFERENCES.json').read_text())['receipts']
  included=0; omitted=[]
  for rec in h:
   for r in rec['references']:
    if r['included']:
     assert sha(work/r['path'])==r['sha256']; included+=1
    else: omitted.append({'receipt':rec['receipt'],'path':r['path'],'sha256':r['sha256']})
  receipt['integrity_checks']['included_historical_receipt_references']=included
  receipt['omitted_historical_receipt_references_not_newly_replayed']=omitted
  tasks=[(review+'/check_controls.py',review+'/CONTROL_RESULTS.json'),(diag+'/check_exact.py',diag+'/EXACT_RESULTS.json'),(review+'/truncated-independent-replay/check_exact.py',review+'/truncated-independent-replay/EXACT_RESULTS.json')]
  # Assert the manifest contains no additional mathematical Python left unrun.
  actual=sorted(str(p.relative_to(work)) for p in work.rglob('*.py'))
  assert actual==sorted(t[0] for t in tasks),actual
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
  for i,(script,result) in enumerate(tasks,1):
   completed=subprocess.run([sys.executable,str(work/script)],cwd=work,env=env,text=True,capture_output=True)
   log=out/f'{i:02d}_{Path(script).stem}.log'; log.write_text(completed.stdout+completed.stderr)
   run={'script':script,'sha256':sha(work/script),'exit_code':completed.returncode,'log':log.name,'result':result,'result_sha256':sha(work/result),'frozen_result_sha256':sha(HERE/'evidence'/result)}
   receipt['script_runs'].append(run)
   assert completed.returncode==0,script
   assert run['result_sha256']==run['frozen_result_sha256'],'Result bytes differ: '+result
  controls=json.loads((work/review/'CONTROL_RESULTS.json').read_text())
  alg=[r for r in controls['results'] if not r['name'].startswith('Unchanged input ')]
  integ=[r for r in controls['results'] if r['name'].startswith('Unchanged input ')]
  assert len(alg)==52 and len(integ)==11 and all(r['pass'] for r in alg+integ)
  receipt['algebraic_controls']={'named_algebraic_or_finite_dimensional':52,'failed':0,'exact_truncated_diagnostic_distinct_scripts':1,'exact_truncated_diagnostic_executions':2,'diagnostic_monomial_basis_size':35,'diagnostic_square_Gram_dimension':10,'diagnostic_assertion_count':'Not aggregated; every assertion in both byte-identical scripts executed successfully.','filtered_operator_new_numeric_tests':0,'note':'Filtered-operator universal argument is accepted ordinary proof review, not a new numeric test.'}
  receipt['integrity_checks']['fresh_result_byte_matches']=3
  receipt['original_review_script_counts']={'algebraic':52,'bound_input_integrity':11,'combined_historical_script_output':63}
  receipt['status']='PASS_FRESH_REPLAY_WITH_EXPLICIT_EXTERNAL_PREREQUISITES'
  receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();record()
  print(json.dumps({'status':receipt['status'],'named_algebraic_controls':52,'original_bound_input_integrity':11,'diagnostic_executions':2,'fresh_result_byte_matches':3,'external_artifacts':len(external)},indent=2));return 0
 except BaseException as e:
  receipt['status']='FAIL';receipt['error']=str(e);record();raise
if __name__=='__main__': sys.exit(main())
