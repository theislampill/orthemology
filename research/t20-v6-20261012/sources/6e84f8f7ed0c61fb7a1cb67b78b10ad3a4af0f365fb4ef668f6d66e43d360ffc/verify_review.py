#!/usr/bin/env python3
"""Replay a finite, digest-bound mathematical review without mutating inputs."""
from pathlib import Path
import hashlib,json,subprocess,sys
BASE=Path(__file__).resolve().parent
ROOT=BASE.parent

def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()

manifest=json.loads((BASE/'REVIEW_MANIFEST.json').read_text())
for x in manifest['files']:
 p=BASE/x['path']
 assert p.stat().st_size==x['bytes'],('review size mismatch',p)
 assert digest(p)==x['sha256'],('review digest mismatch',p)
print('PASS reviewer artifact manifest')
receipt=json.loads((BASE/'REVIEW_RECEIPT.json').read_text())
for x in receipt['reviewed_inputs']:
 p=ROOT/x['path']
 assert digest(p)==x['sha256'],('input digest mismatch',p)
print('PASS all finite reviewed input bindings')
assert digest(BASE/'REVIEW.md')==receipt['review_report_sha256']
print('PASS review report receipt binding')
all_sources=[]
for folder in ['information-geometry-transport-20261009','noetic-gradient-transport-20261009']:
 d=ROOT/folder;m=json.loads((d/'MANIFEST.json').read_text());f=m['files']
 if isinstance(f,dict):
  for name,sha in f.items(): assert digest(d/name)==sha,(folder,name)
 else:
  for x in f:
   p=d/x['path'];assert digest(p)==x['sha256'] and p.stat().st_size==x['bytes'],(folder,x['path'])
 for x in json.loads((d/'SOURCE_LEDGER.json').read_text())['local_sources']:
  data=(ROOT/x['path']).read_bytes();assert hashlib.sha256(data).hexdigest()==x['sha256'],x['path']
  if x.get('git_blob_sha'):
   blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest();assert blob==x['git_blob_sha'],x['path']
  all_sources.append(x)
print('PASS both author manifests and source byte identities')
remote=json.loads((BASE/'REMOTE_SOURCE_BINDINGS.json').read_text())['records']
for r in remote:
 matches=[x for x in all_sources if x.get('url')==r['url']]
 assert matches and all(x.get('git_blob_sha')==r['returned_git_blob'] for x in matches),r['url']
print('PASS retained direct remote-pin observations match local source blobs')
for script,expected in [
 ('geometry-transport-independent-review-20261009/check_independent.py','independent-output.txt'),
 ('noetic-gradient-transport-20261009/verify.py','noetic-review-run.txt'),
 ('information-geometry-transport-20261009/verify.py','information-review-run.txt')]:
 p=subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,capture_output=True,text=True)
 assert p.returncode==0,(script,p.returncode,p.stdout,p.stderr)
 assert p.stdout==(BASE/expected).read_text(),('replay output differs',script)
 print('PASS exact replay:',script)
 print(p.stdout.strip().splitlines()[-1])
print('PASS FINITE REVIEW RECEIPT: ordinary proofs reviewed; exact controls replayed; no new kernel certification, protected integration, or T20 closure')
