#!/usr/bin/env python3
"""Independent review replay: frozen inputs, retained baseline, five fresh modules."""
from pathlib import Path
import argparse,hashlib,json,os,re,subprocess,tempfile
R=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--workspace',type=Path,default=R.parent);p.add_argument('--output',type=Path)
a=p.parse_args();W=a.workspace.resolve();C=W/'hase-finite-raw-obstruction-20261010'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
x=json.loads((R/'frozen/INPUTS.json').read_text());frozen=json.loads((R/'REVIEW_INPUTS.json').read_text())
extra=json.loads((R/'REVIEW_DEPENDENCIES.json').read_text())['extra_external_source_objects']
checks=[]
def check(p,digest):
 assert sha(p)==digest,(str(p),sha(p),digest)
 checks.append({'path':str(p),'sha256':digest})
def verify():
 check(C/'MANIFEST.json',frozen['candidate_manifest_sha256'])
 check(R/'frozen/MANIFEST.json',frozen['candidate_manifest_sha256'])
 for row in frozen['candidate_files']:
  check(C/row['path'],row['sha256']);check(R/'frozen'/row['path'],row['sha256'])
 for row in [x['receipt']]+x['read_only_prior_controls']:check(W/row['path'],row['sha256'])
 for row in x['source_objects']+x['external_source_objects']+extra:
  for k in ['source','object']:check(W/row[k+'_path'],row[k+'_sha256'])
 check(W/'.toolchains/lean-4.19.0-linux/bin/lean',x['lean_binary_sha256'])
 for row in json.loads((R/'MANIFEST.json').read_text())['files']:check(R/row['path'],row['sha256'])
 original=json.loads((W/x['receipt']['path']).read_text())
 assert original['status']=='PASS'
 sources={r['module']:r for r in original['source_checks']}
 objects={r['module']:r for r in original['build_records']}
 for row in x['source_objects']:
  assert sources[row['module']]['sha256']==row['source_sha256']
  obj=objects[row['module']]
  assert obj['source_sha256']==row['source_sha256']
  assert obj['object_sha256']==row['object_sha256']
  assert obj['trust_zero'] and obj['exit_code']==0
verify()
if a.output:
 O=a.output.resolve();O.mkdir(parents=True,exist_ok=False)
else:
 P=W/'hase-finite-raw-review-replay-20261010';P.mkdir(exist_ok=True);O=Path(tempfile.mkdtemp(prefix='final-',dir=P))
lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'
libs=[O,W/'hase-full-per-review-20261010/fresh-lib']+sorted((W/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env={**os.environ,'LEAN_PATH':':'.join(map(str,libs))}
version=subprocess.check_output([str(lean),'--version'],text=True).strip();assert 'version 4.19.0' in version
records=[];logs=[version]
for src in [R/'frozen'/(m+'.lean') for m in ['FiniteK','SourceRaw','RawImages','DependencyAudit']]+[R/'IndependentControls.lean']:
 m=src.stem
 content=re.sub(r'/\-.*?\-/','',src.read_text(),flags=re.S);content=re.sub(r'--[^\n]*','',content);content=re.sub(r'"(?:\\.|[^"\\])*"','""',content)
 assert not re.findall(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern|skipKernelTC)\b',content),m
 cmd=[str(lean),'--trust=0','-o',str(O/(m+'.olean')),str(src)]
 run=subprocess.run(cmd,env=env,capture_output=True,text=True);output=run.stdout+run.stderr
 (O/(m+'.log')).write_text(output);logs.append('$ '+' '.join(cmd)+'\n'+output)
 assert run.returncode==0,(m,output)
 assert not any(s in output for s in ['error:','warning:','sorryAx']),(m,output)
 axioms=set()
 for found in re.findall(r'(?:depends on axioms:|axioms)\s*\[([^\]]*)\]',output,re.S):axioms.update(re.sub(r'\s+','',found).split(','))
 axioms.discard('');assert axioms<={'propext','Classical.choice','Quot.sound'}
 records.append({'module':m,'source':str(src),'source_sha256':sha(src),'object_sha256':sha(O/(m+'.olean')),'log_sha256':sha(O/(m+'.log')),'command':cmd,'exit_code':0,'trust_zero':True,'axioms':sorted(axioms)})
 print(m,'PASS',flush=True)
verify()
(O/'REPLAY.log').write_text('\n'.join(logs))
receipt={'status':'PASS','lean_version':version,'lean_binary_sha256':sha(lean),'candidate_manifest_sha256':frozen['candidate_manifest_sha256'],'review_manifest_sha256':sha(R/'MANIFEST.json'),'output':str(O),'modules':records,'retained_source_objects_matched_to_prior_trust_zero_receipt':len(x['source_objects']),'retained_external_source_object_pairs':len(x['external_source_objects']),'extra_reviewer_external_source_object_pairs':len(extra),'baseline_rebuilt':False,'candidate_and_predecessor_inputs_unchanged_before_and_after':True,'verified_hash_checks':len(checks),'all_hash_checks':checks,'scope':'Independent finite total Raw K-only obstruction review, exact finite compositional summary corollary, and partial-K-slice controls. No source integration, universal W decision, HasE noninhabitation, historical novelty, or audit closure.'}
(O/'REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('Receipt:',O/'REPLAY.json')
