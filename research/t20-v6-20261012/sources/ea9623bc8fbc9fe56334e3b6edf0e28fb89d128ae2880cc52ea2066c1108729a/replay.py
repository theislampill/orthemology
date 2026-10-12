from pathlib import Path
import datetime,hashlib,importlib.util,json,os,shutil,subprocess,time
W=Path(__file__).resolve().parent.parent; R=Path(__file__).resolve().parent; C=W/'hase-coded-mixed-transformations-20261010'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p): return {'path':str(p.relative_to(W)), 'sha256':sha(p),'bytes':p.stat().st_size}
pins=json.loads((C/'validation/INPUT_PINS.json').read_text())
extra=[rec(C/'validation/INPUT_PINS.json'),rec(C/'validation/AUTHOR_REPLAY.json')]
for n in ['AllSyntax','SubstitutionSyntax','FiniteBridge']:
 extra.append(rec(W/'hase-imported-compiler-transport-20261010/sources'/f'{n}.lean'))
(R/'REVIEW_INPUT_PINS.json').write_text(json.dumps(pins+extra,indent=2)+'\n')
def check():
 for p in pins+extra:
  f=W/p['path'];assert sha(f)==p['sha256'] and f.stat().st_size==p['bytes'],p['path']
check();print('PIN_CHECK_BEFORE',len(pins+extra),flush=True)
spec=importlib.util.spec_from_file_location('candidate',C/'verify.py');c=importlib.util.module_from_spec(spec);spec.loader.exec_module(c)
out=R/'output';env={**os.environ,'LEAN_PATH':':'.join(map(str,[out]+c.b.inherited_paths()))}
(R/'env.json').write_text(json.dumps({'lean':str(c.b.LEAN),'LEAN_PATH':env['LEAN_PATH']},indent=2)+'\n')
records=[]
for src in c.SOURCES:
 copied=R/'sources'/src.name;shutil.copy2(src,copied);obj=out/(src.stem+'.olean');assert not obj.exists()
 start=time.monotonic();cmd=[str(c.b.LEAN),'--trust=0','-o',str(obj),str(copied)];p=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=out/(src.stem+'.log');log.write_text(p.stdout)
 records.append({'module':src.stem,'original':rec(src),'source':rec(copied),'object':rec(obj) if obj.exists() else None,'log':rec(log),'exit_code':p.returncode,'seconds':time.monotonic()-start,'command':cmd})
 (R/'PARTIAL_REPLAY.json').write_text(json.dumps(records,indent=2)+'\n')
 assert p.returncode==0 and not any(x in p.stdout for x in ['sorryAx','error:','warning:']),log
 print('PASS',src.stem,flush=True)
neg=[]
for m in c.MUTATIONS:
 src=C/'diagnostics'/(m+'.lean');copied=R/'negative'/(m+'.lean');shutil.copy2(src,copied)
 p=subprocess.run([str(c.b.LEAN),'--trust=0',str(copied)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=out/(m+'.log');log.write_text(p.stdout)
 assert p.returncode!=0 and 'error:' in p.stdout,log
 neg.append({'module':m,'source':rec(copied),'log':rec(log),'exit_code':p.returncode});print('REJECTED',m,flush=True)
check();result={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lean_version':subprocess.check_output([str(c.b.LEAN),'--version'],text=True).strip(),'trust':0,'pins_before_after':len(pins+extra),'author_pins_count':len(pins),'candidate_and_author_receipt_frozen':True,'baseline_rebuilt':False,'positive':records,'negative':neg}
(R/'SELECTIVE_REPLAY.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS_REPLAY',len(records),len(neg),flush=True)
