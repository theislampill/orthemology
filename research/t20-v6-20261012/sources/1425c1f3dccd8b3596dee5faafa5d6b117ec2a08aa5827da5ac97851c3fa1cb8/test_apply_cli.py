#!/usr/bin/env python3
"""Disposable CLI flow using exact candidate code and explicitly synthetic fixture pins."""
from pathlib import Path
import subprocess,tempfile,shutil,json,hashlib,sys
B=Path(__file__).resolve().parents[2];R=B/'review/portability';rows=[]
def git(p,*a):return subprocess.check_output(['git','-C',str(p),*a],text=True,stderr=subprocess.DEVNULL).strip()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def snapshot(p):return {str(x.relative_to(p)):sha(x) for x in p.rglob('*') if x.is_file() and '.git' not in x.relative_to(p).parts}
with tempfile.TemporaryDirectory(dir=R) as t:
 T=Path(t);repo=T/'fixture';repo.mkdir();git(repo,'init');git(repo,'config','user.name','Review Fixture');git(repo,'config','user.email','fixture@example.invalid');(repo/'anchor').write_bytes(b'fixture baseline\n');git(repo,'add','anchor');git(repo,'commit','-m','local fixture')
 package=T/'candidate';shutil.copytree(B/'projection/package',package)
 pins={'commit':git(repo,'rev-parse','HEAD'),'tree':git(repo,'rev-parse','HEAD^{tree}'),'destination':'research/proposal','preimages':[{'path':'anchor','git_blob_sha1':git(repo,'rev-parse','HEAD:anchor'),'sha256':sha(repo/'anchor'),'bytes':(repo/'anchor').stat().st_size}]}
 (package/'INTEGRATION_PINS.json').write_text(json.dumps(pins,indent=2)+'\n')
 manifest=json.loads((package/'PACKAGE_CONTENTS.json').read_text())
 for x in manifest['files']:
  p=package/x['path'];x['sha256']=sha(p);x['bytes']=p.stat().st_size
 (package/'PACKAGE_CONTENTS.json').write_text(json.dumps(manifest,indent=2)+'\n')
 source_before=snapshot(package);repo_before=snapshot(repo);head_before=git(repo,'rev-parse','HEAD')
 for label,flags in [('check_only',[]),('apply',['--apply']),('refuse_second_apply',['--apply'])]:
  r=subprocess.run([sys.executable,'-B',str(package/'apply_additive.py'),str(repo),*flags],capture_output=True,text=True)
  row={'case':label,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr};rows.append(row)
  if label=='check_only':assert r.returncode==0 and snapshot(repo)==repo_before and git(repo,'status','--porcelain')==''
  elif label=='apply':assert r.returncode==0 and snapshot(repo/'research/proposal')==source_before and git(repo,'diff','--cached','--name-only')=='' and git(repo,'rev-parse','HEAD')==head_before
  else:assert r.returncode!=0 and snapshot(repo/'research/proposal')==source_before
 assert snapshot(package)==source_before
out={'scope':'End-to-end exact candidate CLI and payload copy with synthetic local Git fixture; only the disposable package INTEGRATION_PINS and integrity manifest were deliberately adapted for that fixture. This is not application to the protected baseline.','code_sha256':sha(B/'projection/package/apply_additive.py'),'unchanged_source':True,'no_index_or_commit_changes':True,'runs':rows}
(R/'APPLY_CLI_REVIEW.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
