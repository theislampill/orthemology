from pathlib import Path
import hashlib,json,re,subprocess
from datetime import datetime,timezone
base=Path(__file__).resolve().parent
root=base.parent
author=root/'separating-projection-lean-20261009'
copy=base/'clean-copy'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
source_rows={}
for line in (base/'logs/frozen-source-sha256.txt').read_text().splitlines():
 expected,path=line.split(None,1)
 assert sha(copy/path)==expected,(path,'copy hash')
 assert sha(author/path)==expected,(path,'author hash')
 assert (copy/path).read_bytes()==(author/path).read_bytes(),path
 source_rows[path]=expected
assert len(source_rows)==10
assert (copy/'MomentRecovery.lean').read_bytes()==(root/'finite-moment-recovery-lean-20261009/MomentRecovery.lean').read_bytes()
assert (copy/'lake-manifest.json').read_bytes()==(root/'finite-moment-recovery-lean-20261009/lake-manifest.json').read_bytes()
allowed={'propext','Classical.choice','Quot.sound'}
expected=[]
for filename,namespace in [('MomentRecovery.lean','FiniteMoment'),('SeparatingProjection.lean','FiniteMoment'),('Checks.lean','FiniteMoment.Checks')]:
 text=(copy/filename).read_text()
 assert not re.search(r'\b(sorry|admit|axiom|native_decide|unsafe|partial|implemented_by|run_tac)\b',text),filename
 expected += [namespace+'.'+x for x in re.findall(r'^(?:def|theorem)\s+(\w+)',text,re.M)]
verify=(copy/'Verify.lean').read_text()
for line in verify.splitlines():
 assert not line.strip() or re.match(r'^import \w+$|^#print axioms [\w.]+$',line),line
assert len(expected)==len(set(expected))==34
rows=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",(copy/'logs/fresh-Verify.log').read_text())
assert len(rows)==34 and {name for name,_ in rows}==set(expected)
for name,axioms in rows:
 assert {x.strip() for x in axioms.split(',') if x.strip()}<=allowed,(name,axioms)
review_rows=re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",(base/'logs/reviewer-checks.log').read_text())
assert len(review_rows)==13
for name,axioms in review_rows:
 assert {x.strip() for x in axioms.split(',') if x.strip()}<=allowed,(name,axioms)
assert 'error:' not in (base/'logs/reviewer-checks.log').read_text()
neg_inf=(copy/'logs/control-RejectMissingInfinite.log').read_text()
neg_dist=(copy/'logs/control-RejectMissingDistinctness.log').read_text()
assert 'failed to synthesize' in neg_inf and 'Infinite K' in neg_inf
assert 'type mismatch' in neg_dist and 'Function.Injective x →' in neg_dist
prior=json.loads((base/'logs/author-prior-artifacts.json').read_text())
prior_rows=[]
for path,expected_hash in prior.items():
 actual=sha(root/path) if (root/path).is_file() else None
 assert actual==expected_hash,(path,actual,expected_hash)
 prior_rows.append({'path':path,'expected':expected_hash,'actual':actual,'matches':True})
(base/'logs/predecessor-after.json').write_text(json.dumps({'count':len(prior_rows),'all_match':True,'files':prior_rows},indent=2)+'\n')
deps=json.loads((base/'logs/dependency-oleans.json').read_text())
for path,expected_hash in deps.items():
 assert sha(copy/'.lake/packages'/path)==expected_hash,('copy dependency changed',path)
 assert sha(author/'.lake/packages'/path)==expected_hash,('author dependency changed',path)
assert len(deps)==1526
pins=json.loads((base/'logs/dependency-pins.json').read_text())
for dep in pins:
 p=copy/'.lake/packages'/dep['name']
 assert subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()==dep['revision']
 assert not subprocess.check_output(['git','--no-optional-locks','-C',str(p),'status','--porcelain','--untracked-files=no'],text=True).strip()
receipt={
 'review_completed_utc':datetime.now(timezone.utc).isoformat(),
 'status':'PASS',
 'scope':'Independent bounded formal verification of separating scalar projection and composition with inherited finite-moment recovery',
 'clean_project_build':{'start_utc':'2026-10-09T22:34:51Z','end_utc':'2026-10-09T22:35:19Z','exit_code':0,'had_prior_project_build_outputs':False,'modules':['MomentRecovery','SeparatingProjection','Checks','Verify'],'fresh_direct_reelaboration_each_module':True},
 'author_declarations_audited':34,
 'reviewer_theorems_checked':8,
 'additional_imported_lemmas_audited':5,
 'axioms_allowed':sorted(allowed),
 'negative_controls':{'RejectMissingInfinite':'EXPECTED_REJECTION: Infinite K instance unavailable','RejectMissingDistinctness':'EXPECTED_REJECTION: required injectivity argument not supplied'},
 'source_sha256':source_rows,
 'source_inventory_sha256':sha(base/'logs/frozen-source-sha256.txt'),
 'review_checks_sha256':sha(base/'ReviewChecks.lean'),
 'lean_toolchain':'leanprover/lean4:v4.19.0',
 'lean_commit':'6caaee842e94',
 'lean_executable_sha256':sha(root/'.toolchains/lean-4.19.0-linux/bin/lean'),
 'lake_executable_sha256':sha(root/'.toolchains/lean-4.19.0-linux/bin/lake'),
 'dependencies':pins,
 'dependency_oleans_matched_before_and_after':1526,
 'dependency_build_library_oleans':1524,
 'dependency_lake_config_oleans':2,
 'dependency_hash_inventory_sha256':sha(base/'logs/dependency-oleans.json'),
 'predecessor_preservation':{'artifact_count':len(prior_rows),'all_match_before_and_after':True,'inherited_scalar_source_byte_identical':True,'inherited_lockfile_byte_identical':True},
 'ordinary_result_sha256':sha(root/'tensor-moment-continuation-20261009/RESULT.md'),
 'metadata_observation':'Lockfile root name remains finite_moment_recovery; current lakefile package name is separating_projection. Fresh Lake build uses intended targets and exact pins. Nonblocking inherited-label metadata.',
 'trust_boundary':'Shared pinned Lean installation and dependency provenance; dependency artifacts copied and verified, not rebuilt independently. Fresh checking of every local proof source. No full mathlib/compiler rebuild or external attestation.',
 'excluded':['Executable direction-search algorithm','Tensor-space/contraction formalisation','ODE or analytic continuation formalisation','Protected-repository integration','Audit-governor closure','T20/T21 closure']
}
(base/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS: 10 frozen source/config/control files byte-identical; 34 author declarations; 8 reviewer theorems; 5 imported lemmas; 2 intended negative controls; 69 predecessor files preserved; 1,526 dependency oleans unchanged.')
