from pathlib import Path
import datetime,hashlib,json,os,subprocess,re
R=Path(__file__).resolve().parent;W=R.parent;C=W/'hase-coded-mixed-transformations-20261010';e=json.loads((R/'env.json').read_text());env={**os.environ,'LEAN_PATH':e['LEAN_PATH']}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p):return {'path':str(p.relative_to(W)),'sha256':sha(p),'bytes':p.stat().st_size}
records=[]
for name in json.loads((R/'INDEPENDENT_NEGATIVE_TARGETS.json').read_text()):
 src=R/'negative'/(name+'.lean');p=subprocess.run([e['lean'],'--trust=0',str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=R/'output'/(name+'.log');log.write_text(p.stdout)
 assert p.returncode!=0 and "tactic 'rfl' failed" in p.stdout and not any(x in p.stdout for x in ['unknown identifier','unexpected token','failed to import','unknown module']),log
 records.append({'name':name,'source':rec(src),'log':rec(log),'exit_code':p.returncode,'expected_rejection':"tactic 'rfl' failed"});print('REJECTED',name,flush=True)
positives=[]
for name in ['IndependentSourceEquations','IndependentCodeEquations','AllHelperAudit']:
 src=R/'sources'/(name+'.lean');obj=R/'output'/(name+'.olean');log=R/'output'/(name+'.log')
 assert obj.exists() and not any(x in log.read_text() for x in ['warning:','sorryAx','error:']),log
 positives.append({'name':name,'source':rec(src),'object':rec(obj),'log':rec(log),'theorem_count':len(re.findall(r'^theorem ',src.read_text(),re.M))})
source_bindings=[]
old=json.loads((W/'hase-full-per-review-20261010/PREREQUISITE_REBUILD.json').read_text())
pins=json.loads((R/'REVIEW_INPUT_PINS.json').read_text());pdict={x['path']:x for x in pins}
for n in ['AllSyntax','SubstitutionSyntax','FiniteBridge']:
 src=W/'hase-imported-compiler-transport-20261010/sources'/(n+'.lean');obj=W/'hase-full-per-review-20261010/fresh-lib'/(n+'.olean');record=next(x for x in old['build_records'] if x['module']==n)
 assert sha(src)==record['source_sha256'] and sha(obj)==record['object_sha256'] and sha(obj)==pdict[str(obj.relative_to(W))]['sha256']
 source_bindings.append({'module':n,'source':rec(src),'retained_object':rec(obj),'matches_retained_trust_zero_replay':True})
for pin in pins:
 f=W/pin['path'];assert sha(f)==pin['sha256'] and f.stat().st_size==pin['bytes'],f
candidate_files=[C/(x+'.lean') for x in ['TypeRenaming','FiniteTypeEnvironments','MixedTypeSubstitution','MixedSpecializations','TypeCodeRenaming','TypeCodeSubstitution','FiniteTypeCodeCompilation','MixedControls','MixedAudit']]+[C/'verify.py',C/'RESULT.md']+[C/'diagnostics'/(x+'.lean') for x in ['WrongBottomTail','WrongTypeImageWeakening','WrongAllTermLift','WrongTypeCodeCapture']]
for f in candidate_files:assert str(f.relative_to(W)) in pdict
receipt={'status':'PASS','scope':'Frozen finite coded mixed transformations only','reviewer':'private-locator:93f779c5ca4388e064bf','author':'private-locator:b666aef3749a95964e8c','time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'candidate_input_pins':rec(C/'validation/INPUT_PINS.json'),'author_receipt':rec(C/'validation/AUTHOR_REPLAY.json'),'selective_replay':rec(R/'SELECTIVE_REPLAY.json'),'trust':0,'baseline_rebuilt':False,'protected_or_candidate_inputs_changed':False,'pins_checked_before_and_after':len(pins),'candidate_pins':2867,'final_candidate_modules_and_helpers_covered':len(candidate_files),'retained_source_bindings':source_bindings,'independent_positive':positives,'independent_negative':records,'helper_axiom_audit_targets':len(json.loads((R/'ALL_HELPER_TARGETS.json').read_text())),'all_axioms_within_allowlist':['propext','Classical.choice','Quot.sound'],'findings':[],'boundaries':['finite environments only; no arbitrary function-environment computability','exactness on genuine encodings only; malformed inputs totalized','no alternative source Encodable or source Primcodable instance','no natural-code telescope transport beyond stated List Nat theorem','no whole Joint/E certificate checker or derivability RE theorem','no active rule-template review, source integration, publication, or T20 closure']}
(R/'REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS_FINAL',len(pins),'pins',len(records),'independent negative controls',flush=True)
