#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys,zipfile

b=Path(__file__).resolve().parent
digest=lambda data:hashlib.sha256(data).hexdigest()
m=json.loads((b/'MANIFEST.json').read_text())
for item in m['files']:
    raw=(b/item['path']).read_bytes()
    assert len(raw)==item['bytes'] and digest(raw)==item['sha256'],item['path']
assert digest((b/'dependencies/PSPACE_REFINEMENT_V2.md').read_bytes())=='4b560b801f3712be0889c3cd1e9362cbcf0faea09c799ed2be2a52214b8972a9'
assert digest((b/'dependencies/HIDDEN_PARITY_CHARACTERISATION.md').read_bytes())=='71f9d6423816999578aaf97a5333c31f5eeee6a535c13d423fa34665fd0559c3'
with zipfile.ZipFile(b/'dependencies/AUTHOR_COMPLEXITY_V2.zip') as z:
    am=json.loads(z.read('MANIFEST.json'))
    assert set(z.namelist())==set(am)|{'MANIFEST.json'}
    for name,h in am.items():assert digest(z.read(name))==h
    assert z.read('PSPACE_REFINEMENT.md')==(b/'dependencies/PSPACE_REFINEMENT_V2.md').read_bytes()
replay=subprocess.run([sys.executable,str(b/'controls/independent_encoding_controls.py')],text=True,capture_output=True)
assert replay.returncode==0,replay.stderr
actual=json.loads(replay.stdout)
assert actual==json.loads((b/'evidence/INDEPENDENT_CONTROLS.json').read_text())
print(json.dumps({'status':'PASS','manifest_files':len(m['files']),
                  'theorem_v2_bound':True,'independent_controls_replayed':True,
                  'conditional_on_frozen_parity_characterization':True},indent=2))
