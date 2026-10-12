#!/usr/bin/env python3
import argparse,hashlib,json,os,platform,subprocess,sys
from pathlib import Path
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--prerequisite-root');ap.add_argument('--compile',action='store_true');args=ap.parse_args();out=Path(args.output).resolve();assert not out.exists(),'Fresh output required'
 root=Path(__file__).resolve().parent;manifest=json.loads((root/'MANIFEST.json').read_text());actual=lambda:{str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file() and p!=root/'MANIFEST.json'};assert actual()==manifest['files']
 ev=root/'evidence';a=ev/'hase-joint-proof-uniqueness-20261010';r=ev/'hase-joint-proof-uniqueness-independent-review-20261010';receipt=json.loads((r/'REVIEW_RECEIPT.json').read_text());assert sha(a/'SOURCE_BOUNDARY.json')==receipt['candidate_manifest_sha256'];assert sha(a/'RESULT.md')==receipt['candidate_report_sha256']
 for row in receipt['review_files']:assert sha(r/row['path'])==row['sha256'],row['path']
 sources=json.loads((r/'SOURCE_INPUTS.json').read_text());standard=json.loads((r/'STANDARD_OBJECT_PREREQUISITES.json').read_text());runtime=json.loads((root/'prerequisites/RUNTIME_PINS.json').read_text());assert len(sources)==173 and len(standard)==2663
 for row in sources:assert sha(r/'sources'/Path(*row['module'].split('.')).with_suffix('.lean'))==row['sha256'],row['module']
 boundary=json.loads((a/'SOURCE_BOUNDARY.json').read_text())
 for row in boundary['additive']:assert sha(ev/row['path'])==row['sha256'],row['path']
 out.mkdir(parents=True)
 result={'status':'INTEGRITY_PASS_PREREQUISITES_REQUIRED','verification_tier':'INCLUDED_SOURCE_AND_RECEIPT_INTEGRITY_ONLY','python':platform.python_version(),'manifest_sha256':sha(root/'MANIFEST.json'),'included_source_files_verified':173,'source_closure_sha256':sha(r/'SOURCE_INPUTS.json'),'required_standard_object_count':2663,'required_standard_object_manifest_sha256':sha(r/'STANDARD_OBJECT_PREREQUISITES.json'),'kernel_replay_performed':False,'historical_review_compilation':{'project_modules':173,'independent_control_modules':1,'standard_objects_reused':2663},'scope':'Prerequisite-bound intermediate formal evidence. No blanket portable kernel PASS, no standard package source rebuild, no protected source edits, integration or closure.'}
 if args.compile and not args.prerequisite_root:
  result['status']='BLOCKED_MISSING_PREREQUISITES';(out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit('Exact external prerequisites required')
 if args.prerequisite_root:
  pre=Path(args.prerequisite_root).resolve();missing=[]
  for row in [*runtime,*standard]:
   p=pre/row['path']
   if not p.is_file() or sha(p)!=row['sha256']:missing.append(row['path'])
  if missing:
   result.update(status='BLOCKED_MISSING_OR_MISMATCHED_PREREQUISITES',prerequisite_failures=missing);(out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');raise SystemExit('External prerequisite mismatch; see receipt')
  lean=pre/'.toolchains/lean-4.19.0-linux/bin/lean';version=subprocess.check_output([str(lean),'--version'],text=True).strip();assert 'version 4.19.0' in version
  result.update(status='INTEGRITY_AND_PREREQUISITES_PASS_NOT_COMPILED',prerequisites_verified=True,lean_version_output=version)
  if args.compile:
   std=out/'standard-lib';fresh=out/'fresh-project-lib';logs=out/'logs';std.mkdir();fresh.mkdir();logs.mkdir()
   for row in standard:
    link=std/Path(*row['module'].split('.')).with_suffix('.olean');link.parent.mkdir(parents=True,exist_ok=True);link.symlink_to((pre/row['path']).resolve())
   env=os.environ.copy();env['LEAN_PATH']=str(fresh)+os.pathsep+str(std);env.pop('LEAN_SRC_PATH',None);compiled=[]
   for row in [*sources,{'module':'IndependentControls','sha256':sha(r/'IndependentControls.lean')}]:
    name=row['module'];source=(r/'IndependentControls.lean') if name=='IndependentControls' else r/'sources'/Path(*name.split('.')).with_suffix('.lean');target=fresh/Path(*name.split('.')).with_suffix('.olean');target.parent.mkdir(parents=True,exist_ok=True)
    run=subprocess.run([str(lean),'--trust=0','-o',str(target),str(source)],cwd=(r if name=='IndependentControls' else r/'sources'),env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=logs/(name.replace('.','_')+'.log');log.write_text(run.stdout)
    assert run.returncode==0,(name,run.returncode,run.stdout);assert "declaration uses 'sorry'" not in run.stdout,(name,'sorry warning')
    compiled.append({'module':name,'source_sha256':sha(source),'output_sha256':sha(target),'log_sha256':sha(log)});print('COMPILED',len(compiled),name,flush=True)
   audit=(logs/'ProofUniquenessAudit.log').read_text();expected=(r/'ProofUniquenessAudit.log').read_text();important=lambda s:[line for line in s.splitlines() if line.startswith(('PASS ','IMPORTED '))];assert important(audit)==important(expected),'Dependency audit differs';assert (logs/'IndependentControls.log').read_bytes()==(r/'IndependentControls.log').read_bytes(),'Independent controls differ'
   for row in [*runtime,*standard]:assert sha(pre/row['path'])==row['sha256'],row['path']
   result.update(status='PASS_PROJECT_SOURCE_REBUILD_WITH_REUSED_STANDARD_OBJECTS',verification_tier='FRESH_PROJECT_KERNEL_REPLAY_WITH_PINNED_EXTERNAL_STANDARD_OBJECTS',kernel_replay_performed=True,trust=0,project_sources_freshly_compiled=173,independent_control_modules_freshly_compiled=1,standard_objects_reused_not_recompiled=2663,compiled=compiled,audit_lines_match=True,independent_control_log_byte_identical=True)
 assert actual()==manifest['files'],'Extracted evidence changed';result['extracted_evidence_unchanged']=True
 (out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='compiled'}))
if __name__=='__main__':main()
