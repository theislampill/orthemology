#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,zipfile,datetime
R=Path(__file__).resolve().parent
H=lambda b:hashlib.sha256(b).hexdigest()
qpath=R/'qualification-final/QUALIFICATION.json';q=json.loads(qpath.read_text())
assert q['kernel_credit'] and q['target_count']==19 and q['theorem_declaration_count']==16
assert q['driver_sha256']==H((R/'qualify.py').read_bytes())
frozen=json.loads((R/'FROZEN_SOURCE_HASHES.json').read_text())
for name,hash in frozen.items():
 assert H((R/'sources'/name).read_bytes())==hash==q['source_bindings'][Path(name).stem]['sha256']
selected=set()
for name in ['RESULTS.md','REPLAY.md','FROZEN_SOURCE_HASHES.json','qualify.py','seal.py']:
 selected.add(Path(name))
for name in ['sources','handoff','qualification-final']:
 for p in (R/name).rglob('*'):
  if p.is_file() and '__pycache__' not in p.parts:selected.add(p.relative_to(R))
rows=[{'path':str(p),'bytes':(R/p).stat().st_size,'sha256':H((R/p).read_bytes())} for p in sorted(selected)]
manifest={'schema':'p01-canonical-carrier-projection-seal-v1','sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'authoritative_receipt':'qualification-final/QUALIFICATION.json','authoritative_receipt_sha256':H(qpath.read_bytes()),'target_count':19,'theorem_declaration_count':16,'main_module_count':1,'fresh_module_count_before_audit':30,'canonical_commit':q['canonical_commit'],'successor_archive_sha256':q['successor_archive_sha256'],'canonical_adoption':False,'full_U11_closure':False,'arbitrary_heterogeneous_index_transport':False,'canonical_carrier_squares':['raw-index Pi','represented Sigma','raw identity'],'full_recursive_canonical_equality':False,'dependent_predecessor_archive_sha256':q['dependent_archive_sha256'],'novelty_claim':False,'files':rows}
mp=R/'RESULT_MANIFEST.json';mp.write_text(json.dumps(manifest,indent=2)+'\n')
zp=R/'P01_Canonical_Carrier_Projection_2026-09-30.zip';assert not zp.exists()
with zipfile.ZipFile(zp,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(selected):z.write(R/p,str(p))
 z.write(mp,mp.name)
with zipfile.ZipFile(zp) as z:
 assert z.testzip() is None
 assert len(z.namelist())==len(set(z.namelist()))==len(rows)+1
 assert set(z.namelist())=={str(p) for p in selected}|{mp.name}
 for row in rows:
  b=z.read(row['path']);assert len(b)==row['bytes'] and H(b)==row['sha256']
result={'archive':str(zp),'sha256':H(zp.read_bytes()),'bytes':zp.stat().st_size,'members':len(rows)+1,'receipt_sha256':H(qpath.read_bytes()),'manifest_sha256':H(mp.read_bytes())}
zp.with_suffix('.zip.sha256').write_text(result['sha256']+'  '+zp.name+'\n')
(R/'SEALED_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
