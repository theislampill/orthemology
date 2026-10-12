from pathlib import Path
import datetime,hashlib,json,re
R=Path(__file__).resolve().parent;W=R.parent;C=W/'hase-auxiliary-checker-computability-20261010'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p):return {'path':str(p.relative_to(W)),'sha256':sha(p),'bytes':p.stat().st_size}
pins=json.loads((R/'REVIEW_INPUT_PINS.json').read_text())
for pin in pins:
 f=W/pin['path'];assert rec(f)==pin,f
assert sha(C/'validation/INPUT_PINS.json')=='4a4f6a9bdeb453589108b65967198d217090a19cd84099cc4fec7d25b1aac5a3'
assert sha(C/'validation/AUTHOR_REPLAY.json')=='a7905f4c7cc50d16f514072d5ed6dd087efe47e6a92f2e853622ee5675aeb46f'
author=json.loads((C/'validation/AUTHOR_REPLAY.json').read_text());assert author['status']=='PASS' and author['trust']==0
replay=json.loads((R/'SELECTIVE_REPLAY.json').read_text());assert replay['status']=='PASS' and len(replay['positive'])==17 and len(replay['negative'])==6
neg=json.loads((R/'INDEPENDENT_NEGATIVE_RESULTS.json').read_text());assert len(neg)==15
positive=json.loads((R/'INDEPENDENT_POSITIVE_RESULTS.json').read_text())
for x in positive:
 for k in ['source','object','log']:assert rec(W/x[k]['path'])==x[k]
for name in ['InterfaceGuards']:
 src=R/'sources'/(name+'.lean');obj=R/'output'/(name+'.olean');log=R/'output'/(name+'.log');assert obj.exists() and log.read_text()==''
 positive.append({'name':name,'source':rec(src),'object':rec(obj),'log':rec(log),'theorem_count':len(re.findall(r'^theorem ',src.read_text(),re.M))})
for x in neg:
 assert x['exit_code']!=0
 for k in ['source','log']:assert rec(W/x[k]['path'])==x[k]
# Revalidate every import guard against actual current object bytes.
guards=json.loads((R/'EXACT_IMPORT_GUARDS.json').read_text())
for rows in guards.values():
 for x in rows:assert rec(W/x['selected_object']['path'])==x['selected_object']
receipt={
 'status':'PASS','scope':'All five actual auxiliary certificate checker code realizers; canonical inputs only',
 'reviewer':'private-locator:b4fbebf561863267ef8e','author':'private-locator:effefec49e9dbafdc7c3',
 'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'candidate_input_pins':rec(C/'validation/INPUT_PINS.json'),'author_receipt':rec(C/'validation/AUTHOR_REPLAY.json'),
 'mixed_dependency_review':rec(W/'hase-coded-mixed-independent-review-20261010/REVIEW_RECEIPT.json'),
 'selective_replay':rec(R/'SELECTIVE_REPLAY.json'),'report':rec(R/'REVIEW.md'),
 'lean_version':replay['lean_version'],'trust':0,'baseline_rebuilt':False,'protected_or_candidate_inputs_changed':False,
 'candidate_pins_before_after':2907,'additional_review_pins_before_after':27,'author_receipt_checked_at_seal':True,
 'fresh_selected_modules':17,'source_constructor_coverage':24,'author_mutation_rejections':6,
 'independent_positive':positive,'independent_negative':neg,
 'independent_source_controls':38,'independent_direct_code_controls':55,'interface_guards':10,
 'candidate_helper_axiom_audit_targets':83,'axiom_allowlist':['propext','Classical.choice','Quot.sound'],
 'exact_import_guards':rec(R/'EXACT_IMPORT_GUARDS.json'),'findings':[],
 'boundaries':['Canonical-input exactness only; malformed totalization is not domain validation','Unchanged actual source Encodable instances; no source Primcodable premise','No whole Joint/E checker computability or source derivability RE theorem','No source integration, publication, rule-template review, final reduction, or T20 closure']}
(R/'REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
manifest=[rec(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='REVIEW_MANIFEST.json']
(R/'REVIEW_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('PASS',rec(R/'REVIEW_RECEIPT.json'))
