"""Verify this selected research addendum; optionally replay its bounded probes.
Python3.10+ standard library only. This confers no philosophical/owner acceptance.
"""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,os,time
ROOT=Path(__file__).resolve().parent

def verify():
    records=json.loads((ROOT/'MANIFEST.json').read_text())['files']
    for r in records:
        p=ROOT/r['path']
        if not p.resolve().is_relative_to(ROOT) or not p.is_file():
            raise RuntimeError('Invalid/missing payload: '+r['path'])
        b=p.read_bytes()
        if len(b)!=r['bytes'] or hashlib.sha256(b).hexdigest()!=r['sha256']:
            raise RuntimeError('Changed payload: '+r['path'])
    return len(records)

p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');args=p.parse_args()
count=verify();receipts=[]
if args.replay:
    prefix='tranche20/research-frontier-continuation/'
    directories=[
      'exact-cooperation-source-audit/sovereignty/src',
      'exact-cooperation-source-audit/composition/src',
      'targeted-efficacy-source-extension/admissibility-contract/src',
      'ameri-source-screen/plurality-bridge-audit/src']
    commands=[[sys.executable,'-B','-m','unittest','discover','-v','-s',prefix+x] for x in directories]
    commands.append([sys.executable,'-B',prefix+'exact-cooperation-source-audit/source-majmu-jami/check_original_support.py'])
    for cmd in commands:
        start=time.monotonic();r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True,timeout=60,env=os.environ|{'PYTHONDONTWRITEBYTECODE':'1'})
        log=r.stdout+r.stderr
        receipts.append({'command':cmd[1:],'exit_code':r.returncode,'execution_seconds':time.monotonic()-start,'log':log})
        if r.returncode:raise RuntimeError(log)
    verify()
print(json.dumps({'status':'PASS','payload_files_verified':count,'python':sys.version,'replay_requested':args.replay,'receipts':receipts,'credit':'27 scoped Python tests and one positive/negative original-root probe when replayed. No new Lean proof, metaphysical warrant, empirical validation, historical active-time certification or T20 closure.'},indent=2))
