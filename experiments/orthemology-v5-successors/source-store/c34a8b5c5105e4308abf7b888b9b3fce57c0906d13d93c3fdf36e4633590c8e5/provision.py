#!/usr/bin/env python3
"""One bounded, fail-closed qualification of the pinned official Mathlib cache."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, shlex, shutil, signal, subprocess, sys, tarfile, time

R=Path(__file__).resolve().parent
BASE_MANIFEST='9f2a0f116f90fc4189faacc79d5b7c02116e1d36735cc2cdffe4f9117406de95'
LEANTAR_SHA='c3294bf820d5d1d7cc59bc3ce9bdc244b3f45cab37ea9dd649e1a388c20dbe3c'
LEANTAR_ARCHIVE_SHA='87ea796fb4a6cc9a7b7548b392ba19e7da509324ecced9579692fe299d1516df'
LEANTAR_URL='https://github.com/digama0/leangz/releases/download/v0.1.15/leantar-v0.1.15-x86_64-unknown-linux-musl.tar.gz'
TAG='v0.0.57'
def sha(p):
    with p.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
def read(p): return json.loads(p.read_text())
def write(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
def utc(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(test,message):
    if not test: raise RuntimeError(message)
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('stage',choices=['prepare','acquire','verify'])
for name in ['base','sources','toolchain','work']: p.add_argument('--'+name,required=True,type=Path)
a=p.parse_args(); B,S,T,W=[getattr(a,k).resolve() for k in ['base','sources','toolchain','work']]
E=W/'evidence'; D=W/'dependencies'; C=W/'official-cache'
pins=read(R/'inputs/pins.json'); expected=read(B/'dependencies/hidden-change.json')
# No ambient credential, user-home, Lean-path, loader or compiler configuration is inherited.
network_keys=['HTTP_PROXY','HTTPS_PROXY','ALL_PROXY','NO_PROXY','http_proxy','https_proxy','all_proxy','no_proxy','SSL_CERT_FILE','SSL_CERT_DIR','CURL_CA_BUNDLE']
env={k:os.environ[k] for k in network_keys if k in os.environ}
env.update({'PATH':str(T/'bin')+':/usr/bin:/bin','HOME':str(W/'anonymous-home'),'XDG_CONFIG_HOME':str(W/'anonymous-xdg'),'XDG_CACHE_HOME':str(W/'xdg-cache'),'CURL_HOME':str(W/'anonymous-home'),'MATHLIB_CACHE_DIR':str(C),'LEAN_PATH':'','LEAN_SRC_PATH':'','LEAN_NUM_THREADS':'1','MATHLIB_NO_CACHE_ON_UPDATE':'1','LANG':'C.UTF-8','LC_ALL':'C.UTF-8','GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':'/dev/null','GIT_TERMINAL_PROMPT':'0','GIT_ASKPASS':'/bin/false','SSH_ASKPASS':'/bin/false','GCM_INTERACTIVE':'never','GIT_OPTIONAL_LOCKS':'0','GIT_CONFIG_COUNT':'2','GIT_CONFIG_KEY_0':'credential.helper','GIT_CONFIG_VALUE_0':'','GIT_CONFIG_KEY_1':'http.extraHeader','GIT_CONFIG_VALUE_1':''})
seq=0
stage_owned=False

def run(cmd, *, cwd=None, timeout=300, label='command'):
    global seq
    seq+=1; log=E/f'{a.stage}_{seq:03d}_{label}.log'; start=time.monotonic()
    receipt={'command':[str(x) for x in cmd],'cwd':str(cwd or W),'utc_start':utc(),'timeout_seconds':timeout,'log':log.name}
    with (E/'commands.jsonl').open('a') as f: f.write(json.dumps({'event':'start',**receipt})+'\n')
    with log.open('x') as out:
        proc=subprocess.Popen([str(x) for x in cmd],cwd=cwd or W,env=env,stdout=out,stderr=subprocess.STDOUT,start_new_session=True)
        try: code=proc.wait(timeout=timeout); status='PASS' if code==0 else 'FAILED'
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid,signal.SIGTERM)
            try: code=proc.wait(timeout=5)
            except subprocess.TimeoutExpired: os.killpg(proc.pid,signal.SIGKILL); code=proc.wait()
            status='TIMEOUT'
    receipt.update({'status':status,'returncode':code,'utc_end':utc(),'elapsed_seconds':time.monotonic()-start,'log_sha256':sha(log)})
    with (E/'commands.jsonl').open('a') as f: f.write(json.dumps({'event':'end',**receipt})+'\n')
    require(status=='PASS',f'{label}: {status}, code {code}; see {log}')
    return log.read_text()

def git(repo,*args): return run(['/usr/bin/git','-C',repo,*args],label='git').strip()
def recipe_check():
    m=read(R/'RECIPE_MANIFEST.json')
    for row in m['files']:
        f=R/row['path']; require(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],f'recipe changed: {f}')
def base_check():
    require(sha(B/'MANIFEST.json')==BASE_MANIFEST,'immutable base manifest changed')
    for row in read(B/'MANIFEST.json')['files']:
        f=B/row['path']; require(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],f'base changed: {f}')
    require(len(expected['files'])==6646 and expected['exact_olean_set'] is True,'unexpected original inventory')
    require({x['name']:x['revision'] for x in expected['packages']}=={x['name']:x['rev'] for x in pins},'pins differ from immutable inventory')
def toolchain_check():
    for row in read(R/'inputs/toolchain-files.json'):
        f=T/row['path']; require(f.stat().st_size==row['bytes'] and sha(f)==row['sha256'],f'toolchain changed: {f}')
def sources_check(root):
    result=[]
    for pin in pins:
        repo=root/pin['name']; rows=read(R/'inputs/source-inventories'/f"{pin['name']}_source_inventory.json")
        require(git(repo,'rev-parse','HEAD')==pin['rev'],f'revision changed: {repo}')
        require(git(repo,'remote','get-url','origin')==pin['url'],f'origin changed: {repo}')
        require(not git(repo,'status','--porcelain','--untracked-files=no'),f'tracked sources changed: {repo}')
        tracked=git(repo,'ls-files','-z').split('\0'); require(tracked[-1]=='','bad tracked file output');tracked=tracked[:-1]
        require(set(tracked)=={r['path'] for r in rows} and len(tracked)==len(rows),f'tracked set changed: {repo}')
        for row in rows: require(sha(repo/row['path'])==row['sha256'],f'source bytes changed: {repo/row["path"]}')
        extra=git(repo,'ls-files','--others','--exclude-standard','-z').split('\0')
        require(not [x for x in extra if x.endswith('.lean')],f'unexpected Lean sources: {repo}')
        require(not (repo/'.git/objects/info/alternates').exists(),f'Git alternates at {repo}')
        result.append({'name':pin['name'],'revision':pin['rev'],'url':pin['url'],'tracked_clean':True,'tracked_files':len(rows)})
    require(git(root/'proofwidgets','rev-parse',f'refs/tags/{TAG}^{{commit}}')=='c4919189477c3221e6a204008998b0d724f49904','ProofWidgets tag changed')
    return result

def objects_check(cache_only=False):
    wanted=[x for x in expected['files'] if not cache_only or (x['package']=='mathlib' and x['path'].startswith('Cache/'))]
    actual=[]
    for pin in pins:
        build=D/pin['name']/'.lake/build/lib/lean'
        for f in sorted(build.rglob('*.olean')):
            require(f.is_file() and not f.is_symlink(),f'nonregular object: {f}')
            actual.append({'package':pin['name'],'path':f.relative_to(build).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)})
    key=lambda x:(x['package'],x['path'])
    amap={key(x):x for x in actual}; wmap={key(x):x for x in wanted}
    receipt={'status':'PASS' if amap==wmap else 'FAILED','expected_count':len(wanted),'actual_count':len(actual),'missing':[list(x) for x in sorted(wmap.keys()-amap.keys())],'extra':[list(x) for x in sorted(amap.keys()-wmap.keys())],'mismatched':[{'expected':wmap[k],'actual':amap[k]} for k in sorted(amap.keys() & wmap.keys()) if amap[k]!=wmap[k]],'files':sorted(actual,key=key)}
    write(E/(a.stage+'_CACHE_GATE.json' if cache_only else a.stage+'_OBJECT_INVENTORY.json'),receipt)
    require(amap==wmap,'exact object identity gate failed')
    return len(actual)

def disk_check():
    d=shutil.disk_usage(W.parent);require(d.free>=10*1024**3,'less than 10 GiB available before acquisition')
    return {'total':d.total,'used':d.used,'free':d.free,'minimum_free':10*1024**3}

try:
    recipe_check();base_check();toolchain_check()
    if a.stage=='prepare':
        require(not W.exists(),'refuse existing work directory')
        disk=disk_check(); W.mkdir(); E.mkdir();stage_owned=True;D.mkdir();C.mkdir()
        for x in ['anonymous-home','anonymous-xdg','xdg-cache']: (W/x).mkdir()
        write(E/'START.json',{'utc':utc(),'work_absent_before_creation':True,'disk':disk,'base_manifest_sha256':BASE_MANIFEST,'recipe_manifest_sha256':sha(R/'RECIPE_MANIFEST.json'),'source_seed':str(S),'toolchain':str(T),'scope':'Clean local source clones; no inherited proof objects or Mathlib archives; reused verified official toolchain.','inherited_environment_keys':sorted(k for k in network_keys if k in os.environ),'environment':{k:v for k,v in env.items() if k not in network_keys}})
        sources_check(S)
        for pin in pins:
            dest=D/pin['name']
            run(['/usr/bin/git','clone','--no-hardlinks','--no-checkout',S/pin['name'],dest],label='local_clone')
            git(dest,'checkout','--detach',pin['rev']);git(dest,'remote','set-url','origin',pin['url'])
            git(dest,'fsck','--full','--strict')
        sources=sources_check(D)
        require(not list(D.rglob('*.olean')) and not list(D.rglob('*.ilean')) and not list(D.rglob('*.ltar')),'proof/cache objects present before build')
        require(not list(C.iterdir()),'cache not empty at start')
        pkg=D/'mathlib/.lake/packages';pkg.mkdir(parents=True)
        for pin in pins:
            if pin['name']!='mathlib': (pkg/pin['name']).symlink_to(Path('../../..')/pin['name'],target_is_directory=True)
        write(E/'CLEAN_START.json',{'status':'PASS','utc':utc(),'sources':sources,'objects_before_build':0,'archives_before_build':0,'explicit_cache_empty':True,'sibling_links':{p.name:os.readlink(p) for p in pkg.iterdir()}})
        version=run([T/'bin/lean','--version'],label='lean_version').strip()
        require(version=='Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)','unexpected toolchain version')
        run([T/'bin/lake','build','cache'],cwd=D/'mathlib',timeout=300,label='cache_client_build')
        count=objects_check(cache_only=True);sources_check(D);toolchain_check();base_check()
        require(not list(C.iterdir()),'unexpected acquisition during cache-client build')
        write(E/'PREPARED.json',{'status':'PASS','utc':utc(),'fresh_cache_tooling_objects':count,'cache_empty_after_build':True,'cache_executable_sha256':sha(D/'mathlib/.lake/build/bin/cache'),'recipe_manifest_sha256':sha(R/'RECIPE_MANIFEST.json')})
    elif a.stage=='acquire':
        require(read(E/'PREPARED.json')['status']=='PASS','prepare not qualified')
        require(not (E/'ACQUISITION.json').exists(),'one acquisition already started; no relaunch')
        require(read(E/'PREPARED.json')['recipe_manifest_sha256']==sha(R/'RECIPE_MANIFEST.json'),'recipe changed after build')
        start=time.monotonic();deadline=start+1800
        with (E/'ACQUISITION.json').open('x') as f: json.dump({'status':'PREFLIGHT','utc_start':utc(),'attempt':1,'timeout_seconds':1800},f,indent=2)
        stage_owned=True
        sources_check(D);objects_check(cache_only=True);require(not list(C.iterdir()),'explicit cache is not empty before sole acquisition')
        disk=disk_check()
        write(E/'ACQUISITION.json',{'status':'RUNNING','utc_start':utc(),'attempt':1,'timeout_seconds':1800,'disk_before_acquisition':disk,'leantar_url':LEANTAR_URL})
        def remaining():
            left=deadline-time.monotonic();require(left>0,'30-minute acquisition bound exhausted');return left
        archive=C/'leantar-0.1.15.tar.gz'
        run(['/usr/bin/curl','-q','--fail','--location','--retry','5','--proto','=https','--proto-redir','=https',LEANTAR_URL,'-o',archive],timeout=remaining(),label='official_leantar_download')
        require(sha(archive)==LEANTAR_ARCHIVE_SHA,'fresh native leantar archive identity mismatch')
        prefix='leantar-v0.1.15-x86_64-unknown-linux-musl'
        with tarfile.open(archive,'r:gz') as tf:
            members=tf.getmembers()
            require(len(members)==2 and {m.name.rstrip('/') for m in members}=={prefix,prefix+'/leantar'},'unexpected leantar archive members')
            for member in members:
                require(not member.issym() and not member.islnk() and '..' not in Path(member.name).parts and not Path(member.name).is_absolute(),'unsafe leantar archive member')
                if member.name.rstrip('/')==prefix: require(member.isdir(),'unexpected archive root type')
                else: require(member.isfile() and member.size==2529072,'unexpected native helper member')
            member=tf.getmember(prefix+'/leantar')
            with tf.extractfile(member) as src, (C/'leantar-0.1.15').open('xb') as dst: shutil.copyfileobj(src,dst)
        require(sha(C/'leantar-0.1.15')==LEANTAR_SHA,'fresh native leantar identity mismatch')
        (C/'leantar-0.1.15').chmod(0o755)
        write(E/'LEANTAR_IDENTITY.json',{'status':'PASS','url':LEANTAR_URL,'archive_sha256':sha(archive),'binary_sha256':sha(C/'leantar-0.1.15'),'sole_extracted_member':prefix+'/leantar','safe_member_validation':True})
        run([C/'leantar-0.1.15','--version'],timeout=remaining(),label='leantar_version')
        run([T/'bin/lake','exe','cache','get','Mathlib'],cwd=D/'mathlib',timeout=remaining(),label='official_cache_get_Mathlib')
        elapsed=time.monotonic()-start;require(elapsed<=1800,'acquisition exceeded 30-minute bound')
        require(sha(C/'leantar-0.1.15')==LEANTAR_SHA,'native helper changed')
        write(E/'ACQUISITION.json',{'status':'PASS','utc_end':utc(),'attempt':1,'timeout_seconds':1800,'elapsed_seconds':elapsed,'disk_before_acquisition':disk,'leantar_url':LEANTAR_URL,'leantar_sha256':LEANTAR_SHA,'leantar_archive_sha256':sha(archive),'cache_command':['lake','exe','cache','get','Mathlib'],'archive_count':len(list(C.glob('*.ltar'))),'partial_archive_count':len(list(C.glob('*.part')))})
    else:
        require(read(E/'ACQUISITION.json')['status']=='PASS','acquisition has no passing terminal receipt')
        require(not (E/'VERIFY_STARTED.json').exists(),'one verification already started; no overwrite')
        with (E/'VERIFY_STARTED.json').open('x') as f: json.dump({'utc':utc(),'status':'STARTED'},f)
        stage_owned=True
        sources=sources_check(D);n=objects_check();toolchain_check();base_check()
        require(sha(C/'leantar-0.1.15')==LEANTAR_SHA,'native helper changed');require(not list(C.glob('*.part')),'partial downloads remain')
        require(len(list(C.glob('*.ltar')))==6641,'wrong official archive count')
        leanpath=':'.join(str(D/name/'.lake/build/lib/lean') for name in ['Cli','batteries','Qq','aesop','proofwidgets','importGraph','LeanSearchClient','plausible','mathlib'])
        activation='#!/usr/bin/env bash\n# Explicit dependency-only environment; no project objects.\n'+''.join('export '+k+'='+shlex.quote(v)+'\n' for k,v in {'PATH':env['PATH'],'LEAN_PATH':leanpath,'LEAN_SRC_PATH':'','LEAN_NUM_THREADS':'1','MATHLIB_CACHE_DIR':str(C),'XDG_CACHE_HOME':str(W/'xdg-cache')}.items())
        (W/'build_env.sh').write_text(activation)
        write(W/'environment.json',{'lean':str(T/'bin/lean'),'dependency_roots':{'hidden-change':str(D)},'module_timeout_seconds':600})
        smoke=W/'smoke';smoke.mkdir();(smoke/'ImportMathlib.lean').write_text('import Mathlib\n#check Nat.Partrec.Code.evaln\n#check MvPolynomial.funext\nexample : (1 : Nat) + 1 = 2 := rfl\n')
        run(['/bin/bash','--noprofile','--norc','-c','source "$1"; exec lean --root="$2" -o "$2/ImportMathlib.olean" "$2/ImportMathlib.lean"','bash',W/'build_env.sh',smoke],cwd=smoke,timeout=300,label='fresh_import_smoke')
        toolchain_check();base_check();sources_check(D)
        write(E/'QUALIFIED.json',{'status':'PASS','utc':utc(),'scope':'Fresh isolated official-cache provisioning to the immutable prepared-environment object inventory; not a new theorem replay or dependency cold build.','base_manifest_sha256':BASE_MANIFEST,'recipe_manifest_sha256':sha(R/'RECIPE_MANIFEST.json'),'objects_verified':n,'official_cache_objects':6641,'fresh_cache_tooling_objects':5,'repositories':sources,'source_files_verified':sum(x['tracked_files'] for x in sources),'fresh_import_Mathlib_smoke':True,'new_full_proof_replay':False,'environment_sha256':sha(W/'environment.json'),'activation_sha256':sha(W/'build_env.sh'),'disk_after':dict(zip(['total','used','free'],shutil.disk_usage(W)))})
    print(json.dumps({'stage':a.stage,'status':'PASS','work':str(W),'utc':utc()}),flush=True)
except BaseException as exc:
    if stage_owned and E.exists():
        failure={'status':'FAILED','stage':a.stage,'utc':utc(),'type':type(exc).__name__,'message':str(exc)}
        failure_path=E/(a.stage+'_FAILURE_'+str(time.time_ns())+'.json')
        with failure_path.open('x') as f: json.dump(failure,f,indent=2)
        if a.stage=='acquire' and (E/'ACQUISITION.json').exists():
            rec=read(E/'ACQUISITION.json');rec.update(failure);write(E/'ACQUISITION.json',rec)
    print(f'{a.stage}: FAILED: {exc}',file=sys.stderr,flush=True);raise
