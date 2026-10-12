import os,subprocess,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parent;W=R.parent;A=W/'rational-threshold-formal-extension-20261011'
env=dict(os.environ,LEAN_PATH=str(R/'kernel')+':'+(A/'lean_path.txt').read_text().strip());out=[]
for p in sorted((A/'negative-controls').glob('*.lean')):
 r=subprocess.run([str(W/'.toolchains/lean-4.19.0-linux/bin/lean'),'--trust=0',str(p)],cwd=W,env=env,text=True,capture_output=True)
 log=r.stdout+r.stderr;(R/'kernel'/p.with_suffix('.negative.log').name).write_text(log)
 assert r.returncode!=0 and 'false' in log,log
 out.append({'source':str(p),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exit_code':r.returncode,'rejected_as_false':True})
 print('EXPECTED REJECT',p.name,flush=True)
(R/'NEGATIVES.json').write_text(json.dumps(out,indent=2)+'\n')
