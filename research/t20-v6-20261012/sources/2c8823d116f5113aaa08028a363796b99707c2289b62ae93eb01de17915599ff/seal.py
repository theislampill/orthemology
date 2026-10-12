from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;W=R.parent;A=W/'capped-tensor-recovery-20261010';F=W/'capped-tensor-review-replay-20261010'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(A/'RESULT.md')=='262503e92380ec868f28670b18939d701cd51808aedc65f7fe6f2fa57e0dbf6d'
assert sha(A/'MANIFEST.json')=='40315f75e0136493b8706aefdf7bc17a9844a5a38ba60e5d6dd630f84128aad1'
for d in json.loads((A/'MANIFEST.json').read_text())['files']:assert sha(A/d['path'])==d['sha256']==sha(F/d['path'])
assert json.loads((F/'CONTROLS.json').read_text())['checks']==1304
assert json.loads((R/'INDEPENDENT_CHECKS.json').read_text())['total']==2929
files=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(R.rglob('*')) if p.is_file() and p.name!='MANIFEST.json']
out={'status':'PASS','scope':'Independent ordinary positive C1–C7, finite-band recovery, cap-free tensor continuation, support/semantic boundaries, and finite replay. Participating construction role in negative §7.2 disclosed; separate reviewer owns its independent check.','author_result_sha256':sha(A/'RESULT.md'),'author_manifest_sha256':sha(A/'MANIFEST.json'),'snapshot':str(F.relative_to(W)),'baseline_rebuilt':False,'protected_mutations':False,'files':files}
(R/'MANIFEST.json').write_text(json.dumps(out,indent=2)+'\n');print(sha(R/'MANIFEST.json'))
