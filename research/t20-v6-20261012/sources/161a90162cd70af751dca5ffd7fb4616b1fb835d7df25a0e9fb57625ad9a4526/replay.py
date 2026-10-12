from pathlib import Path
import hashlib,json,tempfile,shutil,subprocess,sys
R=Path(__file__).resolve().parent;P=R/'payload';A='positive-high-order-correction-20261011';V='high-order-law-independent-review-20261011'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def require(c,m):
 if not c:raise RuntimeError(m)
def verify():
 for x in json.loads((R/'MANIFEST.json').read_text()):
  p=R/x['path'];require(p.is_file(),'Missing '+x['path']);require(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'Manifest mismatch '+x['path'])
 for x in json.loads((R/'PRESERVATION_MAP.json').read_text()):require(sha(R/x['preserved'])==x['sha256'],'Original identity mismatch '+x['source'])
 for path,h in json.loads((P/A/'INPUT_BINDINGS.json').read_text())['sha256'].items():require(sha(P/path)==h,'Inherited owner binding mismatch '+path)
 for path,h in json.loads((P/A/'AUTHOR_FREEZE.json').read_text())['sha256'].items():require(sha(P/A/path)==h,'Author freeze mismatch '+path)
 review=json.loads((P/V/'REVIEW_RECEIPT.json').read_text())
 for group in ['source_sha256','review_sha256']:
  for path,h in review[group].items():require(sha(P/path)==h,'Review binding mismatch '+path)
 require(sha(P/'infinite-initial-fisher-length-20261011/RESULT.md')=='e8743a543021cd86d205c7b757c038f2acaeb80e0ecc117f1ebf1cef6d6493ec','Fisher report binding mismatch')
 require(sha(P/'initial-fisher-length-independent-review-20261011/REVIEW.md')=='35efa98e6673b44566fb1c6a26dffc4c6a699ec7a59356f60bac70414cb3a6fb','Fisher review binding mismatch')
def replay():
 import sympy,mpmath
 verify();runs=[]
 with tempfile.TemporaryDirectory(prefix='high-order-law-') as tmp:
  work=Path(tmp)/'payload';shutil.copytree(P,work)
  for opt in [False,True]:
   for folder,script,output in [(A,'check.py','CHECKS.json'),(V,'check_independent.py','INDEPENDENT_CHECKS.json')]:
    p=subprocess.run([sys.executable]+(['-O'] if opt else [])+[str(work/folder/script)],cwd=work,text=True,capture_output=True)
    require(p.returncode==0,'Control replay failed '+p.stdout+p.stderr);require(sha(work/folder/output)==sha(P/folder/output),'Exact result mismatch '+folder)
    d=json.loads((work/folder/output).read_text())
    if folder==A:require(d['control_count']==419 and d['numerical_control_count']==4,'Author count mismatch')
    else:require(d['exact_symbolic_controls']==1100 and d['numeric_telescoping_controls']==60,'Review count mismatch')
    runs.append({'packet':folder,'optimized':opt,'status':'PASS','result_sha256':sha(work/folder/output),'stdout':p.stdout})
 verify();print(json.dumps({'status':'PASS','python':sys.version,'sympy':sympy.__version__,'mpmath':mpmath.__version__,'runs':runs,'author_exact_symbolic':415,'author_numerical':4,'review_exact_symbolic':1100,'review_numerical':60,'fisher_length_proof':'Analytical proof and independent review only; no numerical experiment or finite-control replay claimed.','formal_kernel_claim':False,'R3_88_tests_replayed':False},indent=2))
if __name__=='__main__':
 if '--verify-only' in sys.argv:verify();print('PASS: delivery identities, owner snapshots, author freeze and both final reviews')
 else:replay()
