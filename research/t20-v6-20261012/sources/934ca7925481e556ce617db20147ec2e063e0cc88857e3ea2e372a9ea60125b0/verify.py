#!/usr/bin/env python3
"""Fresh pinned selected replay for the actual canonical source checker and RE endpoint."""
from pathlib import Path
import argparse,datetime,importlib.util,json,os,re,subprocess,tempfile
R=Path(__file__).resolve().parent;W=R.parent;V=R/'validation'
Q=W/'hase-coded-rule-templates-20261010';D=W/'hase-certificate-code-validity-20261010'
def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
q=load('rules_verify',Q/'verify.py');d=load('domain_verify',D/'verify.py');b=d.b
OWN=['SerialCertificateCheck','CanonicalCertificateCode','SourceProofSearch','TypeInhabitationSearch','SourceSearchControls','SourceSearchAudit','SourceImportManifest']
MUTATIONS=['AcceptMissing','AcceptExtra','AcceptDistinctSwap','AcceptFalseConversion','AcceptMalformedClaim','DropUnusedImage','MakeInvalidSearchTotal']
SOURCES=[]
for p in q.SOURCES+d.SOURCES+[R/(m+'.lean') for m in OWN]:
 if p.stem=='ImportManifest':continue
 if p not in SOURCES:SOURCES.append(p)

def initialize():
 if (V/'INPUT_PINS.json').exists():raise RuntimeError('Refusing to overwrite input pins')
 dp=json.loads((D/'validation/INPUT_PINS.json').read_text())
 entries=json.loads((Q/'validation/INPUT_PINS.json').read_text())+dp['inputs']
 roots=b.inherited_paths()+[b.LEAN.parent.parent/'lib/lean']
 own={p.stem for p in SOURCES};objects=[]
 for line in (R/'diagnostics/SourceImportManifest.log').read_text().splitlines():
  if not line.startswith('DEPENDENCY '):continue
  m=line.split(' ',1)[1]
  if m in own:continue
  rel=Path(m.replace('.','/')+'.olean');p=next((root/rel for root in roots if (root/rel).exists()),None)
  if p is None:raise RuntimeError('Missing retained import '+m)
  objects.append(b.rec(p))
 entries += [b.rec(p) for p in SOURCES]+objects+[b.rec(b.LEAN)]
 entries += [b.rec(R/p) for p in ['verify.py','compile.sh','RESULT.md','validation/CORE_SOURCE_FREEZE.json','SourceImportManifest.lean','diagnostics/RESOURCE_INCONCLUSIVE.json','diagnostics/DeepRuntimeAttempt.lean']]
 entries += [b.rec(R/'diagnostics'/(m+'.lean')) for m in MUTATIONS]
 seen={}
 for e in entries:
  if e['path'] in seen and e!=seen[e['path']]:raise RuntimeError('Inconsistent input pin '+e['path'])
  seen[e['path']]=e
 pins=dict(inputs=list(seen.values()),retained_import_objects=objects)
 (V/'INPUT_PINS.json').write_text(json.dumps(pins,indent=2)+'\n');return pins

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--init',action='store_true');args=ap.parse_args()
 pins=initialize() if args.init else json.loads((V/'INPUT_PINS.json').read_text());b.check(pins['inputs'])
 out=Path(tempfile.mkdtemp(prefix='fresh-output-',dir=V));env=dict(os.environ,LEAN_PATH=':'.join(map(str,[out]+b.inherited_paths())))
 records=[]
 for src in SOURCES:
  obj=out/(src.stem+'.olean');cmd=[str(b.LEAN),'--trust=0','-s','65536','-o',str(obj),str(src)]
  p=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(src.stem+'.log');log.write_text(p.stdout)
  if p.returncode or any(x in p.stdout for x in ['sorryAx','error:','warning:']):raise RuntimeError('Replay failed '+str(log))
  if src.stem=='SourceSearchControls':
   values=re.findall(r'^(true|false)$',p.stdout,re.M)
   if values!=['true','false','false','false']:raise RuntimeError('Wrong runtime controls')
  if src.stem=='SourceSearchAudit' and len(re.findall(r'^PASS ActualSourceEnumerability\.',p.stdout,re.M))!=29:raise RuntimeError('Wrong endpoint audit count')
  records.append(dict(module=src.stem,source=b.rec(src),object=b.rec(obj),log=b.rec(log),exit_code=p.returncode));print('PASS '+src.stem,flush=True)
 neg=[]
 for m in MUTATIONS:
  src=R/'diagnostics'/(m+'.lean');p=subprocess.run([str(b.LEAN),'--trust=0','-s','65536',str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(m+'.log');log.write_text(p.stdout)
  expected='unsolved goals' if m=='MakeInvalidSearchTotal' else "tactic 'decide' proved that the proposition"
  if p.returncode==0 or expected not in p.stdout:raise RuntimeError('Unexpected negative result '+str(log))
  neg.append(dict(module=m,source=b.rec(src),log=b.rec(log),exit_code=p.returncode,expected_rejection=expected));print('REJECTED '+m,flush=True)
 b.check(pins['inputs'])
 receipt=dict(status='PASS',timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),lean_version=subprocess.check_output([str(b.LEAN),'--version'],text=True).strip(),trust=0,stack_kb=65536,baseline_rebuilt=False,protected_inputs_mutated=False,pins_verified_before_after=len(pins['inputs']),retained_import_objects=len(pins['retained_import_objects']),fresh_output=str(out.relative_to(W)),positive=records,negative=neg,actual_canonical_checker_PR=True,all_accepted_Nat_inputs_sound=True,actual_source_certificate_complete=True,six_actual_coded_judgment_families_RE=True,exact_partial_proof_search=True,actual_closed_type_inhabitation_projection_RE=True,axiom_allowlist=['propext','Classical.choice','Quot.sound'],source_Primcodable_assumed=False,checker_computability_assumed=False,supplied_certificate_runtime_values=['true','false','false','false'],deeper_runtime_status='RESOURCE_INCONCLUSIVE',practical_search_or_machine_listing_claimed=False,source_adoption_or_T20_closure=False)
 (V/'AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS: '+str(len(pins['inputs']))+' pins unchanged')
if __name__=='__main__':main()
