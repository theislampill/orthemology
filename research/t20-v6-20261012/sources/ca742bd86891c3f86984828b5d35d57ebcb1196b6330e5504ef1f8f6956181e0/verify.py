from pathlib import Path
import json,hashlib
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for x in json.loads((R/'MANIFEST.json').read_text()):
 p=R/x['path']
 if not p.is_file() or p.stat().st_size!=x['bytes'] or sha(p)!=x['sha256']:raise RuntimeError('Delivery integrity mismatch: '+x['path'])
for x in json.loads((R/'BINDINGS.json').read_text())['files']:
 if sha(R/x['preserved'])!=x['sha256']:raise RuntimeError('Reviewed source mismatch: '+x['source'])
print(json.dumps({'status':'PASS','reviewed_source_files':4,'scope':'Fresh extraction/source integrity only; analytical claims not numerically or formally proved by this verifier.'},indent=2))
