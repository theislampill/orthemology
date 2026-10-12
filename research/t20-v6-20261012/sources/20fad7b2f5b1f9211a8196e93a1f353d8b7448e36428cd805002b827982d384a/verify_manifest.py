#!/usr/bin/env python3
from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parent
manifest=json.loads((root/'MANIFEST.json').read_text())
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for f in manifest['files']:
    path=root/f['path']
    assert path.stat().st_size==f['bytes'],f['path']
    assert h(path)==f['sha256'],f['path']
ledger=json.loads((root/'SOURCE_LEDGER.json').read_text())
preserved=0
for entry in ledger['local_sources']:
    original=root.parent/entry['path']
    assert h(root/entry['copy_path'])==entry['copy_sha256']
    if original.exists():
        assert h(original)==entry['sha256'],entry['path']
        preserved+=1
print(json.dumps({'status':'PASS','packet_bindings':len(manifest['files']),
                  'unchanged_direct_ancestors_available':preserved},indent=2))
