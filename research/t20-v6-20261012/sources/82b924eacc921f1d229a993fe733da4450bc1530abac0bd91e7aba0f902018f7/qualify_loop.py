import pathlib,json,re,hashlib,subprocess,os,time
ROOT=pathlib.Path(__file__).resolve().parent; TOOL=pathlib.Path('private-locator:d97af50b47918e94879b'); ENV={**os.environ,'PATH':str(TOOL)+':'+os.environ['PATH']};ENV.pop('LEAN_NUM_THREADS',None)
R=ROOT/'receipts'/('loop-'+time.strftime('%Y%m%dT%H%M%SZ',time.gmtime()));R.mkdir();sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def run(label,cmd,expected=0):
 t=time.time();p=subprocess.run(cmd,cwd=ROOT,env=ENV,capture_output=True);(R/(label+'.stdout')).write_bytes(p.stdout);(R/(label+'.stderr')).write_bytes(p.stderr);(R/(label+'.command.json')).write_text(json.dumps({'command':cmd,'start_unix':t,'end_unix':time.time(),'exit':p.returncode,'expected_exit':expected},indent=2));assert p.returncode==expected,(label,p.stdout.decode(),p.stderr.decode());return p.stdout.decode()+p.stderr.decode()
mods=['LoopRenaming','LoopPrimrec','LoopInliningWitnesses','Q8Primrec'];sources={m:sha(ROOT/(m+'.lean')) for m in mods};targets=[];art=[]
for m in mods:
 p=ROOT/(m+'.lean');ns=re.search(r'^namespace (\S+)',p.read_text(),re.M).group(1)
 targets += [{'module':m,'declaration':ns+'.'+n} for n in re.findall(r'^theorem (\w+)',p.read_text(),re.M)]
 o=ROOT/'.lake/build/lib/lean'/(m+'.olean');start=time.time();run('build-'+m,['lake','env','lean','-o',str(o),str(p)]);assert o.stat().st_size and o.stat().st_mtime>=start-2;art.append({'module':m,'bytes':o.stat().st_size,'sha256':sha(o)});print('BUILT',m,flush=True)
audit=ROOT/'LoopAudit.lean';audit.write_text('import LoopInliningWitnesses\nimport Q8Primrec\n'+''.join('#check @'+t['declaration']+'\n#print axioms '+t['declaration']+'\n' for t in targets));out=run('all-types-and-axioms',['lake','env','lean',str(audit)]);assert 'sorryAx' not in out and not re.search(r'\berror:',out);seen={}
for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out):assert n not in seen;seen[n]=[x.strip() for x in a.split(',') if x.strip()]
for n in re.findall(r"'([^']+)' does not depend on any axioms",out):assert n not in seen;seen[n]=[]
assert set(seen)=={t['declaration'] for t in targets}
for n,a in seen.items():
 assert set(a)<={'propext','Classical.choice','Quot.sound'},(n,a)
 assert any(l.lstrip('@').startswith(n+' :') or l.lstrip('@').startswith(n+'.{') for l in out.splitlines()),n
controls=[]
for n,expected in [('InliningBaseline',0),('MissingResetMustFail',1),('CollidingRenameMustFail',1),('NonfreshArgumentMustFail',1)]:
 text=run(n,['lake','env','lean','negative-controls/'+n+'.lean'],expected)
 if expected:assert 'proved that the proposition' in text and 'false' in text
 controls.append({'name':n,'exit':expected,'source_sha256':sha(ROOT/'negative-controls'/(n+'.lean'))})
assert sources=={m:sha(ROOT/(m+'.lean')) for m in mods}
r={'status':'FINITE_REGISTER_RENAMING_FRESH_INLINING_AND_FIXED_PROGRAM_PR_KERNEL_CHECKED','theorem_count':len(targets),'targets':targets,'axioms':seen,'source_sha256':sources,'artifacts':art,'negative_controls':controls,'audit_sha256':sha(audit),'base_130_target_receipt_sha256':sha(ROOT/'receipts/qualification-20260930T134433Z/QUALIFIED_RESULT.json'),'q8_receipt_sha256':sha(ROOT/'receipts/q8-20260930T141007Z/Q8_RESULT.json'),'core_scope':'Finite partial-injection renaming, exact fresh/reset inlining semantics and caller frame property, all fixed grammar programs primitive recursive via faithful finite stores, generated Q8 function class membership','not_claimed':['Universal interpreter is primitive recursive in code','Full Python interpreter or byte codec correctness','Arbitrary PR function has an encoded P02-L1 implementation','Formal code-level hierarchy membership or hardness'],'canonical_adoption':False,'whole_obligation_closure':False}
p=R/'LOOP_RESULT.json';p.write_text(json.dumps(r,indent=2)+'\n');(R/'LOOP_RESULT.json.sha256').write_text(sha(p)+'  LOOP_RESULT.json\n');(ROOT/'LATEST_LOOP_QUALIFICATION.txt').write_text(str(p)+'\n');print(json.dumps({'status':r['status'],'theorem_count':len(targets),'receipt':str(p),'sha256':sha(p)},indent=2))
