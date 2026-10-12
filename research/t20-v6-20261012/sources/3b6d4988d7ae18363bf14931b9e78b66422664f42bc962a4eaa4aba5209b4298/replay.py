#!/usr/bin/env python3
"""Independent bounded replay: frozen full-E port, original controls and boundary checks."""
from pathlib import Path
import hashlib,json,os,re,subprocess,tempfile
R=Path(__file__).resolve().parent;W=R.parent;A=W/'hase-full-e-dependent-induction-20261010'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
author=['FullESupport','FullEInitiality','FullESectionCorollaries','FullEUniformSection',
 'FullEComputationLaws','FullESectionApplication','FullEInductionControls']
controls=['IndependentScopeControl','IndependentBinderJControl','RetainedBoundaryControl','FullEDependencyAudit']
negative=['MissingRigidityMustFail','RawSuccessorMustFail','OriginalPremiseMustFail','CapturedBinderMustFail']
inputs=json.loads((R/'VERIFIED_INPUTS.json').read_text())['checks']
def verify():
 for row in inputs: assert sha(W/row['path'])==row['sha256'],row['path']
 for row in json.loads((R/'MANIFEST.json').read_text())['files']:
  assert sha(R/row['path'])==row['sha256'],row['path']
 for m in author:assert sha(A/f'{m}.lean')==sha(R/'sources'/f'{m}.lean'),m
verify()
out=Path(tempfile.mkdtemp(prefix='replay-',dir=R))
paths=(R/'lean_path.txt').read_text().strip().split(':')
assert paths[0]==str(A/'validation')
paths[0]=str(out)
env=dict(os.environ,LEAN_PATH=':'.join(paths));lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'
version=subprocess.check_output([str(lean),'--version'],text=True).strip();assert '4.19.0' in version
records=[];retained={}
for m in author+controls+negative:
 source=R/'sources'/f'{m}.lean';obj=out/f'{m}.olean';logfile=out/f'{m}.log'
 deps=subprocess.check_output([str(lean),'--deps',str(source)],env=env,text=True).splitlines()
 for d in deps:
  p=Path(d)
  if p.parent!=out:retained[str(p.relative_to(W))]=sha(p)
 command=[str(lean),'--trust=0','-o',str(obj),str(source)]
 p=subprocess.run(command,env=env,text=True,capture_output=True)
 log=p.stdout+p.stderr;logfile.write_text(log)
 expect=m not in negative
 assert (p.returncode==0)==expect,(m,log)
 code=re.sub(r'/\-.*?\-/','',source.read_text(),flags=re.S);code=re.sub(r'--[^\n]*','',code)
 code=re.sub(r'"(?:\\.|[^"\\])*"','""',code)
 assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern|skipKernelTC)\b',code),m
 axioms=[]
 if expect:
  assert not any(x in log for x in ('sorryAx','error:','warning:')),(m,log)
  for ax in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S):
   found=set(re.sub(r'\s+','',ax).split(','))-{''}
   assert found<={'propext','Classical.choice','Quot.sound'},(m,found)
   axioms.extend(found)
 else:
  assert 'type mismatch' in log,(m,log)
  assert not obj.exists(),m
 records.append({'module':m,'source_sha256':sha(source),'exit_code':p.returncode,
  'expected_success':expect,'command':command,'log':str(logfile.relative_to(R)),
  'log_sha256':sha(logfile),'object_sha256':sha(obj) if obj.exists() else None,
  'axioms':sorted(set(axioms)),'resolved_direct_imports':deps})
 print(m,'PASS' if expect else 'EXPECTED REJECTION',flush=True)
verify()
for path,h in retained.items():assert sha(W/path)==h,path
receipt={'status':'PASS','lean_version':version,'lean_binary_sha256':sha(lean),'trust_zero':True,
 'baseline_rebuilt':False,'protected_mutations':False,'source_freeze_unchanged':True,
 'verified_unique_input_bindings':len(inputs),'fresh_output':str(out.relative_to(R)),
 'lean_path':paths,'retained_direct_import_objects':retained,'records':records}
(R/'REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(f'PASS: {len(author)} frozen author modules, {len(controls)} positive review modules, {len(negative)} expected rejections; {len(inputs)} unique bindings unchanged.')
