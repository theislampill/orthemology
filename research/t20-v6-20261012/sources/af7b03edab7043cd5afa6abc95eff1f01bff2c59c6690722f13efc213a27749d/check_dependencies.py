#!/usr/bin/env python3
"""Verify exact predecessor ZIP identities and declared member digests without extracting."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
p=argparse.ArgumentParser();p.add_argument('--archive',action='append',required=True,help='Repeat for all eleven authoritative prior ZIPs; filenames may differ, exact bytes decide.')
a=p.parse_args();archives={sha(Path(x)):Path(x) for x in a.archive}
prior=json.loads((ROOT/'COMPONENT_AND_PRIOR_IDENTITIES.json').read_text())['prior_checkpoints'];assert len(archives)==len(prior)==11
for r in prior:
 assert r['sha256'] in archives,r['path'];assert archives[r['sha256']].stat().st_size==r['bytes']
b=json.loads((ROOT/'PACKING/REVIEW_AND_DEPENDENCY_BINDINGS.json').read_text());checks=[]
for r in b['external_predecessor_bindings']:
 archive=archives[r['predecessor_archive_sha256']]
 with zipfile.ZipFile(archive) as z:
  assert z.namelist().count(r['archive_member'])==1
  rel=PurePosixPath(r['archive_member']);assert not rel.is_absolute() and '..' not in rel.parts
  data=z.read(r['archive_member'])
 assert len(data)==r['bytes'] and hashlib.sha256(data).hexdigest()==r['sha256'],r['path']
 checks.append({'path':r['path'],'sha256':r['sha256'],'archive_sha256':r['predecessor_archive_sha256'],'archive_member':r['archive_member'],'status':'PASS'})
for h,p in archives.items():assert sha(p)==h
print(json.dumps({'status':'PASS','prior_archives_checked':len(prior),'external_members_checked':len(checks),'member_checks':checks,'extracted_or_executed_members':0,'scope':'Read-only exact dependency identities, not historical science/source-body replay.'},indent=2))
