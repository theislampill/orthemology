#!/usr/bin/env python3
"""Verify an extracted package, or extract an archive into an absent directory first."""
from pathlib import Path
import argparse,json,zipfile,sys
from portable_core import sha,validate_files,verify_git_snapshot,extract_zip,safe_path,write_json,order_modules,imports,verify_source_graph,verify_commit_identity

def verify(root):
 root=Path(root).resolve();manifest=root/'MASTER_MANIFEST.json'
 if sha(manifest)!=(root/'MASTER_MANIFEST.sha256').read_text().split()[0]:raise ValueError('Master manifest SHA256 mismatch')
 m=json.loads(manifest.read_text());count=validate_files(root,m)
 expected={r['path'] for r in m['files']}|{'MASTER_MANIFEST.json','MASTER_MANIFEST.sha256'}
 actual={str(p.relative_to(root)) for p in root.rglob('*') if p.is_file()}
 if actual!=expected:raise ValueError('Package file census mismatch: '+repr(sorted(actual^expected)))
 inventory=json.loads((root/'ARCHIVE_INVENTORY.json').read_text())['archives'];archive_rows=[]
 for a in inventory:
  path=root/a['path']
  if sha(path)!=a['sha256'] or path.stat().st_size!=a['bytes']:raise ValueError('Archive identity mismatch '+a['path'])
  if path.suffix=='.zip':
   with zipfile.ZipFile(path) as z:
    if z.testzip() is not None:raise ValueError('Archive CRC failure '+a['path'])
    ns=z.namelist()
    if len(ns)!=len(set(ns)):raise ValueError('Duplicate archive member '+a['path'])
    for n in ns:safe_path(root/'not-extracted',n.rstrip('/'))
   archive_rows.append({'path':a['path'],'sha256':a['sha256'],'members':len(ns),'status':'PASS'})
 identity=json.loads((root/'canonical/IDENTITY.json').read_text());can=root/'canonical/Orthemology_Canonical_Source_03e2604d.zip'
 if sha(can)!=identity['archive_sha256']:raise ValueError('Canonical snapshot archive hash mismatch')
 blobs=verify_git_snapshot(can,identity)
 commit_object=safe_path(root,identity['commit_object_file'])
 if sha(commit_object)!=identity['commit_object_sha256']:raise ValueError('Canonical commit object SHA256 mismatch')
 verify_commit_identity(commit_object.read_bytes(),identity['commit'],identity['tree'])
 suites=json.loads((root/'SUITES.json').read_text())['suites'];source_rows=[]
 graph_count=verify_source_graph(root,suites,json.loads((root/'DEPENDENCY_GRAPH.json').read_text())['custom_modules'])
 owner_rows=json.loads((root/'SOURCE_OWNERS.json').read_text())['files'];validate_files(root,{'files':owner_rows})
 for s in suites:
  sr=root/s['source_root'];texts={m:(sr/Path(*m.split('.')).with_suffix('.lean')).read_text() for m in s['module_order']}
  if order_modules(texts,s['module_order'])!=s['module_order']:raise ValueError('Source topology mismatch '+s['id'])
  source_rows.append({'suite':s['id'],'custom_source_modules':len(texts),'target_counts_by_claim_set':s['target_counts_per_claim_set'],'status':'DEPENDENCY_CLOSURE_PRESENT'})
 return {'status':'INTEGRITY_AND_CUSTOM_SOURCE_CLOSURE_PASS','manifest_sha256':sha(manifest),'files':count,'source_graph_bindings_verified':graph_count,'archives':archive_rows,'canonical_blobs_verified':blobs,'canonical_tree':identity['tree'],'canonical_commit_object_verified':identity['commit'],'suites':source_rows,'scope':'Integrity and source dependency completeness only; compilation/proofs require separate replay receipt'}

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--archive',type=Path);ap.add_argument('--extract-to',type=Path);ap.add_argument('--receipt',type=Path)
 a=ap.parse_args()
 if bool(a.archive)!=bool(a.extract_to):ap.error('--archive and --extract-to must be used together')
 root=extract_zip(a.archive,a.extract_to) if a.archive else a.root
 r=verify(root)
 if a.receipt:
  if a.receipt.resolve().is_relative_to(root.resolve()):ap.error('Receipt must be outside the immutable package')
  write_json(a.receipt,r)
 print(json.dumps(r,indent=2))
if __name__=='__main__':main()
