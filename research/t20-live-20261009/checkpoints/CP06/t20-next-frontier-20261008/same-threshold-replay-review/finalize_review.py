#!/usr/bin/env python3
"""Bind the completed review without writing any author or predecessor file."""
from pathlib import Path
from hashlib import sha256
from datetime import datetime,timezone
import json
root=Path(__file__).resolve().parent
author=root.parent/'same-threshold-replay'
def digest(p): return sha256(p.read_bytes()).hexdigest()
def record(p,base=root): return {'path':str(p.relative_to(base)),'sha256':digest(p),'bytes':p.stat().st_size}
now=datetime.now(timezone.utc).isoformat()
ev=json.loads((root/'evidence_verification.json').read_text())
assert ev['status']=='PASS'
author_manifest={'path':'../same-threshold-replay/MANIFEST.json','sha256':digest(author/'MANIFEST.json'),'bytes':(author/'MANIFEST.json').stat().st_size,'reading_scope':'Full manifest and all ten listed author payloads read.'}
inputs=[]
for x in ev['source_inputs']:
    clean=str((root.parent/x['path']).resolve().relative_to(root.parent))
    scope='Only initial 100 lines read during this review.' if clean=='grouped-calibration-invariants/RESULT.md' else 'Full text read during this review.'
    inputs.append({**x,'path':'../'+clean,'reading_scope':scope})
source={'created_utc':now,'author_manifest':author_manifest,'author_payloads':ev['author_payloads'],'source_inputs':inputs,'predecessor_manifest_verification':ev['predecessor_manifests'],'reading_limit':'Predecessor payload lists hash-verified; no claim every ancillary payload was substantively reread. No predecessor scripts rerun. No new external sources or papers read.','preinspection_record':record(root/'preinspection_manifest.json'),'independent_derivation_before_author_inspection':True,'author_files_modified':False,'predecessor_files_modified':False}
(root/'SOURCE_BINDINGS.json').write_text(json.dumps(source,indent=2)+'\n')
claims=[
'All-command fresh Q and same-threshold two-face J identify fixed finite count, shared coordinate calibrations, and every within-route copula.',
'No differentiability or absolute continuity of the unknown copulas is required.',
'Boundary handling is valid and avoids logs or cancellation of zero factors.',
'Fixed finite grids cannot certify arbitrary global within-route copula factorization in the unrestricted class.',
'The exact t=3/4 count-alias control preserves the full stated held three-bit transcript.',
'Fresh thresholds, held inventory, held thresholds at distinct commands, and identical-command replay have the correctly distinguished observational consequences.',
'Attribution, source-reading limits, and original-source/physical/psychological boundaries are explicitly preserved.']
evidence_names=['independent_derivation.md','verify_controls.py','exact_controls.json','preinspection_manifest.json','REVIEW.md','SOURCE_BINDINGS.json','verify_evidence.py','evidence_verification.json','replay/exact_controls.py','replay/results/exact_controls.json','replay/results/stdout.log']
receipt={'issued_utc':now,'verdict':'PASS_WITHIN_DECLARED_PROBABILITY_AND_OBSERVATION_MODEL','reviewed_author_manifest':author_manifest,'reviewed_author_payload_count':10,'reviewed_author_payloads':ev['author_payloads'],'scoped_claims':claims,'findings':{'mathematical_blockers':[],'boundary_blockers':[],'source_scope_blockers':[],'required_changes':[]},'evidence':[record(root/x) for x in evidence_names],'author_replay':ev['author_replay'],'provenance':{'source_inputs_verified':6,'predecessor_manifests_verified':3,'predecessor_payload_entries_verified':27,'author_and_predecessor_recheck':'PASS'},'exclusions':['Physical replay availability or control','Psychological manipulability','Metaphysical original-source independence','Finite-sample certification','Universal finite-count impossibility','Review of the separate finite-panel-replay certificate','New copula discovery or field-wide priority','Integration','Owner acceptance','T20 closure'],'author_and_predecessor_files_modified':False,'integration_authority':False,'closure_authority':False}
(root/'REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
payloads=[record(p) for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST.json']
manifest={'created_utc':now,'status':'FROZEN_SCOPED_INDEPENDENT_REVIEW','reviewed_author_manifest_sha256':author_manifest['sha256'],'scope':'Mathematical and exact-control review only; no integration or T20 closure.','files':payloads}
(root/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
for x in payloads:
    assert digest(root/x['path'])==x['sha256'] and (root/x['path']).stat().st_size==x['bytes']
assert digest(author/'MANIFEST.json')=='f58c75e855e51be1bf4818b2b4ea6a91b1b5e685cbd45cfe304e9c3627fcbf53'
for x in json.loads((author/'MANIFEST.json').read_text())['files']:
    assert digest(author/x['path'])==x['sha256'] and (author/x['path']).stat().st_size==x['bytes']
print(json.dumps({'status':'PASS','review_payloads':len(payloads),'review_manifest_sha256':digest(root/'MANIFEST.json'),'review_receipt_sha256':digest(root/'REVIEW_RECEIPT.json'),'review_report_sha256':digest(root/'REVIEW.md'),'source_bindings_sha256':digest(root/'SOURCE_BINDINGS.json'),'author_manifest_sha256':digest(author/'MANIFEST.json')},indent=2))
