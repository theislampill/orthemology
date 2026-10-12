#!/usr/bin/env python3
"""Read-only byte-binding and source provenance checks for this review."""
from pathlib import Path
import hashlib, json, tarfile
ROOT = Path(__file__).resolve().parent
WORKSPACE = ROOT.parents[2]
CENTRAL = WORKSPACE/'tranche7-restart/formal/attribution-kernel-closure/checkpoints/central-v1'
CONTROLS = CENTRAL.parent/'controls-v1'
ACCEPTED = WORKSPACE/'tranche7-restart/delivery/unknown-root-attribution-accepted-v1'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def check_manifest(root, name):
    data = json.loads((root/name).read_text())
    for x in data['files']:
        p = root/x['path']
        assert sha(p) == x['sha256'], str(p)
        assert p.stat().st_size == x['size'], str(p)
    return len(data['files'])
assert sha(CENTRAL/'MANIFEST.json') == '2830c05f25dcda6f05617e6da58bac50eb3ea86cc9671f5b8301417bf2a1d295'
assert sha(CONTROLS/'MANIFEST.json') == 'f29de5f526216178d1925281eef35a8f8558dc15810b6f7e40428324963f93e4'
assert sha(ACCEPTED/'PACKET_MANIFEST.json') == 'ad4d729f661b5ef8007a42d6b529dfa5fd78423a820cf47f7db43a4edfbf20f5'
counts = {}
for base, name in [(CENTRAL,'central'), (CONTROLS,'supplement'), (ACCEPTED,'accepted')]:
    manifest = 'PACKET_MANIFEST.json' if base == ACCEPTED else 'MANIFEST.json'
    counts[name] = check_manifest(base,manifest)
for author, copied in [(CENTRAL,ROOT/'frozen-source'),(CONTROLS,ROOT/'frozen-controls')]:
    for p in author.rglob('*'):
        if p.is_file(): assert p.read_bytes() == (copied/p.relative_to(author)).read_bytes(), str(p)
for x in json.loads((CENTRAL/'SOURCE_BINDING.json').read_text())['files']:
    assert sha(ACCEPTED/x['path']) == x['sha256'], x['path']
for name in ['DynamicInterlock','CoveringCore','UnknownRootAttribution']:
    accepted = ACCEPTED/('' if name == 'UnknownRootAttribution' else 'dependencies')/(name+'.lean')
    assert (CENTRAL/'legacy'/(name+'.lean')).read_bytes() == accepted.read_bytes()
lean = Path('private-locator:cb50f30cfa35bdf3a0cf')
assert sha(lean) == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
mathlib = Path('private-locator:18d48e051fd31eaf177f')
archive = Path('private-locator:c8706d03ffdb12093ad5')
assert sha(archive) == '9fce64f31ba5612df46871eee8b4581c81c120604deb08cc35fa9f0fb543a425'
assert (mathlib/'lean-toolchain').read_text().strip() == 'leanprover/lean4:v4.19.0'
archive_files = 0
with tarfile.open(archive,'r:gz') as t:
    for m in t:
        if not m.isfile(): continue
        relative = Path(*Path(m.name).parts[1:])
        assert (mathlib/relative).read_bytes() == t.extractfile(m).read(), str(relative)
        archive_files += 1
print(json.dumps({'status':'PASS','manifest_entries':counts,'review_copies_byte_identical':True,
  'official_lean_binary_verified':True,'mathlib_archive_files_matching':archive_files},indent=2))
