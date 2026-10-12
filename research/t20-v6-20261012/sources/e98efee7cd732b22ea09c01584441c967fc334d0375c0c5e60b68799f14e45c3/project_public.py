#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,re,os,subprocess
B=Path(__file__).resolve().parents[2];P=B/'projection/package';W=B.parent
sha=lambda raw:hashlib.sha256(raw).hexdigest()
manifest=json.loads((P/'PUBLIC_PROJECTION.json').read_text());rows=manifest['files'];byhash={r['original_sha256']:r for r in rows}
MACHINE=re.compile(r'/(?:workspace/|mnt/data/|Users/|home/[^/\s]+/|root/)[^\s`"\'<>]*')
LINK=re.compile(r'\[([^\]\n]+)\]\(([^)\s]+)\)')
changes=[]

def public_location(row):return row.get('public_path',row.get('public_url'))
def source_text_transform(text,path):
 edits=[]
 text,n=MACHINE.subn('[OMITTED_PRIVATE_MACHINE_PATH]',text)
 if n:edits.append({'kind':'private_machine_locator_omission','count':n,'effect':'Original byte hash retained; machine-specific invocation is not a portable command.'})
 if path.suffix=='.md':
  replacements=[]
  def link(m):
   label,target=m.groups()
   if target.startswith(('http://','https://','mailto:','#')):return m.group(0)
   clean=target.split('#',1)[0]
   if (path.parent/clean).exists():return m.group(0)
   replacements.append({'label':label,'original_member_locator':target.replace('/',' / ')})
   return label+' (original packet locator: '+target.replace('/',' / ')+', not a link in this projection)'
  text=LINK.sub(link,text)
  if replacements:edits.append({'kind':'unresolved_original_packet_links_qualified_as_text','replacements':replacements})
 return text,edits

# Scope-correct portable grouped author control: bind supplied original-byte snapshots,
# not a fictional surviving original workspace. Mathematical controls are unchanged.
group_script='replay/grouped-source-audit-gradient-20261011/check_exact.py'
for r in rows:
 if r['disposition']!='included':continue
 paths=[r['public_path']]+[x['path'] for x in r.get('required_replay_copies',[])]
 for rel in paths:
  path=P/rel;raw=path.read_bytes();text=raw.decode('utf-8');out,edits=source_text_transform(text,path)
  if path.name=='check_exact.py' and r['original_sha256']==sha((W/'grouped-source-audit-gradient-20261011/check_exact.py').read_bytes()):
   out=out.replace('for path in (HERE / entry["copy"], ROOT / entry["source"]):','for path in (HERE / entry["copy"],):').replace('record("copied and unchanged original input hashes", 2 * len(bindings))','record("included original-byte input snapshot hashes", len(bindings))')
   edits.append({'kind':'portable_snapshot_binding_scope','effect':'Hash only included original-byte snapshots; remove duplicate check of unavailable original workspace. No mathematical calculation changed.'})
  if out!=text:
   path.write_text(out,encoding='utf-8');changes.append({'path':rel,'original_sha256':r['original_sha256'],'public_sha256':sha(path.read_bytes()),'transformations':edits})
   if rel==r['public_path']:
    r.update(public_sha256=sha(path.read_bytes()),public_bytes=path.stat().st_size,projection='AMENDED',transformations=edits)
   else:
    copy=next(c for c in r['required_replay_copies'] if c['path']==rel);copy.update(sha256=sha(path.read_bytes()),bytes=path.stat().st_size,transformations=edits)
# Add exact grouped input snapshots and a fresh minimal binding table; originals remain bound.
original=json.loads((W/'grouped-source-audit-gradient-20261011/INPUT_BINDINGS.json').read_text())
for folder in ['replay/grouped-source-audit-gradient-20261011','source-suites/grouped-source-audit-gradient-20261011']:
 if not (P/folder).exists():continue
 bindings=[]
 for item in original:
  rel=folder+'/'+item['copy'];dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True);raw=(W/'grouped-source-audit-gradient-20261011'/item['copy']).read_bytes();assert sha(raw)==item['sha256'];dest.write_bytes(raw)
  # Input reports intentionally exact; unchanged mathematical source bytes and original hash.
  r=byhash[item['sha256']]
  r.setdefault('required_replay_copies',[]).append({'path':rel,'sha256':sha(raw),'bytes':len(raw),'reason':'Exact original-byte snapshot required by scoped grouped control.'})
  bindings.append({k:item[k] for k in ['copy','sha256','bytes']})
 (P/folder/'INPUT_BINDINGS.json').write_text(json.dumps(bindings,indent=2)+'\n')
# Metadata names are original packet members, not root-relative repo citations.
for fn in ['FAMILY_DISPOSITIONS.json']:
 p=P/fn;d=json.loads(p.read_text())
 def qualify(x):
  if isinstance(x,dict):return {k:(v.replace('/',' / ') if k=='member' and isinstance(v,str) else qualify(v)) for k,v in x.items()}
  if isinstance(x,list):return [qualify(z) for z in x]
  return x
 p.write_text(json.dumps(qualify(d),indent=2)+'\n')
(P/'PUBLIC_PROJECTION.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
(P/'PUBLIC_TRANSFORMATIONS.json').write_text(json.dumps({'scope':'Bounded public-copy transformations only; original custody bytes remain unchanged. No proof source semantics intentionally changed.','records':changes,'manual_privacy_clearance':[{'original_sha256':'dda057694b1deab9f08d815e58cb04259dd89180e34317a032438b997ee0dd95','finding':'Contact regex false positive on NumPy matrix multiplication expression; exact source retained.'}]},indent=2)+'\n')
# Public reader: strip custody locator arrays, bind every known source to original+public identities.
reader_paths=['CONSOLIDATION_CONTRACT.md','OWNER_REVIEW_CASE.md','README_FIRST.md','FIELD_GUIDE.md','MATHEMATICAL_SYNTHESIS.md','FOUNDATIONAL_CROSSWALK.md','T21_CHARTER.md','EVIDENCE_GUIDE.md',
 'foundations/FOUNDATIONAL_SYNTHESIS.md','geometry/GEOMETRY_MOMENTS_SYNTHESIS.md','proofs/PROOF_TYPE_INQUIRY_SYNTHESIS.md','evidence/EVIDENCE_TRANSPORT_SYNTHESIS.md',
 'foundations/FOUNDATIONAL_CLAIMS.json','geometry/GEOMETRY_MOMENTS_CLAIMS.json','proofs/PROOF_TYPE_INQUIRY_CLAIMS.json','evidence/MATERIAL_CLAIMS.json',
 'evidence/CORRECTION_MAP.json','evidence/DEPENDENCY_EDGES.json','evidence/DEPENDENCY_EDGES_RECEIPT.json','CROSS_FRONT_INTERFACES.json','DEPENDENCY_EDGES.json','coverage/CUMULATIVE_PROGRAMME_CROSSWALK.md','coverage/CUMULATIVE_PROGRAMME_CROSSWALK.json','coverage/SELECTED_SOURCE_READS.json','coverage/COVERAGE_ALERTS.json','tools/build_consolidated_register.py']
original_to_public={}
for r in rows:
 # Build locator lookup from private catalogue, never export that lookup.
 import sqlite3
 db=sqlite3.connect(B/'catalogue/catalogue.sqlite3')
 for x in db.execute('select location from locations where sha256=?',(r['original_sha256'],)):
  original_to_public[x[0]]=public_location(r)
 original_to_public['t20-consolidation-20261011/catalogue/objects/'+r['original_sha256'][:2]+'/'+r['original_sha256']]=public_location(r)
 db.close()
private_prefix=re.compile(r'(?:recovery-20261011|t20-synthesis-owner-input-20261011|t20-consolidation-20261011/catalogue)/(?:[^\s`"<>]+)')
def rewrite_string(s):
 if s in original_to_public:return original_to_public[s]
 s=MACHINE.sub('[OMITTED_PRIVATE_MACHINE_PATH]',s)
 # Long inherited locators in prose cannot become fictional package paths.
 s=private_prefix.sub('[original custody locator omitted; use source digest binding]',s)
 return s
remove={'local_path','source_locations','original_provenance','original_read_path','canonical_byte_home','content_object'}
def rewrite(x):
 if isinstance(x,list):return [rewrite(z) for z in x]
 if isinstance(x,str):return rewrite_string(x)
 if not isinstance(x,dict):return x
 out={k:rewrite(v) for k,v in x.items() if k not in remove}
 h=x.get('sha256')
 if isinstance(h,str) and h in byhash:
  r=byhash[h]
  out['original_sha256']=h;out['sha256_scope']='original source bytes';out['public_source']=public_location(r);out['public_sha256']=r['public_sha256'];out['public_bytes']=r['public_bytes']
  for key in ['path','source_path']:
   if key in out:out[key]=public_location(r)
 return out
reader_bindings=[]
for rel in reader_paths:
 source=B/rel
 if not source.exists():continue
 raw=source.read_bytes();dest=P/rel;dest.parent.mkdir(parents=True,exist_ok=True)
 if source.suffix=='.json':out=json.dumps(rewrite(json.loads(raw)),indent=2,ensure_ascii=False)+'\n'
 else:out=rewrite_string(raw.decode())
 dest.write_text(out,encoding='utf-8')
 reader_bindings.append({'path':rel,'assembly_original_sha256':sha(raw),'public_sha256':sha(dest.read_bytes()),'original_bytes':len(raw),'public_bytes':dest.stat().st_size,'transformation':'Custody locators removed or mapped to selected source/public identities; original scientific statements preserved.'})
# Provide compact track source indexes where narrative refers to original source registers.
for track,filename in [('foundations','SOURCES_AND_READING.json'),('geometry','SOURCE_REGISTER.json'),('proofs','SOURCE_REGISTRY.json'),('evidence','SOURCE_MAP.json')]:
 selected=[{'source_ids':[x['source_id'] for x in r['owners'] if x['track']==track],'original_sha256':r['original_sha256'],'original_bytes':r['original_bytes'],'public_source':public_location(r),'public_sha256':r['public_sha256'],'public_bytes':r['public_bytes']} for r in rows if any(x['track']==track for x in r['owners'])]
 (P/track/filename).write_text(json.dumps({'scope':'Public portable source index; original private custody locators are not exported.','sources':selected},indent=2)+'\n')
subprocess.run(['python','-B',str(P/'tools/build_consolidated_register.py')],check=True)
(P/'READER_PROJECTION.json').write_text(json.dumps({'scope':'New consolidation reader projection, not historical scientific source replacement. Unified claim index regenerated over these public track bytes.','files':reader_bindings},indent=2)+'\n')
print(json.dumps({'source_transformations':len(changes),'reader_files':len(reader_bindings)}))
