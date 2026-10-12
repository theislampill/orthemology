from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys,datetime
W=Path(__file__).resolve().parent.parent;R=Path(__file__).resolve().parent
C=W/'hase-finite-sidecar-realisation-20261011'
hash=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
F=Path(sys.argv[1]);expected=sys.argv[2]
assert hash(F)==expected,'Freeze changed'
freeze=json.loads(F.read_text())
entries=[dict(e, path=str((C/e['name']).relative_to(W))) if 'name' in e else e for e in freeze['files']]
def check(entries):
 for e in entries:
  p=Path(e['path']);p=p if p.is_absolute() else W/p
  assert hash(p)==e['sha256'],str(p)
  if 'bytes' in e:assert p.stat().st_size==e['bytes'],str(p)
check(entries)
for name in ['INHERITED_OBJECTS_BEFORE.json','INHERITED_SOURCES_BEFORE.json']:
 check(json.loads((R/name).read_text())['files'])
source=R/'candidate';source.mkdir(exist_ok=True)
for e in entries:
 p=Path(e['path']);p=p if p.is_absolute() else W/p
 if p.is_relative_to(C):
  q=source/p.relative_to(C);q.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,q)
shutil.copy2(F,R/'CANDIDATE_FREEZE.json')
lib=R/'fresh-lib';lib.mkdir(exist_ok=True)
if any(lib.iterdir()):raise RuntimeError('Fresh output is not empty')
env=os.environ.copy();env['LEAN_PATH']=str(lib)+':'+(R/'INHERITED_LEAN_PATH.txt').read_text()
assert str(C/'validation') not in env['LEAN_PATH']
(R/'REVIEW_LEAN_PATH.txt').write_text(env['LEAN_PATH'])
lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'
modules=['FiniteCorrectionTable','SourceSidecarController','SourceObservableMinimum','SourceCorrectionHistories','FiniteSidecarControls','FiniteSidecarAudit','IndependentBoundaries','IndependentAudit'];results=[]
for m in modules:
 p=(source if m not in ['IndependentBoundaries','IndependentAudit'] else R)/(m+'.lean')
 cmd=[str(lean),'--trust=0','-o',str(lib/(m+'.olean')),str(p)]
 run=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/(m+'.log')).write_text('$ '+' '.join(cmd)+'\n'+run.stdout)
 print(m,'exit',run.returncode,flush=True)
 if run.returncode or any(t in run.stdout for t in ['sorryAx',': warning:',': error:']):
  print(run.stdout,flush=True);raise RuntimeError(m+' failed')
 results.append({'module':m,'source_sha256':hash(p),'object_sha256':hash(lib/(m+'.olean')),'exit_code':run.returncode})
check(entries)
for name in ['INHERITED_OBJECTS_BEFORE.json','INHERITED_SOURCES_BEFORE.json']:
 check(json.loads((R/name).read_text())['files'])
assert hash(F)==expected
(R/'REPLAY.json').write_text(json.dumps({'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lean_version':subprocess.check_output([str(lean),'--version'],text=True).strip(),'trust':0,'freeze_sha256':expected,'candidate_verified_before_after':True,'inherited_sources_verified_before_after':True,'inherited_objects_verified_before_after':True,'no_candidate_or_inherited_writes':True,'inherited_dependencies_rebuilt':False,'candidate_import_path_excluded':True,'results':results},indent=2)+'\n')
print('PASS 8 fresh additive/reviewer modules; inherited inputs preserved',flush=True)
