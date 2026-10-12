"""Read-only terminal evidence validation for the independent composition review."""
from pathlib import Path
import hashlib,json,re
R=Path(__file__).resolve().parent
BASE=R.parent.parent
H=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
versions={1:('06591d2bb2810310182d7c534530352f99b763de702deaf4ff436e37c90222f3','bb589b877490f2956cb3303618dd724ec0135c677f7751bd995b3415c12c3d03'),2:('a795122fa0d4c3d127371e22599bf23a65a9a546d2abdae8d0d96962682416ae','daa8af769210d2b0c8489b74a186399fc61286e5ca8da4f69595dd0af737f651')}
for v,(mh,zh) in versions.items():
 for root in [R/f'freeze-v{v}',BASE/f'formal/composed-execution/delivery/composed-execution-v{v}']:
  assert H(root/'PACKAGE_MANIFEST.json')==mh
  manifest=json.loads((root/'PACKAGE_MANIFEST.json').read_text())
  for x in manifest['files']:
   p=root/x['path']; assert p.stat().st_size==x['bytes'] and H(p)==x['sha256'],str(p)
 for zp in [R/f'Orthemology_Seventh_Composed_Execution_V{v}_20261002.zip',BASE/f'formal/composed-execution/delivery/Orthemology_Seventh_Composed_Execution_V{v}_20261002.zip']:
  assert H(zp)==zh
for folder,manifest_name,mh in [('delivery/dynamic-repair-checkpoint-v2','PACKET_MANIFEST.json','3d620e425f85b9f99681be5ba95ab48f11c4ff9ed706cf56696184e5a9593f67'),('formal/criterion-transport','REVIEW_SNAPSHOT_V3.json','bd349c1c91950f2ed2f1616656a5a5334a22ccdeaad52d4810c9a1e1ccbbc75f')]:
 root=BASE/folder; assert H(root/manifest_name)==mh
 for x in json.loads((root/manifest_name).read_text())['files']:
  p=root/x['path']; assert p.stat().st_size==x.get('bytes',x.get('size')) and H(p)==x['sha256'],str(p)
receipt=json.loads((R/'replay-v2/REPLAY_RECEIPT.json').read_text())
assert receipt['status']=='PASS' and receipt['pass_assertions']==88 and receipt['wrapper_tests']==7
for cmd in receipt['commands']:
 assert cmd['returncode']==0 and H(R/'replay-v2'/cmd['log'])==cmd['sha256']
for n,h in receipt['build_source_hashes'].items(): assert H(R/'replay-v2/build'/n)==h
source=(R/'freeze-v2/Composition.lean').read_text()
assert len(re.findall(r'^theorem ',source,re.M))==26
assert not re.search(r'^axiom |\bsorry\b|\bnative_decide\b|^unsafe ',source,re.M)
mutants=json.loads((R/'mutants-v2/MUTATION_RESULTS.json').read_text())
assert mutants['status']=='PASS' and len(mutants['records'])==6
assert mutants['accepted_source_sha256']==H(R/'freeze-v2/Composition.lean')
for rec in mutants['records']:
 assert rec['status']=='DETECTED' and rec['exit_code']==1
 log=R/'mutants-v2'/rec['mutation']/'runtime.log'
 assert H(log)==rec['runtime_log_sha256'] and rec['expected_failure'] in log.read_text()
extended=R/'extended-v2'
assert (extended/'compile.log').read_text()=='' and (extended/'link.log').read_text()==''
lines=(extended/'runtime.log').read_text().splitlines()
assert lines[-1]=='INDEPENDENT TERMINAL PASS' and sum(l.startswith('PASS independent:') for l in lines)==25
assert not any('FAIL' in l for l in lines)
monotonicity=(extended/'monotonicity-compile.log').read_text()
assert 'error:' not in monotonicity and 'warning:' not in monotonicity and monotonicity.count('depends on axioms:')==3
old=json.loads((R/'replay-v1/REPLAY_RECEIPT.json').read_text())
assert receipt['output_artifact_hashes']==old['output_artifact_hashes']
for name,h in receipt['output_artifact_hashes'].items(): assert H(R/'replay-v2/build'/name)==h
before,installed,repaired=[json.loads((R/f'replay-v2/build/{n}.json').read_text()) for n in ('before','installed','repaired')]
raw=(R/'freeze-v2/imports/proper-function-and-candidate-e.md').read_bytes()
assert installed=={**before,'rule':'exact','rule_version':before['rule_version']+1,'rule_history':before['rule_history']+[before['rule']]}
assert repaired=={**installed,'draft':list(raw),'draft_revision':before['draft_revision']+1,'draft_history':before['draft_history']+[before['draft']]}
for n in ('preserved-source.bin','repaired-draft.bin'): assert (R/f'replay-v2/build/{n}').read_bytes()==raw
print('PASS: original and copied v1/v2 freezes and ZIPs unchanged; all 63 predecessor records unchanged; v2 replay/log bindings; 88+7 checks; six detected runtime mutants; 25 reviewer assertions; three reviewer lemmas; exact full-state outputs.')
