#!/usr/bin/env python3
"""Exact source/evidence custody and bounded Python controls; no Lean or rebuild."""
from pathlib import Path
import argparse,json,hashlib,sys,subprocess,shutil,platform
sys.dont_write_bytecode=True
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(c,s):
 if not c:raise ValueError(s)
def check(p,r):need(p.is_file() and not p.is_symlink() and sha(p)==r['sha256'] and p.stat().st_size==r.get('bytes',p.stat().st_size),'Missing/hash/size/symlink '+str(p))
def verify(root,pin):
 need(sha(root/'MANIFEST.json')==pin,'Manifest external pin mismatch');m=json.loads((root/'MANIFEST.json').read_text());rows=m['files'];names=[r['path'] for r in rows];need(len(set(names))==len(names),'Duplicate paths');actual=[]
 for p in root.rglob('*'):
  need(not p.is_symlink(),'Symlink in packet')
  if p.is_file():actual.append(str(p.relative_to(root)))
 need(set(actual)==set(names)|{'MANIFEST.json'},'Exact inventory mismatch')
 for r in rows:
  p=root/r['path'];need(p.resolve().is_relative_to(root),'Escaping path');check(p,r)
 c=json.loads((root/'REUSE_CONTRACT.json').read_text())
 for r in c['copied_originals']:check(root/r['path'],r)
 A='capped-tensor-recovery-20261010';R='capped-tensor-independent-review-20261010'
 author=json.loads((root/A/'MANIFEST.json').read_text())
 for r in author['files']:check(root/A/r['path'],r)
 review=json.loads((root/R/'MANIFEST.json').read_text())
 for r in review['files']:check(root/R/r['path'],r)
 rr=json.loads((root/R/'REPLAY_RECEIPT.json').read_text());need(rr['status']=='PASS','Review replay status');need(rr['author_result_sha256']==sha(root/A/'RESULT.md') and rr['author_manifest_sha256']==sha(root/A/'MANIFEST.json'),'Final review/author freeze mismatch')
 for r in c['ancestor_bindings']:check(root/A/r['copy_path'],r)
 r=c['fetched_source'];p=root/A/r['path'];b=p.read_bytes();need(b.endswith(b'\n\n'),'Expected documented copied-source trailing bytes');normalized=b[:-1];need(hashlib.sha1(b'blob '+str(len(normalized)).encode()+b'\0'+normalized).hexdigest()==r['git_blob_sha_returned'],'Documented fetched-source normalization mismatch')
 for r in c['final_freeze_pins']:need(sha(root/r['path'])==r['sha256'],'Final freeze pin mismatch')
 hidden=json.loads((root/'hidden-mass-independent-review-20261010/FINAL_SCOPE_RECEIPT.json').read_text())
 for key,hkey in [('source_path','source_sha256'),('author_manifest_path','author_manifest_sha256'),('review_path','review_sha256'),('section_snapshot_path','section_sha256')]:need(sha(root/hidden[key])==hidden[hkey],'Hidden-mass final binding')
 b=(root/hidden['source_path']).read_bytes()[hidden['section_start_byte']:hidden['section_end_byte_exclusive']];need(b==(root/hidden['section_snapshot_path']).read_bytes(),'Hidden-mass exact subsection bytes');need(hashlib.sha256(b[hidden['mathematical_body_start_byte_within_section']:]).hexdigest()==hidden['mathematical_body_sha256'],'Hidden-mass mathematical body')
 return c

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--expected-manifest-sha256',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--replay',action='store_true');a=p.parse_args();root=a.root.resolve();out=a.output.resolve();need(not out.exists() and not out.is_relative_to(root),'Output must be fresh and outside packet');c=verify(root,a.expected_manifest_sha256);out.mkdir(parents=True);receipt={'status':'PASS_CUSTODY','manifest_sha256':a.expected_manifest_sha256,'lean_credit':False,'baseline_rebuild':False,'new_independent_review':False,'closure':False}
 if a.replay:
  stage=out/'stage';stage.mkdir();A='capped-tensor-recovery-20261010';R='capped-tensor-independent-review-20261010'
  for name in [A,R]:shutil.copytree(root/name,stage/name)
  records=[]
  for base,script,result in [(A,'check_controls.py','CONTROLS.json'),(R,'controls/independent_checks.py','INDEPENDENT_CHECKS.json')]:
   q=subprocess.run([sys.executable,str(stage/base/script)],cwd=stage,capture_output=True,text=True);label=Path(script).stem;(out/(label+'.log')).write_text(q.stdout+q.stderr);need(q.returncode==0,'Control failed '+label+': '+q.stdout+q.stderr);need((stage/base/result).read_bytes()==(root/base/result).read_bytes(),'Control result differs '+label);records.append({'script':base+'/'+script,'exit_code':q.returncode,'result_sha256':sha(stage/base/result)});print(label,'PASS',flush=True)
  verify(root,a.expected_manifest_sha256);receipt.update(status='PASS_CUSTODY_AND_FRESH_PYTHON_REPLAY',controls=records,python_version=platform.python_version(),python_executable_sha256=sha(Path(sys.executable)),author_exact_checks=json.loads((stage/A/'CONTROLS.json').read_text())['checks'])
 (out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'])
if __name__=='__main__':main()
