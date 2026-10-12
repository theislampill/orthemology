#!/usr/bin/env python3
"""Run a local research command and persist raw streams, exits and file identities."""
import datetime,hashlib,json,os,pathlib,platform,subprocess,sys,time
out=pathlib.Path(sys.argv[1]);cwd=pathlib.Path(sys.argv[2]);cmd=sys.argv[3:]
out.mkdir(parents=True,exist_ok=False)
def files():
 return {str(p.relative_to(cwd)):{'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(cwd.glob('*.py'))}
pre=files(); start=datetime.datetime.now(datetime.timezone.utc).isoformat(); t=time.monotonic()
r=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
(out/'stdout.bin').write_bytes(r.stdout);(out/'stderr.bin').write_bytes(r.stderr)
rec={'command':cmd,'cwd':str(cwd),'start_utc':start,'elapsed_seconds':time.monotonic()-t,'exit_code':r.returncode,'python':sys.version,'platform':platform.platform(),'source_preimages':pre,'source_postimages':files(),'stdout_bytes':len(r.stdout),'stderr_bytes':len(r.stderr),'stdout_sha256':hashlib.sha256(r.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr).hexdigest()}
(out/'COMMAND.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps({k:rec[k] for k in ['command','exit_code','elapsed_seconds','stdout_bytes','stderr_bytes']},indent=2));sys.exit(r.returncode)
