#!/usr/bin/env python3
"""Run one local command, keeping unmodified streams and its actual exit status."""
import argparse,datetime,hashlib,json,os,platform,subprocess,sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--prefix',required=True);p.add_argument('--cwd',required=True);p.add_argument('--timeout',type=int,default=45);p.add_argument('command',nargs=argparse.REMAINDER)
a=p.parse_args();cmd=a.command[1:] if a.command[:1]==['--'] else a.command
if not cmd:p.error('command required')
pre=Path(a.prefix);pre.parent.mkdir(parents=True,exist_ok=True)
meta={'argv':cmd,'cwd':a.cwd,'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'platform':platform.platform(),'python':sys.version,'timeout_seconds':a.timeout}
try:
 r=subprocess.run(cmd,cwd=a.cwd,capture_output=True,timeout=a.timeout,check=False)
 out,err,code=r.stdout,r.stderr,r.returncode
except subprocess.TimeoutExpired as e:out,err,code=e.stdout or b'',(e.stderr or b'')+b'\nRECORDER: TIMEOUT\n',124
except OSError as e:out,err,code=b'',str(e).encode(),127
for suffix,b in [('stdout',out),('stderr',err),('exit',(str(code)+'\n').encode())]:Path(str(pre)+'.'+suffix).write_bytes(b)
meta.update(exit=code,finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),stdout_sha256=hashlib.sha256(out).hexdigest(),stderr_sha256=hashlib.sha256(err).hexdigest())
Path(str(pre)+'.command.json').write_text(json.dumps(meta,indent=2)+'\n')
print(json.dumps({'exit':code,'prefix':str(pre)}));sys.exit(code)
