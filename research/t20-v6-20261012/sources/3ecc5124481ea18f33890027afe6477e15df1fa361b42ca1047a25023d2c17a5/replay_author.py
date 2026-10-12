#!/usr/bin/env python3
"""Replay the unchanged author program on digest-bound copies; never edit inputs."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,difflib
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
AUTHOR=ROOT/'tensor-likelihood-closure-20261010'
OLD=ROOT/'positive-instrument-cone-review-delta-20261010/PRE_PRECISION_RESULT.md'
EXPECTED='4f5d51008ec623911221c23d685ce21e64c76d9cb6c1ef6c53877b802053fda9'
def digest(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def write(name,x): (HERE/name).write_text(json.dumps(x,indent=2)+'\n')
# Portable mode needs only this review directory and its bundled replay tree.
if '--portable' in sys.argv:
 pa=HERE/'author_replay'/'tensor-likelihood-closure-20261010'
 pm=json.loads((pa/'MANIFEST.json').read_text())
 for f in pm['files']:
  assert digest(pa/f['path'])=={k:f[k] for k in ('bytes','sha256')}
 assert digest(pa/'RESULT.md')['sha256']==EXPECTED
 cp=subprocess.run([sys.executable,str(pa/'verify.py')],capture_output=True,text=True)
 assert cp.returncode==0,cp.stderr
 got=json.loads(cp.stdout)
 assert got['groups']==13 and got['status']=='PASS'
 for f in pm['files']:
  assert digest(pa/f['path'])=={k:f[k] for k in ('bytes','sha256')}
 print(json.dumps({'status':'PASS','author_groups':13,'mode':'portable digest-bound replay','current_external_paths_checked':False},indent=2))
 sys.exit(0)
assert digest(AUTHOR/'RESULT.md')['sha256']==EXPECTED
manifest=json.loads((AUTHOR/'MANIFEST.json').read_text())
before={p.name:digest(p) for p in AUTHOR.iterdir() if p.is_file()}
for f in manifest['files']: assert before[f['path']]=={k:f[k] for k in ('bytes','sha256')}
bindings=json.loads((AUTHOR/'INPUT_BINDINGS.json').read_text())
rr=HERE/'author_replay'
rr.mkdir(exist_ok=True)
pa=rr/AUTHOR.name
shutil.copytree(AUTHOR,pa,dirs_exist_ok=True)
inputcheck=[]
for item in bindings['local_inputs']:
 src=ROOT/item['path'];dst=rr/item['path'];dst.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(src,dst)
 got=digest(src)
 inputcheck.append({'path':item['path'],'expected':{k:item[k] for k in ('bytes','sha256')},'observed':got,'matches':got=={k:item[k] for k in ('bytes','sha256')}})
failures=[x for x in inputcheck if not x['matches']]
assert len(failures)==1 and failures[0]['path']=='positive-instrument-cone-transport-20261010/RESULT.md'
cp=subprocess.run([sys.executable,str(pa/'verify.py')],capture_output=True,text=True)
(HERE/'author_current_path_failure.txt').write_text(cp.stdout+cp.stderr)
assert cp.returncode!=0 and failures[0]['path'] in cp.stderr
oldexpected=failures[0]['expected']
assert digest(OLD)==oldexpected
oldcopy=rr/failures[0]['path'];shutil.copy2(OLD,oldcopy)
current=(ROOT/failures[0]['path']).read_text();old=OLD.read_text()
diff=''.join(difflib.unified_diff(old.splitlines(keepends=True),current.splitlines(keepends=True),fromfile='digest_bound_cone_RESULT.md',tofile='current_cone_RESULT.md'))
(HERE/'DEPENDENCY_DIFF.patch').write_text(diff)
cp=subprocess.run([sys.executable,str(pa/'verify.py')],capture_output=True,text=True)
(HERE/'author_bound_replay.txt').write_text(cp.stdout+cp.stderr)
assert cp.returncode==0,cp.stderr
reproduced=json.loads(cp.stdout)
assert reproduced==json.loads((AUTHOR/'CONTROL_RESULTS.json').read_text())
assert (pa/'CONTROL_RESULTS.json').read_bytes()==(AUTHOR/'CONTROL_RESULTS.json').read_bytes()
after={p.name:digest(p) for p in AUTHOR.iterdir() if p.is_file()}
assert before==after
write('AUTHOR_REPLAY_RESULTS.json',{'status':'PASS_ON_BOUND_SNAPSHOT_WITH_EXPLICIT_CURRENT_PATH_DRIFT','author_groups':reproduced['groups'],'output_byte_identical':True,'frozen_author_unchanged':True,'current_path_replay_exit':1,'bound_snapshot_replay_exit':0,'old_cone_source':str(OLD.relative_to(ROOT)),'old_cone_provenance':'Reconstructed by author using exact inverse of two recorded edits; digest matches original tensor binding. Not represented as an independently retained historical snapshot.','input_checks':inputcheck})
write('INPUT_BINDINGS.json',{'date_utc':'2026-10-10','reviewed_packet':{'directory':AUTHOR.name,'files':before},'bound_author_dependencies':inputcheck,'replay_old_cone':{'path':str(OLD.relative_to(ROOT)),**digest(OLD)},'delta_provenance':{'path':'positive-instrument-cone-review-delta-20261010/PROVENANCE.json',**digest(ROOT/'positive-instrument-cone-review-delta-20261010/PROVENANCE.json')},'external_sources':[{'url':'https://www.cs.cmu.edu/~odonnell/papers/Analysis-of-Boolean-Functions-by-Ryan-ODonnell.pdf','inspected':'Section 1.3 Theorem 1.5 and Fact 1.6 through web; no downloaded hash claim.'},{'url':'https://arxiv.org/pdf/1312.0022','inspected':'Arbitrary-field convention, Definition 2.6 and Proposition 2.11 through web; no downloaded hash claim.'}]})
print(json.dumps({'status':'PASS','author_groups':reproduced['groups'],'dependency_drift_recorded':True,'frozen_author_unchanged':True},indent=2))
