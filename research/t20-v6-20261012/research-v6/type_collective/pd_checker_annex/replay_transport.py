from pathlib import Path
import hashlib,json,os,subprocess,time
b=Path(__file__).resolve().parent;out=b/'fresh_lean';s=json.loads((b.parent/'ASSIGNED_SOURCE_MAP.json').read_text())['sources'];lean=Path('.toolchains/lean-4.19.0-linux/bin/lean').resolve();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();rows=[]
for i in [8,9,12,10]:
 r=s[f'PD-CHECKER-{i}'];p=Path(r['local_object_path']);assert sha(p)==r['original_sha256'];(out/r['names'][0]).write_bytes(p.read_bytes())
env=dict(os.environ,LEAN_PATH=str(out)+':'+os.environ['LEAN_PATH']);env['LEAN_PATH']=str(out.resolve())+':'+os.environ['LEAN_PATH'];(out/'LEAN_PATH.txt').write_text(env['LEAN_PATH']+'\n')
for name in ['CheckerKernel','CheckerSemantics','InitialCheckerBelief','CheckerStateObservation','FiniteHistoryTransport']:
 p=out/(name+'.lean');cmd=[str(lean),'--trust=0','-j1','-o',name+'.olean',name+'.lean'];start=time.time();r=subprocess.run(cmd,cwd=out,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=out/(name+'.log');log.write_text(r.stdout);rows.append({'module':name,'source_sha256':sha(p),'command':cmd,'cwd':str(out.resolve()),'exit_code':r.returncode,'log_sha256':sha(log),'seconds':time.time()-start});print(name,r.returncode,flush=True)
 (out/'FRESH_COMPILATION.json').write_text(json.dumps({'lean_path':str(lean),'lean_sha256':sha(lean),'LEAN_PATH':env['LEAN_PATH'],'rows':rows,'original_custom_objects_reused':False,'official_objects_trusted':True},indent=2)+'\n')
 if r.returncode:print(r.stdout,flush=True);break
