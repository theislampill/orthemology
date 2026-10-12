from pathlib import Path
import sys,os,json,subprocess,hashlib,datetime,re
R=Path(__file__).resolve().parent; rec=json.loads((R/'RESULT.json').read_text()); name=sys.argv[1];stamp=datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S');p=R/'evidence'/(stamp+'-'+name)
env=dict(os.environ);env['LEAN_PATH']=rec['lean_path'];cmd=[rec['compiler_path'],'-j1','-o',str(R/'lib'/(name+'.olean')),name+'.lean'];s=R/'sources'/(name+'.lean')
x=subprocess.run(cmd,cwd=R/'sources',env=env,capture_output=True,timeout=300)
p.with_suffix('.stdout').write_bytes(x.stdout);p.with_suffix('.stderr').write_bytes(x.stderr)
p.with_suffix('.json').write_text(json.dumps({'command':cmd,'source_sha256':hashlib.sha256(s.read_bytes()).hexdigest(),'exit_code':x.returncode,'stdout_sha256':hashlib.sha256(x.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(x.stderr).hexdigest()},indent=2)+'\n')
print(x.returncode);print(x.stdout.decode());print(x.stderr.decode());sys.exit(x.returncode)
