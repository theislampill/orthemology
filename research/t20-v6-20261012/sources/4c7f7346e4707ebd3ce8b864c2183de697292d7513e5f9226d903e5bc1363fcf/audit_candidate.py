from pathlib import Path
import hashlib,json,subprocess,os,time,re
R=Path(__file__).resolve().parent;P=Path('private-locator:6e1cdd2685640ba2eef0');sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
S=P/'CANDIDATE_SEAL.json';assert sha(S)=='00b3c06356f9fbdfa4ea1e7bc9fab4b0072faffda6fc834e47ecd2f2c6ff67e0';seal=json.loads(S.read_text())
for p,h in seal['files'].items():assert sha(P/p)==h,p
rec=P/'receipts/candidate-20260930T150947Z/CANDIDATE_RESULT.json';assert sha(rec)=='2beddd3cab8712b85bfb908afc48b73ebaa4af2b5405d7cadc5a08f7e55086d7';data=json.loads(rec.read_text())
D=R/'candidate-sources';O=R/'candidate-build';L=R/'candidate-receipts';[p.mkdir(exist_ok=True) for p in [D,O,L]]
manifest=json.loads((R/'manifest.json').read_text())
for n,v in manifest['sources'].items():assert sha(Path(v['origin']))==v['sha256'],n
(D/'CANDIDATE_SEAL.json').write_bytes(S.read_bytes());(D/'CANDIDATE_RESULT.json').write_bytes(rec.read_bytes());(D/'CANDIDATE_REFINEMENT_SCOPE.md').write_bytes((P/'CANDIDATE_REFINEMENT_SCOPE.md').read_bytes())
env={**os.environ};ev=subprocess.check_output(['bash','-c','source '+str(R/'env.sh')+'; env -0']);env.update(dict(v.decode().split('=',1) for v in ev.split(b'\0') if b'=' in v));env['LEAN_PATH']=str(O)+':'+env['LEAN_PATH'];res=[]
for n in ['CandidateCompiler','CandidateSource','CandidateWitnesses','Sigma2Compiled','CandidateAudit']:
 p=P/(n+'.lean');expected=data['audit_sha256'] if n=='CandidateAudit' else data['source_sha256'][n];assert sha(p)==expected
 d=D/p.name;d.write_bytes(p.read_bytes());cmd=['lean','-j1','--root='+str(D),'-o',str(O/(n+'.olean')),str(d)];t=time.time();run=subprocess.run(cmd,env=env,cwd=D,capture_output=True,text=True)
 (L/(n+'.log')).write_text(run.stdout+run.stderr);row={'module':n,'source_sha256':sha(d),'command':cmd,'exit':run.returncode,'seconds':time.time()-t};res.append(row);print(row,flush=True);assert run.returncode==0,(run.stdout,run.stderr)
out=(L/'CandidateAudit.log').read_text();ax={n:sorted(x.strip() for x in a.split(',') if x.strip()) for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out)}
for n in re.findall(r"'([^']+)' does not depend on any axioms",out):ax[n]=[]
assert set(ax)=={t['declaration'] for t in data['targets']};assert len(ax)==52;assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in ax.values())
controls=[]
for c in data['negative_controls']:
 p=P/'negative-controls'/(c['name']+'.lean');assert sha(p)==c['source_sha256'];d=D/p.name;d.write_bytes(p.read_bytes());cmd=['lean','-j1','--root='+str(D),str(d)];t=time.time();run=subprocess.run(cmd,env=env,cwd=D,capture_output=True,text=True)
 (L/(c['name']+'.log')).write_text(run.stdout+run.stderr);assert run.returncode==c['exit'],(c,run.stdout,run.stderr)
 if run.returncode:assert 'proved that the proposition' in run.stdout and 'false' in run.stdout
 controls.append({'name':c['name'],'sha256':sha(d),'exit':run.returncode,'command':cmd,'seconds':time.time()-t});print('CONTROL_PASS',c['name'],flush=True)
for n,h in data['source_sha256'].items():assert sha(P/(n+'.lean'))==h,n
result={'status':'INDEPENDENT_COMPILED_SIGMA2_AST_REBUILD_PASSED','seal_sha256':sha(S),'receipt_sha256':sha(rec),'builds':res,'axiom_readbacks':ax,'negative_controls':controls,'dependencies_match_prior_audit':True,'scope':'Actual generated Lean Sigma2 AST semantics and its fair-input law; ordinary Python constructor comparison, not a formal Python byte/numeric-code refinement.'}
(R/'CANDIDATE_STAGE_AUDIT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print('CANDIDATE_STAGE_PASS',flush=True)
