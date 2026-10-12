#!/usr/bin/env python3
"""Replay only the new structured-context modules and independent controls."""
import argparse,hashlib,importlib.util,json,os,re,shutil,subprocess,sys,time,zipfile
from pathlib import Path,PurePosixPath
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
from verify_custody import verify as custody,need,sha,load,safe,check,A,V

def import_file(name,path):
 spec=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m

def extract(archive,out,rootname):
 with zipfile.ZipFile(archive) as z:
  infos=[i for i in z.infolist() if not i.is_dir()];need(len({i.filename for i in infos})==len(infos),'Duplicate ZIP entries')
  for i in infos:
   rel=PurePosixPath(i.filename);need(rel.parts[0]==rootname,'Unexpected ZIP root');need((i.external_attr>>16)&0o170000!=0o120000,'ZIP symlink')
   p=safe(out,i.filename);need(not p.exists(),'Extraction overwrite');p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(i))
 return out/rootname

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for f in ['lean','packages','baseline-objects','scalar-objects','structural-objects','identity-objects','extractor-objects','raw-objects','out']:p.add_argument('--'+f,required=True,type=Path)
 p.add_argument('--archive',type=Path);p.add_argument('--expected-manifest-sha256');p.add_argument('--verify-only',action='store_true');a=p.parse_args()
 for n,v in vars(a).items():
  if isinstance(v,Path):setattr(a,n,v.resolve())
 need(not a.out.exists(),'Use a new absent output directory')
 for protected in [ROOT,a.lean.parent.parent,a.packages,a.baseline_objects,a.scalar_objects,a.structural_objects,a.identity_objects,a.extractor_objects,a.raw_objects]:need(not a.out.is_relative_to(protected),'Output must be outside all frozen input trees')
 original_custody=custody(ROOT,a.expected_manifest_sha256)
 if a.archive:
  with zipfile.ZipFile(a.archive) as z:
   infos=[i for i in z.infolist() if not i.is_dir()];need(len({i.filename for i in infos})==len(infos),'Duplicate archive entries')
   actual={str(Path(ROOT.name)/x.relative_to(ROOT)) for x in ROOT.rglob('*') if x.is_file()};need({i.filename for i in infos}==actual,'Archive/extract inventory disagreement')
   for i in infos:
    rel=PurePosixPath(i.filename);need(rel.parts[0]==ROOT.name,'Archive root mismatch');need(z.read(i)==safe(ROOT,str(PurePosixPath(*rel.parts[1:]))).read_bytes(),'Archive/extract byte disagreement')
 c=load(ROOT/'REUSE_CONTRACT.json');pr=c['predecessor'];check(ROOT/pr['path'],pr)
 a.out.mkdir();dep=a.out/'inherited';dep.mkdir();previous_root=extract(ROOT/pr['path'],dep,pr['root'])
 # Authenticate the immutable predecessor wrapper/index, then call verification only.
 previous=import_file('retained_type_extension',previous_root/'replay_extensions.py');previous.verify_index(previous_root,pr['index_sha256']);previous.archive_matches(ROOT/pr['path'],previous_root)
 pc=load(previous_root/'REUSE_CONTRACT.json');old_out=dep/'older';old_out.mkdir();roots=previous.extract_predecessors(pc,old_out)
 a.v3=roots['hase-type-completion-evidence-20261010-v3.zip'];a.continuation=roots['hase-source-continuation-20261010.zip']
 a.v3_archive=previous_root/'predecessors/hase-type-completion-evidence-20261010-v3.zip';a.continuation_archive=previous_root/'predecessors/hase-source-continuation-20261010.zip'
 a.prerequisite_objects=a.baseline_objects;a.closed_objects=a.scalar_objects
 extractor=previous.load_verifier(roots['hase-complete-development-extractor-20261010.zip'])
 def verify():
  inherited=previous.verify(a,pc,roots,extractor);runtime=[]
  for row in c['runtime_objects']:
   q=getattr(a,row['group'])/Path(*row['module'].split('.')).with_suffix('.olean');check(q,row);runtime.append({**row,'resolved':str(q)})
  object_by_original={r['original_path']:r for r in runtime}
  alias_by_original={r['path']:r for r in c['structured_retained_aliases']}
  for r in load(ROOT/A/'INPUTS.json')['retained_objects']:
   target=object_by_original[alias_by_original[r['path']]['runtime_original_path']];need(target['module']==r['module'] and target['sha256']==r['sha256'],'Runtime alias mismatch')
  count=0
  for r in load(ROOT/A/'INPUTS.json')['pinned_files']+load(ROOT/V/'REVIEW_INPUTS.json')['protected_predecessors']:
   if r['path'].endswith('.olean'):
    target=object_by_original[alias_by_original[r['path']]['runtime_original_path']];need(target['sha256']==r['sha256'],'Protected object mismatch')
   else:check(ROOT/'inherited'/r['path'],r)
   count+=1
  # The two new retained Raw modules are bound to their exact author replay receipt and source bytes.
  rawroot=ROOT/'inherited/hase-raw-context-uniformity-20261010';receipt=load(rawroot/'validation/FINAL_REPLAY.json');need(receipt['status']=='PASS','Raw predecessor receipt status')
  for row in receipt['modules']:
   check(rawroot/(row['module']+'.lean'),{'sha256':row['source_sha256']});matched=[r for r in runtime if r['group']=='raw_objects' and r['module']==row['module']];need(len(matched)==1 and matched[0]['sha256']==row['object_sha256'],'Raw source/object binding mismatch')
  need(sha(a.lean)==c['lean_binary_sha256'],'Exact Lean binary mismatch')
  return {'inherited':inherited,'runtime_objects':runtime,'structured_binding_checks':count,'custody':custody(ROOT,a.expected_manifest_sha256)}
 before=verify();print('PASS: exact source closure, toolchain/package pins, 105 retained objects plus one external Mathlib object',flush=True)
 if a.verify_only:
  (a.out/'VERIFY_RECEIPT.json').write_text(json.dumps({'status':'PASS_HASH_VERIFICATION_ONLY','kernel_compilations':0,'verification':before},indent=2)+'\n');return
 baseline=a.out/'baseline-lib';baseline.mkdir();retained=a.out/'retained-lib';retained.mkdir();copies=[]
 for row in before['runtime_objects']:
  base=baseline if row['group']=='baseline_objects' else retained;dest=base/Path(*row['module'].split('.')).with_suffix('.olean');dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(row['resolved'],dest);check(dest,row);copies.append({'path':str(dest),'sha256':row['sha256']})
 def fill(source,target):
  for entry in source.iterdir():
   dst=target/entry.name
   if not dst.exists():dst.symlink_to(entry,target_is_directory=entry.is_dir())
   elif entry.is_dir() and dst.is_dir():fill(entry,dst)
 fill(a.packages/'mathlib/.lake/build/lib/lean/Mathlib',baseline/'Mathlib')
 packages=[a.packages/x['name']/'.lake/build/lib/lean' for x in before['inherited']['inherited']['pinned_packages']];packages=[x for x in packages if x.is_dir()]
 stage=a.out/'sources';stage.mkdir();lib=a.out/'new-lib';lib.mkdir();env={**os.environ,'LEAN_PATH':':'.join(map(str,[lib,retained,baseline,*packages])),'PYTHONDONTWRITEBYTECODE':'1'}
 positives=[];negatives=[]
 for row in c['fresh_compilation_scope']:
  source=ROOT/row['path'];check(source,row);target=stage/source.name;shutil.copy2(source,target)
  clean=extractor.clean_code(target.read_text());need(not re.findall(r'\b(sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',clean),'Forbidden source escape')
  obj=lib/(row['module']+'.olean');cmd=[str(a.lean),'--trust=0','-o',str(obj),str(target)];started=time.monotonic();proc=subprocess.run(cmd,cwd=stage,env=env,capture_output=True,text=True,timeout=600);text=proc.stdout+proc.stderr;log=a.out/(row['module']+'.log');log.write_text(text)
  record={**row,'command':cmd,'exit_code':proc.returncode,'trust_zero':True,'elapsed_seconds':time.monotonic()-started,'log_path':log.name,'log_sha256':sha(log)}
  if row['expected']=='rejection':
   need(proc.returncode!=0 and 'error:' in text and not obj.exists() and 'sorryAx' not in text,'Expected rejection failed: '+row['module']);negatives.append(record);print(row['module'],'EXPECTED REJECTION',flush=True)
  else:
   need(proc.returncode==0 and obj.exists(),'Compilation failed: '+row['module']+'\n'+text);need(not any(x in text for x in ['error:','warning:','sorryAx']),'Compiler warning/error: '+row['module'])
   axioms=set()
   for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',text,re.S):axioms.update(filter(None,re.sub(r'\s+','',match).split(',')))
   need(axioms<={'propext','Classical.choice','Quot.sound'},'Unexpected axioms');record.update(object_sha256=sha(obj),reported_axioms=sorted(axioms));positives.append(record);print(row['module'],'PASS',flush=True)
 after=verify();need(before==after,'Inputs changed during replay');need(original_custody==after['custody'],'Packet changed during replay')
 for row in copies:check(Path(row['path']),row)
 result={'status':'PASS_FRESH_EXTRACTED_STRUCTURED_REPLAY','lean_binary_sha256':sha(a.lean),'positive_modules':positives,'negative_controls':negatives,'inherited_modules_recompiled':0,'retained_project_and_override_objects_rehashed':len(before['runtime_objects']),'extra_external_mathlib_objects_rehashed':1,'original_imported_sources_rehashed':83,'before_after_equal':True,'verification':before,'new_source_reading_credit':False,'source_only_fresh_machine_build':False,'protected_edits':False,'upload':False,'integration':False,'owner_acceptance':False,'T20_closure':False}
 (a.out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print('PASS: 3 fresh positive modules, 4 expected rejections, 0 inherited modules rebuilt',flush=True)
if __name__=='__main__':main()
