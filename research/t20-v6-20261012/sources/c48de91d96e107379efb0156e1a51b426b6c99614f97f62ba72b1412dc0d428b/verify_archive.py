from pathlib import Path,PurePosixPath
import json,hashlib,zipfile
R=Path(__file__).resolve().parent;F=Path('private-locator:4895465318e5977e697d');H=lambda b:hashlib.sha256(b).hexdigest()
p=F/'P01_Raw_Index_Dependent_Successor_2026-09-30.zip';digest=H(p.read_bytes());assert digest=='dec5951de21c2ef0918f9eb6da130907e4dba4df213dd84ef04209aa251840cc'
j=json.loads((R/'RESULT.json').read_text())
with zipfile.ZipFile(p) as z:
 names=z.namelist();assert len(names)==len(set(names))==178
 assert all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n for n in names)
 manifest=z.read('RESULT_MANIFEST.json');assert H(manifest)=='fe87d7e9a9dcf2e0d06c285f5e46fa3bc286de18094b988d04ce327ff1a4eec0';m=json.loads(manifest)
 assert len(m['files'])==len({x['path'] for x in m['files']})
 assert set(names)=={x['path'] for x in m['files']}|{'RESULT_MANIFEST.json'}
 for row in m['files']:
  b=z.read(row['path']);assert len(b)==row['bytes'] and H(b)==row['sha256'],row['path'];assert H((F/row['path']).read_bytes())==row['sha256'],row['path']
 assert H(z.read('qualification-final/QUALIFICATION.json'))=='adfb079b27c5d918e561fa688eb52ca4906a38d7ce703d1e301e5646b84bc29e'
 for name,row in j['sources'].items():
  assert H(z.read('qualification-final/sources/'+name+'.lean'))==row['sha256'],name
  if name in j['main_modules']:assert H(z.read('sources/'+name+'.lean'))==row['sha256'],name
out={'status':'PASS','archive_path':str(p),'archive_sha256':digest,'bytes':p.stat().st_size,'member_count':len(names),'manifest_bound_payload_members':len(m['files']),'manifest_sha256':H(manifest),'qualification_receipt_sha256':m['authoritative_receipt_sha256'],'all_payload_hashes_match':True,'all_current_author_payloads_match':True,'fresh_audit_sources_match_sealed_sources':True,'member_paths_safe_and_unique':True}
(R/'ARCHIVE_IDENTITY.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
