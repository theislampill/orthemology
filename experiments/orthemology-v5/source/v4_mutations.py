#!/usr/bin/env python3
"""Controlled guard removals in isolated copies; NEVER a mocked Lean build.
Each named positive test is first run against real source. The paired mutant
must make that same test fail with an assertion, not merely fail to import.
The exact source patch and both raw outputs are retained.
"""
import argparse,hashlib,json,os,re,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
# Each removal is a specific mechanism; duplicate/fallback guards are explained.
MUTANTS=[
 ('version_identity','build_gate.py',[("if m is None or m.group(1)!=expected:","if False:")], 'test_build_gate.BuildGateTests.test_version_exact_not_just_recorded'),
 ('audit_target_coverage','build_gate.py',[("if len(names)!=len(set(names)) or set(names)!=set(targets):","if False:")], 'test_build_gate.BuildGateTests.test_each_target_requires_type_and_axioms'),
 ('mandatory_role_floor','build_gate.py',[("if not MANDATORY_TARGETS<=set(all_targets):","if False:")], 'test_build_gate.ContractGateTests.test_required_role_cannot_be_deleted_with_its_source'),
 ('nested_manifest_coverage','build_gate.py',[("if actual!=expected:","if False:")], 'test_build_gate.BuildGateTests.test_manifest_exact_including_nested_manifest'),
 ('raw_duplicate_keys','boundaries.py',[("if k in d:raise Rejection('encoding: duplicate key '+k)","if False:raise Rejection('encoding: duplicate key '+k)")], 'test_v4_regressions.InputRepairs.test_bytes_duplicate_and_bad_encoding'),
 ('absence_of_obligation_binding','operational.py',[("deps.add('need:'+key)","pass # mutated: omitted negative dependency")], 'test_observation_revision.ProbabilityLicences.test_add_requirement_invalidates_preexisting'),
 ('dispatch_version_binding','operational.py',[("return all(rule[1] and self._stamp(k)==rule for k,rule in c.bindings)","return all(rule[1] for k,rule in c.bindings)")], 'test_observation_revision.ProbabilityLicences.test_law_version_change_same_numbers_invalidates'),
 ('ticket_issuer_binding','operational.py',[("if licence.issuer is not self._issuer:","if False:")], 'test_ticket_collision.IssuerBindingTests.test_identical_ticket_bytes_in_two_engines_do_not_cross_authorise'),
 ('ticket_registry_uniqueness','operational.py',[("if token not in self._issued:","if True:")], 'test_ticket_collision.TicketCollisionTests.test_collision_cannot_revive_revoked_ticket'),
 ('census_assertion_under_optimisation','census.py',[("if not condition:raise AssertionError", "if not condition:raise AssertionError")], 'test_v4_regressions.InputRepairs.test_optimisation_negative_control'),
]

def run(test,cwd,mode=()):
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
 p=subprocess.run([sys.executable,'-B',*mode,'-m','unittest',test,'-v'],cwd=cwd/'tests',env={**env,'PYTHONPATH':str(cwd)},capture_output=True,text=True,timeout=40)
 return {'exit_code':p.returncode,'stdout':p.stdout,'stderr':p.stderr}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args();a.output_dir.mkdir(parents=True,exist_ok=True);rows=[]
 for name,file,patches,test in MUTANTS:
  with tempfile.TemporaryDirectory(prefix='orth-v4-mutant-') as td:
   dst=Path(td)
   for p in ROOT.glob('*.py'):shutil.copy2(p,dst/p.name)
   shutil.copytree(ROOT/'tests',dst/'tests',ignore=shutil.ignore_patterns('__pycache__'))
   original=(dst/file).read_text()
   if name=='census_assertion_under_optimisation':
    # Replace the single checked predicate by Python assert. The same deliberately
    # corrupted substitution is then caught normally but escapes in child -O.
    before="def require(ok: bool, label: str) -> None:\n    if not ok:\n        raise RuntimeError('census: ' + label)\n"
    after='def require(ok: bool, label: str) -> None:\n    assert ok, label\n'
    patches=[(before,after)]
   # This is not a Lean simulator. The positive named test is checked first.
   positive=run(test,dst);changed=original
   for before,after in patches:
    if changed.count(before)!=1:raise RuntimeError(f'{name}: ambiguous/missing patch {before!r}')
    changed=changed.replace(before,after)
   (dst/file).write_text(changed)
   negative=run(test,dst)
   positive_ok=positive['exit_code']==0 and 'Ran 1 test' in positive['stderr']
   killed=negative['exit_code']!=0 and 'Ran 1 test' in negative['stderr'] and 'AssertionError' in negative['stderr'] and 'FAILED (failures=' in negative['stderr']
   record={'name':name,'file':file,'test':test,'source_sha256':hashlib.sha256(original.encode()).hexdigest(),'patches':[{'before':x,'after':y} for x,y in patches],'positive':positive,'negative':negative,'positive_ok':positive_ok,'detected_by_intended_test':killed,'scope':'GUARD_REGRESSION_NOT_KERNEL'}
   (a.output_dir/(name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
   rows.append({k:record[k] for k in ['name','test','positive_ok','detected_by_intended_test']})
 result={'status':'PASS' if all(x['positive_ok'] and x['detected_by_intended_test'] for x in rows) else 'FAIL','mutants':len(rows),'results':rows}
 print(json.dumps(result,indent=2));return 0 if result['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
