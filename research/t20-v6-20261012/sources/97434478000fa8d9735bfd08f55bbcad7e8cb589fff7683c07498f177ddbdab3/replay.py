from pathlib import Path
import hashlib,json,os,shutil,subprocess,datetime,tempfile
W=Path.cwd(); R=W/'hase-joint-recursor-uniqueness-independent-review-20261010'; C=W/'hase-joint-recursor-uniqueness-20261010'
F=C/'validation/CANDIDATE_FREEZE.json'; expected='6af3c08e7fd1adee842b110a909e02bbbbeb341bb514be3886421f2072bd95d3'
hash=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert hash(F)==expected
freeze=json.loads(F.read_text()); retained=json.loads((C/'validation/RETAINED_INPUTS.json').read_text())
def verify(entries):
 for e in entries:
  p=W/e['path']; assert hash(p)==e['sha256'],str(p); assert p.stat().st_size==e['bytes'],str(p)
verify(freeze['files']); verify(retained['files'])
for e in retained['files']:
 p=W/e['path']; q=R/'retained'/e['path']; q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,q)
for e in freeze['files']:
 p=W/e['path']; q=R/'candidate'/p.relative_to(C); q.parent.mkdir(parents=True,exist_ok=True); shutil.copy2(p,q)
shutil.copy2(F,R/'CANDIDATE_FREEZE.json')
raw=subprocess.check_output(['bash','-c',f'source "{C}/env.sh"; printf "\\n__PATH__%s" "$LEAN_PATH"'],text=True)
paths=raw.split('__PATH__',1)[1].split(':'); lib=Path(tempfile.mkdtemp(prefix='fresh-lib-',dir=R))
newpaths=[str(lib)]; external=[]; ambient=[]; declared={e['path'] for e in retained['files']}
for p in paths:
 p=Path(p)
 if p.resolve()==(C/'validation').resolve():continue
 q=R/'retained'/p.relative_to(W)
 if q.exists():
  for src in p.rglob('*.olean'):
   dst=R/'retained'/src.relative_to(W)
   if not dst.exists():
    dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
   if str(src.relative_to(W)) not in declared:
    ambient.append({'path':str(src.relative_to(W)),'sha256':hash(src),'bytes':src.stat().st_size})
  newpaths.append(str(q))
 elif '.lake' in p.parts:newpaths.append(str(p));external.append(str(p))
 else:raise RuntimeError(f'Uncopied source import directory: {p}')
(R/'AMBIENT_SUPPORT_INPUTS.json').write_text(json.dumps(ambient,indent=2)+'\n')
env=os.environ.copy();env['LEAN_PATH']=':'.join(dict.fromkeys(newpaths));(R/'LEAN_PATH.txt').write_text(env['LEAN_PATH'])
lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'
modules=['JointRecursorCongruence','JointRecursorUniqueness','JointCanonicalRecursor','JointRecursorControls','JointRecursorAudit']; results=[]
for m in modules:
 cmd=[str(lean),'--trust=0','-o',str(lib/(m+'.olean')),str(R/'candidate'/(m+'.lean'))]
 r=subprocess.run(cmd,cwd=R,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (R/(m+'.log')).write_text('$ '+' '.join(cmd)+'\n'+r.stdout)
 print(m,r.returncode,r.stdout,flush=True)
 assert r.returncode==0 and not any(t in r.stdout for t in ['sorryAx',': warning:',': error:'])
 results.append({'module':m,'source_sha256':hash(R/'candidate'/(m+'.lean')),'object_sha256':hash(lib/(m+'.olean')),'exit_code':r.returncode})
verify(freeze['files']);verify(retained['files']);verify(ambient)
for e in retained['files']:assert hash(R/'retained'/e['path'])==e['sha256']
assert hash(F)==expected
receipt={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lean_version':subprocess.check_output([str(lean),'--version'],text=True).strip(),'trust':0,'freeze_sha256':expected,'retained_count':len(retained['files']),'retained_verified_before_after':True,'candidate_verified_before_after':True,'no_original_writes':True,'baseline_rebuilt':False,'candidate_import_path_excluded':True,'fresh_output':str(lib.relative_to(W)),'ambient_support_object_count':len(ambient),'external_unchanged_package_cache_paths':external,'results':results}
(R/'REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS',len(modules),'modules;',len(retained['files']),'pins',flush=True)
