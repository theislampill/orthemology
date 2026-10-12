#!/usr/bin/env python3
"""Fresh selected trust-zero replay, exact retained imports, controls and input pins."""
from pathlib import Path
import argparse, datetime, importlib.util, json, os, re, subprocess, tempfile
R=Path(__file__).resolve().parent; W=R.parent; V=R/'validation'
B=W/'hase-source-family-computability-20261010'; C=W/'hase-exact-syntax-validity-20261010'; T=W/'hase-telescope-code-validity-20261010'; A=W/'hase-auxiliary-checker-computability-20261010'
sp=importlib.util.spec_from_file_location('base',B/'verify.py'); b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
SCHEMA=json.loads((R/'SCHEMA.json').read_text())
CORE=['ExactSyntaxValidity','CoreGrammar','GrammarComputability','GrammarExactness','GrammarImage','CanonicalDecoderBridge','ValidityControls']
TEL=['TelescopeCodeValidity','TelescopeDecoderBridge','TelescopeValidityControls']
AUX=['AuxiliaryCodeCore','StepCode','PolyCode']
MODULES=['ConstructorDescriptors','CertificateDescriptions','DescriptorLemmas','CertificateGrammar']+[t['type']+'ImageRule' for t in SCHEMA]+[t['type']+'Bounds' for t in SCHEMA]+['CertificateImage','CertificateControls','CertificateAudit','ImportManifest']
SOURCES=[B/'FamilyComputability.lean',W/'hase-coded-scope-computability-20261010/CodedScope.lean']+[C/(m+'.lean') for m in CORE]+[T/(m+'.lean') for m in TEL]+[A/(m+'.lean') for m in AUX]+[R/(m+'.lean') for m in MODULES]
MUTATIONS=['AcceptBadClaimTel','IgnoreSerialHead','IgnoreSerialTail','AcceptBadRuleType','IgnoreSerialTerminator']
STACK_KB=65536

def initialize():
 if (V/'INPUT_PINS.json').exists():raise RuntimeError('Refusing to overwrite input pins')
 own={p.stem for p in SOURCES}; roots=b.inherited_paths()+[b.LEAN.parent.parent/'lib/lean']; objects=[]; retained_modules=[]
 for line in (R/'diagnostics/ImportManifest.log').read_text().splitlines():
  if not line.startswith('DEPENDENCY '):continue
  module=line.split(' ',1)[1]
  if module in own:continue
  rel=Path(module.replace('.','/')+'.olean');p=next((root/rel for root in roots if (root/rel).exists()),None)
  if p is None:raise RuntimeError('Missing retained import '+module)
  objects.append(b.rec(p)); retained_modules.append(module)
 entries=json.loads((T/'validation/RELEASE_PINS.json').read_text())
 entries += [b.rec(p) for p in SOURCES]+objects+[b.rec(b.LEAN)]
 entries += [b.rec(p) for p in R.glob('*.py')]+[b.rec(R/f) for f in ['RESULT.md','SCHEMA.json','AUDIT_NAMES.json','validation/DESCRIPTION_FREEZE.json']]
 entries += [b.rec(R/'diagnostics'/(m+'.lean')) for m in MUTATIONS]
 seen={}
 for e in entries:
  if e['path'] in seen and e!=seen[e['path']]:raise RuntimeError('Inconsistent input pin '+e['path'])
  seen[e['path']]=e
 pins=dict(inputs=list(seen.values()),retained_import_objects=objects,retained_modules=retained_modules)
 (V/'INPUT_PINS.json').write_text(json.dumps(pins,indent=2)+'\n');return pins

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--init',action='store_true');args=ap.parse_args()
 pins=initialize() if args.init else json.loads((V/'INPUT_PINS.json').read_text());b.check(pins['inputs'])
 desc=json.loads((V/'DESCRIPTION_FREEZE.json').read_text());b.check(desc['files'])
 out=Path(tempfile.mkdtemp(prefix='fresh-output-',dir=V));env=dict(os.environ,LEAN_PATH=':'.join(map(str,[out]+b.inherited_paths())))
 records=[]
 for src in SOURCES:
  obj=out/(src.stem+'.olean');cmd=[str(b.LEAN),'--trust=0','-s',str(STACK_KB),'-o',str(obj),str(src)]
  p=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(src.stem+'.log');log.write_text(p.stdout)
  if p.returncode or any(x in p.stdout for x in ['sorryAx','error:','warning:']):raise RuntimeError('Replay failed '+str(log))
  sizes={'ValidityControls':(20,7),'TelescopeValidityControls':(6,4),'CertificateControls':(96,8)}
  if src.stem in sizes:
   yes,no=sizes[src.stem];want=[['true']*yes,['false']*no]
   observed=[[x.strip() for x in row.split(',')] for row in re.findall(r'\[([^]]*)\]',p.stdout)]
   if observed!=want:raise RuntimeError('Unexpected runtime controls '+str(log))
  if src.stem=='CertificateAudit':
   axioms=re.findall(r'depends on axioms: \[([^]]*)\]',p.stdout)
   if len(axioms)!=len(json.loads((R/'AUDIT_NAMES.json').read_text())):raise RuntimeError('Missing axiom audit')
   if any(set(a.split(', '))-{'propext','Classical.choice','Quot.sound'} for a in axioms):raise RuntimeError('Unexpected axiom')
  records.append(dict(module=src.stem,source=b.rec(src),object=b.rec(obj),log=b.rec(log),exit_code=p.returncode));print('PASS '+src.stem,flush=True)
 negative=[]
 for m in MUTATIONS:
  src=R/'diagnostics'/(m+'.lean');p=subprocess.run([str(b.LEAN),'--trust=0','-s',str(STACK_KB),str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(m+'.log');log.write_text(p.stdout);expected="tactic 'decide' proved that the proposition"
  if p.returncode==0 or expected not in p.stdout or 'error:' not in p.stdout:raise RuntimeError('False control not rejected as expected '+str(log))
  negative.append(dict(module=m,source=b.rec(src),log=b.rec(log),exit_code=p.returncode,expected_rejection=expected));print('REJECTED '+m,flush=True)
 # Ensure the final environment has exactly the previously pinned retained imports.
 actual=[l.split(' ',1)[1] for l in (out/'ImportManifest.log').read_text().splitlines() if l.startswith('DEPENDENCY ')]
 owned={p.stem for p in SOURCES};retained=[m for m in actual if m not in owned]
 if retained!=pins['retained_modules']:raise RuntimeError('Retained import coverage changed')
 b.check(pins['inputs']);b.check(desc['files'])
 receipt=dict(status='PASS',timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),trust=0,thread_stack_kb=STACK_KB,lean_version=subprocess.check_output([str(b.LEAN),'--version'],text=True).strip(),baseline_rebuilt=False,protected_inputs_mutated=False,pins_verified_before_after=len(pins['inputs']),retained_import_objects=len(retained),descriptor_freeze_unchanged=True,fresh_output=str(out.relative_to(W)),positive=records,negative=negative,certificate_constructors=96,core_constructors=20,sorts=15,judgment_families=6,main_and_auxiliary_logical_constructors=87,canonical_domain_PR_and_exact=True,ordinary_decode_equivalence_claimed=False,source_Primcodable_assumed=False,whole_semantic_checker_computability_proved=False,source_derivability_RE_proved=False,T20_closure=False)
 (V/'AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS: '+str(len(pins['inputs']))+' pins unchanged')
if __name__=='__main__':main()
