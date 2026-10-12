from pathlib import Path
import subprocess,json,hashlib,zipfile,os,datetime,shutil
W=Path('private-locator:8f24556a330b05a11a95')
A=W/'tranche16/dependency-source-assurance-20261005'
Z=W/'tranche16/proof-package-integration/releases/Sixteenth_Orthemology_Proof_Source_Recovered_v1.zip'
OLD=W/'recovery-20261005-1330/environment/dependencies'
D=A/'dependencies'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(cmd):return subprocess.check_output(cmd,text=True,stderr=subprocess.STDOUT).strip()
assert sha(Z)=='40c77652d3938e95f832023f32f018e1e394ffbd57adcc7d918d07d578e8a3a2'
D.mkdir(exist_ok=True)
with zipfile.ZipFile(Z) as z:
 assert len(z.namelist())==376
 assert all(not n.startswith('/') and '..' not in Path(n).parts for n in z.namelist())
 z.extractall(A/'immutable-extraction')
P=A/'immutable-extraction/Sixteenth_Orthemology_Proof_Source_Recovered_v1'
pins=json.loads((P/'lean/lake-manifest.json').read_text())['packages'];rec=[]
for p in pins:
 n=p['name'];old=OLD/n;new=D/n
 assert run(['git','-C',str(old),'rev-parse','HEAD'])==p['rev']
 assert not run(['git','-C',str(old),'status','--porcelain','--untracked-files=no'])
 tracked=run(['git','-C',str(old),'ls-files']).splitlines()
 rows=[{'path':f,'sha256':sha(old/f)} for f in tracked]
 if not new.exists():
  run(['git','clone','--no-hardlinks','--no-checkout',str(old),str(new)])
  run(['git','-C',str(new),'checkout','--detach',p['rev']])
  run(['git','-C',str(new),'remote','set-url','origin',p['url']])
 assert run(['git','-C',str(new),'rev-parse','HEAD'])==p['rev']
 assert not run(['git','-C',str(new),'status','--porcelain','--untracked-files=no'])
 assert all(sha(new/r['path'])==r['sha256'] for r in rows)
 fsck=run(['git','-C',str(new),'fsck','--full','--strict'])
 (A/'evidence'/f'{n}_source_inventory.json').write_text(json.dumps(rows,indent=2)+'\n')
 rec.append({'package':n,'revision':p['rev'],'origin':p['url'],'tracked_files':len(rows),'inventory_sha256':sha(A/'evidence'/f'{n}_source_inventory.json'),'git_fsck_output':fsck})
 print('CLEAN_SOURCE_COPY',n,len(rows),flush=True)
assert not list(D.rglob('*.olean')) and not list(D.rglob('*.ilean'))
so_files=list(D.rglob('*.so'))
assert len(so_files)==1 and so_files[0].relative_to(D).as_posix()=='mathlib/scripts/bench/fake-root/lib/lean/libleanshared.so' and so_files[0].stat().st_size==0
driver=A/'lake-driver';driver.mkdir()
for n in ['lakefile.lean','lake-manifest.json','lean-toolchain']:shutil.copyfile(P/'lean'/n,driver/n)
(driver/'.lake').mkdir();(driver/'.lake/packages').symlink_to(D,target_is_directory=True)
# Standalone upstream widget target must resolve the exact root pin, rather than its older standalone pin.
pw=D/'proofwidgets';(pw/'.lake/packages').mkdir(parents=True)
(pw/'.lake/packages/batteries').symlink_to(D/'batteries',target_is_directory=True)
(A/'widget-package-overrides.json').write_text(json.dumps({'version':'1.1.0','packages':[p for p in pins if p['name']=='batteries']},indent=2)+'\n')
T=W/'recovery-20261005-1330/environment/toolchain/lean-4.19.0-linux'
env={'PATH':str(T/'bin')+':'+os.environ['PATH'],'LEAN_PATH':'','LEAN_SRC_PATH':'','LEAN_NUM_THREADS':'2','LAKE_NO_CACHE':'1','MATHLIB_NO_CACHE_ON_UPDATE':'1','MATHLIB_CACHE_DIR':str(A/'empty-cache/mathlib'),'XDG_CACHE_HOME':str(A/'empty-cache/xdg'),'PYTHONDONTWRITEBYTECODE':'1','GIT_OPTIONAL_LOCKS':'0','npm_config_cache':str(A/'npm-cache'),'npm_config_audit':'false','npm_config_fund':'false'}
(A/'environment.json').write_text(json.dumps(env,indent=2)+'\n')
receipt={'status':'CLEAN_START_VERIFIED','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'archive_sha256':sha(Z),'archive_entries':376,'source_tree_files':len([p for p in P.rglob('*') if p.is_file()]),'repositories':rec,'preexisting_third_party_olean_count':0,'preexisting_third_party_ilean_count':0,'preexisting_third_party_native_shared_object_count':0,'tracked_empty_benchmark_so_placeholder_outside_search_path':'mathlib/scripts/bench/fake-root/lib/lean/libleanshared.so','preexisting_project_proof_object_count':len(list(P.rglob('*.olean'))),'source_revisions_and_tracked_files_unchanged':True,'lean_version':run([str(T/'bin/lean'),'--version']),'lean_sha256':sha(T/'bin/lean'),'lake_version':run([str(T/'bin/lake'),'--version']),'lake_sha256':sha(T/'bin/lake'),'trusted_official_toolchain_reused':True,'compiler_bootstrapped':False,'environment':env}
(A/'evidence/CLEAN_START.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('CLEAN_START_PASS')
