#!/usr/bin/env python3
"""Expected-failure controls against the independently rebuilt matrix closure."""
import os,pathlib,json,subprocess,sys,hashlib
root=pathlib.Path(__file__).resolve().parent;receipt=pathlib.Path(sys.argv[1]).resolve()
r=json.loads(receipt.read_text());assert r['status']=='PASS';env={**os.environ,'LEAN_PATH':':'.join(r['LEAN_PATH'])}
out=receipt.parent/'negative-controls';out.mkdir(exist_ok=True)
controls={
 'count_classes_not_mass':'''example : heavyCount (programIndex mixedProgram) 1 2 = 1 := by\n  rw [mixed_count_half]\n''',
 'feed_entire_word_early':'''example : outputList (programIndex echoProgram) [true,false] = [false,false] := by\n  rw [echo_prefix_stream]\n''',
 'strict_heavy_threshold':'''example : heavyCount (programIndex mixedProgram) 1 2 = 0 := by\n  rw [mixed_count_half]\n''',
 'wrong_dyadic_denominator':'''example : rationalHeavyMass (P02A2.FiniteOutputTable.indexTable (programIndex mixedProgram)) 1 2 = (heavyCount (programIndex mixedProgram) 1 2 : ℚ≥0) / (2:ℚ≥0)^(2+1) := by\n  rw [rationalHeavyMass_heavyCount,mixed_count_half]\n  norm_num\n''',
 'reject_zero_denominator':'''example : ¬ membershipMatrix (programIndex echoProgram) (Nat.pair 7 0) 1 2 := by\n  simp [membershipMatrix_integer_iff]\n''',
 'treat_one_as_nonvacuous':'''example : ¬ membershipMatrix (programIndex echoProgram) (Nat.pair 1 1) 1 2 := by\n  simp [membershipMatrix_integer_iff]\n''',
 'exclude_rational_equality':'''example : ¬ membershipMatrix (programIndex mixedProgram) (Nat.pair 1 2) 1 2 := by\n  rw [membershipMatrix_integer_iff,mixed_count_half]\n  norm_num\n''',
 'duplicate_word_enumeration':'''example : (allWords 2).length = 5 := by\n  rw [allWords_length]\n  norm_num\n''',
 'drop_positive_scaling':'''example (e a d c k N : ℕ) : membershipMatrix e (Nat.pair (c*a) (c*d)) k N ↔ membershipMatrix e (Nat.pair a d) k N := by\n  exact redundant_fraction e a d c k N\n''',
 'claim_primitive_recursive_matrix':'''example : Primrec (fun z : ℕ => decide (membershipMatrix z.unpair.1 z.unpair.2.unpair.1 z.unpair.2.unpair.2.unpair.1 z.unpair.2.unpair.2.unpair.2)) := membershipMatrix_nat_computable\n''',
}
rows=[]
for name,body in controls.items():
 f=out/(name+'.lean');f.write_text('import MatrixEndpointChecks\nopen P02.Codec P02.Codec.UniformComputability AtomicMembership MatrixIndependentAudit\n'+body)
 p=subprocess.run([r['builds'][0]['command'][0],'-j1',str(f)],cwd=out,env=env,text=True,capture_output=True,timeout=120)
 log=p.stdout+p.stderr;(out/(name+'.log')).write_text(log)
 expected=p.returncode!=0 and ('type mismatch' in log or 'unsolved goals' in log)
 rows.append({'control':name,'exit':p.returncode,'expected_failure':expected,'source_sha256':hashlib.sha256(f.read_bytes()).hexdigest()});print(name,p.returncode,expected,flush=True)
res={'status':'PASS' if all(x['expected_failure'] for x in rows) else 'FAIL','independent_receipt_sha256':hashlib.sha256(receipt.read_bytes()).hexdigest(),'controls':rows}
(out/'RESULT.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res));raise SystemExit(0 if res['status']=='PASS' else 1)
