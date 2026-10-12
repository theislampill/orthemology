from pathlib import Path
import os,sys,subprocess,json,datetime,time,hashlib
A=Path(__file__).resolve().parents[1]
label,cwd,*cmd=sys.argv[1:]
env=dict(os.environ);env.update(json.loads((A/'environment.json').read_text()))
# Do not carry inherited Lean/Lake setup into this source-only build.
for k in ['LEAN_SYSROOT','LEAN_HOME','LAKE_HOME','ELAN_TOOLCHAIN','LD_PRELOAD']:
 env.pop(k,None)
start=datetime.datetime.now(datetime.timezone.utc);begin=time.monotonic();log=A/'evidence'/f'{label}.log'
record={'label':label,'cwd':cwd,'command':cmd,'start_utc':start.isoformat(),'environment_overrides':json.loads((A/'environment.json').read_text()),'status':'RUNNING'}
(A/'evidence'/f'{label}.json').write_text(json.dumps(record,indent=2)+'\n')
with log.open('w') as f:
 r=subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT)
record.update(status='PASS' if r.returncode==0 else 'FAIL',exit_code=r.returncode,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),seconds=round(time.monotonic()-begin,3),log_sha256=hashlib.sha256(log.read_bytes()).hexdigest())
(A/'evidence'/f'{label}.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2));sys.exit(r.returncode)
