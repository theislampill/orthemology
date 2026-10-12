#!/usr/bin/env python3
"""Classify actual git whitespace diagnostics by exact inherited source identity."""
from pathlib import Path
import json,hashlib,re,subprocess,tempfile,shutil
B=Path(__file__).resolve().parents[2];P=B/'projection/package-v2';R=B/'review/portability';D=json.loads((P/'PUBLIC_PROJECTION.json').read_text());exact={}
for x in D['files']:
 if x.get('public_path') and x['projection']=='EXACT':exact[x['public_path']]=x['original_sha256']
 for cp in x.get('required_replay_copies',[]):
  if cp['sha256']==x['original_sha256']:exact[cp['path']]=x['original_sha256']
with tempfile.TemporaryDirectory(dir=R) as t:
 T=Path(t);empty=T/'empty';empty.mkdir();new=T/'authored-amended';new.mkdir()
 for p in P.rglob('*'):
  if p.is_file() and p.relative_to(P).as_posix() not in exact:
   dest=new/p.relative_to(P);dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,dest)
 all_result=subprocess.run(['git','diff','--no-index','--check','--',str(empty),str(P)],capture_output=True,text=True)
 strict=subprocess.run(['git','diff','--no-index','--check','--',str(empty),str(new)],capture_output=True,text=True)
 diagnostics=[];unknown=[]
 for line in all_result.stdout.splitlines():
  m=re.match(re.escape(str(P))+'/(.*):(\d+): (.*)',line)
  if not m:continue
  rel=m[1];path=P/rel;h=hashlib.sha256(path.read_bytes()).hexdigest();r={'path':rel,'line':int(m[2]),'diagnostic':m[3],'sha256':h,'exact_original_sha256':exact.get(rel),'exact_inherited':h==exact.get(rel)};diagnostics.append(r)
  if not r['exact_inherited']:unknown.append(r)
 result={'whole_payload_git_exit':all_result.returncode,'whole_payload_strict_pass':not bool(all_result.stdout or all_result.stderr),'inherited_diagnostics':diagnostics,'unqualified_diagnostics':unknown,'authored_amended_file_count':sum(x.is_file() for x in new.rglob('*')),'authored_amended_git_exit':strict.returncode,'authored_amended_strict_pass':strict.returncode in (0,1) and not strict.stdout and not strict.stderr,'authored_amended_output':strict.stdout+strict.stderr,'scope':'Exact original-source whitespace is retained as a scoped integration advisory; no attribute exemption introduced. No claim whole final delta passes strict git whitespace.'}
 (R/'WHITESPACE_CHECK_V2.txt').write_text(all_result.stdout+all_result.stderr);(R/'WHITESPACE_REVIEW_V2.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='inherited_diagnostics'},indent=2));print('diagnostics',len(diagnostics),'files',len(set(x['path'] for x in diagnostics)))
