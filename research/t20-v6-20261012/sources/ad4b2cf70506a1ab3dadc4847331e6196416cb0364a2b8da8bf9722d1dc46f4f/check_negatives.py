from pathlib import Path
import json,subprocess,os,time,hashlib
R=Path(__file__).resolve().parent;W=R.parent;e=json.loads((R/'env.json').read_text());env={**os.environ,'LEAN_PATH':e['LEAN_PATH']};results=[]
def rec(p):return {'path':str(p.relative_to(W)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
cached={x['name']:x for x in json.loads((R/'INDEPENDENT_NEGATIVE_RESULTS.json').read_text())} if (R/'INDEPENDENT_NEGATIVE_RESULTS.json').exists() else {}
for n in json.loads((R/'INDEPENDENT_NEGATIVE_TARGETS.json').read_text()):
 if n in cached:
  v=cached[n];assert rec(W/v['source']['path'])==v['source'];assert rec(W/v['log']['path'])==v['log'];results.append(v);continue
 src=R/'negative'/(n+'.lean');t=time.monotonic();p=subprocess.run([e['lean'],'--trust=0',str(src)],env=env,cwd=W,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=R/'output'/(n+'.log');log.write_text(p.stdout)
 expected="tactic 'decide' proved that the proposition";assert p.returncode!=0 and expected in p.stdout and not any(x in p.stdout for x in ['unknown identifier','unexpected token','failed to import','unknown module']),str(log)
 results.append({'name':n,'source':rec(src),'log':rec(log),'exit_code':p.returncode,'expected_rejection':expected,'seconds':time.monotonic()-t});(R/'INDEPENDENT_NEGATIVE_RESULTS.json').write_text(json.dumps(results,indent=2)+'\n');print('REJECTED',n,flush=True)
