from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;W=R.parent;A=W/'prior-evidence-correction-20261010';F=W/'m2-prior-review-replay-20261010'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(A/'RESULT.md')=='7c9a4bc45b9d443661e6bd9b879d87c06dada61b0313d1fd273873b11f8332c8'
assert sha(A/'MANIFEST.json')=='a788df52ff8a7bf12a6246eb3cc49c06c754143f2603e47e3a1d1d64f476abc1'
for x in json.loads((A/'MANIFEST.json').read_text())['files']:
 assert sha(A/x['path'])==x['sha256'] and sha(F/x['path'])==x['sha256']
source=W/'warranted-learning-20261009/sources/atomics/skill/references/tactics/M2-prior-probability.md'
assert sha(source)=='c5af7a5627bd53d33ee189e95b1c236d4cb338694d48cf3da82bf3dcd939f4a6'
assert sha(R/'sources/M2-prior-probability.md')==sha(source)
assert json.loads((R/'INDEPENDENT_CONTROLS.json').read_text())['status']=='PASS'
assert json.loads((F/'CHECK_RESULTS.json').read_text())['assertion_groups']==15
items=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(R.rglob('*')) if p.is_file() and p.name!='MANIFEST.json']
out={'status':'PASS','scope':'Independent complete-source charitable assessment, symbolic Bayesian algebra, proposed conditional correction, fresh author finite-control replay and independent exact-rational controls. No empirical likelihood, theological warrant, equal-prior, runtime-failure or deployed-patch claim.','author_manifest_sha256':sha(A/'MANIFEST.json'),'author_result_sha256':sha(A/'RESULT.md'),'original_source_unchanged':True,'protected_mutations':False,'author_replay_snapshot':str(F.relative_to(W)),'files':items}
(R/'MANIFEST.json').write_text(json.dumps(out,indent=2)+'\n')
print('PASS; review manifest sha256',sha(R/'MANIFEST.json'))
