#!/usr/bin/env python3
"""Seal the existing P03 research payload. No research or repository code executes."""
from pathlib import Path
import datetime,hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
NAME='Orthemology_P03_Engine_Refinement_Checkpoint_attempt-0002'
CONTROLS=['MANIFEST.json','MANIFEST.json.sha256','RECEIPT.json','RECEIPT.json.sha256']
def sha(b):return hashlib.sha256(b).hexdigest()
def binding(rel):
    b=(ROOT/rel).read_bytes();return {'path':rel,'bytes':len(b),'sha256':sha(b)}
def write(rel,obj):
    b=(json.dumps(obj,indent=2,ensure_ascii=False)+'\n').encode('utf-8');(ROOT/rel).write_bytes(b);return b

def main():
    for p in ROOT.rglob('*'):
        if p.is_symlink() or p.suffix=='.pyc' or p.name=='__pycache__':raise ValueError('Unexpected generated/link member '+str(p))
    paths=sorted(str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and str(p.relative_to(ROOT)) not in CONTROLS)
    required=['README.md','TERMINAL_STATUSES.json','P02_P03_DEPENDENCY_MAP.json','research/EXHAUSTION_MATRIX.json','research/SELF_REVIEW.json','evidence/EVIDENCE_SUMMARY.json','handoff/CODEX_IMPLEMENTATION_HANDOFF.md','tools/verify_checkpoint.py']
    if not set(required)<=set(paths):raise ValueError('Required payload missing')
    manifest={'schema':'orthemology-p03-attempt2-payload-v1','scope':'SEPARATE_RESEARCH_PROPOSAL_NO_CANONICAL_EFFECT','control_exclusions':CONTROLS,'files':[binding(p) for p in paths]}
    mb=write('MANIFEST.json',manifest);ms=(sha(mb)+'  MANIFEST.json\n').encode();(ROOT/'MANIFEST.json.sha256').write_bytes(ms)
    statuses=json.loads((ROOT/'TERMINAL_STATUSES.json').read_text())
    predecessors=[]
    for kind,path in [('P03','inputs/Orthemology_P03_Engine_Refinement_Checkpoint_attempt-0001.zip'),('P02','inputs/Orthemology_P02_Measure_Research_Checkpoint_20260922(2).zip')]:predecessors.append(dict(binding(path),kind=kind))
    report_paths=['research/U03_GENERAL_REFINEMENT.md','research/U04_OPERATIONAL_REFINEMENT.md','research/P02_OPERATIONAL_INSTANTIATION.md','research/Q1F_LAYERED_VCT.md','research/EXHAUSTION_MATRIX.json','research/NEW_COUNTERMODELS.json','handoff/CODEX_IMPLEMENTATION_HANDOFF.md']
    receipt={'schema':'orthemology-p03-attempt2-research-receipt-v1','checkpoint_id':NAME,'sealed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'status':'TERMINAL_SCOPED_RESEARCH_WITH_EXACT_FORMAL_EXECUTION_BLOCK','statuses':statuses['statuses'],'aliases':{'CV-O':'U04'},
      'canonical_obligation_statuses_changed':False,'canonical_mutation':False,'kernel_credit':False,'external_review_credit':False,
      'preserved_integration':{'main':'03e2604dfcef278b01c60d19b05370fcec4194b6','tree':'3d06e80277ce39286c94307e0f14b215bc94ed83','PR_merged':28,'integration_cells_remaining':0,'fresh_remote_full_tree_requalification':False},
      'predecessors':predecessors,'P02_actual_statuses':statuses['P02_actual_statuses'],
      'P02_reuse':{'map':binding('P02_P03_DEPENDENCY_MAP.json'),'required_ordinary_finite_engine_prerequisites':'DISCHARGED_AT_EXPLICIT_MODEL_HYPOTHESES','new_P02_kernel_results_consumed':0,'unread_future_P02_dependency':False,'detached_P02_outer_seal_supplied':False},
      'statement_reports':[binding(p) for p in report_paths],'evidence_summary':binding('evidence/EVIDENCE_SUMMARY.json'),
      'new_proposal_modules':[binding('proposal/safe_frontend.py'),binding('proposal/atomic_engine.py')],
      'new_formal':{'execution_status':'HOST_EXECUTION_BLOCKED','result_status':'UNPROVED','required_pin':'Lean4.19.0 / 6caaee842e94','requested_targets':14,'observed_types':0,'observed_axioms':0,'new_nonempty_olean_artifacts':0,'acquisition_evidence':binding('evidence/TOOLCHAIN_STATUS.json'),'minimal_execution_packet':binding('handoff/P03_Lean419_Execution_Packet.zip')},
      'negative_evidence_boundary':'New countermodels refute overbroad concrete relations/proposals, not accepted abstract theorems. Prior strict-wrapper FAIL and both predecessors remain exact.',
      'other_effects':{'github_write':False,'integration_replay':False,'owner_adoption':False,'publication':False,'historical_recovery_credit':False,'empirical_world_authority':False,'licensing_adjudication':False,'novelty_credit':False},
      'manifest_sha256':sha(mb),'manifest_sidecar_sha256':sha(ms),'payload_files':len(paths),'archive_members':len(paths)+len(CONTROLS),
      'fresh_reopen':{'required':True,'status':'RECORDED_AFTER_SEAL_IN_EXTERNAL_REPORT','tool':'tools/verify_checkpoint.py','scope':'Every member hash, nested predecessor source/evidence/receipt bindings, result-level P02 links, command streams and minimal formal packet; no independent expert review or kernel credit'}}
    rb=write('RECEIPT.json',receipt);(ROOT/'RECEIPT.json.sha256').write_text(sha(rb)+'  RECEIPT.json\n')
    archive=ROOT.parent/(NAME+'.zip')
    all_names=sorted(paths+CONTROLS)
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for name in all_names:
            info=zipfile.ZipInfo(name,(2026,9,22,0,0,0));info.external_attr=0o100644<<16;info.create_system=3
            z.writestr(info,(ROOT/name).read_bytes(),compress_type=zipfile.ZIP_DEFLATED,compresslevel=9)
    data=archive.read_bytes();seal={'schema':'orthemology-p03-attempt2-detached-seal-v1','file':archive.name,'bytes':len(data),'sha256':sha(data),'members':len(all_names),'uncompressed_bytes':sum((ROOT/n).stat().st_size for n in all_names),'manifest_sha256':sha(mb),'receipt_sha256':sha(rb),'scope':'Transport identity; not theorem/implementation/adoption acceptance'}
    (archive.parent/(archive.name+'.sha256')).write_text(seal['sha256']+'  '+archive.name+'\n')
    (archive.parent/(NAME+'.SEAL.json')).write_text(json.dumps(seal,indent=2)+'\n')
    print(json.dumps(seal,indent=2))
if __name__=='__main__':main()
