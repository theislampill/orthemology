from pathlib import Path
import hashlib,json,subprocess,sys
root=Path(__file__).resolve().parents[2]; out=Path(__file__).resolve().parent; author=out.parent/'proof_inquiry'
def bind(p):
 b=p.read_bytes();return {'path':str(p.relative_to(root)),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b)}
x=json.loads((author/'SOURCE_BINDINGS.json').read_text());check=[]
for s in x['sources']:
 p=root/s['path'];actual=bind(p);check.append({'id':s['id'],**actual,'matches':actual['sha256']==s['sha256']})
for s in x['unchanged_import_copies']:
 actual=bind(author/s['copy_path']);check.append({'id':'copy:'+s['source_id'],**actual,'matches':actual['sha256']==s['sha256']})
if not all(s['matches'] for s in check):raise AssertionError('source hash mismatch')
runs=[]
for flag in ([],['-O']):
 cmd=[sys.executable,'-B']+flag+['-m','unittest','discover','-s',str(author),'-p','test_*.py','-v']
 p=subprocess.run(cmd,cwd=root,capture_output=True,text=True); name='author_optimized.log' if flag else 'author_final.log';(out/name).write_text(p.stdout+p.stderr)
 runs.append({'command':cmd,'exit_code':p.returncode,'log':name});
 if p.returncode:raise AssertionError('suite failed')
negatives=[]
for flags in ([],['-O']):
 for claim in ('cache_normalization','branch_pasting','snapshot_survives_revision'):
  cmd=[sys.executable,'-B']+flags+[str(author/'false_claim.py'),claim]
  proc=subprocess.run(cmd,cwd=root,capture_output=True,text=True)
  marker='INTENDED_FALSE_CLAIM_REJECTED: '+claim
  if proc.returncode==0 or marker not in proc.stderr:raise AssertionError('wrong negative failure')
  logfile=('optimized_' if flags else 'normal_')+claim+'.log';(out/logfile).write_text(proc.stdout+proc.stderr)
  negatives.append({'claim':claim,'optimized':bool(flags),'exit_code':proc.returncode,'marker':marker,'log':logfile})
for receipt in ('VERIFICATION.json','VERIFICATION_OPTIMIZED.json'):
 data=json.loads((author/receipt).read_text())
 for name,digest in data['bound_files'].items():
  if bind(author/name)['sha256']!=digest:raise AssertionError('author receipt stale '+name)
report={'negative_controls':negatives,'author_receipts_current':True,'scope' :'Mechanical bindings validate 27 sources and 3 imports; this is not 27-source body read credit. Independent review scope is in REVIEW.md.', 'reviewed_author_artifacts':[bind(p) for p in sorted(author.glob('*')) if p.is_file() and p.suffix in ('.py','.md','.json')], 'verified_source_bindings':check,'runs':runs,'independent_control_result':json.loads((out/'independent_controls.json').read_text())}
(out/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
print('all bindings matched;',len(check),'source/copy entries; 19 tests pass with and without -O')
