#!/usr/bin/env python3
"""Pinned fresh trust-zero replay for exact actual auxiliary checker realizers."""
from pathlib import Path
import argparse,datetime,importlib.util,json,os,re,subprocess,tempfile
R=Path(__file__).resolve().parent;W=R.parent;V=R/'validation';P=W/'hase-coded-mixed-transformations-20261010';F=W/'hase-exact-syntax-validity-20261010';C=W/'hase-joint-certificate-codec-20261010'
spec=importlib.util.spec_from_file_location('mixed_verify',P/'verify.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p);b=p.b
OWN=['AuxiliaryCodeCore','AuxiliaryExactViews','StepCode','StepExact','PolyCode','PolyExact','RedCode','RedExact','FiniteCode','FiniteExact','LookupCode','AuxiliaryControls','AuxiliaryAudit']
EXTRA=['GrammarComputability','GrammarExactness','GrammarImage']
SOURCES=p.SOURCES+[F/(m+'.lean') for m in EXTRA]+[R/(m+'.lean') for m in OWN]
MUTATIONS=['IgnoreStepChild','IgnoreTransMiddle','CollapseAtomApplication','IgnoreFiniteReduction','IgnoreLookupWeakening','AssumeSyntaxValidation']
def initialize():
 if (V/'INPUT_PINS.json').exists():raise RuntimeError('Pins already exist')
 entries=json.loads((P/'validation/INPUT_PINS.json').read_text())+json.loads((F/'validation/INPUT_PINS.json').read_text())
 added=[R/(m+'.lean') for m in OWN]+[R/'verify.py',R/'RESULT.md']+[R/'diagnostics'/(m+'.lean') for m in MUTATIONS]
 added += [C/(m+'.lean') for m in ['PolyCertificateEncoding','EncodedCertificatePayloads']]+[C/'validation'/(m+'.olean') for m in ['PolyCertificateEncoding','EncodedCertificatePayloads']]
 added += [W/'hase-joint-certificate-auxiliary-20261010/AuxiliaryCertificates.lean',W/'hase-joint-certificate-auxiliary-20261010/validation/AuxiliaryCertificates.olean']
 entries += [b.rec(f) for f in added]
 seen={}
 for e in entries:
  if e['path'] in seen and e != seen[e['path']]:raise RuntimeError('Inconsistent pin '+e['path'])
  seen[e['path']]=e
 pins=list(seen.values());(V/'INPUT_PINS.json').write_text(json.dumps(pins,indent=2)+'\n');return pins

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--init',action='store_true');args=ap.parse_args()
 pins=initialize() if args.init else json.loads((V/'INPUT_PINS.json').read_text());b.check(pins)
 out=Path(tempfile.mkdtemp(prefix='fresh-output-',dir=V));env=dict(os.environ,LEAN_PATH=':'.join(map(str,[out]+b.inherited_paths())))
 records=[]
 for src in SOURCES:
  obj=out/(src.stem+'.olean');r=subprocess.run([str(b.LEAN),'--trust=0','-o',str(obj),str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(src.stem+'.log');log.write_text(r.stdout)
  if r.returncode or any(x in r.stdout for x in ['sorryAx','error:','warning:']):raise RuntimeError('Replay failed '+str(log))
  if src.stem=='AuxiliaryAudit':
   audits=re.findall(r'depends on axioms: \[([^]]*)\]',r.stdout)
   if len(audits)!=10 or any(set(a.split(', '))-{'propext','Classical.choice','Quot.sound'} for a in audits):raise RuntimeError('Axiom audit failed')
  records.append(dict(module=src.stem,source=b.rec(src),object=b.rec(obj),log=b.rec(log),exit_code=r.returncode));print('PASS '+src.stem,flush=True)
 neg=[]
 for m in MUTATIONS:
  src=R/'diagnostics'/(m+'.lean');r=subprocess.run([str(b.LEAN),'--trust=0',str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(m+'.log');log.write_text(r.stdout)
  expected='unsolved goals' if m=='AssumeSyntaxValidation' else "tactic 'decide' proved that the proposition"
  if r.returncode==0 or expected not in r.stdout:raise RuntimeError('Unexpected mutation result '+str(log))
  neg.append(dict(module=m,source=b.rec(src),log=b.rec(log),exit_code=r.returncode,expected_rejection=expected));print('REJECTED '+m,flush=True)
 b.check(pins)
 receipt=dict(status='PASS',timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),lean_version=subprocess.check_output([str(b.LEAN),'--version'],text=True).strip(),trust=0,baseline_rebuilt=False,protected_inputs_mutated=False,pins_verified_before_after=len(pins),fresh_output=str(out.relative_to(W)),positive=records,negative=neg,actual_auxiliary_checkers_PR=['checkStep','checkRed','checkFinite','checkPoly','checkLookup'],canonical_input_exactness=True,malformed_inputs_ungated=True,source_Encodable_unchanged=True,source_Primcodable_assumed=False,whole_checker_computability_proved=False,source_derivability_RE_proved=False,T20_closure=False)
 (V/'AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS: '+str(len(pins))+' pins unchanged')
if __name__=='__main__':main()
