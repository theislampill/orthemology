#!/usr/bin/env python3
"""PRIVATE source-bound translation of composition reviewer terminal stages.

Unexecuted; D03 approval must bind this script to the supplied reviewer Lean
sources and verify_terminal.py. No accepted source or preceding build changes.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,re,signal,subprocess

PINS={'independent-review/verify_terminal.py':'877c22d3527b5b43925e01e68c727b1f38ba392d96e1d43b187c6d9ada4777b1',
      'independent-review/extended-v2/IndependentTests.lean':'db9041027ecf36b058a6c9f62f2dec495882066f6a3b09f0f4eeb4f79801a26e',
      'independent-review/extended-v2/ReviewerMonotonicity.lean':'1a309a2ea8ca97510f94160db9ccbd5cea346e04f4e12403eabbb589bd91701a'}
LEAN_SHA='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
LEANC_SHA='39a4d993906671c6b2eec9e75053aff3917fd1d4530706f32a273aa8f283ab41'
FIXTURE_SHA='e4ae2e2751535e625f245a1bb2f2e4f2f4c447a55c859e1b1c94dbbf48adf359'
ACTIVE=None
def require(value,message):
    if not value:raise ValueError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def write(path,data):Path(path).write_text(json.dumps(data,indent=2,sort_keys=True)+'\n')
def inventory(root):
    result={}
    for p in sorted(root.rglob('*')):
        require(not p.is_symlink(),'Symlink in source/build')
        if p.is_file():result[p.relative_to(root).as_posix()]=sha(p)
    return result
def stop():
    if ACTIVE is not None and ACTIVE.poll() is None:
        os.killpg(ACTIVE.pid,signal.SIGTERM)
        try:ACTIVE.wait(timeout=2)
        except subprocess.TimeoutExpired:os.killpg(ACTIVE.pid,signal.SIGKILL);ACTIVE.wait()
def interrupted(signum,frame):stop();raise SystemExit(128+signum)
def main():
    global ACTIVE
    ap=argparse.ArgumentParser();ap.add_argument('--source-root',type=Path,required=True);ap.add_argument('--clean-build',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True);ap.add_argument('--lean',type=Path,required=True);a=ap.parse_args()
    source=a.source_root.absolute();clean=a.clean_build.absolute();out=a.output.absolute();lean=a.lean.resolve();leanc=lean.with_name('leanc')
    require(source.is_dir() and clean.is_dir() and not source.is_symlink() and not clean.is_symlink(),'Missing exact source/fresh build')
    require(not out.exists() and all(not out.resolve().is_relative_to(p.resolve()) for p in [source,clean]),'Output must be fresh and outside inputs')
    require(sha(lean)==LEAN_SHA and sha(leanc)==LEANC_SHA,'Wrong pinned compiler tool pair')
    for rel,h in PINS.items():require(sha(source/rel)==h,'Wrong reviewer source/terminal contract')
    before=inventory(source);clean_before=inventory(clean)
    require((clean/'source.bin').stat().st_size==3013 and sha(clean/'source.bin')==FIXTURE_SHA,'Wrong fresh full-byte source fixture')
    source_modules={'TypedCriterionGuard':'imports/TypedCriterionGuard.lean','CriterionInstallation':'imports/CriterionInstallation.lean',
                    'DynamicInterlock':'imports/DynamicInterlock.lean','Composition':'Composition.lean','Fixtures':'tests/Fixtures.lean'}
    for module,member in source_modules.items():
        require(sha(clean/(module+'.lean'))==before[member],'Original fresh object source differs')
        require((clean/(module+'.c')).is_file() and (clean/(module+'.olean')).is_file(),'Missing original fresh C/object prerequisite')
    out.mkdir(parents=True);build=out/'build';build.mkdir();logs=out/'logs';logs.mkdir()
    env={k:v for k,v in os.environ.items() if not k.startswith(('LD_','LEAN_','PYTHON')) and k!='DYLD_INSERT_LIBRARIES'}
    env.update({'LEAN_PATH':os.pathsep.join(map(str,[build,clean])),'PYTHONDONTWRITEBYTECODE':'1','PATH':os.pathsep.join([str(lean.parent),os.defpath])})
    stages=[];signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    def run(name,argv,budget=300,cwd=build):
        global ACTIVE
        log=logs/(name+'.log');require(not log.exists(),'Child log exists')
        row={'id':name,'argv':[str(x) for x in argv],'cwd':str(cwd),'budget_seconds':budget,'started_at':now(),'terminal':'RUNNING','exit_code':None,'log':'logs/'+name+'.log'}
        stages.append(row);write(out/'STAGES.json',stages)
        with log.open('xb') as stream:
            ACTIVE=subprocess.Popen(row['argv'],cwd=cwd,env=env,stdout=stream,stderr=subprocess.STDOUT,shell=False,start_new_session=True)
            try:
                code=ACTIVE.wait(timeout=budget);row['terminal']='COMPLETED' if 0<=code<124 else 'INTERRUPTED';row['exit_code']=code if row['terminal']=='COMPLETED' else None
            except subprocess.TimeoutExpired:row['terminal']='TIMEOUT';stop()
            except BaseException:row['terminal']='INTERRUPTED';stop();raise
            finally:
                row['ended_at']=now();ACTIVE=None;stream.flush();row['log_sha256']=sha(log);write(out/'STAGES.json',stages)
        require(row['terminal']=='COMPLETED' and row['exit_code']==0,'Reviewer child did not complete successfully: '+name)
        return log.read_text()
    native_source=source/'independent-review/extended-v2/IndependentTests.lean'
    text=run('independent-compile',[lean,'-j1','-o',build/'IndependentTests.olean','-c',build/'IndependentTests.c',native_source],cwd=native_source.parent)
    require(not any(x in text for x in ['error:','warning:','sorryAx']),'Unclean independent native source compile')
    # Supplied terminal checks require this exact reviewer native test program.
    # Explicit linking reconstructs the command from its import closure; it is
    # disclosed as a translation, not presented as an archived command receipt.
    executable=build/'independent-tests'
    run('independent-link',[leanc,'-O1','-o',executable]+[clean/(m+'.c') for m in source_modules]+[build/'IndependentTests.c'])
    text=run('independent-native',[executable,clean/'source.bin'])
    lines=text.splitlines();require(len([x for x in lines if x.startswith('PASS independent:')])==25 and lines[-1]=='INDEPENDENT TERMINAL PASS' and 'FAIL' not in text,'Missing 25 source-prescribed independent native assertions')
    mono=source/'independent-review/extended-v2/ReviewerMonotonicity.lean'
    text=run('reviewer-monotonicity',[lean,'-j1','-o',build/'ReviewerMonotonicity.olean',mono],cwd=mono.parent)
    require(not any(x in text for x in ['error:','warning:','sorryAx']),'Unclean monotonicity proof compile')
    names=re.findall(r"'([^']+)' (?:depends on axioms:|does not depend on any axioms)",text)
    require(len(names)==3 and {x.rsplit('.',1)[-1] for x in names}=={'local_versions_monotone','install_no_replay_after_monotone_progress','repair_no_replay_after_monotone_progress'},'Incomplete exact three monotonicity readbacks')
    for raw in re.findall(r'depends on axioms:\s*\[([^]]*)\]',text):require({x.strip() for x in raw.split(',') if x.strip()}<={'propext','Classical.choice','Quot.sound'},'Unexpected reviewer axiom')
    require(inventory(source)==before and inventory(clean)==clean_before,'Accepted source or preceding fresh build changed')
    write(out/'REVIEW_COMPONENT_RECEIPT.json',{'status':'PASS_SUPPLIED_REVIEW_COMPONENTS','source_contracts':PINS,'independent_native_assertions':25,'reviewer_monotonicity_readbacks':3,
          'stages':stages,'source_before_after_unchanged':True,'preceding_fresh_build_before_after_unchanged':True,'source_fixture_bytes':3013,'source_fixture_sha256':FIXTURE_SHA,
          'translation_scope':'Reconstructed explicit reviewer compile/link/run vectors from exact supplied Lean source import closure and verify_terminal.py; no archived native command is fabricated.'})
if __name__=='__main__':main()
