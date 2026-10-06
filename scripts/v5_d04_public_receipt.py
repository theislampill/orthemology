"""D04 publication representation, derived only after full private validation.

This is a source-bound summary of reviewed execution evidence. Its public
validator checks summary identity and associations; it does not replay private
log bytes. Raw v2 validation and science execution remain separate interfaces.
"""
import copy
import hashlib
import json
from pathlib import Path
import re

SCHEMA='orthemology-v5-d04-public-receipt-v1'
CONT_SCHEMA='orthemology-v5-d04-public-covering-continuation-v1'
RECIPE='d04-full-private-validation-to-public-summary-v1'
MODE='CAPTURED_THEN_EXACT_RECIPE_REDACTED'
SCOPE='PUBLIC_SUMMARY_IDENTITY_AND_SOURCE_CONTRACT_NOT_RAW_LOG_REVALIDATION'
TRANSPORT={'capture_records','record','log_hex','stream_hex','raw_capture_files','trace_launch','source_root','output_root','bindings','actual_launch_argv','helper_argv','launch_cwd'}
CHILD_KEYS={'id','index','probe','argv','cwd','timeout_seconds','capture','stdin','environment_sha256','source_binding','input_bindings','source_hashes','replacement_bindings','started_at','ended_at','terminal','exit_code','log_sha256','stream_hashes','output_hashes','record_file_sha256','record_canonical_sha256','argv_sha256','cwd_sha256','assessment'}
INV_KEYS={'parent_stage_id','recipe','driver_sha256','source_argv','launch_argv','runner_sha256','contract_data_sha256','context_sha256','replay_id','trace_sha256','trace_manifest','parent_log_sha256','child_count','probe_count','children','normalization','normalization_sha256','qualified_objects','capture_state','capture_error_sha256','private_invocation_sha256','private_binding_sha256','physical_launch_sha256','helper_sha256','mode'}
DERIVATION_KEYS={'recipe','original_schema','original_file_sha256','original_canonical_sha256','original_bytes','raw_validator_sha256','transform_sha256','public_body_sha256','binding_sha256','validation_scope','independent_evidence_increment'}
NORMALIZATION_SCOPES={
    't07-criterion-translated-v1':'Bounded original vectors. Additional fresh CriterionTransport object and exact target audit remain adapter stages.',
    't07-covering-translated-v1':'Source-bound complete covering vectors; exact target closure audit remains separate.',
    't07-composition-projection-v1':'Current public archive projection integrity only; no full upstream/freeze verification.',
    't07-composition-packaging-translated-v1':'Optional packaging controls only; no semantic compiler rejection or new scientific credit.',
    't07-composition-original-v1':'Original main compiled reference run; reviewer and six serial runtime mutations remain separate stages of this physical suite.',
    't07-composition-serial-mutations-v1':'Six theorem-erased native sensitivity controls; actual compiler/link child journals require first-run tracing. Mutants are never accepted theorem sources.'}

def require(value,message):
    if not value:raise ValueError(message)

def canonical(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def sha(raw):return hashlib.sha256(raw).hexdigest()

def keys(value,expected):
    require(isinstance(value,dict) and set(value)==set(expected),'Public projection fields differ')

def digest(value):
    require(isinstance(value,str) and re.fullmatch('[0-9a-f]{64}',value) is not None,'Malformed projection digest')

def _finite(value):
    # JSON roundtrip forbids NaN, infinity and non-JSON types.
    return json.loads(json.dumps(value,ensure_ascii=False,allow_nan=False))

def _public(value):
    if isinstance(value,dict):
        require(not set(value)&TRANSPORT,'Private capture transport in public representation')
        for key,item in value.items():
            require(not key.endswith('_hex'),'Encoded byte transport in public representation')
            if key in {'started_at','ended_at','observed_at'} and item is not None:
                require(isinstance(item,str) and re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?Z',item)is not None,'Noncanonical public UTC timestamp')
            _public(key);_public(item)
    elif isinstance(value,list):
        for item in value:_public(item)
    elif isinstance(value,str):
        require(not re.search(r'(?<![\w{}])/(?:home|mnt|tmp|workspace|private|Users)(?:/|$)|[A-Za-z]:[\\/]|file://',value,re.I),'Private locator in public projection')
        require(not re.search(r'(?:%2f|%5c)(?:home|mnt|users|tmp|workspace)|(?:\\u002[fF]|\\u005[cC])',value,re.I),'Encoded locator in public projection')

def symbolic(value,mapping):
    """Prefix-bound path mapping, including keys; never basename truncation."""
    candidates=sorted([(raw,'{'+name+'}')for name,raw in mapping.items()],key=lambda x:len(x[0]),reverse=True)
    require(all(isinstance(raw,str) and raw.startswith('/')for raw,_ in candidates),'Symbolic map requires absolute roots')
    require(len({x[0]for x in candidates})==len(candidates),'Ambiguous symbolic root mapping')
    def visit(item):
        if isinstance(item,str):
            result=item
            for raw,token in candidates:
                result=re.sub(r'(?<![\w./-])'+re.escape(raw)+r'(?=/|$|[\s:\'\"])',lambda _:token,result)
            require(not re.search(r'(?:^|[=:\s\'\"])/(?![/*])|[A-Za-z]:[\\/]',result),'Unrecognized absolute path in symbolic projection')
            return result
        if isinstance(item,list):return [visit(x)for x in item]
        if isinstance(item,dict):
            result={}
            for k,v in item.items():
                target=visit(k);require(target not in result,'Symbolic path key collision');result[target]=visit(v)
            return result
        return item
    return visit(value)

def _literal_spec(a,contract,row):
    if row['probe']:
        spec=contract.get('tool_probes',[])[row['index']]
        return dict(spec,id='probe-'+str(row['index']),timeout_seconds=None,sources=[],outputs=[],replace_fresh_predecessor=[])
    spec=contract['children'][row['index']]
    require(spec['id']==row['id'],'Child source identity/order changed')
    return spec

def _path_map(actual,declared):
    require(len(actual)==len(declared) and len(set(actual))==len(actual) and len(set(declared))==len(declared),'Ambiguous path contract')
    return dict(zip(actual,declared))

def _project_child(a,inv,item,contract,mapping):
    raw=item['record'];spec=_literal_spec(a,contract,raw);expanded=a.d04_expand(spec,mapping)
    require(raw['argv']==expanded['argv'] and raw['cwd']==expanded['cwd'],'Captured child differs from exact source argv/cwd')
    fields={'id','index','probe','timeout_seconds','capture','stdin','environment_sha256','started_at','ended_at','terminal','exit_code','log_sha256','stream_hashes'}
    child={key:copy.deepcopy(raw[key])for key in fields}
    child.update(argv=copy.deepcopy(spec['argv']),cwd=spec['cwd'],record_file_sha256=item['record_file_sha256'],record_canonical_sha256=canonical(raw),argv_sha256=canonical(raw['argv']),cwd_sha256=canonical(raw['cwd']))
    child['source_binding']=copy.deepcopy(spec.get('source_binding',raw['source_binding']))
    if child['source_binding']['kind']=='GENERATED_BY_ORIGINAL':child['source_binding']['generated_sha256']=raw['source_binding']['generated_sha256']
    inputs=[x for x in spec['sources']if x['kind']!='TOOL_PROBE']
    require(len(inputs)==len(raw['input_bindings']),'Source input census differs')
    child['input_bindings']=[dict(copy.deepcopy(declared),actual_sha256=actual['actual_sha256'])for declared,actual in zip(inputs,raw['input_bindings'])]
    child['source_hashes']={(v.get('member')or v.get('origin_member')or v['path']):v['actual_sha256']for v in child['input_bindings']}
    replacements=spec['replace_fresh_predecessor']
    require(len(replacements)==len(raw['replacement_bindings']),'Replacement source census differs')
    child['replacement_bindings']=[dict(copy.deepcopy(s),actual_sha256=r['actual_sha256'],producer_capture_sha256=r['producer_capture_sha256'])for s,r in zip(replacements,raw['replacement_bindings'])]
    pathmap=_path_map(expanded['outputs'],spec['outputs'])
    require(set(raw['output_hashes'])<=set(pathmap),'Foreign captured output')
    child['output_hashes']={pathmap[name]:value for name,value in raw['output_hashes'].items()}
    complete=inv['normalization']is not None
    child['assessment']=('ACCEPT'if raw['exit_code']==0 else'REJECT')if complete else'NOT_QUALIFIED'
    return child

def _project_normalization(inv):
    raw=inv['normalization']
    if raw is None:return None
    result=raw['result'];projected={k:copy.deepcopy(result[k])for k in ['summary','objects','source_hashes_read_back','scope']if k in result}
    projected['children']=[{k:copy.deepcopy(c[k])for k in ['id','terminal','exit_code','log_sha256']if k in c}for c in result.get('children',[])]
    return {'recipe':raw['recipe'],'normalizer_assets':copy.deepcopy(raw['normalizer_assets']),'result':projected}

def project_invocation(inv,*,adapter):
    a=adapter;contract,mapping=a.d04_capture_specs(inv)
    require(inv['capture_error']is None and inv['raw_capture_files']=={},'Unparsed raw capture remains private; no public summary contract')
    keep={'parent_stage_id','recipe','driver_sha256','source_argv','launch_argv','runner_sha256','contract_data_sha256','context_sha256','replay_id','trace_sha256','trace_manifest','parent_log_sha256','child_count','probe_count','normalization_sha256','qualified_objects','helper_sha256'}
    result={key:copy.deepcopy(inv[key])for key in keep}
    result.update(mode=MODE,children=[_project_child(a,inv,item,contract,mapping)for item in inv['capture_records']],normalization=_project_normalization(inv),capture_state='PARSED',capture_error_sha256=None,private_invocation_sha256=canonical(inv),private_binding_sha256=canonical(mapping),physical_launch_sha256=canonical({'argv':inv['actual_launch_argv'],'cwd':inv['launch_cwd'],'helper':inv['helper_argv']}))
    return result

def _expected_observation(inv,child):
    return {'source_child_id':child['id'],'parent_stage_id':inv['parent_stage_id'],'driver_sha256':inv['driver_sha256'],'parser_id':inv['recipe'],'mode':'NONEXECUTING_OBSERVATION','argv_provenance':MODE,'source_binding':child['source_binding'],'argv':child['argv'],'cwd':child['cwd'],'started_at':child['started_at'],'ended_at':child['ended_at'],'physical_run_sha256':inv['trace_sha256'],'parent_log_sha256':inv['parent_log_sha256'],'terminal':child['terminal'],'exit_code':child['exit_code'],'actual_outcome':child['assessment'],'log_sha256':child['log_sha256'],'result_record_sha256':child['record_canonical_sha256'],'output_hashes':child['output_hashes']}

def _unique_json(raw):
    def pairs(items):
        result={}
        for k,v in items:
            require(k not in result,'Duplicate raw JSON key');result[k]=v
        return result
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda _:(_ for _ in()).throw(ValueError('Nonfinite raw JSON')))

def derive(raw,suite,sources,reviews,root,*,adapter,d02,raw_adapter=None):
    """Validate raw bytes with unchanged D02/D03 before deriving any summary."""
    a=adapter;validator=raw_adapter or a;receipt=_unique_json(raw)
    require(receipt['replay_evidence']['schema']=='orthemology-v5-replay-evidence-v2' and a.d04_is_suite(suite),'Only original D04 raw v2 receipts can use this derivation')
    d02._receipt(receipt,suite,sources,reviews,root,validator.validate_receipt)
    a.validate_suite(suite,sources,root)
    result=copy.deepcopy(receipt);e=result['replay_evidence'];e['schema']=SCHEMA
    e['driver_invocations']=[project_invocation(row,adapter=a)for row in receipt['replay_evidence']['driver_invocations']]
    children={(inv['parent_stage_id'],c['id']):(inv,c)for inv in e['driver_invocations']for c in inv['children']if not c['probe']}
    e['child_observations']=[]
    for observed in receipt['replay_evidence']['child_observations']:
        inv,child=children[(observed['parent_stage_id'],observed['source_child_id'])]
        expected=_expected_observation(inv,child)
        e['child_observations'].append(dict(expected,stage_id=observed['stage_id'],observed_at=observed['observed_at']))
    d={'recipe':RECIPE,'original_schema':receipt['replay_evidence']['schema'],'original_file_sha256':sha(raw),'original_canonical_sha256':canonical(receipt),'original_bytes':len(raw),'raw_validator_sha256':sha(Path(validator.__file__).read_bytes()),'transform_sha256':sha(Path(__file__).read_bytes()),'public_body_sha256':canonical(result),'validation_scope':SCOPE,'independent_evidence_increment':0}
    d['binding_sha256']=canonical(d);e['derivation']=d
    _public(result);d02._receipt(result,suite,sources,reviews,root,a.validate_receipt)
    custody={'original_file_sha256':sha(raw),'original_canonical_sha256':canonical(receipt),'derived_canonical_sha256':canonical(result),'original_to_derived_ids':{receipt['id']:result['id']},'independent_evidence_increment':0,'scientific_executions':0,'field_policy':{'unchanged':'All top-level fields and base execution evidence','derived':'Source-owned child vectors and bounded capture/normalization summaries','private_only':'Raw records, absolute bindings, log and stream bytes, raw parser failure text'},'private_invocation_hashes':[canonical(i)for i in receipt['replay_evidence']['driver_invocations']]}
    return {'receipt':result,'custody':custody}

def _check_child(child,contract,parent,complete,*,adapter):
    a=adapter;keys(child,CHILD_KEYS)
    require(type(child['index'])is int and child['index']>=0 and type(child['probe'])is bool,'Child index/probe type differs')
    spec=_literal_spec(a,contract,child)
    require(child['argv']==spec['argv'] and child['cwd']==spec['cwd'],'Public argv/cwd differs from exact source contract')
    require(child['capture']==spec['capture'] and child['timeout_seconds']==spec['timeout_seconds'] and (child['timeout_seconds']is None or type(child['timeout_seconds'])is int),'Child budget/capture differs')
    require(child['stdin']=={'mode':'INHERITED_NO_INPUT','data_sha256':None},'Public child stdin differs')
    for key in ['environment_sha256','record_file_sha256','record_canonical_sha256','argv_sha256','cwd_sha256']:digest(child[key])
    require(isinstance(child['started_at'],str) and child['started_at'].endswith('Z') and parent['started_at']<=child['started_at']<=parent['ended_at'],'Child start outside measured parent')
    terminal=child['terminal'];require(terminal in {'RUNNING','COMPLETED','TIMEOUT','INTERRUPTED','LAUNCH_ERROR'},'Unknown actual child terminal')
    if terminal=='RUNNING':
        require(not complete and child['ended_at']is None and child['exit_code']is None and child['log_sha256']is None and child['stream_hashes']=={} and child['output_hashes']=={},'Running child acquired terminal credit')
    else:
        require(isinstance(child['ended_at'],str) and child['ended_at'].endswith('Z') and child['started_at']<=child['ended_at']<=parent['ended_at'],'Child end outside measured parent')
        require(type(child['exit_code'])is int and 0<=child['exit_code']<124 if terminal=='COMPLETED' else child['exit_code']is None,'Invalid child exit')
        digest(child['log_sha256'])
        keys(child['stream_hashes'],{'stdout','stderr'}if child['capture']=='SEPARATE_BYTES'else set())
        for value in child['stream_hashes'].values():digest(value)
    inputs=[r for r in spec['sources']if r['kind']!='TOOL_PROBE']
    require(len(child['input_bindings'])==len(inputs),'Missing source input')
    for actual,expected in zip(child['input_bindings'],inputs):
        keys(actual,set(expected)|{'actual_sha256'});require({k:v for k,v in actual.items()if k!='actual_sha256'}==expected,'Wrong original/generated source binding');digest(actual['actual_sha256'])
        expected_sha=expected.get('sha256')or expected.get('expected_sha256')
        if expected_sha is not None:require(actual['actual_sha256']==expected_sha,'Changed original/generated source bytes')
    require(child['source_hashes']=={(r.get('member')or r.get('origin_member')or r['path']):r['actual_sha256']for r in child['input_bindings']},'Source summary association differs')
    if child['probe']:
        expected_binding={'kind':'TOOL_PROBE','tool_name':'lean','executable_sha256':a.LEAN_SHA,'driver_sha256':contract['source_sha256']}
    else:
        expected_binding=copy.deepcopy(spec['source_binding'])
        if expected_binding['kind']=='GENERATED_BY_ORIGINAL':expected_binding['generated_sha256']=child['input_bindings'][0]['actual_sha256']
    require(child['source_binding']==expected_binding,'Changed executed source classification')
    require(len(child['replacement_bindings'])==len(spec['replace_fresh_predecessor']),'Replacement evidence omitted')
    for actual,expected in zip(child['replacement_bindings'],spec['replace_fresh_predecessor']):
        keys(actual,set(expected)|{'actual_sha256','producer_capture_sha256'});require({k:v for k,v in actual.items()if k not in {'actual_sha256','producer_capture_sha256'}}==expected,'Replacement source contract changed');digest(actual['actual_sha256']);digest(actual['producer_capture_sha256'])
    require(isinstance(child['output_hashes'],dict) and set(child['output_hashes'])<=set(spec['outputs']),'Foreign output identity')
    for value in child['output_hashes'].values():digest(value)
    if complete:
        code=0 if child['probe']else spec['expected_exit_code']
        require(terminal=='COMPLETED' and type(child['exit_code'])is int and child['exit_code']==code and set(child['output_hashes'])==set(spec['outputs']),'Incomplete child cannot qualify')
        require(child['assessment']==('ACCEPT'if code==0 else'REJECT'),'Wrong source-bound child outcome')
    else:require(child['assessment']=='NOT_QUALIFIED','Unqualified original parent acquired child credit')

def _check_normalization(inv,*,adapter):
    a=adapter;n=inv['normalization']
    if n is None:
        require(inv['normalization_sha256']is None and inv['qualified_objects']=={},'Missing original normalization acquired qualification');return
    digest(inv['normalization_sha256']);keys(n,{'recipe','normalizer_assets','result'})
    result=n['result'];allowed={'children','summary','objects','source_hashes_read_back','scope'}
    require({'children','summary'}<=set(result)<=allowed,'Unbounded original result payload')
    if inv['recipe']in NORMALIZATION_SCOPES:require(result.get('scope')==NORMALIZATION_SCOPES[inv['recipe']],'Missing/changed original scientific scope')
    else:require('scope'not in result,'Unprescribed scientific scope')
    for c in result['children']:
        require({'id','log_sha256'}<=set(c)<={'id','log_sha256','terminal','exit_code'},'Unbounded normalized child payload')
        if 'exit_code'in c:require(c['exit_code']is None or type(c['exit_code'])is int,'Normalized exit type differs')
    # Reuse only the original pure source-result association validator. No raw
    # capture validator is invoked on these publication summaries.
    association={'recipe':inv['recipe'],'normalization':n,'normalization_sha256':canonical(n),'capture_records':[{'record':c}for c in inv['children']]}
    a.d04_bind_normalization(association)
    recipe=inv['recipe'];fixed=a.d04_fixed_summary(recipe)
    if fixed is None:
        allowed_summary={
          't07-criterion-translated-v1':{'tests','repair_cases','installation_cases','source_bytes'},
          't07-composition-packaging-translated-v1':{'packaging_tests'},
          't07-composition-original-v1':{'native_assertions','wrapper_tests','finite_cases','source_bytes'},
          't07-composition-review-translated-v1':{'native_assertions','monotonicity_readbacks'},
          't07-composition-serial-mutations-v1':{'runtime_mutants','actual_driver_processes'},
          't07-covering-translated-v1':{'status','public_manifest_sha256','science_manifest_sha256','review_receipt_sha256','public_bound_files','science_bound_files','author_declarations_axiom_checked','independent_theorems_axiom_checked','author_mutations_rejected','independent_primary_mutations_rejected','normal_and_optimized_semantic_results_match_archived_evidence','immutable_payload_before_after','successful_compiler_logs_clean','lean_sha256','mathlib_revision','mathlib_source_files_verified','translation'}}
        keys(result['summary'],allowed_summary[recipe])
        if recipe=='t07-covering-translated-v1':
            summary=result['summary']
            for key in ['public_manifest_sha256','science_manifest_sha256','review_receipt_sha256']:digest(summary[key])
            for key in ['public_bound_files','science_bound_files','author_declarations_axiom_checked','independent_theorems_axiom_checked','mathlib_source_files_verified']:
                require(type(summary[key])is int and 0<=summary[key]<=1000000,'Covering finite census type/bound differs')
            require(summary['translation']=='Source-bound shell-free serial command vectors; all 12 compiler rejections retain actual argv, terminal and logs.','Covering source-owned result literal differs')

def validate_children(evidence,plan,stages,successful,*,adapter):
    a=adapter;parents={s['id']:s for s in plan['stages'].values()if s['driver_id']and s['argv'][0]!='{builtin:observe-child}'}
    declared={s['id']:s for s in plan['stages'].values()if s['argv'][0]=='{builtin:observe-child}'}
    launches=a.indexed(evidence['driver_invocations'],'parent_stage_id');observations=a.indexed(evidence['child_observations'],'stage_id')
    require(list(launches)==list(parents)[:len(launches)] and set(observations)<=set(declared),'Omitted/reordered/foreign parent or child')
    if successful:require(set(launches)==set(parents) and set(observations)==set(declared),'Incomplete successful physical census')
    previous=None
    for sid in plan['stages']:
        row=stages[sid]
        if row['terminal']=='SKIPPED':continue
        require(previous is None or previous<=row['started_at'],'Original stages overlap/reorder');previous=row['ended_at']
    expected_observations={};producers={};objects={};runs=set()
    for pid,inv in launches.items():
        keys(inv,INV_KEYS);contract=a.d04_contracts()['recipes'][inv['recipe']];parent=stages[pid]
        require(contract['family']==plan['d04_family'] and contract['parent_stage']['id']==pid,'Foreign original recipe')
        require(inv['source_argv']==contract['parent_stage']['argv'] and inv['driver_sha256']==contract['source_sha256'] and inv['helper_sha256']==(contract['translation_sha256']or contract['source_sha256']),'Original/translated driver identity differs')
        require(inv['launch_argv']==['{tool:python}','-B','{adapter}','--trace-d04','{out}/contexts/'+pid+'.json'] and inv['mode']==MODE,'Changed source-owned tracer representation')
        require(inv['runner_sha256']==evidence['runner_sha256'] and inv['contract_data_sha256']==a.D04_DATA_SHA256 and inv['parent_log_sha256']==parent['log_sha256'],'Wrong source-contract/runner/parent association')
        for key in ['context_sha256','replay_id','private_invocation_sha256','private_binding_sha256','physical_launch_sha256']:digest(inv[key])
        for name,value in inv['trace_manifest'].items():a.relative(name);digest(value)
        require(inv['trace_sha256']==(canonical(inv['trace_manifest'])if inv['trace_manifest']else None),'Wrong physical trace identity')
        if inv['trace_sha256']is not None:require(inv['trace_sha256']not in runs,'Duplicate physical run credit');runs.add(inv['trace_sha256'])
        complete=inv['normalization']is not None
        require(inv['capture_state']=='PARSED' and inv['capture_error_sha256']is None,'Unparsed raw capture has no public summary contract')
        if complete:require(parent['terminal']=='COMPLETED' and parent['exit_code']==0,'Failed parent cannot qualify children')
        if successful:require(complete,'Successful receipt lacks original source result')
        children=[c for c in inv['children']if not c['probe']];probes=[c for c in inv['children']if c['probe']]
        require(type(inv['child_count'])is int and inv['child_count']==len(children)<=len(contract['children']) and type(inv['probe_count'])is int and inv['probe_count']==len(probes)<=len(contract.get('tool_probes',[])),'Wrong child/probe census')
        require([c['id']for c in children]==[c['id']for c in contract['children'][:len(children)]] and [c['index']for c in probes]==list(range(len(probes))),'Physical child/probe order differs')
        if complete:require(len(children)==len(contract['children']) and len(probes)==len(contract.get('tool_probes',[])) and 'LAUNCH.json'in inv['trace_manifest'],'Incomplete complete parent')
        last=parent['started_at'];manifest_names={'LAUNCH.json'}if 'LAUNCH.json'in inv['trace_manifest']else set()
        for child in [*probes,*children]:
            _check_child(child,contract,parent,complete,adapter=a)
            require(last is not None and last<=child['started_at'],'Physical child intervals overlap/reorder');last=child['ended_at']
            stem=('probe-'if child['probe']else'')+f"{child['index']:04}"
            require(inv['trace_manifest'].get(stem+'.json')==child['record_file_sha256'],'Original record-file identity differs');manifest_names.add(stem+'.json')
            if child['log_sha256']is not None:
                require(inv['trace_manifest'].get(stem+'.log')==child['log_sha256'],'Child log/trace association differs');manifest_names.add(stem+'.log')
                for stream,value in child['stream_hashes'].items():require(inv['trace_manifest'].get(stem+'.'+stream+'.log')==value,'Stream/trace hash differs');manifest_names.add(stem+'.'+stream+'.log')
            if not complete:continue
            for binding in child['input_bindings']:
                if binding['kind']=='GENERATED_BY_ORIGINAL' and binding.get('expected_sha256')is None:
                    owner=binding.get('producer_recipe')or inv['recipe'];path=binding.get('predecessor_path',binding['path'])
                    require(producers.get((owner,binding['producer'],path),{}).get('sha256')==binding['actual_sha256'],'Generated input has no exact prior producer')
            for binding in child['replacement_bindings']:
                owner=binding.get('producer_recipe')or inv['recipe'];path=binding.get('predecessor_path',binding['path'])
                require(producers.get((owner,binding['producer'],path))=={'sha256':binding['actual_sha256'],'record':binding['producer_capture_sha256']},'Fresh replacement predecessor differs')
            if child['exit_code']==0:
                for path,value in child['output_hashes'].items():producers[(inv['recipe'],child['id'],path)]={'sha256':value,'record':child['record_canonical_sha256']}
            if not child['probe']:expected_observations[(pid,child['id'])]=_expected_observation(inv,child)
        require(set(inv['trace_manifest'])==manifest_names,'Extra/missing original trace entry')
        _check_normalization(inv,adapter=a)
        expected_objects={}
        if complete:
            by_id={c['id']:c for c in children}
            for module,producer in a.d04_contracts()['families'][plan['d04_family']]['object_producers'].items():
                if producer.get('recipe')!=inv['recipe']:continue
                child=by_id[producer['child_id']];source_sha=a.sha(plan['contents'][plan['modules'][module]['source_id']])
                require(any(b['actual_sha256']==source_sha and (b.get('sha256')or b.get('expected_sha256'))==source_sha for b in child['input_bindings']),'Target producer source differs')
                require(child['terminal']=='COMPLETED' and child['exit_code']==0 and producer['path']in child['output_hashes'],'Missing positive target object producer')
                expected_objects[producer['path'].removeprefix('{out}/')]=child['output_hashes'][producer['path']]
        require(inv['qualified_objects']==expected_objects,'Object qualification differs from physical producer')
        for name,value in expected_objects.items():require(name not in objects,'Duplicate object producer');objects[name]=value
    for sid,row in observations.items():
        key=tuple(declared[sid]['argv'][1:]);require(key in expected_observations,'Observation has no qualified physical child');expected=expected_observations[key]
        keys(row,set(expected)|{'stage_id','observed_at'});require({k:v for k,v in row.items()if k not in {'stage_id','observed_at'}}==expected,'Observation changed captured facts')
        require(all(row[k]==stages[sid][k]for k in ['terminal','exit_code','log_sha256']),'Observation/stage terminal differs')
        require(stages[key[0]]['ended_at']<=stages[sid]['started_at']<=row['observed_at']<=stages[sid]['ended_at'],'Observation interval differs')
    for stage in stages.values():
        for name,value in stage['output_hashes'].items():require(name not in objects or objects[name]==value,'Contradictory output digest');objects[name]=value
    require(evidence['output_hashes']==objects,'Output ledger differs from retained physical producers')

def validate_receipt(receipt,suite,sources,root,*,adapter):
    a=adapter
    try:
        keys(receipt,a.HC_RECEIPT_KEYS)
        _finite(receipt);_public(receipt)
        if receipt['replay_evidence']['schema']==CONT_SCHEMA:return validate_covering(receipt,suite,sources,root,adapter=a)
        plan=a.validate_suite(suite,sources,root)
        require('d04_family'in plan,'Public D04 representation applied to another family')
        e=receipt['replay_evidence'];keys(e,a.EVIDENCE_KEYS|{'child_observations','driver_invocations','derivation'})
        require(e['schema']==SCHEMA and e['cache_policy']==a.CACHE_POLICY,'Wrong public evidence schema/cache policy')
        require(receipt['invocation']==['replay_v5_successors.py','--execute','--suite',suite['id'],'--out','{out}'],'Public invocation differs from original source replay')
        require(receipt['id']==suite['id']+'-replay','Unknown original D04 receipt identity')
        d=e['derivation'];keys(d,DERIVATION_KEYS)
        require(d['recipe']==RECIPE and d['original_schema']=='orthemology-v5-replay-evidence-v2' and d['validation_scope']==SCOPE,'Unknown public derivation contract')
        for key in ['original_file_sha256','original_canonical_sha256','raw_validator_sha256','transform_sha256','public_body_sha256','binding_sha256']:digest(d[key])
        require(type(d['original_bytes'])is int and d['original_bytes']>0 and type(d['independent_evidence_increment'])is int and d['independent_evidence_increment']==0,'Projection fabricated execution/independence credit')
        require(d['transform_sha256']==sha(Path(__file__).read_bytes()),'Projection transform version differs')
        body=copy.deepcopy(receipt);body['replay_evidence'].pop('derivation')
        require(d['public_body_sha256']==canonical(body) and d['binding_sha256']==canonical({k:v for k,v in d.items()if k!='binding_sha256'}),'Projection custody/body digest differs')
        a._validate_receipt_body(receipt,suite,sources,root,plan,e,True,lambda ev,p,s,ok:validate_children(ev,p,s,ok,adapter=a))
        return {'suite_id':suite['id'],'outcome':receipt['outcome'],'scope':SCOPE}
    except (KeyError,TypeError,IndexError,AttributeError,UnicodeError,OverflowError)as error:
        raise ValueError('Malformed D04 public projection: '+str(error))from error


# The covering continuation is the exact already-reviewed one-audit interface,
# not another original source execution. Its raw parser remains in its frozen
# module; only publication summaries are checked here.
CONT_RAW='orthemology-v5-covering-audit-continuation-v1'
CONT_EXECUTOR='f77e456b0b99b7b932013e84bacf105ebc07508e30384b5ca96bbeb4e23f17a4'
CONT_HELPER='ebed39c4cf80983b9ef667a656d519decfc449585004245395eec578948adba7'
CONT_DATA='d9ffbc13339e72a3d39c39938fc2cc5ae25d92ddb8482b1581861325da8af23a'
CONT_POLICY='PINNED_OFFICIAL_CACHES_REUSED_COVERING_EXECUTION_FRESH_COLLECTION_AND_AUDIT'
CONT_METADATA={'descriptor_sha256','closure_sha256','source_hashes_before','source_hashes_after','import_fingerprints','tool_fingerprints','dependency_checks'}
CONT_EVIDENCE=CONT_METADATA|{'schema','runner_sha256','helper_sha256','data_sha256','cache_policy','prior','retained_collection','retained_input_checks','fresh_audit','stage_results','target_audits','output_hashes','accounting','derivation'}

def covering_pins():
    path=Path(__file__).with_name('v5_covering_continuation.json').absolute()
    for part in [path,*path.parents]:require(not part.is_symlink(),'Symlink covering data path is not admitted')
    raw=path.read_bytes()
    require(sha(raw)==CONT_DATA,'Reviewed covering data changed')
    return _unique_json(raw)

def _seal_projection(public,raw,original,validator):
    d={'recipe':RECIPE,'original_schema':original['replay_evidence']['schema'],'original_file_sha256':sha(raw),'original_canonical_sha256':canonical(original),'original_bytes':len(raw),'raw_validator_sha256':sha(Path(validator.__file__).read_bytes()),'transform_sha256':sha(Path(__file__).read_bytes()),'public_body_sha256':canonical(public),'validation_scope':SCOPE,'independent_evidence_increment':0}
    d['binding_sha256']=canonical(d);public['replay_evidence']['derivation']=d

def derive_covering(raw,suite,sources,reviews,root,*,adapter,raw_adapter,d02):
    a=adapter;original=_unique_json(raw)
    require(original['replay_evidence']['schema']==CONT_RAW and sha(Path(raw_adapter.__file__).read_bytes())==CONT_EXECUTOR,'Wrong raw covering contract/validator')
    # This call checks the actual embedded private receipt/failure bytes,
    # captures, original logs, exact recollection and fresh audited log bytes.
    d02._receipt(original,suite,sources,reviews,root,raw_adapter.validate_receipt)
    e=original['replay_evidence'];public=copy.deepcopy(original);out=public['replay_evidence'];out['schema']=CONT_SCHEMA
    prior=e['prior'];nested=derive(bytes.fromhex(prior['receipt_raw_hex']),suite,sources,reviews,root,adapter=a,raw_adapter=raw_adapter,d02=d02)
    out['prior']={key:copy.deepcopy(prior[key])for key in ['receipt_sha256','receipt_canonical_sha256','failure_sha256']}
    out['prior']['receipt']=nested['receipt']
    collection=e['retained_collection'];pubcollection=copy.deepcopy(collection)
    inv=project_invocation(collection['driver_invocation'],adapter=a);pubcollection['driver_invocation']=inv
    children={c['id']:c for c in inv['children']if not c['probe']}
    pubcollection['child_observations']=[dict(_expected_observation(inv,children[row['source_child_id']]),stage_id=row['stage_id'],observed_at=row['observed_at'])for row in collection['child_observations']]
    out['retained_collection']=pubcollection
    rawinv=e['fresh_audit']['resolved_invocation'];oldbindings=prior['receipt']['replay_evidence']['driver_invocations'][0]['bindings']
    pathmap={'out':str(Path(rawinv['argv'][2]).parent.parent),'prior':oldbindings['out'],'tool:lean':oldbindings['tool:lean'],'lean-release':str(Path(oldbindings['tool:lean']).parent.parent),'dependency:mathlib':oldbindings['dependency:mathlib']}
    out['fresh_audit']={'audit_log_sha256':sha(bytes.fromhex(e['fresh_audit']['audit_log_hex'])),'audit_source_sha256':sha(bytes.fromhex(e['fresh_audit']['audit_source_hex'])),'resolved_invocation':symbolic(rawinv,pathmap),'original_resolved_invocation_sha256':e['fresh_audit']['resolved_invocation_sha256'],'argv_provenance':MODE}
    _seal_projection(public,raw,original,raw_adapter)
    _public(public);d02._receipt(public,suite,sources,reviews,root,a.validate_receipt)
    return {'receipt':public,'custody':{'original_file_sha256':sha(raw),'original_canonical_sha256':canonical(original),'derived_canonical_sha256':canonical(public),'original_to_derived_ids':{original['id']:public['id']},'predecessor':nested['custody'],'independent_evidence_increment':0,'scientific_executions':0,'raw_log_revalidation':'Performed only before derivation with exact frozen raw validator','public_validation_scope':SCOPE}}

def _covering_derivation(receipt):
    e=receipt['replay_evidence'];d=e['derivation'];keys(d,DERIVATION_KEYS)
    require(d['recipe']==RECIPE and d['original_schema']==CONT_RAW and d['validation_scope']==SCOPE,'Wrong covering projection contract')
    for key in ['original_file_sha256','original_canonical_sha256','raw_validator_sha256','transform_sha256','public_body_sha256','binding_sha256']:digest(d[key])
    require(type(d['original_bytes'])is int and d['original_bytes']>0 and type(d['independent_evidence_increment'])is int and d['independent_evidence_increment']==0,'Projection acquired new execution credit')
    require(d['raw_validator_sha256']==CONT_EXECUTOR and d['transform_sha256']==sha(Path(__file__).read_bytes()),'Covering validator/transform identity differs')
    body=copy.deepcopy(receipt);body['replay_evidence'].pop('derivation')
    require(d['public_body_sha256']==canonical(body) and d['binding_sha256']==canonical({k:v for k,v in d.items()if k!='binding_sha256'}),'Covering projection/custody digest differs')

def _covering_collection(collection,prior,plan,suite,*,adapter):
    a=adapter;pins=covering_pins()
    keys(collection,{'parser_id','parser_revision','collector_runner_sha256','started_at','ended_at','driver_invocation','child_observations','stage_results','control_diagnostics','controls','output_hashes'})
    require(collection['parser_id']=='t07-covering-translated-v1' and collection['parser_revision']=='d04-covering-retained-negative-controls-v1' and collection['collector_runner_sha256']==CONT_EXECUTOR,'Wrong covering recollection parser')
    require(prior['ended_at']<collection['started_at']<=collection['ended_at'],'Recollection relabelled physical child times')
    old=prior['replay_evidence'];physical=old['driver_invocations'][0];inv=collection['driver_invocation']
    # Only the original source-result classification and object qualification
    # changed during recollection. Every physical/capture identity stays exact.
    omit={'normalization','normalization_sha256','qualified_objects','private_invocation_sha256'}
    physical_body={k:v for k,v in physical.items()if k not in omit};qualified_body={k:v for k,v in inv.items()if k not in omit}
    # The raw failed parent deliberately had NOT_QUALIFIED child classifications.
    for body in [physical_body,qualified_body]:
        body['children']=[{k:v for k,v in c.items()if k!='assessment'}for c in body['children']]
    require(physical_body==qualified_body,'Recollection changed actual retained execution')
    require(inv['trace_sha256']==pins['trace_sha256'] and inv['normalization_sha256']==pins['normalization_sha256'] and inv['qualified_objects']==pins['qualified_objects'],'Recollection changed exact source-result/trace/object identity')
    retained=copy.deepcopy(old);retained['driver_invocations']=[inv];retained['child_observations']=collection['child_observations']
    stages=a.indexed(retained['stage_results']);parsed=a.indexed(collection['stage_results']);observed=a.indexed(collection['child_observations'],'stage_id')
    declared={sid:s for sid,s in plan['stages'].items()if sid!='original-driver'}
    require(list(parsed)==list(observed)==list(declared) and len(parsed)==38,'Recollection omitted/reordered original child')
    last=collection['started_at']
    for sid,spec in declared.items():
        row=parsed[sid];keys(row,a.AC_STAGE_KEYS)
        require(row['id']==sid and row['argv']==spec['argv'] and row['cwd']==spec['cwd'] and type(row['budget_seconds'])is int and row['budget_seconds']==spec['timeout_seconds'] and row['output_hashes']=={},'Recollection became an execution')
        require(last<=row['started_at']<=row['ended_at']<=collection['ended_at'] and observed[sid]['observed_at']==row['ended_at'],'Recollection parsing interval changed');last=row['ended_at'];stages[sid]=row
    retained['output_hashes']=collection['output_hashes']
    validate_children(retained,plan,stages,True,adapter=a)
    expected_controls=[];diagnostics=[]
    definitions={c['id']:c for c in suite['controls']}
    for sid,spec in declared.items():
        row=parsed[sid]
        require(row['terminal']=='COMPLETED' and type(row['exit_code'])is int and row['exit_code']in spec['expected_exit_codes'],'Wrong retained semantic exit')
        for cid in spec['control_ids']:
            control=definitions[cid];outcome='ACCEPT'if row['exit_code']==0 else'REJECT'
            expected_controls.append({'id':cid,**{k:control[k]for k in ['source_id','target_id','role','expected_outcome_sha256']},'actual_outcome':outcome,'actual_outcome_sha256':sha(outcome.encode()),'terminal':row['terminal'],'exit_code':row['exit_code'],'log_sha256':row['log_sha256']})
            diagnostics.append({'control_id':cid,'stage_id':sid,'prerequisite_stage_ids':spec['depends_on'],'expected':spec['expected_diagnostics'],'observed_log_sha256':row['log_sha256'],'match':'MATCHED'})
    require(collection['controls']==expected_controls and collection['control_diagnostics']==diagnostics,'Retained control/diagnostic outcome changed')
    return collection

def validate_covering(receipt,suite,sources,root,*,adapter):
    a=adapter;keys(receipt,a.HC_RECEIPT_KEYS);pins=covering_pins();e=receipt['replay_evidence'];keys(e,CONT_EVIDENCE);_covering_derivation(receipt)
    require(e['schema']==CONT_SCHEMA and e['cache_policy']==CONT_POLICY,'Wrong covering public schema/policy')
    require(suite['id']==pins['suite_id'] and canonical(suite)==pins['suite_sha256'],'Changed covering suite')
    plan=a.validate_suite(suite,sources,root)
    binding=e['prior'];keys(binding,{'receipt','receipt_sha256','receipt_canonical_sha256','failure_sha256'})
    require(binding['receipt_sha256']==pins['prior_receipt_sha256'] and binding['receipt_canonical_sha256']==pins['prior_receipt_canonical_sha256'] and binding['failure_sha256']==pins['failure_sha256'],'Changed retained raw predecessor identity')
    prior=binding['receipt'];validate_receipt(prior,suite,sources,root,adapter=a);old=prior['replay_evidence']
    pd=old['derivation'];require(pd['original_file_sha256']==binding['receipt_sha256'] and pd['original_canonical_sha256']==binding['receipt_canonical_sha256'] and pd['original_bytes']==pins['prior_receipt_bytes'],'Projected predecessor is not the retained raw identity')
    require(prior['outcome']=='FAILED' and prior['proof_scope']=='NONE' and prior['controls']==[] and old['runner_sha256']==pins['original_runner_sha256'],'Failed predecessor acquired qualification')
    for key in ['suite_id','family','suite_sha256','source_hashes','review_hashes','toolchain_sha256']:require(receipt[key]==prior[key],'Continuation source/review/tool identity changed')
    for key in CONT_METADATA:require(e[key]==old[key],'Continuation dependency/import/source identity changed')
    require(e['runner_sha256']==CONT_EXECUTOR and e['helper_sha256']==CONT_HELPER and e['data_sha256']==CONT_DATA,'Wrong exact covering executor/helper/data')
    require(receipt['invocation']==['replay_v5_successors.py','--covering-audit-continuation','--suite',suite['id'],'--prior','{prior}','--out','{out}'],'Continuation became another source execution')
    audit=a._ac_fresh_stages(receipt,e,prior,a);stages=a.indexed(e['stage_results']);pre=stages['_prerequisites']
    collection=_covering_collection(e['retained_collection'],prior,plan,suite,adapter=a)
    require(pre['started_at']<=collection['started_at']<=collection['ended_at']<=pre['ended_at'],'Recollection is outside actual fresh prerequisites')
    require(receipt['controls']==collection['controls'],'Fresh target audit changed retained controls')
    checks=e['retained_input_checks'];keys(checks,{'retained_before','retained_after','objects_before','objects_after','official_cache_measurements'})
    require(checks['retained_before']==checks['retained_after']=={'file_count':356,'tree_sha256':pins['retained_tree_sha256']},'Retained source/output inventory differs')
    require(checks['objects_before']==checks['objects_after']==pins['all_objects'] and checks['official_cache_measurements']==pins['official_cache_measurements'],'Retained objects or official caches differ')
    require(e['accounting']==pins['accounting'] and all(type(v)is int for v in e['accounting'].values()),'Invented compilation/object/independence credit')
    fresh=e['fresh_audit'];keys(fresh,{'audit_log_sha256','audit_source_sha256','resolved_invocation','original_resolved_invocation_sha256','argv_provenance'})
    require(fresh['argv_provenance']==MODE and fresh['audit_log_sha256']==audit['log_sha256'],'Fresh log/provenance differs')
    digest(fresh['original_resolved_invocation_sha256'])
    require(fresh['audit_source_sha256']==pins['audit_source_sha256']==sha(a._audit_source(list(plan['targets'].values())).encode()),'Auditor source/targets changed')
    resolved=fresh['resolved_invocation'];keys(resolved,{'argv','cwd','timeout_seconds','lean_path','generated_source_sha256','scope'})
    paths=['{prior}/'+name for name in suite['replay']['build_roots']]
    caches={r['root_id']:r for r in pins['official_cache_measurements']}
    for name,row in plan['packages'].items():
        if caches[name]['file_count']:paths.append('{dependency:mathlib}/'+(row['path'].rstrip('/')+'/'if row['path']!='.'else'')+'.lake/build/lib/lean')
    paths.append('{lean-release}/lib/lean')
    require(resolved=={'argv':['{tool:lean}','-j1','{out}/generated/V5SuccessorReadback.lean'],'cwd':'{prior}/project','timeout_seconds':300,'lean_path':paths,'generated_source_sha256':pins['audit_source_sha256'],'scope':'ONE_COVERING_TARGET_AUDIT_NO_SOURCE_REPLAY'},'Fresh audit arguments/import environment differ')
    expected_id=suite['id']+'-audit-continuation-'+sha((receipt['started_at']+fresh['original_resolved_invocation_sha256']).encode())[:16]
    require(receipt['id']==expected_id and receipt['id']!=prior['id'],'Continuation identity differs')
    require(e['output_hashes']=={'generated/V5SuccessorReadback.lean':pins['audit_source_sha256']},'Audit output claims new object builds')
    successful=receipt['outcome']=='QUALIFIED_DECLARED_SUITE'
    if successful:
        require(audit['terminal']=='COMPLETED' and type(audit['exit_code'])is int and audit['exit_code']==0 and receipt['proof_scope']=='DECLARED_SUITE' and receipt['exit_code']==0,'Successful continuation lacks audit terminal')
        audits=a.indexed(e['target_audits'],'target_id');require(set(audits)==set(plan['targets']),'Missing audited target')
        for tid,row in audits.items():
            keys(row,{'target_id','name','type_sha256','axioms','closure_status','checked_declarations','stage_id','log_sha256'})
            require(row['name']==plan['targets'][tid]['name'] and row['stage_id']=='_target_audit' and row['log_sha256']==audit['log_sha256'],'Wrong target/name/log association');digest(row['type_sha256'])
            require(set(row['axioms'])<=a.AXIOMS and row['closure_status']=='CHECKED_SAFE' and type(row['checked_declarations'])is int and row['checked_declarations']>0,'Unsafe or incomplete target closure')
        expected=[{'target_id':r['id'],'source_id':r['source_id'],'target_sha256':r['target_sha256'],'outcome':'CHECKED'}for r in suite['targets']]
        require(receipt['target_readbacks']==expected and receipt['axioms']==sorted({x for row in audits.values()for x in row['axioms']}),'Target declaration/axiom census differs')
    else:
        require(receipt['outcome']in {'FAILED','RESOURCE_INCONCLUSIVE'} and receipt['proof_scope']=='NONE' and receipt['exit_code']==1 and receipt['target_readbacks']==[] and receipt['axioms']==[] and e['target_audits']==[],'Unqualified audit acquired target credit')
        if receipt['outcome']=='FAILED':require(audit['terminal']=='COMPLETED' and type(audit['exit_code'])is int and 0<audit['exit_code']<124,'Failed audit lacks concrete failure exit')
        if audit['terminal']in {'TIMEOUT','INTERRUPTED'}:require(receipt['outcome']=='RESOURCE_INCONCLUSIVE','Resource terminal misclassified')
    return {'suite_id':suite['id'],'outcome':receipt['outcome'],'scope':SCOPE}
