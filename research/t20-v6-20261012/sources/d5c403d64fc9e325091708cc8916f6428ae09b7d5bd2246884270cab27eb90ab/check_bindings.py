#!/usr/bin/env python3
"""Independent read-only freeze, original-source and toolchain checks."""
from pathlib import Path
import hashlib,json,sys,tarfile
root=Path(__file__).resolve().parent
workspace=root.parents[2]
candidate=Path(sys.argv[1]).resolve()
expected=sys.argv[2]
out=Path(sys.argv[3])
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def manifest(base,name):
 data=json.loads((base/name).read_text());checks=[]
 for e in data['files']:
  p=base/e['path']; ok=sha(p)==e['sha256'] and p.stat().st_size==e['size']
  if not ok: raise RuntimeError('Manifest mismatch: '+str(p))
  checks.append(e['path'])
 return checks
if sha(candidate/'MANIFEST.json')!=expected: raise RuntimeError('Wrong candidate manifest')
files=manifest(candidate,'MANIFEST.json')
actual={str(p.relative_to(candidate)) for p in candidate.rglob('*') if p.is_file()}
if actual!=set(files)|{'MANIFEST.json'}: raise RuntimeError('Unexpected candidate inventory')
binding=json.loads((candidate/'SOURCE_BINDING.json').read_text());bound=[]
for e in binding['inputs']:
 orig=workspace/e['source'];copy=candidate/e['copy']
 if not orig.exists(): raise RuntimeError('Original is required for cold review: '+str(orig))
 if sha(orig)!=e['sha256'] or orig.read_bytes()!=copy.read_bytes(): raise RuntimeError('Original/copy mismatch '+str(orig))
 bound.append(e['source'])
accepted=workspace/'tranche7-restart/delivery/unknown-root-attribution-accepted-v1'
if sha(accepted/'PACKET_MANIFEST.json')!='ad4d729f661b5ef8007a42d6b529dfa5fd78423a820cf47f7db43a4edfbf20f5': raise RuntimeError('Wrong accepted manifest')
accepted_files=manifest(accepted,'PACKET_MANIFEST.json')
dep=workspace/'tranche7-restart/formal/attribution-kernel-closure/checkpoints/central-v1'
if sha(dep/'MANIFEST.json')!=binding['dependency_manifest_sha256']: raise RuntimeError('Wrong dependency manifest')
dep_files=manifest(dep,'MANIFEST.json')
lean=Path('private-locator:cb50f30cfa35bdf3a0cf')
if sha(lean)!=binding['lean_sha256']: raise RuntimeError('Wrong Lean binary')
archive=Path('private-locator:c8706d03ffdb12093ad5');mathlib=Path('private-locator:18d48e051fd31eaf177f')
if sha(archive)!='9fce64f31ba5612df46871eee8b4581c81c120604deb08cc35fa9f0fb543a425': raise RuntimeError('Wrong Mathlib archive')
n=0
with tarfile.open(archive,'r:gz') as tar:
 for m in tar:
  if not m.isfile(): continue
  parts=Path(m.name).parts
  if parts[0]!='mathlib4-c44e0c8ee63ca166450922a373c7409c5d26b00b': raise RuntimeError('Wrong Mathlib tree prefix')
  p=mathlib/Path(*parts[1:])
  if p.read_bytes()!=tar.extractfile(m).read(): raise RuntimeError('Mathlib source changed: '+str(p))
  n+=1
result={'status':'PASS','candidate_manifest':expected,'candidate_entries':len(files),'bound_originals_checked':bound,'accepted_entries':len(accepted_files),'attribution_dependency_entries':len(dep_files),'lean_sha256':sha(lean),'mathlib_revision':binding['mathlib_commit'],'mathlib_archive_sha256':sha(archive),'mathlib_source_files_checked':n,'cached_third_party_libraries_reused':True}
out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
