#!/usr/bin/env python3
"""Verify exact preserved-byte custody. No theorem or historical campaign is rerun."""
import argparse,hashlib,json,sys
from pathlib import Path,PurePosixPath
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
def need(c,m):
 if not c:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def safe(root,name):
 r=PurePosixPath(name);need(not r.is_absolute() and '..' not in r.parts,'Unsafe path');p=root/r;need(p.resolve().is_relative_to(root.resolve()),'Escaping path');need(not any(q.is_symlink() for q in [p,*p.parents]),'Symlink path');return p
def check(p,r):
 need(p.is_file(),'Missing file '+str(p));need(sha(p)==r['sha256'],'Hash mismatch '+str(p))
 if 'bytes' in r:need(p.stat().st_size==r['bytes'],'Size mismatch '+str(p))
def verify(root,expected=None):
 index=root/'MANIFEST.json'
 if expected:need(sha(index)==expected,'External manifest pin mismatch')
 rows=load(index)['files'];names=[r['path'] for r in rows];need(len(names)==len(set(names)),'Duplicate manifest paths');actual=set()
 for p in root.rglob('*'):
  need(not p.is_symlink(),'Symlink in packet')
  if p.is_file():actual.add(p.relative_to(root).as_posix())
 need(actual==set(names)|{'MANIFEST.json'},'Exact inventory mismatch')
 for r in rows:check(safe(root,r['path']),r)
 c=load(root/'REUSE_CONTRACT.json');inherit=load(root/'EXACT_INHERITANCE.json');omit={r['path']:r for r in inherit['omitted_new_outputs']}
 for r in inherit['copied_files']:check(safe(root,r['packet_path']),r)
 for r in c['frozen_manifests']+c['frozen_results']:check(safe(root,r['path']),r)
 manifest_rows=0;omission_rows=0
 for m in c['frozen_manifests']:
  base=Path(m['path']).parent
  for r in load(root/m['path'])['files']:
   name=(base/r['path']).as_posix()
   if name in omit:
    need(omit[name]['sha256']==r['sha256'],'Historical omission mismatch');need(not (root/name).exists(),'Omitted output present');omission_rows+=1
   else:check(safe(root,name),r);manifest_rows+=1
 # Frozen copies are checked against actual author bytes, except explicit historical object omissions.
 for author,review in [('hase-finite-raw-obstruction-20261010','hase-finite-raw-review-20261010'),('hase-typed-observer-coherence-20261010','hase-typed-observer-review-20261010'),('hase-cross-typing-observer-20261010','hase-cross-typing-review-20261010')]:
  for p in (root/review/'frozen').rglob('*'):
   if p.is_file():
    rel=p.relative_to(root/review/'frozen');q=root/author/rel;need(q.is_file() and q.read_bytes()==p.read_bytes(),'Frozen reviewer snapshot differs '+str(rel))
 return {'status':'PASS_CUSTODY_ONLY','manifest_sha256':sha(index),'inventory_files':len(rows),'copied_originals_checked':len(inherit['copied_files']),'included_frozen_manifest_rows':manifest_rows,'omitted_frozen_manifest_rows_identified':omission_rows,'historical_new_outputs_not_portably_rehashed':len(omit),'fresh_kernel_checks':0,'new_research_credit':False}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--output',type=Path,required=True);p.add_argument('--expected-manifest-sha256');a=p.parse_args();a.root=a.root.resolve();a.output=a.output.resolve();need(not a.output.exists(),'Refusing existing output');need(not a.output.is_relative_to(a.root),'Output must be outside packet');result=verify(a.root,a.expected_manifest_sha256);a.output.write_text(json.dumps(result,indent=2)+'\n');print('PASS_CUSTODY_ONLY',result['inventory_files'],'files')
if __name__=='__main__':main()
