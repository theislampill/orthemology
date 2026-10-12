"""Independent fresh-process ZIP/receipt/manifest and nested predecessor readback.
Usage: python independent_reopen.py ARCHIVE.zip ARCHIVE.SEAL.json OUTPUT.VERIFICATION.json
Does not trust the extracted author workspace and does not mutate any archive.
"""
from pathlib import Path,PurePosixPath
import json,zipfile,hashlib,io,sys,datetime,platform
import jsonschema
EXPECTED='365d6e27c953102aba2f1749286ff731e0b1b50bf15c2a4cc9ed576eeb02bfc9'
def sha(b):return hashlib.sha256(b).hexdigest()
checks=[];member_rows=[]
def ck(x,label):
 checks.append({'check':label,'pass':bool(x)})
 if not x:raise ValueError(label)
def validzip(z,label):
 names=z.namelist();ck(len(names)==len(set(names)),label+': no duplicate names')
 ck(all(not PurePosixPath(n).is_absolute() and '..' not in PurePosixPath(n).parts and '\\' not in n and not n.endswith('/') for n in names),label+': safe relative file paths')
 ck(z.testzip() is None,label+': all CRCs')
 return names
def j(z,n):return json.loads(z.read(n))
def hashrows(z,rows,label,record=False):
 for e in rows:
  b=z.read(e['path']);v=len(b)==e['bytes'] and sha(b)==e['sha256'];ck(v,label+': '+e['path'])
  if record:member_rows.append({'path':e['path'],'bytes':len(b),'sha256':sha(b),'verified':v})
def checkpayload(z,label):
 names=validzip(z,label);m=j(z,'CHECKPOINT_MANIFEST.json')
 listed=[x['path'] for x in m['files']]
 ck(len(listed)==len(set(listed)),label+': manifest names unique')
 ck(set(listed)|{'CHECKPOINT_MANIFEST.json'}==set(names) and 'CHECKPOINT_MANIFEST.json' not in listed,label+': manifest exact coverage')
 hashrows(z,m['files'],label+' manifest',label=='outer')
 rec=j(z,'RECEIPT.json');jsonschema.validate(rec,j(z,'RECEIPT.schema.json'));ck(True,label+': receipt schema')
 ck(sha(z.read('RECEIPT.json'))==z.read('RECEIPT.json.sha256').decode().split()[0],label+': receipt detached digest')
 outs=rec['output_hashes'];ck(len({x['path'] for x in outs})==len(outs),label+': receipt names unique')
 ck({x['path'] for x in outs}==set(names)-{'RECEIPT.json','RECEIPT.json.sha256','CHECKPOINT_MANIFEST.json'},label+': receipt output coverage')
 hashrows(z,outs,label+' receipt')
 return rec
archive,sealpath,outpath=map(Path,sys.argv[1:]);data=archive.read_bytes();seal=json.loads(sealpath.read_text())
ck(archive.name==seal['archive'],'Archive filename')
ck(len(data)==seal['bytes'] and sha(data)==seal['sha256'],'Outer SHA-256 and bytes')
ck(archive.with_suffix('.zip.sha256').read_text().split()[0]==sha(data),'Outer detached SHA-256')
with zipfile.ZipFile(io.BytesIO(data)) as z:
 ck(len(z.infolist())==seal['zip_members'],'Outer member count')
 ck(sum(x.file_size for x in z.infolist())==seal['uncompressed_bytes'],'Outer uncompressed byte count')
 rec=checkpayload(z,'outer');hashrows(z,[seal['manifest'],seal['receipt']],'Detached seal')
 m=seal['manifest'];member_rows.append({'path':m['path'],'bytes':len(z.read(m['path'])),'sha256':sha(z.read(m['path'])),'verified':True})
 ck(len(member_rows)==seal['zip_members'],'Every outer ZIP member hash verified, including manifest')
 b=z.read(rec['input_predecessor']['path']);ck(len(b)==4192393 and sha(b)==EXPECTED,'Predecessor exact frozen identity')
 with zipfile.ZipFile(io.BytesIO(b)) as pred:
  ck(len(pred.infolist())==693,'Predecessor member count');checkpayload(pred,'predecessor')
  nested=pred.read('inputs/Orthemology_Pro_P02_Measure_CV_R_C.zip')
  ck(sha(nested)=='70630d5b703fb3262e123b8424c19580e95bf604db3e9eb5d364653c333fdf13','Original packet SHA-256')
  with zipfile.ZipFile(io.BytesIO(nested)) as packet:
   ck(len(packet.infolist())==620,'Original packet member count');checkpayload(packet,'original packet')
   for name in packet.namelist():ck(packet.read(name)==pred.read('inputs/packet/'+name),'Exact embedded source/evidence copy: '+name)
   obs=j(packet,'OBLIGATIONS.json');ck(json.loads(z.read('provenance/ORIGINAL_OBLIGATIONS.json'))==obs,'Unchanged assigned obligation records')
   for o in obs:
    for e in o['source_bindings']:
     raw=packet.read(e['packet_path']);ck(len(raw)==e['bytes'] and sha(raw)==e['sha256'],'Assigned input binding: '+e['packet_path'])
     ck(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==e['git_blob'],'Assigned Git blob: '+e['packet_path'])
  # Unchanged predecessor Lean sources are actually identical, not simply same-labelled.
  for name in ['MeasureCore.lean','T300ThreeBit.lean']:
   old=pred.read('proposals/lean/P02/'+name)
   ck(z.read('formal/Predecessor/P02/'+name)==old,'Unchanged original Lean candidate: '+name)
 inv=j(z,'provenance/FORMAL_INVENTORY.json')
 for t in inv['theorems']:ck(sha(z.read(t['source']))==t['source_sha256'],'Final candidate source binding: '+t['declaration'])
 cat=j(z,'NEW_RESULT_CATALOGUE.json')['result_sections'];resultids={x['id']:x for x in cat}
 for s in cat:
  ck(sha(z.read(s['proof_file']))==s['proof_file_sha256'],'Final ordinary proof file: '+s['id'])
  ck(sha(s['exact_section'].encode())==s['section_sha256'] and s['exact_section'] in z.read(s['proof_file']).decode(),'Final exact ordinary section: '+s['id'])
 for s in j(z,'P03_CONSUMER_BINDINGS.json')['bindings']:
  ck(s['id'] in resultids and s['section_sha256']==resultids[s['id']]['section_sha256'] and not s['kernel_verified'],'Final P03 evidence-level binding: '+s['id'])
 ck(rec['full_exhaustion_certified'] is False and rec['kernel_verified'] is False,'No unsupported completion/kernel promotion')
report={'status':'PASS','verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'verifier_python':platform.python_version(),'verifier_source_sha256':sha(Path(__file__).read_bytes()),
 'archive':str(archive),'bytes':len(data),'sha256':sha(data),'zip_members':seal['zip_members'],'uncompressed_bytes':seal['uncompressed_bytes'],
 'outer_member_hashes_verified':len(member_rows),'nested_predecessor_members':693,'original_input_members':620,
 'check_count':len(checks),'all_checks_passed':all(x['pass'] for x in checks),'member_hashes':sorted(member_rows,key=lambda x:x['path']),'checks':checks,
 'scope':'Independent fresh-process custody and consistency readback; not independent mathematical review or Lean execution.'}
outpath.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
print(json.dumps({k:v for k,v in report.items() if k not in ('member_hashes','checks')},indent=2))
