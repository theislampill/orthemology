from pathlib import Path
import json,os,subprocess,hashlib
R=Path(__file__).resolve().parent; W=R.parent; O=R/'kernel'; B=W/'rational-threshold-formal-extension-20261011'
env=dict(os.environ,LEAN_PATH=str(O)+':'+(B/'lean_path.txt').read_text().strip());lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'
pre='import RationalShiftRealisation\nopen RationalBinaryWeights OrthemologyTagged OrthemologyTagged.UnaryPrefix\n'
tests={
'WrongEndpointOne':'example : closedDigit 1 1 0 = false := by decide\n',
'WrongStopBit':'example : prefixValue (fun _ _ _ => 1) (fun _ => false) 0 0 2 = 1 := by decide\n',
'WrongSuffixSentinel':'example : suffixWord 2 10 0 = 10 := by decide\n',
'WrongOneHardness':'example : (1 : ℝ) + (1-1)*1 = 1 ↔ (1 : ℝ) = 0 := by norm_num\n',
'WrongHalfFirstDigit':'example : closedDigit 1 2 0 = false := by decide\n',
}
records=[]
for n,body in tests.items():
 p=R/(n+'.lean');p.write_text(pre+body)
 r=subprocess.run([str(lean),'--trust=0',str(p)],cwd=W,env=env,text=True,capture_output=True); (O/(n+'.negative.log')).write_text(r.stdout+r.stderr)
 assert r.returncode!=0,(n,'unexpected acceptance')
 assert 'unknown identifier' not in r.stdout and 'unknown module' not in r.stdout,(n,r.stdout)
 records.append({'test':n,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'exit_code':r.returncode,'diagnostic':r.stdout+r.stderr})
 print('REJECTED',n,flush=True)
(R/'NEGATIVES.json').write_text(json.dumps(records,indent=2)+'\n')
p=R/'PositiveControls.lean'; p.write_text(pre+'''example : closedDigit 1 1 0 = true := by decide
example : closedDigit 1 2 0 = true := by decide
example : closedDigit 1 2 1 = false := by decide
example : closedDigit 0 3 19 = false := by decide
example : prefixValue (fun _ _ _ => 1) (fun _ => false) 0 0 2 = 0 := by decide
example : suffixWord 2 10 0 = 6 := by decide
example : suffixWord 2 10 5 = 1 := by decide
example : prefixValue (fun _ _ w => w) (fun _ => false) 0 2 10 = 6 := by decide
example : prefixValue (fun _ _ _ => 1) (fun _ => true) 0 2 10 = 0 := by decide
example (F : ℕ → ℕ → ℕ → ℕ) (D : ℕ → Bool) (a : ℕ) :
 P02A2.ObserverCore.output (prefixValue F D a) allTrue = allTrue :=
 prefixValue_allTrue F D a
''')
r=subprocess.run([str(lean),'--trust=0',str(p)],cwd=W,env=env,text=True,capture_output=True);(O/'PositiveControls.log').write_text(r.stdout+r.stderr)
assert r.returncode==0,(r.stdout,r.stderr)
print('PASS positive controls',flush=True)
