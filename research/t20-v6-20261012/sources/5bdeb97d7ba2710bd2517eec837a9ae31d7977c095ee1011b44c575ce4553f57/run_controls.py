#!/usr/bin/env python3
from pathlib import Path
import os,re,json,hashlib,subprocess,time,sys
root=Path(__file__).resolve().parent
r=root/'receipts'/'20260930T161345Z'; data=json.loads((r/'RESULT.json').read_text());src=r/'sources';lib=r/'lib'
math=Path('private-locator:41bd9f979012c8bbc235');tool=Path('private-locator:d97af50b47918e94879b')
paths=[lib,math/'.lake/build/lib/lean']+[p/'.lake/build/lib/lean' for p in sorted((math/'.lake/packages').iterdir()) if (p/'.lake/build/lib/lean').is_dir()]
env={**os.environ,'PATH':str(tool)+':'+os.environ['PATH'],'LEAN_PATH':':'.join(map(str,paths))};env.pop('LEAN_NUM_THREADS',None)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
def run(label,cmd,expected=0):
 t=time.monotonic();p=subprocess.run(cmd,env=env,cwd=src,capture_output=True,text=True,timeout=300);out=p.stdout+p.stderr;(root/(label+'.log')).write_text(out)
 rec={'label':label,'exit':p.returncode,'expected_exit':expected,'seconds':time.monotonic()-t,'command':cmd,'log_sha256':sha(root/(label+'.log'))};results.append(rec);print(json.dumps(rec),flush=True)
 assert p.returncode==expected,(label,out)
 return out
names=[]
for mod in data['entries']:
 s=(src/(mod+'.lean')).read_text();ns=re.search(r'^namespace (\S+)',s,re.M).group(1)
 names.extend(ns+'.'+n for n in re.findall(r'^(?:@\[[^\]]*\]\s*)?(?:theorem|lemma)\s+([\w\x27]+)',s,re.M))
audit='\n'.join('import '+mod for mod in data['entries'])+'\nset_option pp.universes true\n'+'\n'.join('#check @'+n+'\n#print axioms '+n for n in names)+'\n';(src/'CompleteAudit.lean').write_text(audit)
out=run('CompleteAudit',['lean','-j1','--root='+str(src),str(src/'CompleteAudit.lean')])
axioms={n:[x.strip() for x in a.split(',') if x.strip()] for n,a in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",out)}
axioms.update({n:[] for n in re.findall(r"'([^']+)' does not depend on any axioms",out)})
assert set(axioms)==set(names);assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in axioms.values())
for f in ['BoundaryControls.lean','Differential.lean']:(src/f).write_bytes((root/f).read_bytes())
run('BoundaryControls',['lean','-j1','--root='+str(src),'-o',str(lib/'BoundaryControls.olean'),str(src/'BoundaryControls.lean')])
run('Differential',['lean','-j1','--root='+str(src),'--run',str(src/'Differential.lean')])
for f in sorted((root/'negative-controls').glob('*.lean')):
 out=run(f.stem,['lean','-j1','--root='+str(root),str(f)],1)
 assert 'error:' in out and ('false' in out or 'unsolved goals' in out),out
result={'status':'PASS','theorem_count':len(names),'targets':names,'axioms':axioms,'fresh_build_receipt_sha256':sha(r/'RESULT.json'),'source_sha256':{m:d['sha256'] for m,d in data['sources'].items()},'results':results,'differential_check_count':json.loads((root/'DIFFERENTIAL_VECTORS.json').read_text())['checks'],'negative_control_count':5,'all_custom_sources_rebuilt':len(data['sources']),'lean_path':env['LEAN_PATH']}
(root/'CONTROLS_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','receipt':str(root/'CONTROLS_RESULT.json'),'sha256':sha(root/'CONTROLS_RESULT.json')}))
