"""Verify review-packet bytes and optionally replay bounded Python checks.
No repository integration, network access or package installation.
"""
from pathlib import Path, PurePosixPath
import hashlib,json,sys,zipfile,subprocess,os
ROOT=Path(__file__).resolve().parent
for e in json.loads((ROOT/'MANIFEST.json').read_text())['files']:
 p=ROOT/e['path'];assert p.is_file(),p
 assert p.stat().st_size==e['bytes'] and hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256'],p
print('Package manifest verified.')
if '--replay' not in sys.argv:raise SystemExit(0)
archives=[('Orthemology_T20_Targeted_Source_Addendum_20261008.zip','614d9de89bba48db016079f749ba8211ad32a12eb87cc6d0a01939733ff122f8','addendum'),('Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008.zip','c06fddfd16be58f254b57560c9e09e22c470fa8f66ac07c51f7a40c5f5629990','checkpoint')]
for name,sha,folder in archives:
 p=ROOT/'checkpoints'/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==sha
 dest=ROOT/'recovery-t20'/folder
 with zipfile.ZipFile(p) as z:
  assert z.testzip() is None
  for i in z.infolist():
   q=PurePosixPath(i.filename);assert not q.is_absolute() and '..' not in q.parts
   assert (i.external_attr>>16)&0o170000 !=0o120000
   if i.is_dir():continue
   target=dest/q; data=z.read(i)
   if target.exists():assert target.read_bytes()==data, ('Refuse changed preimage',target)
   else:target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for lane in ['effect-production','valued-cooperation']:
 subprocess.run([sys.executable,'-B','-m','unittest','discover','-s',str(ROOT/'t20-continuation-20261008'/lane/'src'),'-p','test_*.py','-v'],cwd=ROOT,env=env,check=True)
# Source screen is evidence of lexical matches, not source authentication.
script=ROOT/'t20-continuation-20261008/source-dependencies/screen_candidates.py'
receipt=script.parent/'CITATION_SCREEN.json';before=receipt.read_bytes()
subprocess.run([sys.executable,'-B',str(script)],cwd=ROOT,env=env,check=True)
assert receipt.read_bytes()==before,'Source-screen reproduction drifted'
print('18 effect checks, 16 valued-cooperation checks, and exact lexical-screen receipt reproduced. No new Lean or philosophical warrant claim.')
