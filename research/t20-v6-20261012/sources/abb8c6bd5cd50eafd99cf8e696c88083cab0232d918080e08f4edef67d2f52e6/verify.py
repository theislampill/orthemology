"""Reproduce the exact bounded controls and source-preservation check.

Run normally and under -O; no correctness condition uses Python assert.
"""
from pathlib import Path
import hashlib,json,sys,unittest,subprocess
HERE=Path(__file__).resolve().parent
WORK=HERE.parents[1]
sys.dont_write_bytecode=True

def h(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def sources():
    b=json.loads((HERE/'SOURCE_BINDINGS.json').read_text())
    for row in b['sources']:
        if h(WORK/row['path'])!=row['sha256']:raise RuntimeError('Source changed: '+row['id'])
    for row in b['unchanged_import_copies']:
        if h(HERE/row['copy_path'])!=row['sha256']:raise RuntimeError('Copy changed: '+row['source_id'])
    return {'sources':len(b['sources']),'unchanged_copies':len(b['unchanged_import_copies'])}

before=sources()
import test_cache_transport as cache_tests
import test_policy_contracts as policy_tests
suite=unittest.TestSuite((unittest.defaultTestLoader.loadTestsFromModule(cache_tests),unittest.defaultTestLoader.loadTestsFromModule(policy_tests)))
result=unittest.TextTestRunner(verbosity=2).run(suite)
if not result.wasSuccessful():raise SystemExit(1)
after=sources()
C=cache_tests.CacheTransportTests;P=policy_tests.PolicyContractTests
negative_controls={}
for name in ('cache_normalization','branch_pasting','snapshot_survives_revision'):
    command=[sys.executable,'-B']+(['-O'] if sys.flags.optimize else [])+[str(HERE/'false_claim.py'),name]
    run=subprocess.run(command,capture_output=True,text=True,cwd=HERE)
    marker='INTENDED_FALSE_CLAIM_REJECTED: '+name
    if run.returncode==0 or marker not in run.stderr:
        raise RuntimeError('False claim did not fail for intended reason: '+name)
    logname=('optimized-' if sys.flags.optimize else 'normal-')+'false-'+name+'.log'
    (HERE/logname).write_text(run.stdout+run.stderr)
    negative_controls[name]={'exit_code':run.returncode,'intended_marker':marker,'log':logname}

files={str(p.relative_to(HERE)):h(p) for p in sorted(HERE.rglob('*')) if p.is_file() and p.suffix in ('.py','.md') and 'review' not in p.parts}
receipt={'schema':'t20.proof-inquiry.verification.v1','python_optimized':bool(sys.flags.optimize),'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),'source_preservation_before':before,'source_preservation_after':after,'counts':{'cache_oracle_cases':C.oracle_cases,'dependency_profile_cases':C.dependency_profile_cases,'passive_interleaving_cases':P.postponement_cases,'source_revision_interleaving_cases':P.revision_cases,'finite_memory_controllers':P.finite_memory_controllers,'integer_likelihood_histories':P.likelihood_histories,'likelihood_prefix_comparisons':P.likelihood_prefix_comparisons},'negative_controls':negative_controls,'bound_files':files,'evidence_scope':'Exact finite controls and inherited executable calls; ordinary universal proofs in RESULT.md. No fresh Lean compilation, external empirical evidence, real source authentication or production adoption.'}
name='VERIFICATION_OPTIMIZED.json' if sys.flags.optimize else 'VERIFICATION.json'
(HERE/name).write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({'receipt':name,'tests':result.testsRun,'counts':receipt['counts']}))
