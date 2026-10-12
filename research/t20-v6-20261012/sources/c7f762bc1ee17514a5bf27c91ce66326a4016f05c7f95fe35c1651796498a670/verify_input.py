#!/usr/bin/env python3
"""Read-only verification of the supplied P01 preparation packet."""
import argparse,hashlib,json,stat,sys,zipfile
from pathlib import Path,PurePosixPath

def H(b):return hashlib.sha256(b).hexdigest()
def verify(path,extracted=None):
 b=Path(path).read_bytes();err=[];counts={}
 result={'input_filename':Path(path).name,'input_bytes':len(b),'input_sha256':H(b),'identity_kind':'OBSERVED_ATTACHMENT_IDENTITY_RECHECKED_AGAINST_INITIAL_LOCAL_DIGEST','live_remote_check':False,'full_repository_tree_recomputed':False}
 if H(b)!='e4e89e99bd35326e342761d080a9506c8d2b90780fb0a50c6736343ff172ed4c':err.append('attachment digest mismatch')
 with zipfile.ZipFile(path) as z:
  ns=z.namelist()
  if len(ns)!=len(set(ns)):err.append('duplicate ZIP names')
  for i in z.infolist():
   p=PurePosixPath(i.filename)
   if p.is_absolute() or '..' in p.parts or stat.S_ISLNK(i.external_attr>>16):err.append('unsafe member: '+i.filename)
  crc=z.testzip()
  if crc:err.append('CRC: '+crc)
  result.update(zip_members=len(ns),uncompressed_bytes=sum(i.file_size for i in z.infolist()),crc_status='PASS' if crc is None else 'FAIL')
  allhash=[]
  for name in ns:
   if name.endswith('/'):continue
   raw=z.read(name);allhash.append({'path':name,'bytes':len(raw),'sha256':H(raw)})
   if extracted is not None:
    q=Path(extracted)/name
    if not q.is_file() or q.read_bytes()!=raw:err.append('extracted preimage changed: '+name)
  for label,keyfield,array in [
   ('manifest','path',json.loads(z.read('CHECKPOINT_MANIFEST.json'))['files']),
   ('receipt','path',json.loads(z.read('RECEIPT.json'))['output_hashes']),
   ('source','packet_path',json.loads(z.read('SOURCE_INVENTORY.json'))),
   ('evidence_projection','packet_path',json.loads(z.read('accepted-evidence/PROJECTION_BINDINGS.json')))]:
   good=0
   for r in array:
    raw=z.read(r[keyfield]);ok=len(raw)==r['bytes'] and H(raw)==r['sha256']
    if label=='source':
     blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
     ok=ok and blob==r['git_blob'] and r['main_commit']=='03e2604dfcef278b01c60d19b05370fcec4194b6'
    if ok:good+=1
    else:err.append(label+': '+r[keyfield])
   counts[label]={'expected':len(array),'verified':good}
  declared={r['path'] for r in json.loads(z.read('CHECKPOINT_MANIFEST.json'))['files']}
  if declared!=set(ns)-{'CHECKPOINT_MANIFEST.json'}:err.append('manifest coverage mismatch')
  if z.read('RECEIPT.json.sha256').decode().split()[0]!=H(z.read('RECEIPT.json')):err.append('receipt detached digest')
  final=json.loads(z.read('FINAL_MAIN_IDENTITY.json'))
  if final['main_commit']!='03e2604dfcef278b01c60d19b05370fcec4194b6' or final['main_tree']!='3d06e80277ce39286c94307e0f14b215bc94ed83' or final['PR_state']!='MERGED' or final['PR']!=28 or final['remaining_integration_cells']!=[]:err.append('canonical pin mismatch')
  result.update(counts=counts,canonical_pin=final,all_member_identities=allhash,errors=err,status='PASS' if not err else 'FAIL',extracted_tree_compared=extracted is not None)
 return result
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('packet',type=Path);p.add_argument('--extracted',type=Path);a=p.parse_args();r=verify(a.packet,a.extracted);print(json.dumps(r,indent=2));sys.exit(0 if r['status']=='PASS' else 1)
