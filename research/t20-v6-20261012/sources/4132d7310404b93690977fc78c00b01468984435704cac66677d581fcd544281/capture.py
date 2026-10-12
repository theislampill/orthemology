#!/usr/bin/env python3
"""Run an explicit command and retain raw, hash-bound execution evidence."""
from pathlib import Path
import datetime,hashlib,json,os,platform,subprocess,sys,time
out=Path(sys.argv[1]);out.mkdir(parents=True,exist_ok=True);argv=sys.argv[2:];start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
try:
 p=subprocess.run(argv,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=float(os.environ.get('CAPTURE_TIMEOUT','35')));code=p.returncode;so=p.stdout;se=p.stderr;launched=True
except FileNotFoundError as e:code=127;so=b'';se=(str(e)+'\n').encode();launched=False
except subprocess.TimeoutExpired as e:code=124;so=e.stdout or b'';se=(e.stderr or b'')+b'\nCAPTURE TIMEOUT\n';launched=True
for n,b in [('stdout',so),('stderr',se)]:(out/(n+'.bin')).write_bytes(b)
r={'argv':argv,'cwd':os.getcwd(),'started_utc':start,'elapsed_seconds':time.monotonic()-t,'exit_code':code,'launched':launched,'python':sys.version,'platform':platform.platform(),'PATH':os.environ.get('PATH'),'ELAN_HOME':os.environ.get('ELAN_HOME'),'LEAN_PATH':os.environ.get('LEAN_PATH'),'stdout_bytes':len(so),'stdout_sha256':hashlib.sha256(so).hexdigest(),'stderr_bytes':len(se),'stderr_sha256':hashlib.sha256(se).hexdigest()}
(out/'command.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));print(so.decode(errors='replace')[-2500:]);print(se.decode(errors='replace')[-2500:],file=sys.stderr);sys.exit(code)
