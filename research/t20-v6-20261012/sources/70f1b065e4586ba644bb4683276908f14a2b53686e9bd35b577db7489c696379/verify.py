#!/usr/bin/env python3
"""Pinned fresh proof replay for all actual Rule code maps."""
from pathlib import Path
import argparse,datetime,importlib.util,json,os,re,subprocess,tempfile
R=Path(__file__).resolve().parent;W=R.parent;V=R/'validation'
A=W/'hase-auxiliary-checker-computability-20261010';T=W/'hase-telescope-code-validity-20261010';D=W/'hase-certificate-code-validity-20261010';F=W/'hase-exact-syntax-validity-20261010'
spec=importlib.util.spec_from_file_location('aux_verify',A/'verify.py');a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a);b=a.b
OWN=['PolyTemplates','TypeTemplates','RuleCodeBasics','RuleConclusionCode','RulePremisesCode','RuleSideCode','RuleMapControls','RuleMapAudit']
SOURCES=a.SOURCES+[F/'CanonicalDecoderBridge.lean']+[T/(m+'.lean') for m in ['TelescopeCodeValidity','TelescopeNatTransport','ListNatCodeTransport']]+[D/(m+'.lean') for m in ['ConstructorDescriptors','CertificateDescriptions']]+[R/(m+'.lean') for m in OWN]
MUTATIONS=['DropUnusedImages','IgnoreLookupEvidence','IgnoreConvScope','LiftTermScopeUnderAll','IgnorePolyEvidence','ReverseMotiveArguments']
def initialize():
 if (V/'INPUT_PINS.json').exists():raise RuntimeError('Pins already exist')
 entries=json.loads((A/'validation/INPUT_PINS.json').read_text())+json.loads((T/'validation/RELEASE_PINS.json').read_text())+json.loads((D/'validation/DESCRIPTION_FREEZE.json').read_text())['files']
 added=[R/(m+'.lean') for m in OWN]+[R/p for p in ['verify.py','RESULT.md','generate_rule_maps.py','generate_rule_sides.py','validation/CORE_SOURCE_FREEZE.json']]+[R/'diagnostics'/(m+'.lean') for m in MUTATIONS]
 added += [W/'hase-joint-certificate-codec-20261010'/p for p in ['SerializedCertificateCodec.lean','validation/SerializedCertificateCodec.olean']]
 added += [W/'hase-joint-certificate-checker-20261010'/p for p in ['generate_rules.py','generated_rule_metadata.json','CertificateRules.lean']]
 entries += [b.rec(f) for f in added]
 seen={}
 for e in entries:
  if e['path'] in seen and e!=seen[e['path']]:raise RuntimeError('Inconsistent pin '+e['path'])
  seen[e['path']]=e
 pins=list(seen.values());(V/'INPUT_PINS.json').write_text(json.dumps(pins,indent=2)+'\n');return pins

def regenerate(out):
 # Generator R controls output location; retained metadata remains at the same parent.
 gen=Path(tempfile.mkdtemp(prefix='regenerated-',dir=R));records=[]
 for script in ['generate_rule_maps.py','generate_rule_sides.py']:
  source=(R/script).read_text()
  # Set R after its ordinary declaration without altering any translation logic.
  source=source.replace('R=Path(__file__).resolve().parent','R=Path('+repr(str(gen))+')')
  target=gen/script;target.write_text(source)
 # Both generators locate metadata via R.parent. Rebind only its exact frozen path.
 p=gen/'generate_rule_maps.py';s=p.read_text().replace("R.parent/'hase-joint-certificate-checker-20261010/generated_rule_metadata.json'",repr(str(W/'hase-joint-certificate-checker-20261010/generated_rule_metadata.json')))
 # Preserve Path operand needed by read_text.
 s=s.replace('('+repr(str(W/'hase-joint-certificate-checker-20261010/generated_rule_metadata.json'))+').read_text()', 'Path('+repr(str(W/'hase-joint-certificate-checker-20261010/generated_rule_metadata.json'))+').read_text()');p.write_text(s)
 for script in ['generate_rule_maps.py','generate_rule_sides.py']:
  r=subprocess.run(['python',str(gen/script)],cwd=W,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (out/(script+'.log')).write_text(r.stdout)
  if r.returncode:raise RuntimeError('Regeneration failed '+r.stdout)
 for m in ['RuleConclusionCode','RulePremisesCode','RuleSideCode']:
  p=gen/(m+'.lean')
  if p.read_bytes()!=(R/(m+'.lean')).read_bytes():raise RuntimeError('Regeneration mismatch '+m)
  records.append(b.rec(p))
 return records

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--init',action='store_true');args=ap.parse_args()
 pins=initialize() if args.init else json.loads((V/'INPUT_PINS.json').read_text());b.check(pins)
 out=Path(tempfile.mkdtemp(prefix='fresh-output-',dir=V));generated=regenerate(out)
 env=dict(os.environ,LEAN_PATH=':'.join(map(str,[out]+b.inherited_paths())))
 records=[]
 for src in SOURCES:
  obj=out/(src.stem+'.olean');p=subprocess.run([str(b.LEAN),'--trust=0','-o',str(obj),str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(src.stem+'.log');log.write_text(p.stdout)
  if p.returncode or any(x in p.stdout for x in ['sorryAx','error:','warning:']):raise RuntimeError('Replay failed '+str(log))
  if src.stem=='RuleMapControls' and p.stdout.strip()!='['+', '.join(['true']*17)+']':raise RuntimeError('Wrong runtime controls '+p.stdout)
  if src.stem=='RuleMapAudit':
   audits=re.findall(r'depends on axioms: \[([^]]*)\]',p.stdout)
   if len(audits)!=22 or any(set(x.split(', '))-{'propext','Classical.choice','Quot.sound'} for x in audits):raise RuntimeError('Wrong axiom audit')
  records.append(dict(module=src.stem,source=b.rec(src),object=b.rec(obj),log=b.rec(log),exit_code=p.returncode));print('PASS '+src.stem,flush=True)
 neg=[]
 for m in MUTATIONS:
  src=R/'diagnostics'/(m+'.lean');p=subprocess.run([str(b.LEAN),'--trust=0',str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(m+'.log');log.write_text(p.stdout)
  if p.returncode==0 or "tactic 'decide' proved that the proposition" not in p.stdout:raise RuntimeError('Wrong rejection '+str(log))
  neg.append(dict(module=m,source=b.rec(src),log=b.rec(log),exit_code=p.returncode));print('REJECTED '+m,flush=True)
 b.check(pins)
 receipt=dict(status='PASS',timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),trust=0,baseline_rebuilt=False,protected_inputs_mutated=False,pins_verified_before_after=len(pins),fresh_output=str(out.relative_to(W)),regenerated=generated,positive=records,negative=neg,actual_rule_constructor_count=63,actual_rule_maps=['conclusion','premises','checkSide'],actual_PR_and_source_encoding_exactness=True,full_ordered_type_image_premises=True,assumed_checker_parameters=False,whole_checker_computability_proved=False,source_derivability_RE_proved=False,T20_closure=False)
 (V/'AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS: '+str(len(pins))+' pins unchanged')
if __name__=='__main__':main()
