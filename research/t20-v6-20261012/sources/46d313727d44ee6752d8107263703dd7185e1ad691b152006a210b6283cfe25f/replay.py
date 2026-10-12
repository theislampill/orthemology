#!/usr/bin/env python3
"""Replay preserved Theorem D controls with explicit, fail-closed source prerequisites."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
AUTHOR='diffusive-coercive-realizability-20261010'
REVIEW='diffusive-moment-existence-independent-review-20261010'
FOLLOWUP='diffusive-moment-source-followup-20261010'
COMPARISON='moment-evolution-source-comparison-20261010'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,o):p.write_text(json.dumps(o,indent=2)+'\n')
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def main():
 if not __debug__:raise SystemExit('Do not disable Python assertions for integrity replay.')
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--external-root',type=Path,help='Explicit root containing exact omitted artifacts at their manifest-relative paths; accessed read-only, with no retrieval.')
 ap.add_argument('--output-dir',type=Path,required=True,help='Must be new and outside the preserved package.')
 args=ap.parse_args();out=args.output_dir.resolve()
 if out==HERE or HERE in out.parents:raise SystemExit('Output must be outside preserved package.')
 out.mkdir(parents=True,exist_ok=False)
 external_root=args.external_root.resolve() if args.external_root else None
 receipt={'schema':'diffusive-existence-preservation-replay-v1','started_utc':now(),'status':'STARTED','python':sys.version,'external_root':str(external_root) if external_root else None,'scope':'Fresh execution of the immutable successful author and independent algebra programs plus separately enumerated integrity verification. Not a new proof review or source reading.','integrity_checks':{},'script_runs':[],'author_controls':None,'independent_controls':None,'baseline_rebuild':False,'formal_kernel_verification':False,'T20_closure':False,'active_cumulative_investigation_included':False}
 def record():dump(out/'REPLAY_RECEIPT.json',receipt)
 def check_file(p,row):
  assert p.is_file(),'Missing: '+str(p)
  assert not p.is_symlink(),'Unexpected symlink: '+str(p)
  if 'bytes' in row:assert p.stat().st_size==row['bytes'],'Size mismatch: '+str(p)
  assert sha(p)==row['sha256'],'SHA-256 mismatch: '+str(p)
 try:
  manifest=json.loads((HERE/'MANIFEST.json').read_text())['files']
  actual={str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file()}
  assert actual=={r['path'] for r in manifest}|{'MANIFEST.json'},'Unexpected or missing package payload'
  for r in manifest:check_file(HERE/r['path'],r)
  receipt['integrity_checks']['archive_manifest_files']=len(manifest)
  copies=json.loads((HERE/'COPY_MANIFEST.json').read_text())['files']
  for r in copies:check_file(HERE/r['archive_path'],r)
  receipt['integrity_checks']['unchanged_canonical_original_copies']=len(copies)
  acceptance=json.loads((HERE/'ACCEPTANCE_BINDINGS.json').read_text())
  for p,h in acceptance['anchors'].items():assert sha(HERE/'evidence'/p)==h,p
  receipt['integrity_checks']['frozen_acceptance_anchors']=len(acceptance['anchors'])
  ext=json.loads((HERE/'EXTERNAL_PREREQUISITES.json').read_text())['sources'];missing=[]
  for r in ext:
   p=external_root/r['path'] if external_root else None
   if p is None or not p.is_file():missing.append(r['path'])
   else:check_file(p,r)
  if missing:
   receipt.update(status='BLOCKED_MISSING_EXTERNAL_PREREQUISITES',missing_external_artifacts=missing,finished_utc=now())
   record();print('BLOCKED: exact external artifacts required; no mathematical replay performed.');return 2
  receipt['integrity_checks']['explicit_external_artifacts']=len(ext)
  receipt['external_verification_boundary']='Exact bytes checked against explicitly provided retained or retrieved files; no new source retrieval, source reading, or blanket source certification.'
  external_paths={r['path'] for r in ext}
  def original(path):
   p=HERE/'evidence'/path
   if p.is_file():return p
   assert path in external_paths,'No declared canonical input: '+path
   return external_root/path
  ar=json.loads(original(AUTHOR+'/AUTHOR_RECEIPT.json').read_text())
  assert ar['status']=='author_complete_pending_independent_review'
  for r in ar['files']:check_file(original(AUTHOR+'/'+r['path']),r)
  receipt['integrity_checks']['author_receipt_file_bindings']=len(ar['files'])
  receipt['historical_author_status_preserved']=ar['status']
  aliases=json.loads((HERE/'REVIEW_REPLAY_ALIASES.json').read_text())['entries']
  old_manifest=json.loads(original(REVIEW+'/MANIFEST.json').read_text())
  assert len(aliases)==len(old_manifest)
  for r,a in zip(old_manifest,aliases):
   assert a['historical_path']==REVIEW+'/'+r['path'] and a['sha256']==r['sha256'] and a['bytes']==r['bytes']
   check_file(original(a['canonical_path']),r)
  receipt['integrity_checks']['original_independent_manifest_bindings_via_canonical_copies']=len(aliases)
  review=json.loads(original(REVIEW+'/REVIEW_RECEIPT.json').read_text())
  assert review['verdict']=='accepted_within_stated_scope'
  assert review['author_result_sha256']==sha(original(AUTHOR+'/RESULT.md'))
  assert review['author_receipt_sha256']==sha(original(AUTHOR+'/AUTHOR_RECEIPT.json'))
  assert review['review_sha256']==sha(original(REVIEW+'/REVIEW.md'))
  assert review['author_fresh_replay']['original_control_results_sha256']==sha(original(AUTHOR+'/CONTROL_RESULTS.json'))
  assert review['independent_fresh_controls']['script_sha256']==sha(original(REVIEW+'/independent_controls.py'))
  assert review['independent_fresh_controls']['results_sha256']==sha(original(REVIEW+'/INDEPENDENT_RESULTS.json'))
  for r in review['inherited_originals_verified_before_and_after']:check_file(original(r['path']),r)
  receipt['integrity_checks']['accepted_review_explicit_binding_and_verdict_checks']=7+len(review['inherited_originals_verified_before_and_after'])
  fm=json.loads(original(FOLLOWUP+'/MANIFEST.json').read_text())
  for r in fm['new_files']:check_file(original(FOLLOWUP+'/'+r['path']),r)
  check_file(original(fm['completed_report_preserved']['path']),fm['completed_report_preserved'])
  receipt['integrity_checks']['bounded_followup_original_manifest_bindings']=len(fm['new_files'])+1
  for folder in (AUTHOR,COMPARISON):
   m=json.loads(original(folder+'/SOURCE_MANIFEST.json').read_text())
   rows=m if isinstance(m,list) else m['sources']
   for r in rows:check_file(original(folder+'/'+r.get('local_file',r.get('file'))),r)
   receipt['integrity_checks'][folder+'_source_manifest_bindings']=len(rows)
  cb=json.loads(original(COMPARISON+'/INPUT_BINDINGS.json').read_text())['read_only_inputs']
  for r in cb:check_file(original(r['path']),r)
  receipt['integrity_checks']['inherited_comparison_input_bindings']=len(cb)
  hist=json.loads((HERE/'HISTORICAL_RECEIPT_REFERENCES.json').read_text())['receipts']
  checked=0;omitted=[]
  for rec in hist:
   for r in rec['references']:
    if r['disposition']=='historical_inherited_campaign_not_replayed':omitted.append({'receipt':rec['receipt'],**r})
    else:check_file(original(r['path']),r);checked+=1
  receipt['integrity_checks']['included_or_external_historical_receipt_references']=checked
  receipt['omitted_inherited_campaign_references_not_replayed']=omitted
  work=out/'work';shutil.copytree(HERE/'evidence',work)
  for r in ext:
   if r['consumed_by_author_control_script']:
    dest=work/r['path'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(external_root/r['path'],dest)
  receipt['external_artifacts_copied_only_to_disposable_replay_sandbox']=sum(r['consumed_by_author_control_script'] for r in ext)
  execution=json.loads((HERE/'EXECUTION_SCOPE.json').read_text())
  actual_scripts=sorted(str(p.relative_to(work)) for p in work.rglob('*.py'))
  assert actual_scripts==sorted(r['path'] for r in execution['scripts']),actual_scripts
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0')
  for item in execution['scripts']:
   if item['execution']!='run':continue
   script=item['path'];result=item['result']
   completed=subprocess.run([sys.executable,str(work/script)],cwd=work,env=env,text=True,capture_output=True)
   log=out/(Path(script).stem+'.log');log.write_text(completed.stdout+completed.stderr)
   row={'script':script,'script_sha256':sha(work/script),'exit_code':completed.returncode,'log':log.name,'log_sha256':sha(log),'result':result}
   receipt['script_runs'].append(row)
   assert completed.returncode==0,'Failed script: '+script
   row.update(result_sha256=sha(work/result),frozen_result_sha256=sha(original(result)))
   assert row['result_sha256']==row['frozen_result_sha256'],'Result bytes differ from historical frozen run: '+result
  receipt['historical_scripts_deliberately_not_executed']=[r for r in execution['scripts'] if r['execution']!='run']
  author=json.loads((work/AUTHOR/'CONTROL_RESULTS.json').read_text())
  assert author['status']=='passed'
  checks=author['checks'];integrity=[x for x in checks if x.startswith(('snapshot hash ','unchanged inherited ','source hash '))];algebra=[x for x in checks if x not in integrity]
  assert author['exact_checks']==len(checks)==685 and len(algebra)==675 and len(integrity)==10
  receipt['author_controls']={'algebraic':675,'integrity':10,'historical_script_total':685,'integrity_labels':integrity,'result_sha256':sha(work/AUTHOR/'CONTROL_RESULTS.json')}
  independent=json.loads((work/REVIEW/'INDEPENDENT_RESULTS.json').read_text())
  assert independent['status']=='pass' and independent['exact_checks']==len(independent['checks'])==133
  assert all(r['status']=='pass' for r in independent['checks'])
  receipt['independent_controls']={'algebraic':133,'result_sha256':sha(work/REVIEW/'INDEPENDENT_RESULTS.json'),'boundary':'Separately authored independent finite algebra controls; not disjoint mathematical claims or a universal analytic proof.'}
  # All archive payload bytes and every read-only external prerequisite remain unchanged.
  for r in manifest:check_file(HERE/r['path'],r)
  for r in ext:check_file(external_root/r['path'],r)
  receipt['integrity_checks']['archive_files_rechecked_after_replay']=len(manifest)
  receipt['integrity_checks']['external_files_rechecked_after_replay']=len(ext)
  receipt.update(status='PASS_FRESH_EXTRACTION_REPLAY_WITH_EXPLICIT_EXTERNAL_PREREQUISITES',finished_utc=now())
  record();print(json.dumps({'status':receipt['status'],'author_algebra':675,'author_integrity':10,'independent_algebra':133,'external_artifacts':len(ext),'byte_identical_regenerated_results':len(receipt['script_runs'])},indent=2));return 0
 except BaseException as e:
  receipt.update(status='FAIL',error=str(e),finished_utc=now());record();raise
if __name__=='__main__':sys.exit(main())
