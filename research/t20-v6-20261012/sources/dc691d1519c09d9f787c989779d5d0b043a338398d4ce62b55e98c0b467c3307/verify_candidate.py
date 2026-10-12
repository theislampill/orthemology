#!/usr/bin/env python3
"""Independent frozen-candidate binding/delta check. Writes reviewer receipts only."""
import hashlib,json,datetime,sys
from pathlib import Path
R=Path(__file__).resolve().parents[2];D=Path(__file__).resolve().parent
P=R/'t20-consolidation-20261011/projection/package-v3'
V=R/'t20-consolidation-20261011/projection/package-v2'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):
 def pairs(xs):
  d={}
  for k,v in xs:
   if k in d:raise ValueError('duplicate JSON key: '+k)
   d[k]=v
  return d
 return json.loads(p.read_text(),object_pairs_hook=pairs)
errors=[]; checks=[]
def require(label,ok,detail=None):
 checks.append({'label':label,'pass':bool(ok),'detail':detail})
 if not ok:errors.append(checks[-1])
def tree(p):
 files={}
 for x in p.rglob('*'):
  require('no symlink '+str(x.relative_to(p)),not x.is_symlink())
  if x.is_file():files[str(x.relative_to(p))]={'sha256':h(x),'bytes':x.stat().st_size}
 return files
old=read(D/'V2_BASELINE_CHECK.json')['files'];a=tree(V);b=tree(P)
require('v2 all bytes unchanged since independent baseline',a==old)
m=read(P/'PACKAGE_CONTENTS.json');exp={x['path']:{'sha256':x['sha256'],'bytes':x['bytes']} for x in m['files']}
require('manifest unique paths',len(exp)==len(m['files']))
require('manifest exact member set',set(exp)|{'PACKAGE_CONTENTS.json'}==set(b))
for r,s in exp.items():require('manifest binding '+r,b.get(r)==s)
removed=sorted(set(a)-set(b));added=sorted(set(b)-set(a));changed=sorted(r for r in set(a)&set(b) if a[r]!=b[r])
require('v2 files not removed',not removed)
projection=read(P/'PUBLIC_PROJECTION.json');rows=projection['files'];prior=read(V/'PUBLIC_PROJECTION.json')['files']
identities={x['original_sha256']:x for x in rows};require('unique source identities',len(rows)==len(identities))
for row in rows:
 if row['disposition']=='included':require('projected source '+row['public_path'],b.get(row['public_path'])=={'sha256':row['public_sha256'],'bytes':row['public_bytes']})
 elif row['disposition']=='pinned_existing_public_source':require('pinned inherited source',row['public_url'].startswith(projection['repository']['pinned_blob_prefix']))
 else:require('known disposition',False,row['disposition'])
 if row['projection']=='EXACT':require('exact binding original/public match '+row['original_sha256'],row['original_sha256']==row['public_sha256'] and row['original_bytes']==row['public_bytes'])
 else:require('nonexact transformation disclosed '+row['original_sha256'],bool(row.get('transformations')))
 for copy in row.get('required_replay_copies',[]):require('extra replay copy '+copy['path'],b.get(copy['path'])=={'sha256':copy['sha256'],'bytes':copy['bytes']})
for row in prior:
 cur=identities.get(row['original_sha256']);require('prior source identity retained '+row['original_sha256'],cur is not None)
 if cur:
  for k in ['original_sha256','original_bytes','disposition','projection','public_path','public_url','public_sha256','public_bytes']:
   if k in row:require('prior source field unchanged '+row['original_sha256']+' '+k,cur.get(k)==row[k])
for rel in ['reassessment/SOURCE_OWNERS.json','reassessment/audit_symmetries/SOURCE_BINDINGS.json','reassessment/foundational_interface/SOURCE_BINDINGS.json','reassessment/independent_review/SOURCE_BINDINGS.json','reassessment/contract_repair/SOURCE_BINDINGS.json']:
 j=read(P/rel)
 for row in j.get('sources',[]):
  q=row.get('public_source')
  if not q:continue
  if q.startswith('https://'):require('source owner pinned URL '+q,q.startswith(projection['repository']['pinned_blob_prefix']));continue
  require('local source owner '+q,b.get(q)=={'sha256':row['public_sha256'],'bytes':row['public_bytes']},rel)
for row in read(P/'reassessment/independent_review/PORTABLE_REVIEW_BINDINGS.json')['targets']:
 require('portable review target '+row['public_target'],b.get(row['public_target'])=={'sha256':row['public_sha256'],'bytes':row['public_bytes']})
claims=read(P/'CLAIM_REGISTER.json');oldclaims=read(V/'CLAIM_REGISTER.json');require('137 typed claim entries',claims['claim_count']==137 and len(claims['claims'])==137)
for row in oldclaims['claims']:require('inherited claim record retained '+str(row.get('id',row.get('claim_id'))),row in claims['claims'])
for rel in ['DEPENDENCY_INDEX.json','CORRECTION_INDEX.json','CROSS_FRONT_INTERFACES.json']:
 key={'DEPENDENCY_INDEX.json':'edges','CORRECTION_INDEX.json':'corrections','CROSS_FRONT_INTERFACES.json':'interfaces'}[rel]
 new=read(P/rel)[key];priorlist=read(V/rel)[key]
 require('inherited '+rel+' records preserved',all(x in new for x in priorlist))
for row in read(P/'reassessment/CLAIMS.json')['claims']:
 own=row['source_owner'];require('new claim source '+row['id'],b[own['path']]['sha256']==own['sha256'])
for rel in ['OWNER_ASSESSMENT.md','COMBINED_RESEARCH_SYNTHESIS.md','audit_symmetries/RESULT.md','restricted_controls/RESULT.md','foundational_interface/RESULT.md','independent_review/REVIEW.md']:
 require('exact new narrative/proof '+rel,h(P/'reassessment'/rel)==h(R/'t20-depth-reassessment-20261011'/rel))
for rel in ['foundations/FOUNDATIONAL_SYNTHESIS.md','geometry/GEOMETRY_MOMENTS_SYNTHESIS.md','evidence/EVIDENCE_TRANSPORT_SYNTHESIS.md','MATHEMATICAL_SYNTHESIS.md','FOUNDATIONAL_CROSSWALK.md','FIELD_GUIDE.md']:
 before=(V/rel).read_text();after=(P/rel).read_text();tail=before.split('\n',1)[1];require('entire old reader body preserved after qualification header '+rel,tail in after)
for row in read(P/'READER_PROJECTION.json').get('v3_reader_files',[]):
 require('v3 reader current binding '+row['path'],b[row['path']]['sha256']==row['v3_sha256'])
 require('v2 reader historical binding '+row['path'],a[row['path']]['sha256']==row['v2_sha256'])
for run in read(P/'REASSESSMENT_REPLAY_VERIFICATION.json')['runs']:
 for row in run['suite_sources']:
  require('builder replay source current '+row['path'],b[row['path']]=={'sha256':row['sha256'],'bytes':row['bytes']})
delta=read(P/'reassessment/V2_TO_V3_DIFF.json')
excluded={'PACKAGE_CONTENTS.json','reassessment/V2_TO_V3_DIFF.json','reassessment/V2_TO_V3.patch'}
require('delta added accounting',set(x['path'] for x in delta['added'])==set(added)-excluded)
require('delta changed accounting',set(x['path'] for x in delta['changed'])==set(changed)-excluded)
require('delta removed accounting',delta['removed']==removed)
for row in delta['added']:require('delta new binding '+row['path'],b[row['path']]=={'sha256':row['sha256'],'bytes':row['bytes']})
for row in delta['changed']:
 require('delta old binding '+row['path'],a[row['path']]=={'sha256':row['v2_sha256'],'bytes':row['v2_bytes']})
 require('delta current binding '+row['path'],b[row['path']]=={'sha256':row['v3_sha256'],'bytes':row['v3_bytes']})
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if not errors else 'FAIL','manifest_sha256':h(P/'PACKAGE_CONTENTS.json'),'candidate_files':len(b),'candidate_bytes':sum(x['bytes'] for x in b.values()),'baseline_files':len(a),'unchanged_files':len(a)-len(changed)-len(removed),'added_files':added,'changed_files':changed,'removed_files':removed,'source_identities':len(rows),'included_identities':sum(x['disposition']=='included' for x in rows),'pinned_identities':sum(x['disposition']=='pinned_existing_public_source' for x in rows),'additional_replay_copies':sum(len(x.get('required_replay_copies',[])) for x in rows),'new_identity_count':len(rows)-len(prior),'checks':len(checks),'errors':errors,'scope':'Frozen-candidate byte/semantic-index qualification; no acceptance or scientific closure.'}
(D/'CANDIDATE_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');(D/'BINDING_CHECKS.json').write_text(json.dumps(checks,indent=2)+'\n');(D/'CANDIDATE_FILES.json').write_text(json.dumps(b,indent=2)+'\n')
print(json.dumps(result,indent=2));sys.exit(bool(errors))
