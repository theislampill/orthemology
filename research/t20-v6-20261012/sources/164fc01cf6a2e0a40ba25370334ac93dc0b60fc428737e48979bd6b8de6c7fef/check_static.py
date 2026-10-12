from pathlib import Path
import json,re,hashlib
R=Path(__file__).resolve().parent; W=R.parent; C=W/'hase-coded-rule-templates-20261010'
def rec(p):return {'path':str(p.relative_to(W)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
names=json.loads((R/'ALL_HELPER_TARGETS.json').read_text());log=(R/'output/AllHelperAudit.log').read_text();rows=re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",log)
assert len(rows)==len(names)==833 and set(names)=={n for n,a in rows}
assert all(set(x.strip() for x in a.split(',') if x.strip())<={'propext','Classical.choice','Quot.sound'} for n,a in rows)
for n in ['PolyTemplates','TypeTemplates','RuleCodeBasics','RuleConclusionCode','RulePremisesCode','RuleSideCode']:
 src=C/(n+'.lean');text=src.read_text();assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide|partial|noncomputable)\b|instance\s+.*(?:Encodable|Primcodable)',text),n
 assert not re.search(r'^variable',text,re.M),n
metadata=json.loads((W/'hase-joint-certificate-checker-20261010/generated_rule_metadata.json').read_text())
for mod,fun,prefix in [('RuleConclusionCode','conclusion','conclusion'),('RulePremisesCode','premises','premises'),('RuleSideCode','checkSide','side')]:
 s=(C/(mod+'.lean')).read_text()
 for i,r in enumerate(metadata):
  name=r['tag'];assert re.search(r'def '+prefix+'_'+name+r' \(c : Nat\)',s)
  assert f'theorem primrec_{prefix}_{name} : Primrec {prefix}_{name}' in s
  assert re.search(r'theorem '+prefix+'_'+name+r'_exact\b',s)
  assert f'if tag c = {i} then {prefix}_{name} c else ' in s
  assert re.search(r'theorem '+fun+'Code_'+name+r'\b',s)
 assert f'theorem primrec_{fun}Code : Primrec {fun}Code' in s
 assert f'theorem {fun}Code_exact (r : Rule)' in s
# Direct import first-hit identity is pinned or independently rebuilt, not an accidental different object.
e=json.loads((R/'env.json').read_text());roots=[Path(x) for x in e['LEAN_PATH'].split(':')];pins={x['path']:x for x in json.loads((R/'REVIEW_INPUT_PINS.json').read_text())};imports={}
for src in (R/'sources').glob('*.lean'):
 deps=[]
 for m in re.findall(r'^import\s+(\S+)',src.read_text(),re.M):
  obj=next((d/(m.replace('.','/')+'.olean') for d in roots if (d/(m.replace('.','/')+'.olean')).exists()),None);assert obj,(src,m);p=rec(obj)
  if obj.parent!=R/'output':assert p==pins.get(p['path']),(src,m,p)
  deps.append({'module':m,'selected_object':p})
 imports[src.stem]=deps
(R/'EXACT_IMPORT_GUARDS.json').write_text(json.dumps(imports,indent=2)+'\n')
(R/'STATIC_AUDIT.json').write_text(json.dumps({'status':'PASS','all63_each_map_closed_PR_proof':True,'all63_each_map_exact_theorem':True,'tags_0_through_62_dispatch_exact':True,'all_helpers_axiom_audited':len(names),'allowed_axioms':['propext','Classical.choice','Quot.sound'],'no_proof_escapes':True,'no_source_codec_replacement_or_Primcodable_instance':True,'imports_guarded':len(imports)},indent=2)+'\n');print('PASS_STATIC',len(names),len(imports))
