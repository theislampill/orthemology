#!/usr/bin/env python3
"""Verify frozen author/source bytes and replay the author script only under this review."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent
AUTHOR=ROOT.parent/'same-threshold-replay'
EXPECTED='f58c75e855e51be1bf4818b2b4ea6a91b1b5e685cbd45cfe304e9c3627fcbf53'

def digest(path): return sha256(path.read_bytes()).hexdigest()
def verify(path,record):
    assert path.is_file(),str(path)
    assert digest(path)==record['sha256'],str(path)
    assert path.stat().st_size==record['bytes'],str(path)
    return {'path':str(path.relative_to(ROOT.parent)),'sha256':digest(path),'bytes':path.stat().st_size,'verified':True}

manifest_path=AUTHOR/'MANIFEST.json'
assert digest(manifest_path)==EXPECTED
manifest=json.loads(manifest_path.read_text())
verified_author=[verify(AUTHOR/x['path'],x) for x in manifest['files']]
bindings=json.loads((AUTHOR/'SOURCE_BINDINGS.json').read_text())
verified_inputs=[verify(AUTHOR/x['path'],x) for x in bindings['inputs']]
verified_predecessors=[]
for entry in bindings['predecessor_manifests']:
    path=(AUTHOR/entry['path']).resolve()
    got=verify(path,entry)
    source_manifest=json.loads(path.read_text())
    # Verify against the actual predecessor manifest, not merely the author's copied list.
    originals={x['path']:x for x in source_manifest['files']}
    copied={x['path']:x for x in entry['verified_payloads']}
    assert originals.keys()==copied.keys()
    files=[]
    for rel,orig in originals.items():
        assert orig['sha256']==copied[rel]['sha256']
        assert orig['bytes']==copied[rel]['bytes']
        files.append(verify(path.parent/rel,orig))
    got['payloads']=files
    verified_predecessors.append(got)
pre=json.loads((ROOT/'preinspection_manifest.json').read_text())
verified_independent=[verify(ROOT/x['path'],x) for x in pre['files']]
replay=ROOT/'replay'
(replay/'results').mkdir(parents=True,exist_ok=True)
shutil.copyfile(AUTHOR/'exact_controls.py',replay/'exact_controls.py')
assert digest(replay/'exact_controls.py')==digest(AUTHOR/'exact_controls.py')
run=subprocess.run([sys.executable,str(replay/'exact_controls.py')],capture_output=True,text=True,cwd=str(replay))
(replay/'results'/'stdout.log').write_text(run.stdout)
(replay/'results'/'stderr.log').write_text(run.stderr)
assert run.returncode==0,run.stderr
assert (replay/'results'/'exact_controls.json').read_bytes()==(AUTHOR/'results'/'exact_controls.json').read_bytes()
assert (replay/'results'/'stdout.log').read_bytes()==(AUTHOR/'results'/'exact_controls.log').read_bytes()
output=json.loads((replay/'results'/'exact_controls.json').read_text())
assert output['status']=='PASS' and output['assertions']==16598 and len(output['families'])==29
# End-of-replay recheck proves all bound external files stayed byte-identical.
assert digest(manifest_path)==EXPECTED
for x in manifest['files']: verify(AUTHOR/x['path'],x)
for x in bindings['inputs']: verify(AUTHOR/x['path'],x)
for entry in bindings['predecessor_manifests']:
    path=(AUTHOR/entry['path']).resolve(); verify(path,entry)
    for x in entry['verified_payloads']: verify(path.parent/x['path'],x)
result={
 'status':'PASS','verified_utc':datetime.now(timezone.utc).isoformat(),
 'author_manifest_sha256':EXPECTED,'author_payloads':verified_author,
 'source_inputs':verified_inputs,'predecessor_manifests':verified_predecessors,
 'preinspection_independent_payloads':verified_independent,
 'author_replay':{'exit_code':run.returncode,'assertions':output['assertions'],'families':len(output['families']),'script_byte_identical':True,'output_json_byte_identical':True,'stdout_byte_identical':True,'executed_only_in_review':True},
 'end_of_run_author_and_predecessor_recheck':'PASS',
 'scope':'Byte verification and reproducibility; reading coverage and mathematics are addressed separately in REVIEW.md.'
}
(ROOT/'evidence_verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'author_payloads':len(verified_author),'source_inputs':len(verified_inputs),'predecessor_manifests':len(verified_predecessors),'predecessor_payloads':sum(len(x['payloads']) for x in verified_predecessors),'author_replay':result['author_replay']},indent=2))
