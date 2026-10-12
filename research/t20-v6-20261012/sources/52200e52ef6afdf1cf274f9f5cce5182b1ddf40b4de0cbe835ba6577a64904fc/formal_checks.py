#!/usr/bin/env python3
"""Formal source/receipt custody only. Does not invoke Lean or rebuild dependencies."""
from pathlib import Path
import argparse,hashlib,json
P=Path;ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=P,required=True);args=ap.parse_args();R=P(__file__).resolve().parent;out=args.output_dir.resolve()
if out==R or R in out.parents:raise SystemExit('Output must be outside bundle.')
out.mkdir(parents=True,exist_ok=True);h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def check(name,value):
 checks.append({'name':name,'passed':bool(value)})
 if not value:raise RuntimeError(name)
A=R/'hase-finite-sidecar-realisation-20261011';V=R/'hase-finite-sidecar-independent-review-20261011'
check('final reviewer receipt pin',h(V/'REVIEW_RECEIPT.json')=='661a26658e27ec170eeb251885aef6c6cbf1c0461ca532630c11224a3c83a323')
f=json.loads((A/'CANDIDATE_FREEZE.json').read_text());check('ten frozen mathematical files',len(f['files'])==10)
for row in f['files']:
 p=A/row['name'];check('exact frozen candidate '+row['name'],p.stat().st_size==row['bytes'] and h(p)==row['sha256']);check('reviewer candidate snapshot '+row['name'],(V/'candidate'/row['name']).read_bytes()==p.read_bytes())
r=json.loads((V/'REVIEW_RECEIPT.json').read_text())
for row in r['files']:
 p=V/row['path'];check('review receipt artifact '+row['path'],p.stat().st_size==row['bytes'] and h(p)==row['sha256'])
check('reviewed candidate identity',h(A/'CANDIDATE_FREEZE.json')==r['candidate_freeze_sha256'])
rev=json.loads((A/'VERIFICATION_REVISION.json').read_text())
for key in ['current_source_boundary','current_author_replay','current_verifier']:
 row=rev[key];check('current metadata revision '+key,h(A/row['path'])==row['sha256'])
check('earlier metadata bytes explicitly not preserved',not rev['earlier_source_boundary']['bytes_preserved'] and not rev['earlier_author_replay']['bytes_preserved']);check('earlier author receipt hash explicitly unavailable',rev['earlier_author_replay']['sha256'] is None)
check('metadata-only revision preserves candidate pin',rev['unchanged_candidate_freeze']['sha256']==h(A/'CANDIDATE_FREEZE.json') and rev['unchanged_candidate_freeze']['files_checked']==10 and rev['unchanged_candidate_freeze']['all_match'])
a=json.loads((A/'validation/AUTHOR_REPLAY.json').read_text());check('recorded author log pin',a['log_sha256']==h(A/'validation/pinned-replay.log'));check('recorded author source boundary',a['manifest_sha256']==h(A/'SOURCE_BOUNDARY.json'))
p=json.loads((V/'REPLAY.json').read_text());check('recorded eight successful fresh module results',len(p['results'])==8 and all(x['exit_code']==0 for x in p['results']));check('recorded trust zero',p['trust']==0);check('recorded dependencies not rebuilt',p['inherited_dependencies_rebuilt'] is False)
for row in p['results']:
 path=(A if row['module'] not in ['IndependentAudit','IndependentBoundaries'] else V)/(row['module']+'.lean');check('recorded fresh module source pin '+row['module'],h(path)==row['source_sha256'])
b=json.loads((A/'SOURCE_BOUNDARY.json').read_text());ob=json.loads((V/'INHERITED_OBJECTS_BEFORE.json').read_text());ai=json.loads((V/'ACTUAL_IMPORTED_OBJECTS.json').read_text())
check('2835 inherited object metadata rows',len(ob['files'])==2835 and len(b['actual_imports'])==2835 and r['inherited_object_pin_count']==2835);check('2841 actual imported object metadata rows',len(ai['files'])==2841 and r['final_imported_object_count']==2841)
check('no compiled objects packaged',not list(R.rglob('*.olean')));check('formal dependency gap explicit',json.loads((R/'FORMAL_DEPENDENCIES.json').read_text())['objects_packaged']==0)
receipt={'status':'PASS_SOURCE_AND_RECEIPT_CUSTODY_ONLY','fresh_kernel_replay_performed':False,'frozen_math_files':10,'recorded_fresh_author_modules':6,'recorded_reviewer_modules':2,'inherited_objects_recorded_not_rebuilt_or_packaged':2835,'historical_metadata_byte_loss_disclosed':True,'checks':checks,'scope':'No Lean process invoked. Source/manifest custody and historical receipt coherence only; exact inherited objects and Lean4.19.0 are external dependencies.'}
(out/'FORMAL_CUSTODY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='checks'},indent=2))
