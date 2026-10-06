"""Exact selector/G1 family adapter. Candidate; no admission is implied.

Only the three code-owned descriptors dispatch here. Original drivers are run
unchanged in a separate process. Pure readers and traces do not themselves
establish Lean semantics. Current dependency receipts, captured children,
unchanged source/object/cache trees and checked target closure are all required.
"""
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager
import copy
import importlib.util
import json
import os
import re
import runpy
import shutil
import subprocess
import sys

SELECTOR_G1_CATALOG_SHA256 = '1c04885e6a997afd24e831315a1bd313fbaef693c2d682402db0637407b55344'
SELECTOR_G1_RECIPES = {'t09-selector-original-v2':'selector','t09-g1-author-original-v2':'g1','t09-g1-review-original-v2':'g1-review'}
SELECTOR_G1_IDS = {'d06-selector':'selector','d08-g1':'g1','d08-g1-review':'g1-review'}
SELECTOR_G1_GIT_SHA256 = '2a8c18fbf43da9f692d75474c72bea9dfd796c260b0f3dfe456376abc3bbd668'
SELECTOR_G1_CORE_SUITE_SHA256 = 'a775764e1ba9d626f9eebaf6642428769a1016f9d779c1832d1f0b3814722128'
SELECTOR_G1_CORE_PRIOR_SHA256 = 'a83603f4b746920aab44f8c7a599298c49a7750327811a81773fef641254166c'
SELECTOR_G1_CORE_RESULT_SHA256 = '260dd5a450a9d1874562aa7fbc696a8567a7f62e9c16c03d56433c772a116958'
SELECTOR_G1_CORE_TRACE_SHA256 = '76719061dcee7c07eac0a76f72e184de2fb945d63a1136d1ad704894f265284e'
SELECTOR_G1_CORE_CONTINUATION_SHA256 = '25209b12b33e4728ab682644b0a111ab0bc3df27d4f23bd271c974381264bb43'
SELECTOR_G1_CORE_CONTINUATION_CANONICAL = '9c5c52621469fab8373b8234faf5a3cf8c3e48e385b0e21bbe2e5a29f5f44c53'
SELECTOR_G1_CORE_RETAINED_TREE_SHA256 = '748a5d8d993637c120afc3b0998bf0109b5c6658c7f2de0ff29f426859a524a8'
# Root/D03 must add the exact successful *current* cold-author receipt after
# admission/execution. No descriptor, receipt field, path or CLI flag can add it.
# canonical receipt digest -> exact receipt-file and retained whole-run digests.
SELECTOR_G1_CURRENT_AUTHOR_RECEIPTS = {'da3e904d18f5656add78cf079f4d7879e7f7ab06b7089a50eb03cb3800ccb46d': {'receipt_file_sha256': '1b39b168f89d8b7575131a27a0697ec22b2c1d4bc333b506f1a6f3516a01b152', 'retained_tree_sha256': '3bf5bbe70c697b581aecc7dee47f25e758afdca8bbed243b1ca84594e4819b29'}}
SELECTOR_G1_REVIEWED_EXECUTORS = frozenset({('ab06a34e10487b396cf83b3e07eba135ad821dab1e91b25cad0780e1b444a8f0', 'f2704f521f5c55cd3a0866b4e3f98d520dd57daa782e1f052b972d7de8b05d87')})
SELECTOR_G1_SCHEMA = 'orthemology-v5-replay-evidence-v2'
SELECTOR_G1_POLICY = 'EXACT_ORIGINAL_COLD_OR_EXPLICIT_CURRENT_DEPENDENCY_REUSE'
SELECTOR_G1_HELPERS = {
    'replay_selector_g1_selector':'928788441b812eb0162e25638329c6650a7246ffaca2d2796ad491af1728517d',
    'replay_selector_g1_g1':'0a83738d934e7d2b307dc921a87430ca7da0f67842e7bee456f8bd7a763c6f77',
    'replay_selector_g1_normalizers':'476b25e264ed332cc6f514f6735ebb32c2f8800b849b04d5464fbbaec3aca23c',
}


def selector_g1_catalog(api):
    path=api.no_symlinks(Path(__file__).with_name('replay_selector_g1_catalog.json'))
    raw=path.read_bytes()
    api.require(api.sha(raw)==SELECTOR_G1_CATALOG_SHA256,'Changed code-owned selector/G1 catalogue')
    def pairs(items):
        result={}
        for key,value in items:
            api.require(key not in result,'Duplicate JSON key');result[key]=value
        return result
    def invalid(value):raise ValueError('Nonfinite JSON number')
    return json.loads(raw.decode('utf-8'),object_pairs_hook=pairs,parse_constant=invalid)



def selector_g1_handles(suite):
    if not isinstance(suite,dict):return False
    if suite.get('id') in SELECTOR_G1_IDS:return True
    replay=suite.get('replay');drivers=replay.get('drivers') if isinstance(replay,dict) else None
    return isinstance(drivers,list) and any(isinstance(d,dict) and d.get('recipe') in SELECTOR_G1_RECIPES for d in drivers)


class _SelectorG1AdapterView:
    """Use the calling adapter globals even under unregistered importlib loads."""
    def __init__(self,namespace):object.__setattr__(self,'_namespace',namespace)
    def __getattr__(self,name):
        try:return self._namespace[name]
        except KeyError:raise AttributeError(name) from None
    def __setattr__(self,name,value):self._namespace[name]=value


def selector_g1_adapter_view(namespace):return _SelectorG1AdapterView(namespace)


@contextmanager
def selector_g1_helpers(api):
    old={name:sys.modules.get(name) for name in SELECTOR_G1_HELPERS};loaded={}
    try:
        for name,pin in SELECTOR_G1_HELPERS.items():
            path=api.no_symlinks(Path(__file__).with_name(name+'.py'));raw=path.read_bytes()
            api.require(api.sha(raw)==pin,'Changed reviewed family helper')
            spec=importlib.util.spec_from_file_location(name,path)
            module=importlib.util.module_from_spec(spec);sys.modules[name]=module
            exec(compile(raw,str(path),'exec'),module.__dict__)
            loaded[name.rsplit('_',1)[-1]]=module
        yield loaded
    finally:
        for name,value in old.items():
            if value is None:sys.modules.pop(name,None)
            else:sys.modules[name]=value



def selector_g1_check_binding(api,binding,sources):
    api.require(isinstance(binding,dict),'Source binding must be an object')
    kind=binding.get('kind')
    fields={'ORIGINAL_SOURCE':{'kind','source_id','source_sha256'},
            'ARCHIVE_MEMBER':{'kind','archive_source_id','archive_sha256','member','source_sha256'},
            'GENERATED_BY_ORIGINAL':{'kind','source_id','source_sha256','generated_sha256','derivation_id'},
            'TOOL_PROBE':{'kind','tool_name','executable_sha256','driver_sha256'}}
    api.require(kind in fields,'Unknown source binding variant');api.keys(binding,fields[kind])
    if kind in {'ORIGINAL_SOURCE','GENERATED_BY_ORIGINAL'}:
        sid=binding['source_id'];api.require(sid in sources,'Invented original source owner')
        api.require(binding['source_sha256']==sources[sid]['original_sha256'],'Original owner source differs')
        if kind=='GENERATED_BY_ORIGINAL':api.digest(binding['generated_sha256']);api.identifier(binding['derivation_id'])
    elif kind=='ARCHIVE_MEMBER':
        sid=binding['archive_source_id'];api.require(sid in sources,'Invented archive owner')
        api.require(binding['archive_sha256']==sources[sid]['original_sha256'],'Archive owner differs')
        api.relative(binding['member']);api.digest(binding['source_sha256'])
    else:
        api.require(binding['tool_name'] in {'lean','git','python'},'Unknown metadata probe tool')
        api.digest(binding['executable_sha256']);api.digest(binding['driver_sha256'])
    return binding


def selector_g1_validate_suite(api,suite,sources,root):
    cat=selector_g1_catalog(api);family=SELECTOR_G1_IDS.get(suite.get('id'))
    api.require(family is not None,'Unknown selector/G1 suite')
    definition=cat['families'][family]
    api.require(api.canonical(suite)==definition['suite_sha256'] and suite==definition['suite'],'Unreviewed selector/G1 descriptor')
    selected=set(suite['source_ids'])|{definition['driver_source_id']}|{r['source_id'] for r in definition['archives'].values()}
    selected|={s['source']['source_id'] for s in definition['contract']['stages'] if s['source']['source_id']}
    selected|={s['source']['source_id'] for s in definition['contract'].get('auxiliary_children',[])}
    for sid in selected:
        api.require(sid in sources and sid in cat['sources'],'Missing code-owned source identity')
        api.require(sources[sid]==cat['sources'][sid],'Changed original/projection/source ancestry')
    contents={sid:api.public_bytes(root,sources[sid]) for sid in suite['source_ids']}
    api.require({sid:api.sha(data) for sid,data in contents.items()}==definition['source_hashes'],'Changed selected source bytes')
    replay=suite['replay'];files=api.indexed(replay['files'],'source_id')
    for target in suite['targets']:
        api.require(target['declaration'].encode() in contents[target['source_id']] and api.sha(target['declaration'].encode())==target['target_sha256'],'Changed exact target text')
    return {'selector_g1_family':family,'definition':definition,'files':files,'file_paths':{f['path']:f for f in files.values()},
            'contents':contents,'modules':api.indexed(replay['modules'],'name'),'official':api.indexed(replay['official_imports'],'module'),
            'drivers':api.indexed(replay['drivers']),'inputs':api.indexed(replay['external_inputs']),'input_manifests':{},'fixtures':{},
            'stages':api.indexed(replay['stages']),'targets':api.indexed(replay['target_names'],'target_id'),
            'packages':api.indexed(replay['packages'],'name'),'build_roots':replay['build_roots']}


def selector_g1_audit_source(api,targets):
    # Lean name quotations are literal Name values: `_root_.Nat contains the
    # actual `_root_ component. Root-qualify elaborated #check/#print syntax,
    # while leaving lookup Name values exactly equal to the declared names.
    for row in targets:api.lean_name(row['name']);api.lean_name(row['module'])
    body=api._audit_source(targets)
    for row in targets:
        name=row['name'];body=body.replace('#check @'+name+'\n','#check @_root_.'+name+'\n')
        body=body.replace('#print axioms '+name+'\n','#print axioms _root_.'+name+'\n')
    body=body.replace('open Lean Elab Command','open _root_.Lean _root_.Lean.Elab.Command')
    body=body.replace('V5SuccessorCheckedAudit.audit `','_root_.V5SuccessorCheckedAudit.audit `')
    api.require('scheduled' in body and 'env.checked.get.find?' in body and 'UNSAFE_OR_PARTIAL_DEPENDENCY' in body,'Changed required safe auditor')
    return body


def selector_g1_capture_call(api,original_run,trace,index,event,argv,kwargs):
    """Capture an actual child call; never replace its stream or return object."""
    trace=api.no_symlinks(trace);record_path=api.path_in(trace,f'{index:04}.json');log=api.path_in(trace,f'{index:04}.log')
    api.require(type(index) is int and index>=0 and not record_path.exists() and not log.exists(),'Trace overwrite or bad index')
    inherited=event.get('profile')=='INHERITED_STDOUT_CHECK'
    file_capture=event.get('capture')=='FILE'
    kind='INHERITED_PARENT_STDOUT' if inherited else 'SOURCE_PRESCRIBED_FILE' if file_capture else 'CAPTURED_PIPE'
    row={'id':event['id'],'index':index,'argv':list(argv),'cwd':str(Path(kwargs.get('cwd',Path.cwd())).absolute()),
         'explicit_cwd':'cwd' in kwargs,'started_at':api.utc(),'ended_at':None,'terminal':'RUNNING','exit_code':None,
         'capture_kind':kind,'log_sha256':None,'source_binding':event['source_binding'],'output_hashes':{},
         'metadata_only':bool(event.get('readonly')),'timeout_seconds':kwargs.get('timeout')}
    api.write_json(record_path,row)
    descriptor=None
    if file_capture:
        stream=kwargs['stdout'];descriptor=os.fstat(stream.fileno());named=api.no_symlinks(stream.name).stat()
        api.require((descriptor.st_dev,descriptor.st_ino)==(named.st_dev,named.st_ino),'Original capture descriptor was redirected')
    def finish(terminal,code,stdout):
        if inherited:
            api.require(stdout is None,'Inherited stdout was fabricated')
        else:
            if file_capture:
                stream.flush();named=api.no_symlinks(stream.name).stat()
                api.require((descriptor.st_dev,descriptor.st_ino)==(named.st_dev,named.st_ino),'Original capture descriptor changed')
                raw=Path(stream.name).read_bytes()
            else:raw=stdout.encode('utf-8') if isinstance(stdout,str) else stdout or b''
            api.require(isinstance(raw,bytes),'Nonbyte captured stream')
            log.write_bytes(raw);row['log_sha256']=api.sha(raw)
        for key in ('object_path','c_output'):
            path=event.get(key)
            if path is not None and api.no_symlinks(path).is_file():row['output_hashes'][path]=api.sha(Path(path).read_bytes())
        row.update(ended_at=api.utc(),terminal=terminal,exit_code=code);api.write_json(record_path,row)
    try:result=original_run(argv,**kwargs)
    except subprocess.CalledProcessError as error:
        valid=type(error.returncode) is int and 0<=error.returncode<124
        finish('COMPLETED' if valid else 'INTERRUPTED',error.returncode if valid else None,error.stdout)
        raise
    except (subprocess.TimeoutExpired,KeyboardInterrupt) as error:
        finish('TIMEOUT' if isinstance(error,subprocess.TimeoutExpired) else 'INTERRUPTED',None,getattr(error,'stdout',None))
        raise
    except BaseException:
        finish('INTERRUPTED',None,None);raise
    api.require(type(result.returncode) is int,'Boolean/noninteger process exit')
    valid=0<=result.returncode<124
    finish('COMPLETED' if valid else 'INTERRUPTED',result.returncode if valid else None,result.stdout)
    return result


def selector_g1_inventory(api,root):
    root=api.no_symlinks(root);api.require(root.is_dir(),'Input tree is absent');result={}
    for p in sorted(root.rglob('*')):
        api.no_symlinks(p)
        if p.is_file():result[p.relative_to(root).as_posix()]=api.sha(p.read_bytes())
        else:api.require(p.is_dir(),'Nonregular input/output file')
    return result


def selector_g1_replace(value,old,new):
    if isinstance(value,str):return value.replace(str(old),str(new))
    if isinstance(value,list):return [selector_g1_replace(x,old,new) for x in value]
    if isinstance(value,dict):return {selector_g1_replace(k,old,new):selector_g1_replace(v,old,new) for k,v in value.items()}
    return value


def selector_g1_events(api,family,context):
    """Derive complete ordered calls from exact originals without importing them."""
    cat=selector_g1_catalog(api);definition=cat['families'][family]
    output=Path(context['out']);probe=output.parent/'_selector_g1_absent_plan_namespace'
    api.require(not probe.exists(),'Planning namespace unexpectedly exists')
    roots={k:Path(v) for k,v in context['roots'].items()};archives={k:Path(v) for k,v in context['archives'].items()}
    common=[Path(context[n]) for n in ('lean','mathlib','python','cwd')]
    math=common[1]
    cache_plan={'packages':api.indexed(definition['suite']['replay']['packages'],'name'),'official':api.indexed(definition['suite']['replay']['official_imports'],'module')}
    selector_g1_verified_library_paths(api,cache_plan,{'mathlib':math})
    with selector_g1_helpers(api) as helper:
        if family=='selector':
            lean,mathlib,python,cwd=common
            plan=helper['selector'].prepare(api,roots['selector'],probe,Path(context['dependency_run'])/'original',lean,mathlib,python,archives['selector-archive'],archives['core-archive'],archives['literal-archive'],cwd)
        elif family=='g1':plan=helper['g1'].prepare_author(api,archives['g1-archive'],roots['g1'],probe,*common)
        else:plan=helper['g1'].prepare_review(api,archives['g1-archive'],archives['g1-review-archive'],roots['g1'],roots['g1-review'],probe,Path(context['dependency_run'])/'original',*common)
    plan=selector_g1_replace(plan,probe,output)
    sources=cat['sources']
    def original(packet,member,digest):
        archive=definition['archives'][packet+'-archive'];prefix=cat['families'][packet]['prefix'] if packet in cat['families'] else ''
        full=prefix+member
        selected=[r for r in sources.values() if r['origin_archive_sha256']==archive['sha256'] and r['member_chain'][-1]==full and r['original_sha256']==digest]
        if selected:return {'kind':'ORIGINAL_SOURCE','source_id':selected[0]['id'],'source_sha256':digest}
        return {'kind':'ARCHIVE_MEMBER','archive_source_id':archive['source_id'],'archive_sha256':archive['sha256'],'member':full,'source_sha256':digest}
    for index,event in enumerate(plan['events']):
        event.setdefault('id','probe-'+str(index));event.setdefault('cwd',context['cwd']);event.setdefault('explicit_cwd',False)
        if event.get('readonly'):
            if event.get('profile')=='INHERITED_STDOUT_CHECK':
                event['source_binding']=original('g1','replay.py',selector_g1_driver_sha(cat,'g1'))
            else:
                name='git' if event['argv'][0]=='git' else 'lean'
                event['source_binding']={'kind':'TOOL_PROBE','tool_name':name,'executable_sha256':SELECTOR_G1_GIT_SHA256 if name=='git' else api.LEAN_SHA,'driver_sha256':plan['driver_sha256']}
        else:
            source=Path(event['source_path']);generated=plan.get('derivations',{}).get(source.relative_to(output).as_posix()) if source.is_relative_to(output) else None
            if generated:
                owner=generated['owner'];packet=family
                if owner.startswith('author/'):packet='g1';owner=owner[len('author/'):]
                elif owner.startswith('review/'):packet='g1-review';owner=owner[len('review/'):]
                binding=original(packet,owner,generated['owner_sha256'])
                api.require(binding['kind']=='ORIGINAL_SOURCE','Generated source has no actual retained owner')
                event['source_binding']={**binding,'kind':'GENERATED_BY_ORIGINAL','generated_sha256':event['source_sha256'],'derivation_id':event['id']}
            elif family=='selector' and source.is_relative_to(output):
                if event['id'] in {'finite-controls','original-census-controls'}:
                    member='controls/finite_controls.py' if event['id']=='finite-controls' else 'controls/check_original_replay_guards.py'
                    event['source_binding']=original('selector',member,event['source_sha256'])
                else:event['source_binding']=original('literal',source.relative_to(output/'dependencies/literal').as_posix(),event['source_sha256'])
            else:
                packet=next(k for k,p in roots.items() if source.is_relative_to(p))
                event['source_binding']=original(packet,source.relative_to(roots[packet]).as_posix(),event['source_sha256'])
        selector_g1_check_binding(api,event['source_binding'],sources)
    # replace() creates separate copies of event dictionaries; make child rows
    # refer to the enriched exact physical plan by ID, preserving source order.
    by={e['id']:e for e in plan['events']};plan['children']=[by[e['id']] for e in plan['children']]
    plan['event_plan_sha256']=api.canonical(plan['events'])
    return plan


def selector_g1_driver_sha(cat,family):return cat['families'][family]['contract']['driver']['sha256']


@contextmanager
def selector_g1_trace_environment(api,driver,arguments,invoke):
    old_run=subprocess.run;old_argv=sys.argv[:];old_path=sys.path[:];old_modules=dict(sys.modules)
    old_cwd=Path.cwd();old_env=dict(os.environ);old_bytecode=sys.dont_write_bytecode
    try:
        subprocess.run=invoke;sys.argv=[str(driver),*arguments];sys.path.insert(0,str(driver.parent));sys.dont_write_bytecode=True
        # Never use a previously imported producer helper from another packet.
        for name in ('verify_dependency_identity','verify_artifact','selector_external_dependency_identity'):sys.modules.pop(name,None)
        yield
    finally:
        subprocess.run=old_run;sys.argv=old_argv;sys.path[:]=old_path;sys.dont_write_bytecode=old_bytecode
        os.chdir(old_cwd);os.environ.clear();os.environ.update(old_env)
        for name in list(sys.modules):
            if name not in old_modules:sys.modules.pop(name,None)
        for name,value in old_modules.items():sys.modules[name]=value


def selector_g1_trace_main(api,family,context_file):
    api.require(family in {'selector','g1','g1-review'} and not sys.flags.optimize,'Original drivers require normal Python')
    context=api.read_json(context_file);api.keys(context,{'family','roots','archives','out','dependency_run','lean','mathlib','python','cwd','trace','arguments','driver'})
    api.require(context['family']==family and str(Path.cwd().resolve())==context['cwd'],'Changed original inherited working directory')
    api.require(not any(k.startswith('LD_') or k in {'LEAN_SYSROOT','LEAN_SRC_PATH','PYTHONOPTIMIZE'} for k in os.environ),'Unreviewed original driver environment')
    api.require(api.sha(Path(sys.executable).read_bytes())==selector_g1_catalog(api)['python']['executable_sha256'],'Wrong tracing interpreter')
    git=Path(shutil.which('git') or '');api.require(git.is_file() and api.sha(git.read_bytes())==SELECTOR_G1_GIT_SHA256,'Changed original Git probe executable')
    plan=selector_g1_events(api,family,context)
    driver=api.no_symlinks(context['driver']);api.require(api.sha(driver.read_bytes())==plan['driver_sha256'],'Original driver changed')
    expected=selector_g1_source_argv(api,family,context)[3:]
    api.require(context['arguments']==expected,'Changed original arguments')
    api.require(not api.no_symlinks(context['out']).exists(),'Original output must be absent')
    trace=api.no_symlinks(context['trace']);api.require(not trace.exists(),'Trace must be absent');trace.mkdir(parents=True)
    api.write_json(trace/'PLAN.json',{'family':family,'event_plan_sha256':plan['event_plan_sha256']})
    position=0;original_run=subprocess.run
    with selector_g1_helpers(api) as helpers:
        def invoke(argv,*args,**kwargs):
            nonlocal position
            api.require(position<len(plan['events']),'Unexpected extra original child')
            event=plan['events'][position]
            helper=helpers['selector'] if family=='selector' else helpers['g1']
            helper.validate_call(api,event,argv,args,kwargs,Path.cwd())
            # Metadata probes also inherit exactly the source launch cwd.
            api.require(str(Path.cwd().resolve())==context['cwd'],'Original metadata inherited cwd changed')
            index=position;position+=1
            return selector_g1_capture_call(api,original_run,trace,index,event,argv,kwargs)
        try:
            with selector_g1_trace_environment(api,driver,context['arguments'],invoke):runpy.run_path(str(driver),run_name='__main__')
            api.require(position==len(plan['events']),'Original omitted required calls')
        finally:api.write_json(trace/'TERMINAL.json',{'observed_calls':position,'required_calls':len(plan['events']),'finished_at':api.utc()})
    return 0


def selector_g1_source_argv(api,family,context):
    definition=selector_g1_catalog(api)['families'][family]
    mapping={'tool:python':context['python'],'driver:'+family:context['driver'],'tool:lean-bin':str(Path(context['lean']).parent),
             'dependency:mathlib':context['mathlib'],'out':str(Path(context['out']).parent),'dependency-run':context['dependency_run'] or ''}
    mapping.update({'input:'+k:v for k,v in context['archives'].items()})
    mapping.update({'archive:'+k+'-archive':v for k,v in context['roots'].items()})
    return [api._expand(v,mapping) for v in definition['suite']['replay']['stages'][0]['argv']]


def selector_g1_collect(api,family,context,parent,output):
    """Join full original records to actual calls; no success from filenames."""
    cat=selector_g1_catalog(api);definition=cat['families'][family];plan=selector_g1_events(api,family,context)
    out=Path(context['out']);trace=Path(context['trace']);events=plan['events'];output=Path(output)
    api.require(parent['terminal']=='COMPLETED' and type(parent['exit_code']) is int and parent['exit_code']==0,'Original parent did not succeed')
    expected={f'{i:04}.json' for i in range(len(events))}|{'PLAN.json','TERMINAL.json'}
    api.require({p.name for p in trace.glob('*.json')}==expected,'Incomplete/extra physical child trace')
    api.require(api.read_json(trace/'PLAN.json')=={'family':family,'event_plan_sha256':plan['event_plan_sha256']},'Changed physical plan')
    terminal=api.read_json(trace/'TERMINAL.json')
    api.require(type(terminal['observed_calls']) is int and terminal['observed_calls']==terminal['required_calls']==len(events),'Original physical census incomplete')
    roots={'root:'+k:Path(v) for k,v in context['roots'].items()}
    roots.update({'out':out,'tool:lean':Path(context['lean']),'tool:python':Path(context['python']),'lean-root':Path(context['lean']).parent.parent,'dependency:mathlib':Path(context['mathlib'])})
    roots.update({'root:literal':out/'dependencies/literal','root:core':out/'dependencies/core'} if family=='selector' else {})
    physical=[];observations=[];objects={};last=parent['started_at'];accepted=[]
    contract=definition['contract'];childspec={s['id']:s for s in contract['stages']};aux={s['id']:s for s in contract.get('auxiliary_children',[])}
    with selector_g1_helpers(api) as helpers:
        normalized=helpers['normalizers'].normalize(contract,out,roots)
        api.require(normalized['original_full_terminal_present'] and not normalized['resource_children'] and not normalized['not_run_children'],'Original full terminal/controls not established')
        original=api.read_json(out/'RESULT.json')
        if family=='g1':
            api.require(original['public_manifest_sha256']==helpers['g1'].PUBLIC_MANIFEST and original['source_manifest_sha256']==helpers['g1'].SOURCE_MANIFEST and original['custom_objects_reused'] is False,'Author is not exact current cold v4')
        elif family=='g1-review':
            api.require(original['source_identical_command_preserving_v2_bridge'] is False and original['core_packet_public_manifest_sha256']==helpers['g1'].PUBLIC_MANIFEST,'Historical G1 v2 bridge is forbidden')
        for i,event in enumerate(events):
            row=api.read_json(trace/f'{i:04}.json')
            api.require(row['index']==i and type(row['index']) is int and row['id']==event['id'] and row['argv']==event['argv'] and row['cwd']==context['cwd'] and row['explicit_cwd'] is False,'Captured physical call identity/cwd differs')
            api.require(last<=row['started_at']<=row['ended_at']<=parent['ended_at'],'Child interval is outside actual parent/order');last=row['ended_at']
            api.require(row['source_binding']==event['source_binding'] and row['metadata_only'] is bool(event.get('readonly')),'Physical source or metadata role differs')
            selector_g1_check_binding(api,row['source_binding'],cat['sources'])
            api.require(row['terminal']=='COMPLETED' and type(row['exit_code']) is int and 0<=row['exit_code']<124,'Physical child is resource-inconclusive')
            raw=None
            if event.get('profile')=='INHERITED_STDOUT_CHECK':
                api.require(row['capture_kind']=='INHERITED_PARENT_STDOUT' and row['log_sha256'] is None and not (trace/f'{i:04}.log').exists() and row['exit_code']==0,'Unsuccessful/fabricated inherited-stdout preflight')
            else:
                raw=(trace/f'{i:04}.log').read_bytes();api.require(api.sha(raw)==row['log_sha256'],'Physical captured log changed')
            if event.get('readonly'):
                api.require(row['exit_code']==0 and row['output_hashes']=={},'Metadata probe has failure/object credit')
                classification='METADATA_ONLY'
            else:
                original_log=Path(event['log']).read_bytes()
                helper=helpers['selector'] if family=='selector' else helpers['g1']
                result=helper.classify_stage(api,event,row,raw,original_log,*([accepted] if family!='selector' else []))
                api.require(result['outcome'] in {'ACCEPT','REJECT'},'Original child not semantically established')
                classification=result['outcome']
                if classification=='ACCEPT':accepted.append(event['id'])
                expected_outputs={}
                for key in ('object_path','c_output'):
                    path=event.get(key)
                    if path is not None:
                        if classification=='REJECT':api.require(not Path(path).exists(),'Rejected child emitted an artifact')
                        else:expected_outputs[path]=api.sha(api.no_symlinks(path).read_bytes())
                api.require(row['output_hashes']==expected_outputs,'Physical output census/hash differs')
                objects.update({Path(p).relative_to(output).as_posix():h for p,h in expected_outputs.items()})
                spec=childspec.get(event['id'],aux.get(event['id']))
                observed={'source_child_id':event['id'],'physical_child_id':event['id'],'source_binding':event['source_binding'],
                          'mode':'NONEXECUTING_OBSERVATION','actual_outcome':classification,'terminal':row['terminal'],'exit_code':row['exit_code'],
                          'log_sha256':api.sha(original_log),'physical_record_sha256':api.canonical(row),
                          'original_record_sha256':api.canonical(next(r for r in original['runs'] if r.get('label',r.get('module'))==event['id'])) if event['id'] in childspec else None,
                          'output_hashes':{Path(p).relative_to(output).as_posix():h for p,h in expected_outputs.items()},
                          'credit':'FINITE_ONLY' if event['id'] in aux else 'SOURCE_CHILD'}
                observations.append(observed)
            physical.append(selector_g1_public_child(api,row,context,parent['log_sha256'],classification))
            if not event.get('readonly'):observations[-1]['physical_record_sha256']=api.canonical(physical[-1])
        # The original normalizer checks only .olean entries. Reject auxiliary
        # foreign files in every actual formal build namespace as well.
        formal_roots={}
        for spec in contract['stages']:
            for obj in spec['objects']:
                path=obj['path'];suffix=obj['module'].replace('.','/')+'.olean';base=path[:-len(suffix)].rstrip('/')
                formal_roots.setdefault(base,set())
                if spec['expected_exit_code']==0:formal_roots[base].add(suffix)
        for base,names in formal_roots.items():
            actual=set(selector_g1_inventory(api,out/base))
            if base=='codegen':names=names|{Path(s['c_output']).name for s in contract['stages'] if s.get('c_output')}
            api.require(actual==names,'Foreign or missing file in formal build namespace')
    return {'original_result':original,'original_result_sha256':api.sha((out/'RESULT.json').read_bytes()),
            'normalization_sha256':api.canonical(normalized),'normalized':normalized,'physical_children':physical,'child_observations':observations,
            'output_hashes':objects,'trace_sha256':api._file_hashes(trace),'event_plan_sha256':plan['event_plan_sha256'],
            'original_run_count':1,'independent_evidence_increment':0}


def selector_g1_public_child(api,row,context,parent_log,credit):
    substitutions={context['out']:'{original}',context['cwd']:'{project}',context['lean']:'{tool:lean}',
                   context['python']:'{tool:python}',context['mathlib']:'{dependency:mathlib}'}
    substitutions.update({v:'{root:'+k+'}' for k,v in context['roots'].items()})
    if context['dependency_run']:substitutions[context['dependency_run']]='{dependency-run}'
    result=copy.deepcopy(row)
    for old,new in sorted(substitutions.items(),key=lambda x:len(x[0]),reverse=True):result=selector_g1_replace(result,old,new)
    result['output_hashes']={Path(p).relative_to(Path(context['out']).parent).as_posix():h for p,h in row['output_hashes'].items()}
    result.update(parent_log_sha256=parent_log,credit=credit,raw_capture_sha256=api.canonical(row))
    return result


def selector_g1_expected_binding(api,cat,family,spec):
    source=spec['source'];sid=source['source_id']
    if sid is not None:return {'kind':'ORIGINAL_SOURCE','source_id':sid,'source_sha256':source['sha256']}
    basename=source['path'].rsplit('/',1)[-1]
    packet='g1-review' if basename=='ReviewerControls.lean' else 'g1'
    owner='src/CertificateSyntax.lean' if basename=='CertificateSyntax.lean' else 'controls/CertificateFixtures.lean' if basename=='CertificateFixtures.lean' else 'tests/ReviewerControls.lean' if basename=='ReviewerControls.lean' else 'replay.py'
    prefix=cat['families'][packet]['prefix'];archive=cat['families'][packet]['archives'][packet+'-archive']['sha256']
    matches=[s for s in cat['sources'].values() if s['origin_archive_sha256']==archive and s['member_chain'][-1]==prefix+owner]
    api.require(len(matches)==1,'Ambiguous generated source owner')
    selected=matches[0]
    return {'kind':'GENERATED_BY_ORIGINAL','source_id':selected['id'],'source_sha256':selected['original_sha256'],
            'generated_sha256':source['sha256'],'derivation_id':spec['id']}


def selector_g1_expected_physical(api,family):
    cat=selector_g1_catalog(api);definition=cat['families'][family];contract=definition['contract'];events=[]
    def probe(argv,text=True,inherited=False):
        index=len(events);tool='git' if argv[0]=='git' else 'lean'
        binding={'kind':'TOOL_PROBE','tool_name':tool,'executable_sha256':SELECTOR_G1_GIT_SHA256 if tool=='git' else api.LEAN_SHA,'driver_sha256':contract['driver']['sha256']}
        if inherited:
            sid=cat['families']['g1']['driver_source_id'];binding={'kind':'ORIGINAL_SOURCE','source_id':sid,'source_sha256':cat['sources'][sid]['original_sha256']}
        events.append({'id':'probe-'+str(index),'argv':argv,'timeout_seconds':None,'source_binding':binding,'metadata_only':True,
                       'capture_kind':'INHERITED_PARENT_STDOUT' if inherited else 'CAPTURED_PIPE','expected_exit':0,'outputs':[]})
    if family=='g1-review':probe(['{tool:python}','{root:g1}/replay.py','--verify-only'],inherited=True)
    probe(['{tool:lean}','--version'])
    if family!='g1-review':
        for row in cat['toolchain']['packages']:
            root='{dependency:mathlib}'+('' if row['name']=='mathlib' else '/.lake/packages/'+row['name'])
            for args in (['rev-parse','HEAD'],['status','--porcelain','--untracked-files=all'],['ls-files','-z']):probe(['git','-C',root,*args])
    for spec in contract['stages']+contract.get('auxiliary_children',[]):
        argv=[v.replace('{out}','{original}') for v in spec['expected_argv']]
        if family=='selector':argv=[v.replace('{root:literal}','{original}/dependencies/literal') for v in argv]
        code=spec.get('expected_exit_code',0)
        outputs=['original/'+r['path'] for r in spec.get('objects',[]) if code==0]
        if spec.get('c_output'):outputs.append('original/'+spec['c_output'])
        events.append({'id':spec['id'],'argv':argv,'timeout_seconds':spec['budget_seconds'],
            'source_binding':selector_g1_expected_binding(api,cat,family,spec),'metadata_only':False,
            'capture_kind':'SOURCE_PRESCRIBED_FILE' if spec in contract.get('auxiliary_children',[]) else 'CAPTURED_PIPE',
            'expected_exit':code,'outputs':outputs})
    return events


def selector_g1_expected_helpers(api,family):
    cat=selector_g1_catalog(api);driver=selector_g1_driver_sha(cat,family);rows=[]
    def add(argv,tool,log):
        pin=api.LEAN_SHA if tool=='lean' else cat['python']['executable_sha256'] if tool=='python' else SELECTOR_G1_GIT_SHA256
        rows.append({'argv':argv,'cwd':'{out}','timeout_seconds':30,'log_path':log,
                     'source_binding':{'kind':'TOOL_PROBE','tool_name':tool,'executable_sha256':pin,'driver_sha256':driver}})
    for key,tool in [('lean','lean'),('python','python'),('lean-bin','lean')]:add(['{tool:'+tool+'}','--version'],tool,'logs/tool-'+key+'.log')
    for row in cat['toolchain']['packages']:
        root='{dependency:mathlib}'+('' if row['name']=='mathlib' else '/.lake/packages/'+row['name'])
        add(['{tool:git}','-C',root,'rev-parse','HEAD'],'git','logs/'+row['name']+'-head.log')
        add(['{tool:git}','-C',root,'status','--porcelain','--untracked-files=no'],'git','logs/'+row['name']+'-clean.log')
    return rows


def selector_g1_dependency_identity(api,family,receipt,suite,sources,root):
    """Offline identity gate; disk captures/objects are a separate mandatory join."""
    api.require(family in {'selector','g1-review'},'This family has no reusable custom dependency')
    api.require(receipt.get('outcome')=='QUALIFIED_DECLARED_SUITE' and receipt.get('proof_scope')=='DECLARED_SUITE' and type(receipt.get('exit_code')) is int and receipt['exit_code']==0,'Dependency lacks current complete qualification')
    evidence=receipt.get('replay_evidence',{})
    if family=='selector':
        api.require(api.canonical(receipt)==SELECTOR_G1_CORE_CONTINUATION_CANONICAL,'Not the parent-consumed current core continuation')
        api.require(api.canonical(suite)==SELECTOR_G1_CORE_SUITE_SHA256 and evidence.get('schema')=='orthemology-v5-audit-continuation-v1','Selector requires the exact core continuation, not a portable or failed prior')
        api.require(callable(getattr(api,'validate_audit_continuation',None)),'D03 audit continuation validator is not integrated')
        api.validate_receipt(receipt,suite,sources,root)
        prior=evidence['prior']['receipt']
        api.require(api.canonical(prior)==SELECTOR_G1_CORE_PRIOR_SHA256,'Changed embedded original core prior')
        api.require(evidence['retained_input_checks']['original_result_sha256']==SELECTOR_G1_CORE_RESULT_SHA256 and evidence['retained_input_checks']['physical_trace_sha256']==SELECTOR_G1_CORE_TRACE_SHA256,'Changed original core result/physical capture')
        original=prior['replay_evidence'];objects=evidence['retained_input_checks']['custom_objects_after']
        api.require(len(objects)==167 and evidence['retained_input_checks']['custom_objects_before']==objects,'Core object set is not complete and stable')
        api.require(evidence['accounting']['new_source_owned_physical_runs']==0 and evidence['accounting']['new_custom_objects']==0,'Continuation was promoted to a second production run')
    else:
        api.require(api.canonical(receipt) in SELECTOR_G1_CURRENT_AUTHOR_RECEIPTS,'Current cold-author receipt is not code-owned and sealed')
        api.require(suite.get('id')=='d08-g1' and evidence.get('selector_g1_family')=='g1','Reviewer requires current v4 cold author recipe')
        selector_g1_validate_receipt(api,receipt,suite,sources,root)
        original=evidence;prior=receipt
        top=evidence['original_collection']['original_result']
        api.require(top['public_manifest_sha256']=='9d8675b5d180d35651ee3a95aec28b3a977f52c0a46b7e9831ca88366736cfbd' and top['custom_objects_reused'] is False,'Historical v2 author receipt is not admitted')
        objects={p:h for p,h in evidence['output_hashes'].items() if p.startswith('original/build/') and p.endswith('.olean')}
        api.require(len(objects)==106,'Author root object census is incomplete')
    return {'receipt_canonical_sha256':api.canonical(receipt),'suite_sha256':api.canonical(suite),
            'original_receipt_canonical_sha256':api.canonical(prior),'source_hashes':receipt['source_hashes'],
            'import_fingerprints':evidence['import_fingerprints'],'tool_fingerprints':evidence['tool_fingerprints'],
            'dependency_checks':evidence['dependency_checks'],'target_audits_sha256':api.canonical(evidence['target_audits']),
            'physical_ledger_sha256':api.canonical(original['child_observations']),
            'physical_invocations_sha256':api.canonical(original['driver_invocations']),
            'objects':objects,'receipt':receipt,'original_receipt':prior,'new_kernel_checks_from_reuse':0}


def selector_g1_dependency_join(api,family,context,inputs,root,sources):
    cat=selector_g1_catalog(api);prior_root=api.no_symlinks(inputs['dependency-run']).resolve()
    receipt_path=api.no_symlinks(inputs['dependency-receipt']).resolve();receipt=api.read_json(receipt_path)
    if family=='selector':api.require(api.sha(receipt_path.read_bytes())==SELECTOR_G1_CORE_CONTINUATION_SHA256,'Current core receipt bytes changed')
    suite=cat['core_suite'] if family=='selector' else cat['families']['g1']['suite']
    if family=='g1-review':api.require(receipt_path==prior_root/'RECEIPT.json','Author receipt is outside its physical run')
    identity=selector_g1_dependency_identity(api,family,receipt,suite,sources,root)
    with selector_g1_helpers(api) as helpers:
        bound=helpers['selector'].bind_core_objects(api,prior_root/'original',context['archives']['core-archive']) if family=='selector' else helpers['g1'].bind_author_production(api,context['archives']['g1-archive'],prior_root/'original')
    original=identity['original_receipt']['replay_evidence']
    invocations=original['driver_invocations'];api.require(len(invocations)==1,'Reusable dependency has more than one physical producer')
    invocation=invocations[0];trace=api.path_in(prior_root,'traces/'+invocation['parent_stage_id'])
    api.require(api._file_hashes(trace)==invocation['trace_sha256'],'Retained physical dependency capture changed')
    oldparent=next(row for row in original['stage_results'] if row['id']==invocation['parent_stage_id'])
    api.require(api.sha(api.path_in(prior_root,'logs/'+oldparent['id']+'.log').read_bytes())==oldparent['log_sha256'],'Retained parent log changed')
    api.require(bound['receipt_sha256']==api.sha((prior_root/'original/RESULT.json').read_bytes()),'Original result identity differs')
    if family=='selector':api.require(bound['receipt_sha256']==SELECTOR_G1_CORE_RESULT_SHA256,'Wrong current original core result')
    else:api.require(bound['receipt_sha256']==original['original_collection']['original_result_sha256'],'Wrong current original author result')
    for path,digest in identity['objects'].items():
        api.require(api.sha(api.path_in(prior_root,path).read_bytes())==digest,'Reusable object differs from physical producer')
    pairs=bound['pairs'] if family=='selector' else bound['production_pairs']
    physical_by_module={}
    for row in original['child_observations']:
        name=row['source_child_id'].removeprefix('runtime/').removeprefix('cost-')
        if name not in {p['module'] for p in pairs}:continue
        api.require(name not in physical_by_module,'Duplicate physical production view');physical_by_module[name]=row
    for pair in pairs:
        row=physical_by_module[pair['module']]
        expected_source=row['source_sha256'] if family=='selector' else row['source_binding']['source_sha256']
        expected_path='original/'+('runtime/' if family=='selector' else '')+'build/'+pair['module'].replace('.','/')+'.olean'
        api.require(expected_source==pair['source_sha256'] and row['output_hashes'].get(expected_path)==pair['object_sha256'],'Source/object/physical child join differs')
    source_rows={r['name']:r for r in suite['replay']['modules']}
    transitive={p['module']:{'source_sha256':p['source_sha256'],'object_sha256':p['object_sha256'],'imports':source_rows[p['module']]['imports']} for p in pairs}
    joined={'identity':identity,'binding':bound,'receipt_file_sha256':api.sha(receipt_path.read_bytes()),
            'physical_trace_sha256':invocation['trace_sha256'],'production_count':len(pairs),
            'transitive_source_object_fingerprint':api.canonical(transitive),
            'retained_tree_sha256':api.canonical(selector_g1_inventory(api,prior_root)),
            'independent_evidence_increment':0,'new_kernel_checks_from_reuse':0}
    selector_g1_validate_reuse(api,family,joined,suite)
    return joined


def selector_g1_validate_reuse(api,family,reuse,previous):
    """Recompute the reusable source/object/physical/transitive contract."""
    api.keys(reuse,{'identity','binding','receipt_file_sha256','physical_trace_sha256','production_count','transitive_source_object_fingerprint','retained_tree_sha256','independent_evidence_increment','new_kernel_checks_from_reuse'})
    cat=selector_g1_catalog(api);contract=cat['reuse_contracts'][family];identity=reuse['identity']
    original=identity['original_receipt']['replay_evidence']
    api.require(len(original['driver_invocations'])==1,'Dependency has more than one original producer')
    invocation=original['driver_invocations'][0]
    api.require(reuse['physical_trace_sha256']==invocation['trace_sha256'],'Reused capture does not belong to the sealed producer')
    base='original/runtime/build/' if family=='selector' else 'original/build/'
    root_pairs=[{'module':name,'source_sha256':source,'object_sha256':identity['objects'][base+name.replace('.','/')+'.olean']} for name,source in contract['root_sources'].items()]
    api.require(set(identity['objects'])=={base+p['module'].replace('.','/')+'.olean' for p in root_pairs},'Reused root object census differs')
    pairs=[p for p in root_pairs if p['module'] in contract['production_sources']]
    for pair in root_pairs:
        api.digest(pair['object_sha256'])
        child_id=('runtime/' if family=='selector' else 'cost-' if pair['module'].startswith('Orthemology.') else '')+pair['module']
        # The source contracts determine the actual author cost labels; do not
        # infer their spelling from an arbitrary producer row or module prefix.
        if family=='g1-review':
            matches=[r for r in cat['families']['g1']['contract']['stages'] if any(o['path']=='build/'+pair['module'].replace('.','/')+'.olean' for o in r['objects'])]
            api.require(len(matches)==1,'Ambiguous original root production child');child_id=matches[0]['id']
        observed=[r for r in original['child_observations'] if r['source_child_id']==child_id]
        api.require(len(observed)==1,'Missing or duplicate reusable physical production view')
        row=observed[0];source=row['source_sha256'] if family=='selector' else row['source_binding']['source_sha256']
        api.require(source==pair['source_sha256'] and row['output_hashes'].get(base+pair['module'].replace('.','/')+'.olean')==pair['object_sha256'],'Reused pair differs from the physical producer')
    result_sha=SELECTOR_G1_CORE_RESULT_SHA256 if family=='selector' else original['original_collection']['original_result_sha256']
    bound={'receipt_sha256':result_sha,'source_manifest_sha256':contract['source_manifest_sha256'],
           'dependency_pins_sha256':contract['dependency_pins_sha256'],'lean_executable_sha256':cat['toolchain']['executable_sha256'],
           'qualification':'REQUIRES_D03_VALIDATED_RECEIPT_AND_CAPTURE_JOIN','new_kernel_checks_from_reuse':0}
    if family=='selector':
        bound.update(objects_verified=167,source_object_fingerprint=api.canonical(pairs),pairs=pairs)
        pins={'receipt_file_sha256':SELECTOR_G1_CORE_CONTINUATION_SHA256,'retained_tree_sha256':SELECTOR_G1_CORE_RETAINED_TREE_SHA256}
    else:
        bound.update(production_objects_verified=95,root_objects_bound=106,production_pairs=pairs,root_pairs=root_pairs,
            production_fingerprint=api.canonical(pairs),root_object_fingerprint=api.canonical(root_pairs),public_manifest_sha256=contract['public_manifest_sha256'])
        api.require(identity['receipt_canonical_sha256'] in SELECTOR_G1_CURRENT_AUTHOR_RECEIPTS,'Unsealed current author dependency')
        pins=SELECTOR_G1_CURRENT_AUTHOR_RECEIPTS[identity['receipt_canonical_sha256']]
        api.keys(pins,{'receipt_file_sha256','retained_tree_sha256'})
    api.require(reuse['binding']==bound,'Changed source/object reuse binding')
    modules={r['name']:r for r in previous['replay']['modules']}
    transitive={p['module']:{'source_sha256':p['source_sha256'],'object_sha256':p['object_sha256'],'imports':modules[p['module']]['imports']} for p in pairs}
    api.require(reuse['transitive_source_object_fingerprint']==api.canonical(transitive),'Changed reusable transitive source/object fingerprint')
    api.require(all(reuse[k]==value for k,value in pins.items()),'Changed sealed dependency receipt or retained tree')
    for value in pins.values():api.digest(value)
    api.require(type(reuse['production_count']) is int and reuse['production_count']==len(pairs)==(167 if family=='selector' else 95),'Changed production subset census')
    for key in ('new_kernel_checks_from_reuse','independent_evidence_increment'):
        api.require(type(reuse[key]) is int and reuse[key]==0,'Reused objects acquired new execution/independence')
    return {'family':family,'production_count':len(pairs),'new_kernel_checks_from_reuse':0}


def selector_g1_verified_library_paths(api,plan,tools):
    """Exact available package-library census before each original/audit use."""
    math=api.no_symlinks(tools['mathlib']).resolve();available={}
    for name,row in plan['packages'].items():
        path=api.no_symlinks(api.path_in(math,row['path'],dot=True)/'.lake/build/lib/lean')
        libraries=api.package_library(name,path,plan['official'])
        # The exact source pin admits only the known unimported Lake-only Cli
        # absence; other missing or non-directory entries are not widened.
        api.require(libraries or (name=='Cli' and not path.exists() and not any(r['package']=='Cli' for r in plan['official'].values())),'Missing imported cache or undeclared absence')
        api.require(libraries==([path] if path.is_dir() else []),'Changed package-library semantics')
        if libraries:available[name]=path
    api.require('mathlib' in available,'Missing mathlib library')
    actual=set((math/'.lake/packages').glob('*/.lake/build/lib/lean'))
    for path in actual:api.no_symlinks(path)
    api.require(actual=={path for name,path in available.items() if name!='mathlib'},'Unreviewed extra original import cache')
    return [available['mathlib'],*sorted(path for name,path in available.items() if name!='mathlib')]


def selector_g1_cache_measurements(api,plan,tools):
    selector_g1_verified_library_paths(api,plan,tools)
    lean=Path(tools['lean']).resolve();math=Path(tools['mathlib']).resolve()
    roots={'lean':lean.parent.parent/'lib/lean'}
    roots.update({name:api.path_in(math,row['path'],dot=True)/'.lake/build/lib/lean' for name,row in plan['packages'].items()})
    result={}
    for name,path in roots.items():
        if path.is_dir():
            inventory=selector_g1_inventory(api,path);api.require(inventory,'Empty official cache')
        else:
            api.require(name=='Cli' and not path.exists() and not any(r['package']=='Cli' for r in plan['official'].values()),'Missing imported cache')
            inventory={}
        result[name]={'tree_sha256':api.canonical(inventory),'files':len(inventory)}
    return result


def selector_g1_stage(api,stage):
    now=api.utc()
    return {'id':stage['id'],'argv':stage['argv'],'cwd':stage['cwd'],'budget_seconds':stage['timeout_seconds'],
            'started_at':now,'ended_at':now,'terminal':'SKIPPED','exit_code':None,'log_sha256':api.sha(b''),'output_hashes':{}}


def selector_g1_execute(api,suite,sources,root,output,tools,inputs,scope=None,*,reviews=None):
    """Execute only after public owner admission; this proposal never calls it."""
    api.require(scope is None or scope==suite['replay']['scope'],'Changed family execution scope')
    api.require(isinstance(reviews,dict) and set(suite['review_ids'])<=set(reviews),'Missing source-bound reviews')
    plan=selector_g1_validate_suite(api,suite,sources,root);family=plan['selector_g1_family'];definition=plan['definition']
    api.require({rid:reviews[rid]['review_sha256'] for rid in suite['review_ids']}==definition['review_hashes'],'Changed source-bound review bytes')
    output=api.no_symlinks(output).absolute();root=Path(root).resolve()
    api.require(not output.exists(),'Preserve prior attempt: output must be absent')
    required=set(plan['inputs'])|({'dependency-run','dependency-receipt'} if family!='g1' else set())
    api.require(set(inputs)==required,'Missing or extra family input binding')
    for protected in [root,*[Path(p).resolve() for p in inputs.values()],*[Path(p).resolve() for p in tools.values()]]:
        api.require(not output.is_relative_to(protected) and not protected.is_relative_to(output),'Family output overlaps protected input')
    api.require(set(tools)=={'lean','lean-bin','python','mathlib'},'Exact family tools are required')
    api.require(Path(tools['lean']).resolve().parent==Path(tools['lean-bin']).resolve(),'Duplicate Lean tool aliases differ')
    output.mkdir(parents=True);logs=output/'logs';logs.mkdir();project=output/'project';project.mkdir()
    for sid,row in plan['files'].items():
        target=api.path_in(project,row['path']);target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(plan['contents'][sid])
    receipt=api._initial_receipt(suite,sources,reviews);evidence=receipt['replay_evidence']
    evidence.update(schema=SELECTOR_G1_SCHEMA,cache_policy=SELECTOR_G1_POLICY,selector_g1_family=family,
                    selector_g1_module_sha256=api.sha(Path(__file__).read_bytes()),catalog_sha256=SELECTOR_G1_CATALOG_SHA256,
                    driver_invocations=[],child_observations=[],helper_invocations=[],original_collection=None,
                    dependency_reuse=None,official_caches_before={},official_caches_after={},source_inventory_before={},source_inventory_after={})
    # The family auditor uses root-qualified elaborated names. Its invocation
    # otherwise retains the existing adapter target-audit shape.
    stages={r['id']:r for r in evidence['stage_results']};current=stages['_prerequisites']
    def save():
        receipt['stages']=[{k:r[k] for k in ('id','terminal','exit_code','log_sha256')} for r in evidence['stage_results']]
        receipt['log_sha256']=api.canonical({r['id']:r['log_sha256'] for r in evidence['stage_results']})
        receipt['ended_at']=api.utc();api.write_json(output/'RECEIPT.json',receipt)
    save();context=None
    try:
        current['started_at']=api.utc();environment_suite=copy.deepcopy(suite);environment_suite['replay']['build_roots']=[]
        git=Path(shutil.which('git') or '')
        api.require(git.is_file() and api.sha(git.read_bytes())==SELECTOR_G1_GIT_SHA256,'Changed metadata Git executable')
        # Capture every outside-parent prerequisite process separately. This
        # wrapper never puts those intervals into the original driver's ledger.
        old_process=api.run_process
        def prerequisite_process(argv,cwd,env,log,timeout):
            run=old_process(argv,cwd,env,log,timeout)
            executable=Path(argv[0]);tool='git' if executable==git else 'python' if api.sha(executable.read_bytes())==selector_g1_catalog(api)['python']['executable_sha256'] else 'lean'
            args=[str(v) for v in argv]
            for old,new in sorted({str(output):'{out}',str(tools['mathlib']):'{dependency:mathlib}',str(git):'{tool:git}',str(tools['python']):'{tool:python}',str(tools['lean']):'{tool:lean}'}.items(),key=lambda x:len(x[0]),reverse=True):args=[a.replace(old,new) for a in args]
            evidence['helper_invocations'].append({'argv':args,'cwd':'{out}','timeout_seconds':timeout,**run,'log_path':Path(log).relative_to(output).as_posix(),'credit':'METADATA_ONLY',
                'source_binding':{'kind':'TOOL_PROBE','tool_name':tool,'executable_sha256':api.sha(executable.read_bytes()),'driver_sha256':selector_g1_driver_sha(selector_g1_catalog(api),family)}})
            return run
        try:
            api.run_process=prerequisite_process
            resolved,fingerprints,dependencies,env,input_hashes=api._verify_environment(environment_suite,plan,tools,{k:inputs[k] for k in plan['inputs']},output)
        finally:api.run_process=old_process
        evidence['tool_fingerprints']=fingerprints;evidence['dependency_checks']=dependencies
        roots={};archives={k:str(Path(inputs[k]).resolve()) for k in plan['inputs']}
        for iid in archives:
            packet=iid.removesuffix('-archive')
            if packet not in {'selector','g1','g1-review'}:continue
            archive=output/'archives'/iid;api.extract_source_zip(archives[iid],archive)
            prefix=selector_g1_catalog(api)['families'].get(packet,{}).get('prefix','')
            if packet in {'selector','g1','g1-review'}:roots[packet]=str(archive/prefix.rstrip('/'))
        driver=Path(roots[family])/('replay_review.py' if family=='g1-review' else 'replay.py')
        context={'family':family,'roots':roots,'archives':archives,'out':str(output/'original'),
                 'dependency_run':str(Path(inputs['dependency-run']).resolve()) if family!='g1' else None,
                 'lean':str(resolved['lean'].resolve()),'mathlib':str(Path(tools['mathlib']).resolve()),'python':str(resolved['python']),
                 'cwd':str(project.resolve()),'trace':str(output/'traces'/('original-'+family)),'arguments':[],'driver':str(driver)}
        context['arguments']=selector_g1_source_argv(api,family,context)[3:]
        eventplan=selector_g1_events(api,family,context)
        evidence['source_inventory_before']={k:selector_g1_inventory(api,Path(v)) for k,v in roots.items()}
        api.require(evidence['source_inventory_before']=={k:definition['original_inventory'][k] for k in roots},'Changed complete original source packet inventory')
        evidence['official_caches_before']=selector_g1_cache_measurements(api,plan,tools)
        if family!='g1':
            evidence['dependency_reuse']=selector_g1_dependency_join(api,family,context,inputs,root,sources)
            old=evidence['dependency_reuse']['identity']
            api.require(old['tool_fingerprints']==fingerprints and old['dependency_checks']==dependencies,'Dependency tool/cache package fingerprints changed')
            if family=='selector':
                caches=old['receipt']['replay_evidence']['retained_input_checks']['official_cache_measurements']
                expected={r['root_id']:{'tree_sha256':r['tree_after_sha256'],'files':r['file_count']} for r in caches}
            else:expected=old['receipt']['replay_evidence']['official_caches_after']
            api.require(evidence['official_caches_before']==expected,'Current official cache differs from qualified dependency')
        prelog=logs/'prerequisites.log';prelog.write_text('Exact family sources, tools, packages and current dependency joins checked. Metadata only.\n')
        current.update(terminal='COMPLETED',exit_code=0,ended_at=api.utc(),log_sha256=api.sha(prelog.read_bytes()));save()
        parent_spec=suite['replay']['stages'][0];current=stages[parent_spec['id']]
        context_file=output/'TRACE_CONTEXT.json';api.write_json(context_file,context)
        launch=[str(resolved['python']),'-B',str(Path(api.__file__).resolve()),'--trace-selector-g1',family,str(context_file)]
        parent_log=logs/(parent_spec['id']+'.log')
        run=api.run_process(launch,project,env,parent_log,parent_spec['timeout_seconds']);current.update(run)
        invocation={'parent_stage_id':parent_spec['id'],'driver_sha256':selector_g1_driver_sha(selector_g1_catalog(api),family),
                    'source_argv':parent_spec['argv'],'launch_argv':['{tool:python}','-B','{adapter}','--trace-selector-g1',family,'{out}/TRACE_CONTEXT.json'],
                    'launch_cwd':'{project}','runner_sha256':evidence['runner_sha256'],'parent_log_sha256':run['log_sha256'],
                    'trace_sha256':api._file_hashes(Path(context['trace'])) if Path(context['trace']).exists() else None,
                    'child_count':len(list(Path(context['trace']).glob('[0-9][0-9][0-9][0-9].json'))),'physical_children':[]}
        evidence['driver_invocations']=[invocation]
        # Retain partial actual children even when the original terminates early.
        if Path(context['trace']).exists():
            invocation['physical_children']=[selector_g1_public_child(api,api.read_json(p),context,run['log_sha256'],'NO_CREDIT') for p in sorted(Path(context['trace']).glob('[0-9][0-9][0-9][0-9].json'))]
        api.require(run['terminal']=='COMPLETED' and run['exit_code']==0,'Original family process did not complete successfully')
        collection=selector_g1_collect(api,family,context,run,output)
        evidence['original_collection']={k:v for k,v in collection.items() if k not in {'physical_children','child_observations','output_hashes'}}
        invocation.update(physical_children=collection['physical_children'],trace_sha256=collection['trace_sha256'],child_count=len(collection['physical_children']))
        evidence['output_hashes'].update(collection['output_hashes']);current['output_hashes']={'original':api._file_hashes(output/'original')}
        evidence['output_hashes'].update(current['output_hashes']);save()
        children={c['source_child_id']:c for c in collection['child_observations']}
        for stage in suite['replay']['stages'][1:]:
            current=stages[stage['id']];current['started_at']=api.utc();observed=children[stage['argv'][2]]
            event=next(e for e in eventplan['children'] if e['id']==observed['source_child_id'])
            data=Path(event['log']).read_bytes();api.require(api.sha(data)==observed['log_sha256'],'Original child log changed during observation')
            (logs/(stage['id']+'.log')).write_bytes(data)
            current.update(terminal=observed['terminal'],exit_code=observed['exit_code'],log_sha256=observed['log_sha256'],ended_at=api.utc())
            evidence['child_observations'].append({**observed,'stage_id':stage['id'],'parent_stage_id':parent_spec['id'],
                'physical_run_sha256':collection['trace_sha256'],'parent_log_sha256':run['log_sha256'],'observed_at':current['ended_at']})
            for cid in stage['control_ids']:
                control=next(c for c in suite['controls'] if c['id']==cid);actual=observed['actual_outcome']
                api.require(actual==control['expected_outcome'],'Original control outcome differs')
                receipt['controls'].append({k:control[k] for k in ('id','source_id','target_id','role','expected_outcome_sha256')}|{'actual_outcome':actual,'actual_outcome_sha256':api.sha(actual.encode()),'terminal':'COMPLETED','exit_code':current['exit_code'],'log_sha256':current['log_sha256']})
                evidence['control_diagnostics'].append({'control_id':cid,'stage_id':stage['id'],'prerequisite_stage_ids':stage['depends_on'],'expected':stage['expected_diagnostics'],'observed_log_sha256':current['log_sha256'],'match':'MATCHED'})
            save()
        current=stages['_target_audit'];generated=output/'generated';generated.mkdir();audit=generated/'V5SuccessorReadback.lean'
        body=selector_g1_audit_source(api,list(plan['targets'].values()));audit.write_text(body)
        libs=[output/p for p in suite['replay']['build_roots']]
        if family!='g1':libs.append(Path(inputs['dependency-run'])/('original/runtime/build' if family=='selector' else 'original/build'))
        libs.extend([*selector_g1_verified_library_paths(api,plan,tools),resolved['lean'].resolve().parent.parent/'lib/lean'])
        audit_env=dict(env);audit_env['LEAN_PATH']=os.pathsep.join(map(str,libs))
        audit_log=logs/'target-audit.log';audit_run=api.run_process([resolved['lean'],'-j1',audit],project,audit_env,audit_log,300);current.update(audit_run)
        api.require(audit_run['terminal']=='COMPLETED' and audit_run['exit_code']==0,'Family checked target audit failed')
        audits=api.parse_readbacks(audit_log.read_text(),list(plan['targets'].values()))
        evidence['target_audits']=[{'target_id':tid,**value,'stage_id':'_target_audit','log_sha256':audit_run['log_sha256']} for tid,value in audits.items()]
        evidence['output_hashes']['generated/V5SuccessorReadback.lean']=api.sha(body.encode())
        evidence['source_inventory_after']={k:selector_g1_inventory(api,Path(v)) for k,v in roots.items()}
        api.require(evidence['source_inventory_after']==evidence['source_inventory_before'],'Original packet bytes changed during execution')
        evidence['official_caches_after']=selector_g1_cache_measurements(api,plan,tools)
        api.require(evidence['official_caches_after']==evidence['official_caches_before'],'Official cache changed during execution')
        if family!='g1':api.require(selector_g1_dependency_join(api,family,context,inputs,root,sources)==evidence['dependency_reuse'],'Dependency changed during execution')
        for iid in plan['inputs']:api.require(api._input_inventory(plan['inputs'][iid],inputs[iid],plan)==input_hashes[iid],'Original archive changed during execution')
        for sid,row in plan['files'].items():api.require((project/row['path']).read_bytes()==plan['contents'][sid],'Projected source changed during execution')
        evidence['source_hashes_after']={sid:api.sha(api.public_bytes(root,sources[sid])) for sid in suite['source_ids']}
        receipt.update(outcome='QUALIFIED_DECLARED_SUITE',exit_code=0,proof_scope='DECLARED_SUITE',
            axioms=sorted({a for value in audits.values() for a in value['axioms']}),
            target_readbacks=[{'target_id':t['id'],'source_id':t['source_id'],'target_sha256':t['target_sha256'],'outcome':'CHECKED'} for t in suite['targets']])
    except (ValueError,OSError,KeyError,TypeError,subprocess.SubprocessError) as error:
        api.write_json(output/'FAILURE.json',{'stage_id':current['id'],'observed_at':api.utc(),'error':type(error).__name__+': '+str(error)})
        resource=current['terminal'] in {'TIMEOUT','INTERRUPTED'} or any(c.get('terminal') in {'TIMEOUT','INTERRUPTED','RUNNING'} for i in evidence['driver_invocations'] for c in i['physical_children'])
        receipt.update(outcome='RESOURCE_INCONCLUSIVE' if resource else 'BLOCKED_TOOLCHAIN' if isinstance(error,api.MissingTool) else 'BLOCKED_EXTERNAL_INPUT' if isinstance(error,api.MissingInput) else 'FAILED',exit_code=1,proof_scope='NONE')
        receipt['target_readbacks']=[];receipt['axioms']=[];evidence['target_audits']=[]
        if current['terminal']=='SKIPPED':
            p=logs/(current['id']+'-failure.log');p.write_text(type(error).__name__+': '+str(error)+'\n')
            current.update(terminal='COMPLETED',exit_code=1,ended_at=api.utc(),log_sha256=api.sha(p.read_bytes()))
    save();selector_g1_validate_receipt(api,receipt,suite,sources,root);return receipt


def selector_g1_time(api,value):
    api.require(isinstance(value,str) and value.endswith('Z'),'Invalid UTC timestamp')
    try:return datetime.fromisoformat(value[:-1]+'+00:00')
    except ValueError:raise ValueError('Invalid actual timestamp') from None


def selector_g1_validate_receipt(api,receipt,suite,sources,root):
    """Strict receipt dispatch for these exact new family recipes only."""
    try:return _selector_g1_validate_receipt(api,receipt,suite,sources,root)
    except (KeyError,TypeError,IndexError,AttributeError,OverflowError) as error:
        raise ValueError('Malformed selector/G1 receipt: '+str(error)) from error


def _selector_g1_validate_receipt(api,receipt,suite,sources,root):
    json.dumps(receipt,allow_nan=False)
    plan=selector_g1_validate_suite(api,suite,sources,root);family=plan['selector_g1_family'];cat=selector_g1_catalog(api)
    api.keys(receipt,{'id','suite_id','family','suite_sha256','source_hashes','review_hashes','toolchain_sha256','outcome','target_readbacks','controls','stages','invocation','started_at','ended_at','exit_code','log_sha256','axioms','proof_scope','replay_evidence'})
    evidence=receipt['replay_evidence'];extra={'child_observations','driver_invocations','selector_g1_family','selector_g1_module_sha256','catalog_sha256','helper_invocations','original_collection','dependency_reuse','official_caches_before','official_caches_after','source_inventory_before','source_inventory_after'}
    api.keys(evidence,api.EVIDENCE_KEYS|extra)
    api.require(evidence['schema']==SELECTOR_G1_SCHEMA and evidence['cache_policy']==SELECTOR_G1_POLICY and evidence['selector_g1_family']==family and evidence['catalog_sha256']==SELECTOR_G1_CATALOG_SHA256,'Wrong family schema/policy/catalogue')
    api.require(receipt['id']==suite['id']+'-replay' and receipt['suite_id']==suite['id'] and receipt['family']==suite['family'],'Receipt belongs to another suite')
    api.require(receipt['suite_sha256']==api.canonical(suite) and receipt['toolchain_sha256']==api.canonical(suite['toolchain']),'Changed suite/toolchain')
    api.require(receipt['invocation']==['replay_v5_successors.py','--execute','--suite',suite['id'],'--out','{out}'],'Changed family invocation')
    hashes=plan['definition']['source_hashes']
    api.require(receipt['source_hashes']==evidence['source_hashes_before']==evidence['source_hashes_after']==hashes,'Changed family source identity')
    api.require(receipt['review_hashes']==plan['definition']['review_hashes'],'Changed code-owned source review identity')
    for value in receipt['review_hashes'].values():api.digest(value)
    api.require(evidence['descriptor_sha256']==api.canonical(suite['replay']) and evidence['closure_sha256']==api.closure_fingerprint(suite,sources) and evidence['import_fingerprints']==api.import_fingerprints(suite,sources),'Changed source/import/transitive closure')
    api.require(evidence['driver_hashes']=={d['id']:d['sha256'] for d in suite['replay']['drivers']},'Original driver identity differs')
    current_runner=api.sha(Path(api.__file__).read_bytes());current_module=api.sha(Path(__file__).read_bytes())
    api.require((evidence['runner_sha256'],evidence['selector_g1_module_sha256']) in SELECTOR_G1_REVIEWED_EXECUTORS or (evidence['runner_sha256']==current_runner and evidence['selector_g1_module_sha256']==current_module),'Unreviewed executing adapter/helper bytes')
    successful=receipt['outcome']=='QUALIFIED_DECLARED_SUITE'
    api.require(receipt['outcome'] in {'QUALIFIED_DECLARED_SUITE','FAILED','RESOURCE_INCONCLUSIVE','BLOCKED_TOOLCHAIN','BLOCKED_EXTERNAL_INPUT'},'Unknown family terminal')
    api.require(type(receipt['exit_code']) is int and receipt['exit_code']==(0 if successful else 1) and receipt['proof_scope']==('DECLARED_SUITE' if successful else 'NONE'),'Invented family success/scope')
    start=selector_g1_time(api,receipt['started_at']);end=selector_g1_time(api,receipt['ended_at']);api.require(start<=end,'Reversed family interval')
    stages=api.indexed(evidence['stage_results']);expected=['_prerequisites',*plan['stages'],'_target_audit']
    api.require(list(stages)==expected,'Missing/reordered stage ledger')
    api.require(receipt['stages']==[{k:r[k] for k in ('id','terminal','exit_code','log_sha256')} for r in stages.values()] and receipt['log_sha256']==api.canonical({r['id']:r['log_sha256'] for r in stages.values()}),'Contradictory top-level stage/log ledger')
    prior_end=start
    for sid,row in stages.items():
        api.keys(row,{'id','argv','cwd','budget_seconds','started_at','ended_at','terminal','exit_code','log_sha256','output_hashes'})
        spec=plan['stages'].get(sid)
        if spec is None:
            spec={'argv':['{builtin:prerequisites}'] if sid=='_prerequisites' else ['{tool:lean}','-j1','{out}/generated/V5SuccessorReadback.lean'],'cwd':'.','timeout_seconds':30 if sid=='_prerequisites' else 300,'expected_exit_codes':[0],'output_paths':[]}
        api.require(row['argv']==spec['argv'] and row['cwd']==spec['cwd'] and type(row['budget_seconds']) is int and row['budget_seconds']==spec['timeout_seconds'],'Changed stage recipe/budget')
        api.require(row['terminal'] in {'COMPLETED','TIMEOUT','INTERRUPTED','SKIPPED','MISSING'},'Unknown stage terminal')
        if row['terminal']=='COMPLETED':api.require(type(row['exit_code']) is int and 0<=row['exit_code']<124,'Invalid completed exit')
        else:api.require(row['exit_code'] is None,'Nonterminal has process credit')
        rs,re_=selector_g1_time(api,row['started_at']),selector_g1_time(api,row['ended_at'])
        api.require(start<=rs<=re_<=end,'Stage interval outside run')
        api.digest(row['log_sha256'])
        for value in row['output_hashes'].values():api.digest(value)
        if successful:
            api.require(prior_end<=rs and row['terminal']=='COMPLETED' and row['exit_code'] in spec['expected_exit_codes'],'Successful suite has unordered/incomplete stage')
            api.require(set(row['output_hashes'])==set(spec['output_paths']),'Successful stage output identity missing')
            prior_end=re_
    parent_id=suite['replay']['stages'][0]['id'];parent=stages[parent_id]
    api.require(len(evidence['driver_invocations'])<=1,'Duplicate physical original run')
    physical=[];expected_events=selector_g1_expected_physical(api,family)
    if evidence['driver_invocations']:
        invocation=evidence['driver_invocations'][0]
        api.keys(invocation,{'parent_stage_id','driver_sha256','source_argv','launch_argv','launch_cwd','runner_sha256','parent_log_sha256','trace_sha256','child_count','physical_children'})
        api.require(invocation['parent_stage_id']==parent_id and invocation['driver_sha256']==selector_g1_driver_sha(cat,family) and invocation['source_argv']==parent['argv'],'Changed physical original identity')
        api.require(invocation['launch_argv']==['{tool:python}','-B','{adapter}','--trace-selector-g1',family,'{out}/TRACE_CONTEXT.json'] and invocation['launch_cwd']=='{project}','Changed instrumented launch/cwd')
        api.require(invocation['runner_sha256']==evidence['runner_sha256'] and invocation['parent_log_sha256']==parent['log_sha256'],'Parent capture association differs')
        if invocation['trace_sha256'] is not None:api.digest(invocation['trace_sha256'])
        physical=invocation['physical_children']
        api.require(type(invocation['child_count']) is int and invocation['child_count']==len(physical)<=len(expected_events),'Physical call census differs')
        previous=selector_g1_time(api,parent['started_at'])
        for index,(row,event) in enumerate(zip(physical,expected_events)):
            api.keys(row,{'id','index','argv','cwd','explicit_cwd','started_at','ended_at','terminal','exit_code','capture_kind','log_sha256','source_binding','output_hashes','metadata_only','timeout_seconds','parent_log_sha256','credit','raw_capture_sha256'})
            api.require(type(row['index']) is int and row['index']==index and row['id']==event['id'] and row['argv']==event['argv'],'Missing/reordered/substituted physical call')
            api.require(row['cwd']=='{project}' and row['explicit_cwd'] is False,'Original omitted cwd was altered')
            api.require(row['source_binding']==event['source_binding'] and row['metadata_only'] is event['metadata_only'] and row['capture_kind']==event['capture_kind'],'Source/capture/role changed')
            api.require(row['timeout_seconds']==event['timeout_seconds'] and type(row['timeout_seconds']) is type(event['timeout_seconds']),'Changed original child wall budget')
            selector_g1_check_binding(api,row['source_binding'],cat['sources']);api.digest(row['raw_capture_sha256'])
            api.require(row['parent_log_sha256']==parent['log_sha256'],'Physical child belongs to another parent')
            if row['capture_kind']=='INHERITED_PARENT_STDOUT':api.require(row['log_sha256'] is None,'Fabricated inherited child log')
            elif row['log_sha256'] is not None:api.digest(row['log_sha256'])
            rs=selector_g1_time(api,row['started_at']);api.require(previous<=rs,'Reordered physical intervals')
            if row['ended_at'] is not None:
                previous=selector_g1_time(api,row['ended_at']);api.require(rs<=previous<=selector_g1_time(api,parent['ended_at']),'Physical child interval is outside parent')
            else:api.require(not successful and row['terminal']=='RUNNING' and index==len(physical)-1,'Missing completed child end')
            api.require(row['terminal'] in {'COMPLETED','TIMEOUT','INTERRUPTED','RUNNING'},'Unknown physical terminal')
            if row['terminal']=='COMPLETED':api.require(type(row['exit_code']) is int and 0<=row['exit_code']<124,'Invalid physical exit')
            else:api.require(row['exit_code'] is None,'Physical nonterminal has exit credit')
            if successful:
                api.require(row['terminal']=='COMPLETED' and row['exit_code']==event['expected_exit'],'Unfulfilled physical contract')
                api.require(row['credit']==('METADATA_ONLY' if event['metadata_only'] else 'REJECT' if event['expected_exit'] else 'ACCEPT'),'Wrong physical credit')
                api.require(set(row['output_hashes'])==set(event['outputs']),'Physical output census differs')
                if row['capture_kind']!='INHERITED_PARENT_STDOUT':api.require(row['log_sha256'] is not None,'Missing captured child log')
            else:api.require(row['credit'] in {'NO_CREDIT','METADATA_ONLY','REJECT','ACCEPT'},'Unknown retained partial credit')
            for path,h in row['output_hashes'].items():api.relative(path);api.digest(h)
    if successful:api.require(len(physical)==len(expected_events),'Successful suite omitted original physical calls')
    childmap={r['id']:r for r in physical};observations=api.indexed(evidence['child_observations'],'stage_id')
    declared={s['id']:s for s in suite['replay']['stages'][1:]}
    api.require(set(observations)<=set(declared),'Foreign observation')
    if successful:api.require(set(observations)==set(declared),'Missing original child observations')
    for sid,row in observations.items():
        api.keys(row,{'source_child_id','physical_child_id','source_binding','mode','actual_outcome','terminal','exit_code','log_sha256','physical_record_sha256','original_record_sha256','output_hashes','credit','stage_id','parent_stage_id','physical_run_sha256','parent_log_sha256','observed_at'})
        child=childmap[row['physical_child_id']];stage=declared[sid]
        api.require(row['source_child_id']==row['physical_child_id']==stage['argv'][2] and row['parent_stage_id']==parent_id and row['mode']=='NONEXECUTING_OBSERVATION','Observation is not a view of the original physical call')
        api.require(row['physical_record_sha256']==api.canonical(child) and row['physical_run_sha256']==evidence['driver_invocations'][0]['trace_sha256'] and row['parent_log_sha256']==parent['log_sha256'],'Observation/capture join changed')
        api.require(row['source_binding']==child['source_binding'] and row['output_hashes']==child['output_hashes'],'Observation source/output differs')
        api.require(row['terminal']==child['terminal']==stages[sid]['terminal'] and row['exit_code']==child['exit_code']==stages[sid]['exit_code'] and row['actual_outcome']==child['credit'],'Observation terminal differs')
        api.require(row['log_sha256']==stages[sid]['log_sha256']==child['log_sha256'],'Completed original/captured/observation logs differ')
        api.require(row['credit']==('FINITE_ONLY' if child['capture_kind']=='SOURCE_PRESCRIBED_FILE' else 'SOURCE_CHILD'),'Finite observation promoted')
        when=selector_g1_time(api,row['observed_at']);api.require(selector_g1_time(api,parent['ended_at'])<=selector_g1_time(api,stages[sid]['started_at'])<=when<=selector_g1_time(api,stages[sid]['ended_at']),'Observation interval replaced original execution')
        if row['original_record_sha256'] is not None:api.digest(row['original_record_sha256'])
    # Outside-parent tool/package readbacks have their own real timing/logs.
    helper_specs=selector_g1_expected_helpers(api,family)
    api.require(len(evidence['helper_invocations'])<=len(helper_specs),'Extra outside-parent helper')
    if successful:api.require(len(evidence['helper_invocations'])==len(helper_specs),'Required outside-parent helper omitted')
    for row,spec in zip(evidence['helper_invocations'],helper_specs):
        api.keys(row,{'argv','cwd','timeout_seconds','terminal','exit_code','started_at','ended_at','log_sha256','log_path','credit','source_binding'})
        api.require(row['credit']=='METADATA_ONLY' and row['timeout_seconds']==30 and type(row['timeout_seconds']) is int,'Helper acquired scientific credit/budget')
        api.require(selector_g1_time(api,stages['_prerequisites']['started_at'])<=selector_g1_time(api,row['started_at'])<=selector_g1_time(api,row['ended_at'])<=selector_g1_time(api,stages['_prerequisites']['ended_at']),'Helper forged inside parent interval')
        api.relative(row['log_path']);api.digest(row['log_sha256'])
        selector_g1_check_binding(api,row['source_binding'],cat['sources'])
        api.require(all(row[k]==spec[k] for k in spec),'Outside-parent helper identity/order changed')
        if successful:api.require(row['terminal']=='COMPLETED' and type(row['exit_code']) is int and row['exit_code']==0,'Prerequisite process did not succeed')
    controls=api.indexed(receipt['controls']);diagnostics=api.indexed(evidence['control_diagnostics'],'control_id')
    expected_controls=api.indexed(suite['controls'])
    api.require(set(controls)==set(diagnostics)<=set(expected_controls),'Unbound/foreign control evidence')
    if successful:api.require(set(controls)==set(expected_controls),'Required controls omitted')
    for cid,row in controls.items():
        spec=expected_controls[cid];diag=diagnostics[cid];stage=plan['stages'][diag['stage_id']];obs=observations[stage['id']]
        api.keys(row,{'id','source_id','target_id','role','expected_outcome_sha256','actual_outcome','actual_outcome_sha256','terminal','exit_code','log_sha256'})
        api.keys(diag,{'control_id','stage_id','prerequisite_stage_ids','expected','observed_log_sha256','match'})
        api.require(all(row[k]==spec[k] for k in ('id','source_id','target_id','role','expected_outcome_sha256')),'Changed control identity/target')
        api.require(cid in stage['control_ids'] and diag['prerequisite_stage_ids']==stage['depends_on'] and diag['expected']==stage['expected_diagnostics'] and diag['match']=='MATCHED','Changed source-owned control predicate')
        api.require(row['actual_outcome']==spec['expected_outcome']==obs['actual_outcome'] and row['actual_outcome_sha256']==api.sha(row['actual_outcome'].encode()),'Invented control outcome')
        api.require(row['terminal']==obs['terminal'] and row['exit_code']==obs['exit_code'] and row['log_sha256']==obs['log_sha256']==diag['observed_log_sha256'],'Control did not come from matching physical child')
    if evidence['original_collection'] is not None:
        collection=evidence['original_collection']
        api.keys(collection,{'original_result','original_result_sha256','normalization_sha256','normalized','trace_sha256','event_plan_sha256','original_run_count','independent_evidence_increment'})
        api.require(type(collection['original_run_count']) is int and collection['original_run_count']==1 and type(collection['independent_evidence_increment']) is int and collection['independent_evidence_increment']==0,'Duplicated execution/independence')
        api.require(collection['trace_sha256']==evidence['driver_invocations'][0]['trace_sha256'] and collection['normalization_sha256']==api.canonical(collection['normalized']),'Original collection/capture changed')
        api.digest(collection['original_result_sha256']);api.digest(collection['event_plan_sha256'])
        contract=plan['definition']['contract'];original=collection['original_result'];normal=collection['normalized']
        api.require(original['status']==contract['terminal_status'] and normal['original_full_terminal_present'] is True and normal['resource_children']==[] and normal['not_run_children']==[],'Original source-specific completion is absent')
        for path,value in contract['receipt_constraints']:
            found=original
            for key in path.split('/'):found=found[int(key)] if isinstance(found,list) else found[key]
            api.require(type(found) is type(value) and found==value,'Original required terminal field changed')
        api.require(len(original['runs'])==len(contract['stages']),'Original full row census changed')
        for spec,row in zip(contract['stages'],original['runs']):
            api.require(row.get(spec['row_key'])==spec['label'] and row['source_sha256']==spec['source']['sha256'] and type(row['exit_code']) is int and row['exit_code']==spec['expected_exit_code'],'Changed original child order/source/terminal')
            child=childmap[spec['id']];api.require(row['log_sha256']==child['log_sha256'],'Original result log differs from physical capture')
            for obj in spec['objects']:
                if spec['expected_exit_code']==0:api.require(child['output_hashes']['original/'+obj['path']]==row[obj['row_hash_field']],'Original object/capture differs')
        if family=='g1-review':api.require(original['source_identical_command_preserving_v2_bridge'] is False,'Historical v2 bridge was credited')
    elif successful:raise ValueError('No complete original collector')
    if successful:
        inventory=plan['definition']['original_inventory'];root_names={'selector'} if family=='selector' else {'g1'} if family=='g1' else {'g1','g1-review'}
        api.require(evidence['source_inventory_before']==evidence['source_inventory_after']=={k:inventory[k] for k in root_names},'Original source packet changed or was not measured')
        api.require(evidence['official_caches_before']==evidence['official_caches_after'] and set(evidence['official_caches_before'])=={'lean',*plan['packages']},'Official caches changed or omitted')
        for row in evidence['official_caches_after'].values():
            api.keys(row,{'tree_sha256','files'});api.digest(row['tree_sha256']);api.require(type(row['files']) is int and row['files']>=0,'Invalid cache census')
        definitions={'lean':suite['toolchain'],**{r['name']:r for r in suite['replay']['tools']}}
        api.require(set(evidence['tool_fingerprints'])==set(definitions),'Incomplete tool evidence')
        for name,definition in definitions.items():
            actual=evidence['tool_fingerprints'][name];api.keys(actual,{'kind','version','platform','executable_sha256','version_log_sha256'})
            api.require(all(actual[k]==definition[k] for k in ('kind','version','platform','executable_sha256')),'Substituted tool fingerprint');api.digest(actual['version_log_sha256'])
        pins={r['name']:r for r in suite['toolchain']['packages']};api.require(set(evidence['dependency_checks'])==set(pins),'Incomplete package checks')
        for name,row in evidence['dependency_checks'].items():
            api.keys(row,{'kind','revision','manifest_sha256','tracked_clean','cache_policy','head_log_sha256','status_log_sha256'})
            api.require(row['kind']=='GIT' and row['revision']==pins[name]['revision'] and row['manifest_sha256']==api.sha(plan['contents'][plan['packages'][name]['manifest_source_id']]) and row['tracked_clean'] is True and row['cache_policy']=='TRUSTED_PINNED_OFFICIAL_CACHE','Package/source/cache identity differs')
            api.digest(row['head_log_sha256']);api.digest(row['status_log_sha256'])
        if family=='g1':api.require(evidence['dependency_reuse'] is None,'Cold author reused custom objects')
        else:
            reuse=evidence['dependency_reuse'];api.keys(reuse,{'identity','binding','receipt_file_sha256','physical_trace_sha256','production_count','transitive_source_object_fingerprint','retained_tree_sha256','independent_evidence_increment','new_kernel_checks_from_reuse'})
            previous=cat['core_suite'] if family=='selector' else cat['families']['g1']['suite']
            expected_identity=selector_g1_dependency_identity(api,family,reuse['identity']['receipt'],previous,sources,root)
            api.require(reuse['identity']==expected_identity,'Changed dependency receipt identity')
            selector_g1_validate_reuse(api,family,reuse,previous)
            api.require(type(reuse['production_count']) is int and reuse['production_count']==(167 if family=='selector' else 95) and type(reuse['new_kernel_checks_from_reuse']) is int and reuse['new_kernel_checks_from_reuse']==0 and type(reuse['independent_evidence_increment']) is int and reuse['independent_evidence_increment']==0,'Reuse was credited as new execution')
            for key in ('receipt_file_sha256','physical_trace_sha256','transitive_source_object_fingerprint','retained_tree_sha256'):api.digest(reuse[key])
    audits=api.indexed(evidence['target_audits'],'target_id');axes=set()
    if successful:api.require(set(audits)==set(plan['targets']),'Incomplete safe target audits')
    else:api.require(audits=={} and receipt['target_readbacks']==[] and receipt['axioms']==[],'Failed attempt acquired fresh target qualification')
    for tid,row in audits.items():
        api.keys(row,{'target_id','name','type_sha256','axioms','closure_status','checked_declarations','stage_id','log_sha256'})
        api.require(row['name']==plan['targets'][tid]['name'] and row['closure_status']=='CHECKED_SAFE' and type(row['checked_declarations']) is int and row['checked_declarations']>0,'Target closure not checked')
        api.require(row['stage_id']=='_target_audit' and row['log_sha256']==stages['_target_audit']['log_sha256'] and stages['_target_audit']['exit_code']==0,'Safe audit/physical log differs')
        api.digest(row['type_sha256']);api.require(isinstance(row['axioms'],list) and len(set(row['axioms']))==len(row['axioms']) and set(row['axioms'])<=api.AXIOMS,'Wrong axiom closure');axes.update(row['axioms'])
    if successful:
        api.require(receipt['axioms']==sorted(axes) and receipt['target_readbacks']==[{'target_id':t['id'],'source_id':t['source_id'],'target_sha256':t['target_sha256'],'outcome':'CHECKED'} for t in suite['targets']],'Changed target summary')
        expected_outputs={p:h for child in physical for p,h in child['output_hashes'].items()}
        expected_outputs.update(stages[parent_id]['output_hashes']);expected_outputs['generated/V5SuccessorReadback.lean']=api.sha(selector_g1_audit_source(api,list(plan['targets'].values())).encode())
        api.require(evidence['output_hashes']==expected_outputs,'Unbound/omitted/falsely fresh artifacts')
    return {'suite_id':suite['id'],'outcome':receipt['outcome'],'scope':'EXACT_FAMILY_RECEIPT_AND_PHYSICAL_DEPENDENCY_CONTRACT'}
