#!/usr/bin/env python3
"""Portable source-only replay, using explicit pinned dependencies and new outputs."""
from pathlib import Path
import argparse,json,os,shutil,subprocess,sys,time
sys.dont_write_bytecode=True
from package_checks import sha,check_source_locks
from compile_project import compile_project
from run_controls import run_controls
PACKAGE=Path(__file__).resolve().parent

def main():
 a=argparse.ArgumentParser(description=__doc__);a.add_argument('--lean',default='lean');a.add_argument('--dependencies',type=Path);a.add_argument('--output',type=Path);a.add_argument('--source-only',action='store_true');x=a.parse_args()
 if x.output is not None and x.output.resolve().exists():raise SystemExit('FRESH_OUTPUT_REFUSED: choose a new output path; nothing was deleted')
 count=check_source_locks(PACKAGE, require_integrity=True)
 if x.source_only:print('RECOVERED_SOURCE_INTEGRITY_PASS',count);return
 if x.output is None:a.error('--output is required for a full replay')
 out=x.output.resolve()
 if out.exists():raise SystemExit('FRESH_OUTPUT_REFUSED: choose a new output path; nothing was deleted')
 if out==PACKAGE or PACKAGE in out.parents:raise SystemExit('OUTPUT_INSIDE_SOURCE_REFUSED')
 lean=Path(shutil.which(x.lean) or x.lean).resolve();version=subprocess.check_output([str(lean),'--version'],text=True).strip()
 assert 'version 4.19.0,' in version and '6caaee842e94' in version,'Wrong official Lean version/commit'
 deps=(x.dependencies or PACKAGE/'lean/.lake/packages').resolve();pins=json.loads((PACKAGE/'lean/lake-manifest.json').read_text())['packages'];records=[];env=dict(os.environ);env['GIT_OPTIONAL_LOCKS']='0'
 closure=json.loads((PACKAGE/'DEPENDENCY_CLOSURE.json').read_text())['recorded_source_modules']
 for p in pins:
  d=deps/p['name']
  def git(*args):return subprocess.check_output(['git','-C',str(d),*args],text=True,env=env).strip()
  assert git('rev-parse','HEAD')==p['rev'],'Wrong dependency revision: '+p['name']
  assert not git('status','--porcelain','--untracked-files=no'),'Modified tracked dependency: '+p['name']
  tracked=set(git('ls-files').splitlines());lib=d/'.lake/build/lib/lean';objects={}
  assert lib.is_dir() or p['name']=='Cli','Unprepared dependency: '+p['name']
  for row in closure:
   if row['package']!=p['name']:continue
   src=row['source_path'];rel=row['object_relative_path'];f=lib/rel
   assert src in tracked,'Untracked dependency-object source: '+src
   assert sha(d/src)==row['source_sha256'],'Pinned source closure changed: '+src
   assert f.is_file(),'Missing prepared dependency object: '+rel
   objects[rel]=sha(f)
  records.append({'package':p['name'],'revision':p['rev'],'object_hashes':objects})
 paths=[deps/p['name']/'.lake/build/lib/lean' for p in pins]
 out.mkdir(parents=True);start=time.monotonic()
 build=compile_project(PACKAGE,out/'project-build',lean,paths)
 controls=run_controls(PACKAGE,out/'project-build',out/'controls',lean,paths)
 check_source_locks(PACKAGE)
 for r in records:
  lib=deps/r['package']/'.lake/build/lib/lean'
  assert all(sha(lib/name)==digest for name,digest in r['object_hashes'].items()),'A required reused dependency object changed'
 result={'status':'PASS','candidate':'new recovered-v1 integration','source_package_integrity_sha256':sha(PACKAGE/'FILE_INTEGRITY.json'),'lean_version':version,'lean_binary_sha256':sha(lean),'fresh_mathematical_sources':build['fresh_mathematical_modules'],'project_object_reuse':False,'new_dependency_cold_build':False,'prepared_dependency_object_reuse':True,'dependency_bindings':records,'controls_executed':controls['executed_control_files'],'control_counts':controls['role_counts'],'control_recovery_statuses':controls['restoration_counts'],'proof_coverage':controls['coverage'],'constructor_retention':controls['packaged_constructor_check'],'elapsed_seconds':round(time.monotonic()-start,3),'native_compiler_and_ffi_unverified':True}
 (out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n');print('RECOVERED_SIXTEENTH_SOURCE_PACKAGE_REPLAY_PASS',flush=True)
if __name__=='__main__':main()
