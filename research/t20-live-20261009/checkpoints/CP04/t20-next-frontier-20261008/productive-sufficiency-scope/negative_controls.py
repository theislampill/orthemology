#!/usr/bin/env python3
"""Reject three precise scope promotions. Does not test metaphysical truth."""
from pathlib import Path
import os, subprocess, json, hashlib
ROOT=Path(__file__).resolve().parent
DEP=ROOT.parent/'formal-identification'; PROB=ROOT.parent/'formal-route-probability'
env=os.environ.copy(); env['PATH']=str(DEP/'toolchain/lean-4.19.0-linux/bin')+':'+env['PATH']
cache=subprocess.run(['lake','env','printenv','LEAN_PATH'],cwd=DEP/'mathlib',env=env,capture_output=True,text=True,check=True).stdout.strip()
env['LEAN_PATH']=':'.join(map(str,[ROOT,ROOT/'inherited',PROB,DEP]))+':'+cache
cases={
'necessary_target':'''example : Necessary positive.existsAt true := by
  simp only [Necessary, positive]
  decide
''',
'fixed_act_token':'''example : ∀ w, actOccurs w .left := by
  simp only [actOccurs]
  decide
''',
'normalization_forces_nonempty_endpoint':'''example : endpoint oneRoute .A (realization true) ≠ ∅ := by
  rw [failure_endpoint]
  decide
'''}
header='''import ScopeTest
open ProductiveSufficiencyScope
open Orthemology.Tranche3.SourceIdentity
open Orthemology.Tranche20.OriginalBearerBridge.Controls
open RouteProbability
'''
results=[]
for name,body in cases.items():
 p=ROOT/'results'/f'{name}.lean'; p.write_text(header+body)
 r=subprocess.run(['lean','-DwarningAsError=true','--trust=0',f'--root={ROOT}',str(p)],cwd=DEP/'mathlib',env=env,capture_output=True,text=True)
 output=r.stdout+r.stderr; (ROOT/'results'/f'{name}.log').write_text(output)
 intended=(r.returncode!=0 and "tactic 'decide' proved that the proposition" in output and 'is false' in output and 'unknown module' not in output and 'unknown identifier' not in output)
 results.append({'claim':name,'exit_code':r.returncode,'intended_false_proposition_rejected':intended,'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
(ROOT/'results'/'NEGATIVE_CONTROLS.json').write_text(json.dumps(results,indent=2)+'\n')
print(json.dumps(results,indent=2))
assert all(x['intended_false_proposition_rejected'] for x in results)
