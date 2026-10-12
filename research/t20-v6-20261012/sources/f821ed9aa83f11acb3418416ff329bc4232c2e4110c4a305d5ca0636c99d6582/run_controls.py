#!/usr/bin/env python3
"""Independent controls using only the fresh receipt's custom library."""
from pathlib import Path
import os,re,json,hashlib,subprocess,time,sys,argparse
root=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--receipt',type=Path)
parser.add_argument('--mathlib-root',type=Path,default=Path('private-locator:41bd9f979012c8bbc235'))
parser.add_argument('--lean-bin',type=Path,default=Path('private-locator:d97af50b47918e94879b'))
args=parser.parse_args()
receipt=args.receipt or Path((root/'LATEST_REPLAY.txt').read_text().strip()); data=json.loads(receipt.read_text()); assert data['status']=='PASS'; out=receipt.parent;src=out/'sources';lib=out/'lib'
math=args.mathlib_root.resolve();tool=args.lean_bin.resolve()
paths=[lib,math/'.lake/build/lib/lean']+[p/'.lake/build/lib/lean' for p in sorted((math/'.lake/packages').iterdir()) if (p/'.lake/build/lib/lean').is_dir()]
env={**os.environ,'PATH':str(tool)+':'+os.environ['PATH'],'LEAN_PATH':':'.join(map(str,paths))};env.pop('LEAN_NUM_THREADS',None)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
results=[]
def run(label,cmd,expected=0,cwd=src):
 t=time.monotonic();p=subprocess.run(cmd,env=env,cwd=cwd,capture_output=True,text=True,timeout=600);output=p.stdout+p.stderr;log=out/(label+'.log');log.write_text(output)
 rec={'label':label,'exit':p.returncode,'expected_exit':expected,'seconds':time.monotonic()-t,'command':cmd,'log_sha256':sha(log)};results.append(rec);print(json.dumps(rec),flush=True)
 assert p.returncode==expected,(label,output)
 return output
for f in ['BoundaryControls.lean','EndpointControls.lean','Differential.lean']:(src/f).write_bytes((root/f).read_bytes())
run('BoundaryControls',['lean','-j1','--root='+str(src),'-o',str(lib/'BoundaryControls.olean'),str(src/'BoundaryControls.lean')])
run('EndpointControls',['lean','-j1','--root='+str(src),'-o',str(lib/'EndpointControls.olean'),str(src/'EndpointControls.lean')])
names=['AtomicMembershipAudit.'+x for f in ['BoundaryControls.lean','EndpointControls.lean'] for x in re.findall(r'^(?:theorem|lemma)\s+([\w\x27]+)',(src/f).read_text(),re.M)]
(src/'ControlAudit.lean').write_text('import BoundaryControls\nimport EndpointControls\n'+'\n'.join('#check @'+n+'\n#print axioms '+n for n in names)+'\n')
output=run('ControlAudit',['lean','-j1','--root='+str(src),str(src/'ControlAudit.lean')])
axioms={n:[x.strip() for x in a.split(',') if x.strip()] for n,a in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",output)}
axioms.update({n:[] for n in re.findall(r"'([^']+)' does not depend on any axioms",output)})
assert set(axioms)==set(names);assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in axioms.values())
run('Differential',['lean','-j1','--root='+str(src),'--run',str(src/'Differential.lean')])
run('ExactControls',[sys.executable,str(root/'exact_controls.py')])
mutants=[
 ('strict-heavy-threshold','RationalNormalForm','Finset.univ.filter (fun w => (1/2 : ℚ≥0)^k ≤ p n w)','Finset.univ.filter (fun w => (1/2 : ℚ≥0)^k < p n w)'),
 ('off-by-one-cylinder-weight','FiniteOutputTable','(preimageWords P N w).card / (2 : ℚ≥0)^N','(preimageWords P N w).card / (2 : ℚ≥0)^(N+1)'),
 ('complete-source-word-too-early','FiniteOutputTable','bitsPrefix N (output P (extendWord N v))','fun i => decide (P i.val (sentinel (List.ofFn v)) % 2 = 1)'),
]
for label,module,old,new in mutants:
 mdir=out/'mutants'/label;mdir.mkdir(parents=True)
 original=(src/(module+'.lean')).read_text();assert original.count(old)==1,(label,original.count(old))
 f=mdir/(module+'.lean');f.write_text(original)
 run(label+'-baseline',['lean','-j1','--root='+str(mdir),'-o',str(mdir/'baseline.olean'),str(f)])
 f.write_text(original.replace(old,new))
 output=run(label+'-rejected',['lean','-j1','--root='+str(mdir),'-o',str(mdir/'mutated.olean'),str(f)],1)
 assert 'error:' in output and ('unsolved goals' in output or 'type mismatch' in output or 'Tactic' in output or 'tactic' in output),output
 assert 'unknown module' not in output and 'object file' not in output,output
 results[-1]['mutated_source_sha256']=sha(f)
# A terminal contradiction cannot be admitted by the independent proof controls.
neg=src/'FalseAtomicity.lean';neg.write_text('import BoundaryControls\nopen P02A2 P02A2.Q8Measure AtomicMembershipAudit\nexample : mass fairCantor = 1 := by\n  rw [fair_mass_zero]\n  norm_num\n')
output=run('FalseAtomicity',['lean','-j1','--root='+str(src),str(neg)],1)
assert 'unsolved goals' in output and ('0 = 1' in output or '⊢ False' in output),output
result={'status':'PASS','control_theorem_count':len(names),'control_targets':names,'control_axioms':axioms,'fresh_build_receipt_sha256':sha(receipt),'source_sha256':{m:d['sha256'] for m,d in data['sources'].items()},'results':results,'differential_check_count':json.loads((root/'DIFFERENTIAL_VECTORS.json').read_text())['checks'],'exact_rational_check_count':json.loads((root/'EXACT_CONTROLS_RESULT.json').read_text())['exact_checks'],'negative_control_count':len(mutants)+1,'all_custom_sources_rebuilt':len(data['sources']),'lean_path':env['LEAN_PATH'],'origins_unchanged':all(sha(Path(d['origin']))==d['sha256'] for d in data['sources'].values()),'not_claimed':['The original soft/excess formula','Uniform Mathlib Computable certificate','Formal arithmetical-hierarchy classification','Universal PR evaluation','Canonical adoption']}
assert result['origins_unchanged']
(out/'CONTROLS_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(root/'LATEST_CONTROLS.txt').write_text(str(out/'CONTROLS_RESULT.json')+'\n')
print(json.dumps({'status':'PASS','receipt':str(out/'CONTROLS_RESULT.json'),'sha256':sha(out/'CONTROLS_RESULT.json')}))
