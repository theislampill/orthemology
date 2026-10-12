#!/usr/bin/env python3
"""Verify packet identities and reproduce its bounded mathematical check.

Successful verification is not acceptance of the normative or metaphysical
premises, source attribution, or any actual-world conclusion.
"""
from pathlib import Path
import hashlib,json,subprocess,sys
P=Path(__file__).resolve().parent
M=json.loads((P/'MANIFEST.json').read_text())
expected={x['path'] for x in M['files']}
actual={str(x.relative_to(P)) for x in P.rglob('*') if x.is_file()}
assert actual==expected|{'MANIFEST.json','MANIFEST.sha256'}, (actual,expected)
def hashes():
 for x in M['files']:
  b=(P/x['path']).read_bytes()
  assert len(b)==x['bytes'],x['path']
  assert hashlib.sha256(b).hexdigest()==x['sha256'],x['path']
hashes()
for line in (P/'MANIFEST.sha256').read_text().splitlines():
 digest,name=line.split('  ',1)
 assert hashlib.sha256((P/name).read_bytes()).hexdigest()==digest,name
before=(P/'PROFILE_MODEL_CHECK.json').read_bytes()
subprocess.run([sys.executable,str(P/'check_profile_models.py')],check=True,stdout=subprocess.DEVNULL)
assert (P/'PROFILE_MODEL_CHECK.json').read_bytes()==before
hashes()
result=json.loads(before)
assert result['totals']['nonempty_profile_sets']==65808
assert result['totals']['actual_profile_checks']==525348
assert result['totals']['violations']==0
assert result['script_sha256']==hashlib.sha256((P/'check_profile_models.py').read_bytes()).hexdigest()
main=(P/'SOURCE_INTEGRITY_WARRANT.md').read_text()
paras=main.split('## Primary-text control\n')[1].split('\n## ')[0].strip().split('\n\n')
sm=json.loads((P/'SOURCE_MAP.json').read_text())
inc=json.loads((P/'INCREMENT_LEDGER.json').read_text())
wording=json.loads((P/'SOURCE_WORDING_LEDGER.json').read_text())
counts={
 'S1':sum(len(t.split()) for t in [paras[0],sm['source_to_claim_map'][0]['claim'],sm['source_to_claim_map'][1]['claim'],inc['increments'][0]['result']]),
 'S2':sum(len(t.split()) for t in [paras[1],sm['source_to_claim_map'][2]['claim']])}
for src in wording['sources']:
 assert src['source_derived_word_count']==counts[src['source_id']]
 assert src['direct_quotation_words']==0
assert counts['S1']<=200
print(json.dumps({'identity_check':'pass','finite_check':'pass',
 'profile_sets':65808,'actual_profile_assignments':525348,
 'conditional_violations':0,'source_exposition_words':counts,
 'epistemic_limit':'No source-nature, normative, metaphysical possibility or recipient-warrant conclusion follows from packet verification'},indent=2))
