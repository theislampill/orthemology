from pathlib import Path
import json,hashlib,subprocess,concurrent.futures,sys
A=Path(__file__).resolve().parent;P=A.parents[1]/'t20-consolidation-20261011/projection/package-v4'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
files=[{'path':p.relative_to(P).as_posix(),'sha256':h(p),'bytes':p.stat().st_size} for p in sorted(P.rglob('*')) if p.is_file() and p.name!='PACKAGE_CONTENTS.json']
(P/'PACKAGE_CONTENTS.json').write_text(json.dumps({'schema':'t20-consolidated-package-contents-v1','scope':'Unsealed v4 staging; exact file integrity only','files':files},indent=2)+'\n')
names=json.loads((P/'depth/PORTABLE_TARGETS.json').read_text())['suites']
if len(sys.argv)>1:names={k:v for k,v in names.items() if k in sys.argv[1:]}
def run(name):
 closure=[{'path':p.relative_to(P).as_posix(),'sha256':h(p),'bytes':p.stat().st_size} for p in sorted((P/'replay'/names[name]['directory']).rglob('*')) if p.is_file()]
 (A/('closure-'+name+'.json')).write_text(json.dumps(closure,indent=2)+'\n')
 r=subprocess.run([sys.executable,'-B',str(P/'replay_selected.py'),'--suite',name],capture_output=True,text=True)
 (A/('replay-'+name+'.json')).write_text(r.stdout);(A/('replay-'+name+'.stderr')).write_text(r.stderr)
 print(name,r.returncode,flush=True)
 return r.returncode
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex: codes=list(ex.map(run,names))
raise SystemExit(any(codes))
