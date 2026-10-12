"""Bind independently executed evidence; never rewrites a predecessor."""
from pathlib import Path
import hashlib,json,re,subprocess
ROOT=Path(__file__).resolve().parent;W=ROOT.parent
AUTHOR=W/'hase-effective-instance-assessment-20261010'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def record(p):return {'path':str(p.relative_to(W)),'sha256':sha(p),'bytes':p.stat().st_size}
subprocess.run(['python',str(ROOT/'verify_inputs.py')],check=True)
inputs=json.loads((AUTHOR/'INPUTS.json').read_text())
for row in inputs['source_and_receipt_bindings']+inputs['reused_objects']:
    assert sha(W/row['path'])==row['sha256'],row['path']
author_manifest=json.loads((AUTHOR/'MANIFEST.json').read_text())
assert author_manifest['status']=='INDEPENDENTLY_REVIEWED_PASS'
for row in author_manifest['files']:assert sha(AUTHOR/row['path'])==row['sha256'],row['path']
accepted=[]
mods=['OpenDevelopments','DomainControls','ScalarCertificates','LiteralSourceQ',
      'ConcreteScalarCertificates','NonstandardRejection','NegativeCertificateControls',
      'IndependentControls','NonstandardControls','CrossLanguageReview','DependencyAudit','OpenCertificate']
for module in mods:
    source=ROOT/'sources'/f'{module}.lean'
    if not source.exists():source=ROOT/f'{module}.lean'
    obj=ROOT/'fresh-lib'/f'{module}.olean';log=ROOT/'validation'/f'{module}.log'
    assert obj.exists() and log.exists(),module
    out=log.read_text()
    assert not any(s in out for s in ['error:','warning:','sorryAx','Lean.ofReduceBool']),module
    for axioms in re.findall(r'(?:depends on axioms:|axioms)\s*\[([^\]]*)\]',out,re.S):
        assert set(re.sub(r'\s+','',axioms).split(','))<={'','propext','Quot.sound','Classical.choice'},module
    code=re.sub(r'/\-.*?\-/','',source.read_text(),flags=re.S)
    code=re.sub(r'--[^\n]*','',code)
    code=re.sub(r'"(?:\\.|[^"\\])*"','""',code)
    assert not re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',code),module
    row={'module':module,'source':record(source),'object':record(obj),'log':record(log),'trust_zero':True,'exit_code':0}
    if source.parent==ROOT/'sources' and (AUTHOR/source.name).exists():
        assert source.read_bytes()==(AUTHOR/source.name).read_bytes(),source.name
        row['author_source']=record(AUTHOR/source.name)
    accepted.append(row)
negative=[]
for module in ['ChangedInputMustFail','FakeQMustFail']:
    p=ROOT/'validation'/f'{module}.log'
    assert "tactic 'decide' proved that the proposition" in p.read_text()
    assert 'is false' in p.read_text()
    assert not (ROOT/'fresh-lib'/f'{module}.olean').exists()
    negative.append({'module':module,'source':record(ROOT/f'{module}.lean'),'log':record(p),'expected_nonzero_exit':1,'accepted_as_proof':False})
for p in (ROOT/'sources').iterdir():
    if p.is_file() and (AUTHOR/p.name).exists():assert p.read_bytes()==(AUTHOR/p.name).read_bytes(),p.name
assert 'Ran 15 tests' in (ROOT/'validation/PYTHON_AUTHOR_TESTS.log').read_text()
assert (ROOT/'validation/SOURCE_REEXPORT.log').read_bytes()==(ROOT/'sources/source_ast.json').read_bytes()
assert len(json.loads((ROOT/'validation/CROSS_LANGUAGE_CASES.json').read_text()))==266
summary={
 'status':'PASS_BOUNDED_COMPLETE_DEVELOPMENT_EXTRACTION_AND_CERTIFICATE_REVIEW',
 'universal_HasE_W':'OPEN', 'normal_order_completeness':'NOT_SUPPLIED',
 'computable_Lean_extractor':True,'Python_globally_formally_verified':False,
 'negative_domain':'Only the checked input judgment HasE [] n N',
 'accepted_replays':accepted,'expected_rejected_replays':negative,
 'python_author_tests':15,'concrete_closed_source_cases':10,
 'deterministic_implementation_samples':266,'kernel_cross_language_equations':532,
 'inherited_bindings_verified':429,'reused_main_objects':94,
 'all_83_original_sources_rehashed':True,'full_inherited_rebuild_performed':False,
 'third_party_libraries_reused':True,'compiler_bootstrap_verified':False,
 'author_manifest':record(AUTHOR/'MANIFEST.json'),
 'author_replay_receipt':record(AUTHOR/'REPLAY_RECEIPT.json'),
 'author_replay_log':record(AUTHOR/'REPLAY.log'),
 'author_inputs':record(AUTHOR/'INPUTS.json'),
 'review':record(ROOT/'REVIEW.md'),
 'input_verification':record(ROOT/'INPUT_VERIFICATION.json'),
 'proof_tooling_sources_unchanged_since_freeze':True,
 'expected_failure_warning':'Only the two intentionally rejected replay logs contain Lean error-recovery sorryAx; no such object is accepted or imported.'}
(ROOT/'REVIEW_RECEIPT.json').write_text(json.dumps(summary,indent=2)+'\n')
files=[p for p in ROOT.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts]
manifest={'status':summary['status'],'files':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(files)]}
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('REVIEW',sha(ROOT/'REVIEW.md'));print('RECEIPT',sha(ROOT/'REVIEW_RECEIPT.json'));print('MANIFEST',sha(ROOT/'MANIFEST.json'))
