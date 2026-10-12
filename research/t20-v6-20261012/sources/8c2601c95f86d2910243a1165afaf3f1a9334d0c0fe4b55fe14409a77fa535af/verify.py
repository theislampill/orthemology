#!/usr/bin/env python3
"""Validate the static foundational register and its existing byte homes.

Run from the original workspace root:
  python t20-consolidation-20261011/foundations/verify.py

Or pass the workspace root with --root. No network, source mutation, mathematical
replay, historical authentication or philosophical validation is performed.
"""
from pathlib import Path
import argparse, hashlib, json, re
parser=argparse.ArgumentParser()
parser.add_argument('--root',type=Path,default=Path.cwd())
a=parser.parse_args();root=a.root.resolve();base=Path(__file__).resolve().parent
reg=json.loads((base/'FOUNDATIONAL_CLAIMS.json').read_text())
ledger=json.loads((base/'SOURCES_AND_READING.json').read_text())
ids=[x['id'] for x in reg['claims']]
assert len(ids)==len(set(ids))==reg['claim_count']
allowed=set(reg['dependency_types']);sources={x['source_id']:x for x in ledger['sources']}
assert len(sources)==ledger['source_count']
for source in sources.values():
 p=root/source['canonical_byte_home']
 assert p.is_file(),f'Missing archival source dependency: {p}'
 assert hashlib.sha256(p.read_bytes()).hexdigest()==source['sha256'],f'Changed source: {p}'
for claim in reg['claims']:
 for d in claim['dependencies']:
  assert d['type'] in allowed
  assert d['target'] in ids or d['target'] in reg['external_claim_references'],d
 for source in claim['supporting_sources']:
  assert source['source_id'] in sources
  assert source['sha256']==sources[source['source_id']]['sha256']
refs=set(re.findall(r'FND-\d{3}',(base/'FOUNDATIONAL_SYNTHESIS.md').read_text()))
assert refs.issubset(ids),refs-set(ids)
print(json.dumps({'result':'PASS','claims':len(ids),'sources':len(sources),'source_hashes_verified':True,'fresh_proof_execution':False,'semantic_or_historical_authentication':False},indent=2))
