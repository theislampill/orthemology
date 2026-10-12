from pathlib import Path
import json,os,subprocess,sys
R=Path(__file__).resolve().parent;W=R.parent;e=json.loads((R/'env.json').read_text());src=Path(sys.argv[1]);out=R/'output'/src.with_suffix('.log').name
p=subprocess.run([e['lean'],'--trust=0','-o',str(R/'output'/src.with_suffix('.olean').name),str(src)],cwd=W,env={**os.environ,'LEAN_PATH':e['LEAN_PATH']},text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);out.write_text(p.stdout);print(p.stdout);print('EXIT',p.returncode)
raise SystemExit(p.returncode)
