from pathlib import Path
import os,json,subprocess,sys
R=Path(__file__).resolve().parent;W=R.parent;e=json.loads((R/'env.json').read_text());env={**os.environ,'LEAN_PATH':e['LEAN_PATH']}
for x in sys.argv[1:]:
 src=R/'sources'/(x+'.lean');p=subprocess.run([e['lean'],'--trust=0','-o',str(R/'output'/(x+'.olean')),str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(R/'output'/(x+'.log')).write_text(p.stdout);print(p.stdout,end='');print(x,p.returncode,flush=True)
 if p.returncode:sys.exit(p.returncode)
