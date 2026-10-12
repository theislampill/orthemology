"""Fresh source/selector checks. Does not replay any predecessor engineering."""
import hashlib,json,re,yaml
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT.parent/'p02_predecessor/inputs/packet'
def ident(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
rows=[]
for o in json.loads((P/'OBLIGATIONS.json').read_text()):
 p=P/'source-main'/o['source_locator'];text=p.read_text()
 data=yaml.safe_load(text) if p.suffix=='.yaml' else json.loads(text)
 collection=o['source_selector'].split('[')[0]
 matches=[v for v in data[collection] if v['id']==o['id']]
 if len(matches)!=1 or matches[0]!=o['exact_source_record']:raise ValueError('Selector mismatch '+o['id'])
 rows.append({'id':o['id'],'selector':o['source_selector'],'path':str(p.relative_to(P)),**ident(p),'exact_record_equal':True})
sources=[]
for e in json.loads((P/'SOURCE_INVENTORY.json').read_text()):
 p=P/e['packet_path'];b=p.read_bytes();assert ident(p)=={k:e[k] for k in ('bytes','sha256')}
 blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();assert blob==e['git_blob']
 sources.append({**e,'git_blob_verified':True})
projections=[]
for e in json.loads((P/'EVIDENCE_REUSE_MAP.json').read_text())['source_bindings']:
 p=P/e['packet_path'];assert ident(p)=={k:e[k] for k in ('bytes','sha256')}
 projections.append({**e,'projection_verified':True,'full_origin_archive_recovered':False})
(ROOT/'provenance/SOURCE_AND_SELECTOR_READBACK.json').write_text(json.dumps({'status':'PASS','selectors':rows,'sources':sources,'accepted_projections':projections},indent=2))
for name in ['FINAL_MAIN_IDENTITY.json','FORMAL_TOOLCHAIN_STATE.json','DEPENDENCY_DAG.json']:
 (ROOT/'provenance'/('INHERITED_'+name)).write_bytes((P/name).read_bytes())
print(json.dumps({'selectors':len(rows),'source_sha_and_git_blob':len(sources),'accepted_projections':len(projections),'status':'PASS'}))
