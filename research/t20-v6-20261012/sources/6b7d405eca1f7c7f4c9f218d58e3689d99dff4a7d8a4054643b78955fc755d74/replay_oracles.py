#!/usr/bin/env python3
"""Replay finite SCC/MEC/parity comparisons against hash-verified fresh objects."""
from pathlib import Path
import argparse,hashlib,importlib.util,json,os,subprocess,sys
sys.dont_write_bytecode=True
os.environ['PYTHONDONTWRITEBYTECODE']='1'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,x):Path(p).write_text(json.dumps(x,indent=2,sort_keys=True)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--baseline',type=Path,required=True);ap.add_argument('--lean-bin',type=Path,required=True);ap.add_argument('--mathlib',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 root=a.root.resolve();out=a.out.resolve();baseline=a.baseline.resolve()
 if out.exists() or out.is_relative_to(root):raise SystemExit('Output must be absent and outside immutable source')
 spec=importlib.util.spec_from_file_location('core',root/'tooling/portable_core.py');core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
 identity=core.verify(root);receipt=json.loads((baseline/'REPLAY_RESULT.json').read_text());assert receipt['status']=='PASS' and receipt['input_manifest_sha256']==identity['manifest_sha256']
 suite=next(s for s in receipt['suites'] if s['id']=='scc_parity_pruning');assert suite['status']=='PASS'
 build=baseline/'scc_parity_pruning/build'
 for row in suite['modules']:assert row['status']=='FRESH_COMPILE' and sha(build/(row['module']+'.olean'))==row['olean_sha256']
 pins=json.loads((root/'replay/DEPENDENCY_PINS.json').read_text());lean,libs,version,checks=core.verify_pins(a.lean_bin,a.mathlib,pins,{r['module'] for r in suite['modules']})
 out.mkdir(parents=True);env=dict(os.environ);env['LEAN_PATH']=':'.join(map(str,[build]+libs));env.pop('LEAN_SRC_PATH',None)
 results=[]
 for name,generator,filename in [('generic','oracle.py','IndependentOracle.lean'),('normalized','normalized_oracle.py','NormalizedOracle.lean'),('mec','mec_oracle.py','MECOracle.lean')]:
  d=out/name
  p=subprocess.run([sys.executable,str(root/'checks'/generator),'--output',str(d)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(out/(name+'-generation.log')).write_text(p.stdout);assert p.returncode==0
  p=subprocess.run([str(lean),'-j1','--run',str(d/filename)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(d/'LEAN_OUTPUT.csv').write_text(p.stdout);assert p.returncode==0,p.stdout
  actual=[list(map(int,x.split(','))) for x in p.stdout.splitlines()]
  if name=='generic':expected=[[i]+v for i,v in enumerate(json.loads((d/'ORACLE_CASES.json').read_text())['expected'])]
  elif name=='normalized':expected=[[i,v] for i,v in enumerate(json.loads((d/'CASES.json').read_text())['expected_targets'])]
  else:expected=json.loads((d/'EXPECTED.json').read_text())
  assert actual==expected,(name,len(actual),len(expected))
  results.append({'corpus':name,'cases':len(actual),'output_sha256':sha(d/'LEAN_OUTPUT.csv'),'status':'PASS'});print(name,len(actual),'PASS',flush=True)
 result={'status':'PASS_AUTHOR_FINITE_ORACLE_COMPARISONS','input_manifest_sha256':identity['manifest_sha256'],'baseline_receipt_sha256':sha(baseline/'REPLAY_RESULT.json'),'lean_version':version,'dependency_checks':checks,'results':results,'scope':'finite execution tests, separate from kernel equivalence and ordinary cost account'}
 core.verify(root);save(out/'RESULT.json',result)
if __name__=='__main__':main()
