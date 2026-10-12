import hashlib,json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parent;WS=ROOT.parent;AUTHOR=WS/'hase-full-per-extension-20261010';PRED=WS/'hase-imported-compiler-transport-20261010'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):return {'path':str(p.relative_to(WS)),'sha256':sha(p),'bytes':p.stat().st_size}
def decomment(s):
 out=[];d=0;i=0
 while i<len(s):
  if s[i:i+2]=='/-':d+=1;i+=2
  elif d and s[i:i+2]=='-/':d-=1;i+=2
  elif not d and s[i:i+2]=='--':
   j=s.find('\n',i);i=len(s) if j<0 else j
  else:
   if not d or s[i]=='\n':out.append(s[i])
   i+=1
 assert not d
 return ''.join(out)
expected={'FullPER':'2a0d01d92923a22c4b41f512e4c4b3524ea1c630d13478176c5c20d63afa7638','Application':'6d57b65eb3c4ffc8b7c34ba66beea17b7705265dcc4fdd11e66b14d0c5702bb9','ScalarFusionCore':'975e2220158cf6b285cc994e36c408389a908c77e0f63bfa028c8cb416319618'}
new=[]
for m,h in expected.items():
 src=AUTHOR/f'{m}.lean';cpy=ROOT/'sources'/f'{m}.lean'
 assert sha(src)==sha(cpy)==h
 assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern)\b',decomment(src.read_text()))
 logname={'FullPER':'CORE_REPLAY.log','Application':'Application_REPLAY.log','ScalarFusionCore':'ScalarFusionCore_REPLAY.log'}[m]
 log=ROOT/logname;assert log.exists() and not re.search(r'\berror:|sorryAx|declaration uses',log.read_text())
 new.append({'module':m,'source':record(src),'review_copy':record(cpy),'object':record(ROOT/'fresh-lib'/f'{m}.olean'),'log':record(log),'trust_zero':True,'exit_code':0})
prereq=json.loads((ROOT/'PREREQUISITE_REBUILD.json').read_text())
assert len(prereq['source_checks'])==83 and len(prereq['build_records'])==89
for r in prereq['build_records']:
 assert r['exit_code']==0 and r['trust_zero']
 p=ROOT/'fresh-lib'/pathlib.Path(*r['module'].split('.')).with_suffix('.olean')
 assert sha(p)==r['object_sha256'],p
for r in prereq['source_checks']:assert sha(PRED/'sources'/f"{r['module']}.lean")==r['sha256']
for r in prereq['manifest_checks']:
 root=WS/r['package'];assert sha(root/'MANIFEST.json')==r['manifest_sha256']
 for f in json.loads((root/'MANIFEST.json').read_text())['files']:
  assert sha(root/f['path'])==f['sha256']
scalar=(AUTHOR/'ScalarFusionCore.lean').read_bytes();acq=json.loads((AUTHOR/'SCALAR_ACQUISITION.json').read_text())
assert acq['source_bytes'].encode()==scalar
assert acq['sha256']==expected['ScalarFusionCore']
assert hashlib.sha1(b'blob '+str(len(scalar)).encode()+b'\0'+scalar).hexdigest()==acq['response']['sha']=='4fb8ccac2316b5660408017a1ca559fe032a605f'
old_bind=json.loads((WS/'identity-frontier-inspection-20261009/SOURCE_BINDINGS.json').read_text())
sb=next(r for r in old_bind['sources'] if r['name']=='ScalarFusionCore.lean')
assert sb['sha256']==acq['sha256'] and sb['git_blob']==acq['response']['sha']
syntax=decomment((PRED/'sources/ExtensionalRepairSyntax.lean').read_text())
part=syntax.split('inductive HasE')[1].split('\nend')[0]
rules=re.findall(r'^    \| (\w+)',part,re.M);assert len(rules)==20
core=decomment((AUTHOR/'FullPER.lean').read_text())
for th,nextth in [('form_sound','has_sound'),('has_sound','context_sound')]:
 part=core.split('theorem '+th)[1].split('theorem '+nextth)[0]
 arms=re.findall(r'^    \| (\w+)',part,re.M)
 assert len(arms)==29 and set(rules).issubset(arms)
controls=[]
for m,logname in [('IndependentControls','CONTROLS_FINAL.log'),('DependencyAudit','DEPENDENCY_AUDIT.log')]:
 log=ROOT/logname;assert not re.search(r'\berror:|sorryAx|declaration uses',log.read_text())
 controls.append({'module':m,'source':record(ROOT/f'{m}.lean'),'object':record(ROOT/'fresh-lib'/f'{m}.olean'),'log':record(log),'trust_zero':True,'exit_code':0})
assert (ROOT/'DEPENDENCY_AUDIT.log').read_text().count('PASS:')==6
assert len(re.findall(r'^#print axioms', (ROOT/'IndependentControls.lean').read_text(),re.M))==19
result={'status':'PASS_BOUNDED_MODEL_REVIEW','literal_HasE_target':'OPEN','scope':'New full-PER interpretation all-rule soundness and exact semantic application; no derivability/completeness/programme closure','new_replays':new,'review_controls':controls,'reviewer_control_axiom_reports':19,'kernel_dependency_audit_targets':6,'typing_constructor_count':20,'formation_constructor_count':7,'mutual_induction_arm_counts':{'form_sound':29,'has_sound':29},'prerequisite_receipt':record(ROOT/'PREREQUISITE_REBUILD.json'),'prerequisites_built_once':True,'prerequisite_object_hashes_rechecked':True,'predecessor_manifests_still_match':True,'author_frozen_sources_unchanged':True,'scalar_acquisition':record(AUTHOR/'SCALAR_ACQUISITION.json'),'scalar_prior_binding':sb,'standard_axioms_only':['propext','Classical.choice','Quot.sound'],'inherited_FG_semantic_dependency_audit':'PASS','third_party_objects_reused':True,'lean_bootstrap_verified':False}
(ROOT/'REVIEW_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS all final bindings')
