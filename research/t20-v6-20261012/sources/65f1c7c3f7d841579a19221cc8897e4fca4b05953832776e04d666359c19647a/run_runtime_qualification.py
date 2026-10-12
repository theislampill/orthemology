from pathlib import Path
import subprocess,os,json,sys,hashlib,datetime
root=Path('private-locator:b161f5e6ec5b32183f0f');out=root/'evidence/python'; records=[]
def run(name,args,cwd,env={}):
 e={**os.environ,'PYTHONDONTWRITEBYTECODE':'1',**env};start=datetime.datetime.now(datetime.timezone.utc).isoformat();p=subprocess.run(args,cwd=cwd,env=e,capture_output=True,timeout=600)
 (out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr)
 record={'label':name,'argv':args,'cwd':str(cwd),'started':start,'exit_code':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()};records.append(record)
 (out/'RUNS.json').write_text(json.dumps(records,indent=2)+'\n');print(name,p.returncode,flush=True)
for label in ['source','canonical']:
 base=root/'python-bases'/label
 for mode,extra in [('normal',[]),('optimised',['-O'])]:
  run(label+'-base-suite-'+mode,[sys.executable,'-B',*extra,'-m','unittest','discover','-s','tests','-v'],base)
  run(label+'-frontier-'+mode,[sys.executable,'-B',*extra,str(root/'shadow/tools/test_new_frontier.py')],root/'shadow',{'P03_BASE':str(base)})
