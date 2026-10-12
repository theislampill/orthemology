from pathlib import Path
import hashlib,json,subprocess,os,time,re,zipfile
R=Path(__file__).resolve().parent;T=Path('private-locator:1dc07ecc133a6053717a');S=T/'sealed-v2';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
A=T/'Tagged_Prefix_Primrec_Successor_20260930.zip';assert sha(A)=='f9a1a33ffd9ad62b711674caed952e26d403dc55084a26faa3bb8285469cfe6d';rec=T/'receipts/20260930T154454Z/RESULT.json';assert sha(rec)=='506f25fd9b149b43b15a5f5980a22da6eefbf4cb340270ac7c7c5e5a4c507bda';d=json.loads(rec.read_text());old=json.loads((T/'sealed-v1/RESULT.json').read_text())
assert not (R/'PREFIX_STAGE_AUDIT_RESULT.json').exists(),'Existing prefix audit requires reconciliation, not rerun'
with zipfile.ZipFile(A) as z:
 for p in S.rglob('*'):
  if p.is_file():
   name=next((n for n in z.namelist() if n.endswith('/'+str(p.relative_to(S))) or n==str(p.relative_to(S))),None);assert name and z.read(name)==p.read_bytes(),str(p)
for n,v in old['sources'].items():assert d['sources'][n]['sha256']==v['sha256'];assert sha(R/'tagged-sources'/(n.replace('.','/')+'.lean'))==v['sha256']
D=R/'prefix-sources';O=R/'prefix-build';L=R/'prefix-receipts';[p.mkdir(exist_ok=True) for p in [D,O,L]]
new=[n for n in d['order'] if n not in old['sources']];targets=[n for n in d['targets'] if n not in old['targets']];assert len(new)==6 and len(targets)==24
for n in new:
 p=S/'sources'/(n+'.lean');assert sha(p)==d['sources'][n]['sha256'];(D/p.name).write_bytes(p.read_bytes())
audit='\n'.join('import '+n for n in new)+'\n'+''.join('#check @'+n+'\n#print axioms '+n+'\n' for n in targets);(D/'PrefixAudit.lean').write_text(audit)
env={**os.environ};ev=subprocess.check_output(['bash','-c','source '+str(R/'tagged-env.sh')+'; env -0']);env.update(dict(v.decode().split('=',1) for v in ev.split(b'\0') if b'=' in v));env['LEAN_PATH']=str(O)+':'+env['LEAN_PATH'];res=[]
for n in new+['PrefixAudit']:
 p=D/(n+'.lean');cmd=['lean','-j1','--root='+str(D),'-o',str(O/(n+'.olean')),str(p)];t=time.time();p1=subprocess.run(cmd,env=env,cwd=D,capture_output=True,text=True);(L/(n+'.log')).write_text(p1.stdout+p1.stderr);row={'module':n,'sha256':sha(p),'command':cmd,'exit':p1.returncode,'seconds':time.time()-t};res.append(row);print(row,flush=True);assert p1.returncode==0,(p1.stdout,p1.stderr)
out=(L/'PrefixAudit.log').read_text();ax={n:sorted(x.strip() for x in a.split(',') if x.strip()) for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out)}
for n in re.findall(r"'([^']+)' does not depend on any axioms",out):ax[n]=[]
assert set(ax)==set(targets);assert len(ax)==24;assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in ax.values())
for n,v in d['sources'].items():assert sha(Path(v['origin']))==v['sha256'],n
result={'status':'INDEPENDENT_PRODUCTIVE_PREFIX_AUDIT_PASSED','archive_sha256':sha(A),'author_receipt_sha256':sha(rec),'new_modules':6,'new_target_count':24,'prior_35_targets_not_recounted':True,'builds':res,'axioms':ax,'scope':'Actual finite-prefix output equals sealed tagged observer, and joint PR under a fixed jointly PR matrix premise; no generated AST/numeric codec or hierarchy completeness claim.'};(R/'PREFIX_STAGE_AUDIT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print('PREFIX_STAGE_PASS',flush=True)
