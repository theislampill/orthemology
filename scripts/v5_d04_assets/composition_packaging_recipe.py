"""PRIVATE unexecuted translation of the four optional projection tests.

The original test uses temporary children of its own source directory. An exact
two-file disposable copy keeps all of those writes outside the input archive.
This confers packaging evidence only; no Lean or scientific assertion executes.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,re,signal,subprocess

PINS={'verify_projection.py':'33643c09fee29687c966f944b4fde3d91b480ca6547f2d6cca6cb7044c2eaae0',
      'packaging-tests/test_projection.py':'ce95f6bb2ab3353ee4360b093700b7ba85c2817d962b5efe16b2408e41e31880'}
PYTHON_SHA='d1483a82342508f2ec2b172b788d5b676a59eaf70ed01ae846a0f84f63a3a82a'
NAMES=['test_exact_projection_passes','test_excluded_process_file_fails','test_missing_retained_file_fails','test_modified_science_fails']
def require(value,message):
    if not value:raise ValueError(message)
def sha(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def write(path,value):Path(path).write_text(json.dumps(value,sort_keys=True,indent=2)+'\n')
def interrupted(signum,frame):raise KeyboardInterrupt('Packaging translation interrupted')

def main():
    p=argparse.ArgumentParser();p.add_argument('--source-root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--python',type=Path,required=True);a=p.parse_args()
    source=a.source_root.absolute();out=a.output.absolute();python=a.python.resolve()
    require(source.is_dir() and not source.is_symlink(),'Missing source root')
    require(not out.exists() and not out.resolve().is_relative_to(source.resolve()),'Fresh external output required')
    require(sha(python)==PYTHON_SHA,'Wrong pinned interpreter')
    for rel,h in PINS.items():require(sha(source/rel)==h,'Original packaging source changed')
    out.mkdir(parents=True);work=out/'work';work.mkdir();(out/'logs').mkdir()
    for rel,h in PINS.items():
        dst=work/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes((source/rel).read_bytes())
    env={k:v for k,v in os.environ.items() if not k.startswith(('PYTHON','LEAN_','LD_')) and k!='DYLD_INSERT_LIBRARIES'}
    env.update(PYTHONDONTWRITEBYTECODE='1',PATH=os.pathsep.join([str(python.parent),os.defpath]))
    argv=[str(python),'-B','-m','unittest','discover','-s','packaging-tests','-p','test_*.py','-v']
    row={'id':'packaging-unittest','argv':argv,'cwd':str(work),'budget_seconds':120,'started_at':now(),'terminal':'RUNNING','exit_code':None}
    log=out/'logs/packaging-unittest.log';write(out/'STAGES.json',[row]);signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
    with log.open('xb') as stream:
        proc=subprocess.Popen(argv,cwd=work,env=env,stdout=stream,stderr=subprocess.STDOUT,shell=False)
        try:
            code=proc.wait(timeout=120);row.update(terminal='COMPLETED' if 0<=code<124 else 'INTERRUPTED',exit_code=code if 0<=code<124 else None)
        except subprocess.TimeoutExpired:
            row['terminal']='TIMEOUT';proc.terminate()
            try:proc.wait(timeout=2)
            except subprocess.TimeoutExpired:proc.kill();proc.wait()
        except BaseException:
            row['terminal']='INTERRUPTED'
            if proc.poll() is None:
                proc.terminate()
                try:proc.wait(timeout=2)
                except subprocess.TimeoutExpired:proc.kill();proc.wait()
            raise
        finally:
            stream.flush();row.update(ended_at=now(),log_sha256=sha(log));write(out/'STAGES.json',[row])
    text=log.read_text();require(row['terminal']=='COMPLETED' and row['exit_code']==0,'Packaging tests did not complete')
    require(re.search(r'Ran 4 tests in ',text) and re.search(r'(?m)^OK\s*$',text),'Packaging test count/terminal differs')
    for name in NAMES:require(re.search(r'(?m)^'+re.escape(name)+r' \([^\n]+\) \.\.\. ok$',text),'Missing original packaging test '+name)
    require({p.relative_to(work).as_posix() for p in work.rglob('*') if p.is_file()}==set(PINS),'Disposable packaging work files differ')
    for rel,h in PINS.items():require(sha(source/rel)==sha(work/rel)==h,'Packaging source bytes changed')
    write(out/'PACKAGING_RECEIPT.json',{'status':'PASS_OPTIONAL_SOURCE_PACKAGING_TESTS','source_hashes':PINS,'tests':NAMES,'stages':[row],
        'scope':'Four original optional packaging controls in an exact disposable two-file copy. No mathematical or native-runtime credit.'})
if __name__=='__main__':main()
