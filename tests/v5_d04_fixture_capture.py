"""Explicitly synthetic receipt fixtures; never execute archived sources."""
import copy
from datetime import datetime,timedelta
from pathlib import Path

def make_capture(a, recipe, output='/synthetic-d04-fixture', producers=None, start='2026-10-05T12:00:00Z'):
    producers={} if producers is None else producers
    contract=a.d04_contracts()['recipes'][recipe]; family=a.d04_contracts()['families'][contract['family']]
    initial=datetime.fromisoformat(start.replace('Z','+00:00'))
    instant=lambda seconds:(initial+timedelta(seconds=seconds)).isoformat().replace('+00:00','Z')
    bindings={'out':output,'project':output+'/project','build':output+'/build','adapter':str(Path(a.__file__).resolve()),
        'tool:python':'/synthetic-tools/python','tool:python312':'/synthetic-tools/python312','tool:lean':'/synthetic-tools/lean',
        'tool:leanc':'/synthetic-tools/leanc','dependency:mathlib':'/synthetic-tools/mathlib','locked:mathlib-package-libraries':'/synthetic-tools/mathlib/.lake/packages/fake/.lake/build/lib/lean'}
    bindings['source']=str(Path(output)/'archives/source-archive'/family['archive_root'])
    wanted={'out','project','build','adapter','source','tool:lean'}|{'tool:'+row['name']for row in family['suite']['replay']['tools']}
    if family['suite']['replay']['packages']:wanted|={'dependency:mathlib','locked:mathlib-package-libraries'}
    bindings={key:value for key,value in bindings.items()if key in wanted}
    local=dict(bindings,trace=output+'/traces/'+contract['parent_stage']['id'])
    if contract.get('temporary_cwd_binding'):
        prefix='dynamic-interlock-replay-' if recipe=='t07-dynamic-base-v1' else 'root-attribution-replay-'
        local[contract['temporary_cwd_binding']['token'][1:-1]]=output+'/tmp/'+prefix+'synthetic'
    helper,args,cwd=a.d04_launch_description(recipe,bindings)
    launch=['{tool:python}','-B','{adapter}','--trace-d04','{out}/contexts/'+contract['parent_stage']['id']+'.json']
    invocation={'parent_stage_id':contract['parent_stage']['id'],'recipe':recipe,'driver_sha256':contract['source_sha256'],
        'source_argv':contract['parent_stage']['argv'],'launch_argv':launch,'actual_launch_argv':a.d04_expand(launch,bindings),'launch_cwd':str(cwd),
        'helper_argv':[str(helper),*args],'helper_sha256':contract['translation_sha256']or contract['source_sha256'],
        'runner_sha256':a.sha(Path(a.__file__).read_bytes()),'contract_data_sha256':a.D04_DATA_SHA256,
        'context_sha256':a.sha(b'SYNTHETIC CONTEXT'),'source_root':bindings['source'],'output_root':output,'bindings':bindings,
        'replay_id':a.sha(b'SYNTHETIC REPLAY'),'trace_sha256':None,'trace_manifest':{},'trace_launch':None,'parent_log_sha256':a.sha(b'SYNTHETIC PARENT'),
        'child_count':len(contract['children']),'probe_count':len(contract.get('tool_probes',[])),'capture_records':[],
        'normalization':None,'normalization_sha256':None,'qualified_objects':{}}
    if hasattr(a,'d04_expected_objects'):invocation.update(capture_error=None,raw_capture_files={})
    invocation['trace_launch']={'recipe':recipe,'parent_stage_id':invocation['parent_stage_id'],'context_sha256':invocation['context_sha256'],
        'runner_sha256':invocation['runner_sha256'],'original_source_sha256':contract['source_sha256'],'helper_sha256':invocation['helper_sha256'],
        'helper_argv':invocation['helper_argv'],'helper_cwd':invocation['launch_cwd'],'mechanism':'RUNPY_IN_TRACER'}
    for probe, definitions in [(False,contract['children']),(True,contract.get('tool_probes',[]))]:
        for index,definition in enumerate(definitions):
            spec=a.d04_expand(definition,local);name=('probe-'if probe else'')+f'{index:04}'
            inputs=[];source_hashes={}
            for source in spec.get('sources',[]):
                if source['kind']=='TOOL_PROBE':continue
                digest=source.get('sha256')or source.get('expected_sha256')or producers.get((source.get('producer_recipe')or recipe,source.get('producer'),source.get('predecessor_path',source['path'])),{}).get('sha256')or a.sha(('SYNTHETIC INPUT '+source['path']).encode())
                inputs.append({**source,'actual_sha256':digest});source_hashes[source.get('member')or source.get('origin_member')or source['path']]=digest
            binding=({'kind':'TOOL_PROBE','tool_name':'lean','executable_sha256':a.LEAN_SHA,'driver_sha256':contract['source_sha256']}if probe else dict(spec['source_binding']))
            if binding['kind']=='GENERATED_BY_ORIGINAL':binding['generated_sha256']=inputs[0]['actual_sha256']
            log=('SYNTHETIC CHILD\n'+'\n'.join(spec.get('required_diagnostics',[]))+'\n').encode()
            row={'id':'probe-'+str(index)if probe else spec['id'],'index':index,'probe':probe,'recipe':recipe,'replay_id':invocation['replay_id'],
                'parent_stage_id':invocation['parent_stage_id'],'argv':spec['argv'],'cwd':spec['cwd'],'timeout_seconds':spec['timeout_seconds'],
                'capture':spec['capture'],'stdin':{'mode':'INHERITED_NO_INPUT','data_sha256':None},'environment_sha256':a.sha(b'SYNTHETIC ENVIRONMENT'),
                'source_binding':binding,'input_bindings':inputs,'source_hashes':source_hashes,
                'started_at':instant(1+3*(index if probe else index+len(contract.get('tool_probes',[])))),
                'ended_at':instant(2+3*(index if probe else index+len(contract.get('tool_probes',[])))),
                'terminal':'COMPLETED','exit_code':spec.get('expected_exit_code',0),'log_sha256':a.sha(log),'stream_hashes':{},
                'output_hashes':{path:a.sha(('SYNTHETIC OUTPUT '+path).encode())for path in spec.get('outputs',[])},'log_file':name+'.log'}
            streams={}
            if spec['capture']=='SEPARATE_BYTES':
                streams={'stdout':log.hex(),'stderr':''};row['stream_hashes']={'stdout':a.sha(log),'stderr':a.sha(b'')}
            # Additive capture fields are conditional so the same tests distinguish old/new code.
            if hasattr(a,'d04_replacement_evidence'):
                row['replacement_bindings']=[]
                for replacement in spec.get('replace_fresh_predecessor',[]):
                    key=(replacement.get('producer_recipe')or recipe,replacement['producer'],replacement.get('predecessor_path',replacement['path']))
                    prior=producers[key]
                    row['replacement_bindings'].append({**replacement,'actual_sha256':prior['sha256'],'producer_capture_sha256':prior['record']})
            item={'record':row,'record_file':name+'.json','record_file_sha256':a.sha(a.d04_record_bytes(row)),'log_hex':log.hex(),'stream_hex':streams}
            invocation['capture_records'].append(item)
            if row['exit_code']==0:
                for path,value in row['output_hashes'].items():producers[(recipe,row['id'],path)]={'sha256':value,'record':a.canonical(row)}
    refresh(a,invocation)
    parent={'id':invocation['parent_stage_id'],'terminal':'COMPLETED','exit_code':0,'log_sha256':invocation['parent_log_sha256'],
        'started_at':instant(0),'ended_at':instant(3*(len(contract['children'])+len(contract.get('tool_probes',[])))+1)}
    return invocation,parent

def refresh(a, invocation):
    manifest={}
    if invocation['trace_launch'] is not None:manifest['LAUNCH.json']=a.sha(a.d04_record_bytes(invocation['trace_launch']))
    for item in invocation['capture_records']:
        row=item['record'];item['record_file_sha256']=a.sha(a.d04_record_bytes(row));manifest[item['record_file']]=item['record_file_sha256']
        if item['log_hex']is not None:manifest[row['log_file']]=a.sha(bytes.fromhex(item['log_hex']))
        for key,value in item['stream_hex'].items():manifest[item['record_file'][:-5]+'.'+key+'.log']=a.sha(bytes.fromhex(value))
    invocation['trace_manifest']=manifest;invocation['trace_sha256']=a.canonical(manifest)if manifest else None

def qualify(a,invocation,plan):
    """Synthetic source-shaped normalized data, never a claim of source execution."""
    recipe=invocation['recipe'];contract=a.d04_contracts()['recipes'][recipe]
    summaries={
        't07-criterion-translated-v1':{'tests':44,'repair_cases':393216,'installation_cases':4096,'source_bytes':3013},
        't07-composition-packaging-translated-v1':{'packaging_tests':4},
        't07-composition-original-v1':{'native_assertions':88,'wrapper_tests':7,'finite_cases':{'revocation':80,'cancellation':60,'open_withheld':20,'two_batch_taint_sets':5,'macro_attempts':40},'source_bytes':3013},
        't07-composition-review-translated-v1':{'native_assertions':25,'monotonicity_readbacks':3},
        't07-composition-serial-mutations-v1':{'runtime_mutants':6,'actual_driver_processes':66},
        't07-covering-translated-v1':{'status':'PASS','author_mutations_rejected':6,'independent_primary_mutations_rejected':6,'lean_sha256':a.LEAN_SHA,
            'mathlib_revision':'c44e0c8ee63ca166450922a373c7409c5d26b00b','normal_and_optimized_semantic_results_match_archived_evidence':True,
            'immutable_payload_before_after':True,'successful_compiler_logs_clean':True}}
    children=[]
    for item in invocation['capture_records']:
        row=item['record']
        if row['probe']or(recipe=='t07-composition-serial-mutations-v1'and not row['id'].endswith('/runtime')):continue
        children.append({key:row[key]for key in ['id','log_sha256','terminal','exit_code']})
    result={'children':children,'summary':copy.deepcopy(contract.get('fixed_summary')or summaries[recipe])}
    if recipe in {'t07-criterion-translated-v1','t07-covering-translated-v1','t07-composition-original-v1','t07-composition-review-translated-v1'}:
        result['objects']={Path(path).stem:value for item in invocation['capture_records']for path,value in item['record']['output_hashes'].items()if path.endswith('.olean')and item['record']['exit_code']==0}
    if 'normalized_source_hashes'in contract:result['source_hashes_read_back']=contract['normalized_source_hashes']
    normalization={'recipe':recipe,'normalizer_assets':{name:row['sha256']for name,row in a.d04_contracts()['adapter_assets'].items()if name.startswith('v5_d04_normalizers_')},'result':result}
    invocation.update(normalization=normalization,normalization_sha256=a.canonical(normalization),qualified_objects=a.d04_expected_objects(plan,invocation))
    return invocation

def family_evidence(a,plan):
    producers={};invocations=[];observations=[];stages={};output_hashes={};captured={}
    next_time=datetime.fromisoformat('2026-10-05T12:00:00+00:00')
    stamp=lambda value:value.isoformat().replace('+00:00','Z')
    for sid,stage in plan['stages'].items():
        if stage['argv'][0]=='{builtin:observe-child}':
            child=captured[tuple(stage['argv'][1:])]
            stages[sid]={'id':sid,**{key:child[key]for key in ['terminal','exit_code','log_sha256']},'started_at':stamp(next_time),'ended_at':stamp(next_time+timedelta(seconds=1))}
            next_time+=timedelta(seconds=2)
            observations.append({**child,'stage_id':sid,'observed_at':stages[sid]['ended_at']})
        elif stage['driver_id']:
            recipe=plan['drivers'][stage['driver_id']]['recipe'];invocation,parent=make_capture(a,recipe,producers=producers,start=stamp(next_time))
            next_time=datetime.fromisoformat(parent['ended_at'].replace('Z','+00:00'))+timedelta(seconds=1)
            qualify(a,invocation,plan);invocations.append(invocation);stages[sid]=parent;output_hashes.update(invocation['qualified_objects'])
            children,_=a.d04_observations(invocation,plan,parent);captured.update(children)
    return {'driver_invocations':invocations,'child_observations':observations,'runner_sha256':a.sha(Path(a.__file__).read_bytes()),'output_hashes':output_hashes},stages
