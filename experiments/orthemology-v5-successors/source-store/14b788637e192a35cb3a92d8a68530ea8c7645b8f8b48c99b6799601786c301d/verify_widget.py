"""Record newly generated widget assets and lock-bound npm distributions."""
from pathlib import Path
import datetime, hashlib, json
from context import context
A,D,P,T,E=context()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
receipt=json.loads((E/'WIDGET_SOURCE_BUILD.json').read_text())
assert receipt['status']=='PASS' and receipt['exit_code']==0
assert sha(E/'WIDGET_SOURCE_BUILD.log')==receipt['log_sha256']
pw=D/'proofwidgets'; lock=pw/'widget/package-lock.json'
pin=next(r for r in json.loads((E/'proofwidgets_source_inventory.json').read_text()) if r['path']=='widget/package-lock.json')
assert sha(lock)==pin['sha256']
assets=[{'path':f.relative_to(pw).as_posix(),'bytes':f.stat().st_size,'sha256':sha(f)} for f in sorted((pw/'.lake/build/js').glob('*.js'))]
assert len(assets)==19
start=datetime.datetime.fromisoformat(receipt['start_utc']).timestamp();end=datetime.datetime.fromisoformat(receipt['end_utc']).timestamp()
assert all(start<=(pw/r['path']).stat().st_mtime<=end+1 for r in assets)
installed=json.loads((pw/'widget/node_modules/.package-lock.json').read_text())['packages']
pinned=json.loads(lock.read_text())['packages'];rows=[]
for path,row in installed.items():
    assert path in pinned,path
    assert all(row.get(k)==pinned[path].get(k) for k in ['version','integrity','resolved']),path
    rows.append({'path':path,**{k:row[k] for k in ['version','integrity','resolved'] if k in row}})
assert len(rows)==365,len(rows)
assert not list((pw/'widget/node_modules').rglob('*.olean'))
out={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'fresh_source_built_assets':assets,'pinned_package_lock_sha256':sha(lock),'installed_distributions_matching_lock':len(rows),'installed_distributions':rows,'trusted_registry_build_tools_not_source_bootstrapped':True,'no_lean_proof_artifacts_from_npm':True}
(E/'WIDGET_SOURCE_ASSETS.json').write_text(json.dumps(out,indent=2)+'\n')
print('WIDGET_ASSETS_PASS',len(assets),len(rows))
