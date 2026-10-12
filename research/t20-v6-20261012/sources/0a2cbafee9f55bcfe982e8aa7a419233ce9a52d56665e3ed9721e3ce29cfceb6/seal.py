#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,zipfile,datetime
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
assert json.loads((R/'RESULT.json').read_text())['status']=='PASS_SCOPED'
files=[]
for p in sorted(R.rglob('*')):
 if not p.is_file():continue
 rel=p.relative_to(R)
 if rel.parts[0]=='build' or '__pycache__' in rel.parts or p.suffix in {'.olean','.ilean','.zip','.pyc'} or str(rel) in {'MANIFEST.json','DELIVERY_SEAL.json'}:continue
 files.append({'path':str(rel),'bytes':p.stat().st_size,'sha256':sha(p)})
manifest={'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'scope':'Geometry boundary delta independent audit portable files. Builds, bytecode, archive, delivery seal and this manifest excluded.','files':files}
(R/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
archive=R/'Geometry_Boundary_Delta_Audit_20261001.zip'
with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for row in files:z.write(R/row['path'],row['path'])
 z.write(R/'MANIFEST.json','MANIFEST.json')
with zipfile.ZipFile(archive) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(files)+1
 for row in files:
  data=z.read(row['path']);assert len(data)==row['bytes'];assert hashlib.sha256(data).hexdigest()==row['sha256']
seal={'status':'PASS_SCOPED','sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive':archive.name,'archive_bytes':archive.stat().st_size,'archive_sha256':sha(archive),'manifest_sha256':sha(R/'MANIFEST.json'),'result_sha256':sha(R/'RESULT.json'),'portable_file_count':len(files),'zip_crc':'PASS','manifest_archive_reopen':'PASS'}
(R/'DELIVERY_SEAL.json').write_text(json.dumps(seal,indent=2)+'\n');print(json.dumps(seal,indent=2))
