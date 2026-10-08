"""Two isolated nonexecuting namespace views of one original portable run.

Additive evidence schema; this helper never routes a view through execute_suite.
Only execute_family launches the physical original, exactly once. Object copies
retain the physical source/capture identity and earn zero new compile credit.
"""
from pathlib import Path
import argparse,copy,os,subprocess,uuid
import portable_capture
import portable_admission as admission
import portable_source as source
import portable_collector as collector
PHYSICAL_SCHEMA='orthemology-v5-portable-physical-run-v1'
EVIDENCE_SCHEMA='orthemology-v5-portable-view-evidence-v1'
NAMES=('d06-portable-cost','d06-portable-runtime-literal')
FAILURES={'FAILED','RESOURCE_INCONCLUSIVE','BLOCKED_TOOLCHAIN','BLOCKED_EXTERNAL_INPUT'}

def component_fingerprints(api):
    modules={'portable_family':Path(__file__),'portable_capture':Path(portable_capture.__file__),'portable_collector':Path(collector.__file__),'portable_admission':Path(admission.__file__),'portable_source':Path(source.__file__)}
    return {name:api.sha(path.read_bytes()) for name,path in modules.items()}|{'portable_bindings_v2':admission.BINDINGS_SHA}


def validate_family(api,suites,sources,root):
    api.require(isinstance(suites,list) and len(suites)==2 and {s['id'] for s in suites}==set(NAMES),'Portable family requires exact two views')
    by_id={s['id']:s for s in suites};plans={name:api.validate_suite(by_id[name],sources,root) for name in NAMES}
    first,second=[by_id[n] for n in NAMES]
    for field in ['toolchain']:
        api.require(api.canonical(first[field])==api.canonical(second[field]),'Portable views use different toolchain pins')
    for field in ['tools','external_inputs','drivers']:
        api.require(api.canonical(first['replay'][field])==api.canonical(second['replay'][field]),'Portable views use different physical prerequisite definitions')
    api.require(first['replay']['stages'][0]==second['replay']['stages'][0],'Portable views disagree about their one parent process')
    return plans

def launch_argv():
    return ['{tool:python}','-B','{adapter}','--trace-portable','{physical}/archives/portable-archive/replay_review_portable.py','{physical}/trace','{physical}/TRACE_STATE.json','--review-zip','{input:core-review-archive}','--lean-bin','{tool:lean-bin}','--mathlib','{dependency:mathlib}','--out','{physical}/original']

def _parent_run(api,row):
    api.require(row['terminal'] in {'COMPLETED','TIMEOUT','INTERRUPTED','SKIPPED','MISSING'},'Unknown physical/audit terminal')
    api.require(type(row['exit_code']) is int and 0<=row['exit_code']<124 if row['terminal']=='COMPLETED' else row['exit_code'] is None,'Invalid physical/audit exit')
    api.require(all(isinstance(row[k],str) and row[k].endswith('Z') for k in ['started_at','ended_at']) and row['started_at']<=row['ended_at'],'Unmeasured physical/audit interval');api.digest(row['log_sha256'])

def _physical(api,physical):
    api.require(physical['schema']==PHYSICAL_SCHEMA and physical['recipe']==admission.RECIPE,'Unknown portable physical recipe')
    api.digest(physical['run_id']);api.require(type(physical['physical_execution_count']) is int and physical['physical_execution_count'] in {0,1},'Portable physical execution count differs')
    collection=physical['collection']
    if collection is None:
        api.require(physical['failure_outcome'] in FAILURES,'Invalid uncollected original outcome');return
    api.require(physical['physical_execution_count']==1 and collection['schema']==collector.SCHEMA and collection['proof_scope']=='NONE' and collection['bindings_sha256']==admission.BINDINGS_SHA and collection['source_archive_sha256']==source.REVIEW_ARCHIVE_SHA,'Foreign portable physical evidence')
    api.keys(physical['launch'],{'argv','cwd','actual_argv_sha256','actual_cwd_sha256','argv_provenance'})
    api.require(physical['launch']['argv']==launch_argv() and physical['launch']['cwd']=='{physical}/project' and physical['launch']['argv_provenance']=='CAPTURED_BY_ADAPTER_AT_LAUNCH','Portable physical launch identity differs')
    api.digest(physical['launch']['actual_argv_sha256']);api.digest(physical['launch']['actual_cwd_sha256'])
    _parent_run(api,collection['parent'])
    owned=admission.bindings();bindings={r['id']:r for view in owned.values() for r in view['children']}
    order=[r['id'] for r in owned[NAMES[1]]['children'] if r['id'].startswith('runtime/')]+[r['id'] for r in owned[NAMES[0]]['children']]+[r['id'] for r in owned[NAMES[1]]['children'] if r['id'].startswith('literal/')]
    observations=collection['observations'];api.require([r['source_child_id'] for r in observations]==order[:len(observations)],'Foreign or reordered portable observation')
    by_id={r['source_child_id']:r for r in observations}
    for i,row in enumerate(observations):
        bound=bindings[row['source_child_id']];api.require(row['capture_index']==i and row['source_sha256']==bound['source_sha256'] and row['source_binding']==bound['source_binding'] and row['positive_prerequisites']==bound['positive_prerequisites'],'Portable child source/capture owner differs')
        _parent_run(api,{**row,'log_sha256':row['captured_log_sha256']});api.require(collection['parent']['started_at']<=row['started_at']<=row['ended_at']<=collection['parent']['ended_at'],'Portable child interval differs')
        api.require(row['outcome'] in {'ACCEPT','REJECT','FAILED','RESOURCE_INCONCLUSIVE'} and row['semantic_outcome']==(row['outcome'] if row['outcome'] in {'ACCEPT','REJECT'} else None),'Portable semantic outcome contradicts terminal')
        if row['outcome'] in {'ACCEPT','REJECT'}:
            api.require(row['terminal']=='COMPLETED' and row['exit_code']==bound['expected_exit'],'Portable control lacks actual required exit')
            api.require(row['outcome']==('REJECT' if bound['expected_exit'] else 'ACCEPT'),'Portable control role differs')
        if row['outcome']=='REJECT':api.require(row['source_child_id']=='cost/ExactInheritedCostMutant' and row['concrete_application_mismatch'] and not row['mismatch_precedes_resource'] and row['source_log_augmentation'] is None and all(pid in by_id and by_id[pid]['outcome']=='ACCEPT' for pid in bound['positive_prerequisites']),'Unbound cost rejection')
        for key in ['captured_log_sha256','capture_record_sha256']:api.digest(row[key])
        if row['original_log_sha256'] is not None:api.digest(row['original_log_sha256'])
    resource=[r['source_child_id'] for r in observations if r['outcome']=='RESOURCE_INCONCLUSIVE'];api.require(resource==collection['resource_children'],'Physical resource census differs')
    if collection['full_original_contract']:
        api.require(len(observations)==326 and collection['parent']['terminal']=='COMPLETED' and collection['parent']['exit_code']==0 and collection['full_checks']['own_fresh_runtime_objects']==167 and collection['full_checks']['finite_cases']==340 and collection['full_checks']['native_process_exit_code']==0 and collection['full_checks']['finite_checks_are_formal_counterexamples'] is False,'Incomplete portable full source contract')
    api.require(collection['physical_outcome']==('RESOURCE_INCONCLUSIVE' if resource or collection['parent']['terminal']!='COMPLETED' else 'CONTRACT_COMPLETE' if collection['full_original_contract'] else 'FAILED'),'Physical aggregate hides child outcome')
    object_ids=[]
    for obj in collection['objects']:
        cid=obj['source_child_id'];api.require(cid in bindings and cid in by_id and by_id[cid]['outcome']=='ACCEPT' and obj['source_binding']==bindings[cid]['source_binding'] and 'original/'+obj['relative_path']==bindings[cid]['object_path'] and obj['capture_index']==by_id[cid]['capture_index'] and obj['compiled_in_physical_run'] is True,'Foreign physical source/object owner');api.digest(obj['sha256']);object_ids.append(cid)
    api.require(len(object_ids)==len(set(object_ids)),'Duplicate physical object')
    for name,view in owned.items():
        ids=[r['id'] for r in view['children']];local=[by_id[cid] for cid in ids if cid in by_id];limited=[r['source_child_id'] for r in local if r['outcome']=='RESOURCE_INCONCLUSIVE']
        ready=collection['full_original_contract'] and len(local)==len(ids) and all(r['outcome'] in {'ACCEPT','REJECT'} for r in local)
        expected={'outcome':'RESOURCE_INCONCLUSIVE' if limited else 'READY_FOR_AUDIT' if ready else 'FAILED_OR_INCOMPLETE','source_child_ids':ids,'resource_children':limited,'missing_children':[cid for cid in ids if cid not in by_id],'physical_child_count':len(local),'new_compilations_from_view':0}
        api.require(collection['views'][name]==expected,'Portable view hides physical child limits')

def _provenance(api,name,physical):
    _physical(api,physical);collection=physical['collection']
    if collection is None:return []
    by_child={r['source_child_id']:r for r in collection['objects']};result=[]
    for binding in admission.bindings()[name]['module_objects']:
        obj=by_child.get(binding['child_id'])
        if obj is None:continue
        api.require(obj['source_binding']['source_id']==binding['source_id'] and obj['relative_path']==binding['relative_object'],'Namespace object/source join differs')
        result.append({'module':binding['module'],'source_binding':obj['source_binding'],'sha256':obj['sha256'],'physical_run_id':physical['run_id'],'physical_source_child_id':binding['child_id'],'physical_object_path':'original/'+obj['relative_path'],'destination_path':'original/'+binding['relative_object'],'capture_index':obj['capture_index'],'new_compilation_credit':0})
    return result

def copy_objects(api,name,physical,original,output):
    api.require(name in NAMES,'Unknown portable view');rows=_provenance(api,name,physical);original=api.no_symlinks(original);output=api.no_symlinks(output)
    pending=[]
    for row in rows:
        src=api.path_in(original,row['physical_object_path'].removeprefix('original/'));dest=api.path_in(output,row['destination_path'])
        api.require(src.is_file() and api.sha(src.read_bytes())==row['sha256'] and not dest.exists(),'Physical object changed or consumer destination exists');pending.append((src,dest,row['sha256']))
    for src,dest,expected in pending:
        dest.parent.mkdir(parents=True,exist_ok=True);data=src.read_bytes();api.require(api.sha(data)==expected,'Physical object changed during consumption');dest.write_bytes(data);api.require(api.sha(dest.read_bytes())==expected,'Copied object differs')
    return rows

def _environment(api,suite,plan,environment,required):
    api.digest(environment['runner_sha256']);api.require(environment['adapter_components']==component_fingerprints(api),'Portable helper closure changed')
    if not required:return
    definitions={'lean':suite['toolchain'],**{r['name']:r for r in suite['replay']['tools']}}
    api.require(set(environment['tools'])==set(definitions),'Missing exact portable tools')
    for name,row in definitions.items():
        actual=environment['tools'][name];api.require(all(actual[k]==row[k] for k in ['kind','version','platform','executable_sha256']),'Portable tool substitution');api.digest(actual['version_log_sha256'])
    pins={r['name']:r['revision'] for r in suite['toolchain']['packages']};api.require(set(environment['dependencies'])==set(plan['packages']),'Missing portable dependencies')
    for name,row in plan['packages'].items():
        actual=environment['dependencies'][name];api.require(actual['kind']=='GIT' and actual['revision']==pins[name] and actual['tracked_clean'] is True and actual['cache_policy']=='TRUSTED_PINNED_OFFICIAL_CACHE' and actual['manifest_sha256']==api.sha(plan['contents'][row['manifest_source_id']]),'Portable dependency/source substitution');api.digest(actual['head_log_sha256']);api.digest(actual['status_log_sha256'])
    expected={r['id']:{'sha256':r['expected_sha256'],'bytes':r['expected_bytes']} for r in suite['replay']['external_inputs']}
    api.require(environment['input_hashes']==expected,'Portable exact input identities differ')

def _audit_valid(api,suite,plan,audit,provenance,ready):
    if audit is None:return False
    api.require(ready,'Ineligible portable view received a target audit')
    api.keys(audit,{'run','source_sha256','object_provenance_sha256','target_audits','status','resource_diagnostic'})
    _parent_run(api,audit['run']);api.require(audit['source_sha256']==api.sha(api._audit_source(list(plan['targets'].values())).encode()) and audit['object_provenance_sha256']==api.canonical(provenance),'Audit script or namespace object mapping differs')
    api.require(type(audit['resource_diagnostic']) is bool and audit['status'] in {'COMPLETE','FAILED_OR_RESOURCE'},'Invalid audit status')
    if audit['status']!='COMPLETE':api.require(not audit['target_audits'],'Failed audit grants target proof credit');return False
    api.require(audit['run']['terminal']=='COMPLETED' and audit['run']['exit_code']==0 and not audit['resource_diagnostic'],'Successful audit has a resource or terminal failure')
    rows=api.indexed(audit['target_audits'],'target_id');api.require(set(rows)==set(plan['targets']),'Incomplete portable safe target audit')
    for tid,row in rows.items():
        target=plan['targets'][tid];api.keys(row,{'target_id','name','type_sha256','axioms','closure_status','checked_declarations','stage_id','log_sha256'})
        api.require(row['name']==target['name'] and row['stage_id']=='_target_audit' and row['log_sha256']==audit['run']['log_sha256'] and row['closure_status']=='CHECKED_SAFE' and type(row['checked_declarations']) is int and row['checked_declarations']>0 and set(row['axioms'])<=api.AXIOMS,'Portable target audit identity or closure differs');api.digest(row['type_sha256'])
    return True

def make_view_receipt(api,suite,sources,reviews,physical,provenance,audit=None,*,plan=None):
    name=suite['id'];api.require(name in NAMES,'Unknown portable view');_physical(api,physical)
    collection=physical['collection'];by_id={r['source_child_id']:r for r in collection['observations']} if collection else {}
    expected=_provenance(api,name,physical);api.require(provenance==expected,'Copied-object provenance differs')
    if plan is None:plan={'targets':{r['target_id']:r for r in suite['replay']['target_names']}}
    # Callers pass the actual validated plan; fixture construction can derive
    # the target-name records directly from the frozen descriptor.
    if isinstance(suite['replay']['target_names'],list):
        targets={r['target_id']:r for r in suite['replay']['target_names']}
        plan={**plan,'targets':targets}
    ready=collection is not None and collection['views'][name]['outcome']=='READY_FOR_AUDIT'
    audited=_audit_valid(api,suite,plan,audit,provenance,ready)
    if collection is None:outcome=physical['failure_outcome']
    elif collection['views'][name]['outcome']=='RESOURCE_INCONCLUSIVE':outcome='RESOURCE_INCONCLUSIVE'
    elif audit is not None and (audit['run']['terminal']!='COMPLETED' or audit['resource_diagnostic']):outcome='RESOURCE_INCONCLUSIVE'
    else:outcome='QUALIFIED_DECLARED_SUITE' if ready and audited else 'FAILED'
    successful=outcome=='QUALIFIED_DECLARED_SUITE'
    parent=collection['parent'] if collection else physical['parent'];end=audit['run']['ended_at'] if audit else parent['ended_at']
    stages=[{'id':admission.PARENT,**{k:parent[k] for k in ['terminal','exit_code','log_sha256']}}];observations=[];controls=[]
    declared_controls={r['id']:r for r in suite['controls']}
    for stage in suite['replay']['stages'][1:]:
        cid=stage['argv'][2];row=by_id.get(cid)
        terminal=row['terminal'] if row else 'SKIPPED';code=row['exit_code'] if row else None;log=row['original_log_sha256'] or row['captured_log_sha256'] if row else api.sha(b'')
        stages.append({'id':stage['id'],'terminal':terminal,'exit_code':code,'log_sha256':log})
        if row:observations.append(copy.deepcopy(row))
        if row and row['semantic_outcome'] is not None:
            for control_id in stage['control_ids']:
                control=declared_controls[control_id];api.require(row['semantic_outcome']==control['expected_outcome'],'Portable declared control outcome mismatch')
                controls.append({k:control[k] for k in ['id','source_id','target_id','role','expected_outcome_sha256']}|{'actual_outcome':row['semantic_outcome'],'actual_outcome_sha256':api.sha(row['semantic_outcome'].encode()),'terminal':terminal,'exit_code':code,'log_sha256':log})
    stages.append({'id':'_target_audit',**{k:audit['run'][k] for k in ['terminal','exit_code','log_sha256']}} if audit else {'id':'_target_audit','terminal':'SKIPPED','exit_code':None,'log_sha256':api.sha(b'')})
    hashes={sid:sources[sid]['public_sha256'] for sid in suite['source_ids']}
    axes=sorted({axis for row in (audit['target_audits'] if audited else []) for axis in row['axioms']})
    evidence={'schema':EVIDENCE_SCHEMA,'view_id':name,'physical_run_id':physical['run_id'],'physical_run_sha256':api.canonical(physical),'physical_run':physical,'descriptor_sha256':api.canonical(suite['replay']),'closure_sha256':api.closure_fingerprint(suite,sources),'import_fingerprints':api.import_fingerprints(suite,sources),'source_hashes_before':hashes,'source_hashes_after':hashes,'runner_sha256':physical['environment']['runner_sha256'],'driver_hashes':{d['id']:d['sha256'] for d in suite['replay']['drivers']},'tool_fingerprints':physical['environment']['tools'],'dependency_checks':physical['environment']['dependencies'],'object_provenance':provenance,'child_observations':observations,'audit':audit,'cache_policy':api.CACHE_POLICY,'view_compilation_count':0,'stage_operation':'NONEXECUTING_SHARED_PHYSICAL_OBSERVATIONS_PLUS_OPTIONAL_VIEW_TARGET_AUDIT'}
    return {'id':name+'-replay','suite_id':name,'family':suite['family'],'suite_sha256':api.canonical(suite),'source_hashes':hashes,'review_hashes':{rid:reviews[rid]['review_sha256'] for rid in suite['review_ids']},'toolchain_sha256':api.canonical(suite['toolchain']),'outcome':outcome,'target_readbacks':[{k:r[k] for k in ['source_id','target_sha256']}|{'target_id':r['id'],'outcome':'CHECKED'} for r in suite['targets']] if successful else [],'controls':controls,'stages':stages,'invocation':['{builtin:portable-view-consumer}',name,physical['run_id']],'started_at':parent['started_at'],'ended_at':end,'exit_code':0 if successful else 2 if outcome in {'BLOCKED_TOOLCHAIN','BLOCKED_EXTERNAL_INPUT'} else 1,'log_sha256':api.canonical({r['id']:r['log_sha256'] for r in stages}),'axioms':axes,'proof_scope':'DECLARED_SUITE' if successful else 'NONE','replay_evidence':evidence}

def validate_receipt(api,receipt,suite,sources,root):
    plan=api.validate_suite(suite,sources,root);evidence=receipt['replay_evidence'];api.require(evidence['schema']==EVIDENCE_SCHEMA,'Unknown portable evidence schema');physical=evidence['physical_run'];_physical(api,physical)
    _environment(api,suite,plan,physical['environment'],physical['collection'] is not None)
    api.require(set(receipt['review_hashes'])==set(suite['review_ids']),'Portable review census differs')
    for value in receipt['review_hashes'].values():api.digest(value)
    reviews={rid:{'review_sha256':value} for rid,value in receipt['review_hashes'].items()}
    expected=make_view_receipt(api,suite,sources,reviews,physical,_provenance(api,suite['id'],physical),evidence['audit'],plan=plan)
    api.require(api.canonical(receipt)==api.canonical(expected),'Portable view receipt differs from exact physical/source/audit evidence')
    if receipt['outcome']=='QUALIFIED_DECLARED_SUITE':
        api.require(len(evidence['object_provenance'])==len(suite['replay']['module_order']) and {r['module'] for r in evidence['object_provenance']}==set(suite['replay']['module_order']),'Successful portable view lacks exact fresh physical closure')
        api.require({r['id'] for r in receipt['controls']}=={r['id'] for r in suite['controls']},'Successful portable view lacks full controls')
    return {'suite_id':suite['id'],'outcome':receipt['outcome'],'scope':'ONE_PHYSICAL_RUN_EXACT_SOURCE_AND_NAMESPACE_AUDIT'}

def _verification_plan(api,suites,plans):
    first=suites[NAMES[0]];suite=copy.deepcopy(first);plan=copy.deepcopy(plans[NAMES[0]])
    suite['replay']['build_roots']=['original/core/cost/build','original/core/runtime/build','original/literal/build'];plan['build_roots']=suite['replay']['build_roots']
    # Union only external import checks and the set of names forbidden in the
    # official cache. Custom compile namespaces and objects are never merged.
    for name in NAMES[1:]:
        for key in ['contents','official','modules']:
            for identity,row in plans[name][key].items():
                if key=='official' and identity in plan[key]:api.require(plan[key][identity]==row,'Different official import identities')
                if identity not in plan[key]:plan[key][identity]=row
    return suite,plan

def _verify_original_libraries(api,plan,mathlib):
    """Cover the unchanged original driver's whole package-cache search path."""
    mathlib=api.no_symlinks(mathlib).resolve()
    declared=[]
    for name,row in plan['packages'].items():
        api.require(row['kind']=='GIT','Portable cache plan requires declared Git packages')
        repository=api.path_in(mathlib,row['path'],dot=True)
        library=api.path_in(repository,'.lake/build/lib/lean')
        # Retain the shared verifier's allowance for absent unimported Cli,
        # and its MissingTool outcome for an absent imported package cache.
        declared.extend(api.package_library(name,library,plan['official']))
    actual=[api.path_in(mathlib,'.lake/build/lib/lean')]+sorted(api.path_in(mathlib,'.lake/packages').glob('*/.lake/build/lib/lean'))
    for library in actual:
        api.no_symlinks(library)
        api.require(library.is_dir(),'Portable original library search contains a non-directory cache')
    api.require(set(actual)==set(declared),'Portable original library search differs from declared package caches')

def _produce(api,suites,plans,sources,root,output,tools,inputs):
    output.mkdir(parents=True);(output/'logs').mkdir();(output/'project').mkdir()
    start=api.utc();parent={'id':admission.PARENT,'terminal':'SKIPPED','exit_code':None,'started_at':start,'ended_at':start,'log_sha256':api.sha(b'')}
    physical={'schema':PHYSICAL_SCHEMA,'run_id':api.sha(uuid.uuid4().bytes),'recipe':admission.RECIPE,'physical_execution_count':0,'environment':{'tools':{},'dependencies':{},'input_hashes':{},'runner_sha256':api.sha(Path(api.__file__).read_bytes()),'adapter_components':component_fingerprints(api)},'collection':None,'parent':parent,'failure_outcome':'FAILED','launch':None}
    resolved={};env={};trace=output/'trace';state=output/'TRACE_STATE.json';original=output/'original';suite,plan=_verification_plan(api,suites,plans)
    api.write_json(output/'PHYSICAL.json',physical)
    try:
        resolved,fingerprints,dependencies,env,input_hashes=api._verify_environment(suite,plan,tools,inputs,output)
        physical['environment'].update(tools=fingerprints,dependencies=dependencies,input_hashes=input_hashes)
        _verify_original_libraries(api,plan,tools['mathlib'])
        archive_root=output/'archives/portable-archive';inventory=api.extract_source_zip(inputs['portable-archive'],archive_root)
        driver=archive_root/admission.DRIVER['driver_path'];api.require(api.sha(driver.read_bytes())==admission.DRIVER['driver_sha256'],'Extracted portable driver differs')
        run_plan=source.build_plan(api,inputs['core-review-archive'],original,resolved['lean'],tools['mathlib'],resolved['python'])
        argv=[resolved['python'],'-B',Path(api.__file__).resolve(),'--trace-portable',driver,trace,state,'--review-zip',inputs['core-review-archive'],'--lean-bin',resolved['lean-bin'].parent,'--mathlib',tools['mathlib'],'--out',original]
        physical['launch']={'argv':launch_argv(),'cwd':'{physical}/project','actual_argv_sha256':api.canonical([str(x) for x in argv]),'actual_cwd_sha256':api.sha(str(output/'project').encode()),'argv_provenance':'CAPTURED_BY_ADAPTER_AT_LAUNCH'}
        api.write_json(output/'ACTUAL_LAUNCH.json',{'argv':[str(x) for x in argv],'cwd':str(output/'project')})
        physical['physical_execution_count']=1;api.write_json(output/'PHYSICAL.json',physical)
        parent.update(api.run_process(argv,output/'project',env,output/'logs/original-portable.log',suite['replay']['stages'][0]['timeout_seconds']))
        if trace.exists() and state.is_file():physical['collection']=collector.collect(api,run_plan,original,trace,parent,api.read_json(state))
        else:api.require(False,'Original portable tracer did not return a terminal capture')
        actual={q.relative_to(archive_root).as_posix():api.sha(api.no_symlinks(q).read_bytes()) for q in archive_root.rglob('*') if q.is_file()};api.require(actual==inventory,'Extracted portable wrapper archive changed')
        for iid,row in plan['inputs'].items():api.require(api._input_inventory(row,inputs[iid],plan)==input_hashes[iid],'Portable external input changed')
        post=output/'postconditions';post.mkdir();(post/'logs').mkdir()
        _,after_tools,after_deps,_,after_inputs=api._verify_environment(suite,plan,tools,inputs,post)
        _verify_original_libraries(api,plan,tools['mathlib'])
        api.require(after_tools==fingerprints and after_deps==dependencies and after_inputs==input_hashes,'Portable tool or dependency changed during physical run')
    except (ValueError,OSError,KeyError,TypeError,subprocess.SubprocessError) as error:
        physical['collection']=None
        if isinstance(error,api.MissingInput):physical['failure_outcome']='BLOCKED_EXTERNAL_INPUT'
        elif isinstance(error,api.MissingTool):physical['failure_outcome']='BLOCKED_TOOLCHAIN'
        elif parent['terminal'] not in {'SKIPPED','COMPLETED'} or (trace.exists() and api.trace_resource_inconclusive(trace)):physical['failure_outcome']='RESOURCE_INCONCLUSIVE'
        api.write_json(output/'FAILURE.json',{'error':type(error).__name__+': '+str(error),'observed_at':api.utc()})
    physical['parent']=parent
    physical['raw_capture_sha256']=api._file_hashes(trace) if trace.exists() else None
    physical['raw_trace_state_sha256']=api.sha(state.read_bytes()) if state.is_file() else None
    api.write_json(output/'PHYSICAL.json',physical)
    return physical,resolved,env

def _run_audit(api,suite,plan,output,resolved,base_env,provenance,physical_output):
    generated=output/'generated';generated.mkdir();logs=output/'logs';logs.mkdir();body=api._audit_source(list(plan['targets'].values()));path=generated/'V5SuccessorReadback.lean';path.write_text(body)
    env=dict(base_env);old_roots={str(physical_output/p) for p in ['original/core/cost/build','original/core/runtime/build','original/literal/build']}
    libraries=[p for p in env['LEAN_PATH'].split(os.pathsep) if p not in old_roots]
    env['LEAN_PATH']=os.pathsep.join([str(output/p) for p in suite['replay']['build_roots']]+libraries)
    run=api.run_process([resolved['lean'],'-j1',path],output/'project',env,logs/'target-audit.log',300)
    text=(logs/'target-audit.log').read_text();resource=source.RESOURCE.search(text) is not None
    audit={'run':run,'source_sha256':api.sha(body.encode()),'object_provenance_sha256':api.canonical(provenance),'target_audits':[],'status':'FAILED_OR_RESOURCE','resource_diagnostic':resource}
    if run['terminal']=='COMPLETED' and run['exit_code']==0 and not resource:
        try:
            parsed=api.parse_readbacks(text,list(plan['targets'].values()));audit['target_audits']=[{'target_id':tid,**row,'stage_id':'_target_audit','log_sha256':run['log_sha256']} for tid,row in parsed.items()];audit['status']='COMPLETE'
        except ValueError as error:api.write_json(output/'AUDIT_FAILURE.json',{'error':str(error),'log_sha256':run['log_sha256']})
    return audit

def execute_family(api,suites,sources,root,output,tools,inputs,*,reviews):
    output=api.no_symlinks(output).absolute();api.require(not output.exists() and not output.resolve().is_relative_to(Path(root).resolve()),'Portable family output must be absent and outside selected sources')
    for name in ['mathlib','lean-bin']:
        if name in tools:
            protected=Path(tools[name]).resolve();protected=protected.parent if name=='lean-bin' else protected
            api.require(not output.resolve().is_relative_to(protected),'Portable family output is inside a protected dependency/tool root')
    plans=validate_family(api,suites,sources,root);by_id={s['id']:s for s in suites}
    api.require(isinstance(reviews,dict) and all(set(s['review_ids'])<=set(reviews) for s in suites),'Missing source-bound portable reviews')
    output.mkdir(parents=True);physical_output=output/'physical'
    # Exactly one call produces both namespace views. Consumers below never
    # invoke the parent again, even when an audit or a view is inconclusive.
    physical,resolved,env=_produce(api,by_id,plans,sources,root,physical_output,tools,inputs)
    receipts={}
    for name in NAMES:
        receipts[name]=consume_view(api,by_id[name],sources,root,output/'views'/name,reviews,physical_output,physical,resolved,env,plans[name])
    result={'schema':'orthemology-v5-portable-family-result-v1','physical_run_id':physical['run_id'],'physical_run_sha256':api.canonical(physical),'physical_execution_count':physical['physical_execution_count'],'views':{name:{'receipt_sha256':api.canonical(row),'outcome':row['outcome'],'proof_scope':row['proof_scope']} for name,row in receipts.items()}}
    api.write_json(output/'FAMILY_RESULT.json',result);return result


def consume_view(api,suite,sources,root,view_output,reviews,physical_output,physical,resolved,env,plan):
    """Implement the portable-view-consumer builtin; never launch the original."""
    name=suite['id'];api.project_suite(suite,sources,root,view_output)
    provenance=copy_objects(api,name,physical,physical_output/'original',view_output);audit=None
    if physical['collection'] is not None and physical['collection']['views'][name]['outcome']=='READY_FOR_AUDIT':
        audit=_run_audit(api,suite,plan,view_output,resolved,env,provenance,physical_output)
    for row in provenance:api.require(api.sha(api.path_in(view_output,row['destination_path']).read_bytes())==row['sha256'],'View audit changed copied object')
    for sid,row in plan['files'].items():api.require(api.path_in(view_output/'project',row['path']).read_bytes()==plan['contents'][sid] and api.public_bytes(root,sources[sid])==plan['contents'][sid],'View audit changed selected source')
    receipt=make_view_receipt(api,suite,sources,reviews,physical,provenance,audit,plan=plan);validate_receipt(api,receipt,suite,sources,root);api.write_json(view_output/'RECEIPT.json',receipt)
    return receipt


def command_line(api,arguments):
    parser=argparse.ArgumentParser(description='Execute the exact portable physical family once and consume its two fixed namespace views.')
    parser.add_argument('--root',type=Path,required=True);parser.add_argument('--out',type=Path,required=True);parser.add_argument('--tool',action='append',default=[]);parser.add_argument('--input',action='append',default=[])
    args=parser.parse_args(arguments)
    def mapping(rows):
        result={}
        for item in rows:
            api.require('=' in item,'Typed binding requires NAME=PATH');name,path=item.split('=',1);api.identifier(name);api.require(name not in result and path,'Repeated or empty portable binding');result[name]=Path(path)
        return result
    import validate_v5_successors as records
    bundle=records.load_bundle(args.root);suites={r['id']:r for r in bundle['suites']};sources={r['id']:r for r in bundle['sources']};reviews={r['id']:r for r in bundle['reviews']}
    api.require(set(NAMES)<=set(suites),'The exact two portable views are not installed')
    result=execute_family(api,[suites[name] for name in NAMES],sources,args.root,args.out,mapping(args.tool),mapping(args.input),reviews=reviews)
    print(api.json.dumps(result));return 0 if all(row['outcome']=='QUALIFIED_DECLARED_SUITE' for row in result['views'].values()) else 1
