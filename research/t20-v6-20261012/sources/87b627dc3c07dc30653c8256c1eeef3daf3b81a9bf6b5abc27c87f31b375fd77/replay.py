from pathlib import Path
import os,sys,json,hashlib,subprocess,time
R=Path(__file__).resolve().parent; W=R.parent
L=W/'.toolchains/lean-4.19.0-linux/bin/lean'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
modules=['UniquenessConverse','IndependentControls','DependencyAudit']
paths=(R/'lean_path.txt').read_text().strip();records=[]
for m in modules:
 p=R/'sources'/f'{m}.lean';o=R/'fresh-lib'/f'{m}.olean';log=R/'logs'/f'{m}.log'
 cmd=[str(L),'--trust=0','-o',str(o),str(p)];start=time.time()
 x=subprocess.run(cmd,env={**os.environ,'LEAN_PATH':paths},capture_output=True,text=True);log.write_text(x.stdout+x.stderr)
 records.append({'module':m,'command':cmd,'source_sha256':sha(p),'object_sha256':sha(o) if o.exists() else None,'log_sha256':sha(log),'exit_code':x.returncode,'seconds':time.time()-start})
 (R/'REPLAY.json').write_text(json.dumps(records,indent=2)+'\n');print(m,x.returncode,flush=True)
 if x.returncode:sys.exit(x.returncode)
