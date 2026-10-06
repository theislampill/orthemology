#!/usr/bin/env python3
"""Prepare exact official dependency checkouts/cache in a separate new directory.
Requires an already installed official Lean 4.19.0 toolchain on PATH. This performs
network reads and writes only inside the requested new preparation directory.
"""
from pathlib import Path
import argparse,json,os,re,subprocess,sys
if not __debug__:raise SystemExit('OPTIMIZED_PYTHON_UNSUPPORTED')
sys.dont_write_bytecode=True
from package_checks import check_source_locks
PACKAGE=Path(__file__).resolve().parent

def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--directory',type=Path,required=True);x=a.parse_args();out=x.directory.resolve()
 if out.exists():raise SystemExit('PREPARATION_DIRECTORY_EXISTS: choose a new path; nothing was deleted')
 if out==PACKAGE or PACKAGE in out.parents:raise SystemExit('PREPARATION_INSIDE_SOURCE_REFUSED')
 check_source_locks(PACKAGE,require_integrity=True)
 version=subprocess.check_output(['lean','--version'],text=True).strip()
 if 'version 4.19.0,' not in version or '6caaee842e94' not in version:raise SystemExit('Official Lean 4.19.0 is required')
 pins=json.loads((PACKAGE/'lean/lake-manifest.json').read_text())['packages'];out.mkdir(parents=True);deps=out/'dependencies';deps.mkdir();logs=out/'logs';logs.mkdir()
 env=dict(os.environ);env['GIT_TERMINAL_PROMPT']='0';env['MATHLIB_CACHE_DIR']=str(out/'official-cache');env['XDG_CACHE_HOME']=str(out/'xdg-cache')
 for p in pins:
  if not p['url'].startswith(('https://github.com/leanprover/','https://github.com/leanprover-community/')):raise SystemExit('Unexpected dependency origin')
  d=deps/p['name']
  with (logs/(p['name']+'.log')).open('w') as log:
   for cmd in [['git','init',str(d)],['git','-C',str(d),'remote','add','origin',p['url']],['git','-C',str(d),'fetch','--depth','1','origin',p['rev']],['git','-C',str(d),'checkout','--detach','FETCH_HEAD']]:subprocess.run(cmd,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
  actual=subprocess.check_output(['git','-C',str(d),'rev-parse','HEAD'],text=True).strip()
  if actual!=p['rev']:raise SystemExit('Wrong checkout: '+p['name'])
  print('PINNED_SOURCE_PREPARED',p['name'],flush=True)
 # Lake release lookup needs this exact official tag, not a different revision.
 pw=deps/'proofwidgets';subprocess.run(['git','-C',str(pw),'fetch','--depth','1','origin','tag','v0.0.57'],env=env,check=True)
 if subprocess.check_output(['git','-C',str(pw),'rev-parse','v0.0.57^{commit}'],text=True).strip()!='c4919189477c3221e6a204008998b0d724f49904':raise SystemExit('Unexpected ProofWidgets release tag')
 math=deps/'mathlib';mp=math/'.lake/packages';mp.mkdir(parents=True,exist_ok=True)
 expected={p['name']:p['rev'] for p in pins}
 for p in json.loads((math/'lake-manifest.json').read_text())['packages']:
  if p['rev']!=expected[p['name']]:raise SystemExit('Mathlib transitive pin differs')
  (mp/p['name']).symlink_to(deps/p['name'],target_is_directory=True)
 roots=sorted({m for f in (PACKAGE/'lean').glob('*.lean') for m in re.findall(r'^import\s+(Mathlib\.[\w.]+)',f.read_text(),re.M)})
 with (logs/'official-cache.log').open('w') as log:subprocess.run(['lake','exe','cache','get',*roots],cwd=math,env=env,stdout=log,stderr=subprocess.STDOUT,check=True)
 for p in pins:
  if subprocess.check_output(['git','-C',str(deps/p['name']),'status','--porcelain','--untracked-files=no'],text=True).strip():raise SystemExit('Tracked dependency source changed: '+p['name'])
 (out/'PREPARATION_RECEIPT.json').write_text(json.dumps({'status':'PASS','lean_version':version,'source_revisions':expected,'dependency_roots':roots,'objects':'new official pinned cache acquisition, not a source cold build','source_package_modified':False},indent=2)+'\n')
 print('PINNED_DEPENDENCIES_PREPARED',deps,flush=True)
if __name__=='__main__':main()
