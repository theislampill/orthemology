from pathlib import Path
import json,hashlib,tempfile,shutil,subprocess,sys
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(c,m):
 if not c:raise RuntimeError(m)
def verify():
 for x in json.loads((R/'MANIFEST.json').read_text()):
  p=R/x['path'];check(p.is_file(),'Missing delivered file '+x['path']);check(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'Manifest mismatch '+x['path'])
 for x in json.loads((R/'PRESERVATION_MAP.json').read_text()):check(sha(R/x['preserved'])==x['sha256'],'Original-copy mismatch '+x['source'])
 omit={x['path']:x for x in json.loads((R/'OMISSION_LEDGER.json').read_text())}
 for x in json.loads((R/'BOUND_INPUT_STATUS.json').read_text()):
  if x['status']=='included':check(sha(R/x['preserved'])==x['sha256'],'Included binding mismatch '+x['path'])
  elif x['status']=='omitted-explicitly':check(x['path'] in omit and omit[x['path']]['sha256']==x['sha256'],'Omission identity mismatch '+x['path'])
  else:raise RuntimeError('Unknown disposition')
 author=R/'payload/coupled-credal-inquiry-transport-20261011'
 for x in json.loads((author/'AUTHOR_MANIFEST.json').read_text())['files']:
  check(sha(author/x['path'])==x['sha256'],'Author manifest mismatch '+x['path'])
def replay():
 verify();results=[]
 with tempfile.TemporaryDirectory(prefix='inquiry-portable-') as tmp:
  work=Path(tmp)/'payload';shutil.copytree(R/'payload',work)
  for folder,script,resultname in [('coupled-credal-inquiry-transport-20261011','run_checks.py','RUN_RECEIPT.json'),('coupled-credal-inquiry-independent-review-20261011','run_review.py','REPLAY_RECEIPT.json')]:
   p=subprocess.run([sys.executable,str(work/folder/script)],cwd=work,capture_output=True,text=True)
   check(p.returncode==0,script+' failed\n'+p.stdout+p.stderr)
   result=json.loads(p.stdout);check(result['status']=='PASS',script+' nonpassing')
   check(sha(work/folder/resultname)==sha(R/'payload'/folder/resultname),'Regenerated receipt mismatch '+resultname)
   results.append({'runner':script,'result':result,'exact_receipt_match':True})
  for optimized in [False,True]:
   script=work/'credal-inquiry-root-controls-20261011/zero_branch_control.py'
   p=subprocess.run([sys.executable]+(['-O'] if optimized else [])+[str(script)],cwd=work,capture_output=True,text=True)
   check(p.returncode==0,'Zero-branch root control failed '+p.stderr)
   expected=R/'payload/credal-inquiry-root-controls-20261011'/('ZERO_OPTIMISED.txt' if optimized else 'ZERO_NORMAL.txt')
   check(p.stdout==expected.read_text(),'Zero-branch replay output mismatch')
   results.append({'runner':'zero_branch_control.py','optimized':optimized,'stdout':p.stdout,'exact_output_match':True})
 verify()
 print(json.dumps({'status':'PASS','python':sys.version,'results':results,'source_body_replay':False,'scope':'Exact computation and archive integrity; no source authentication'},indent=2))
if __name__=='__main__':
 if '--verify-only' in sys.argv:verify();print('PASS: delivery manifest, original identities, explicit binding dispositions and author manifest')
 else:replay()
