#!/usr/bin/env python3
from pathlib import Path
import subprocess,os,json,re,hashlib,datetime
A=Path(__file__).resolve().parent;R=A.parent;sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();lean=R/'toolchain/lean-4.19.0-linux/bin/lean';env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip())
def run(src,log):
 p=subprocess.run([str(lean),'--root='+str(src.parent),str(src)],cwd=R/'toolchain/mathlib4',env=env,text=True,capture_output=True);log.write_text(p.stdout+p.stderr);return p
p=run(A/'controls/TargetReadback.lean',A/'logs/TargetReadback.log');assert p.returncode==0,p.stdout
log=p.stdout;targets=json.loads((A/'TARGETS.json').read_text());axioms={}
for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^]]*)\]|does not depend on any axioms)",log):
 assert m[1] not in axioms;axioms[m[1]]=sorted(x.strip() for x in (m[2] or '').split(',') if x.strip())
assert set(axioms)==set(targets);assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in axioms.values());assert 'sorryAx' not in log
(A/'AXIOM_READBACK.json').write_text(json.dumps({'status':'PASS','target_count':len(targets),'source_sha256':sha(A/'snapshot/RecurrentSupport.lean'),'readback_sha256':sha(A/'logs/TargetReadback.log'),'targets':axioms},indent=2)+'\n')
controls=re.findall(r'^\s*(?:theorem|lemma)\s+(\w+)',(A/'controls/RecurrenceControls.lean').read_text(),re.M)
(A/'controls/ControlReadback.lean').write_text('import RecurrenceControls\n'+''.join(f'#check @RecurrenceAudit.{n}\n#print axioms RecurrenceAudit.{n}\n' for n in controls));p=run(A/'controls/ControlReadback.lean',A/'logs/ControlReadback.log');assert p.returncode==0 and 'sorryAx' not in p.stdout,p.stdout
for m in re.finditer(r"depends on axioms:\s*\[([^]]*)\]",p.stdout):assert set(x.strip() for x in m[1].split(',') if x.strip())<={'propext','Classical.choice','Quot.sound'}
mutations=[('FiniteZeroMeasureAllowed','[IsProbabilityMeasure μ]','[IsFiniteMeasure μ]'),('WeakTransfer','0 < μ η (tailEvent X U N))','0 ≤ μ η (tailEvent X U N))'),('DropExactSupportFromTail','exactRecurrentEvent X U ∩ {ω | ∀ n, N ≤ n → X ω n ∈ U}','{ω | ∀ n, N ≤ n → X ω n ∈ U}'),('OnceInsteadOfRecurrence','∃ᶠ n in atTop, x n = a','∃ n : ℕ, x n = a')]
results=[]
for name,old,new in mutations:
 d=A/'mutations'/name;d.mkdir(parents=True,exist_ok=True);s=(A/'snapshot/RecurrentSupport.lean').read_text();assert old in s;dest=d/'RecurrentSupport.lean';dest.write_text(s.replace(old,new));log=A/'logs'/(name+'.log');p=run(dest,log);assert p.returncode!=0 and 'error:' in p.stdout and 'unknown module' not in p.stdout,(name,p.stdout);results.append({'name':name,'old':old,'new':new,'expected':'REJECT','exit':p.returncode,'source_sha256':sha(dest),'log_sha256':sha(log)});print(name,'REJECTED',flush=True)
assert 'error:' not in (A/'logs/RecurrenceControls.log').read_text();assert sha(R/'necessity-bridge-review/lean/RecurrentSupport.lean')==sha(A/'snapshot/RecurrentSupport.lean')
(A/'CONTROL_RESULT.json').write_text(json.dumps({'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'positive_theorems':controls,'positive_count':len(controls),'mutations':results,'replay_sha256':sha(A/'REPLAY_RESULT.json')},indent=2)+'\n')
