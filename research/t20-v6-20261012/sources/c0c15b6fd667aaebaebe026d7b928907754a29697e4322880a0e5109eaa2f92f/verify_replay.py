#!/usr/bin/env python3
"""Bounded artifact custody and exact final Python controls; no new proof credit."""
from pathlib import Path
import argparse,json,hashlib,sys,subprocess,shutil,platform
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
 for r in c['final_freeze_pins']:need(sha(root/r['path'])==r['sha256'],'Final freeze binding mismatch')
 for r in c['ancestor_bindings']:check(root/'determinate-moment-effectivity-20261010'/r['snapshot'],r)
 for spec in c['declared_manifests']:
  for r in json.loads((root/spec['path']).read_text())['files']:check(root/spec['prefix']/r['path'],r)
 receipt=json.loads((root/'determinate-moment-independent-review-20261010/RECEIPT.json').read_text())
 need(receipt['verdict']=='PASS within declared scope','Review verdict')
 for key in ['author_files','review_files']:
  for name,h in receipt[key].items():need(sha(root/name)==h,'Review frozen binding '+name)
 for r in receipt['input_original_copy_checks']:need(sha(root/r['copy'])==r['sha256'],'Reviewer input copy binding')
 return c

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--expected-manifest-sha256',required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--replay',action='store_true');a=p.parse_args();root=a.root.resolve();out=a.output.resolve();need(not out.exists() and not out.is_relative_to(root),'Output must be fresh and outside packet');c=verify(root,a.expected_manifest_sha256);out.mkdir(parents=True);receipt={'status':'PASS_CUSTODY','manifest_sha256':a.expected_manifest_sha256,'lean_credit':False,'baseline_rebuild':False,'new_independent_review':False,'closure':False}
 if a.replay:
  stage=out/'stage';stage.mkdir()
  for base in c['script_directories']:shutil.copytree(root/base,stage/base)
  for r in c['ancestor_bindings']:
   dst=stage/r['path'];need(dst.resolve().is_relative_to(stage),'Unsafe ancestor overlay');dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(root/'determinate-moment-effectivity-20261010'/r['snapshot'],dst)
  records=[]
  for r in c['replay_scripts']:
   q=subprocess.run([sys.executable,str(stage/r['script'])],cwd=stage,capture_output=True,text=True);label=Path(r['script']).stem;(out/(label+'.log')).write_text(q.stdout+q.stderr);need(q.returncode==0,'Control failed '+label+': '+q.stdout+q.stderr)
   result=json.loads(q.stdout) if r.get('stdout_result') else json.loads((stage/r['result']).read_text());expected=json.loads((root/r['expected_result']).read_text())
   for key in r.get('variable_fields',[]):result.pop(key,None);expected.pop(key,None)
   need(result==expected,'Control result differs '+label);records.append({'script':r['script'],'exit_code':q.returncode,'result':result,'stdout_sha256':hashlib.sha256(q.stdout.encode()).hexdigest()});print(label,'PASS',flush=True)
  verify(root,a.expected_manifest_sha256);receipt.update(status='PASS_CUSTODY_AND_FRESH_PYTHON_REPLAY',controls=records,python_version=platform.python_version(),python_executable_sha256=sha(Path(sys.executable)))
 (out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'])
if __name__=='__main__':main()
