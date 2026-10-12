#!/usr/bin/env python3
"""Offline source-archive and candidate-public-projection integrity (no execution of archive code)."""
from pathlib import Path
import hashlib,json,sys,zipfile
ROOT=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def main():
 idx=json.loads((ROOT/'inventory/ALL_MEMBERS.json').read_text());p=json.loads((ROOT/'inventory/PUBLIC_PROJECTION.json').read_text());archives=json.loads((ROOT/'inventory/CHECKPOINT_ARCHIVES.json').read_text())
 archive_data={}
 for e in archives:
  ap=ROOT/e['private_archive_path']; b=ap.read_bytes(); assert sha(b)==e['sha256'] and len(b)==e['bytes'],e['id'];z=zipfile.ZipFile(ap);assert z.testzip() is None
  archive_data[e['id']]=z
  assert sum(not x.is_dir() for x in z.infolist())==e['members'],e['id']
 for e in idx:
  bb=archive_data[e['checkpoint_id']].read(e['archive_member'])
  assert sha(bb)==e['original_sha256'] and len(bb)==e['original_bytes'],e['archive_member']
  if e.get('public_sha256'):
   q=(ROOT/'PUBLIC_OVERLAY'/e['repo_path']);v=q.read_bytes()
   assert sha(v)==e['public_sha256'] and len(v)==e['public_bytes'],e['repo_path']
   if e['projection']=='exact':assert v==bb,e['repo_path']
   elif e['projection']=='machine_locator_redacted':
    assert b'[OMITTED_PRIVATE_MACHINE_PATH]' in v,e['repo_path']
 for e in p['published']:
  assert sha((ROOT/'PUBLIC_OVERLAY'/e['repo_path']).read_bytes())==e['public_sha256'],e['repo_path']
 print('PASS: '+str(len(archives))+' archives, '+str(len(idx))+' member bytes, '+str(len(p['published']))+' published candidate files verified (source copies and projections)')
if __name__=='__main__':
 try:main()
 except Exception as ex:print('FAIL:',ex,file=sys.stderr);sys.exit(2)
