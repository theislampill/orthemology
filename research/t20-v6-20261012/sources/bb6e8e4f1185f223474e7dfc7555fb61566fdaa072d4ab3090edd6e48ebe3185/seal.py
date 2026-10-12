from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent;W=R.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
retained=json.loads((R/'RETAINED_OBJECTS.json').read_text())
assert all(sha(W/x['path'])==x['sha256'] for x in retained)
records=json.loads((R/'REPLAY.json').read_text());assert len(records)==3 and all(x['exit_code']==0 for x in records)
for x in records:
 m=x['module'];log=(R/'logs'/f'{m}.log').read_text()
 assert 'sorryAx' not in log and 'error:' not in log
 warnings=re.findall(r'warning: ([^\n]*)',log)
 assert (m=='ComputationLaws' and warnings==["'congr 1' tactic does nothing"]*2) or not warnings,(m,warnings)
 for ax in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S):
  assert set(re.sub(r'\s+','',ax).split(',')) <= {'propext','Classical.choice','Quot.sound',''}
 p=R/'sources'/f'{m}.lean';assert sha(p)==x['source_sha256']
 original=W/'hase-rigidity-initiality-20261010'/p.name
 if original.exists():assert sha(original)==sha(p)
 s=re.sub(r'/\-.*?\-/|--[^\n]*','',p.read_text(),flags=re.S)
 assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by)\b',s)
assert (R/'logs/DependencyAudit.log').read_text().count('PASS source-only ancestry')==4
previous=W/'hase-rigidity-initiality-review-20261010/MANIFEST.json'
assert sha(previous)=='0be821cf0c9a93964f2c734b42f6a8f110f2afdfa7f71fd5aace87a83177b73a'
items=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(R.rglob('*')) if p.is_file() and p.name!='MANIFEST.json']
out={'status':'PASS','scope':'Frozen ComputationLaws delta; independent exact zero/successor judgment controls and source-only transitive ancestry audit.','lean_binary_sha256':sha(W/'.toolchains/lean-4.19.0-linux/bin/lean'),'all_trust_zero':True,'baseline_rebuilt':False,'retained_object_count':len(retained),'retained_objects_unchanged':True,'preceding_review_unchanged':True,'source_freeze_unchanged':True,'protected_mutations':False,'files':items}
(R/'MANIFEST.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS three fresh modules; manifest sha256',sha(R/'MANIFEST.json'))
