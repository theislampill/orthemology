from pathlib import Path
import hashlib,json,shutil,subprocess,sys
R=Path(__file__).resolve().parent
W=R.parent
A=W/'bounded-energy-signed-continuation-20261010'
def record(p):
    b=p.read_bytes(); return {'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
files={str(p.relative_to(W)):record(p) for p in sorted(A.rglob('*')) if p.is_file()}
bindings=json.loads((A/'INPUT_BINDINGS.json').read_text())
for item in bindings['files']:
    p=W/item['original_path']; files[str(p.relative_to(W))]=record(p)
F=R/'frozen_workspace'
assert not F.exists(), 'Use a new review version rather than overwriting a frozen snapshot'
for path,rec in files.items():
    out=F/path;out.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(W/path,out)
    assert record(out)==rec
(R/'ARTIFACT_BINDINGS.json').write_text(json.dumps({'status':'FROZEN','source_files':files},indent=2)+'\n')
P=R/'replay_workspace'; shutil.copytree(F,P)
a=subprocess.run([sys.executable,str(P/A.name/'check_controls.py')],capture_output=True,text=True)
(R/'AUTHOR_REPLAY.log').write_text(a.stdout+a.stderr)
assert a.returncode==0,a.stderr
post={path:record(W/path) for path in files}
assert post==files,'Author or ancestry changed during independent replay'
res=json.loads((P/A.name/'CONTROL_RESULTS.json').read_text())
receipt={'status':'PASS','originals_unchanged':True,'frozen_author_result':record(F/A.name/'RESULT.md'),'author_replay_check_count':res['check_count'],'independent_check_count':json.loads((R/'INDEPENDENT_CONTROLS.json').read_text())['count'],'author_replay_exit':a.returncode,'bindings_sha256':record(R/'ARTIFACT_BINDINGS.json')['sha256']}
(R/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
