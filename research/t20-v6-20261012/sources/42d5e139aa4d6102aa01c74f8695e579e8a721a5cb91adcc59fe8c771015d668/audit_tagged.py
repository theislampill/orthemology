from pathlib import Path
import hashlib,json,subprocess,os,time,re,zipfile
R=Path(__file__).resolve().parent;T=Path('private-locator:1dc07ecc133a6053717a');S=T/'sealed-v1';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
A=T/'Tagged_Row_Measure_Bridge_20260930.zip';assert sha(A)=='7f1dc1ecce6717ff02cd9349dfe96635e3e0741e87291ca80f3de13f66b88ca9'
rec=T/'receipts/20260930T151445Z/RESULT.json';assert sha(rec)=='294054cc309ac7cf86e4193b8f1d8e098694fe20c2b21304cf13a183967dbafc';data=json.loads(rec.read_text());assert (S/'RESULT.json').read_bytes()==rec.read_bytes()
with zipfile.ZipFile(A) as z:
 for p in S.rglob('*'):
  if p.is_file():
   name=next((n for n in z.namelist() if n.endswith('/'+str(p.relative_to(S))) or n==str(p.relative_to(S))),None);assert name and z.read(name)==p.read_bytes(),str(p)
D=R/'tagged-sources';O=R/'tagged-build';L=R/'tagged-receipts';[p.mkdir(exist_ok=True) for p in [D,O,L]]
for n,v in data['sources'].items():
 p=S/'sources'/(n.replace('.','/')+'.lean');assert sha(p)==v['sha256'];d=D/p.relative_to(S/'sources');d.parent.mkdir(exist_ok=True,parents=True);d.write_bytes(p.read_bytes());assert sha(Path(v['origin']))==v['sha256'],n
(D/'Audit.lean').write_bytes((S/'sources/Audit.lean').read_bytes())
env={**os.environ};ev=subprocess.check_output(['bash','-c','source '+str(R/'env.sh')+'; env -0']);env.update(dict(v.decode().split('=',1) for v in ev.split(b'\0') if b'=' in v));env['LEAN_PATH']=str(O)+':'+':'.join(env['LEAN_PATH'].split(':')[1:]);res=[]
for n in data['order']+['Audit']:
 d=D/(n.replace('.','/')+'.lean');o=O/(n.replace('.','/')+'.olean');o.parent.mkdir(exist_ok=True,parents=True);cmd=['lean','-j1','--root='+str(D),'-o',str(o),str(d)];t=time.time();run=subprocess.run(cmd,env=env,cwd=D,capture_output=True,text=True)
 (L/(n+'.log')).write_text(run.stdout+run.stderr);row={'module':n,'source_sha256':sha(d),'command':cmd,'exit':run.returncode,'seconds':time.time()-t};res.append(row);print(row,flush=True);assert run.returncode==0,(run.stdout,run.stderr)
out=(L/'Audit.log').read_text();ax={n:sorted(x.strip() for x in a.split(',') if x.strip()) for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out)}
for n in re.findall(r"'([^']+)' does not depend on any axioms",out):ax[n]=[]
assert set(ax)==set(data['targets']);assert len(ax)==35;assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in ax.values())
for n,v in data['sources'].items():assert sha(Path(v['origin']))==v['sha256'],n
result={'status':'INDEPENDENT_TAGGED_ACTUAL_LAW_REBUILD_PASSED','archive_sha256':sha(A),'receipt_sha256':sha(rec),'builds':res,'axiom_readbacks':ax,'sources_preserved':True,'scope':'Actual fair prefix/tail disintegration and tagged-row law; semantic Pi3-shaped endpoints, no effective hierarchy reduction.'}
(R/'TAGGED_STAGE_AUDIT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print('TAGGED_STAGE_PASS',flush=True)
