#!/usr/bin/env python3
"""Selected trust-zero replay with complete retained import-object pins and negative controls."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, subprocess, tempfile
R=Path(__file__).resolve().parent; W=R.parent; V=R/'validation'
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
MODULES=['FamilyComputability','CodeBoundary','FamilyControls','FamilyAudit']
MUTATIONS=['WrongConstructorTag','WrongNumeralStep']
def digest(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def rec(p):return dict(path=str(p.relative_to(W)),sha256=digest(p),bytes=p.stat().st_size)
def inherited_paths():
 raw=subprocess.check_output(['bash','-c',f'source "{R}/env.sh"; printf "\\n__PATH__%s" "$LEAN_PATH"'],text=True,cwd=W)
 return [Path(p) for p in raw.split('__PATH__',1)[1].split(':') if Path(p)!=V]
def check(entries):
 for e in entries:
  if digest(W/e['path'])!=e['sha256']:raise RuntimeError('Changed pinned input: '+e['path'])
def initialize():
 roots=inherited_paths()+[LEAN.parent.parent/'lib/lean']
 own={*MODULES,'ImportManifest'}
 objects=[]
 for line in (V/'imports.log').read_text().splitlines():
  if not line.startswith('DEPENDENCY '):continue
  module=line.split(' ',1)[1]
  if module in own:continue
  rel=Path(module.replace('.','/')+'.olean')
  p=next((root/rel for root in roots if (root/rel).exists()),None)
  if p is None:raise RuntimeError('Cannot resolve '+module)
  objects.append(rec(p))
 sources=[R/(m+'.lean') for m in MODULES]+[R/'ImportManifest.lean',R/'env.sh',R/'verify.py',R/'RESULT.md']
 sources += [R/'diagnostics'/(m+'.lean') for m in MUTATIONS]
 retained=[W/'hase-joint-certificate-codec-20261010/EncodedCertificateSyntax.lean',W/'hase-joint-certificate-codec-20261010/CodecDeriveEncodable.lean',W/'hase-fullper-effective-boundary-20261010/FullPERHalting.lean',W/'hase-fullper-effective-boundary-20261010/FullPERTests.lean',W/'hase-bounded-halting-pr-20261010/BoundedHaltingPR.lean',W/'hase-open-term-standardness-20261010/sources/P01Polynomials.lean',W/'hase-open-term-standardness-20261010/sources/EffectiveObserver.lean',W/'hase-open-term-standardness-20261010/sources/EffectivePrimitiveRecursion.lean']
 pins=dict(created_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),candidate_sources=[rec(p) for p in sources],retained_sources=[rec(p) for p in retained],retained_objects=objects,toolchain=rec(LEAN))
 (V/'INPUT_PINS.json').write_text(json.dumps(pins,indent=2)+'\n')
 return pins
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--init',action='store_true');args=ap.parse_args()
 if args.init and (V/'INPUT_PINS.json').exists():raise RuntimeError('Refusing to overwrite existing pins')
 pins=initialize() if args.init else json.loads((V/'INPUT_PINS.json').read_text())
 allpins=pins['candidate_sources']+pins['retained_sources']+pins['retained_objects']+[pins['toolchain']]
 check(allpins)
 out=Path(tempfile.mkdtemp(prefix='fresh-output-',dir=V));env=dict(os.environ,LEAN_PATH=':'.join(map(str,[out]+inherited_paths())))
 records=[]
 for module in MODULES:
  src=R/(module+'.lean');obj=out/(module+'.olean');cmd=[str(LEAN),'--trust=0','-o',str(obj),str(src)]
  result=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(module+'.log');log.write_text(result.stdout)
  if result.returncode or any(s in result.stdout for s in ['sorryAx','error:','warning:']):raise RuntimeError('Replay failed '+module+'; '+str(log))
  records.append(dict(module=module,source=rec(src),object=rec(obj),log=rec(log),exit_code=result.returncode))
  print('PASS '+module,flush=True)
 negative=[]
 for module in MUTATIONS:
  src=R/'diagnostics'/(module+'.lean');cmd=[str(LEAN),'--trust=0',str(src)]
  result=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(module+'.log');log.write_text(result.stdout)
  expected='tactic \'rfl\' failed' if module=='WrongConstructorTag' else 'type mismatch'
  if result.returncode==0 or expected not in result.stdout:raise RuntimeError('Mutation control did not reject as expected '+module)
  negative.append(dict(module=module,expected_rejection=expected,exit_code=result.returncode,source=rec(src),log=rec(log)))
  print('REJECTED '+module,flush=True)
 check(allpins)
 receipt=dict(status='PASS',timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),lean_version=subprocess.check_output([str(LEAN),'--version'],text=True).strip(),trust=0,baseline_rebuilt=False,protected_inputs_mutated=False,pins_verified_before_after=len(allpins),retained_import_objects=len(pins['retained_objects']),fresh_output=str(out.relative_to(W)),positive=records,negative=negative,axiom_allowlist=['propext','Classical.choice','Quot.sound'],checker_computability_proved=False,source_Primcodable_assumed=False,source_adoption_or_T20_closure=False)
 (V/'AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
 print(json.dumps({k:receipt[k] for k in ['status','trust','retained_import_objects','pins_verified_before_after','baseline_rebuilt']}))
if __name__=='__main__':main()
