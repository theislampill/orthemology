"""Run one local evidence command and retain exact output/exit/environment metadata."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, platform, subprocess, sys, time

def main() -> int:
    p=argparse.ArgumentParser()
    p.add_argument('--label',required=True);p.add_argument('--cwd',required=True)
    p.add_argument('--timeout',type=float,default=35);p.add_argument('command',nargs=argparse.REMAINDER)
    a=p.parse_args();cmd=a.command[1:] if a.command[:1]==['--'] else a.command
    root=Path(__file__).resolve().parents[1];out=root/'evidence'/a.label
    out.mkdir(parents=True,exist_ok=False)
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1';env['PYTHONHASHSEED']='0'
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();clock=time.monotonic()
    timed=False
    try:
        r=subprocess.run(cmd,cwd=a.cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=a.timeout)
        code,stdout,stderr=r.returncode,r.stdout,r.stderr
    except subprocess.TimeoutExpired as ex:
        timed=True;code=124;stdout=ex.stdout or b'';stderr=ex.stderr or b''
    except OSError as ex:
        code=127;stdout=b'';stderr=(repr(ex)+'\n').encode()
    (out/'stdout.bin').write_bytes(stdout);(out/'stderr.bin').write_bytes(stderr)
    record={'command':cmd,'cwd':a.cwd,'started_utc':start,'ended_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'elapsed_seconds':time.monotonic()-clock,'exit_code':code,'timed_out':timed,'python':sys.version,'executable':sys.executable,
      'platform':platform.platform(),'environment':{k:env.get(k) for k in ('PYTHONDONTWRITEBYTECODE','PYTHONHASHSEED','PATH','PYTHONPATH','P03_SOURCE')},
      'capture_script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
      'stdout':{'bytes':len(stdout),'sha256':hashlib.sha256(stdout).hexdigest()},'stderr':{'bytes':len(stderr),'sha256':hashlib.sha256(stderr).hexdigest()}}
    for item in cmd:
        path=Path(item)
        if path.is_file():record.setdefault('command_file_hashes',{})[str(path)]=hashlib.sha256(path.read_bytes()).hexdigest()
    (out/'command.json').write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record,indent=2));print(stdout.decode(errors='replace'));print(stderr.decode(errors='replace'),file=sys.stderr)
    return code
if __name__=='__main__':raise SystemExit(main())
