from pathlib import Path
import os,json,subprocess,sys,time,hashlib
R=Path(__file__).resolve().parent;W=R.parent;e=json.loads((R/'env.json').read_text());env={**os.environ,'LEAN_PATH':e['LEAN_PATH']}
for n in sys.argv[1:]:
 src=R/'sources'/(n+'.lean');obj=R/'output'/(n+'.olean');cmd=[e['lean'],'--trust=0','-o',str(obj),str(src)];t=time.monotonic();p=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(R/'output'/(n+'.log')).write_text(p.stdout);print(n,p.returncode,'seconds',time.monotonic()-t);print(p.stdout);assert p.returncode==0
