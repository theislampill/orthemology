"""Byte-custody checks only. These do not prove a source interpretation."""
from pathlib import Path
import hashlib,json
BASE=Path(__file__).resolve().parent.parent
AUTHOR=BASE/'particular-determination-semantics-20261010'
EXPECTED={'REPORT.md':'f16f5e9cb35e5fa47475c3ce1fbcecabdef1233323e973d5a55620dd75696da2',
'INPUT_BINDINGS.json':'3f13d0bb0070644a451a5de4993715898e3eb4ed80794be0a9e100680f977112',
'READING_RECORD.json':'4f3f30efc5fc8c22ae08bc9de36b684faeee183ffc199d3dca8a649eadcd6207',
'MANIFEST.json':'091926f7ab24255c58bdbd150d0a47c534fd1198cac9f0c5f2ceca1c999669d1'}
def sha(b):return hashlib.sha256(b).hexdigest()
def git(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for p,h in EXPECTED.items():assert sha((AUTHOR/p).read_bytes())==h,p
manifest=json.loads((AUTHOR/'MANIFEST.json').read_text())
for row in manifest['entries']:
 data=(AUTHOR/row['path']).read_bytes()
 assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
inputs=json.loads((AUTHOR/'INPUT_BINDINGS.json').read_text())['records']
pinned=0
for row in inputs:
 data=(BASE/row['path']).read_bytes()
 assert len(data)==row['bytes'] and sha(data)==row['sha256'],row['path']
 assert git(data)==row['actual_git_blob_sha1'],row['path']
 if 'git_blob_sha1' in row:
  assert git(data)==row['git_blob_sha1'],row['path']
  pinned+=1
sources=json.loads((AUTHOR/'READING_RECORD.json').read_text())['sources']
for row in sources:
 if 'raw_path' in row:
  raw=(BASE/row['raw_path']).read_bytes();txt=(BASE/row['text_path']).read_bytes()
  assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
  assert git(raw)==row['actual_git_blob_sha1'] and sha(txt)==row['text_sha256']
 else:
  raw=(BASE/row['path']).read_bytes()
  assert len(raw)==row['bytes'] and sha(raw)==row['sha256'] and git(raw)==row['actual_git_blob_sha1']
selections=json.loads((AUTHOR/'SELECTIONS.json').read_text())['selections']
substrings=[]
normalized_count=0
for row in selections:
 data=(BASE/row['path']).read_bytes();source=(BASE/row['source']).read_bytes()
 assert len(data)==row['bytes'] and sha(data)==row['sha256']
 # Explicitly check excerpt copying rather than inferring it from declared provenance.
 if 'MIFTAH_' in row['path']:
  source=source.replace(b'\r\n',b'\n').replace(b'\r',b'\n').replace(b'\x01',b'').replace(b'\x0b',b'\n')
  normalized_count+=1
 assert data in source,row['path']
 substrings.append(row['path'])
print(json.dumps({'status':'PASS','author_manifest_entries':len(manifest['entries']),
 'bound_input_records':len(inputs),'exact_pinned_git_blob_matches':pinned,
 'source_records_verified':len(sources),'selected_excerpts_verified':len(substrings),'direct_literal_substrings':len(substrings)-normalized_count,
 'substrings_after_declared_display_normalization':normalized_count,
 'scope':'Exact byte custody only; no independent edition authentication, proof of interpretation, formal theorem or closure.'},indent=2))
