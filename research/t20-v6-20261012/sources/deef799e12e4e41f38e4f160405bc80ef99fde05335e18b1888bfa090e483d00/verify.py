from pathlib import Path
import json,hashlib,sys
root=Path(__file__).resolve().parent
manifest=json.loads((root/'SOURCE_PACKAGE_MANIFEST.json').read_text())
expected={x['path'] for x in manifest['files']}
actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and p.name!='SOURCE_PACKAGE_MANIFEST.json'}
errors=[]
if expected!=actual:errors.append({'file_set_mismatch':{'missing':sorted(expected-actual),'unexpected':sorted(actual-expected)}})
for x in manifest['files']:
 p=root/x['path']
 if not p.is_file():continue
 b=p.read_bytes()
 if len(b)!=x['bytes'] or hashlib.sha256(b).hexdigest()!=x['sha256']:errors.append({'binding_mismatch':x['path']})
# Check that every included original remains identical to its received binding.
for x in json.loads((root/'PRESERVED_ORIGINALS.json').read_text())['records']:
 p=root/x['path']
 if not p.is_file() or p.stat().st_size!=x['bytes'] or hashlib.sha256(p.read_bytes()).hexdigest()!=x['sha256']:errors.append({'preserved_original_mismatch':x['path']})
print(json.dumps({'success':not errors,'verified_payload_files':len(expected),'preserved_originals':len(json.loads((root/'PRESERVED_ORIGINALS.json').read_text())['records']),'errors':errors},indent=2))
sys.exit(1 if errors else 0)
