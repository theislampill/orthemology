#!/usr/bin/env python3
"""Pinned selected trust-zero replay for the exact canonical syntax validator."""
from pathlib import Path
import argparse, datetime, importlib.util, json, os, re, subprocess, tempfile
R=Path(__file__).resolve().parent;W=R.parent;V=R/'validation';B=W/'hase-source-family-computability-20261010';S=W/'hase-coded-scope-computability-20261010'
spec=importlib.util.spec_from_file_location('family_verify',B/'verify.py');b=importlib.util.module_from_spec(spec);spec.loader.exec_module(b)
MODULES=['ExactSyntaxValidity','CoreGrammar','GrammarComputability','GrammarExactness','GrammarImage','CanonicalDecoderBridge','ValidityControls','ValidityAudit']
SOURCES=[B/'FamilyComputability.lean',S/'CodedScope.lean']+[R/(m+'.lean') for m in MODULES]
MUTATIONS=['AcceptBadTerminator','AcceptBadCrossSort','IgnoreIdentityRightPoly','WrongTypeCodeTag','IgnoreBadBound']
def initialize():
 if (V/'INPUT_PINS.json').exists(): raise RuntimeError('Refusing to overwrite pins')
 entries=json.loads((S/'validation/INPUT_PINS.json').read_text())
 own=[R/(m+'.lean') for m in MODULES]+[R/'verify.py',R/'RESULT.md',V/'FOUNDATION_FREEZE.json']+[R/'diagnostics'/(m+'.lean') for m in MUTATIONS]
 entries += [b.rec(p) for p in own]
 seen={}
 for e in entries:
  if e['path'] in seen and e != seen[e['path']]:raise RuntimeError('Inconsistent upstream pin '+e['path'])
  seen[e['path']]=e
 pins=list(seen.values());(V/'INPUT_PINS.json').write_text(json.dumps(pins,indent=2)+'\n');return pins
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--init',action='store_true');args=ap.parse_args()
 pins=initialize() if args.init else json.loads((V/'INPUT_PINS.json').read_text());b.check(pins)
 foundation=json.loads((V/'FOUNDATION_FREEZE.json').read_text());b.check(foundation['files'])
 out=Path(tempfile.mkdtemp(prefix='fresh-output-',dir=V));env=dict(os.environ,LEAN_PATH=':'.join(map(str,[out]+b.inherited_paths())))
 records=[]
 for src in SOURCES:
  obj=out/(src.stem+'.olean');p=subprocess.run([str(b.LEAN),'--trust=0','-o',str(obj),str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(src.stem+'.log');log.write_text(p.stdout)
  if p.returncode or any(x in p.stdout for x in ['sorryAx','error:','warning:']):raise RuntimeError('Failed '+str(log))
  if src.stem=='ValidityControls':
   want=['['+', '.join(['true']*20)+']','['+', '.join(['false']*7)+']']
   if p.stdout.strip().splitlines()!=want:raise RuntimeError('Unexpected runtime controls '+p.stdout)
  if src.stem=='ValidityAudit':
   axioms=re.findall(r'depends on axioms: \[([^]]*)\]',p.stdout)
   if len(axioms)!=11:raise RuntimeError('Missing axiom audit')
   if any(set(a.split(', '))-{'propext','Classical.choice','Quot.sound'} for a in axioms):raise RuntimeError('Unexpected axiom')
  records.append(dict(module=src.stem,source=b.rec(src),object=b.rec(obj),log=b.rec(log),exit_code=p.returncode));print('PASS '+src.stem,flush=True)
 neg=[]
 for m in MUTATIONS:
  src=R/'diagnostics'/(m+'.lean');p=subprocess.run([str(b.LEAN),'--trust=0',str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(m+'.log');log.write_text(p.stdout)
  expected="tactic 'rfl' failed" if m=='WrongTypeCodeTag' else "tactic 'decide' proved that the proposition"
  if p.returncode==0 or expected not in p.stdout or 'error:' not in p.stdout:raise RuntimeError('Mutation not rejected as expected '+str(log))
  neg.append(dict(module=m,source=b.rec(src),log=b.rec(log),exit_code=p.returncode,expected_rejection=expected));print('REJECTED '+m,flush=True)
 b.check(pins);b.check(foundation['files'])
 receipt=dict(status='PASS',timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),trust=0,lean_version=subprocess.check_output([str(b.LEAN),'--version'],text=True).strip(),baseline_rebuilt=False,protected_inputs_mutated=False,pins_verified_before_after=len(pins),foundation_freeze_unchanged=True,fresh_output=str(out.relative_to(W)),positive=records,negative=neg,core_canonical_validity=True,canonical_decode2_reencode_PR=True,ordinary_decode_equivalence_claimed=False,whole_checker_computability_proved=False,source_Primcodable_assumed=False,source_derivability_RE_proved=False,T20_closure=False)
 (V/'AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS: '+str(len(pins))+' pins unchanged')
if __name__=='__main__':main()
