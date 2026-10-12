from pathlib import Path
import os,subprocess,json,datetime,hashlib,concurrent.futures
R=Path(__file__).resolve().parent;W=R.parent;LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
SRC=R/'baseline';OUT=R/'baseline-build';OUT.mkdir(exist_ok=True)
paths=[p/'.lake/build/lib/lean' for p in (R/'dependency-overlay/.lake/packages').iterdir() if (p/'.lake/build/lib/lean').is_dir()]
env=dict(os.environ,LEAN_PATH=':'.join(map(str,[OUT]+paths)))
(R/'lean_path.txt').write_text(env['LEAN_PATH'])
mods={str(p.relative_to(SRC).with_suffix('')).replace('/','.'):p for p in SRC.rglob('*.lean')}
deps={m:{v for l in p.read_text().splitlines() if l.strip().startswith('import ') for v in l.strip().split()[1:] if v in mods} for m,p in mods.items()}
done=set();rec=[]
def build(m):
 p=mods[m];o=OUT/p.relative_to(SRC).with_suffix('.olean');o.parent.mkdir(parents=True,exist_ok=True)
 result=subprocess.run([str(LEAN),'--trust=0','-o',str(o),str(p)],env=env,cwd=W,capture_output=True,text=True)
 log=OUT/(m+'.log');log.write_text(result.stdout+result.stderr)
 if result.returncode:raise RuntimeError(m+' failed: '+str(log)+'\n'+result.stdout+result.stderr)
 print('PASS '+m,flush=True)
 return {'module':m,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'object_sha256':hashlib.sha256(o.read_bytes()).hexdigest(),'exit_code':result.returncode}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 while len(done)<len(mods):
  ready=[m for m in mods if m not in done and deps[m]<=done]
  if not ready:raise RuntimeError('Cycle')
  results=list(ex.map(build,ready));rec+=results;done.update(ready)
(R/'BASELINE_REBUILD.json').write_text(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trust':0,'modules':rec},indent=2)+'\n')
