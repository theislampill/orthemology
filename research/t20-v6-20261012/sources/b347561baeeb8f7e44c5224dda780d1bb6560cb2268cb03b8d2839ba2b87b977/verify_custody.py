#!/usr/bin/env python3
"""Artifact/source custody only. No new philosophical review or theorem execution."""
from pathlib import Path
import argparse,json,hashlib,sys,struct
sys.dont_write_bytecode=True
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,s):
 if not c:raise ValueError(s)
def check(p,r):need(p.is_file() and not p.is_symlink() and sha(p)==r['sha256'] and p.stat().st_size==r.get('bytes',p.stat().st_size),'Missing/hash/size/symlink '+str(p))
def verify(root,pin):
 need(sha(root/'MANIFEST.json')==pin,'Manifest external pin mismatch');rows=json.loads((root/'MANIFEST.json').read_text())['files'];names=[r['path'] for r in rows];need(len(names)==len(set(names)),'Duplicate paths');actual=[]
 for p in root.rglob('*'):
  need(not p.is_symlink(),'Symlink in packet')
  if p.is_file():actual.append(str(p.relative_to(root)))
 need(set(actual)==set(names)|{'MANIFEST.json'},'Exact inventory mismatch')
 for r in rows:
  p=root/r['path'];need(p.resolve().is_relative_to(root),'Escaping path');check(p,r)
 c=json.loads((root/'REUSE_CONTRACT.json').read_text())
 for r in c['copied_originals']:check(root/r['path'],r)
 for r in c['final_freeze_pins']:need(sha(root/r['path'])==r['sha256'],'Final freeze pin mismatch')
 A='immanent-self-praise-20261010'
 for r in json.loads((root/A/'MANIFEST.json').read_text())['files']:check(root/A/r['path'],r)
 for r in json.loads((root/A/'RECEIVED_BINDINGS.json').read_text())['records']:
  p=root/A/r['local_path'];b=p.read_bytes();need(len(b)==r['local_bytes'] and sha(p)==r['sha256'],'Historical received-copy binding');need(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['git_blob'],'Historical Git blob mismatch')
 review=json.loads((root/'immanent-self-praise-review-20261010/REVIEW_BINDINGS.json').read_text())
 for r in review['author_final_bindings']+review['review_artifacts']:check(root/r['path'],r)
 images=[]
 for p in sorted((root/A/'sources').glob('page-*.png')):
  b=p.read_bytes();need(b[:8]==b'\x89PNG\r\n\x1a\n' and b[12:16]==b'IHDR','PNG format');width,height=struct.unpack('>II',b[16:24]);need(width>0 and height>0,'PNG dimensions');images.append({'path':str(p.relative_to(root)),'width':width,'height':height,'sha256':sha(p)})
 need(len(images)==5,'Five page images required')
 return c,images

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--expected-manifest-sha256',required=True);p.add_argument('--workspace',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args();root=a.root.resolve();out=a.output.resolve();need(not out.exists() and not out.is_relative_to(root),'Output must be fresh and outside packet');c,images=verify(root,a.expected_manifest_sha256);receipt={'status':'PASS_PACKET_CUSTODY','manifest_sha256':a.expected_manifest_sha256,'images':images,'historical_git_bindings':2,'new_source_reading':False,'new_philosophical_review':False,'formal_theorem_credit':False,'closure':False}
 if a.workspace:
  w=a.workspace.resolve();A='immanent-self-praise-20261010';bindings=json.loads((root/A/'INPUT_BINDINGS.json').read_text())['records']
  for r in bindings:check(w/r['path'],r)
  for r in json.loads((root/'immanent-self-praise-review-20261010/REVIEW_BINDINGS.json').read_text())['supporting_controls']:check(w/r['path'],r)
  ext=json.loads((root/A/'EXTRACTION.json').read_text());raw=w/ext['source'];need(sha(raw)==ext['sha256'],'Raw source binding');s=raw.read_bytes().decode('utf-8').replace('\r\n','\n').replace('\r','\n').replace('\x01','').replace('\x0b','\n');checks=[]
  for volume,lo,hi in ext['selections']:
   p=root/A/'sources'/f'SHIFA_EDITED_{volume}_{lo}_{hi}.txt';t=p.read_text();need(t in s,'Extract is not literal in declared transform');start=s.index(f'({volume}/{lo-1})')+len(f'({volume}/{lo-1})');end=s.index(f'({volume}/{hi})',start)+len(f'({volume}/{hi})');need(t.strip()==s[start:end].strip(),'Bounded page-range mismatch');checks.append({'path':str(p.relative_to(root)),'literal_transform_match':True,'bounded_range_match_ignoring_outer_whitespace':True})
  for r in bindings:check(w/r['path'],r)
  for r in json.loads((root/'immanent-self-praise-review-20261010/REVIEW_BINDINGS.json').read_text())['supporting_controls']:check(w/r['path'],r)
  verify(root,a.expected_manifest_sha256);receipt.update(status='PASS_FRESH_EXTRACT_AND_RETAINED_SOURCE_CUSTODY',retained_input_bindings=len(bindings),excerpt_checks=checks)
 out.mkdir(parents=True);(out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'])
if __name__=='__main__':main()
