#!/usr/bin/env python3
"""Compile only frozen cross-typing module and independent controls; retained objects only."""
from pathlib import Path
import hashlib,json,os,re,subprocess,tempfile,argparse
R=Path(__file__).resolve().parent; W=R.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
bind=json.loads((R/'REVIEW_INPUTS.json').read_text())
def custody():
 for row in bind['pinned_files']:
  assert sha(W/row['path'])==row['sha256'],row['path']
custody()
for m in ['CrossTypedObserver']:
 assert sha(R/'frozen'/f'{m}.lean') == sha(W/'hase-cross-typing-observer-20261010'/f'{m}.lean'),m
if (R/'MANIFEST.json').exists():
 for row in json.loads((R/'MANIFEST.json').read_text())['files']:
  assert sha(R/row['path'])==row['sha256'],row['path']
out=args.output or Path(tempfile.mkdtemp(prefix='fresh-',dir=R/'validation'))
out=out.resolve();out.mkdir(parents=True,exist_ok=True)
paths=[out,W/'hase-typed-observer-coherence-20261010/validation/fresh-8iwsptvg',W/'hase-internal-graph-review-20261010/fresh-lib',W/'hase-full-per-review-20261010/fresh-lib']
paths+=list((W/'separating-projection-lean-20261009/.lake/packages').glob('*/.lake/build/lib/lean'))
env={**os.environ,'LEAN_PATH':':'.join(map(str,paths))}
lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'
modules=[(R/'frozen'/f'{m}.lean',True) for m in ['CrossTypedObserver']]
modules += [(R/f'{m}.lean',True) for m in ['CrossReviewControls','CrossReviewDependencies']]
modules += [(R/f'{m}.lean',False) for m in ['RejectCarrierIdentification','RejectMembershipAsCoherence','RejectUnshiftedProduct']]
records=[]; runtime={}
for p,positive in modules:
 m=p.stem
 s=re.sub(r'/\-.*?\-/','',p.read_text(),flags=re.S);s=re.sub(r'--[^\n]*','',s)
 assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern|skipKernelTC)\b',s),m
 cmd=[str(lean),'--trust=0','-o',str(out/f'{m}.olean'),str(p)]
 run=subprocess.run(cmd,env=env,text=True,capture_output=True)
 log=run.stdout+run.stderr;(out/f'{m}.log').write_text('$ '+' '.join(cmd)+'\n'+log)
 record={'module':m,'source_sha256':sha(p),'exit_code':run.returncode,'trust_zero':True,'expected_accept':positive,'log_sha256':sha(out/f'{m}.log')}
 if positive:
  assert run.returncode==0,(m,log)
  assert not any(x in log for x in ['warning:','error:','sorryAx']),(m,log)
  record['object_sha256']=sha(out/f'{m}.olean')
  dep=subprocess.run([str(lean),'--deps',str(p)],env=env,text=True,capture_output=True)
  assert dep.returncode==0,(m,dep.stdout+dep.stderr)
  for name in dep.stdout.splitlines():
   x=Path(name.strip())
   if x.is_file(): runtime[str(x)]=sha(x)
 else:
  assert run.returncode!=0 and 'error:' in log,(m,log)
  assert not any(x in log for x in ['unknown module','unknown constant','failed to synthesize','sorryAx']),(m,log)
 records.append(record);print(m,'PASS' if positive else 'EXPECTED REJECTION',flush=True)
custody()
report={'status':'PASS','positive_modules':3,'expected_rejections':3,'baseline_rebuilds':0,'pinned_originals_unchanged':len(bind['pinned_files']),'modules':records,'direct_import_objects':[{'path':p,'sha256':h} for p,h in sorted(runtime.items())],'scope':'One exact-polynomial Sigma/Pi dual-typing test and conditional observation-coherence obstruction. No core/baseline rebuild, graph bridge, universal W decision, or closure.'}
(out/'REVIEW_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
print('RECEIPT',out/'REVIEW_REPLAY.json',flush=True)
