from pathlib import Path
import hashlib,json,subprocess,os,zipfile,time,re
R=Path(__file__).resolve().parent;S=Path('private-locator:320aa9aa9e0c2d2d5bd0');A=S.parent/'Mealy_Measure_Bridge_Stage3_20260930.zip';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert not (R/'ATOMS_STAGE_AUDIT_RESULT.json').exists(),'Existing atoms audit requires reconciliation, not rerun'
assert sha(A)=='9533e5bbd7023c113141391e87bd597d76a77528822e65532405c14b7a3ee962'
for line in (S/'SHA256SUMS').read_text().splitlines():
 h,p=line.split(maxsplit=1);assert sha(S/p)==h,p
with zipfile.ZipFile(A) as z:
 for p in S.rglob('*'):
  if p.is_file():
   name=next((n for n in z.namelist() if n.endswith('/'+str(p.relative_to(S))) or n==str(p.relative_to(S))),None);assert name and z.read(name)==p.read_bytes(),str(p)
manifest=json.loads((R/'manifest.json').read_text())
for mod,v in manifest['sources'].items():
 if Path(v['origin']).parent.name=='sealed-v1':assert sha(S/(mod+'.lean'))==v['sha256'],mod
for mod in ['MealySolver','MealySolverFixtures','SolverVerification']:assert sha(S/(mod+'.lean'))==sha(R/'solver-sources'/(mod+'.lean')),mod
D=R/'atoms-sources';O=R/'atoms-build';L=R/'atoms-receipts';[p.mkdir(exist_ok=True) for p in [D,O,L]]
mods=['TargetMass','PositiveAtomMass','AtomEnumeration','GeneratorEquality','EffectiveAtoms','AtomicReconstruction','AtomicApproximation','TargetMassFixtures','AtomicApproximationFixtures','AtomVerification']
for mod in mods:(D/(mod+'.lean')).write_bytes((S/(mod+'.lean')).read_bytes())
env={**os.environ};ev=subprocess.check_output(['bash','-c','source '+str(R/'env.sh')+'; env -0']);env.update(dict(v.decode().split('=',1) for v in ev.split(b'\0') if b'=' in v));env['LEAN_PATH']=str(O)+':'+str(R/'solver-build')+':'+env['LEAN_PATH'];res=[]
for n in mods:
 d=D/(n+'.lean');cmd=['lean','-j1','--root='+str(D),'-o',str(O/(n+'.olean')),str(d)];t=time.time();run=subprocess.run(cmd,env=env,cwd=D,capture_output=True,text=True);(L/(n+'.log')).write_text(run.stdout+run.stderr);row={'module':n,'sha256':sha(d),'command':cmd,'exit':run.returncode,'seconds':time.time()-t};res.append(row);print(row,flush=True);assert run.returncode==0,(run.stdout,run.stderr)
out=(L/'AtomVerification.log').read_text();ax={n:sorted(x.strip() for x in a.split(',') if x.strip()) for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out)}
for n in re.findall(r"'([^']+)' does not depend on any axioms",out):ax[n]=[]
expected={'Orthemology.Frontier.MealyMeasure.'+l.removeprefix('#print axioms ') for l in (D/'AtomVerification.lean').read_text().splitlines() if l.startswith('#print axioms ')}
assert set(ax)==expected;assert len(ax)==39;assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in ax.values())
for mod in mods:assert sha(S/(mod+'.lean'))==sha(D/(mod+'.lean'))
result={'status':'INDEPENDENT_ATOMIC_RECONSTRUCTION_AND_APPROXIMATION_PASS','archive_sha256':sha(A),'builds':res,'new_axiom_targets':ax,'new_target_count':39,'prior_stage_sources_unchanged':True,'scope':'Exact generated-target singleton mass, duplicate-free enumeration with skips, actual atomic restriction reconstruction and terminating residual atomic approximation modulus. No nth-positive-atom selector or approximation to unremoved diffuse measure.'};(R/'ATOMS_STAGE_AUDIT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print('ATOMS_STAGE_PASS',flush=True)
