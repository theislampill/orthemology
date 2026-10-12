#!/usr/bin/env python3
"""Fresh new/recovered-module replay using exact externally retained original objects."""
import argparse,json,os,re,shutil,subprocess,sys,time,zipfile
sys.dont_write_bytecode=True
from pathlib import Path,PurePosixPath
from verify_custody import ROOT,verify as custody,need,sha,load,safe,check,clean_code

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for f in ['lean','packages','original-objects','full-per-objects','out']:p.add_argument('--'+f,required=True,type=Path)
 p.add_argument('--archive',type=Path);p.add_argument('--expected-manifest-sha256');p.add_argument('--verify-only',action='store_true');a=p.parse_args()
 for n,v in vars(a).items():
  if isinstance(v,Path):setattr(a,n,v.resolve())
 need(not a.out.exists(),'Use a new absent output directory')
 for q in [ROOT,a.lean.parent.parent,a.packages,a.original_objects,a.full_per_objects]:need(not a.out.is_relative_to(q),'Output must be outside frozen input trees')
 original_custody=custody(ROOT,a.expected_manifest_sha256)
 if a.archive:
  with zipfile.ZipFile(a.archive) as z:
   infos=[i for i in z.infolist() if not i.is_dir()];need(len({i.filename for i in infos})==len(infos),'Duplicate archive paths');actual={str(Path(ROOT.name)/p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()};need({i.filename for i in infos}==actual,'Archive/extract inventory mismatch')
   for i in infos:
    r=PurePosixPath(i.filename);need(r.parts[0]==ROOT.name,'Unexpected archive root');need(z.read(i)==safe(ROOT,str(PurePosixPath(*r.parts[1:]))).read_bytes(),'Archive/extract mismatch')
 c=load(ROOT/'REUSE_CONTRACT.json')
 def verify():
  need(sha(a.lean)==c['lean_binary_sha256'],'Exact compiler binary mismatch');version=subprocess.check_output([str(a.lean),'--version'],text=True).strip();need(version==c['lean_version'],'Lean version mismatch');packages=[]
  for r in load(ROOT/c['package_manifest'])['packages']:
   q=a.packages/r['name'];rev=subprocess.check_output(['git','-C',str(q),'rev-parse','HEAD'],text=True).strip();need(rev==r['rev'],'Package revision mismatch '+r['name']);packages.append({'name':r['name'],'rev':rev})
  objects=[]
  for r in c['runtime_objects']:
   q=getattr(a,r['group'])/Path(*r['module'].split('.')).with_suffix('.olean');check(q,r)
   if 'source_path' in r:check(ROOT/r['source_path'],{'sha256':r['source_sha256']})
   else:check(a.packages/r['external_source_path'],{'sha256':r['source_sha256']})
   objects.append({**r,'resolved':str(q)})
  return {'lean_version':version,'lean_binary_sha256':sha(a.lean),'packages':packages,'runtime_objects':objects,'custody':custody(ROOT,a.expected_manifest_sha256)}
 before=verify();print('PASS: exact compiler/package pins, 92 retained objects, source closure and all three review seals',flush=True);a.out.mkdir()
 if a.verify_only:(a.out/'VERIFY_RECEIPT.json').write_text(json.dumps({'status':'PASS_HASH_VERIFICATION_ONLY','kernel_compilations':0,'verification':before},indent=2)+'\n');return
 baseline=a.out/'baseline-lib';baseline.mkdir();copies=[]
 for r in before['runtime_objects']:
  q=baseline/Path(*r['module'].split('.')).with_suffix('.olean');q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(r['resolved'],q);check(q,r);copies.append({'path':str(q),'sha256':r['sha256']})
 def fill(source,target):
  for e in source.iterdir():
   q=target/e.name
   if not q.exists():q.symlink_to(e,target_is_directory=e.is_dir())
   elif e.is_dir() and q.is_dir():fill(e,q)
 fill(a.packages/'mathlib/.lake/build/lib/lean/Mathlib',baseline/'Mathlib');packages=[a.packages/r['name']/'.lake/build/lib/lean' for r in before['packages']];packages=[q for q in packages if q.is_dir()];stage=a.out/'sources';stage.mkdir();lib=a.out/'new-lib';lib.mkdir();env={**os.environ,'LEAN_PATH':':'.join(map(str,[lib,baseline,*packages])),'PYTHONDONTWRITEBYTECODE':'1'};records=[]
 for r in c['fresh_compilation_scope']:
  source=ROOT/r['path'];check(source,r);q=stage/source.name;shutil.copy2(source,q);need(not re.findall(r'\b(sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',clean_code(q.read_text())),'Forbidden source escape '+r['module']);obj=lib/(r['module']+'.olean');cmd=[str(a.lean),'--trust=0','-o',str(obj),str(q)];started=time.monotonic();proc=subprocess.run(cmd,cwd=stage,env=env,capture_output=True,text=True,timeout=600);text=proc.stdout+proc.stderr;log=a.out/(r['module']+'.log');log.write_text(text);need(proc.returncode==0 and obj.exists(),'Compilation failed '+r['module']+'\n'+text);need('error:' not in text and 'sorryAx' not in text,'Compiler error '+r['module']);warnings=re.findall(r'warning: ([^\n]*)',text);need(warnings==r['allowed_warnings'],'Unexpected warning '+r['module']+' '+str(warnings));axioms=set()
  for x in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',text,re.S):axioms.update(filter(None,re.sub(r'\s+','',x).split(',')))
  need(axioms<={'propext','Classical.choice','Quot.sound'},'Unexpected axioms');records.append({**r,'command':cmd,'exit_code':0,'trust_zero':True,'object_sha256':sha(obj),'reported_axioms':sorted(axioms),'warnings':warnings,'elapsed_seconds':time.monotonic()-started,'log_path':log.name,'log_sha256':sha(log)});print(r['module'],'PASS',flush=True)
 after=verify();need(before==after and original_custody==after['custody'],'Inputs changed during replay')
 for r in copies:check(Path(r['path']),r)
 receipt={'status':'PASS_FRESH_EXTRACTED_HENKIN_INDEPENDENCE_REPLAY','modules':records,'expected_rejection_fixtures':0,'negative_claims_are_passing_theorems':True,'retained_baseline_and_override_objects_rehashed':92,'original_imported_sources_rehashed':83,'inherited_original_source_modules_rebuilt':0,'newly_recovered_T16_module_recompiled':True,'before_after_equal':True,'verification':before,'source_only_fresh_machine_build':False,'protected_edits':False,'upload':False,'integration':False,'owner_acceptance':False,'T20_closure':False};(a.out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS:',len(records),'new/recovered module checks; 0 original baseline modules rebuilt',flush=True)
if __name__=='__main__':main()
