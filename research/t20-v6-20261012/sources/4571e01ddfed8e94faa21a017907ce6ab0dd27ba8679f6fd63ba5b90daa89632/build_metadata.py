#!/usr/bin/env python3
"""Bind this research packet's already-executed results. No research or repo effects."""
from pathlib import Path
import datetime,hashlib,io,json,zipfile
O=Path(__file__).resolve().parents[1]
def sha(b):return hashlib.sha256(b).hexdigest()
def write(p,d):
    p=O/p;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2)+'\n')
def fileid(p):
    b=(O/p).read_bytes();return {'path':p,'bytes':len(b),'sha256':sha(b)}
P03='inputs/Orthemology_P03_Engine_Refinement_Checkpoint_attempt-0001.zip'
P02='inputs/Orthemology_P02_Measure_Research_Checkpoint_20260922(2).zip'
with zipfile.ZipFile(O/P03) as z:
    oldreceipt=json.loads(z.read('RECEIPT.json'));original=z.read('inputs/Orthemology_Pro_P03_Engine_Refinement.zip')
    with zipfile.ZipFile(io.BytesIO(original)) as n:
        obligations=json.loads(n.read('OBLIGATIONS.json'));inventory=json.loads(n.read('SOURCE_INVENTORY.json'))
        records=[]
        for ob in obligations:
            raw=n.read('source-main/'+ob['source_locator'])
            if ob['source_locator'].endswith('.json'):doc=json.loads(raw);row=next(x for x in doc['items'] if x['id']==ob['id'])
            else:
                import yaml
                row=next(x for x in yaml.safe_load(raw)['queue'] if x['id']==ob['id'])
            if row!=ob['exact_source_record']:raise ValueError('source selector differs '+ob['id'])
            records.append({'id':ob['id'],'attempt1_status':oldreceipt['obligations'][ob['id']],
                'exact_inherited_obligation':ob,'source_selector_verified_equal':True,
                'source_record_file_sha256':sha(raw),'predecessor_zip':fileid(P03)})
        write('inputs/P03_OBLIGATION_CONFIRMATIONS.json',{'canonical_statuses_changed':False,'records':records})
        names=['INDEX.md','OBLIGATIONS.json','CURRENT_CANONICAL_STATE.md','DO_NOT_REOPEN.md','OWNER_ONLY_OR_EXTERNAL_ITEMS.md','INPUTS_AND_BOUNDARIES.md','DEPENDENCY_DAG.json','FORMAL_TOOLCHAIN_STATE.json']
        for name in names:
            p=O/'inputs/governing'/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(n.read(name))
        formal=['source-main/experiments/orthemology-v5/source/lean-toolchain','source-main/experiments/orthemology-v5/formal_project/lakefile.lean','source-main/experiments/orthemology-v5/formal_project/lake-manifest.json']
        for name in formal:
            p=O/'inputs/formal-pin'/Path(name).name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(n.read(name))
        used=set(p for ob in obligations for p in ob['source_paths'])
        used.update('experiments/orthemology-v5/source/'+p for p in ['observations.py','extensions.py','guarded_sampler.py','productive.py','productive_observer.py'])
        used.update(['docs/project-closure/ar8r-v11/post-merge-pmr001-source/PMR_AGCOM_01_CANDIDATE.md','docs/project-closure/ar8r-v11/formalization/AR8R-PMR007-TEN-RESULT-FORMALIZATION-MAP-V11.yaml'])
        selected=[r for r in inventory if r['repository_path'] in used]
        for r in selected:
            b=n.read(r['packet_path'])
            if sha(b)!=r['sha256']:raise ValueError(r['packet_path'])
        for path in ['docs/project-closure/ar8r-v11/post-merge-pmr001-source/PMR_AGCOM_01_CANDIDATE.md','docs/project-closure/ar8r-v11/formalization/AR8R-PMR007-TEN-RESULT-FORMALIZATION-MAP-V11.yaml']:
            p=O/'inputs/supplemental'/Path(path).name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(n.read('source-main/'+path))
    for r in json.loads(z.read('inputs/SUPPLEMENTAL_IDENTITIES.json')):
        p=O/r['path'];p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(r['path']))
    graph=z.read('proposal/lean/P03GuardedGraph.lean')
    if graph!=(O/'formal/P03GuardedGraph.lean').read_bytes():raise ValueError('attempt1 graph preimage drift')
    source_bindings={'merged_main':'03e2604dfcef278b01c60d19b05370fcec4194b6','merged_tree':'3d06e80277ce39286c94307e0f14b215bc94ed83',
      'scope':'Packet SHA/Git-blob identities, not a new live full-tree qualification','original_archive':{'bytes':len(original),'sha256':sha(original)},
      'selected_consumed_canonical_sources':selected,'all_included_verified_source_bindings':inventory,
      'attempt1_supplemental_sources':json.loads(z.read('inputs/SUPPLEMENTAL_IDENTITIES.json')),
      'attempt1_proposal_pre_post_map':json.loads(z.read('proposal/PATCH_MAP.json')),
      'exact_graph_predecessor':{'zip_sha256':sha((O/P03).read_bytes()),'member':'proposal/lean/P03GuardedGraph.lean','sha256':sha(graph)}}
    write('inputs/SOURCE_BINDINGS.json',source_bindings)
    write('inputs/ATTEMPT1_STATEMENT_AND_NEGATIVE_PRESERVATION.json',{'receipt':oldreceipt,'prior_negative_report':z.read('research/NEGATIVE_FINDINGS.md').decode(),'preservation':'Exact entire ZIP retained; no old conclusion was silently changed.'})

statuses={
'U03':'REFUTED / REFORMULATED — total/unsnapshotted native round-trip claims are false; ordinary bounded partial parser/checker/export refinement and owned-ingress specification are supplied.',
'U04':'REFUTED / REFORMULATED — unconditional deployed host-failure atomicity is false; complete-state forward-stuttering, precommit-failure and explicitly coupled probability refinement are supplied for the separate guarded publication proposal.',
'Q1f':'PARTIAL — EXACT IRREDUCIBLE BLOCKER: native Lean 4.19.0 compilation and declaration/type/axiom/artifact readback of the new guarded-VCT candidate have not run after failed exact-toolchain acquisition.'}
write('TERMINAL_STATUSES.json',{'statuses':statuses,'aliases':{'CV-O':'U04'},'canonical_obligation_statuses_changed':False,
 'interpretation':'U03/U04 terminal research reformulations refute overbroad concrete claims, not accepted abstract theorems. They are ordinary conditional source-level proofs, not new kernel verification.',
 'P02_actual_statuses':dict.fromkeys(['U05','U08','CV-R','CV-C','Q1c'],'PARTIAL'),
 'P02_required_ordinary_finite_engine_dependencies':'FULLY_CONSUMED_AND_DISCHARGED_AT_STATED_MODEL_HYPOTHESES',
 'P02_new_kernel_dependencies':'NONE_AVAILABLE_NONE_PRESUMED',
 'ordinary_P03_work_left_as_future_work':[],
 'required_external_gate':{'id':'P03-A2-LEAN419-NATIVE','execution_status':'HOST_EXECUTION_BLOCKED','formal_result_status':'UNPROVED','targets':14,
   'interface':'formal/EXPECTED_TARGETS.json + formal/P03Audit.lean; tools/run_formal419.py',
   'not_a_blocker_from':'unread P02, P12 optional TRC, owner adoption, or historical missing-source recovery'},
 'conditional_extensions':[{'name':'general measurable/probabilistic histories','premises':'Declared measurable joint environment law and commuting/coupled history maps; infinite defect accounting additionally retains J.'}],
 'unclaimed_external_properties':['physical law/entropy/scheduler identification','future-epoch authority','process-crash durability and transparent exactly-once retry','owner adoption/external review']})

new_sources=[fileid('proposal/'+n) for n in ['safe_frontend.py','atomic_engine.py']]
write('proposal/PATCH_AND_STATEMENT_MAP.json',{'canonical_changes':[],
 'new_modules':[dict(r,proposed_repository_path='experiments/orthemology-v5/source/'+Path(r['path']).name,
    preimage='ABSENT_IN_SUPPLIED_SOURCE_SUBTREE; verify absence before later repository addition',adoption='NOT_GRANTED') for r in new_sources],
 'base_choices':[
   {'base':'exact canonical source','status':'15 new adapter tests pass normal and optimised; new named APIs leave legacy iterable behavior intact'},
   {'base':'exact attempt1 three-patch source','status':'new adapters and finite history/measure tests qualified; parent patch identities preserved, not automatically adopted'}],
 'legacy_compatibility':'Do not silently replace proof_export.module with the restrictive parent patch under the old name. export_module_owned is a new named strict boundary; canonical generator-row behavior was freshly compared and preserved.',
 'statement_mapping':[
  {'id':'P03-A2-U03-T1..T5','kind':'ORDINARY_PARTIAL_REFINEMENT_AND_CONSTRUCTOR_PROOFS','report':'research/U03_GENERAL_REFINEMENT.md'},
  {'id':'CV-O-A2-SEQ/ATOMIC/CONCURRENT/FAIL','kind':'ORDINARY_COMPLETE_STATE_THEOREM_FAMILY','report':'research/U04_OPERATIONAL_REFINEMENT.md'},
  {'id':'P03-A2-PROB-MODEL/BUDGET/PUSH','kind':'ORDINARY_P02_INSTANTIATIONS_AND_NEW_COUPLING_DERIVATION','report':'research/P02_OPERATIONAL_INSTANTIATION.md'},
  {'id':'P03A2.guarded_reason_version_composition','kind':'NEW_UNVERIFIED_FORMAL_PROPOSAL_NOT_HISTORICAL_IDENTITY','report':'research/Q1F_LAYERED_VCT.md'}],
 'new_definition_proposals':['owned native capture/outcome algebra','copy-on-write complete-state publication adapter','indexed guarded evidence/semantic/version/root/authority-path model','resource-aware probability-carrying operational abstraction'],
 'rejected_preimages':[fileid(str(p.relative_to(O))) for p in sorted((O/'proposal/rejected-preimages').glob('*')) if p.is_file()]+[fileid(str(p.relative_to(O))) for p in sorted((O/'formal/rejected-preimages').glob('*')) if p.is_file()]})

acq=[]
for label in ['lean-version','toolchain-local-search','acquire-elan','acquire-lean419','acquire-lean-source']:
 d=json.loads((O/'evidence'/label/'command.json').read_text());acq.append({'label':label,'exit_code':d['exit_code'],'command':fileid('evidence/'+label+'/command.json')})
write('evidence/TOOL_DOWNLOAD_RESULT.json',{'provenance':'Assistant transcription of separate container.download tool result in this continuation; not a native stdout stream',
 'url':'https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst',
 'target':'private-locator:b2ee3a75a648f68beefc','tool_response':'ERROR: download failed','compiler_bytes_acquired':False})
write('evidence/TOOLCHAIN_STATUS.json',{'execution_status':'HOST_EXECUTION_BLOCKED','formal_result_status':'UNPROVED',
 'required_lean':'4.19.0 / 6caaee842e94','required_lake':'5.0.0-6caaee8','whole_project_mathlib':'c44e0c8ee63ca166450922a373c7409c5d26b00b',
 'new_core_only_candidate_mathlib_dependency':False,'acquisition_attempts':acq,'separate_download_attempt':fileid('evidence/TOOL_DOWNLOAD_RESULT.json'),
 'compiled_new_targets':0,'new_olean_artifacts':0,'observed_types':0,'observed_axiom_readbacks':0,
 'driver_negative_controls':{'missing_native':'evidence/formal-missing-native-driver/RUN_RECEIPT.json','real_wrong_native':'evidence/formal-wrong-native-driver/RUN_RECEIPT.json'},
 'strict_wrapper_FAIL_preserved':True,'mapped_native_419_not_reused_as_new_proof':True,'432_substitution':False})

rows=[
 ('P03-A2-CE-HOST-REVISION','U04','Observed deployed instruction-prefix counterhistory: content changed, stamps unchanged, failed revision leaves stale-valid edge','evidence/new-countermodels-baseline.json'),
 ('P03-A2-CE-HOST-ISSUANCE','U04','Failed Licence construction occurs after registry insertion in base engine','evidence/new-countermodels-baseline.json'),
 ('P03-A2-CE-MUTABLE-ENCODE','U03','Caller mutation after validation can make unsnapshotted encoder return float bytes rejected by decoder','evidence/new-countermodels-baseline.json'),
 ('P03-A2-CE-REENTRY','U04','Rejected first COW proposal: nested public success can be overwritten without a reentry guard','evidence/reentrancy-red/stderr.bin'),
 ('P03-A2-CE-POSTCOMMIT','U04','Postpublication KeyboardInterrupt does not roll back a committed revision','tools/test_new_frontier.py'),
 ('P03-A2-CE-COUNT-CAPTURE','U03','Rejected first strict exporter capture: two length reads allow 17 traversed rows after validating one','evidence/export-capture-count-red/stderr.bin'),
 ('P03-A2-CE-AE-COMPLETENESS','U04','Pointwise grammar may reject an a.s.-valid factorisation on a zero-mass component','evidence/probability-bridge-normal/RESULT.json'),
 ('P03-A2-CE-ARITHMETIC-COMPLETENESS','U04','Intermediate exact-arithmetic bounds can reject one order of a valid rational law but accept its reordered equivalent','evidence/probability-bridge-normal/RESULT.json'),
 ('P03-A2-CE-TRACE-LAW','U04','Equal trace supports do not entail equal probability laws','evidence/SCOPE_BOUNDARY_CONTROLS.json')]
write('research/NEW_COUNTERMODELS.json',{'countermodels':[{'id':i,'obligation':o,'statement':s,'evidence':fileid(p),'canonical_theorem_refuted':False} for i,o,s,p in rows],
 'Q1f_layer_models':fileid('evidence/vct-layers-normal/LAYER_MODELS.json'),'prior_negative_evidence':'Exact attempt1 and P02 ZIPs, preserved without rerun/relabelled credit'})

required=['final-portable-workspace-run','final-frontier-normal','final-frontier-optimised','final-base-regression-normal','final-base-regression-optimised','final-canonical-adapter-normal','final-canonical-adapter-optimised','final-histories-optimised-run','final-probability-optimised-run','final-vct-optimised-run','scope-boundaries-run']
commands=[]
for p in sorted((O/'evidence').glob('*/command.json')):
 d=json.loads(p.read_text())
 for stream in ['stdout','stderr']:
  b=(p.parent/(stream+'.bin')).read_bytes()
  if len(b)!=d[stream+'_bytes'] or sha(b)!=d[stream+'_sha256']:raise ValueError('command raw binding '+str(p))
 commands.append({'label':p.parent.name,'exit_code':d['exit_code'],'record':fileid(str(p.relative_to(O)))})
for label in required:
 if json.loads((O/'evidence'/label/'command.json').read_text())['exit_code']!=0:raise ValueError('final command failed '+label)
write('evidence/EVIDENCE_SUMMARY.json',{'scope':'FINITE_EXECUTION_AND_ORDINARY_RESEARCH_NOT_KERNEL_PROOF',
 'required_final_commands':[{'path':'evidence/'+label+'/command.json','expected_exit':0} for label in required],
 'recorded_commands':commands,
 'new_unit_tests':{'methods':15,'normal':'PASS','optimised':'PASS','bases':['canonical','attempt1_three_patch']},
 'frozen_base_regression_requalification':{'methods_per_mode':183,'modes':['normal','optimised'],'purpose':'Fresh portable source reconstruction compatibility; no new theorem/census credit'},
 'histories':json.loads((O/'evidence/histories-normal/SUMMARY.json').read_text()),
 'probability':json.loads((O/'evidence/probability-bridge-normal/RESULT.json').read_text()),
 'vct_layers':json.loads((O/'evidence/vct-layers-normal/SUMMARY.json').read_text()),
 'repeat_comparison':fileid('evidence/REPEAT_COMPARISON.json'),
 'final_portable_source':fileid('evidence/FINAL_PORTABLE_SOURCE_READBACK.json'),
 'new_source_hashes':new_sources,
 'formal_scope':fileid('evidence/TOOLCHAIN_STATUS.json'),
 'historical_censuses_reexecuted_for_new_credit':False})
print(json.dumps({'status':'METADATA_BOUND','obligations':len(records),'selected_sources':len(selected),'commands':len(commands),'terminal_statuses':statuses},indent=2))
