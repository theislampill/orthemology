#!/usr/bin/env python3
"""Exact-byte custody, source closure and receipt checks; no baseline compilation."""
import argparse,hashlib,json,re,sys
from pathlib import Path,PurePosixPath
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent;I='hase-imported-compiler-transport-20261010';V='review-henkin-source-model-20261010';Q='homogeneous-per-root-20261010'
def need(c,m):
 if not c:raise ValueError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
def safe(root,name):
 r=PurePosixPath(name);need(not r.is_absolute() and '..' not in r.parts,'Unsafe path');p=root/r;need(p.resolve().is_relative_to(root.resolve()),'Escaping path');need(not any(x.is_symlink() for x in [p,*p.parents]),'Symlink path');return p
def check(p,r):
 need(p.is_file(),'Missing '+str(p));need(sha(p)==r['sha256'],'Hash mismatch '+str(p))
 if 'bytes' in r:need(p.stat().st_size==r['bytes'],'Size mismatch '+str(p))
def clean_code(s):
 out=[];depth=0;i=0
 while i<len(s):
  if s[i:i+2]=='/-':depth+=1;i+=2
  elif depth and s[i:i+2]=='-/':depth-=1;i+=2
  elif not depth and s[i:i+2]=='--':j=s.find('\n',i);i=len(s) if j<0 else j
  else:
   if not depth or s[i]=='\n':out.append(s[i])
   i+=1
 need(depth==0,'Unclosed block comment');return re.sub(r'"(?:\\.|[^"\\])*"','""',''.join(out))
def verify(root,expected=None):
 index=root/'MANIFEST.json'
 if expected:need(sha(index)==expected,'External manifest pin mismatch')
 rows=load(index)['files'];names=[r['path'] for r in rows];need(len(names)==len(set(names)),'Duplicate inventory');actual=set()
 for p in root.rglob('*'):
  need(not p.is_symlink(),'Symlink in packet')
  if p.is_file():actual.add(p.relative_to(root).as_posix())
 need(actual==set(names)|{'MANIFEST.json'},'Exact inventory mismatch')
 for r in rows:check(safe(root,r['path']),r)
 c=load(root/'REUSE_CONTRACT.json');inherited=load(root/'EXACT_INHERITANCE.json');omit={r['path']:r for r in inherited['omitted_new_outputs']};mapping={r['path']:r['packet_path'] for r in inherited['copied_files']}
 for r in inherited['copied_files']:check(root/r['packet_path'],r)
 for r in c['frozen_review_pins']:check(root/r['path'],r)
 def original(name):return root/mapping.get(name,name)
 manifest_checked=manifest_omitted=0
 for m in c['frozen_manifests']:
  check(root/m['path'],m);j=load(root/m['path']);records=j if isinstance(j,list) else [r for k in m['keys'] for r in j[k]]
  for r in records:
   name=m['prefix']+r['path']
   if name in omit:need(omit[name]['sha256']==r['sha256'],'Historical omission mismatch');need(not (root/name).exists(),'Omitted object present');manifest_omitted+=1
   else:check(original(name),r);manifest_checked+=1
 for r in c['source_snapshot_pins']:
  check(original(r['path']),r);check(root/V/'sources'/Path(r['path']).name,r)
 for r in c['retained_original_source_pins']:check(original(r['path']),r)
 acq=load(root/c['source_acquisition']);need(acq['pin']==c['source_pin'] and len(acq['sources'])==83 and not acq['missing'],'Original closure size/pin')
 sourcechecks=[]
 for r in acq['sources']:
  p=root/'inherited'/I/'sources'/(r['module']+'.lean');check(p,r);b=p.read_bytes();need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob'],'Original Git blob mismatch');need(r['sha256'] in PurePosixPath(r['path']).parts,'Source-store content address')
  imports=[x for line in clean_code(b.decode()).splitlines() if re.match(r'^\s*import\s',line) for x in line.split()[1:]];need(imports==r['imports'],'Recorded import mismatch');sourcechecks.append({'module':r['module'],'sha256':r['sha256'],'git_blob':r['git_blob']})
 need({p.stem for p in (root/'inherited'/I/'sources').glob('*.lean')}=={r['module'] for r in acq['sources']},'Original source inventory')
 # Exact independently retrieved T16 bytes, including source-store and Git-blob identity.
 p=root/Q/'inherited/UnaryCertificateSyntax.lean';b=p.read_bytes();ac=load(root/V/'certificate-delta/ACQUISITION.json');fetch=load(root/V/'certificate-delta/GITHUB_FETCH.json')['structuredContent'];check(p,ac);need(fetch['content'].encode()==b,'T16 fetched content mismatch');blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();need(blob==ac['git_blob_sha']==fetch['sha'],'T16 Git blob mismatch');need(b==(root/V/'certificate-delta/sources/UnaryCertificateSyntax.lean').read_bytes(),'T16 review snapshot mismatch')
 final=load(root/V/'FINAL_REVIEW_RECEIPT.json');need(final['status']=='INDEPENDENT_REVIEW_PASS','Review seal status');need(sha(root/V/'FINAL_REVIEW.md')==final['report_sha256'],'Review report seal')
 for r in final['passes']:check(root/V/r['receipt'],r)
 return {'status':'PASS_CUSTODY_AND_SOURCE_BINDINGS_ONLY','manifest_sha256':sha(index),'inventory_files':len(rows),'copied_originals_checked':len(inherited['copied_files']),'included_frozen_manifest_rows':manifest_checked,'omitted_manifest_rows_identified':manifest_omitted,'original_source_checks':sourcechecks,'newly_recovered_T16_source_sha256':sha(p),'T16_git_blob_sha1':blob,'baseline_modules_recompiled':0,'new_research_credit':False}
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=ROOT);p.add_argument('--output',type=Path,required=True);p.add_argument('--expected-manifest-sha256');a=p.parse_args();a.root=a.root.resolve();a.output=a.output.resolve();need(not a.output.exists(),'Refusing existing output');need(not a.output.is_relative_to(a.root),'Output must be outside packet');r=verify(a.root,a.expected_manifest_sha256);a.output.write_text(json.dumps(r,indent=2)+'\n');print(r['status'],r['inventory_files'],'files; 83 original source bindings and recovered T16 bytes')
if __name__=='__main__':main()
