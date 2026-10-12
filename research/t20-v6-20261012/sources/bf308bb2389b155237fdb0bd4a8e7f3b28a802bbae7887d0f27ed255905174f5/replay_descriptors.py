from pathlib import Path
import sys,importlib.util,json,os,subprocess,datetime,re
sys.dont_write_bytecode=True
W=Path.cwd(); R=W/'hase-certificate-domain-independent-review-20261010'; V=R/'descriptor-replay-final';V.mkdir(exist_ok=False)
spec=importlib.util.spec_from_file_location('release',W/'hase-telescope-code-validity-20261010/verify_release.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
C=W/'hase-certificate-code-validity-20261010';A=W/'hase-auxiliary-checker-computability-20261010'
freeze=json.loads((C/'validation/DESCRIPTION_FREEZE.json').read_text()); pins=json.loads((p.V/'RELEASE_PINS.json').read_text())+json.loads((A/'validation/INPUT_PINS.json').read_text())+freeze['files']
for n in ['PolyCertificateEncoding','EncodedCertificatePayloads','SerializedCertificateCodec']:
 for ext in ['.lean','.olean']:
  pins.append(p.b.rec(W/'hase-joint-certificate-codec-20261010'/('validation' if ext=='.olean' else '')/(n+ext)))
p.b.check(pins)
schema=json.loads((C/'SCHEMA.json').read_text()); assert [len(x['ctors']) for x in schema]==[5,2,7,8,2,6,63,1,2]
audit=R/'DescriptorReviewAudit.lean'
lemmas=[c['lemma'] for t in schema for c in t['ctors']]
assert len(lemmas)==96 and len(set(lemmas))==96
audit.write_text('import CertificateDescriptions\nopen CertificateCodeValidity\n'+'\n'.join('#print axioms '+n for n in lemmas+['primrec_pack','primrec_iterRest','primrec_slot','primrec_fieldCode','primrec_rebuildField','primrec_dependencies','primrec_rebuild','primrec_localShape','primrec_localChildren'])+'\n')
sources=[A/(n+'.lean') for n in ['AuxiliaryCodeCore','StepCode','PolyCode']]+[C/(n+'.lean') for n in ['ConstructorDescriptors','CertificateDescriptions']]+[R/'DescriptorReviewControls.lean',audit]
pins += [p.b.rec(s) for s in sources]+[p.b.rec(R/'replay_descriptors.py')]
(R/'DESCRIPTOR_REVIEW_PINS.json').write_text(json.dumps(pins,indent=2)+'\n')
env=dict(os.environ,LEAN_PATH=':'.join(map(str,[V,R/'telescope-replay']+p.b.inherited_paths())))
rows=[]
for src in sources:
 obj=V/(src.stem+'.olean');run=subprocess.run([str(p.b.LEAN),'--trust=0','-o',str(obj),str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=V/(src.stem+'.log');log.write_text(run.stdout)
 assert run.returncode==0 and not any(x in run.stdout for x in ['sorryAx','error:','warning:']),str(log)
 if src==audit:
  ax=re.findall(r'depends on axioms: \[([^]]*)\]',run.stdout); noax=run.stdout.count('does not depend on any axioms');assert len(ax)+noax==105
  assert all(set(filter(None,x.split(', ')))-{'propext','Classical.choice','Quot.sound'}==set() for x in ax)
 rows.append({'module':src.stem,'source':p.b.rec(src),'object':p.b.rec(obj),'log':p.b.rec(log),'exit_code':run.returncode});print('PASS '+src.stem,flush=True)
p.b.check(pins)
receipt={'status':'PASS_FROZEN_DESCRIPTOR_LAYER_ONLY','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trust':0,'lean_version':subprocess.check_output([str(p.b.LEAN),'--version'],text=True).strip(),'baseline_rebuilt':False,'protected_inputs_mutated':False,'pins_verified_before_after':len(pins),'freeze':p.b.rec(C/'validation/DESCRIPTION_FREEZE.json'),'positive':rows,'constructor_counts':[len(t['ctors']) for t in schema],'axiom_audits':105,'independent_kernel_controls':9,'global_certificate_canonical_validity_accepted':False}
(R/'DESCRIPTOR_REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS descriptors only',flush=True)
