from pathlib import Path
import hashlib,json,re
root=Path(__file__).resolve().parents[1]
inputs=json.loads((root/'INPUT_SOURCE_MANIFEST.json').read_text())
candidate=json.loads((root/'CANDIDATE_v1.json').read_text())
assert hashlib.sha256((root/'INPUT_SOURCE_MANIFEST.json').read_bytes()).hexdigest()==candidate['input_manifest_sha256']
for row in inputs:
 p=root/row['local_path'];b=p.read_bytes()
 assert len(b)==row['bytes'],str(p)
 assert hashlib.sha256(b).hexdigest()==row['sha256'],str(p)
for row in candidate['modules']:
 p=root/row['path'];b=p.read_bytes()
 assert len(b)==row['bytes'],str(p)
 assert hashlib.sha256(b).hexdigest()==row['sha256'],str(p)
 s=b.decode()
 assert not re.search(r'\b(sorry|admit|axiom|sorryAx)\b',s),str(p)
 assert not re.search(r'set_option\s+(maxHeartbeats|maxRecDepth)',s),str(p)
review=json.loads((root/'review/VERIFICATION.json').read_text())
assert all(row['exit_code']==0 for row in review['commands'])
assert hashlib.sha256((root/'review/sources/IndependentControls.lean').read_bytes()).hexdigest()==review['independent_controls_sha256']
print(f'PASS: {len(inputs)} exact accepted modules and {len(candidate["modules"])} frozen extension/check modules plus hash-verified independent controls; no holes, custom axioms or limit overrides in the extension.')
