#!/usr/bin/env python3
"""Fresh source replay for actual finite mixed and TypeCode transformations."""
from pathlib import Path
import argparse,datetime,importlib.util,json,os,subprocess,tempfile
R=Path(__file__).resolve().parent;W=R.parent;V=R/'validation';P=W/'hase-coded-poly-transformations-20261010'
spec=importlib.util.spec_from_file_location('predecessor_verify',P/'verify.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p);b=p.b
OWN=['TypeRenaming','FiniteTypeEnvironments','MixedTypeSubstitution','MixedSpecializations','TypeCodeRenaming','TypeCodeSubstitution','FiniteTypeCodeCompilation','MixedControls','MixedAudit']
SOURCES=p.SOURCES+[R/(m+'.lean') for m in OWN]
MUTATIONS=['WrongBottomTail','WrongTypeImageWeakening','WrongAllTermLift','WrongTypeCodeCapture']
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--init',action='store_true');args=ap.parse_args()
 if args.init:
  if (V/'INPUT_PINS.json').exists():raise RuntimeError('Pins already exist')
  entries=json.loads((P/'validation/INPUT_PINS.json').read_text())
  added=[R/(m+'.lean') for m in OWN]+[R/'verify.py',R/'RESULT.md']+[R/'diagnostics'/(m+'.lean') for m in MUTATIONS]
  entries += [b.rec(f) for f in added]
  (V/'INPUT_PINS.json').write_text(json.dumps(entries,indent=2)+'\n')
 entries=json.loads((V/'INPUT_PINS.json').read_text());b.check(entries)
 out=Path(tempfile.mkdtemp(prefix='fresh-output-',dir=V));env=dict(os.environ,LEAN_PATH=':'.join(map(str,[out]+b.inherited_paths())))
 records=[]
 for src in SOURCES:
  obj=out/(src.stem+'.olean');result=subprocess.run([str(b.LEAN),'--trust=0','-o',str(obj),str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(src.stem+'.log');log.write_text(result.stdout)
  if result.returncode or any(x in result.stdout for x in ['sorryAx','error:','warning:']):raise RuntimeError('Replay failed '+str(log))
  records.append(dict(module=src.stem,source=b.rec(src),object=b.rec(obj),log=b.rec(log),exit_code=result.returncode));print('PASS '+src.stem,flush=True)
 neg=[]
 for m in MUTATIONS:
  src=R/'diagnostics'/(m+'.lean');result=subprocess.run([str(b.LEAN),'--trust=0',str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(m+'.log');log.write_text(result.stdout)
  if result.returncode==0 or 'error:' not in result.stdout:raise RuntimeError('Mutation did not reject '+m)
  neg.append(dict(module=m,source=b.rec(src),log=b.rec(log),exit_code=result.returncode));print('REJECTED '+m,flush=True)
 b.check(entries)
 receipt=dict(status='PASS',timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),trust=0,baseline_rebuilt=False,protected_inputs_mutated=False,pins_verified_before_after=len(entries),fresh_output=str(out.relative_to(W)),positive=records,negative=neg,actual_mixed_substitution_proved=True,actual_TypeCode_instantiation_proved=True,source_Encodable_unchanged=True,arbitrary_function_environment_computability_assumed=False,whole_checker_computability_proved=False)
 (V/'AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS: '+str(len(entries))+' pins unchanged')
if __name__=='__main__':main()
