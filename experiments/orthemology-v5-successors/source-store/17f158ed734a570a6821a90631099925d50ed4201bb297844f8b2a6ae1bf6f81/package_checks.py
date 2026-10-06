"""New recovery integration checks, separated from frozen mathematical bytes."""
from pathlib import Path
import hashlib,json,re

if not __debug__:
 raise SystemExit("OPTIMIZED_PYTHON_UNSUPPORTED: disable -O, -OO and PYTHONOPTIMIZE")

def sha(p):
 digest=hashlib.sha256()
 with p.open('rb') as f:
  for chunk in iter(lambda:f.read(1024*1024),b''):digest.update(chunk)
 return digest.hexdigest()
def check_source_locks(package, require_integrity=False):
 if require_integrity:
  assert (package/'FILE_INTEGRITY.json').is_file(),'MISSING_PACKAGE_INTEGRITY_SEAL'
  assert (package/'CONTROL_MANIFEST.json').is_file(),'MISSING_CONTROL_MANIFEST'
 locks=json.loads((package/'MATHEMATICAL_SOURCE_LOCK.json').read_text())
 assert len(locks)==111 and len({r['module'] for r in locks})==111
 actual={p.stem for p in (package/'lean').glob('*.lean') if p.stem!='lakefile'}
 assert actual=={r['module'] for r in locks},'Mathematical module set changed'
 for row in locks:assert sha(package/row['path'])==row['sha256'],'Frozen mathematical byte mismatch: '+row['module']
 if (package/'CONTROL_MANIFEST.json').exists():
  for test in json.loads((package/'CONTROL_MANIFEST.json').read_text())['tests']:
   if test.get('packaged',True):assert sha(package/test['path'])==test['sha256'],'Control source byte mismatch: '+test['path']
 if (package/'FILE_INTEGRITY.json').exists():
  for member in package.rglob('*'):
   if not str(member.relative_to(package)).startswith('lean/.lake/'):
    assert not member.is_symlink(),'SOURCE_PACKAGE_SYMLINK_REFUSED: '+str(member.relative_to(package))
  inventory=json.loads((package/'FILE_INTEGRITY.json').read_text())
  actual={str(p.relative_to(package)) for p in package.rglob('*') if p.is_file() and not str(p.relative_to(package)).startswith('lean/.lake/')}
  assert actual==set(inventory)|{'FILE_INTEGRITY.json'},'Unexpected package members'
  for name,digest in inventory.items():assert sha(package/name)==digest,'File integrity mismatch: '+name
 return len(locks)

def constructor_check(package):
 s=(package/'lean/AllSyntax.lean').read_text();t=(package/'lean/UnaryCertificateSyntax.lean').read_text()
 old=s[s.index('mutual\n'):s.index('\nend\n\nend P01AC')+4];new=t[t.index('mutual\n'):t.index('\nend\n\n')+4]
 marker='    /-- Finite computational evidence; no semantic relation is a rule premise. -/'
 assert new.count(marker)==1
 inherited=new[:new.index(marker)]+'end'
 for x,y in [('CtxC','Ctx'),('FormC','Form'),('HasC','Has')]:inherited=re.sub(r'\b'+x+r'\b',y,inherited)
 assert old==inherited,'HasC inherited mutual constructors changed'
 counts={}
 for name,nextname in [('Ctx','Form'),('Form','Has'),('Has',None)]:
  chunk=old[old.index('inductive '+name):]
  if nextname:chunk=chunk[:chunk.index('inductive '+nextname)]
  counts[name]=len(re.findall(r'^    \| ',chunk,re.M))
 assert counts=={'Ctx':2,'Form':7,'Has':18}
 assert 'P01DF.PolyConv' in new and 'PolyConvPlus' not in new
 assert 'verifyCertificate e f c = true' in new[new.index(marker):]
 return {'status':'PASS','compared_packaged_files':['lean/AllSyntax.lean','lean/UnaryCertificateSyntax.lean'],'retained_constructor_counts':counts,'added_constructor':'HasC.certified','source_hashes':{n:sha(package/'lean'/n) for n in ['AllSyntax.lean','UnaryCertificateSyntax.lean']}}

def coverage_check(package,output):
 modules=set(json.loads((package/'MODULES.json').read_text()));rows=json.loads((output/'declaration-inventory.json').read_text());proofs=set(json.loads((output/'proof-roots.json').read_text()));exclusions=json.loads((output/'nonproof-auxiliary-exclusions.json').read_text())
 assert set(json.loads((output/'module-inventory.json').read_text()))==modules
 assert {r['module'] for r in rows}<=modules
 assert proofs=={r['name'] for r in rows if r['theorem']},'Missing or extra theorem roots'
 assert not proofs & {r['name'] for r in exclusions},'Excluded theorem'
 assert {r['name'] for r in exclusions}=={r['name'] for r in rows if (r['unsafe'] or r['partial']) and not r['theorem']}
 acceptance=json.loads((package/'ACCEPTANCE_MAP.json').read_text())
 accepted={r['module']:r for r in acceptance['modules']}
 assert set(accepted)==modules and len(acceptance['modules'])==len(modules),'Acceptance-root map incomplete or duplicated'
 for lock in json.loads((package/'MATHEMATICAL_SOURCE_LOCK.json').read_text()):
  assert accepted[lock['module']]['source_sha256']==lock['sha256'],'Acceptance map source identity mismatch'
  family=accepted[lock['module']]['accepted_family']
  assert lock['module'] in acceptance['families'][family]['modules'],'Acceptance family module mismatch'
 lanes=json.loads((package/'MODULE_LANES.json').read_text())
 return {'status':'PASS','modules':len(modules),'declarations':len(rows),'theorem_roots':len(proofs),'missing_theorems':[],'extra_theorems':[],'accepted_scope_root_coverage_equal':True,'nonproof_exclusions':len(exclusions),'logical_opaque_declarations':len(json.loads((output/'logical-opaque-inventory.json').read_text())),'logical_opaque_inventory_sha256':sha(output/'logical-opaque-inventory.json'),'import_only_modules':sorted(modules-{r['module'] for r in rows}),'by_lane':{lane:{'modules':len(names),'declarations':sum(r['module'] in names for r in rows),'theorems':sum(r['module'] in names and r['theorem'] for r in rows),'excluded_nonproof':sum(r['module'] in names for r in exclusions)} for lane,names in lanes.items()}}
