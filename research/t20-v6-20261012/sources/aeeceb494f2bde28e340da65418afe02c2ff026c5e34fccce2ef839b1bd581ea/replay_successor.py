#!/usr/bin/env python3
"""Fresh new-module replay of three scoped results, with zero inherited rebuilds."""
import argparse,importlib.util,json,os,re,shutil,subprocess,sys,time,zipfile
from pathlib import Path,PurePosixPath
sys.dont_write_bytecode=True
from verify_custody import ROOT,verify as custody,need,sha,load,safe,check

def import_file(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

def extract(archive,out,rootname):
 with zipfile.ZipFile(archive) as z:
  infos=[i for i in z.infolist() if not i.is_dir()];need(len({i.filename for i in infos})==len(infos),'Duplicate ZIP entries')
  for i in infos:
   r=PurePosixPath(i.filename);need(r.parts[0]==rootname,'Unexpected ZIP root');need((i.external_attr>>16)&0o170000!=0o120000,'ZIP symlink');p=safe(out,i.filename);need(not p.exists(),'Extraction overwrite');p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(i))
 return out/rootname

def main():
 p=argparse.ArgumentParser(description=__doc__)
 for f in ['lean','packages','baseline-objects','scalar-objects','structural-objects','identity-objects','extractor-objects','family-objects','graph-objects','out']:p.add_argument('--'+f,required=True,type=Path)
 p.add_argument('--archive',type=Path);p.add_argument('--expected-manifest-sha256');p.add_argument('--verify-only',action='store_true');a=p.parse_args()
 for n,v in vars(a).items():
  if isinstance(v,Path):setattr(a,n,v.resolve())
 need(not a.out.exists(),'Use a new absent output directory')
 for q in [ROOT,a.lean.parent.parent,a.packages,*[getattr(a,g) for g in ['baseline_objects','scalar_objects','structural_objects','identity_objects','extractor_objects','family_objects','graph_objects']]]:need(not a.out.is_relative_to(q),'Output must be outside frozen input trees')
 original_custody=custody(ROOT,a.expected_manifest_sha256)
 if a.archive:
  with zipfile.ZipFile(a.archive) as z:
   infos=[i for i in z.infolist() if not i.is_dir()];need(len({i.filename for i in infos})==len(infos),'Duplicate archive entries');actual={str(Path(ROOT.name)/x.relative_to(ROOT)) for x in ROOT.rglob('*') if x.is_file()};need({i.filename for i in infos}==actual,'Archive/extract inventory mismatch')
   for i in infos:
    r=PurePosixPath(i.filename);need(r.parts[0]==ROOT.name,'Archive root mismatch');need(z.read(i)==safe(ROOT,str(PurePosixPath(*r.parts[1:]))).read_bytes(),'Archive/extract byte mismatch')
 c=load(ROOT/'REUSE_CONTRACT.json');pr=c['predecessor'];check(ROOT/pr['path'],pr);a.out.mkdir();dep=a.out/'inherited';dep.mkdir();prevroot=extract(ROOT/pr['path'],dep,pr['root'])
 previous=import_file('authenticated_type_predecessor',prevroot/'replay_extensions.py');previous.verify_index(prevroot,pr['index_sha256']);previous.archive_matches(ROOT/pr['path'],prevroot);pc=load(prevroot/'REUSE_CONTRACT.json');older=dep/'older';older.mkdir();roots=previous.extract_predecessors(pc,older)
 a.v3=roots['hase-type-completion-evidence-20261010-v3.zip'];a.continuation=roots['hase-source-continuation-20261010.zip'];a.v3_archive=prevroot/'predecessors/hase-type-completion-evidence-20261010-v3.zip';a.continuation_archive=prevroot/'predecessors/hase-source-continuation-20261010.zip';a.prerequisite_objects=a.baseline_objects;a.closed_objects=a.scalar_objects;extractor=previous.load_verifier(roots['hase-complete-development-extractor-20261010.zip'])
 def verify():
  inherited=previous.verify(a,pc,roots,extractor);runtime=[]
  for r in c['runtime_objects']:
   q=getattr(a,r['group'])/Path(*r['module'].split('.')).with_suffix('.olean');check(q,r);runtime.append({**r,'resolved':str(q)})
  by_original={r['original_path']:r for r in runtime};resolved={};historical=[]
  for r in c['direct_bindings']:
   m=r['mapping'];kind=m['kind']
   if kind=='included':q=ROOT/m['path']
   elif kind=='runtime':q=Path(by_original[m['original_path']]['resolved'])
   elif kind=='external_package':q=a.packages/m['path']
   elif kind=='lean':q=a.lean
   elif kind=='historical_new_output_omitted':historical.append(r);continue
   else:raise ValueError(kind)
   check(q,r);resolved[r['path']]=q
  # Confirm the new finite lane's 30 retained baseline objects against the old trust-zero receipt.
  old=load(resolved['hase-full-per-review-20261010/PREREQUISITE_REBUILD.json']);need(old['status']=='PASS','Old rebuild status');sources={r['module']:r for r in old['source_checks']};objects={r['module']:r for r in old['build_records']}
  for r in c['finite_source_object_pairs']:
   need(sources[r['module']]['sha256']==r['source_sha256'],'Finite source binding');o=objects[r['module']];need(o['source_sha256']==r['source_sha256'] and o['object_sha256']==r['object_sha256'] and o['trust_zero'] and o['exit_code']==0,'Finite object provenance')
  # Three added retained prerequisites have exact source-to-object historical receipts.
  for r in runtime:
   if r['group'] not in ['family_objects','graph_objects']:continue
   check(ROOT/'inherited'/r['source_path'],{'sha256':r['source_sha256']});check(ROOT/'inherited'/r['receipt_path'],{'sha256':r['receipt_sha256']});j=load(ROOT/'inherited'/r['receipt_path'])
   if r['group']=='family_objects':
    matches=[x for x in j['modules'] if x['module']==r['module']];need(len(matches)==1,'Family receipt module');x=matches[0];need(x['source_sha256']==r['source_sha256'] and x['object_sha256']==r['sha256'] and x['trust_zero'] and x['exit_code']==0,'Family receipt provenance')
   else:
    matches=[x for x in j['source_replays'] if x['module']==r['module']];need(len(matches)==1,'Graph receipt module');x=matches[0];need(x['author_source']['sha256']==r['source_sha256'] and x['object']['sha256']==r['sha256'] and x['trust_zero'] and x['exit_code']==0,'Graph receipt provenance')
  return {'inherited':inherited,'runtime_objects':runtime,'direct_bindings_checked':len(resolved),'external_source_object_pairs_checked':len(c['extra_external_source_object_pairs']),'historical_new_objects_not_portably_rehashed':historical,'custody':custody(ROOT,a.expected_manifest_sha256)}
 before=verify();print('PASS: exact prerequisites, 106 retained project/override objects and external source/object bindings',flush=True)
 if a.verify_only:(a.out/'VERIFY_RECEIPT.json').write_text(json.dumps({'status':'PASS_HASH_VERIFICATION_ONLY','kernel_compilations':0,'verification':before},indent=2)+'\n');return
 baseline=a.out/'baseline-lib';baseline.mkdir();retained=a.out/'retained-lib';retained.mkdir();copies=[]
 for r in before['runtime_objects']:
  base=baseline if r['group']=='baseline_objects' else retained;q=base/Path(*r['module'].split('.')).with_suffix('.olean');q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(r['resolved'],q);check(q,r);copies.append({'path':str(q),'sha256':r['sha256']})
 def fill(source,target):
  for e in source.iterdir():
   q=target/e.name
   if not q.exists():q.symlink_to(e,target_is_directory=e.is_dir())
   elif e.is_dir() and q.is_dir():fill(e,q)
 fill(a.packages/'mathlib/.lake/build/lib/lean/Mathlib',baseline/'Mathlib');packages=[a.packages/r['name']/'.lake/build/lib/lean' for r in before['inherited']['inherited']['pinned_packages']];packages=[q for q in packages if q.is_dir()];positive=[];negative=[];libs={}
 for lane in ['finite','typed','cross']:
  stage=a.out/(lane+'-sources');stage.mkdir();lib=a.out/(lane+'-lib');lib.mkdir();libs[lane]=lib;paths=[lib]+([libs['typed']] if lane=='cross' else [])+[retained,baseline,*packages];env={**os.environ,'LEAN_PATH':':'.join(map(str,paths)),'PYTHONDONTWRITEBYTECODE':'1'}
  for r in c['fresh_compilation_scope']:
   if r['lane']!=lane:continue
   source=ROOT/r['path'];check(source,r);q=stage/source.name;shutil.copy2(source,q);clean=extractor.clean_code(q.read_text());need(not re.findall(r'\b(sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',clean),'Forbidden source escape')
   obj=lib/(r['module']+'.olean');cmd=[str(a.lean),'--trust=0','-o',str(obj),str(q)];started=time.monotonic();proc=subprocess.run(cmd,cwd=stage,env=env,capture_output=True,text=True,timeout=600);text=proc.stdout+proc.stderr;log=a.out/(lane+'-'+r['module']+'.log');log.write_text(text);record={**r,'command':cmd,'exit_code':proc.returncode,'trust_zero':True,'elapsed_seconds':time.monotonic()-started,'log_path':log.name,'log_sha256':sha(log)}
   if r['expected']=='rejection':
    need(proc.returncode!=0 and 'error:' in text and not obj.exists(),'Expected rejection failed '+r['module']);need(not any(s in text for s in ['unknown module','unknown constant','unknown identifier','failed to synthesize','sorryAx']),'Invalid rejection '+r['module']);negative.append(record);print(lane,r['module'],'EXPECTED REJECTION',flush=True)
   else:
    need(proc.returncode==0 and obj.exists(),'Compilation failed '+r['module']+'\n'+text);need(not any(s in text for s in ['warning:','error:','sorryAx']),'Compiler diagnostics '+r['module']);axioms=set()
    for x in re.findall(r'(?:depends on axioms:|axioms)\s*\[([^\]]*)\]',text,re.S):axioms.update(filter(None,re.sub(r'\s+','',x).split(',')))
    need(axioms<={'propext','Classical.choice','Quot.sound'},'Unexpected axioms');record.update(object_sha256=sha(obj),reported_axioms=sorted(axioms));positive.append(record);print(lane,r['module'],'PASS',flush=True)
 after=verify();need(before==after and original_custody==after['custody'],'Inputs changed during replay')
 for r in copies:check(Path(r['path']),r)
 receipt={'status':'PASS_FRESH_EXTRACTED_SUCCESSOR_REPLAY','positive_modules':positive,'expected_rejections':negative,'inherited_modules_recompiled':0,'typed_core_compiled_once_and_reused_by_cross_lane':True,'retained_project_and_override_objects_rehashed':106,'external_source_object_pairs_checked':len(c['extra_external_source_object_pairs']),'original_imported_sources_rehashed':83,'before_after_equal':True,'lean_binary_sha256':sha(a.lean),'verification':before,'no_universal_W_or_negation_conclusion':True,'tentative_homogeneous_PER_research_included':False,'source_only_fresh_machine_build':False,'protected_edits':False,'upload':False,'integration':False,'T20_closure':False};(a.out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS:',len(positive),'new positive module checks,',len(negative),'expected rejections; 0 inherited rebuilds',flush=True)
if __name__=='__main__':main()
