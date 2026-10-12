#!/usr/bin/env python3
"""Independent bounded source replay. It never reuses candidate target oleans."""
from pathlib import Path
import datetime,hashlib,json,os,re,shutil,subprocess,tempfile,time
R=Path(__file__).resolve().parent;W=R.parent;C=W/'hase-coded-rule-templates-20261010'
def rec(p):return {'path':str(p.relative_to(W)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
pins=json.loads((R/'FINAL_REVIEW_PINS.json').read_text())
def check():
 for p in pins: assert rec(W/p['path'])==p,p['path']
check();print('PINS_BEFORE',len(pins),flush=True)
e=json.loads((R/'env.json').read_text());L=Path(e['lean']);out=Path(tempfile.mkdtemp(prefix='fresh-replay-',dir=R));roots=[Path(x) for x in e['LEAN_PATH'].split(':') if Path(x)!=R/'output'];env={**os.environ,'LEAN_PATH':':'.join(map(str,[out]+roots))}
modules=['TelescopeNatTransport','ListNatCodeTransport','ConstructorDescriptors','CertificateDescriptions','PolyTemplates','TypeTemplates','RuleCodeBasics','RuleConclusionCode','RulePremisesCode','RuleSideCode','RuleMapControls','RuleMapAudit','IndependentTemplateControls','MalformedRuntime','AllHelperAudit']
records=[]
for n in modules:
 src=R/'sources'/(n+'.lean');obj=out/(n+'.olean');cmd=[str(L),'--trust=0','-o',str(obj),str(src)];t=time.monotonic();p=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=out/(n+'.log');log.write_text(p.stdout)
 assert p.returncode==0 and not any(x in p.stdout for x in ['sorryAx','error:','warning:']),str(log)
 if n=='RuleMapControls':assert p.stdout.strip()=='['+', '.join(['true']*17)+']',p.stdout
 if n=='MalformedRuntime':assert p.stdout.strip()=='(true, true)\n(0, [], false)',p.stdout
 if n in ['RuleMapAudit','AllHelperAudit']:
  rows=re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",p.stdout);expected=22 if n=='RuleMapAudit' else 833;assert len(rows)==expected
  assert all(set(x.strip() for x in a.split(',') if x.strip())<={'propext','Classical.choice','Quot.sound'} for _,a in rows)
  if n=='AllHelperAudit':assert {r[0] for r in rows}==set(json.loads((R/'ALL_HELPER_TARGETS.json').read_text()))
 records.append({'module':n,'source':rec(src),'object':rec(obj),'log':rec(log),'exit_code':p.returncode,'seconds':time.monotonic()-t,'command':cmd});print('PASS',n,flush=True)
 (out/'PARTIAL.json').write_text(json.dumps(records,indent=2)+'\n')
negative=[]
for n in json.loads((R/'INDEPENDENT_NEGATIVE_TARGETS.json').read_text()):
 src=R/'negative'/(n+'.lean');cmd=[str(L),'--trust=0',str(src)];t=time.monotonic();p=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=out/(n+'.log');log.write_text(p.stdout);expected="tactic 'decide' proved that the proposition"
 assert p.returncode!=0 and expected in p.stdout and not any(x in p.stdout for x in ['unknown identifier','unexpected token','failed to import','unknown module']),str(log)
 negative.append({'name':n,'source':rec(src),'log':rec(log),'exit_code':p.returncode,'expected_rejection':expected,'seconds':time.monotonic()-t,'command':cmd});print('REJECTED',n,flush=True)
 (out/'NEGATIVE_PARTIAL.json').write_text(json.dumps(negative,indent=2)+'\n')
# Run unchanged generator scripts under the same relative directory structure.
gen=out/'generator-tree'/C.name;meta=gen.parent/'hase-joint-certificate-checker-20261010';gen.mkdir(parents=True);meta.mkdir()
for name in ['generate_rule_maps.py','generate_rule_sides.py']:shutil.copy2(C/name,gen/name)
shutil.copy2(W/'hase-joint-certificate-checker-20261010/generated_rule_metadata.json',meta/'generated_rule_metadata.json')
for name in ['generate_rule_maps.py','generate_rule_sides.py']:
 p=subprocess.run(['python',str(gen/name)],cwd=W,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/(name+'.log')).write_text(p.stdout);assert p.returncode==0,p.stdout
regenerated=[]
for n in ['RuleConclusionCode','RulePremisesCode','RuleSideCode']:
 f=gen/(n+'.lean');assert f.read_bytes()==(C/f.name).read_bytes();regenerated.append(rec(f))
# Record actual first-resolved import objects; every retained object is pinned.
pinmap={p['path']:p for p in pins};imports={}
for r in records:
 src=W/r['source']['path'];deps=[]
 for m in re.findall(r'^import\s+(\S+)',src.read_text(),re.M):
  f=next((d/(m.replace('.','/')+'.olean') for d in [out]+roots if (d/(m.replace('.','/')+'.olean')).exists()),None);assert f,(src,m);pin=rec(f)
  if f.parent!=out:assert pin==pinmap.get(pin['path']),(src,m)
  deps.append({'module':m,'selected_object':pin})
 imports[src.stem]=deps
(out/'EXACT_IMPORT_GUARDS.json').write_text(json.dumps(imports,indent=2)+'\n');check()
receipt={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lean_version':subprocess.check_output([str(L),'--version'],text=True).strip(),'trust':0,'pins_verified_before_after':len(pins),'author_pin_count':3032,'baseline_rebuilt':False,'protected_inputs_mutated':False,'fresh_output':str(out.relative_to(W)),'positive':records,'negative':negative,'regenerated':regenerated,'import_guards':rec(out/'EXACT_IMPORT_GUARDS.json'),'all_candidate_and_generic_transport_theorems_audited':833,'all63_constructor_and_three_function_metadata_exact':True,'actual_rule_maps_PR_and_canonical_exactness':True,'full_ordered_J_and_E_type_image_premises':True,'malformed_decoder_none_but_side_true':True,'unknown_tag_defaults':[0,[],False],'whole_checker_computability_proved':False,'source_derivability_RE_proved':False,'T20_closure':False}
(out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');(R/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('INDEPENDENT_PASS',out,flush=True)
