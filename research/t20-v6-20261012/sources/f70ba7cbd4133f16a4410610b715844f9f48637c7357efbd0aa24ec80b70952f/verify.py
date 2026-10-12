#!/usr/bin/env python3
"""Pinned selected trust-zero replay of additive telescope code validity."""
from pathlib import Path
import argparse, datetime, importlib.util, json, os, re, subprocess, tempfile
R=Path(__file__).resolve().parent; W=R.parent; V=R/'validation'
UP=W/'hase-exact-syntax-validity-20261010'; B=W/'hase-source-family-computability-20261010'
spec=importlib.util.spec_from_file_location('family_verify',B/'verify.py'); b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
UPSTREAM=['ExactSyntaxValidity','CoreGrammar','GrammarComputability','GrammarExactness','GrammarImage','CanonicalDecoderBridge']
MODULES=['TelescopeCodeValidity','TelescopeDecoderBridge','TelescopeValidityControls','TelescopeValidityAudit']
SOURCES=[B/'FamilyComputability.lean',W/'hase-coded-scope-computability-20261010/CodedScope.lean']+[UP/(m+'.lean') for m in UPSTREAM]+[R/(m+'.lean') for m in MODULES]
MUTATIONS=['AcceptBadHead','AcceptBadTail','WrongListCodec']
def initialize():
 if (V/'INPUT_PINS.json').exists():raise RuntimeError('Refusing to overwrite existing pins')
 entries=json.loads((UP/'validation/INPUT_PINS.json').read_text())
 entries+=json.loads((UP/'validation/FINAL_FREEZE.json').read_text())['files']
 entries += [b.rec(p) for p in [R/(m+'.lean') for m in MODULES]+[R/'run.py',R/'verify.py',R/'RESULT.md']+[R/'diagnostics'/(m+'.lean') for m in MUTATIONS]]
 seen={}
 for e in entries:
  if e['path'] in seen and e!=seen[e['path']]:raise RuntimeError('Inconsistent pin '+e['path'])
  seen[e['path']]=e
 pins=list(seen.values());(V/'INPUT_PINS.json').write_text(json.dumps(pins,indent=2)+'\n');return pins
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--init',action='store_true');args=ap.parse_args()
 pins=initialize() if args.init else json.loads((V/'INPUT_PINS.json').read_text());b.check(pins)
 out=Path(tempfile.mkdtemp(prefix='fresh-output-',dir=V));env=dict(os.environ,LEAN_PATH=':'.join(map(str,[out]+b.inherited_paths())))
 records=[]
 for src in SOURCES:
  obj=out/(src.stem+'.olean');p=subprocess.run([str(b.LEAN),'--trust=0','-o',str(obj),str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(src.stem+'.log');log.write_text(p.stdout)
  if p.returncode or any(x in p.stdout for x in ['sorryAx','error:','warning:']):raise RuntimeError('Replay failed '+str(log))
  if src.stem=='TelescopeValidityControls':
   if p.stdout.strip().splitlines()!=['[true, true, true, true, true, true]','[false, false, false, false]']:raise RuntimeError('Wrong controls '+p.stdout)
  if src.stem=='TelescopeValidityAudit':
   axioms=re.findall(r'depends on axioms: \[([^]]*)\]',p.stdout)
   if len(axioms)!=8:raise RuntimeError('Missing axiom audit '+p.stdout)
   if any(set(a.split(', '))-{'propext','Classical.choice','Quot.sound'} for a in axioms):raise RuntimeError('Unexpected axiom')
  records.append(dict(module=src.stem,source=b.rec(src),object=b.rec(obj),log=b.rec(log),exit_code=p.returncode));print('PASS '+src.stem,flush=True)
 negative=[]
 for m in MUTATIONS:
  src=R/'diagnostics'/(m+'.lean');p=subprocess.run([str(b.LEAN),'--trust=0',str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(m+'.log');log.write_text(p.stdout)
  expected="tactic 'rfl' failed" if m=='WrongListCodec' else "tactic 'decide' proved that the proposition"
  if p.returncode==0 or expected not in p.stdout or 'error:' not in p.stdout:raise RuntimeError('Mutation not rejected as expected '+str(log))
  negative.append(dict(module=m,source=b.rec(src),log=b.rec(log),exit_code=p.returncode,expected_rejection=expected));print('REJECTED '+m,flush=True)
 b.check(pins)
 receipt=dict(status='PASS',timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),trust=0,lean_version=subprocess.check_output([str(b.LEAN),'--version'],text=True).strip(),baseline_rebuilt=False,protected_inputs_mutated=False,pins_verified_before_after=len(pins),fresh_output=str(out.relative_to(W)),positive=records,negative=negative,telescope_canonical_validity=True,canonical_decode2_reencode_PR=True,ordinary_decode_equivalence_claimed=False,source_Primcodable_assumed=False,whole_checker_computability_proved=False,T20_closure=False)
 (V/'AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS: '+str(len(pins))+' pins unchanged')
if __name__=='__main__':main()
