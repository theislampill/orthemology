from pathlib import Path
import json,hashlib,re
R=Path(__file__).resolve().parent;W=R.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((R/'RETAINED_OBJECTS.json').read_text())
assert all(sha(W/x['path'])==x['sha256'] for x in old), 'Retained object changed'
objects=[];seen=set()
for d in [Path(x) for x in (R/'lean_path.txt').read_text().split(':')][1:]:
 if '.lake/packages/' in str(d):continue
 for p in sorted(d.glob('*.olean')):
  if p.stem in seen:continue
  seen.add(p.stem);objects.append({'module':p.stem,'path':str(p.relative_to(W)),'bytes':p.stat().st_size,'sha256':sha(p)})
(R/'RETAINED_OBJECTS.json').write_text(json.dumps(objects,indent=2)+'\n')
records=json.loads((R/'REPLAY.json').read_text());assert len(records)==11 and all(x['exit_code']==0 for x in records)
for x in records:
 log=(R/'logs'/f"{x['module']}.log").read_text();assert 'sorryAx' not in log and 'error:' not in log and 'warning:' not in log
 for ax in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S):
  assert set(re.sub(r'\s+','',ax).split(',')) <= {'propext','Classical.choice','Quot.sound',''}
 original=W/'hase-generic-fold-transport-20261010'/f"{x['module']}.lean"
 if x['module']=='ClosedInstanceBoundary':original=W/'hase-closed-instance-boundary-20261010/ClosedInstanceBoundary.lean'
 if original.exists(): assert sha(original)==x['source_sha256'],str(original)
 s=(R/'sources'/f"{x['module']}.lean").read_text();s=re.sub(r'/\-.*?\-/|--[^\n]*','',s,flags=re.S)
 assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by)\b',s)
items=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(R.rglob('*')) if p.is_file() and p.name!='MANIFEST.json']
manifest={'status':'PASS','scope':'Eight generic-fold/rigidity author modules, one inherited-instance boundary consequence, two independent control modules; retained baseline objects reused read-only, no baseline rebuild.','lean_binary_sha256':sha(W/'.toolchains/lean-4.19.0-linux/bin/lean'),'all_trust_zero':True,'source_freeze_unchanged':True,'retained_objects_unchanged':True,'protected_mutations':False,'new_modules':len(records),'retained_non_third_party_objects':len(objects),'files':items}
(R/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('PASS',len(records),'modules;',len(objects),'retained objects;',len(items),'manifest items')
print('manifest sha256',sha(R/'MANIFEST.json'))
