#!/usr/bin/env python3
"""Expected-failure controls against ONLY the completed independent library."""
import os,pathlib,json,subprocess,sys,hashlib
root=pathlib.Path(__file__).resolve().parent
receipt=pathlib.Path(sys.argv[1]).resolve();r=json.loads(receipt.read_text());assert r['status']=='PASS'
env={**os.environ,'LEAN_PATH':':'.join(r['LEAN_PATH'])}
out=receipt.parent/'negative-controls';out.mkdir(exist_ok=True)
controls={
 'computable_is_not_primrec': '''example : Primrec (fun code : ℕ => evaluateIndex code.unpair.1 code.unpair.2.unpair.1 code.unpair.2.unpair.2) := evaluateIndex_nat_computable\n''',
 'cannot_discard_suffix_condition': '''example (original rest : List ℕ) (table : List ExprResult) (fuel : ℕ) (ht : ∀ i, i ≤ original.length → table.getD i none = readExpr fuel (original.drop i)) : exprLookup original table rest = readExpr fuel rest := by\n  exact exprLookup_correct original table fuel ht rest\n''',
 'cannot_make_readExpr_unfuelled': '''example : readExpr 1 [3,1,1,1,2] = some (.add (.constant 1) (.constant 2),[]) := by\n  rw [UniformIndependentAudit.expr_insufficient_depth]\n''',
 'cannot_accept_overlong_varint': '''example : uvRead [128,0] = some (0,[]) := by\n  rw [UniformIndependentAudit.reject_overlong_zero]\n''',
 'cannot_ignore_trailing_bytes': '''example : decodeBytes (magic ++ [2,0,17,0,999]) = some ⟨2,0,.skip⟩ := by\n  rw [UniformIndependentAudit.decode_trailing_rejected]\n''',
}
rows=[]
for name,body in controls.items():
 source='import EndpointChecks\nopen P02.Codec P02.Codec.UniformComputability P02A2.ObserverCore\n'+body
 f=out/(name+'.lean');f.write_text(source)
 run=subprocess.run([r['builds'][0]['command'][0],'-j1',str(f)],cwd=out,env=env,text=True,capture_output=True,timeout=120)
 log=run.stdout+run.stderr;(out/(name+'.log')).write_text(log)
 expected=run.returncode!=0 and ('type mismatch' in log or 'unsolved goals' in log)
 rows.append({'control':name,'exit':run.returncode,'expected_failure':expected,'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
 print(name,run.returncode,expected,flush=True)
res={'status':'PASS' if all(x['expected_failure'] for x in rows) else 'FAIL','independent_receipt_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest(),'controls':rows}
(out/'RESULT.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res))
raise SystemExit(0 if res['status']=='PASS' else 1)
