from pathlib import Path
import hashlib,json,subprocess,os,zipfile,time,re
R=Path(__file__).resolve().parent;S=Path('private-locator:1a489effecf96feb9c4c');A=S.parent/'Mealy_Measure_Bridge_Stage2_20260930.zip';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(A)=='be139a29c285da780a20609b2b60e3cf3551338793030560b61da9ff8656523d'
for line in (S/'SHA256SUMS').read_text().splitlines():
 h,p=line.split(maxsplit=1);assert sha(S/p)==h,p
with zipfile.ZipFile(A) as z:
 for p in S.rglob('*'):
  if p.is_file():
   name=next((n for n in z.namelist() if n.endswith('/'+str(p.relative_to(S))) or n==str(p.relative_to(S))),None);assert name and z.read(name)==p.read_bytes(),str(p)
manifest=json.loads((R/'manifest.json').read_text())
for mod,v in manifest['sources'].items():
 if Path(v['origin']).parent.name=='sealed-v1':assert sha(S/(mod+'.lean'))==v['sha256'],mod
O=R/'solver-build';O.mkdir(exist_ok=True);D=R/'solver-sources';D.mkdir(exist_ok=True);L=R/'solver-receipts';L.mkdir(exist_ok=True)
env={**os.environ};ev=subprocess.check_output(['bash','-c','source '+str(R/'env.sh')+'; env -0']);env.update(dict(v.decode().split('=',1) for v in ev.split(b'\0') if b'=' in v));env['LEAN_PATH']=str(O)+':'+env['LEAN_PATH'];res=[]
for name in ['MealySolver','MealySolverFixtures','SolverVerification']:
 p=S/(name+'.lean');d=D/p.name;d.write_bytes(p.read_bytes());cmd=['lean','-j1','--root='+str(D),'-o',str(O/(name+'.olean')),str(d)]
 t=time.time();run=subprocess.run(cmd,env=env,cwd=D,capture_output=True,text=True);(L/(name+'.log')).write_text(run.stdout+run.stderr)
 row={'module':name,'source_sha256':sha(d),'command':cmd,'exit':run.returncode,'seconds':time.time()-t,'artifact_sha256':sha(O/(name+'.olean')) if run.returncode==0 else None};res.append(row);print(row,flush=True)
 assert run.returncode==0,(run.stdout,run.stderr)
 assert sha(p)==sha(d)
out=(L/'SolverVerification.log').read_text();ax={n:sorted(x.strip() for x in a.split(',') if x.strip()) for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out)}
for n in re.findall(r"'([^']+)' does not depend on any axioms",out):ax[n]=[]
expected={'Orthemology.Frontier.MealyMeasure.'+l.removeprefix('#print axioms ') for l in (D/'SolverVerification.lean').read_text().splitlines() if l.startswith('#print axioms ')}
assert set(ax)==expected;assert len(ax)==11;assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in ax.values())
result={'status':'INDEPENDENT_SOLVER_REBUILD_PASSED','seal_sha256':sha(A),'builds':res,'new_axiom_readbacks':ax,'stage1_source_hashes_unchanged':True,'scope':'Exact executable Lean determinant solver for actual fair-input hitting probability and defect. No Python source/codec/complexity correspondence.'}
(R/'SOLVER_STAGE_AUDIT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print('SOLVER_STAGE_PASS',flush=True)
