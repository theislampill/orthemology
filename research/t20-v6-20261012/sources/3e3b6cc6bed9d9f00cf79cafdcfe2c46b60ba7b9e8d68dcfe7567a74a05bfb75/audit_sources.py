#!/usr/bin/env python3
"""Verify immutable accepted inputs and the exact compiled central checkpoint."""
from pathlib import Path
import hashlib, json, sys, datetime
root = Path(__file__).resolve().parent
workspace = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd()
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
binding = json.loads((root/'SOURCE_BINDING.json').read_text())
accepted = workspace/binding['accepted_source']
checks=[]
for x in binding['files']:
    p=accepted/x['path']; actual=sha(p)
    assert actual == x['sha256'], (str(p),actual,x['sha256'])
    checks.append({'path':str(p),'sha256':actual,'status':'MATCH'})
manifest=json.loads((accepted/'PACKET_MANIFEST.json').read_text())
for x in manifest['files']:
    p=accepted/x['path']
    assert p.stat().st_size == x['size'] and sha(p) == x['sha256'], str(p)
for name in ['DynamicInterlock','CoveringCore','UnknownRootAttribution']:
    p=root/'legacy'/f'{name}.lean'
    source=accepted/('' if name=='UnknownRootAttribution' else 'dependencies')/f'{name}.lean'
    assert p.read_bytes()==source.read_bytes(), name
frozen=root/'checkpoints'/'central-v1'
fm=json.loads((frozen/'MANIFEST.json').read_text())
for x in fm['files']:
    p=frozen/x['path']
    assert p.stat().st_size==x['size'] and sha(p)==x['sha256'], str(p)
for name in ['RootImage','Availability','FixedFamilies','Correspondence','ImageMinima','MapTransport']:
    assert (root/f'{name}.lean').read_bytes()==(frozen/f'{name}.lean').read_bytes(),name
lean=Path('private-locator:cb50f30cfa35bdf3a0cf')
assert sha(lean)=='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
mathlib=Path('private-locator:18d48e051fd31eaf177f')
assert (mathlib/'lean-toolchain').read_text().strip()=='leanprover/lean4:v4.19.0'
report={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'status':'PASS','accepted_manifest_entries_verified':len(manifest['files']),
 'accepted_bindings':checks,'legacy_sources_byte_identical':True,
 'frozen_central_manifest_sha256':sha(frozen/'MANIFEST.json'),
 'frozen_entries_verified':len(fm['files']),'working_central_sources_unchanged':True,
 'lean_binary_sha256':sha(lean),'mathlib_commit':binding['mathlib_commit'],
 'mathlib_archive_sha256':sha(Path('private-locator:c8706d03ffdb12093ad5')),
 'mathlib_lake_manifest_sha256':sha(mathlib/'lake-manifest.json')}
print(json.dumps(report,indent=2))
