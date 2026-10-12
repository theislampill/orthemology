from pathlib import Path
import json,hashlib,difflib
R=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def check(c,m):
 if not c:raise RuntimeError(m)
manifest=json.loads((R/'MANIFEST.json').read_text())
for x in manifest:
 p=R/x['path'];check(p.is_file(),'Missing delivered file '+x['path']);check(p.stat().st_size==x['bytes'] and sha(p)==x['sha256'],'Manifest mismatch '+x['path'])
for x in json.loads((R/'PRESERVATION_MAP.json').read_text()):check(sha(R/x['preserved'])==x['sha256'],'Original-copy mismatch '+x['source'])
omit={x['path']:x for x in json.loads((R/'OMISSION_LEDGER.json').read_text())}
for x in json.loads((R/'BOUND_INPUT_STATUS.json').read_text()):
 if x['status']=='included':check(sha(R/x['preserved'])==x['sha256'],'Included binding mismatch '+x['path'])
 elif x['status']=='omitted-explicitly':check(x['path'] in omit and omit[x['path']]['sha256']==x['sha256'],'Omission identity mismatch '+x['path'])
 else:raise RuntimeError('Unknown binding disposition')
p=R/'payload/source-selection-fitness-20261011';rec=json.loads((p/'REVISION_RECEIPT.json').read_text())
check(sha(p/'REPORT.prior-v1.md')==rec['prior_sha256'],'Prior report mismatch')
check(sha(p/'REPORT.md')==rec['revised_sha256'],'Current report mismatch')
check(sha(p/'REVISION.diff')==rec['diff_sha256'],'Recorded diff mismatch')
diff=''.join(difflib.unified_diff((p/'REPORT.prior-v1.md').read_text().splitlines(True),(p/'REPORT.md').read_text().splitlines(True),fromfile='REPORT.prior-v1.md',tofile='REPORT.md'))
check(diff==(p/'REVISION.diff').read_text(),'Diff does not reproduce exact revision')
print(json.dumps({'status':'PASS','manifest_files':len(manifest),'original_files':len(json.loads((R/'PRESERVATION_MAP.json').read_text())),'explicit_omissions':len(omit),'exact_revision_diff':'PASS','source_body_replay':False,'scope':'Preservation integrity only; no source-reading or historical-authentication credit'},indent=2))
