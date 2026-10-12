from pathlib import Path
import hashlib,importlib.util,json,os,shutil,subprocess,time,datetime
R=Path(__file__).resolve().parent;W=R.parent;C=W/'hase-auxiliary-checker-computability-20261010';M=W/'hase-coded-mixed-independent-review-20261010'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p): return {'path':str(p.relative_to(W)),'sha256':sha(p),'bytes':p.stat().st_size}
spec=importlib.util.spec_from_file_location('candidate',C/'verify.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
pins=json.loads((C/'validation/INPUT_PINS.json').read_text())
extra=[rec(C/'validation/INPUT_PINS.json'),rec(M/'REVIEW_RECEIPT.json'),rec(M/'SELECTIVE_REPLAY.json')]+[rec(p) for p in sorted((M/'output').glob('*.olean'))]
(R/'REVIEW_INPUT_PINS.json').write_text(json.dumps(pins+extra,indent=2)+'\n')
def check():
 for p in pins+extra:
  f=W/p['path'];assert sha(f)==p['sha256'] and f.stat().st_size==p['bytes'],p['path']
check();print('PIN_CHECK_BEFORE',len(pins+extra),flush=True)
out=R/'output';env={**os.environ,'LEAN_PATH':':'.join(map(str,[out,M/'output']+c.b.inherited_paths()))}
(R/'env.json').write_text(json.dumps({'lean':str(c.b.LEAN),'LEAN_PATH':env['LEAN_PATH']},indent=2)+'\n')
sources=[W/'hase-joint-certificate-auxiliary-20261010/AuxiliaryCertificates.lean']+[c.F/(m+'.lean') for m in c.EXTRA]+[C/(m+'.lean') for m in c.OWN]
records=[]
for src in sources:
 copied=R/'sources'/src.name;shutil.copy2(src,copied);obj=out/(src.stem+'.olean');assert not obj.exists()
 start=time.monotonic();cmd=[str(c.b.LEAN),'--trust=0','-o',str(obj),str(copied)];p=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=out/(src.stem+'.log');log.write_text(p.stdout)
 records.append({'module':src.stem,'original':rec(src),'source':rec(copied),'object':rec(obj) if obj.exists() else None,'log':rec(log),'exit_code':p.returncode,'seconds':time.monotonic()-start,'command':cmd})
 (R/'PARTIAL_REPLAY.json').write_text(json.dumps(records,indent=2)+'\n')
 assert p.returncode==0 and not any(x in p.stdout for x in ['sorryAx','error:','warning:']),log
 print('PASS',src.stem,flush=True)
neg=[]
for m in c.MUTATIONS:
 src=C/'diagnostics'/(m+'.lean');copied=R/'negative'/('Author'+m+'.lean');shutil.copy2(src,copied)
 p=subprocess.run([str(c.b.LEAN),'--trust=0',str(copied)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=out/('Author'+m+'.log');log.write_text(p.stdout)
 expected='unsolved goals' if m=='AssumeSyntaxValidation' else "tactic 'decide' proved that the proposition"
 assert p.returncode!=0 and expected in p.stdout and not any(x in p.stdout for x in ['unknown identifier','unexpected token','failed to import','unknown module']),log
 neg.append({'module':m,'source':rec(copied),'log':rec(log),'exit_code':p.returncode,'expected_rejection':expected});print('REJECTED',m,flush=True)
check();result={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lean_version':subprocess.check_output([str(c.b.LEAN),'--version'],text=True).strip(),'trust':0,'pins_before_after':len(pins+extra),'candidate_pins':len(pins),'baseline_rebuilt':False,'reused_independent_mixed_output':rec(M/'REVIEW_RECEIPT.json'),'positive':records,'negative':neg}
(R/'SELECTIVE_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS_REPLAY',len(records),len(neg),flush=True)
