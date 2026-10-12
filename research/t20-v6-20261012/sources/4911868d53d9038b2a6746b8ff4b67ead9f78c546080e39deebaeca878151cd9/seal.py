from pathlib import Path
import hashlib,json
R=Path(__file__).resolve().parent;W=R.parent;A=W/'effective-stationary-selection-20261010';F=W/'effective-stationary-review-replay-20261010'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(A/'RESULT.md')=='ec03a2d42894f7e16c109631d884fec6023ab85e4c149bc6639d01e399f91f9c'
assert sha(A/'MANIFEST.json')=='dbc337f0600e67326889be3341020b60100bb58cd21b4cded6326fec4c67b15a'
for p,h in json.loads((A/'MANIFEST.json').read_text())['files'].items():assert sha(A/p)==h and sha(F/p)==h,p
assert json.loads((F/'CONTROLS.json').read_text())['total_checks']==5081
for p in ['INDEPENDENT_CHECKS.json','DIAMETER_CHECKS.json']:assert json.loads((R/p).read_text())['status']=='PASS'
items=[{'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in sorted(R.rglob('*')) if p.is_file() and p.name!='MANIFEST.json']
out={'status':'PASS','scope':'Ordinary independent mathematical/effective-representation review, exact cap diameter and universal kernel criterion, explicit diagonal selector obstruction, infinite lift and no-tail boundary; finite corroboration only, no kernel claim.','author_result_sha256':sha(A/'RESULT.md'),'author_manifest_sha256':sha(A/'MANIFEST.json'),'author_snapshot':str(F.relative_to(W)),'protected_mutations':False,'baseline_rebuilt':False,'files':items}
(R/'MANIFEST.json').write_text(json.dumps(out,indent=2)+'\n');print('PASS; review manifest sha256',sha(R/'MANIFEST.json'))
