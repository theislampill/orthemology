"""Source-specific portable collector. Does not execute or qualify proofs."""
from pathlib import Path
import ast,json,re
import portable_source as source
import portable_admission as admission
SCHEMA='orthemology-v5-portable-physical-evidence-v1'
TRACE_SCHEMA='orthemology-v5-portable-trace-state-v1'
PROGRAMS={'OLD_FALSE':'40f25f3bd087bfb672d9a390913e6959bd399d6bfa90889d4c4d935f91c4eb40','OLD_TRUE':'1bc2df93721979bb9806940d69d03a331d87964b61fb35e1de15fafcc3314424','COMPUTED_FALSE':'08ed35c82f63c180f1c5ea4778efbbebc70521cec514bf9870ab91c558eb7908','COMPUTED_TRUE':'d1a9ed7903def5a682f334d816ab3615bd2f8ef9b350149442404ca1fcd4712f'}

def _equal(api,actual,expected,message):
    api.require(api.canonical(actual)==api.canonical(expected),message)

def _fields(api,row,expected):
    for key,value in expected.items():
        api.require(key in row,'Missing original field: '+key)
        _equal(api,row[key],value,'Original field differs: '+key)

def _read(api,root,name,required=True):
    path=api.path_in(root,name)
    if not path.exists():
        api.require(not required,'Missing original file: '+name);return None
    return api.read_json(path)

def _hash(api,root,name,expected):
    path=api.path_in(root,name);api.require(path.is_file() and api.sha(path.read_bytes())==expected,'Changed original output: '+name)
    return expected

def _symbolic(api,argv,plan,original):
    substitutions=[(plan['children'][0]['argv'][0],'{tool:lean}'),(plan['children'][-1]['argv'][0],'{tool:python}'),(str(original),'{physical}/original')]
    rows=[]
    for value in argv:
        for before,after in sorted(substitutions,key=lambda row:len(row[0]),reverse=True):value=value.replace(before,after)
        api.require(not re.search(r'(?:^|=)/(?![/*])|[A-Za-z]:[\\/]',value),'Private locator outside reviewed symbolic map')
        rows.append(value)
    return rows

def _readbacks(api,bound,text,source_text):
    if bound['axiom_count'] is not None:
        names=api.source_readback_names(source_text,[])
        api.require(len(names)==bound['axiom_count'],'Source-owned axiom census differs')
        if bound['axiom_names']:_equal(api,names,bound['axiom_names'],'Pinned axiom declaration names differ')
        api.check_original_readbacks(text,names)
    for literal,count in bound['literal_counts'].items():
        api.require(text.count(literal)==count,'Original required diagnostic census differs: '+bound['id'])

def _axiom_summary(text,literal=False):
    empty=len(re.findall(r'does not depend on any axioms',text));standard=len(re.findall(r'depends on axioms:\s*\[([^\]]*)\]',text))
    return {'count':empty+standard,**({'empty':empty,'standard_only':standard} if literal else {'without_axioms':empty,'with_only_standard_axioms':standard})}

def _dependencies(api,value,plan):
    pins=json.loads(plan['members']['snapshot/DEPENDENCY_PINS.json'])
    expected=lambda row:dict(name=row['name'],mode='CLEAN_EXACT_GIT',revision=row['revision'],tracked_clean=True,unexpected_lean_sources=False)
    _equal(api,value,{'mathlib':expected(pins['packages'][0]),'packages':[expected(r) for r in pins['packages'][1:]],'dependency_writes':False,'official_cache_objects_trusted':True},'Original dependency identity differs from exact clean Git route')

def _final_checks(api,plan,original,values,by_id,rows,logs):
    wrapper,core,literal=values['wrapper'],values['core'],values['literal']
    _fields(api,wrapper,{'status':'PASS_END_TO_END_PORTABLE_INDEPENDENT_REVIEW','proof_sources_changed':False,'proof_loops_changed':False,'verified_entries':737,'wrapper_sha256':admission.DRIVER['driver_sha256'],'archive_sha256':source.REVIEW_ARCHIVE_SHA,'review_manifest_sha256':source.FILES['REVIEW_MANIFEST.json'],'core_driver_sha256':source.FILES['replay_review.py'],'literal_original_driver_sha256':source.FILES['replay_literal_independent.py'],'literal_derived_driver_sha256':source.DERIVED_LITERAL_SHA})
    _hash(api,original,'core/RESULT.json',wrapper['core_receipt_sha256']);_hash(api,original,'literal/RESULT.json',wrapper['literal_receipt_sha256']);_hash(api,original,'literal_portable_driver.py',source.DERIVED_LITERAL_SHA)
    _fields(api,core,{'status':'PASS_INDEPENDENT_REVIEW_CHECKS','runner_sha256':source.FILES['replay_review.py'],'source_manifest_sha256':source.FILES['snapshot/SOURCE_MANIFEST.json'],'dependency_verifier_sha256':source.FILES['snapshot/verify_dependency_identity.py'],'author_custom_objects_reused':False,'own_prior_custom_objects_reused':False,'source_snapshot_modified':False,'added_heartbeat_settings':False,'parallel_lean_processes':1,'old_runtime_mutant_recompiled':False})
    _fields(api,core['runtime'],{'fresh_custom_modules':167,'closure':'PASS','EveryNewAxiom':_axiom_summary(logs['runtime/EveryNewAxiom']),'ExactStatementReview':_axiom_summary(logs['runtime/ExactStatementReview']),'negative_proof_independence':'PASS_6_TARGETS_WITH_POSITIVE_DETECTOR_CONTROL','source_shape_controls':'PASS_SYNTACTIC_ONLY','old_old_positive_control':'PASS_EVERY_TAPE_KERNEL_THEOREM'})
    cost=by_id['cost/ExactInheritedCostMutant'];cost_text=logs['cost/ExactInheritedCostMutant']
    # The original disposition remains preserved even when the actual child is
    # resource-inconclusive; it is never copied into semantic rejection credit.
    api.require(cost['concrete_application_mismatch'] and (not source.RESOURCE.search(cost_text) or cost['mismatch_precedes_resource']),'Original cost mismatch/order contract failed')
    _fields(api,core['cost'],{'fresh_custom_modules':146,'closure':'PASS','axiom_readback':_axiom_summary(logs['cost/CostReadback']),'mutant':{'disposition':'CONCRETE_PROOF_APPLICATION_REJECTION','rejection_precedes_resource_diagnostic':True,'additional_resource_diagnostic':bool(re.search(r'timeout|maximum number of heartbeats|WALL_TIMEOUT',cost_text,re.I)),'unchanged_statement_not_refuted':True}})
    _dependencies(api,core['dependency_identity'],plan)
    _fields(api,literal,{'status':'PASS_INDEPENDENT_LITERAL_ADDENDUM','runner_sha256':source.DERIVED_LITERAL_SHA,'source_manifest_sha256':source.FILES['literal-snapshot/SOURCE_MANIFEST.json'],'core_source_manifest_sha256':source.FILES['snapshot/SOURCE_MANIFEST.json'],'own_core_objects_verified':167,'author_custom_objects_reused':False,'literal_objects_reused':False,'heartbeat_flags_added':False,'parallel_lean_processes':1,'all_new_axioms':_axiom_summary(logs['literal/EveryLiteralAxiom'],True),'endpoint_correspondence':_axiom_summary(logs['literal/LiteralEndpointReview'],True)})
    _dependencies(api,literal['dependency_identity'],plan)
    _hash(api,original,'core/RESULT.json',literal['core_receipt_sha256']);_hash(api,original,'literal/OWN_FRESH_CORE_BINDINGS.json',literal['core_bindings_sha256'])
    expected=[{'module':r['label'],'source_sha256':r['source_sha256'],'object_sha256':r['object_sha256']} for r in core['runs'][:167]]
    api.require(all(r['suite']=='runtime' and r['exit_code']==0 for r in core['runs'][:167]),'Literal core producer rows are not positive runtime children')
    _equal(api,_read(api,original,'literal/OWN_FRESH_CORE_BINDINGS.json'),expected,'Literal own-fresh dependency join differs')
    api.require(len({r['module'] for r in expected})==167,'Literal runtime object census differs')
    for row in expected:_hash(api,original,'core/runtime/build/'+row['module'].replace('.','/')+'.olean',row['object_sha256'])
    _hash(api,original,'literal/NATIVE_RESULT.json',literal['native_receipt_sha256']);_hash(api,original,'literal/logs/native.log',literal['native_log_sha256'])
    native=_read(api,original,'literal/NATIVE_RESULT.json')
    _fields(api,native,{'status':'PASS_BOUNDED_LITERAL_PARSED_CODE','history_cases':340,'zero_resource_guard_passed':True,'all_results_match_independent_reference':True})
    api.require(isinstance(native['cases'],list) and len(native['cases'])==340 and all(api.canonical(r['actual'])==api.canonical(r['expected']) for r in native['cases']),'Native finite case ledger differs')
    numerals=logs['literal/SelectorNumeralReadback'];api.require('44812' in numerals and '24332' in numerals and numerals.count('428783445879334172098560')==2 and numerals.count('64080')==2,'Literal numeric readback contract differs')
    program_rows=literal['programs'];api.require(len(program_rows)==4 and {r['name'] for r in program_rows}==set(PROGRAMS),'Literal program census differs')
    readback={line.split('=',1)[0]:line.split('=',1)[1] for line in logs['literal/LiteralCodeReadback'].splitlines() if '_BYTES=' in line}
    api.require(set(readback)=={name+'_BYTES' for name in PROGRAMS},'Literal program readback census differs')
    for row in program_rows:
        name=row['name'];_fields(api,row,{'bytes':48389,'sha256':PROGRAMS[name]});_hash(api,original,'literal/programs/'+name+'.bin',PROGRAMS[name])
        data=bytes(ast.literal_eval(readback[name+'_BYTES']));api.require(len(data)==48389 and api.sha(data)==PROGRAMS[name],'Literal program source readback differs')
    return {'core_receipt_sha256':wrapper['core_receipt_sha256'],'literal_receipt_sha256':wrapper['literal_receipt_sha256'],'native_receipt_sha256':literal['native_receipt_sha256'],'own_fresh_runtime_objects':167,'finite_cases':340,'native_process_exit_code':by_id['literal/native']['exit_code'],'finite_checks_are_formal_counterexamples':False}

def collect(api,plan,original,trace,parent,trace_state):
    """Join one physical trace to exact originals; return nonqualifying facts.

    Every event is from the exact source-owned plan. Complete original status is
    checked independently from child outcome; its cost timeout cannot be hidden
    by a wrapper exit zero or transferred to a scoped runtime view.
    """
    original=api.no_symlinks(original).absolute();trace=api.no_symlinks(trace)
    owned=admission.bindings();bindings={row['id']:row for view in owned.values() for row in view['children']}
    api.require(set(bindings)=={r['id'] for r in plan['children']} and len(bindings)==326,'Portable source/capture census differs')
    for event in plan['children']:
        bound=bindings[event['id']]
        api.require(event['source_sha256']==bound['source_sha256'] and event['member']==bound['archive_member'],'Portable child source owner differs')
    captured=source.read_capture(api,plan,trace)
    api.keys(trace_state,{'schema','events_observed','children_observed','complete','event_plan_sha256'})
    api.require(trace_state['schema']==TRACE_SCHEMA and trace_state['event_plan_sha256']==plan['event_plan_sha256'] and type(trace_state['events_observed']) is int and 0<=trace_state['events_observed']<=381 and type(trace_state['children_observed']) is int and trace_state['children_observed']==len(captured) and type(trace_state['complete']) is bool,'Trace completion state differs')
    api.require(trace_state['complete'] is (trace_state['events_observed']==381 and len(captured)==326),'Trace completion flag contradicts census')
    completed_parent=parent['terminal']=='COMPLETED' and type(parent['exit_code']) is int and parent['exit_code']==0
    if completed_parent:api.require(trace_state['complete'],'Successful parent omitted original children/events')
    values={'wrapper':_read(api,original,'WRAPPER_RESULT.json',False),'core':_read(api,original,'core/RESULT.json',False),'literal':_read(api,original,'literal/RESULT.json',False)}
    row_by_id={}
    for kind in ['core','literal']:
        value=values[kind]
        if value is None:continue
        rows=value.get('runs',[]);api.require(isinstance(rows,list),'Original runs field differs')
        expected=[e['id'] for e in plan['children'] if (e['id'].startswith('literal/') if kind=='literal' else not e['id'].startswith('literal/')) and e['id']!='literal/native']
        ids=[('literal' if kind=='literal' else row['suite'])+'/'+row['label'] for row in rows]
        api.require(ids==expected[:len(ids)],'Original namespace/child order differs')
        row_by_id.update(zip(ids,rows))
    native_present=values['literal'] is not None and 'native_command' in values['literal']
    if native_present:row_by_id['literal/native']=values['literal']
    api.require(set(row_by_id)<={e['id'] for e in plan['children'][:len(captured)]},'Original row has no captured child')
    observations=[];objects=[];all_objects={};logs={}
    for i,cap in enumerate(captured):
        event=plan['children'][i];bound=bindings[event['id']];row=row_by_id.get(event['id'])
        api.require(all(isinstance(cap[k],str) and cap[k].endswith('Z') for k in ['started_at','ended_at']) and parent['started_at']<=cap['started_at']<=cap['ended_at']<=parent['ended_at'],'Child interval outside physical parent')
        _fields(api,cap,{'timeout_seconds':event['timeout'],'source_sha256_before':event['source_sha256'],'source_sha256_after':event['source_sha256'],'output_absent_before':True})
        api.require(api.sha(api.no_symlinks(event['source_path']).read_bytes())==event['source_sha256'],'Source changed after child capture')
        rawcode=cap['raw_returncode'];api.require(rawcode is None or type(rawcode) is int,'Invalid raw captured return code')
        api.require(rawcode==cap['exit_code'] if cap['terminal']=='COMPLETED' else (rawcode is None or rawcode<0 or rawcode>=124),'Raw/canonical child terminal contradicts')
        rawlog=api.path_in(trace,f'{i:04}.log').read_bytes();logpath=api.path_in(original,event['original_log']);original_log=logpath.read_bytes() if logpath.is_file() else None
        if row is not None and event['id']!='literal/native':
            prefix='literal' if event['id'].startswith('literal/') else 'core'
            api.require(prefix+'/'+row['log']==event['original_log'],'Original log path/namespace differs')
            if prefix=='core':api.require(row['source']==event['member'],'Original source locator differs')
        observed=source.classify_child(api,event,row,cap,original_log,rawlog)
        text=(original_log if original_log is not None else rawlog).decode();logs[event['id']]=text
        if observed['outcome']=='ACCEPT':_readbacks(api,bound,text,plan['members'][event['member']].decode())
        actual_objects=cap['output_hashes_after'];api.require(isinstance(actual_objects,dict),'Missing output-at-completion record')
        expected_paths={event['object_path']} if event['object_path'] and Path(event['object_path']).is_file() else set()
        api.require(set(actual_objects)==expected_paths,'Captured child object path differs')
        if observed['outcome']=='ACCEPT' and event['object_path']:api.require(expected_paths,'Successful child omitted object')
        for path,expected_hash in actual_objects.items():
            obj=api.no_symlinks(path);api.require(obj.is_file() and api.sha(obj.read_bytes())==expected_hash,'Fresh object changed after capture')
            api.require(row is not None and row.get('object_sha256')==expected_hash,'Original object hash differs from completion capture')
            rel=obj.relative_to(original).as_posix();api.require(rel not in all_objects,'Physical object was produced twice');all_objects[rel]=expected_hash
            if observed['outcome']=='ACCEPT':objects.append({'relative_path':rel,'sha256':expected_hash,'source_child_id':event['id'],'source_binding':bound['source_binding'],'capture_index':i,'compiled_in_physical_run':True})
        observed.update(capture_index=i,source_binding=bound['source_binding'],argv=_symbolic(api,cap['argv'],plan,original),argv_provenance='CAPTURED_THEN_EXACT_RECIPE_REDACTED',cwd='{physical}/original/review-source',started_at=cap['started_at'],ended_at=cap['ended_at'],budget_seconds=event['timeout'],raw_returncode=rawcode,original_log_path=event['original_log'],capture_record_sha256=api.sha(api.path_in(trace,f'{i:04}.json').read_bytes()),positive_prerequisites=bound['positive_prerequisites'])
        observations.append(observed)
    actual={}
    for root in ['core/runtime/build','core/cost/build','literal/build']:
        folder=api.path_in(original,root)
        if folder.exists():
            for path in folder.rglob('*'):
                api.no_symlinks(path)
                if path.is_file() and path.suffix=='.olean':actual[path.relative_to(original).as_posix()]=api.sha(path.read_bytes())
    _equal(api,actual,all_objects,'Missing or extra physical namespace object')
    by_id={r['source_child_id']:r for r in observations}
    for row in observations:
        if row['outcome']=='REJECT':api.require(all(pid in by_id and by_id[pid]['outcome']=='ACCEPT' for pid in row['positive_prerequisites']),'Negative child lacks exact positive prerequisites')
    full=completed_parent and values['wrapper'] is not None and values['wrapper'].get('status')=='PASS_END_TO_END_PORTABLE_INDEPENDENT_REVIEW'
    checks={}
    if completed_parent:api.require(full,'Successful parent lacks original full receipt')
    if full:
        api.require(len(observations)==326 and all(r['outcome']=='ACCEPT' or (r['source_child_id']=='cost/ExactInheritedCostMutant' and r['outcome'] in {'REJECT','RESOURCE_INCONCLUSIVE'}) for r in observations),'Original PASS contradicts captured child outcome')
        checks=_final_checks(api,plan,original,values,by_id,row_by_id,logs)
        snapshot=api.path_in(original,'review-source');inventory={q.relative_to(snapshot).as_posix():api.sha(api.no_symlinks(q).read_bytes()) for q in snapshot.rglob('*') if q.is_file()}
        _equal(api,inventory,{name:api.sha(data) for name,data in plan['members'].items()},'Extracted original archive changed')
    resource=[r['source_child_id'] for r in observations if r['outcome']=='RESOURCE_INCONCLUSIVE']
    views={}
    for name,view in owned.items():
        ids=[r['id'] for r in view['children']];local=[by_id[cid] for cid in ids if cid in by_id];local_resource=[r['source_child_id'] for r in local if r['outcome']=='RESOURCE_INCONCLUSIVE']
        ready=full and len(local)==len(ids) and all(r['outcome'] in {'ACCEPT','REJECT'} for r in local)
        views[name]={'outcome':'RESOURCE_INCONCLUSIVE' if local_resource else 'READY_FOR_AUDIT' if ready else 'FAILED_OR_INCOMPLETE','source_child_ids':ids,'resource_children':local_resource,'missing_children':[cid for cid in ids if cid not in by_id],'physical_child_count':len(local),'new_compilations_from_view':0}
    return {'schema':SCHEMA,'proof_scope':'NONE','physical_outcome':'RESOURCE_INCONCLUSIVE' if resource or parent['terminal']!='COMPLETED' else 'CONTRACT_COMPLETE' if full else 'FAILED','full_original_contract':full,'source_archive_sha256':source.REVIEW_ARCHIVE_SHA,'bindings_sha256':admission.BINDINGS_SHA,'event_plan_sha256':plan['event_plan_sha256'],'trace_state':trace_state,'parent':parent,'observations':observations,'objects':objects,'views':views,'full_checks':checks,'resource_children':resource,'original_receipt_hashes':{kind:api.sha(api.path_in(original,path).read_bytes()) for kind,path in [('wrapper','WRAPPER_RESULT.json'),('core','core/RESULT.json'),('literal','literal/RESULT.json')] if values[kind] is not None}}
