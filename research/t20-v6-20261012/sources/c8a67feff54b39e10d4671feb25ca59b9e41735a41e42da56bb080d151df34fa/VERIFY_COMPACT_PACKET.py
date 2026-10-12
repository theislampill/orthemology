"""Check compact-packet bytes and declared scope, without requiring omitted witnesses.
Run inside a fresh extracted packet: python VERIFY_COMPACT_PACKET.py
This does not authenticate editions, rerun philosophical interpretation, or close T20.
"""
from pathlib import Path
import hashlib, json, sys
BASE=Path(__file__).resolve().parent
AUTHOR=BASE/'particular-determination-semantics-20261010'
def sha(b): return hashlib.sha256(b).hexdigest()
def git(b): return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def check(path, row):
    b=path.read_bytes()
    assert len(b)==row['bytes'] and sha(b)==row['sha256'],str(path)
    return b
packet=json.loads((BASE/'PACKET_MANIFEST.json').read_text())
entries=packet['entries']
actual={p.relative_to(BASE).as_posix() for p in BASE.rglob('*') if p.is_file()}
assert actual=={r['path'] for r in entries}|{'PACKET_MANIFEST.json'},'File set differs from packet manifest'
for r in entries: check(BASE/r['path'],r)
custody=json.loads((BASE/'CUSTODY_SCOPE.json').read_text())
omitted={r['path']:r for r in custody['omitted_witnesses']}
assert all(not (BASE/p).exists() for p in omitted),'Omitted witness unexpectedly included'
author=json.loads((AUTHOR/'MANIFEST.json').read_text())['entries']
included_author=omitted_author=0
for r in author:
    p=AUTHOR/r['path']
    if p.exists(): check(p,r); included_author+=1
    else:
        key=p.relative_to(BASE).as_posix()
        assert key in omitted and omitted[key]['sha256']==r['sha256'] and omitted[key]['bytes']==r['bytes'],key
        omitted_author+=1
inputs=json.loads((AUTHOR/'INPUT_BINDINGS.json').read_text())['records']
pinned=0
for r in inputs:
    b=check(BASE/r['path'],r)
    assert git(b)==r['actual_git_blob_sha1'],r['path']
    if 'git_blob_sha1' in r: assert git(b)==r['git_blob_sha1']; pinned+=1
selections=json.loads((AUTHOR/'SELECTIONS.json').read_text())['selections']
for r in selections:
    check(BASE/r['path'],r)
    assert r['source'] in omitted,r['source']
    assert 'display_normalization' in r,r['path']
review=BASE/'particular-determination-review-20261010'
assert (review/'REVIEW.md').is_file()
review_manifest=json.loads((review/'MANIFEST.json').read_text())['files']
for r in review_manifest: check(review/r['path'],r)
review_bindings=json.loads((review/'REVIEW_BINDINGS.json').read_text())['files']
review_embedded=review_omitted=0
for r in review_bindings:
    p=BASE/r['path']
    if p.exists(): check(p,r); review_embedded+=1
    else:
        assert r['path'] in omitted and omitted[r['path']]['sha256']==r['sha256'] and omitted[r['path']]['bytes']==r['bytes'],r['path']
        review_omitted+=1
assert sha((AUTHOR/'REPORT.md').read_bytes())=='f16f5e9cb35e5fa47475c3ce1fbcecabdef1233323e973d5a55620dd75696da2'
print(json.dumps({
    'status':'PASS',
    'packet_payload_files_verified':len(entries),
    'author_manifest_entries_verified_from_embedded_bytes':included_author,
    'author_manifest_entries_bound_but_omitted':omitted_author,
    'input_records_verified_from_embedded_bytes':len(inputs),
    'exact_pinned_git_blob_matches':pinned,
    'selected_excerpt_bytes_verified':len(selections),
    'review_manifest_entries_verified':len(review_manifest),
    'review_bound_inputs_verified_from_embedded_bytes':review_embedded,
    'review_bound_inputs_declared_omitted':review_omitted,
    'omitted_witness_files':len(omitted),
    'full_witness_custody_reexecuted':False,
    'excerpt_substring_transform_reexecuted':False,
    'full_witness_check_evidence':'Retained independent reviewer CUSTODY_RECEIPT.json and verify_custody.py; original source files are omitted from this compact packet.',
    'scope':'Compact byte-custody replay only. No fresh source reading, edition authentication, proof of interpretation, new formal result, protected integration or T20 closure.'
},indent=2))
