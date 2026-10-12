"""Verify the reviewed bytes and independently recorded replay outputs.
Run from any cwd while the sibling source directories remain available.
"""
from pathlib import Path
import hashlib, json

HERE=Path(__file__).resolve().parent
BASE=HERE.parent
snapshot=json.loads((HERE/'INPUT_SNAPSHOT.json').read_text())
for row in snapshot['files']:
    data=(BASE/row['path']).read_bytes()
    assert len(data)==row['bytes'],row['path']
    assert hashlib.sha256(data).hexdigest()==row['sha256'],row['path']
source=json.loads((BASE/'source-audit-revision-semantics-20261010/SOURCE_BINDINGS.json').read_text())
for row in source['files']:
    data=(BASE/row['path']).read_bytes()
    assert len(data)==row['bytes']
    assert hashlib.sha256(data).hexdigest()==row['sha256']
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==row['git_blob_sha1']
    if 'normalized_git_blob_sha1' in row:
        assert data.endswith(b'\n\n')
        normalized=data[:-1]
        assert len(normalized)==row['normalized_bytes']
        assert hashlib.sha1(b'blob '+str(len(normalized)).encode()+b'\0'+normalized).hexdigest()==row['normalized_git_blob_sha1']
author=json.loads((HERE/'AUTHOR_REPLAY.json').read_text())
assert author==json.loads((BASE/'source-audit-revision-20261010/CONTROL_RESULTS.json').read_text())
triple=json.loads((HERE/'TRIPLE_INTERACTION_REPLAY.json').read_text())
assert triple==json.loads((BASE/'source-audit-revision-20261010/TRIPLE_CONTROL_RESULTS.json').read_text())
for name in ('TRIPLE_INTERACTION.md','check_triple_interaction.py'):
    assert (BASE/'audit-aware-correction-root-20261010'/name).read_bytes()==(BASE/'source-audit-revision-20261010/companions'/name).read_bytes()
for name in ('AUTHOR_REPLAY.json','ZERO_AUDIT_REPLAY.json','TRIPLE_INTERACTION_REPLAY.json','INDEPENDENT_RESULTS.json'):
    assert json.loads((HERE/name).read_text())['status']=='PASS'
print(json.dumps({'status':'PASS','bound_files':len(snapshot['files']),
 'source_bindings_verified':len(source['files']),
 'cp03_one_final_lf_difference_verified':True,
 'author_replay_matches_recorded_output':True,
 'root_companions_byte_identical':True,
 'triple_replay_matches_recorded_output':True,
 'scope':'Snapshot integrity and recorded replay comparison; no empirical or formal-kernel certification.'},indent=2))
