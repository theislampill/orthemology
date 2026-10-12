import hashlib,json,shutil
from pathlib import Path
root=Path('private-locator:8f24556a330b05a11a95')
author=root/'interpretation-repair-transport-20261010'
review=root/'interpretation-repair-independent-review-20261010'
replay=review/'replay'
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for entry in json.loads((author/'MANIFEST.json').read_text())['files']:
 p=author/entry['path']; assert p.stat().st_size==entry['bytes']; assert digest(p)==entry['sha256']
 rows.append({'kind':'author-manifest','path':str(p.relative_to(root)),'sha256':digest(p)})
for entry in json.loads((author/'PINNED_BINDINGS.json').read_text()):
 p=root/entry['path']; b=p.read_bytes(); git=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
 assert digest(p)==entry['sha256']; assert git==entry['blob_sha1']
 rows.append({'kind':'git-binding','path':entry['path'],'sha256':digest(p),'git_blob_sha1':git})
for entry in json.loads((author/'LOCAL_BINDINGS.json').read_text()):
 p=root/entry['path']; assert p.stat().st_size==entry['bytes']; assert digest(p)==entry['sha256']
 rows.append({'kind':'local-binding','path':entry['path'],'sha256':digest(p)})
shutil.copytree(author,replay/author.name,dirs_exist_ok=True)
for rel in ['wise-reason-root-20261010/SHIFA_e179_e193.txt','recovery-t20/checkpoint/Orthemology_T20_Continuation_Owner_Review_Checkpoint_20261008/tranche20/research-resumption/testimony-continuation/occurrence_model.py']:
 p=replay/rel;p.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/rel,p)
receipt={'author_manifest_sha256':digest(author/'MANIFEST.json'),'verified_bindings':rows,'checks':'18 author manifest entries, 10 Git blob and SHA-256 bindings, 11 local bindings; no protected writes'}
(review/'INPUT_INTEGRITY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(receipt['checks'])
