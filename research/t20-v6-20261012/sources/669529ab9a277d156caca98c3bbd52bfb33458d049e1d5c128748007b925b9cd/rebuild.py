from pathlib import Path
import os,json,re,hashlib,subprocess,datetime,sys
R=Path(__file__).resolve().parent
L=Path('private-locator:4211d241978f643cb623')
M=Path('private-locator:41bd9f979012c8bbc235')
H=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
NOW=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
S=R/'sources'; B=R/'lib'; E=R/'evidence'
main=sys.argv[1:] or ['P01DependentModel','P01DependentSubstitution','P01DependentFundamental','P01DependentControls']
roots=[Path('private-locator:2f5cad8da7ca52b2ae7a'),Path('private-locator:c8d14264d664a4de8512'),Path('private-locator:f27ed1fe8acaf6f42e17')]
rec={'started_utc':NOW(),'status':'RUNNING','main_modules':main,'compiler_path':str(L),'compiler_sha256':H(L),'compiler':subprocess.check_output([str(L),'--version'],text=True).strip(),'sources':{},'builds':[]}
assert '4.19.0' in rec['compiler'] and '6caaee842e94' in rec['compiler']
rec['mathlib_commit']=subprocess.check_output(['git','-C',str(M),'rev-parse','HEAD'],text=True).strip();assert rec['mathlib_commit']=='c44e0c8ee63ca166450922a373c7409c5d26b00b'
rec['canonical_commit']=subprocess.check_output(['git','-C','private-locator:36fb2027a2cd56fb6b89','rev-parse','HEAD'],text=True).strip();assert rec['canonical_commit']=='03e2604dfcef278b01c60d19b05370fcec4194b6'
paths=[B,M/'.lake/build/lib/lean']+[p/'.lake/build/lib/lean' for p in (M/'.lake/packages').iterdir() if p.is_dir()]
env=dict(os.environ);env['LEAN_PATH']=':'.join(map(str,paths));env.pop('LEAN_SYSROOT',None);rec['lean_path']=env['LEAN_PATH']
order=[];seen=set()
def visit(n):
 if n in seen:return
 p=next((r/(n.replace('.','/')+'.lean') for r in roots if (r/(n.replace('.','/')+'.lean')).is_file()),None)
 if p is None:return
 seen.add(n)
 for ln in p.read_text().splitlines():
  if ln.startswith('import '):
   for d in ln[7:].split():visit(d)
 dest=S/(n.replace('.','/')+'.lean');dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(p.read_bytes());rec['sources'][n]={'origin':str(p),'sha256':H(p),'bytes':p.stat().st_size};order.append(n)
for n in main:visit(n)
def save(): (R/'RESULT.json').write_text(json.dumps(rec,indent=2)+'\n')
try:
 for n in order:
  op=B/(n.replace('.','/')+'.olean');op.parent.mkdir(parents=True,exist_ok=True)
  args=[str(L),'-j1','--root='+str(S),'-o',str(op),str(S/(n.replace('.','/')+'.lean'))]
  p=subprocess.run(args,cwd=S,env=env,capture_output=True,timeout=600)
  (E/(n+'.stdout')).write_bytes(p.stdout);(E/(n+'.stderr')).write_bytes(p.stderr)
  rec['builds'].append({'name':n,'command':args,'exit_code':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest()});save()
  print(n,p.returncode,flush=True)
  assert p.returncode==0 and not re.search(rb'error:|sorryAx|declaration uses',p.stdout+p.stderr),(n,p.stdout,p.stderr)
  rec['sources'][n]['olean_sha256']=H(op);save()
 rec['status']='PRESEAL_SNAPSHOT_FRESH_BUILD_PASS';rec['finished_utc']=NOW();save()
except BaseException as e:rec['status']='FAIL';rec['error']=repr(e);save();raise
