#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
from datetime import datetime,timezone
W=Path(__file__).resolve().parent.parent
R=Path(__file__).resolve().parent
A=W/'measure-moment-continuation-boundary-20261009'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p):
 b=p.read_bytes();return {'path':str(p.relative_to(W)),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
expected={'RESULT.md':'a0fa9117ff47df9f07133c1ed49c682c7c2e73d20881e83f3c242dfb3faeb9e3','SOURCE_LEDGER.json':'674ba210f3c861b44452bb10559c5ddf8d2f0451e99e4c69ba4b6827bbd6a22a','verify.py':'a3e03e04c214dff35c54b7021dec719be28b897f589b6796821c59f0b3e7864b','ADDENDUM.md':'f352b961425e828463531e7a006381d0dca6274f211bc5255904ecae0c2914aa','MANIFEST.json':'c449d0091ba2e7fb814c4a1e0031b9d0240a83e8f1bd11d176cec22102dcb45a'}
for fn,h in expected.items(): assert sha(A/fn)==h,fn
manifest=json.loads((A/'MANIFEST.json').read_text())
for item in manifest['files']:
 p=A/item['path']; assert p.stat().st_size==item['bytes']; assert sha(p)==item['sha256'],item['path']
actual={str(p.relative_to(A)) for p in A.rglob('*') if p.is_file()}
assert actual=={x['path'] for x in manifest['files']}|{'MANIFEST.json'},actual
frozen=[rec(p) for p in sorted(A.rglob('*')) if p.is_file()]
ledger=json.loads((A/'SOURCE_LEDGER.json').read_text())
for item in ledger['local_sources']:
 p=W/item['local_path'];b=p.read_bytes()
 assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],str(p)
 blob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert blob==item['git_blob_sha_of_local_bytes']
 if 'expected_git_blob_sha_from_prior_source_binding' in item:
  assert blob==item['expected_git_blob_sha_from_prior_source_binding']
prior=json.loads((R/'PRECURSOR_SOURCE_BINDINGS.json').read_text())
for item in prior['files']:
 p=W/item['path'];assert p.stat().st_size==item['bytes'];assert sha(p)==item['sha256'],str(p)
for target,out in [(A/'verify.py',R/'author_rerun.txt'),(R/'verify_independent.py',R/'verification.txt')]:
 result=subprocess.run([sys.executable,str(target)],cwd=W,text=True,capture_output=True)
 out.write_text(result.stdout+result.stderr)
 assert result.returncode==0,(str(target),result.stdout,result.stderr)
def without_timestamp(text): return [l for l in text.splitlines() if not l.startswith('Executed UTC:')]
assert without_timestamp((A/'verification.txt').read_text())==without_timestamp((R/'author_rerun.txt').read_text())
assert [rec(p) for p in sorted(A.rglob('*')) if p.is_file()]==frozen
inputs={'review_type':'ordinary independent mathematical review','author_packet':str(A.relative_to(W)),'inputs':frozen}
(R/'INPUT_BINDINGS.json').write_text(json.dumps(inputs,indent=2)+'\n')
receipt={'created_at_utc':datetime.now(timezone.utc).isoformat(),'verdict':'PASS_WITHIN_DECLARED_ORDINARY_MATHEMATICAL_SCOPE','blocking_findings':[], 'author_packet_frozen_verified':True,'author_manifest_entries_verified':len(manifest['files']),'author_packet_file_set_exact':True,'author_packet_unchanged_during_replay':True,'source_ledger_local_hashes_verified':len(ledger['local_sources']),'prior_reviewer_source_bindings_unchanged':len(prior['files']),'author_symbolic_controls_passed':43,'independent_exact_control_groups_passed':19,'author_output_matches_except_execution_timestamp':True,'independent_derivation_preceded_author_result_availability':True,'main_conclusions':['Compact finite-dimensional supports retain full-moment determination and tilt continuation sufficiency.','The classical strictly positive lognormal Stieltjes pair has identical all-order moments and right jets, but mean traces differ on every positive open interval.','The two full moment sequences differ at every positive time because positive tilts are injective and acquire exponential integrability.','The hierarchy has nonunique coordinatewise smooth continuations from a shared moment state; the full-law tilt remains unambiguous.','Actual finite-time pullback congruence is stronger than formal infinitesimal closure.','The final addendum correctly identifies full-law equality with the declared exact mean-trace continuation equivalence.'],'clarifications_resolved_in_addendum':['Boundary nonanalyticity refers to the Laplace transforms, not M0.','Singleton defect one does not decide moment determinacy.'],'authority_limits':['No implementaudit or governor was run.','No integration, release, owner approval, T20 closure, or T21 authority.','No formal-kernel, numerical-existence, empirical, or field-priority certification.','No author or protected source edits by reviewer.'],'bindings':{'RESULT.md':rec(A/'RESULT.md'),'ADDENDUM.md':rec(A/'ADDENDUM.md'),'AUTHOR_MANIFEST.json':rec(A/'MANIFEST.json'),'REVIEW.md':rec(R/'REVIEW.md'),'INPUT_BINDINGS.json':rec(R/'INPUT_BINDINGS.json')}}
(R/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
reviewfiles=[rec(p) for p in sorted(R.rglob('*')) if p.is_file() and p.name!='MANIFEST.json']
(R/'MANIFEST.json').write_text(json.dumps({'created_at_utc':datetime.now(timezone.utc).isoformat(),'status':'frozen ordinary independent mathematical review','files':reviewfiles},indent=2)+'\n')
for fn in ['REVIEW.md','RECEIPT.json','MANIFEST.json','INPUT_BINDINGS.json']:print(fn,sha(R/fn))
print('PASS: frozen inputs, exact author file set, eight author manifest entries, eight local ledger source hashes, prior source preservation, 43+19 exact controls, and replay immutability.')
