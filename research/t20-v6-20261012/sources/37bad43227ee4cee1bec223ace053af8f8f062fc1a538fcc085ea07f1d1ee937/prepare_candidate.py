"""Stage a content-bound candidate for parent review; never archives, uploads or edits a repo."""
from pathlib import Path
import json,hashlib,subprocess,sys,shutil
W=Path(__file__).resolve().parents[2];D=W/'t20-closure-audit-20261011';A=Path(__file__).parent;P=W/'deliverables/t20-v5-candidate';H=P/'historical_coverage';V=W/'deliverables/t20-v4-sealed'
def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(x if isinstance(x,str) else json.dumps(x,indent=2,ensure_ascii=False)+'\n')
for name in ['verify_supplement.py','replay_supplement.py','resolve_source.py','test_supplement.py']:shutil.copyfile(A/name,H/name)
# Candidate manifest covers additions; preserved v4 inventory supplies all unchanged original paths.
def manifest():
 old={p.relative_to(V).as_posix() for p in V.rglob('*') if p.is_file()}
 rows=[{'path':p.relative_to(P).as_posix(),'sha256':h(p),'bytes':p.stat().st_size} for p in sorted(P.rglob('*')) if p.is_file() and p.relative_to(P).as_posix() not in old|{'historical_coverage/CANDIDATE_CONTENTS.json'}]
 put(H/'CANDIDATE_CONTENTS.json',{'schema':'t20-v5-additive-candidate-contents-v1','status':'STAGED_FOR_ROOT_REVIEW_NOT_A_DELIVERY_SEAL','scope':'Exact additive file inventory; every v4 member separately preserved. This is not owner acceptance, scientific closure or repository authority.','files':rows})
manifest()
check=subprocess.run([sys.executable,'-B',str(H/'verify_supplement.py')],capture_output=True,text=True);put(A/'supplement-verification.log',check.stdout+check.stderr)
if check.returncode:raise RuntimeError(check.stdout+check.stderr)
receipts=[]
for name in ['early-operations','foundations-custody','independent-foundations-operations','later-accounting']:
 run=subprocess.run([sys.executable,'-B',str(H/'replay_supplement.py'),'--suite',name],capture_output=True,text=True)
 put(A/('replay-'+name+'.json'),run.stdout);put(A/('replay-'+name+'.stderr'),run.stderr)
 if run.returncode:raise RuntimeError(name+' failed: '+run.stderr)
 data=json.loads(run.stdout);receipts.append(data)
put(H/'PORTABLE_REPLAY_VERIFICATION.json',{'status':'PASS','scope':'Four selected author/reviewer programs run in disposable declared-alias layouts. Author source-hash/stored-flag checks remain weaker than independent reconstruction. Normal and optimized modes do not multiply results. No old v4 science rerun, new kernel execution, corpus-wide replay or empirical/Arabic authentication.','runs':receipts,'resolver_sha256':h(H/'SOURCE_PATH_RESOLVER.json'),'runner_sha256':h(H/'replay_supplement.py'),'unchanged_v4_manifest_sha256':h(P/'package/PACKAGE_CONTENTS.json')})
manifest()
check=subprocess.run([sys.executable,'-B',str(H/'verify_supplement.py')],capture_output=True,text=True);put(A/'supplement-verification.log',check.stdout+check.stderr)
if check.returncode:raise RuntimeError(check.stdout+check.stderr)
test=subprocess.run([sys.executable,'-B',str(H/'test_supplement.py')],capture_output=True,text=True)
put(A/'adversarial.stderr',test.stderr)
if test.returncode:raise RuntimeError(test.stdout+test.stderr)
put(H/'ADVERSARIAL_VERIFICATION.json',json.loads(test.stdout));manifest()
for name in ['validate_package.py','validate_depth.py']:
 r=subprocess.run([sys.executable,'-B',name],cwd=P/'package',capture_output=True,text=True);put(A/(name+'.log'),r.stdout+r.stderr)
 if r.returncode:raise RuntimeError(name+' failed')
old=[p for p in V.rglob('*') if p.is_file()]
for p in old:
 if h(p)!=h(P/p.relative_to(V)):raise RuntimeError('v4 changed')
result={'status':'STAGED_FOR_ROOT_REVIEW','additive_manifest_sha256':h(H/'CANDIDATE_CONTENTS.json'),'v4_manifest_sha256':h(P/'package/PACKAGE_CONTENTS.json'),'preserved_v4_files':len(old),'total_candidate_files':sum(p.is_file() for p in P.rglob('*')),'fresh_portable_targets':len(receipts),'archive_created':False,'repository_mutation':False}
put(A/'CANDIDATE_VERIFICATION.json',result);print(json.dumps(result,indent=2))
