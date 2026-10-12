import pathlib,json,re,hashlib,subprocess,os,time
ROOT=pathlib.Path(__file__).resolve().parent; TOOL=pathlib.Path('private-locator:d97af50b47918e94879b'); ENV={**os.environ,'PATH':str(TOOL)+':'+os.environ['PATH']};ENV.pop('LEAN_NUM_THREADS',None)
R=ROOT/'receipts'/('candidate-'+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime()));R.mkdir();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,cmd,expected=0):
 t=time.time();p=subprocess.run(cmd,cwd=ROOT,env=ENV,capture_output=True);(R/(label+'.stdout')).write_bytes(p.stdout);(R/(label+'.stderr')).write_bytes(p.stderr);(R/(label+'.command.json')).write_text(json.dumps({'command':cmd,'start_unix':t,'end_unix':time.time(),'exit':p.returncode,'expected_exit':expected},indent=2));assert p.returncode==expected,(label,p.stdout.decode(),p.stderr.decode());return p.stdout.decode()+p.stderr.decode()
assert run('lean-version',['lean','--version']).strip()=='Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)'
mods=['CandidateCompiler','CandidateSource','CandidateWitnesses','Sigma2Compiled'];sources={m:sha(ROOT/(m+'.lean')) for m in mods};targets=[];art=[]
for m in mods:
 p=ROOT/(m+'.lean');ns=re.search(r'^namespace (\S+)',p.read_text(),re.M).group(1);targets += [{'module':m,'declaration':ns+'.'+n} for n in re.findall(r'^(?:@\[[^\]]*\]\s*)?theorem (\w+)',p.read_text(),re.M)]
 o=ROOT/'.lake/build/lib/lean'/(m+'.olean');start=time.time();run('build-'+m,['lake','env','lean','-o',str(o),str(p)]);assert o.stat().st_size and o.stat().st_mtime>=start-2;art.append({'module':m,'bytes':o.stat().st_size,'sha256':sha(o)});print('BUILT',m,flush=True)
audit=ROOT/'CandidateAudit.lean';audit.write_text('import CandidateWitnesses\nimport Sigma2Compiled\n'+''.join('#check @'+t['declaration']+'\n#print axioms '+t['declaration']+'\n' for t in targets));out=run('all-types-and-axioms',['lake','env','lean',str(audit)]);assert 'sorryAx' not in out and not re.search(r'\berror:',out);seen={}
for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out):assert n not in seen;seen[n]=[x.strip() for x in a.split(',') if x.strip()]
for n in re.findall(r"'([^']+)' does not depend on any axioms",out):assert n not in seen;seen[n]=[]
assert set(seen)=={t['declaration'] for t in targets}
for n,a in seen.items():
 assert set(a)<={'propext','Classical.choice','Quot.sound'},(n,a)
 assert any(l.lstrip('@').startswith(n+' :') or l.lstrip('@').startswith(n+'.{') for l in out.splitlines()),n
controls=[]
for n,expected in [('CandidateBaseline',0),('ExcludedUpperTestMustFail',1),('OverwriteFirstSuccessMustFail',1)]:
 text=run(n,['lake','env','lean','negative-controls/'+n+'.lean'],expected)
 if expected:assert 'proved that the proposition' in text and 'false' in text,text
 controls.append({'name':n,'exit':expected,'source_sha256':sha(ROOT/'negative-controls'/(n+'.lean'))})
assert sources=={m:sha(ROOT/(m+'.lean')) for m in mods}
r={'status':'ACTUAL_CANDIDATE_AND_SIGMA2_AST_COMPILER_KERNEL_CHECKED','theorem_count':len(targets),'targets':targets,'axioms':seen,'source_sha256':sources,'artifacts':art,'negative_controls':controls,'audit_sha256':sha(audit),'base_130_target_receipt_sha256':sha(ROOT/'receipts/qualification-20260930T134433Z/QUALIFIED_RESULT.json'),'loop_receipt_sha256':sha(ROOT/'receipts/loop-20260930T142933Z/LOOP_RESULT.json'),'scope':'Actual source-layout matrix inlining and candidate control block are proved; the two fresh compile_sigma2 blocks generate syntax whose execution equals the established row prefix function. Its actual law has the stated endpoints.','not_claimed':['Python byte/numeric serialization and interpreter refinement','Uniform numeric-code many-one reduction','General PR derivation-to-grammar completeness','General soft-mass membership or Pi03 tagged compiler proof','Novelty or canonical adoption'],'whole_obligation_closure':False}
p=R/'CANDIDATE_RESULT.json';p.write_text(json.dumps(r,indent=2)+'\n');(R/'CANDIDATE_RESULT.json.sha256').write_text(sha(p)+'  CANDIDATE_RESULT.json\n');(ROOT/'LATEST_CANDIDATE_QUALIFICATION.txt').write_text(str(p)+'\n');print(json.dumps({'status':r['status'],'theorem_count':len(targets),'receipt':str(p),'sha256':sha(p)},indent=2))
