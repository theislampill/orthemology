"""PRIVATE pure readers for the six reviewed original output contracts.

No subprocess, producer import, execution, writes, qualification or public receipt
creation occurs here. The caller must independently bind each returned child to
the first-run D03 process trace, approved descriptor and fresh-output provenance.
An original terminal assertion is never labelled a captured child exit or argv.
"""
from pathlib import Path, PurePosixPath
import ast, hashlib, json, re

class InvalidOriginalEvidence(ValueError): pass

def require(ok, message):
    if not ok: raise InvalidOriginalEvidence(message)

def digest(data): return hashlib.sha256(data).hexdigest()
def canonical(value): return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def unique(pairs):
    out={}
    for key,value in pairs:
        require(key not in out,'duplicate JSON key: '+key);out[key]=value
    return out
def read_json(path):
    def bad(value): raise InvalidOriginalEvidence('nonfinite JSON: '+value)
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=unique,parse_constant=bad)
def safe_file(root, relative):
    require(isinstance(relative,str) and relative and '\\' not in relative,'bad relative path')
    p=PurePosixPath(relative)
    require(not p.is_absolute() and all(x not in ('','.','..') for x in relative.split('/')),'unsafe relative path')
    root=Path(root).resolve(strict=True);current=root
    for part in p.parts:
        current=current/part;require(not current.is_symlink(),'symlink in output/source path')
    require(current.resolve(strict=False).is_relative_to(root),'path escaped root')
    return current
def path_for(symbolic, roots):
    m=re.match(r'^\{([^}]+)\}(?:/(.*))?$',symbolic)
    require(m is not None and m[1] in roots,'unbound symbolic source path: '+symbolic)
    return safe_file(roots[m[1]],m[2]) if m[2] else Path(roots[m[1]]).resolve(strict=True)
def neutral(value, roots, alias):
    replacements=[(candidate,'{'+k+'}') for k,v in roots.items() for candidate in {str(Path(v)),str(Path(v).resolve())}]
    replacements += [('$PACKET','{root:p1}'),('$OUTPUT','{out}'),('$LEAN_ROOT','{lean-root}'),('$MATHLIB_ROOT','{dependency:mathlib}'),('$PYTHON','{tool:python}')]
    text=str(value)
    for old,new in sorted(replacements,key=lambda x:len(x[0]),reverse=True):text=text.replace(old,new)
    if 'lean-root' in roots:text=text.replace('{lean-root}/bin/lean','{tool:lean}')
    return text
def pointer(obj, value):
    for key in value.split('/'):
        obj=obj[int(key)] if isinstance(obj,list) else obj[key]
    return obj

RESOURCE=re.compile(r'\btimeout\b|WALL_CLOCK_LIMIT|WALL_TIMEOUT|RESOURCE_LIMIT|maximum number of heartbeats|maximum recursion depth|TIMEOUT: NO REJECTION OR SUCCESS CREDIT',re.I)
INFRASTRUCTURE=re.compile(r'unknown module|unknown constant|unknown identifier|file not found|object file .* does not exist|no such file|failed to load|cannot load',re.I)
ALLOWED_AXIOMS={'propext','Classical.choice','Quot.sound'}

def axioms(text, count=None, names=None):
    populated=re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",text)
    empty=re.findall(r"'([^']+)' does not depend on any axioms",text)
    names_seen=[n for n,_ in populated]+empty
    require(len(names_seen)==len(set(names_seen)),'duplicate axiom declaration readback')
    for name,block in populated:
        require({s.strip() for s in block.split(',') if s.strip()}<=ALLOWED_AXIOMS,'unapproved axiom for '+name)
    if count is not None:require(len(names_seen)==count,'axiom readback count mismatch')
    if names is not None:require(set(names_seen)==set(names) and len(names_seen)==len(names),'axiom declaration census mismatch')
    return {'declaration_count':len(names_seen),'names':sorted(names_seen)}

def p1_comparison_records(observed, source_bytes, script_bytes):
    """Validate recorded finite comparisons, never run or compile Python code."""
    require(observed['status']=='PASS_FINITE_INDEPENDENT_CONTROLS','P1 finite status mismatch')
    require(observed['source_sha256']==digest(source_bytes) and observed['independent_literal_copy_sha256']==digest(source_bytes),'P1 literal source identity mismatch')
    require(observed['script_sha256']==digest(script_bytes),'P1 comparison driver identity mismatch')
    require(observed['differential_cases']==266760 and observed['seeded_boundary_cases']==1593,'P1 finite case census')
    tree=ast.parse(script_bytes.decode('utf-8'))
    assignments=[x for x in ast.walk(tree) if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='mutations' for t in x.targets)]
    require(len(assignments)==1,'P1 source mutation table identity')
    cases=ast.literal_eval(assignments[0].value)
    require(len(cases)==len(observed['mutation_controls'])==18,'P1 finite mutation census')
    source=source_bytes.decode('utf-8')
    for (name,before,after,case),row in zip(cases,observed['mutation_controls']):
        require(row['name']==name and canonical(row['case'])==canonical(case),'P1 finite mutation identity/witness mismatch')
        require(source.count(before)==1,'P1 finite mutation anchor mismatch')
        require(row['changed_source_sha256']==digest(source.replace(before,after).encode()),'P1 changed source digest mismatch')
        require(row['detected'] is True and row['original']!=row['mutant'],'P1 recorded model comparison did not detect its mutation')
    return {'differential_cases':266760,'seeded_boundary_cases':1593,'detected_mutations':[x[0] for x in cases],'credit':'FINITE_COMPARISON_ACCEPT; no rejecting subprocess inferred'}

def _load_receipts(contract,out):
    paths={s['receipt'] for s in contract['stages']}|{contract['terminal_receipt']}
    values={}
    for relative in paths:
        p=safe_file(out,relative)
        if p.is_file():values[relative]=read_json(p)
    return values

def _rows(contract,values):
    indexed={};by_receipt={}
    for spec in contract['stages']:by_receipt.setdefault(spec['receipt'],[]).append(spec)
    for receipt,specs in by_receipt.items():
        if receipt not in values:continue
        head=specs[0];value=values[receipt]
        rows=value if head['rows_field'] is None else value.get(head['rows_field'],[])
        require(isinstance(rows,list),'original command rows are not a list')
        expected=[(s['row_group'],s['label']) for s in specs]
        seen=[]
        for row in rows:
            require(isinstance(row,dict),'original command row is not an object')
            group=row.get('suite') if any(s['row_group'] for s in specs) else None
            label=row.get(head['row_key']);key=(group,label)
            require(key in expected and key not in seen,'unknown/duplicate original child row')
            seen.append(key);indexed[(receipt,group,label)]=row
        require(seen==expected[:len(seen)],'original child order or omission mismatch')
    return indexed

def normalize_child(spec,row,out,roots,alias,object_lookup):
    """Return observed facts only; D03 trace matching remains mandatory."""
    log=safe_file(out,spec['log']);base={'id':spec['id'],'namespace':spec['namespace'],'label':spec['label'],'role':spec['role'],'source_sha256':spec['source']['sha256'],'expected_exit_code':spec['expected_exit_code'],'positive_prerequisites':spec['positive_prerequisites'],'expected_argv':spec['expected_argv'],'argv_provenance':spec['argv_provenance'],'captured_argv':None,'captured_exit_code':None,'trace_binding':'REQUIRED_NOT_SUPPLIED','log_path':spec['log'],'log_sha256':None,'terminal':'NOT_RUN','observed_objects':[],'diagnostic_match':False,'rejection_credit':False,'positive_credit':False,'narrow_findings':[]}
    if row is None:
        if log.is_file():
            text=log.read_text(encoding='utf-8');base['log_sha256']=digest(log.read_bytes())
            if RESOURCE.search(text):base['terminal']='RESOURCE_INCONCLUSIVE'
            else:base['terminal']='UNBOUND_LOG_WITHOUT_CHILD_ROW'
        return base
    src=path_for(spec['source']['path'],roots)
    require(src.is_file() and digest(src.read_bytes())==spec['source']['sha256'],'child source bytes changed: '+spec['id'])
    require(row.get('source_sha256')==spec['source']['sha256'],'child source identity mismatch: '+spec['id'])
    require(log.is_file(),'missing child log: '+spec['id'])
    b=log.read_bytes();text=b.decode('utf-8');actual_hash=digest(b)
    require(row.get(spec['log_hash_field'])==actual_hash,'child log hash mismatch: '+spec['id'])
    if 'log' in row:
        expected='/'.join(x for x in [spec['receipt_log_prefix'],row['log']] if x)
        require(expected==spec['log'],'child log path mismatch: '+spec['id'])
    code=row.get('exit_code')
    require(code is None or type(code) is int,'invalid child exit code')
    if 'expected_exit' in row:require(type(row['expected_exit']) is int and row['expected_exit']==spec['expected_exit_code'],'producer expected-exit mismatch')
    if 'expectation' in row:require(row['expectation']==('REJECT' if spec['expected_exit_code'] else 'ACCEPT'),'producer expectation mismatch')
    base.update(captured_exit_code=code,log_sha256=actual_hash,exit_provenance='RECORDED_BY_ORIGINAL')
    if 'command' in row:
        require(isinstance(row['command'],list) and all(isinstance(x,str) for x in row['command']),'invalid captured argv')
        argv=[neutral(x,roots,alias) for x in row['command']]
        require(argv==spec['expected_argv'],'recorded child argv differs from reviewed recipe: '+spec['id'])
        base['captured_argv']=argv
    else:base['argv_provenance']='DERIVED_FROM_REVIEWED_RECIPE'
    resource=code is None or code in (124,137,143) or (code is not None and code<0) or RESOURCE.search(text) is not None
    base['terminal']='RESOURCE_INCONCLUSIVE' if resource else 'COMPLETED'
    matched=all(x in text for x in spec['diagnostic_literals'])
    base['diagnostic_match']=matched
    if spec['label']=='ExactInheritedCostMutant':
        mismatch=all(x in text for x in ['error: application type mismatch','η ≤ ε : Prop','η ≤ ε / 2 : Prop'])
        if mismatch:
            where=RESOURCE.search(text)
            base['narrow_findings'].append({'kind':'CONCRETE_APPLICATION_MISMATCH','log_sha256':actual_hash,'precedes_resource_diagnostic':where is None or text.index('error: application type mismatch')<where.start(),'does_not_refute_unchanged_positive_statement':True,'does_not_reclassify_historical_receipts':True})
    if spec['expected_exit_code']==1:
        base['rejection_credit']=code==1 and not resource and matched and INFRASTRUCTURE.search(text) is None
        for obj in spec['objects']:require(not safe_file(out,obj['path']).exists(),'rejected child emitted object: '+spec['id'])
    else:
        clean=code==0 and not resource and 'error:' not in text and 'sorryAx' not in text and "declaration uses 'sorry'" not in text
        base['positive_credit']=clean
        if clean:
            base['axiom_readbacks']=axioms(text,spec['axiom_count'],spec.get('axiom_names'))
            for literal,count in spec.get('literal_counts',{}).items():require(text.count(literal)==count,'source-required diagnostic count mismatch')
            for obj in spec['objects']:
                p=safe_file(out,obj['path']);require(p.is_file(),'missing fresh output: '+obj['path']);h=digest(p.read_bytes())
                field=obj['row_hash_field'];recorded=row.get(field) if field else object_lookup.get(obj['path'])
                if recorded is not None:require(recorded==h,'object hash mismatch: '+obj['path'])
                base['observed_objects'].append({'path':obj['path'],'sha256':h,'recorded_hash':recorded,'freshness':'REQUIRES_FIRST_RUN_TRACE_BINDING'})
            if spec['c_output']:
                p=safe_file(out,spec['c_output']);require(p.is_file() and p.stat().st_size>0,'missing C emission')
                require(row.get('c_sha256')==digest(p.read_bytes()) and row.get('c_bytes')==p.stat().st_size,'C output binding mismatch')
                base['c_output']={'path':spec['c_output'],'sha256':digest(p.read_bytes()),'bytes':p.stat().st_size}
    return base

def _final_checks(c,out,values,roots):
    top=values[c['terminal_receipt']];checks=[]
    for path,expected in c['receipt_constraints']:
        actual=pointer(top,path)
        require(type(actual) is type(expected) and actual==expected,'terminal source-required field mismatch: '+path)
    def hashed(relative, expected):
        p=safe_file(out,relative);require(p.is_file() and digest(p.read_bytes())==expected,'receipt/output hash mismatch: '+relative)
    if c['id']=='portable':
        hashed('core/RESULT.json',top['core_receipt_sha256']);hashed('literal/RESULT.json',top['literal_receipt_sha256'])
        hashed('literal_portable_driver.py',c['derived_literal_driver_sha256'])
        core=values['core/RESULT.json'];lit=values['literal/RESULT.json']
        require(core['status']=='PASS_INDEPENDENT_REVIEW_CHECKS' and lit['status']=='PASS_INDEPENDENT_LITERAL_ADDENDUM','inner terminal status missing')
        require(core['runner_sha256']==c['inner_driver_sources'][0]['sha256'],'wrong executed core driver')
        require(lit['runner_sha256']==c['derived_literal_driver_sha256'],'wrong executed derived literal driver')
        require(core['runtime']['source_shape_controls']=='PASS_SYNTACTIC_ONLY','source-shape control was promoted')
        require(core['old_runtime_mutant_recompiled'] is False,'historical mutant was rerun')
        hashed('core/RESULT.json',lit['core_receipt_sha256']);hashed('literal/OWN_FRESH_CORE_BINDINGS.json',lit['core_bindings_sha256'])
        bindings=read_json(safe_file(out,'literal/OWN_FRESH_CORE_BINDINGS.json'))
        require(len(bindings)==167 and len({x['module'] for x in bindings})==167,'literal inherited object census')
        core_rows={r['label']:r for r in core['runs'] if r['suite']=='runtime' and 'object_sha256' in r}
        for row in bindings:
            other=core_rows[row['module']];require(row['source_sha256']==other['source_sha256'] and row['object_sha256']==other['object_sha256'],'literal source/object join mismatch')
            hashed('core/runtime/build/'+row['module'].replace('.','/')+'.olean',row['object_sha256'])
        hashed('literal/NATIVE_RESULT.json',lit['native_receipt_sha256']);hashed('literal/logs/native.log',lit['native_log_sha256'])
        native=read_json(safe_file(out,'literal/NATIVE_RESULT.json'))
        require(len(native['cases'])==340 and all(x['actual']==x['expected'] for x in native['cases']),'literal reference cases mismatch')
        numerals=safe_file(out,'literal/logs/SelectorNumeralReadback.log').read_text()
        require('44812' in numerals and '24332' in numerals and numerals.count('428783445879334172098560')==2 and numerals.count('64080')==2,'literal numeral readback mismatch')
        expected={'OLD_FALSE':'40f25f3bd087bfb672d9a390913e6959bd399d6bfa90889d4c4d935f91c4eb40','OLD_TRUE':'1bc2df93721979bb9806940d69d03a331d87964b61fb35e1de15fafcc3314424','COMPUTED_FALSE':'08ed35c82f63c180f1c5ea4778efbbebc70521cec514bf9870ab91c558eb7908','COMPUTED_TRUE':'d1a9ed7903def5a682f334d816ab3615bd2f8ef9b350149442404ca1fcd4712f'}
        require({x['name']:x['sha256'] for x in lit['programs']}==expected,'program receipt census')
        for name,h in expected.items():
            hashed('literal/programs/'+name+'.bin',h);require(safe_file(out,'literal/programs/'+name+'.bin').stat().st_size==48389,'program byte count')
        checks.append('Portable wrapper, core, literal, dependency object join, exact programs and bounded case ledger bound.')
    elif c['id']=='selector':
        ref=read_json(path_for('{root:selector}/evidence/FINITE_CONTROLS.json',roots))
        observed=read_json(safe_file(out,'finite-controls/evidence/FINITE_CONTROLS.json'))
        require(canonical(ref)==canonical(observed),'finite control JSON mismatch')
        guards=read_json(safe_file(out,'original-census-controls/evidence/REPLAY_GUARDS.json'))
        require(guards['status']=='PASS_FROZEN_CENSUS_HELPER_CONTROLS' and len(guards['cases'])==6,'guard census mismatch')
        expected=['positive','extra-object','missing-object','symlink','wrong-object-digest','wrong-source-digest']
        require([x['case'] for x in guards['cases']]==expected,'guard case identity/order mismatch')
        require(all(x['accepted'] is (x['case']=='positive') and x['expected_outcome_observed'] is True for x in guards['cases']),'guard case disposition mismatch')
        require(guards['lean_processes_started'] is False and guards['dependency_objects_changed'] is False,'census helper scope changed')
        checks.append('Original finite JSON and six frozen census guards bound; external fresh core join remains adapter-owned.')
    elif c['id']=='p1':
        hashed('COMMANDS.json',top['commands_sha256'])
        actual={p.relative_to(Path(out)/'build').as_posix():digest(p.read_bytes()) for p in (Path(out)/'build').rglob('*.olean')}
        require(actual=={x['path']:x['sha256'] for x in top['objects']} and len(actual)==9,'P1 custom object census mismatch')
        obs=read_json(safe_file(out,'control-layout/tranche9/reviews/python-runtime-refinement/evidence/INDEPENDENT_SOURCE_CONTROLS.json'))
        p1_comparison_records(obs,path_for('{root:p1}/source/prcodec.py',roots).read_bytes(),path_for('{root:p1}/reviewer/independent_source_controls.py',roots).read_bytes())
        checks.append('Original command digest, nine object hashes, complete independent finite case ledger bound.')
    else:checks.append('Original complete child order and explicit terminal conditions bound; exact external dependency join remains adapter-owned where declared.')
    return checks

def object_census(contract,out):
    """Only formal build roots: do not mistake selector's dummy census fixtures
    for compiler outputs. Original modules, codegen and mutant roots stay apart.
    """
    expected={}
    for spec in contract['stages']:
        for obj in spec['objects']:
            suffix=obj['module'].replace('.','/')+'.olean'
            require(obj['path'].endswith('/'+suffix),'object module suffix mismatch')
            root=obj['path'][:-len(suffix)].rstrip('/')
            expected.setdefault(root,set())
            if spec['expected_exit_code']==0:expected[root].add(suffix)
    for root,names in expected.items():
        base=safe_file(out,root);require(base.is_dir(),'missing formal build root')
        require(not any(p.is_symlink() for p in base.rglob('*')),'symlink in formal build root')
        actual={p.relative_to(base).as_posix() for p in base.rglob('*.olean')}
        require(actual==names,'unexpected/missing compiler object census: '+root)

def normalize(contract,out,roots):
    """Read original outputs, returning no D02/D03 acceptance or execution claim.

    roots maps contract tokens (out,root:core,tool:lean,... ) to live private
    paths. Exact source bytes, log bytes and existing object hashes are checked.
    Captured first-run process argv/times/terminal/freshness must be joined by D03.
    """
    require(contract['schema']=='PRIVATE-ORIGINAL-CHILD-CONTRACT-1','wrong private contract')
    clone={k:v for k,v in contract.items() if k!='source_contract_digest'}
    require(digest(canonical(clone))==contract['source_contract_digest'],'private contract changed')
    out=Path(out).resolve(strict=True);roots=dict(roots);roots['out']=out
    require(out.is_dir(),'output absent')
    values=_load_receipts(contract,out);rows=_rows(contract,values)
    top=values.get(contract['terminal_receipt']);terminal=top.get('status') if isinstance(top,dict) else None
    objects={('build/'+x['path']):x['sha256'] for x in (top or {}).get('objects',[])}
    children=[]
    for spec in contract['stages']:
        row=rows.get((spec['receipt'],spec['row_group'],spec['label']))
        children.append(normalize_child(spec,row,out,roots,contract['id'],objects))
    by_id={x['id']:x for x in children}
    for child in children:
        if child['rejection_credit']:
            require(all(by_id[x]['positive_credit'] for x in child['positive_prerequisites']),'negative child lacks its full positive prerequisites')
    complete=terminal==contract['terminal_status']
    final_checks=_final_checks(contract,out,values,roots) if complete else []
    if complete:
        require(all(x['terminal']!='NOT_RUN' for x in children),'original terminal omitted a required child')
        require(all(x['positive_credit'] for x in children if x['expected_exit_code']==0),'completed original has an invalid positive child')
        require(all(x['rejection_credit'] or x['terminal']=='RESOURCE_INCONCLUSIVE' for x in children if x['expected_exit_code']==1),'completed original has an invalid rejecting child')
        object_census(contract,out)
    aux=[]
    for spec in contract.get('auxiliary_children',[]):
        row={'id':spec['id'],'expected_argv':spec['expected_argv'],'captured_argv':None,'captured_exit_code':None,'argv_provenance':'DERIVED_FROM_REVIEWED_RECIPE','exit_provenance':'NOT_RECORDED_BY_ORIGINAL','trace_binding':'REQUIRED_NOT_SUPPLIED','terminal_asserted_by_original':complete,'log_path':spec['log'],'log_sha256':None}
        log=safe_file(out,spec['log'])
        if log.is_file():row['log_sha256']=digest(log.read_bytes())
        if complete:
            require(log.is_file(),'missing auxiliary log');source=path_for(spec['source']['path'],roots)
            require(digest(source.read_bytes())==spec['source']['sha256'],'auxiliary source drift')
            observed=read_json(safe_file(out,spec['receipt']))
            if 'status' in spec:require(observed.get('status')==spec['status'],'auxiliary status mismatch')
            for path,expected in spec.get('constraints',[]):require(pointer(observed,path)==expected,'auxiliary field mismatch')
        aux.append(row)
    return {'scope':'ORIGINAL_OUTPUT_CONTRACT_ONLY','full_receipt_qualified':False,'reason':'D03 first-run child tracing, fresh build provenance, exact descriptor/target audit and shared dependency bindings are mandatory.','contract_id':contract['id'],'contract_sha256':digest(canonical(contract)),'original_terminal':terminal,'original_full_terminal_present':complete,'children':children,'auxiliary_children':aux,'full_checks':final_checks,'resource_children':[x['id'] for x in children if x['terminal']=='RESOURCE_INCONCLUSIVE'],'not_run_children':[x['id'] for x in children if x['terminal']=='NOT_RUN']}
