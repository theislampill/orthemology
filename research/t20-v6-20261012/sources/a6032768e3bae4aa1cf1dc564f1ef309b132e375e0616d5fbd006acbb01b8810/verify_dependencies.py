from pathlib import Path
import json,hashlib,re,subprocess,os
R=Path(__file__).resolve().parent; W=R.parent; S=R/'candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((S/'IMPORTED_OBJECT_MANIFEST.json').read_text()); external=[]; local=[]
for row in manifest:
    path=Path(row['object_path'])
    if row['module'] in ['TruncatedMoment','ScalarPositivity','DegreeBridge','Certificate','Controls','MomentValues','Verify']:
        local.append(row['module']);continue
    assert path.is_file(),row
    assert sha(path)==row['object_sha256'],row
    if 'source_path' in row:assert sha(Path(row['source_path']))==row['source_sha256'],row
    external.append(row['module'])
assert len(external)+len(local)==2454 and len(local)==7
record={'status':'PASS','total_manifest_entries':len(manifest),'retained_dependency_objects_and_sources_verified':len(external),'production_objects_rebuilt_separately':local,'source_unavailable':[row['module'] for row in manifest if row.get('source_unavailable')]}
(R/'evidence/dependency-integrity.json').write_text(json.dumps(record,indent=2)+'\n'); print(json.dumps(record,indent=2))
