"""Omission-aware integrity only; no proof, source-content, or novelty certification."""
from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parent

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def require(c,m):
    if not c:raise RuntimeError(m)
def verify():
    manifest=json.loads((ROOT/'DELIVERY_MANIFEST.json').read_text())
    expected={x['path']:x for x in manifest['files']}
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p.name!='DELIVERY_MANIFEST.json'}
    require(actual==set(expected),'Delivery file set mismatch')
    for rel,x in expected.items():
        p=ROOT/rel
        require(p.stat().st_size==x['bytes'] and digest(p)==x['sha256'],'Delivery hash/size mismatch: '+rel)
    preserved=json.loads((ROOT/'PRESERVATION_MAP.json').read_text())['included']
    omitted=json.loads((ROOT/'OMISSION_LEDGER.json').read_text())['files']
    om={x['path']:x for x in omitted}
    require(len(om)==len(omitted),'Duplicate omission')
    for x in preserved:
        p=ROOT/'payload'/x['path']
        require(p.stat().st_size==x['bytes'] and digest(p)==x['sha256'],'Preservation mismatch: '+x['path'])
    for rel,x in om.items():
        require(not (ROOT/'payload'/rel).exists(),'Omitted content unexpectedly included: '+rel)
        require(x['bytes']>0 and len(x['sha256'])==64 and x['source_url'].startswith('https://'),'Invalid omission record')
    verified=0; acknowledged=0
    for n in ['reference-bregman-classification-20261011','reference-bregman-independent-review-20261011','reference-geometry-root-controls-20261011']:
        for rel,sha in json.loads((ROOT/'payload'/n/'MANIFEST.json').read_text()).items():
            key=n+'/'+rel;p=ROOT/'payload'/key
            if p.is_file():require(digest(p)==sha,'Original manifest mismatch: '+key);verified+=1
            else:require(key in om and om[key]['sha256']==sha,'Unexplained original manifest absence: '+key);acknowledged+=1
    C=ROOT/'payload'/'cumulative-source-transmission-20261011'
    for x in json.loads((C/'MANIFEST.json').read_text())['shareable_files']:
        p=ROOT/'payload'/x['path'];require(digest(p)==x['sha256'] and p.stat().st_size==x['bytes'],'Supplement manifest mismatch');verified+=1
    for line in (C/'SHA256SUMS').read_text().splitlines():
        sha,rel=line.split(maxsplit=1); p=ROOT/'payload'/rel
        if not p.exists():p=C/rel
        require(p.is_file() and digest(p)==sha,'Supplement SHA256SUMS mismatch: '+rel)
    R=ROOT/'payload'/'reference-bregman-independent-review-20261011'
    A=ROOT/'payload'/'reference-bregman-classification-20261011'
    freeze=json.loads((R/'REVIEW_FREEZE.json').read_text());bind=json.loads((R/'REVIEW_BINDINGS.json').read_text())
    require(freeze['verdict']=='PASS' and not freeze['outstanding_findings'],'Review freeze is not clean PASS')
    require(digest(A/'RESULT.md')==freeze['author_result_sha256'],'Freeze author binding mismatch')
    require(digest(R/'MANIFEST.json')==freeze['review_manifest_sha256'],'Freeze review binding mismatch')
    require(digest(A/'MANIFEST.json')==bind['author_manifest_sha256'],'Author manifest binding mismatch')
    require(bind['author_bound_files']==json.loads((A/'MANIFEST.json').read_text()),'Review file bindings mismatch')
    G=ROOT/'payload'/'reference-gradient-descent-classification-20261011'
    for x in json.loads((G/'MANIFEST.json').read_text())['files']:
        p=ROOT/'payload'/x['path']
        require(digest(p)==x['sha256'] and p.stat().st_size==x['bytes'],'Gradient manifest mismatch')
        verified+=1
    sha='097e12106db027914a1a05795c8d4dde647e9c73e52882562eef5f546f6d7c18'
    require(digest(G/'RESULT.md')==sha,'Final gradient report binding mismatch')
    review=(ROOT/'payload'/'reference-gradient-descent-review-20261011'/'REVIEW.md').read_text()
    require(sha in review and 'Verdict: PASS' in review,'Final gradient review binding missing')
    return {'status':'PASS','class':'integrity / byte preservation only','delivery_files_verified':len(expected),'preserved_original_files':len(preserved),'omitted_source_files':len(om),'original_manifest_entries_rehashed':verified,'original_manifest_omissions_acknowledged_not_rehashed':acknowledged,'review_freeze':'PASS, bound to preserved author result and review manifest','limitations':'Omitted sources and inherited dependencies are not re-read/revalidated by this package; hashes do not establish mathematical truth or source attribution.'}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
