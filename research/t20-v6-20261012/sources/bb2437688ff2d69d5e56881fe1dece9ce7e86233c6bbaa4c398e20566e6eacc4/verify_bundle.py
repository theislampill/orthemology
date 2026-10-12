from pathlib import Path
import hashlib,json
p=Path(__file__).resolve().parent
r=json.loads((p/'MANIFEST.json').read_text())
for item in r['files']:
 f=p/item['path']
 if not f.is_file() or hashlib.sha256(f.read_bytes()).hexdigest()!=item['sha256']:
  raise SystemExit('FAIL: '+item['path'])
print('PASS:',len(r['files']),'bundled files match the manifest')
