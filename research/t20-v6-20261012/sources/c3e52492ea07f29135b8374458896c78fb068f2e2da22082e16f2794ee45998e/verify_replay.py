#!/usr/bin/env python3
"""Exact custody verification and optional new-module-only retained-dependency replay."""
import argparse,hashlib,json,os,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True

def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def need(c,s):
 if not c: raise ValueError(s)
def check(p,r):
 need(p.is_file() and not p.is_symlink(),'Missing or symlink '+str(p));need(p.stat().st_size==r['bytes'] and sha(p)==r['sha256'],'Mismatch '+str(p))
def verify(root,pin):
 need(sha(root/'MANIFEST.json')==pin,'Manifest external pin mismatch')
 rows=json.loads((root/'MANIFEST.json').read_text())['files']
 names=[r['path'] for r in rows];need(len(names)==len(set(names)),'Duplicate paths')
 actual=[]
 for p in root.rglob('*'):
  need(not p.is_symlink(),'Symlink in packet')
  if p.is_file():actual.append(p.relative_to(root).as_posix())
 need(set(actual)==set(names)|{'MANIFEST.json'},'Exact inventory mismatch')
 for r in rows:
  p=root/r['path'];need(p.resolve().is_relative_to(root),'Escaping path');check(p,r)
 c=json.loads((root/'REUSE_CONTRACT.json').read_text())
 for r in c['copied_originals']:check(root/r['path'],r)
 for r in c['modules']:check(root/r['path'],r)
 omitted={r['path']:r for r in c['omitted_original_files']}
 for review in c['frozen_reviews']:
  historical=json.loads((root/review/'MANIFEST.json').read_text());need(historical['status']=='PASS','Review seal')
  for r in historical['files']:
   name=review+'/'+r['path']
   if name in omitted:need(omitted[name]['sha256']==r['sha256'] and omitted[name]['bytes']==r['bytes'],'Omitted review binding')
   else:check(root/name,r)
  replay=json.loads((root/review/'REVIEW_RECEIPT.json').read_text())
  need(replay['status']=='PASS','Review replay status')
  for r in replay['records']:
   need(r['exit_code']==r['expected'],'Historical control exit')
   need(sha(root/review/'sources'/(r['module']+'.lean'))==r['source_sha256'],'Review source binding')
 author=json.loads((root/'hase-rigidity-polymorphic-transfer-20261010/validation/PRESERVATION_CHECK.json').read_text())
 need(author['result']=='PASS','Author preservation status')
 for name,h in author['new_sources'].items():need(sha(root/'hase-rigidity-polymorphic-transfer-20261010'/name)==h,'Author freeze')
 need(sha(root/'hase-rigidity-polymorphic-transfer-20261010/validation/build.log')==author['new_build_log_sha256'],'Author build log')
 for r in c['review_source_bindings']:
  need(sha(root/r['author'])==sha(root/r['review']),'Author/reviewer freeze mismatch')
 return c

def dependencies(w,c):
 for row in c['dependency_roots']:
  p=w/row['path'];actual=sorted(str(q.relative_to(p)) for q in p.rglob('*.olean') if q.is_file()) if p.exists() else []
  need(actual==sorted(row['olean_inventory']),'Dependency root inventory changed: '+str(p))
 for r in c['retained_dependency_files']:
  p=w/r['path']
  if 'symlink_target' in r:
   need(p.is_symlink() and os.readlink(p)==r['symlink_target'],'Retained symlink changed')
   need(p.resolve().is_relative_to(w),'Retained symlink escaped workspace')
   check(p.resolve(),r)
  else:check(p,r)

def main():
 a=argparse.ArgumentParser();a.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);a.add_argument('--expected-manifest-sha256',required=True);a.add_argument('--workspace',type=Path);a.add_argument('--output',required=True,type=Path);a.add_argument('--replay',action='store_true');x=a.parse_args();root=x.root.resolve();out=x.output.resolve();need(not out.exists(),'Output exists');need(not out.is_relative_to(root),'Output must be outside packet');c=verify(root,x.expected_manifest_sha256);out.mkdir(parents=True)
 receipt={'status':'PASS_CUSTODY','manifest_sha256':x.expected_manifest_sha256,'baseline_modules_rebuilt':0,'new_independent_review':False,'t20_closure':False}
 if x.replay:
  need(x.workspace is not None,'Workspace required');w=x.workspace.resolve();dependencies(w,c);lib=out/'lib';lib.mkdir();env={**os.environ,'LEAN_PATH':':'.join([str(lib)]+[str(w/r) for r in c['lean_search_order']])};records=[]
  for r in c['modules']:
   m=r['module'];label=r['group']+'-'+m;dest=lib if r['group']=='core' else out/r['group'];dest.mkdir(exist_ok=True);p=root/r['path'];cmd=[str(w/c['lean_binary']),'--trust=0','-o',str(dest/(m+'.olean')),str(p)];q=subprocess.run(cmd,env=env,capture_output=True,text=True);s=q.stdout+q.stderr;(out/(label+'.log')).write_text(s);axs=set(a.strip() for group in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',s,re.S) for a in group.split(',') if a.strip());row={'module':m,'group':r['group'],'exit_code':q.returncode,'source_sha256':sha(p),'log_sha256':sha(out/(label+'.log')),'axioms':sorted(axs),'command':cmd};records.append(row);print(label,q.returncode,flush=True)
   if r.get('expected_failure',False):
    expected=(root/r['historical_log']).read_text();expected=expected.replace(r['historical_source_path'],str(p))
    need(q.returncode!=0 and s==expected,'Expected-rejection diagnostic mismatch '+label)
    need(not (dest/(m+'.olean')).exists(),'Rejected source produced object')
    row['status']='EXPECTED_REJECTION';continue
   need(q.returncode==0 and not re.search(r'error:|sorryAx',s),'Replay failure '+m+': '+s);need(re.findall(r'warning: ([^\n]*)',s)==r.get('warning_first_lines',[]),'Unexpected warnings '+label);need(axs <= {'propext','Classical.choice','Quot.sound'},'Unexpected axioms');row['object_sha256']=sha(dest/(m+'.olean'))
  dependencies(w,c);verify(root,x.expected_manifest_sha256);receipt.update(status='PASS_CUSTODY_AND_FRESH_REPLAY',modules=records,retained_dependencies_unchanged=True,lean_path=env['LEAN_PATH'])
 (out/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(receipt['status'],flush=True)
if __name__=='__main__':main()
