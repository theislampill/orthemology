"""Provision an absent proof-object-free workspace at the exact retained pins.

The optional source/cache seeds contain verified Git sources and npm registry
downloads only. Without a source seed Git uses the recorded official URLs.
No inherited Lean proof objects or node_modules are copied.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, os, platform, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def run(cmd): return subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT).strip()
def write(p,v): Path(p).write_text(json.dumps(v,indent=2)+'\n')

def main():
    if sys.flags.optimize: raise ValueError('Assertions must be enabled')
    p=argparse.ArgumentParser()
    p.add_argument('--work',type=Path,required=True)
    p.add_argument('--toolchain',type=Path,required=True)
    p.add_argument('--source-seed',type=Path)
    p.add_argument('--npm-cache-seed',type=Path)
    a=p.parse_args(); A=a.work.resolve(); T=a.toolchain.resolve(); I=ROOT/'inputs'
    if A.exists(): raise ValueError('Work directory must be absent')
    if any(c.isspace() or c==':' for c in str(A)+str(T)):
        raise ValueError('This upstream-log adapter requires work and toolchain paths without whitespace or colons')
    for row in json.loads((I/'INPUT_MANIFEST.json').read_text())['files']:
        assert sha(I/row['path'])==row['sha256']
    tool_files=[]
    for row in json.loads((I/'OFFICIAL_TOOLCHAIN_ARCHIVE_BYTE_CHECK.json').read_text())['files']:
        rel=Path(row['archive_member']).relative_to('lean-4.19.0-linux'); f=T/rel
        assert sha(f)==row['sha256'],f
        tool_files.append({'path':str(f),'sha256':sha(f),'bytes':f.stat().st_size})
    assert '4.19.0' in run([str(T/'bin/lean'),'--version'])
    pins=json.loads((I/'lean/lake-manifest.json').read_text())['packages']; assert len(pins)==9
    A.mkdir(parents=True); E=A/'evidence';E.mkdir(); D=A/'dependencies';D.mkdir()
    write(A/'config.json',{'toolchain':str(T),'source_seed':str(a.source_seed.resolve()) if a.source_seed else None,
        'npm_cache_seed':str(a.npm_cache_seed.resolve()) if a.npm_cache_seed else None})
    repos=[]
    for pin in pins:
        name=pin['name']; new=D/name
        rows=json.loads((I/'source-inventories'/f'{name}_source_inventory.json').read_text())
        if a.source_seed:
            old=a.source_seed.resolve()/name
            assert run(['git','-C',str(old),'rev-parse','HEAD'])==pin['rev']
            assert not run(['git','-C',str(old),'status','--porcelain','--untracked-files=no'])
            assert all(sha(old/r['path'])==r['sha256'] for r in rows)
            source=str(old)
        else: source=pin['url']
        run(['git','clone','--no-hardlinks','--no-checkout',source,str(new)])
        run(['git','-C',str(new),'checkout','--detach',pin['rev']])
        run(['git','-C',str(new),'remote','set-url','origin',pin['url']])
        assert run(['git','-C',str(new),'rev-parse','HEAD'])==pin['rev']
        assert not run(['git','-C',str(new),'status','--porcelain','--untracked-files=no'])
        assert set(run(['git','-C',str(new),'ls-files']).splitlines())=={r['path'] for r in rows}
        assert all(sha(new/r['path'])==r['sha256'] for r in rows)
        fsck=run(['git','-C',str(new),'fsck','--full','--strict'])
        shutil.copyfile(I/'source-inventories'/f'{name}_source_inventory.json',E/f'{name}_source_inventory.json')
        repos.append({'package':name,'revision':pin['rev'],'origin':pin['url'],'tracked_files':len(rows),'source_inventory_sha256':sha(E/f'{name}_source_inventory.json'),'git_fsck_output':fsck})
        print('CLEAN_SOURCE_COPY',name,len(rows),flush=True)
    assert not list(D.rglob('*.olean')) and not list(D.rglob('*.ilean'))
    assert not list(D.rglob('node_modules'))
    so=list(D.rglob('*.so'))
    assert len(so)==1 and so[0].relative_to(D).as_posix()=='mathlib/scripts/bench/fake-root/lib/lean/libleanshared.so' and so[0].stat().st_size==0
    driver=A/'lake-driver';shutil.copytree(I/'lean',driver)
    (driver/'.lake').mkdir();(driver/'.lake/packages').symlink_to(D,target_is_directory=True)
    pw=D/'proofwidgets';(pw/'.lake/packages').mkdir(parents=True)
    (pw/'.lake/packages/batteries').symlink_to(D/'batteries',target_is_directory=True)
    shutil.copyfile(I/'widget-package-overrides.json',A/'widget-package-overrides.json')
    cache=A/'npm-cache'
    if a.npm_cache_seed:
        cache.mkdir();shutil.copytree(a.npm_cache_seed.resolve()/'_cacache',cache/'_cacache')
    else: cache.mkdir()
    env={'PATH':str(T/'bin')+':'+os.environ['PATH'],'LEAN_PATH':'','LEAN_SRC_PATH':'','LEAN_NUM_THREADS':'2',
         'LAKE_NO_CACHE':'1','MATHLIB_NO_CACHE_ON_UPDATE':'1','MATHLIB_CACHE_DIR':str(A/'empty-cache/mathlib'),
         'XDG_CACHE_HOME':str(A/'empty-cache/xdg'),'PYTHONDONTWRITEBYTECODE':'1','PYTHONNOUSERSITE':'1','GIT_OPTIONAL_LOCKS':'0',
         'npm_config_cache':str(cache),'npm_config_audit':'false','npm_config_fund':'false'}
    if a.npm_cache_seed: env['npm_config_offline']='true'
    write(A/'environment.json',env)
    write(E/'PLATFORM_TOOLS.json',{'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'platform':platform.platform(),'python':platform.python_version(),'files':tool_files,
        'node_version':run(['node','--version']),'npm_version':run(['npm','--version']),
        'lean_version':run([str(T/'bin/lean'),'--version']),'lake_version':run([str(T/'bin/lake'),'--version'])})
    write(E/'CLEAN_START.json',{'status':'CLEAN_START_VERIFIED','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'repositories':repos,'preexisting_dependency_olean_count':0,'preexisting_dependency_ilean_count':0,
        'preexisting_project_proof_object_count':0,'preexisting_node_modules_count':0,
        'empty_tracked_benchmark_so_outside_search_path':str(so[0].relative_to(D)),
        'source_acquisition':'CLEAN_LOCAL_CLONES' if a.source_seed else 'OFFICIAL_GIT_URLS',
        'npm_download_source':'REUSED_REGISTRY_CACHE_OFFLINE' if a.npm_cache_seed else 'REGISTRY',
        'network_acquisition_test':False if a.source_seed else True,'compiler_bootstrapped':False,'environment':env})
    print('CLEAN_START_PASS')

if __name__=='__main__': main()
