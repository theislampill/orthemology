"""Exact covering-only recollection and one-audit continuation.

Completed source-owned events remain retained events. This module never invokes
an original producer, compiler object build, mutation generator or source replay.
"""
import copy
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re

SCHEMA = 'orthemology-v5-covering-audit-continuation-v1'
PARSER = 'd04-covering-retained-negative-controls-v1'
DATA_SHA256 = 'd9ffbc13339e72a3d39c39938fc2cc5ae25d92ddb8482b1581861325da8af23a'
CACHE_POLICY = 'PINNED_OFFICIAL_CACHES_REUSED_COVERING_EXECUTION_FRESH_COLLECTION_AND_AUDIT'
REVIEWED_EXECUTOR_HASHES = frozenset()

def data(adapter):
    path = adapter.no_symlinks(Path(__file__).with_suffix('.json'))
    raw = path.read_bytes()
    adapter.require(adapter.sha(raw) == DATA_SHA256, 'Covering continuation data changed')
    return json.loads(raw)

def instant(value, adapter):
    adapter.require(isinstance(value,str) and value.endswith('Z'), 'Covering UTC interval missing')
    return datetime.fromisoformat(value[:-1]+'+00:00')

def executor_hash(adapter): return adapter.sha(Path(adapter.__file__).read_bytes())

def verify_inventory(root, expected, *, adapter):
    a=adapter; root=a.no_symlinks(root); a.require(root.is_dir(),'Retained covering tree missing'); actual={}
    for path in sorted(root.rglob('*')):
        a.no_symlinks(path)
        if path.is_file():
            with path.open('rb') as stream: digest=hashlib.file_digest(stream,'sha256').hexdigest()
            actual[path.relative_to(root).as_posix()]={'sha256':digest,'bytes':path.stat().st_size}
        else:a.require(path.is_dir(),'Nonregular retained covering input')
    a.require(actual==expected,'Retained covering inventory changed')
    return {'file_count':len(actual),'tree_sha256':a.canonical({p:r['sha256']for p,r in actual.items()})}

def prior_value(raw, failure, suite, sources, root, *, adapter):
    a=adapter; pins=data(a)
    a.require(suite['id']==pins['suite_id'] and a.canonical(suite)==pins['suite_sha256']
              and a.d04_declared_admitted(suite,sources),'Unapproved covering continuation suite')
    a.require(len(raw)==pins['prior_receipt_bytes'] and a.sha(raw)==pins['prior_receipt_sha256'],'Wrong retained covering receipt bytes')
    a.require(a.sha(failure)==pins['failure_sha256'],'Wrong retained covering failure bytes')
    receipt=json.loads(raw)
    a.require(a.canonical(receipt)==pins['prior_receipt_canonical_sha256'],'Changed covering prior receipt value')
    a.require(receipt['outcome']=='FAILED' and receipt['proof_scope']=='NONE' and receipt['controls']==[], 'Covering prior acquired qualification')
    a.validate_receipt(receipt,suite,sources,root)
    a.require(receipt['replay_evidence']['runner_sha256']==pins['original_runner_sha256'],'Wrong original covering executor')
    return {'receipt':receipt,'receipt_raw_hex':raw.hex(),'failure_raw_hex':failure.hex(),
        'receipt_sha256':pins['prior_receipt_sha256'],'receipt_canonical_sha256':pins['prior_receipt_canonical_sha256'],
        'failure_sha256':pins['failure_sha256']}

def _prior(binding, suite, sources, root, adapter):
    a=adapter
    a.keys(binding,{'receipt','receipt_raw_hex','failure_raw_hex','receipt_sha256','receipt_canonical_sha256','failure_sha256'})
    actual=prior_value(bytes.fromhex(binding['receipt_raw_hex']),bytes.fromhex(binding['failure_raw_hex']),suite,sources,root,adapter=a)
    a.require(actual==binding,'Covering embedded prior differs from exact raw bytes')
    return actual['receipt']

def _qualified(invocation, normalization, plan, parent, adapter):
    a=adapter; pins=data(a); value=copy.deepcopy(invocation)
    a.d04_validate_captured_invocation(value,plan,parent,True)
    a.require(value['trace_sha256']==pins['trace_sha256'],'Wrong original covering trace')
    a.require(a.canonical(normalization)==pins['normalization_sha256'],'Covering source-output normalization changed')
    value['normalization']=normalization;value['normalization_sha256']=a.canonical(normalization)
    a.d04_bind_normalization(value)
    value['qualified_objects']=a.d04_expected_objects(plan,value)
    a.require(value['qualified_objects']==pins['qualified_objects'],'Covering target/import producer mapping changed')
    return value

def _observations(qualified, old, plan, suite, start, adapter):
    a=adapter; stages=a.indexed(old['stage_results']); parent=stages['original-driver']
    children,_=a.d04_observations(qualified,plan,parent)
    collection={'parser_id':'t07-covering-translated-v1','parser_revision':PARSER,'collector_runner_sha256':executor_hash(a),
        'started_at':start,'ended_at':start,'driver_invocation':qualified,'child_observations':[],'stage_results':[],
        'control_diagnostics':[],'controls':[],'output_hashes':qualified['qualified_objects']}
    completed={sid:{**row,'matched':True}for sid,row in stages.items()if row['terminal']=='COMPLETED'}
    captures={item['record']['id']:item for item in qualified['capture_records']}
    for sid,spec in plan['stages'].items():
        if sid=='original-driver':continue
        a.require(spec['argv'][:1]==['{builtin:observe-child}'],'Covering continuation would execute a source stage')
        began=a.utc(); observed=children[tuple(spec['argv'][1:])]
        run={'terminal':observed['terminal'],'exit_code':observed['exit_code'],'started_at':began,'ended_at':a.utc(),'log_sha256':observed['log_sha256']}
        a.assess_stage(spec,run,bytes.fromhex(captures[observed['source_child_id']]['log_hex']).decode(),completed)
        collection['child_observations'].append({**observed,'stage_id':sid,'observed_at':run['ended_at']})
        collection['stage_results'].append({**stages[sid],**run})
        completed[sid]={**run,'matched':True}
        for cid in spec['control_ids']:
            collection['control_diagnostics'].append({'control_id':cid,'stage_id':sid,'prerequisite_stage_ids':spec['depends_on'],
                'expected':spec['expected_diagnostics'],'observed_log_sha256':run['log_sha256'],'match':'MATCHED'})
    collection['controls']=a._hc_exec_controls(suite,plan,collection,a)
    collection['ended_at']=a.utc()
    return collection

def validate_collection(collection, prior, plan, suite, *, adapter):
    a=adapter; pins=data(a)
    a.keys(collection,{'parser_id','parser_revision','collector_runner_sha256','started_at','ended_at','driver_invocation',
        'child_observations','stage_results','control_diagnostics','controls','output_hashes'})
    a.require(collection['parser_id']=='t07-covering-translated-v1' and collection['parser_revision']==PARSER,'Unreviewed covering collector')
    a.require(collection['collector_runner_sha256'] in {executor_hash(a),*REVIEWED_EXECUTOR_HASHES},'Unreviewed covering collector executor')
    start=instant(collection['started_at'],a);end=instant(collection['ended_at'],a)
    a.require(instant(prior['ended_at'],a)<start<=end,'Covering collection relabelled original intervals')
    old=prior['replay_evidence']; physical=old['driver_invocations'][0]; parent=a.indexed(old['stage_results'])['original-driver']
    qualified=collection['driver_invocation']
    a.require({k:v for k,v in qualified.items()if k not in {'normalization','normalization_sha256','qualified_objects'}}==
              {k:v for k,v in physical.items()if k not in {'normalization','normalization_sha256','qualified_objects'}},'Original covering physical invocation changed')
    expected=_qualified(physical,qualified['normalization'],plan,parent,a)
    a.require(qualified==expected,'Qualified covering collection changed')
    children,_=a.d04_observations(expected,plan,parent)
    observations=a.indexed(collection['child_observations'],'stage_id');stages=a.indexed(collection['stage_results'])
    declared={sid:s for sid,s in plan['stages'].items()if sid!='original-driver'}
    a.require(list(observations)==list(stages)==list(declared) and len(stages)==38,'Incomplete or reordered covering observation census')
    completed={sid:{**row,'matched':True}for sid,row in a.indexed(old['stage_results']).items()if row['terminal']=='COMPLETED'}
    captures={item['record']['id']:item for item in physical['capture_records']}; diagnostics=[];last=start
    for sid,spec in declared.items():
        row=stages[sid];expected_row=children[tuple(spec['argv'][1:])];observed=observations[sid]
        a.keys(observed,set(expected_row)|{'stage_id','observed_at'})
        a.require({k:v for k,v in observed.items()if k not in {'stage_id','observed_at'}}==expected_row,'Covering observation changed physical facts')
        a.keys(row,a.AC_STAGE_KEYS)
        a.require(type(row['exit_code'])is int if row['terminal']=='COMPLETED'else row['exit_code']is None,'Covering parsed terminal must preserve its actual exit type')
        a.require(row['id']==sid and row['argv']==spec['argv'] and row['cwd']==spec['cwd'] and row['budget_seconds']==spec['timeout_seconds'] and row['output_hashes']=={},'Covering parsing stage became an execution')
        begin=instant(row['started_at'],a);finish=instant(row['ended_at'],a)
        a.require(last<=begin<=finish<=end and observed['observed_at']==row['ended_at'],'Covering observation interval is not the actual parsing interval')
        last=finish
        a.require(all(row[k]==expected_row[k]for k in ['terminal','exit_code','log_sha256']),'Covering parsing stage changed child terminal/log')
        a.assess_stage(spec,row,bytes.fromhex(captures[expected_row['source_child_id']]['log_hex']).decode(),completed)
        completed[sid]={**row,'matched':True}
        for cid in spec['control_ids']:diagnostics.append({'control_id':cid,'stage_id':sid,'prerequisite_stage_ids':spec['depends_on'],
            'expected':spec['expected_diagnostics'],'observed_log_sha256':row['log_sha256'],'match':'MATCHED'})
    a.require(collection['control_diagnostics']==diagnostics,'Covering control diagnostics differ')
    a.require(collection['controls']==a._hc_exec_controls(suite,plan,collection,a) and len(collection['controls'])==13,'Covering control census or evidence differs')
    a.require(collection['output_hashes']==pins['qualified_objects'],'Covering qualified output mapping differs')
    return collection

def read_retained(prior, suite, sources, root, *, adapter):
    a=adapter;pins=data(a);prior=a.no_symlinks(prior).absolute();start=a.utc()
    binding=prior_value(a.path_in(prior,'RECEIPT.json').read_bytes(),a.path_in(prior,'FAILURE.json').read_bytes(),suite,sources,root,adapter=a)
    original=binding['receipt'];old=original['replay_evidence'];plan=a.validate_suite(suite,sources,root)
    before=verify_inventory(prior,pins['retained_files'],adapter=a)
    a.require(before['tree_sha256']==pins['retained_tree_sha256'],'Wrong retained covering tree')
    for sid,row in plan['files'].items():a.require(a.path_in(prior/'project',row['path']).read_bytes()==plan['contents'][sid],'Retained covering source projection changed')
    objects=a._ac_exec_objects(prior,pins['all_objects'],suite['replay']['build_roots'],a)
    physical=old['driver_invocations'][0];a.require(physical['output_root']==str(prior),'Retained physical output location changed')
    parent=a.indexed(old['stage_results'])['original-driver'];a.require(parent['terminal']=='COMPLETED'and parent['exit_code']==0,'Original covering parent was not successful')
    normalization=a.d04_normalize(physical['recipe'],Path(physical['source_root']),prior/'original',parent,a.path_in(prior,'logs/original-driver.log').read_text())
    qualified=_qualified(physical,normalization,plan,parent,a)
    a.require(a.d04_object_outputs(plan,physical['recipe'],qualified)==pins['qualified_objects'],'Retained descriptor objects changed')
    collection=_observations(qualified,old,plan,suite,start,a)
    validate_collection(collection,original,plan,suite,adapter=a)
    a.require(verify_inventory(prior,pins['retained_files'],adapter=a)==before,'Retained covering run changed during collection')
    return {'prior':binding,'inventory':before,'all_objects':objects,'qualified_objects':pins['qualified_objects'],'collection':collection}

def output_path(output, protected, *, adapter):
    return adapter._ac_exec_output(output,protected,adapter)

def audit_result(run, raw, targets, *, adapter):
    a=adapter;terminal=run['terminal'];code=run['exit_code'];text=raw.decode('utf-8')
    if terminal in {'TIMEOUT','INTERRUPTED'}:
        a.require(code is None,'Covering resource terminal has fabricated exit');return 'RESOURCE_INCONCLUSIVE',{}
    a.require(terminal=='COMPLETED'and type(code)is int and 0<=code<124,'Covering audit has no actual final terminal')
    if re.search(r'timed out|out of memory|maximum (?:number of heartbeats|recursion depth)|deterministic timeout|WALL_CLOCK_LIMIT',text,re.I):return 'RESOURCE_INCONCLUSIVE',{}
    if code:return 'FAILED',{}
    a.require(not re.search(r'error:|warning:|sorryAx|UNCHECKED_DEPENDENCY|UNSAFE_OR_PARTIAL_DEPENDENCY|INCOMPLETE_PROOF_CLOSURE',text),'Covering audit contains a proof hole or diagnostic')
    a.require(bool(targets),'Covering audit has no declared targets')
    return 'QUALIFIED_DECLARED_SUITE',a.parse_readbacks(text,targets)

def audit_once(output, prior, plan, resolved, env, *, adapter):
    a=adapter;pins=data(a);output=Path(output);prior=Path(prior)
    a.require(len(plan['targets'])==4,'Covering audit target census changed')
    body=a._audit_source(list(plan['targets'].values())).encode('utf-8')
    a.require(a.sha(body)==pins['audit_source_sha256'],'Covering generated auditor changed')
    generated=output/'generated';a.require(not generated.exists(),'Covering auditor must be fresh');generated.mkdir()
    audit=generated/'V5SuccessorReadback.lean'
    with audit.open('xb')as stream:stream.write(body)
    argv=[resolved['lean'],'-j1',audit];cwd=prior/'project';log=output/'logs/target-audit.log'
    a.write_json(output/'RESOLVED_AUDIT_INVOCATION.json',{'argv':[str(x)for x in argv],'cwd':str(cwd),'timeout_seconds':300,
        'lean_path':env['LEAN_PATH'].split(os.pathsep),'generated_source_sha256':pins['audit_source_sha256'],
        'scope':'ONE_COVERING_TARGET_AUDIT_NO_SOURCE_REPLAY'})
    run=a.run_process(argv,cwd,env,log,300)
    a.write_json(output/'AUDIT_PROCESS.json',run)
    a.require(a.sha(log.read_bytes())==run['log_sha256'],'Covering audit log changed after actual process')
    return run,log.read_bytes()

METADATA = ('descriptor_sha256','closure_sha256','source_hashes_before','source_hashes_after',
            'import_fingerprints','tool_fingerprints','dependency_checks')
IDENTITY = ('suite_id','family','suite_sha256','source_hashes','review_hashes','toolchain_sha256')
EVIDENCE_KEYS = set(METADATA) | {'schema','runner_sha256','helper_sha256','data_sha256','cache_policy','prior',
    'retained_collection','retained_input_checks','fresh_audit','stage_results','target_audits','output_hashes','accounting'}

def expected_lean_path(prior, plan, *, adapter):
    pins=data(adapter);bindings=prior['replay_evidence']['driver_invocations'][0]['bindings']
    caches={r['root_id']:r for r in pins['official_cache_measurements']}
    roots=[str(PurePosixPath(bindings['out'])/name)for name in plan['suite']['replay']['build_roots']] if 'suite'in plan else [str(PurePosixPath(bindings['out'])/'original/kernel')]
    for name,row in plan['packages'].items():
        if caches[name]['file_count']:roots.append(str(PurePosixPath(bindings['dependency:mathlib'])/row['path']/'.lake/build/lib/lean'))
    roots.append(str(PurePosixPath(bindings['tool:lean']).parent.parent/'lib/lean'))
    return roots

def compose_receipt(checked, suite, plan, fresh, *, adapter):
    a=adapter;pins=data(a);prior=checked['prior']['receipt'];old=prior['replay_evidence'];stages=fresh['stage_results']
    run=stages[-1];raw=bytes.fromhex(fresh['audit_log_hex'])
    outcome,audits=audit_result(run,raw,list(plan['targets'].values()),adapter=a);success=outcome=='QUALIFIED_DECLARED_SUITE'
    resolved=fresh['resolved_invocation']
    evidence={key:copy.deepcopy(old[key])for key in METADATA}
    evidence.update(schema=SCHEMA,runner_sha256=executor_hash(a),helper_sha256=a.sha(Path(__file__).read_bytes()),data_sha256=DATA_SHA256,
        cache_policy=CACHE_POLICY,prior=copy.deepcopy(checked['prior']),retained_collection=copy.deepcopy(checked['collection']),
        retained_input_checks={key:copy.deepcopy(fresh[key])for key in ('retained_before','retained_after','objects_before','objects_after','official_cache_measurements')},
        fresh_audit={'audit_log_hex':fresh['audit_log_hex'],'audit_source_hex':fresh['audit_source_hex'],
            'resolved_invocation':copy.deepcopy(resolved),'resolved_invocation_sha256':a.canonical(resolved)},
        stage_results=copy.deepcopy(stages),target_audits=[{'target_id':tid,**row,'stage_id':'_target_audit','log_sha256':run['log_sha256']}for tid,row in audits.items()],
        output_hashes={'generated/V5SuccessorReadback.lean':pins['audit_source_sha256']},accounting=dict(pins['accounting']))
    receipt={key:copy.deepcopy(prior[key])for key in IDENTITY}
    receipt.update(id=suite['id']+'-audit-continuation-'+a.sha((fresh['started_at']+a.canonical(resolved)).encode())[:16],
        invocation=['replay_v5_successors.py','--covering-audit-continuation','--suite',suite['id'],'--prior','{prior}','--out','{out}'],
        started_at=fresh['started_at'],ended_at=fresh['ended_at'],outcome=outcome,proof_scope='DECLARED_SUITE'if success else'NONE',
        exit_code=0 if success else 1,controls=copy.deepcopy(checked['collection']['controls']),
        stages=[{key:row[key]for key in ('id','terminal','exit_code','log_sha256')}for row in stages],
        log_sha256=a.canonical({row['id']:row['log_sha256']for row in stages}),
        target_readbacks=[{'target_id':r['id'],'source_id':r['source_id'],'target_sha256':r['target_sha256'],'outcome':'CHECKED'}for r in suite['targets']]if success else[],
        axioms=sorted({axiom for row in audits.values()for axiom in row['axioms']}),replay_evidence=evidence)
    return receipt

def _validate_receipt(receipt, suite, sources, root, adapter):
    json.dumps(receipt,ensure_ascii=False,allow_nan=False)
    a=adapter;pins=data(a);a.keys(receipt,a.HC_RECEIPT_KEYS);e=receipt['replay_evidence'];a.keys(e,EVIDENCE_KEYS)
    a.require(e['schema']==SCHEMA and e['cache_policy']==CACHE_POLICY,'Unknown covering continuation schema/policy')
    prior=_prior(e['prior'],suite,sources,root,a);old=prior['replay_evidence'];plan=a.validate_suite(suite,sources,root)
    for key in IDENTITY:a.require(receipt[key]==prior[key],'Covering suite/source/review/toolchain identity changed')
    for key in METADATA:a.require(e[key]==old[key],'Covering original environment/source/import evidence changed')
    a.require(e['runner_sha256'] in {executor_hash(a),*REVIEWED_EXECUTOR_HASHES} and e['runner_sha256']!=pins['original_runner_sha256'],'Unreviewed covering executor')
    a.require(e['helper_sha256']==a.sha(Path(__file__).read_bytes()) and e['data_sha256']==DATA_SHA256,'Covering continuation helper/data changed')
    a.require(receipt['invocation']==['replay_v5_successors.py','--covering-audit-continuation','--suite',suite['id'],'--prior','{prior}','--out','{out}'],'Not the covering-only audit invocation')
    a._ac_fresh_stages(receipt,e,prior,a)
    stages=a.indexed(e['stage_results']);pre=stages['_prerequisites'];audit=stages['_target_audit']
    collection=validate_collection(e['retained_collection'],prior,plan,suite,adapter=a)
    a.require(pre['started_at']<=collection['started_at']<=collection['ended_at']<=pre['ended_at'],'Recollection is outside fresh prerequisite interval')
    a.require(receipt['controls']==collection['controls'],'New audit became a control or changed retained controls')
    retained=e['retained_input_checks'];a.keys(retained,{'retained_before','retained_after','objects_before','objects_after','official_cache_measurements'})
    expected_inventory={'file_count':356,'tree_sha256':pins['retained_tree_sha256']}
    a.require(retained['retained_before']==retained['retained_after']==expected_inventory,'Original run inventory changed')
    a.require(retained['objects_before']==retained['objects_after']==pins['all_objects'],'Missing/foreign/changed original covering object')
    a.require(a.canonical(retained['official_cache_measurements'])==a.canonical(pins['official_cache_measurements']),'Official cache identities/census changed')
    fresh=e['fresh_audit'];a.keys(fresh,{'audit_log_hex','audit_source_hex','resolved_invocation','resolved_invocation_sha256'})
    body=bytes.fromhex(fresh['audit_source_hex']);raw=bytes.fromhex(fresh['audit_log_hex'])
    a.require(a.sha(body)==pins['audit_source_sha256'] and body==a._audit_source(list(plan['targets'].values())).encode(),'Covering audit generator or target set changed')
    a.require(a.sha(raw)==audit['log_sha256'],'New audit terminal/log bytes disagree')
    resolved=fresh['resolved_invocation'];a.keys(resolved,{'argv','cwd','timeout_seconds','lean_path','generated_source_sha256','scope'})
    a.require(a.canonical(resolved)==fresh['resolved_invocation_sha256'],'Resolved covering invocation digest changed')
    original=old['driver_invocations'][0];bindings=original['bindings'];argv=resolved['argv']
    a.require(isinstance(argv,list)and len(argv)==3 and argv[:2]==[bindings['tool:lean'],'-j1'],'Covering audit may not compile objects or launch another producer')
    auditor=PurePosixPath(argv[2]);a.require(auditor.is_absolute() and auditor.parts[-2:]==('generated','V5SuccessorReadback.lean'),'Wrong fresh covering auditor path')
    out=auditor.parent.parent;old_root=PurePosixPath(original['output_root'])
    protected=[old_root,PurePosixPath(bindings['dependency:mathlib']),PurePosixPath(bindings['tool:lean']).parent.parent,PurePosixPath(bindings['tool:python']).parent.parent]
    a.require(all(not out.is_relative_to(p)and not p.is_relative_to(out)for p in protected),'Fresh covering auditor overlaps retained input')
    a.require(resolved['cwd']==str(old_root/'project') and type(resolved['timeout_seconds'])is int and resolved['timeout_seconds']==300,'Wrong covering audit cwd/budget')
    a.require(resolved['lean_path']==expected_lean_path(prior,plan,adapter=a),'Covering audit import namespace changed')
    a.require(resolved['generated_source_sha256']==pins['audit_source_sha256'] and resolved['scope']=='ONE_COVERING_TARGET_AUDIT_NO_SOURCE_REPLAY','Wrong covering audit scope')
    expected_id=suite['id']+'-audit-continuation-'+a.sha((receipt['started_at']+a.canonical(resolved)).encode())[:16]
    a.require(receipt['id']==expected_id and receipt['id']!=prior['id'],'Covering continuation identity differs')
    a.require(a.canonical(e['accounting'])==a.canonical(pins['accounting']),'Invented covering execution/object/independence credit')
    a.require(e['output_hashes']=={'generated/V5SuccessorReadback.lean':pins['audit_source_sha256']},'Fresh covering outputs include unreviewed objects')
    outcome,audits=audit_result(audit,raw,list(plan['targets'].values()),adapter=a);success=outcome=='QUALIFIED_DECLARED_SUITE'
    a.require(receipt['outcome']==outcome and receipt['proof_scope']==('DECLARED_SUITE'if success else'NONE')and type(receipt['exit_code'])is int and receipt['exit_code']==(0 if success else 1),'Covering final outcome exceeds actual audit')
    expected_audits=[{'target_id':tid,**row,'stage_id':'_target_audit','log_sha256':audit['log_sha256']}for tid,row in audits.items()]
    a.require(e['target_audits']==expected_audits,'Covering target/type/axiom/safe-closure readback association changed')
    expected_targets=[{'target_id':r['id'],'source_id':r['source_id'],'target_sha256':r['target_sha256'],'outcome':'CHECKED'}for r in suite['targets']]if success else[]
    a.require(receipt['target_readbacks']==expected_targets and receipt['axioms']==sorted({x for r in audits.values()for x in r['axioms']}),'Covering target declaration or axiom footprint changed')
    a.require(receipt['stages']==[{k:r[k]for k in ('id','terminal','exit_code','log_sha256')}for r in e['stage_results']]
              and receipt['log_sha256']==a.canonical({r['id']:r['log_sha256']for r in e['stage_results']}),'Covering aggregate terminal/log differs')
    return receipt

def validate_receipt(receipt, suite, sources, root, *, adapter):
    try:return _validate_receipt(receipt,suite,sources,root,adapter)
    except (KeyError,TypeError,IndexError,AttributeError,OSError,UnicodeError,OverflowError)as error:
        raise ValueError('Malformed or unavailable covering continuation: '+str(error))from error

def execute(suite, sources, root, prior, output, tools, inputs, *, reviews, adapter):
    """Recollect the exact retained attempt, then invoke only its missing audit.

    Tool/version and source/cache custody probes are prerequisites. The single
    scientific process is audit_once; there is no source extraction or producer
    dispatch here. Any refusal preserves the process terminal and fresh files.
    """
    a=adapter;pins=data(a);plan=a.validate_suite(suite,sources,root)
    prior=a.no_symlinks(prior).absolute()
    a.require(prior.is_dir(),'Retained covering run is unavailable')
    protected=[root,prior,Path(__file__).parent,Path(a.__file__).parent,*inputs.values()]
    if 'mathlib'in tools:protected.append(tools['mathlib'])
    protected.extend(Path(path).resolve().parent.parent for name,path in tools.items()if name!='mathlib')
    output=output_path(output,protected,adapter=a);started=a.utc();run=None
    runner=executor_hash(a);helper=a.sha(Path(__file__).read_bytes())
    output.mkdir(parents=True,exist_ok=False);(output/'logs').mkdir()
    try:
        pre_start=a.utc();checked=read_retained(prior,suite,sources,root,adapter=a)
        original=checked['prior']['receipt'];old=original['replay_evidence']
        a.require(isinstance(reviews,dict)and set(suite['review_ids'])<=set(reviews),'Missing current covering reviews')
        a.require({rid:reviews[rid]['review_sha256']for rid in suite['review_ids']}==original['review_hashes'],'Covering review identity changed')
        hashes={sid:a.sha(a.public_bytes(root,sources[sid]))for sid in suite['source_ids']}
        a.require(hashes==original['source_hashes']==old['source_hashes_before']==old['source_hashes_after']
            and a.canonical(suite['replay'])==old['descriptor_sha256']
            and a.closure_fingerprint(suite,sources)==old['closure_sha256']
            and a.import_fingerprints(suite,sources)==old['import_fingerprints'],'Covering source/import binding changed')
        bindings=old['driver_invocations'][0]['bindings']
        # The original tracer records the resolved interpreter; the authorized
        # venv entry is a symlink to that same hash-checked Python executable.
        a.require({name:str(Path(path).resolve())for name,path in tools.items()}=={
            'lean':bindings['tool:lean'],'python':bindings['tool:python'],'mathlib':bindings['dependency:mathlib']},'Covering tool locations changed')
        a.require(set(inputs)==set(plan['inputs']),'Missing or foreign covering external input')
        before=output/'prerequisites-before';before.mkdir()
        resolved,fingerprints,dependencies,env,input_hashes=a._verify_environment(suite,plan,tools,inputs,before)
        a.require(fingerprints==old['tool_fingerprints']and dependencies==old['dependency_checks'],'Covering tool/dependency binding changed')
        roots,libraries=a._ac_exec_cache_roots(resolved,tools,plan,a)
        cache_rows,inventories=a._ac_exec_caches(roots,plan,a)
        a.require(a.canonical(cache_rows)==a.canonical(pins['official_cache_measurements']),'Covering official caches differ from reviewed custody')
        env['LEAN_PATH']=os.pathsep.join(str(p)for p in [*[a.path_in(prior,name)for name in suite['replay']['build_roots']],*libraries])
        a.require(env['LEAN_PATH'].split(os.pathsep)==expected_lean_path(original,plan,adapter=a),'Covering import namespace changed')
        a.write_json(output/'RETAINED_COLLECTION.json',checked['collection'])
        a.write_json(output/'RETAINED_INPUT_CHECKS_BEFORE.json',{'inventory':checked['inventory'],'objects':checked['all_objects'],'official_caches':cache_rows})
        pre_log=output/'logs/prerequisites.log'
        pre_log.write_text('Exact covering prior, 356 retained files, 38 physical captures, 18 objects and seven import objects verified.\n'
            'Current sources, reviews, tools and official caches bound. Parsing observes retained events; no producer or object build.\n',encoding='utf-8')
        pre={'id':'_prerequisites','argv':['{builtin:prerequisites}'],'cwd':'.','budget_seconds':30,
            'started_at':pre_start,'ended_at':a.utc(),'terminal':'COMPLETED','exit_code':0,
            'log_sha256':a.sha(pre_log.read_bytes()),'output_hashes':{}}
        run,raw=audit_once(output,prior,plan,resolved,env,adapter=a)
        after=output/'prerequisites-after';after.mkdir()
        resolved_after,fingerprints_after,dependencies_after,_,inputs_after=a._verify_environment(suite,plan,tools,inputs,after)
        a.require(resolved_after==resolved and fingerprints_after==fingerprints and dependencies_after==dependencies
            and inputs_after==input_hashes,'Covering tools/dependencies/inputs changed during audit')
        roots_after,libraries_after=a._ac_exec_cache_roots(resolved_after,tools,plan,a)
        rows_after,inventories_after=a._ac_exec_caches(roots_after,plan,a)
        a.require(roots_after==roots and libraries_after==libraries and rows_after==cache_rows and inventories_after==inventories,
            'Covering official cache changed during audit')
        retained_after=verify_inventory(prior,pins['retained_files'],adapter=a)
        objects_after=a._ac_exec_objects(prior,pins['all_objects'],suite['replay']['build_roots'],a)
        a.require(retained_after==checked['inventory']and objects_after==checked['all_objects'],'Retained covering inputs changed during audit')
        a.require(prior_value(a.path_in(prior,'RECEIPT.json').read_bytes(),a.path_in(prior,'FAILURE.json').read_bytes(),suite,sources,root,adapter=a)==checked['prior'],
            'Covering old receipt/failure changed during audit')
        a.require({sid:a.sha(a.public_bytes(root,sources[sid]))for sid in suite['source_ids']}==hashes,'Covering public source changed during audit')
        audit=output/'generated/V5SuccessorReadback.lean'
        a.require(a.sha(audit.read_bytes())==pins['audit_source_sha256']and executor_hash(a)==runner
            and a.sha(Path(__file__).read_bytes())==helper and data(a)==pins,'Covering auditor/executor/helper/data changed')
        a.require(a.sha((output/'logs/target-audit.log').read_bytes())==run['log_sha256']and raw==(output/'logs/target-audit.log').read_bytes(),
            'Covering actual audit log changed during postchecks')
        audit_stage={'id':'_target_audit','argv':['{tool:lean}','-j1','{out}/generated/V5SuccessorReadback.lean'],
            'cwd':'.','budget_seconds':300,**run,'output_hashes':{}}
        fresh={'started_at':started,'ended_at':a.utc(),'stage_results':[pre,audit_stage],
            'audit_log_hex':raw.hex(),'audit_source_hex':audit.read_bytes().hex(),
            'resolved_invocation':json.loads((output/'RESOLVED_AUDIT_INVOCATION.json').read_bytes()),
            'official_cache_measurements':cache_rows,'retained_before':checked['inventory'],'retained_after':retained_after,
            'objects_before':checked['all_objects'],'objects_after':objects_after}
        receipt=compose_receipt(checked,suite,plan,fresh,adapter=a)
        validate_receipt(receipt,suite,sources,root,adapter=a)
        a.write_json(output/'RECEIPT.json',receipt)
        return receipt
    except (ValueError,OSError,KeyError,TypeError,KeyboardInterrupt)as error:
        # audit_once writes this immediately after run_process returns, before
        # checking its log. Preserve even a post-return association refusal.
        process_file=output/'AUDIT_PROCESS.json'
        if run is None and process_file.is_file():run=json.loads(process_file.read_bytes())
        a.write_json(output/'REFUSAL.json',{'status':'COVERING_CONTINUATION_REFUSED','started_at':started,'ended_at':a.utc(),
            'audit_process':run,'error':type(error).__name__+': '+str(error),'prior_receipt_sha256':pins['prior_receipt_sha256'],
            'qualified_receipt_written':False})
        raise
