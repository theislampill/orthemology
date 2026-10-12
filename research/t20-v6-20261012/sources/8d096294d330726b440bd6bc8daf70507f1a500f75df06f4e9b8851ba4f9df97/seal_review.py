from pathlib import Path
import hashlib,json,subprocess,sys,re
R=Path(__file__).resolve().parent; W=R.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p): return {'path':str(p.relative_to(W)),'sha256':sha(p),'bytes':p.stat().st_size}
for script in ['verify_inputs.py','verify_source_coverage.py']:
    subprocess.run([sys.executable,str(R/script)],check=True)
records=json.loads((R/'REPLAY_RECORDS.json').read_text())
expected=['HasEStructuralBase','HasEStructuralRename','HasEClosedWeakening',
 'ClosedChurchIdentity','EffectiveChurchIdentity','IdentityControls',
 'ClosedChurchReviewControls','ExtensionInputControls','DependencyAudit']
assert set(records)==set(expected)
for mod,row in records.items():
    assert row['exit_code']==0 and row['trust_zero']
    for k in ['source','object','log']:assert sha(W/row[k])==row[k+'_sha256'],(mod,k)
    assert '--trust=0' in row['command']
    out=(W/row['log']).read_text()
    assert not any(s in out for s in ['error:','warning:','sorryAx','Lean.ofReduceBool'])
    source=(W/row['source']).read_text()
    code=re.sub(r'/\-.*?\-/','',source,flags=re.S)
    code=re.sub(r'--[^\n]*','',code);code=re.sub(r'"(?:\\.|[^"\\])*"','""',code)
    assert not re.findall(r'\b(sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',code),mod
    if mod in expected[:6]:
        original=W/('hase-church-structural-20261010' if mod in expected[:3] else 'hase-closed-church-identity-20261010')/(mod+'.lean')
        assert original.read_bytes()==(W/row['source']).read_bytes()
assert '2\n2\n3\n' in (R/'validation/ClosedChurchReviewControls.log').read_text()
assert (R/'validation/ExtensionInputControls.log').read_text().startswith('2\n')
assert 'PASS: exact mutual grammar' in (R/'validation/DependencyAudit.log').read_text()
assert 'version 4.19.0' in (R/'validation/LEAN_VERSION.log').read_text()
summary={
 'status':'PASS_ACTUAL_CLOSED_CHURCH_SOURCE_IDENTITY_COMPLETENESS',
 'verified_input_bindings':len(json.loads((R/'INPUT_VERIFICATION.json').read_text())['records']),
 'actual_HasE_constructors':20,'actual_FormE_constructors':7,
 'accepted_replays':records,
 'author_executable_guards':5,'reviewer_executable_guards':6,
 'runtime_counts':[2,2,3,2],
 'structural_axioms':['propext','Quot.sound'],
 'identity_allowed_axioms':['propext','Classical.choice','Quot.sound'],
 'any_witness_negative_direction_verified':True,
 'direct_identity_construction_piExt_uses':2,'direct_identity_construction_allExt_uses':1,
 'actual_J_derived_Church_input_verified':True,'source_typed_non_SN_control_verified':True,
 'raw_nonconversion_distinction_verified':True,
 'closed_typed_domain_only':True,'untyped_membership_decision':False,
 'unrestricted_type_completeness':False,'internal_universal_W':'NOT_ESTABLISHED',
 'new_field_level_theorem':False,'baseline_rebuilt':False,'compiler_bootstrap_verified':False,
 'protected_repository_mutation':False,'integration':False,
 'author_identity_manifest':rec(W/'hase-closed-church-identity-20261010/MANIFEST.json'),
 'author_structural_manifest':rec(W/'hase-church-structural-20261010/MANIFEST.json'),
 'predecessor_review_manifest':rec(W/'hase-complete-development-review-20261010/MANIFEST.json'),
 'input_verification':rec(R/'INPUT_VERIFICATION.json'),
 'review':rec(R/'REVIEW.md'),
 'proof_sources_unchanged_since_freeze':True,
 'dependency_environment':rec(R/'lean_env.json')}
(R/'REVIEW_RECEIPT.json').write_text(json.dumps(summary,indent=2)+'\n')
files=[p for p in R.rglob('*') if p.is_file() and p.name!='MANIFEST.json' and '__pycache__' not in p.parts]
manifest={'status':summary['status'],'files':[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(files)]}
(R/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('REVIEW',sha(R/'REVIEW.md'))
print('RECEIPT',sha(R/'REVIEW_RECEIPT.json'))
print('MANIFEST',sha(R/'MANIFEST.json'))
