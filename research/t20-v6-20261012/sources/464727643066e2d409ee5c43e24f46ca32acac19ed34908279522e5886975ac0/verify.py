#!/usr/bin/env python3
"""Fresh exact-code scope proof replay, retaining the established final codec pins."""
from pathlib import Path
import argparse, datetime, hashlib, importlib.util, json, os, subprocess, tempfile
R=Path(__file__).resolve().parent;W=R.parent;V=R/'validation';B=W/'hase-source-family-computability-20261010'
spec=importlib.util.spec_from_file_location('bridge_verify',B/'verify.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
SOURCES=[B/'FamilyComputability.lean']+[R/(m+'.lean') for m in ['CodedScope','ScopeControls','ScopeAudit']]
MUTATIONS=['WrongBound','IgnoreRightChild']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--init',action='store_true');args=ap.parse_args()
 if args.init:
  if (V/'INPUT_PINS.json').exists():raise RuntimeError('Pins already exist')
  base=json.loads((B/'validation/final-codec-refresh/INPUT_PINS.json').read_text())
  own=[R/(m+'.lean') for m in ['CodedScope','ScopeControls','ScopeAudit']]+[R/'verify.py',R/'RESULT.md']+[R/'diagnostics'/(m+'.lean') for m in MUTATIONS]
  entries=base['candidate_sources']+base['retained_sources']+base['retained_objects']+[base['toolchain']]+[b.rec(p) for p in own]
  (V/'INPUT_PINS.json').write_text(json.dumps(entries,indent=2)+'\n')
 entries=json.loads((V/'INPUT_PINS.json').read_text());b.check(entries)
 out=Path(tempfile.mkdtemp(prefix='fresh-output-',dir=V));env=dict(os.environ,LEAN_PATH=':'.join(map(str,[out]+b.inherited_paths())))
 records=[]
 for src in SOURCES:
  obj=out/(src.stem+'.olean');cmd=[str(b.LEAN),'--trust=0','-o',str(obj),str(src)]
  p=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(src.stem+'.log');log.write_text(p.stdout)
  if p.returncode or any(x in p.stdout for x in ['sorryAx','error:','warning:']):raise RuntimeError('Failed '+str(log))
  records.append(dict(module=src.stem,source=b.rec(src),object=b.rec(obj),log=b.rec(log),exit_code=p.returncode));print('PASS '+src.stem,flush=True)
 neg=[]
 for m in MUTATIONS:
  src=R/'diagnostics'/(m+'.lean');p=subprocess.run([str(b.LEAN),'--trust=0',str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(m+'.log');log.write_text(p.stdout)
  if p.returncode==0 or 'decide' not in p.stdout or 'error:' not in p.stdout:raise RuntimeError('Mutation did not reject '+m)
  neg.append(dict(module=m,source=b.rec(src),log=b.rec(log),exit_code=p.returncode));print('REJECTED '+m,flush=True)
 b.check(entries)
 receipt=dict(status='PASS',timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),trust=0,baseline_rebuilt=False,protected_inputs_mutated=False,pins_verified_before_after=len(entries),fresh_output=str(out.relative_to(W)),positive=records,negative=neg,actual_Scoped_exactness=True,whole_checker_computability_proved=False,source_Primcodable_assumed=False)
 (V/'AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS: '+str(len(entries))+' pins unchanged')
if __name__=='__main__':main()
