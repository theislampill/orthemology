#!/usr/bin/env python3
"""Validate origin-bound continuation sources and evidence; integrity is not proof."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

AREA = 'experiments/orthemology-v5-continuations'
PROV = 'docs/provenance/v5-research-continuations'
AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
OFFICIAL = {'Mathlib','Batteries','Lean','Std','Init','Aesop','Qq','ProofWidgets','Plausible','ImportGraph','LeanSearchClient','Cli'}
CLASSIFICATIONS = {'COLLECTION','CURRENT_EVIDENCE','PREDECESSOR','SUPERSEDED','REJECTED','RECOVERY_ONLY','CONTEXTUAL','UNRESOLVED'}
FORMS = {'FORMAL','ORDINARY','MIXED','CONDITIONAL','IMPLEMENTATION','PROPOSAL'}
INHERITED = {'RETAINED_FORMAL_REVIEW','RETAINED_FORMAL_AND_FINITE','MIXED_RETAINED_EVIDENCE',
             'MIXED_FORMAL_AND_ORDINARY','ORDINARY_REVIEW_AND_FINITE','SOURCE_RECOVERY_ORDINARY_AND_FINITE',
             'ORDINARY_REVIEW','ORDINARY_REVIEW_WITH_FORMAL_SUBCLAIMS','MIXED_FORMAL_ORDINARY_AND_FINITE',
             'IMPLEMENTATION_AND_ORDINARY_REVIEW','RETAINED_FORMAL_REVIEW_PLUS_ORDINARY_COROLLARIES',
             'RETAINED_FORMAL_AND_SOURCE_REVIEW','FORMAL_ARITHMETIC_AND_IMPLEMENTATION_REVIEW',
             'CONDITIONAL_PHILOSOPHY_WITH_FORMAL_MODELS','NONE'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def keys(value, required, optional=()):
    require(isinstance(value, dict), 'Expected an object')
    require(set(required) <= value.keys() <= set(required) | set(optional),
            'Missing or unknown fields: ' + repr(set(value) ^ set(required)))


def digest(value):
    require(isinstance(value, str) and re.fullmatch('[0-9a-f]{64}', value), 'Invalid SHA-256')
    return value


def nonempty(value):
    require(isinstance(value, str) and bool(value.strip()), 'Expected nonempty text')
    return value


def enum(value, choices):
    require(isinstance(value, str) and value in choices, 'Unknown or empty enum: '+repr(value))


def safe_relative(name):
    nonempty(name)
    p = PurePosixPath(name)
    require(not p.is_absolute() and '\\' not in name and ':' not in name and '\0' not in name
            and all(x not in {'','.','..'} for x in name.split('/')), 'Unsafe path: '+name)
    return p


def path_in(root, name, exists=True):
    p=safe_relative(name)
    target = root.joinpath(*p.parts)
    require(target.resolve().is_relative_to(root.resolve()), 'Escaping path: '+name)
    current=root
    for part in p.parts:
        current=current/part
        require(not current.is_symlink(), 'Symlink path: '+name)
    if exists: require(target.is_file(), 'Missing regular file: '+name)
    return target


def read_json(path):
    def pairs(rows):
        result={}
        for name,value in rows:
            require(name not in result, 'Duplicate JSON key: '+name)
            result[name]=value
        return result
    def constant(value):
        raise ValueError('Nonfinite JSON value: '+value)
    return json.loads(Path(path).read_text(encoding='utf-8'), object_pairs_hook=pairs, parse_constant=constant)


def indexed(rows, key):
    require(isinstance(rows,list), 'Expected list')
    result={}
    for row in rows:
        require(isinstance(row,dict) and key in row, 'Missing row identity')
        name=nonempty(row[key]);require(name not in result,'Duplicate identity: '+name);result[name]=row
    return result


def check_public_text(text):
    private = r'(?:/mnt/' + r'(?:data|c/Users|c/workspace)|/(?:home/(?:oai|agent)|tmp)/|[A-Za-z]:[\\/](?:Users|workspace)[\\/]|sandbox:)'
    credential = r'ghp_' + r'[A-Za-z0-9]{30,}|github_pat_' + r'[A-Za-z0-9_]{40,}|-----BEGIN [A-Z ]*PRIVATE KEY-----'
    require(not re.search(private+'|'+credential,text), 'Private locator or credential in public content')


def strip_comments(text):
    """Handle nested Lean comments without treating quoted strings as comments."""
    out=[];i=0;depth=0;quote=False
    while i<len(text):
        if depth:
            if text.startswith('/-',i):depth+=1;i+=2
            elif text.startswith('-/',i):depth-=1;i+=2
            else:
                if text[i]=='\n':out.append('\n')
                i+=1
        elif quote:
            out.append(text[i])
            if text[i]=='\\' and i+1<len(text):i+=1;out.append(text[i])
            elif text[i]=='"':quote=False
            i+=1
        elif text.startswith('/-',i):depth=1;i+=2
        elif text.startswith('--',i):
            end=text.find('\n',i);i=len(text) if end<0 else end
        else:
            if text[i]=='"':quote=True
            out.append(text[i]);i+=1
    require(depth==0,'Unclosed Lean comment')
    return ''.join(out)


def lean_imports(text):
    return [name for line in re.findall(r'^\s*import\s+([^\n]+)',strip_comments(text),re.M) for name in line.split()]


def check_lean(text):
    code=re.sub(r'"(?:\\.|[^"\\])*"','""',strip_comments(text))
    require(not re.search(r'\b(sorry|admit|sorryAx|native_decide|unsafe|axiom)\b|debug\.skipKernelTC|^\s*(?:(?:private|protected)\s+)?constant\s',code,re.M),
            'Unapproved proof hole, axiom, or unsafe source')


def module_name(name):
    require(isinstance(name,str) and re.fullmatch(r"[A-Za-z_][\w']*(?:\.[A-Za-z_][\w']*)*",name), 'Invalid module/target name')


def declared_targets(text):
    scopes=[];names=[]
    for line in strip_comments(text).splitlines():
        line=line.strip()
        m=re.match(r'namespace\s+(\S+)',line)
        if m:scopes.append(('namespace',m[1]));continue
        m=re.match(r'(?:noncomputable\s+)?(section|mutual)(?:\s+(\S+))?$',line)
        if m:scopes.append(('section',m[2]));continue
        if re.match(r'end(?:\s+\S+)?$',line):
            if scopes:scopes.pop()
            continue
        m=re.match(r"(?:@\[[^]]*\]\s*)*(?:(?:noncomputable|protected|nonrec)\s+)*(?:def|abbrev|lemma|theorem|instance|structure|inductive|class)\s+(«[^»]+»|[\w'.]+)",line)
        if m:names.append('.'.join([v for k,v in scopes if k=='namespace']+[m[1].strip('«»')]))
    return set(names)


def owner_contains(path, statement, cache=None):
    cache={} if cache is None else cache
    if path not in cache:
        text=path.read_text(encoding='utf-8')
        values=[json.loads(line) for line in text.splitlines() if line.strip()] if path.suffix=='.jsonl' else [json.loads(text)] if path.suffix=='.json' else []
        cache[path]=(text,values)
    text,values=cache[path]
    if statement in text:return True
    if path.suffix not in {'.json','.jsonl'}:return False
    def contains(value):
        if isinstance(value,str):return value==statement
        if isinstance(value,dict):
            return json.dumps(value,sort_keys=True,ensure_ascii=False)==statement or any(contains(v) for v in value.values())
        if isinstance(value,list):return any(contains(v) for v in value)
        return False
    return any(contains(value) for value in values)


def validate_suite(suite, sources, root, parsed_sources=None):
    parsed_sources={} if parsed_sources is None else parsed_sources
    keys(suite, {'id','origin','descriptor_source_id','modules','module_order','targets','pins','official_imports','driver','controls','classification'})
    require(re.fullmatch(r'[a-z0-9][a-z0-9_-]*',suite['id']), 'Unsafe suite ID')
    digest(suite['origin']);enum(suite['classification'],CLASSIFICATIONS)
    require(suite['descriptor_source_id'] in sources,'Missing original suite descriptor')
    require(sources[suite['descriptor_source_id']]['origin']==suite['origin'],'Descriptor origin mismatch')
    keys(suite['driver'],{'source_id','lean_argument'})
    require(suite['driver']['source_id'] in sources,'Missing original driver binding')
    enum(suite['driver']['lean_argument'],{'EXECUTABLE','BIN_DIRECTORY','ENVIRONMENT_DIRECTORY','NOT_SPECIFIED'})
    enum(suite['controls'],{'ORIGINAL_DRIVER_REQUIRED','DECLARED_SOURCE_CONTROLS'})
    mods=indexed(suite['modules'],'module');require(mods,'Empty suite')
    order=suite['module_order']
    require(isinstance(order,list) and len(order)==len(set(order)) and set(order)==set(mods),'Module order/census mismatch')
    official=indexed(suite['official_imports'],'module')
    for name,row in official.items():
        keys(row,{'module','repository','source','sha256'});module_name(name);digest(row['sha256'])
        require(name.split('.')[0] in OFFICIAL,'Unknown official namespace')
        require(row['source']==name.replace('.','/')+'.lean','Official source/module mismatch')
    seen=set();owners={}
    for name in order:
        module_name(name);row=mods[name];keys(row,{'module','source_id','imports'})
        require(name.split('.')[0] not in OFFICIAL,'Custom source shadows official namespace')
        require(row['source_id'] in sources,'Missing source binding: '+name)
        source=sources[row['source_id']]
        require(source['path'] is not None and source['path'].endswith('.lean'),'Custom module has no projected Lean source')
        if source['path'] not in parsed_sources:
            text=path_in(root,source['path']).read_text(encoding='utf-8');check_lean(text)
            parsed_sources[source['path']]=(lean_imports(text),declared_targets(text))
        imports,declared=parsed_sources[source['path']]
        require(row['imports']==imports,'Source/import mismatch: '+name)
        for dep in row['imports']:
            require(dep in seen or dep in official,'Missing, cyclic, or unordered import: '+name+' -> '+dep)
        for target in declared:owners.setdefault(target,set()).add(name)
        seen.add(name)
    targets=indexed(suite['targets'],'name');require(targets,'Empty target inventory')
    for name,row in targets.items():
        keys(row,{'name','module'});module_name(name)
        require(row['module'] in mods and owners.get(name)=={row['module']},'Wrong or ambiguous target owner: '+name)
    pins=suite['pins'];keys(pins,{'lean_version','lean_binary_sha256','packages'})
    require(pins['lean_version']=='4.19.0','Wrong Lean version');digest(pins['lean_binary_sha256'])
    require(pins['lean_binary_sha256']=='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023','Wrong official Linux compiler pin')
    packages=indexed(pins['packages'],'name')
    require('mathlib' in packages and packages['mathlib']['revision']=='c44e0c8ee63ca166450922a373c7409c5d26b00b','Wrong Mathlib pin')
    for row in packages.values():
        keys(row,{'name','revision'})
        require(re.fullmatch(r'[A-Za-z][A-Za-z0-9_-]*',row['name']),'Unsafe package name')
        require(re.fullmatch('[0-9a-f]{40}',row['revision']),'Unpinned package')
    require(all(r['repository'] in packages or r['repository']=='lean-release' for r in official.values()),'Official import has no package owner')


def suite_fingerprints(suite, sources):
    rows={r['module']:r for r in suite['modules']};official={r['module']:r for r in suite['official_imports']};result={}
    for name in suite['module_order']:
        row=rows[name];deps={d:result[d] if d in rows else official[d] for d in row['imports']}
        result[name]=hashlib.sha256(json.dumps({'module':name,'source':sources[row['source_id']]['sha256'],
                                              'dependencies':deps,'pins':suite['pins']},sort_keys=True).encode()).hexdigest()
    return result


def validate_receipt(receipt, suite, suite_path, sources, context=None, active=()):
    require(isinstance(receipt,dict),'Expected receipt object')
    require(receipt.get('status')=='FRESH_KERNEL_COMPONENTS' and receipt.get('kernel_verified') is True,'Not a fresh kernel component receipt')
    require(type(receipt.get('exit_code')) is int and receipt['exit_code']==0,'Receipt has no successful terminal exit')
    require(receipt.get('suite_id')==suite['id'] and receipt.get('suite_sha256')==sha(suite_path),'Stale/foreign suite receipt')
    expected={m['module']:sources[m['source_id']]['sha256'] for m in suite['modules']}
    require(receipt.get('source_hashes')==expected and receipt.get('post_source_hashes')==expected,'Stale source receipt')
    require(receipt.get('compiler_sha256')==suite['pins']['lean_binary_sha256'],'Receipt compiler mismatch')
    require(receipt.get('pins')==suite['pins'],'Receipt dependency pins mismatch')
    modules=indexed(receipt.get('modules',[]),'module')
    require(set(modules)==set(expected),'Incomplete compiled closure')
    fingerprints=suite_fingerprints(suite,sources)
    for name,row in modules.items():
        if row.get('status')=='FRESH_COMPILE':
            require(type(row.get('exit_code')) is int and row['exit_code']==0,'Unqualified custom object')
        else:
            require(row.get('status')=='QUALIFIED_PREDECESSOR' and context is not None,'Unqualified predecessor object')
            rel=row.get('predecessor_receipt');require(rel not in active,'Receipt dependency cycle')
            cache=context.setdefault('validated_receipts',{})
            if rel not in cache:
                path=path_in(context['root'],rel);actual_sha=sha(path)
                prior=read_json(path);require(isinstance(prior,dict),'Expected predecessor receipt object')
                sid=prior.get('suite_id');require(sid in context['suites'],'Unknown predecessor suite')
                validate_receipt(prior,context['suites'][sid],context['paths'][sid],sources,context,(*active,rel))
                cache[rel]=(actual_sha,prior)
            actual_sha,prior=cache[rel]
            require(actual_sha==row.get('predecessor_receipt_sha256'),'Changed predecessor receipt')
            before=indexed(prior.get('modules',[]),'module').get(name,{})
            for key in ['source_sha256','object_sha256','transitive_source_fingerprint']:
                require(before.get(key)==row.get(key),'Predecessor source/object/transitive binding mismatch')
        require(row.get('source_sha256')==expected[name],'Object/source mismatch');digest(row.get('object_sha256'))
        require(row.get('transitive_source_fingerprint')==fingerprints[name],'Wrong transitive source fingerprint')
    readbacks=receipt.get('readbacks',{})
    require(set(readbacks)=={t['name'] for t in suite['targets']},'Incomplete readback')
    for name,row in readbacks.items():
        if 'type' in row:
            nonempty(row['type']);require(re.match(r'^@?'+re.escape(name)+r'(?:\.\{[^}]*\})?\s*:',row['type']),'Wrong receipt declaration type')
        else:digest(row.get('type_sha256'))
        require(isinstance(row.get('axioms'),list) and set(row['axioms'])<=AXIOMS,'Unapproved axiom')


def statement_digest(row):
    statement={k:row[k] for k in ['id','origin','claim','limit','math_form','implementation']}
    return hashlib.sha256(json.dumps(statement,sort_keys=True,ensure_ascii=False).encode()).hexdigest()


def source_identities(ids, sources):
    return {sid:{'original_sha256':sources[sid]['original_sha256'],'public_sha256':sources[sid]['sha256']} for sid in ids}


def result_targets(row, suite, sources):
    """Only targets owned by this family's actual sources, allowing exact aliases."""
    mods=indexed(suite['modules'],'module');by_hash={}
    for sid in sorted(row['source_ids']):
        if sources[sid]['sha256'] is not None:by_hash.setdefault(sources[sid]['sha256'],sid)
    targets={}
    for target in suite['targets']:
        sid=mods[target['module']]['source_id']
        owner=sid if sid in row['source_ids'] else by_hash.get(sources[sid]['sha256'])
        if owner is not None:targets[target['name']]=owner
    return targets


def validate_association(binding, row, suites, sources):
    keys(binding,{'id','statement_sha256','sources','reviews','suite_targets'})
    require(binding['statement_sha256']==statement_digest(row),'Changed result statement association')
    require(binding['sources']==source_identities(row['source_ids'],sources),'Changed result source association')
    require(binding['reviews']==source_identities(row['review_source_ids'],sources),'Changed result review association')
    bound=indexed(binding['suite_targets'],'suite_id')
    require(set(bound)==set(row['suite_ids']),'Changed result suite association')
    for sid,entry in bound.items():
        keys(entry,{'suite_id','targets'})
        expected=result_targets(row,suites[sid],sources)
        require(bool(expected) and entry['targets']==expected,'Wrong result target/source binding: '+sid)


def validate_qualified_controls(rec, suite, sources, contracts, root):
    require(rec.get('original_controls')=='PASS','Original controls not qualified')
    driver=suite['driver']['source_id']
    require(rec.get('original_driver_sha256')==sources[driver]['original_sha256'],'Missing or foreign original control driver')
    require(isinstance(rec.get('original_receipt_sha256'),str),'Missing original control receipt')
    digest(rec['original_receipt_sha256'])
    require(suite['id'] in contracts,'Missing original control contract')
    contract=contracts[suite['id']]
    keys(contract,{'suite_id','driver_source_id','review_driver_source_id','control_source_ids','stages','receipt','sha256'})
    require(contract['driver_source_id']==driver,'Control contract driver mismatch')
    require(contract['review_driver_source_id'] in contract['control_source_ids'],'Control review driver not registered')
    require(all(sid in sources for sid in contract['control_source_ids']),'Unknown control source')
    path=path_in(root,contract['receipt'])
    require(sha(path)==digest(contract['sha256']),'Changed control receipt')
    control=read_json(path)
    keys(control,{'status','exit_code','suite_id','suite_sha256','source_hashes','driver_source_id','driver_sha256',
                  'original_receipt_sha256','review_driver_source_id','review_driver_sha256','review_receipt_sha256',
                  'control_sources','stages','counts','scope'})
    require(control['status']=='PASS' and type(control['exit_code']) is int and control['exit_code']==0,'Controls have no successful terminal exit')
    require(control['suite_id']==suite['id'] and control['suite_sha256']==rec['suite_sha256']
            and control['source_hashes']==rec['source_hashes'],'Foreign control source closure')
    require(control['driver_source_id']==driver and control['driver_sha256']==rec['original_driver_sha256']
            and control['original_receipt_sha256']==rec['original_receipt_sha256'],'Control driver/receipt binding mismatch')
    review_driver=contract['review_driver_source_id']
    require(control['review_driver_source_id']==review_driver and control['review_driver_sha256']==sources[review_driver]['original_sha256'],
            'Foreign control review driver')
    digest(control['review_receipt_sha256'])
    require(control['control_sources']=={sid:sources[sid]['original_sha256'] for sid in contract['control_source_ids']},'Changed control source binding')
    stages=indexed(control['stages'],'stage')
    require(bool(stages) and set(stages)==set(contract['stages']),'Incomplete original control stages')
    for stage in stages.values():
        keys(stage,{'stage','exit_code','log_sha256'})
        require(type(stage['exit_code']) is int and stage['exit_code']==0,'Original control stage failed')
        digest(stage['log_sha256'])
    require(isinstance(control['counts'],dict) and all(type(x) is int and x>=0 for x in control['counts'].values()),'Invalid control counts')
    nonempty(control['scope']);check_public_text(control['scope'])


def _validate(root):
    registry=read_json(root/AREA/'registry.json')
    keys(registry,{'schema','programme','cutoff','source_map','result_status','supersession','obligations','lineages','evidence_bindings','suites','results'})
    require(registry['schema']=='orthemology-v5-continuations-v1' and registry['programme']=='Orthemology v5','Wrong programme/schema')
    require(registry['cutoff']=='sixth-tranche-checkpoint-3','Wrong research cutoff')
    data={name:read_json(path_in(root,registry[name])) for name in ['source_map','result_status','supersession','obligations','lineages']}
    archives=indexed(data['lineages']['archives'],'sha256')
    for ident,row in archives.items():
        digest(ident);enum(row['classification'],CLASSIFICATIONS);nonempty(row['basis'])
        require(type(row['bytes']) is int and row['bytes']>0,'Invalid archive size')
        for parent in row['parents']:
            require(parent['archive'] in archives,'Unknown parent archive');nonempty(parent['member'])
    sources=indexed(data['source_map']['sources'],'id');require(sources,'Empty source map')
    checked_files={}
    for row in sources.values():
        keys(row,{'id','origin','member','original_sha256','original_bytes','path','sha256','bytes','projection','derivation'})
        require(row['origin'] in archives,'Unknown source origin');safe_relative(row['member'])
        digest(row['original_sha256']);require(type(row['original_bytes']) is int and row['original_bytes']>=0,'Invalid original byte count')
        enum(row['projection'],{'EXACT','DERIVED','CUSTODY_ONLY'})
        if row['projection']=='CUSTODY_ONLY':
            require(row['path'] is None and row['sha256'] is None and row['bytes'] is None and row['derivation'] is None,'Custody is not public projection')
            continue
        digest(row['sha256']);require(type(row['bytes']) is int and row['bytes']>=0,'Invalid byte count')
        if row['path'] not in checked_files:
            p=path_in(root,row['path']);require(p.suffix in {'.lean','.md','.json','.py','.txt','.yaml','.p02'},'Forbidden public source type')
            raw=p.read_bytes();check_public_text(raw.decode('utf-8'))
            checked_files[row['path']]=(len(raw),hashlib.sha256(raw).hexdigest())
        require(checked_files[row['path']]==(row['bytes'],row['sha256']),'Source digest/size mismatch: '+row['id'])
        if row['projection']=='EXACT':
            require(row['sha256']==row['original_sha256'] and row['bytes']==row['original_bytes'] and row['derivation'] is None,'False exact-source claim')
        else:
            d=row['derivation'];keys(d,{'method','diff_sha256','review_status'});nonempty(d['method']);digest(d['diff_sha256'])
            require(d['review_status']=='REVIEWED','Unreviewed public derivation')
    suites={};suite_paths={};parsed_sources={}
    require(isinstance(registry['suites'],list),'Invalid suites')
    for rel in registry['suites']:
        path=path_in(root,rel);suite=read_json(path)
        require(suite['id'] not in suites,'Duplicate suite ID');validate_suite(suite,sources,root,parsed_sources)
        suites[suite['id']]=suite;suite_paths[suite['id']]=path
    results=indexed(registry['results'],'id');require(results,'Empty result registry')
    evidence=read_json(path_in(root,registry['evidence_bindings']))
    keys(evidence,{'schema','results','control_contracts'})
    require(evidence['schema']=='orthemology-v5-evidence-bindings-v1','Unknown evidence binding schema')
    bindings=indexed(evidence['results'],'id');require(set(bindings)==set(results),'Missing result evidence association')
    contracts=indexed(evidence['control_contracts'],'suite_id')
    require(set(contracts)<=set(suites),'Unknown control contract suite')
    statuses=indexed(data['result_status']['results'],'id');require(set(statuses)==set(results),'Missing/unexpected result status')
    for name,row in results.items():
        keys(row,{'id','origin','title','claim','limit','source_ids','review_source_ids','suite_ids','math_form','implementation'})
        require(row['origin'] in archives,'Unknown result origin')
        for field in ['title','claim','limit']:nonempty(row[field]);check_public_text(row[field])
        enum(row['math_form'],FORMS)
        enum(row['implementation'],{'MATHEMATICAL_POLICY','FORMAL_COMPONENT','EFFECTIVE_ALGORITHM','SOURCE_PROGRAM','RUNTIME_COMPONENT','FINITE_EXECUTION','NONE'})
        require(row['source_ids'] and row['review_source_ids'],'Result requires actual source and review')
        require(all(x in sources for x in row['source_ids']+row['review_source_ids']),'Missing result source/review')
        require(any(sources[x]['origin']==row['origin'] for x in row['source_ids']+row['review_source_ids']),'Mismatched result origin')
        require(all(x in suites for x in row['suite_ids']),'Unknown result suite')
        validate_association(bindings[name],row,suites,sources)
        status=statuses[name]
        keys(status,{'id','custody','inherited','fresh','adoption','receipts','external_warrant'})
        enum(status['custody'],{'EXACT','VERIFIED_DERIVED','PARTIAL'});enum(status['inherited'],INHERITED)
        enum(status['fresh'],{'NOT_RUN','BLOCKED','FAILED','FINITE_ONLY','FRESH_COMPONENTS','QUALIFIED'})
        enum(status['adoption'],{'CANDIDATE','DEFERRED','REJECTED'})
        keys(status['external_warrant'],{'empirical','normative','external_peer_review','novelty'})
        for v in status['external_warrant'].values():enum(v,{'NOT_ESTABLISHED','NOT_APPLICABLE'})
        require(isinstance(status['receipts'],list),'Invalid receipt list')
        verified=set()
        for rel in status['receipts']:
            rec=read_json(path_in(root,rel));require(isinstance(rec,dict),'Expected receipt object');sid=rec.get('suite_id')
            require(sid in row['suite_ids'],'Receipt not owned by result')
            validate_receipt(rec,suites[sid],suite_paths[sid],sources,{'root':root,'suites':suites,'paths':suite_paths},(rel,));verified.add(sid)
            if status['fresh']=='QUALIFIED':validate_qualified_controls(rec,suites[sid],sources,contracts,root)
        if status['fresh'] in {'QUALIFIED','FRESH_COMPONENTS'}:require(bool(verified),'Missing fresh receipt')
        if status['fresh']=='QUALIFIED':
            require(row['math_form']=='FORMAL' and bool(row['suite_ids']) and verified==set(row['suite_ids']),'Illegal promotion of ordinary/conditional/partial evidence')
    graph={};statements={}
    for edge in data['supersession']['edges']:
        keys(edge,{'from','to','statement','relation'})
        require(edge['from'] in sources and edge['to'] in sources,'Unknown supersession endpoint')
        nonempty(edge['statement']);enum(edge['relation'],{'SUPERSEDES','REFINES','CORRECTS'})
        key=(edge['from'],edge['statement']);require(key not in statements,'Contradictory/duplicate supersession')
        statements[key]=edge['to'];graph.setdefault(edge['from'],[]).append(edge['to'])
    def walk(node,active,done):
        require(node not in active,'Supersession cycle')
        if node in done:return
        for child in graph.get(node,[]):walk(child,active|{node},done)
        done.add(node)
    done=set()
    for node in graph:walk(node,set(),done)
    owner_hashes={};owner_cache={}
    for row in indexed(data['obligations']['obligations'],'id').values():
        keys(row,{'id','owner_path','owner_sha256','statement','result_ids','disposition','residual'})
        if row['owner_path'] not in owner_hashes:owner_hashes[row['owner_path']]=sha(path_in(root,row['owner_path']))
        require(owner_hashes[row['owner_path']]==row['owner_sha256'],'Changed obligation owner')
        nonempty(row['statement']);nonempty(row['residual']);enum(row['disposition'],{'PRESERVED_OPEN','SCOPED_SUCCESSOR','PRESERVED_STATUS'})
        require(owner_contains(root/row['owner_path'],row['statement'],owner_cache),'Obligation statement does not match its exact owner')
        require(all(x in results for x in row['result_ids']),'Unknown obligation successor')
    return {'status':'SOURCE_AND_STATUS_INTEGRITY_PASS','results':len(results),'sources':len(sources),'suites':len(suites),
            'archives':len(archives),'fresh_qualified_results':sum(r['fresh']=='QUALIFIED' for r in statuses.values()),
            'scope':'Source/status consistency only; no kernel, empirical, normative or adoption credit.'}


def validate(root: Path) -> dict:
    try:return _validate(Path(root).resolve())
    except (KeyError,TypeError,OSError) as exc:raise ValueError('Malformed continuation registry: '+str(exc)) from exc


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1])
    args=parser.parse_args()
    try:print(json.dumps(validate(args.root),indent=2))
    except ValueError as exc:parser.exit(1,'REFUSED: '+str(exc)+'\n')
