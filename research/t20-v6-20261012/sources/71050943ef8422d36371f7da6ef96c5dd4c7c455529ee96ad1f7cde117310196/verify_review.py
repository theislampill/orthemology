from pathlib import Path
import json, hashlib
out=Path(__file__).resolve().parent; root=out.parent
hashof=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
before=json.loads((out/'ORIGINALS_BEFORE.json').read_text())['files']
assert all((root/r['path']).stat().st_size==r['bytes'] and hashof(root/r['path'])==r['sha256'] for r in before)
binding=json.loads((out/'BINDING_VERIFICATION.json').read_text())['checks']
assert all(c['hash_match'] and c['bytes_match'] and hashof(root/c['path'])==c['expected_sha256'] for c in binding)
extract=json.loads((out/'EXTRACTION_CHECK.json').read_text())['checks']
assert all(c['exact_match'] for c in extract)
ev=json.loads((out/'EVIDENCE_CHECK.json').read_text())['records']
assert all(c['quote'] in (root/c['path']).read_text() and hashof(root/c['path'])==c['source_sha256'] for c in ev)
for p in out.glob('*.json'): json.loads(p.read_text())
print(f'PASS: {len(before)} original files unchanged; {len(binding)} recorded binding checks match; {len(extract)} extraction reproductions exact; {len(ev)} Arabic excerpts exact; JSON parses.')
