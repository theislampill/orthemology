#!/usr/bin/env python3
"""Isolated bounded probe replay and pinned custody; no semantic authorization claim."""
from pathlib import Path
import argparse,json,hashlib,sys,subprocess,shutil,os,importlib.metadata
sys.dont_write_bytecode=True
A='interpretation-repair-transport-20261010';R='interpretation-repair-independent-review-20261010'
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
 for r in c['copied_originals']:check(root/r.get('packet_path',r['path']),r)
 for r in c['final_freeze_pins']:need(sha(root/r['path'])==r['sha256'],'Final freeze mismatch')
 for r in json.loads((root/A/'MANIFEST.json').read_text())['files']:check(root/A/r['path'],r)
 review=json.loads((root/R/'FINAL_RECEIPT.json').read_text())
 for r in review['files']:check(root/R/r['path'],r)
 need(review['accepted_author_result_sha256']==sha(root/A/'RESULT.md') and review['accepted_author_manifest_sha256']==sha(root/A/'MANIFEST.json'),'Final qualified-review target mismatch')
 for r in json.loads((root/A/'PINNED_BINDINGS.json').read_text()):
  p=root/r['path'];b=p.read_bytes();need(sha(p)==r['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['blob_sha1'],'Repository source binding')
 return c

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--expected-manifest-sha256',required=True);p.add_argument('--workspace',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--replay',action='store_true');a=p.parse_args();root=a.root.resolve();w=a.workspace.resolve();out=a.output.resolve();need(not out.exists() and not out.is_relative_to(root),'Output must be fresh and outside packet');c=verify(root,a.expected_manifest_sha256)
 for r in json.loads((root/A/'LOCAL_BINDINGS.json').read_text()):check(w/r['path'],r)
 out.mkdir(parents=True);receipt={'status':'PASS_CUSTODY','manifest_sha256':a.expected_manifest_sha256,'pinned_git_bindings':10,'local_bindings':11,'new_theorem':False,'proven_implementation_bug':False,'closure':False}
 if a.replay:
  stage=out/'stage';stage.mkdir();shutil.copytree(root/A,stage/A);shutil.copytree(root/R,stage/R)
  for r in c['replay_inputs']:
   dest=stage/r['path'];need(dest.resolve().is_relative_to(stage),'Unsafe stage path');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/r['packet_path'],dest)
  env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1');records=[]
  q=subprocess.run([sys.executable,str(stage/A/'probe.py')],cwd=stage,env=env,capture_output=True,text=True);(out/'AUTHOR_REPLAY.log').write_text(q.stdout+q.stderr);need(q.returncode==0,'Author replay failure: '+q.stderr);author=json.loads(q.stdout);need(author==json.loads((root/A/'PROBE_RESULTS.json').read_text()),'Author output mismatch')
  for name in ['PROBE_RESULTS.json','PROBE_DOCUMENTS.json','DECLARED_SNAPSHOTS.json']:need((stage/A/name).read_bytes()==(root/A/name).read_bytes(),'Replayed probe artifact mismatch')
  (stage/R/'replay').mkdir();shutil.copytree(stage/A,stage/R/'replay'/A)
  q=subprocess.run([sys.executable,str(stage/R/'independent_controls.py')],cwd=stage,env=env,capture_output=True,text=True);(out/'INDEPENDENT_REPLAY.log').write_text(q.stdout+q.stderr);need(q.returncode==0,'Independent replay failure: '+q.stderr);independent=json.loads(q.stdout);need(independent==json.loads((root/R/'INDEPENDENT_CONTROLS.json').read_text()),'Independent output mismatch')
  for r in json.loads((root/A/'LOCAL_BINDINGS.json').read_text()):check(w/r['path'],r)
  verify(root,a.expected_manifest_sha256);receipt.update(status='PASS_CUSTODY_AND_FRESH_ISOLATED_PROBES',author_results=author,independent_results=independent,dependencies={n:importlib.metadata.version(n) for n in ['PyYAML','jsonschema']},source_execution='Unmodified copied validators/native occurrence helpers, read-only originals; no installed patches or runtime-deployment claim.')
 (out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'])
if __name__=='__main__':main()
