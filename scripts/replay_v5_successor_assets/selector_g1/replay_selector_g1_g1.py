"""Private exact G1 author/reviewer recipe primitives. No execution/admission.

The pinned selector proposal supplies the already-tested safe ZIP reader only.
Generated mutation bytes are reconstructed from a restricted, data-only AST
of the exact original drivers; no original Python code is imported or run.
"""
from pathlib import Path
import ast
import json
import re
import subprocess
from replay_selector_g1_selector import _archive

AUTHOR_ARCHIVE='7879f8f4011a7596109760d7d113d3bea5a59253df885e39f39f4956992d318a'
REVIEW_ARCHIVE='dc56dfac753ae86f5fd9ea308c46a38464da9e0dd91d826da3872248adbd3713'
AUTHOR_PREFIX='Orthemic_Existence_Certificate_Calculus_v4/'
REVIEW_PREFIX='Orthemic_Existence_Certificate_Calculus_Independent_Acceptance_v2/'
AUTHOR_DRIVER='119fee26d6e3b3a642d03e8fe6af25e7671ac9d06fb0c8954a0bf2f0234e806a'
REVIEW_DRIVER='d8b1bc636da5cb56b05801ca3961188a9b3cf04e406f3beb26bea82d5da3ba64'
SOURCE_MANIFEST='5a5e4e8a129b70fe713e76f7b24a97823751264fe4bd67a280682b09a407979f'
PUBLIC_MANIFEST='9d8675b5d180d35651ee3a95aec28b3a977f52c0a46b7e9831ca88366736cfbd'
PYTHON='d1483a82342508f2ec2b172b788d5b676a59eaf70ed01ae846a0f84f63a3a82a'
RESOURCE=re.compile(r'\btimeout\b|WALL_CLOCK_LIMIT|maximum number of heartbeats|maximum recursion depth|out of memory',re.I)
INFRASTRUCTURE=re.compile(r'unknown module|unknown constant|unknown identifier|file not found|no such file|object file .* does not exist',re.I)


def _packet(api,archive,pin,prefix,root=None):
    raw=_archive(api,archive,pin);api.require(all(n.startswith(prefix) for n in raw),'Wrong G1 archive root')
    members={n[len(prefix):]:data for n,data in raw.items()}
    if root is not None:
        root=api.no_symlinks(root).resolve();actual=set()
        for path in root.rglob('*'):
            api.no_symlinks(path)
            if path.is_file():actual.add(path.relative_to(root).as_posix())
        api.require(actual==set(members),'G1 full packet census differs')
        for name,data in members.items():api.require(api.path_in(root,name).read_bytes()==data,'G1 packet member differs')
    return members


def _author(api,archive,root=None):
    members=_packet(api,archive,AUTHOR_ARCHIVE,AUTHOR_PREFIX,root)
    api.require(api.sha(members['replay.py'])==AUTHOR_DRIVER and api.sha(members['SOURCE_MANIFEST.json'])==SOURCE_MANIFEST and api.sha(members['PUBLIC_MANIFEST.json'])==PUBLIC_MANIFEST,'Wrong current G1 v4 source/driver/manifests')
    manifest=json.loads(members['SOURCE_MANIFEST.json'])
    for row in manifest['sources']:api.require(api.sha(members[row['path']])==row['sha256'] and len(members[row['path']])==row['bytes'],'G1 scientific source differs')
    return members,manifest


def _mutations(api,driver,base,review):
    tree=ast.parse(driver.decode());main=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='main')
    names={'source' if review else 'base':base.decode()}
    assignments={}
    for node in ast.walk(main):
        if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name):
            name=node.targets[0].id
            if name in {'old','closure','parity','keys','mutations','mutants'}:
                api.require(name not in assignments,'Ambiguous mutation assignment');assignments[name]=node.value
    for name in ('closure','parity','keys') if review else ('old','parity'):names[name]=ast.literal_eval(assignments[name])
    def value(node):
        if isinstance(node,ast.Constant) and type(node.value) in {str,int}:return node.value
        if isinstance(node,ast.Name) and node.id in names:return names[node.id]
        if isinstance(node,(ast.Tuple,ast.List)):return [value(n) for n in node.elts]
        if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='replace' and not node.keywords:
            receiver=value(node.func.value);args=[value(x) for x in node.args]
            api.require(isinstance(receiver,str) and len(args) in (2,3) and isinstance(args[0],str) and args[0] and isinstance(args[1],str) and (len(args)==2 or type(args[2]) is int),'Unreviewed mutation expression')
            api.require(args[0] in receiver,'Mutation anchor absent')
            return receiver.replace(*args)
        raise ValueError('Unreviewed mutation expression')
    rows=value(assignments['mutants' if review else 'mutations'])
    expected=['AllReceiptsRemoved','RivalParityRemoved','SupportOnlyMatching','MenuGrantRemoved','ExactKeysRemoved'] if review else ['AllReceiptsRemoved','RivalParityRemoved']
    api.require([r[0] for r in rows]==expected,'Changed G1 mutation order/census')
    return rows


def _context(api,roots,out,lean,mathlib,python,cwd,dependency=None):
    roots=[api.no_symlinks(p).resolve() for p in roots];out=api.no_symlinks(out).absolute();lean=api.no_symlinks(lean).resolve();mathlib=api.no_symlinks(mathlib).resolve();python=Path(python).absolute();cwd=api.no_symlinks(cwd).resolve()
    api.require(not out.exists(),'Original G1 output must be absent')
    for p in [*roots,mathlib,lean.parent,*([api.no_symlinks(dependency).absolute()] if dependency is not None else [])]:
        api.require(not out.is_relative_to(p) and not p.is_relative_to(out),'G1 output overlaps input')
    api.require(api.sha(lean.read_bytes())==api.LEAN_SHA and api.sha(python.read_bytes())==PYTHON,'Changed G1 tool bytes')
    libs=[mathlib/'.lake/build/lib/lean']+sorted((mathlib/'.lake/packages').glob('*/.lake/build/lib/lean'))
    return roots,out,lean,mathlib,python,cwd,libs


def _child(api,children,events,label,source,data,root,obj,cfile,path,cwd,out,expected=0,review=False):
    argv=[str(root['lean']),'-j1','--root='+str(root['source'])]
    if obj is not None:argv+=['-o',str(obj)]
    if cfile is not None:argv+=['-c',str(cfile)]
    argv.append(str(source))
    row={'readonly':False,'profile':'LEAN_PIPE','id':label,'argv':argv,'cwd':str(cwd),'explicit_cwd':False,
         'source_path':str(source),'source_sha256':api.sha(data),'object_path':str(obj) if obj is not None else None,
         'c_output':str(cfile) if cfile is not None else None,'lean_path':path,'timeout':180,'expected_exit':expected,
         'positive_prerequisites':[r['id'] for r in children if r['expected_exit']==0] if expected else [],
         'diagnostic_literal':'did not evaluate to `true`' if review else 'did not evaluate to',
         'timeout_marker':'\nWALL_CLOCK_LIMIT_180_SECONDS' if review else '\nWALL_CLOCK_LIMIT_180',
         'review':review,'log':str(out/'logs'/(label+'.log'))}
    children.append(row);events.append(row)


def prepare_author(api,archive,root,out,lean,mathlib,python,cwd):
    members,manifest=_author(api,archive,root)
    roots,out,lean,mathlib,python,cwd,libs=_context(api,[root],out,lean,mathlib,python,cwd);root=roots[0]
    events=[{'readonly':True,'profile':'CHECK_OUTPUT','argv':[str(lean),'--version'],'text':True}];children=[];derived={};generated={}
    for package in json.loads(members['DEPENDENCY_PINS.json'])['packages']:
        path=mathlib if package['name']=='mathlib' else mathlib/'.lake/packages'/package['name']
        for tail,text in [(['rev-parse','HEAD'],True),(['status','--porcelain','--untracked-files=all'],True),(['ls-files','-z'],False)]:events.append({'readonly':True,'profile':'CHECK_OUTPUT','argv':['git','-C',str(path),*tail],'text':text})
    by={r['module']:r for r in manifest['sources'] if r['group']=='inherited-cost'};ordered=[];seen=set()
    def visit(name,trail):
        api.require(name not in trail,'G1 inherited import cycle')
        if name in seen:return
        for imported in api.imports(members[by[name]['path']].decode()):
            if imported in by:visit(imported,trail|{name})
            else:api.require(imported.startswith(('Mathlib','Lean','Std','Init')),'Missing G1 custom import')
        seen.add(name);ordered.append(name)
    visit('GlobalParitySufficiency',set());api.require(len(ordered)==len(by)==87,'G1 inherited closure differs')
    basepath=':'.join(str(p) for p in [out/'build',*libs])
    def run(label,member,object_relative=None,c_relative=None,source_root=None,expected=0,derived_bytes=None,menv=None):
        src=(out if derived_bytes is not None else root)/member;data=derived_bytes if derived_bytes is not None else members[member]
        _child(api,children,events,label,src,data,{'lean':lean,'source':root/source_root if source_root else src.parent},out/object_relative if object_relative else None,out/c_relative if c_relative else None,menv or basepath,cwd,out,expected)
    for name in ordered:run('cost-'+name,by[name]['path'],'build/'+name.replace('.','/')+'.olean',source_root='inherited/cost/src')
    for name in manifest['own_order']:run(name,'src/'+name+'.lean','build/'+name+'.olean')
    for name in manifest['positive_controls']:run(name,'controls/'+name+'.lean','build/'+name+'.olean')
    for name in ['CertificateData','CertificateOrder','CertificatePath','CertificateSyntax','CertificateComposition','CertificateBinding']:run('C-'+name,'src/'+name+'.lean','codegen/'+name+'.olean','codegen/'+name+'.c')
    for mutant,control in [('PathLengthMutant','PathLengthMutationControl'),('PathEdgesMutant','PathEdgesMutationControl')]:
        run(mutant,'mutations/'+mutant+'.lean','build/'+mutant+'.olean');run(control,'mutations/'+control+'.lean',expected=1)
    for label,text,test in _mutations(api,members['replay.py'],members['src/CertificateSyntax.lean'],False):
        sources=[('CertificateSyntax',text.encode(),'SOURCE_REPLACEMENT','src/CertificateSyntax.lean'),('CertificateFixtures',members['controls/CertificateFixtures.lean'],'COPIED_EXACT','controls/CertificateFixtures.lean'),('MutationControl',('import CertificateFixtures\nopen OrthemicCertificate OrthemicCertificate.Fixtures\n'+test).encode(),'DRIVER_LITERAL','replay.py')]
        for name,data,kind,owner in sources:
            relative='mutations/'+label+'/src/'+name+'.lean';generated[relative]=data
            derived[relative]={'kind':kind,'owner':owner,'owner_sha256':api.sha(members[owner]),'derived_sha256':api.sha(data),'driver_sha256':AUTHOR_DRIVER}
            run(label+'-'+name,relative,None if name=='MutationControl' else 'mutations/'+label+'/build/'+name+'.olean',expected=1 if name=='MutationControl' else 0,derived_bytes=data,menv=str(out/'mutations'/label/'build')+':'+basepath)
    api.require(len(children)==120 and len(events)==148,'G1 author full process census differs')
    return {'events':events,'children':children,'event_plan_sha256':api.canonical(events),'derivations':derived,'generated_bytes':generated,'original_sources_changed':False,'driver_sha256':AUTHOR_DRIVER,'requires_existing_author_run':False}


def prepare_review(api,author_archive,review_archive,author,review,out,author_output,lean,mathlib,python,cwd):
    authored,manifest=_author(api,author_archive,author);members=_packet(api,review_archive,REVIEW_ARCHIVE,REVIEW_PREFIX,review)
    api.require(api.sha(members['replay_review.py'])==REVIEW_DRIVER,'Wrong G1 review driver')
    roots,out,lean,mathlib,python,cwd,libs=_context(api,[author,review],out,lean,mathlib,python,cwd,author_output);author,review=roots;prior=api.no_symlinks(author_output).absolute()
    events=[{'readonly':True,'profile':'INHERITED_STDOUT_CHECK','argv':[str(python),str(author/'replay.py'),'--verify-only'],'cwd':str(cwd)},
            {'readonly':True,'profile':'CHECK_OUTPUT','argv':[str(lean),'--version'],'text':True}];children=[];derived={};generated={}
    basepath=':'.join(str(p) for p in [out/'review-build',prior/'build',*libs])
    for name in ['ReviewerControls','ReviewerCompositionControls','ReviewerPathReadback','ReviewerFullDependencies','ReviewerSemanticReadback']:
        member='tests/'+name+'.lean';src=review/member
        _child(api,children,events,name,src,members[member],{'lean':lean,'source':src.parent},out/'review-build'/(name+'.olean'),None,basepath,cwd,out,review=True)
    for label,text in _mutations(api,members['replay_review.py'],authored['src/CertificateSyntax.lean'],True):
        for name,data,kind,owner,owner_data,short in [('CertificateSyntax',text.encode(),'SOURCE_REPLACEMENT','author/src/CertificateSyntax.lean',authored['src/CertificateSyntax.lean'],'Syntax'),('ReviewerControls',members['tests/ReviewerControls.lean'],'COPIED_EXACT','review/tests/ReviewerControls.lean',members['tests/ReviewerControls.lean'],'Controls')]:
            relative='mutations/'+label+'/src/'+name+'.lean';src=out/relative;generated[relative]=data
            derived[relative]={'kind':kind,'owner':owner,'owner_sha256':api.sha(owner_data),'derived_sha256':api.sha(data),'driver_sha256':REVIEW_DRIVER}
            _child(api,children,events,label+'-'+short,src,data,{'lean':lean,'source':src.parent},out/'mutations'/label/'build'/(name+'.olean'),None,str(out/'mutations'/label/'build')+':'+basepath,cwd,out,expected=1 if short=='Controls' else 0,review=True)
    api.require(len(children)==15 and len(events)==17,'G1 review full process census differs')
    return {'events':events,'children':children,'event_plan_sha256':api.canonical(events),'derivations':derived,'generated_bytes':generated,'original_sources_changed':False,'driver_sha256':REVIEW_DRIVER,'requires_existing_author_run':True,'new_author_kernel_checks':0}


def bind_author_production(api,archive,output):
    members,manifest=_author(api,archive);output=api.no_symlinks(output);receipt=api.read_json(output/'RESULT.json')
    api.require(receipt['status']=='PASS_FRESH_CLOSURE_CONTROLS_AXIOMS_AUDIT_CODEGEN_AND_MUTATIONS' and receipt['source_manifest_sha256']==SOURCE_MANIFEST and receipt['public_manifest_sha256']==PUBLIC_MANIFEST and receipt['custom_objects_reused'] is False,'Expected successful current v4 cold author result')
    runs={}
    for row in receipt['runs']:
        api.require(row['label'] not in runs,'Duplicate G1 author row');runs[row['label']]=row
    api.require(len(runs)==120,'G1 original child census differs')
    production={r['module']:r for r in manifest['sources'] if r['group'] in {'own','inherited-cost'}}
    all_sources={r['module']:r for r in manifest['sources']}
    root_names=set(production)|set(manifest['positive_controls'])|{'PathLengthMutant','PathEdgesMutant'}
    api.require(len(production)==95 and len(root_names)==106,'G1 production/root source census differs')
    build=api.no_symlinks(output/'build');actual=set()
    for path in build.rglob('*'):
        api.no_symlinks(path)
        if path.is_file():actual.add(path.relative_to(build).as_posix())
        else:api.require(path.is_dir(),'Nonregular G1 build entry')
    api.require(actual=={name.replace('.','/')+'.olean' for name in root_names},'G1 complete root object census differs')
    pairs=[];all_pairs=[]
    for name in sorted(root_names):
        source=all_sources[name];label='cost-'+name if source['group']=='inherited-cost' else name;row=runs[label]
        api.require(type(row['exit_code']) is int and row['exit_code']==0 and row['source_sha256']==source['sha256'],'G1 root source/exit binding differs')
        digest=api.sha(api.path_in(build,name.replace('.','/')+'.olean').read_bytes());api.require(row['object_sha256']==digest,'G1 object digest differs')
        pair={'module':name,'source_sha256':source['sha256'],'object_sha256':digest};all_pairs.append(pair)
        if name in production:pairs.append(pair)
    pins=json.loads(members['DEPENDENCY_PINS.json']);api.require(pins['lean_binary_sha256']==api.LEAN_SHA,'Wrong G1 toolchain pin')
    return {'production_objects_verified':95,'root_objects_bound':106,'production_pairs':pairs,'root_pairs':all_pairs,
            'production_fingerprint':api.canonical(pairs),'root_object_fingerprint':api.canonical(all_pairs),'receipt_sha256':api.sha((output/'RESULT.json').read_bytes()),
            'source_manifest_sha256':SOURCE_MANIFEST,'public_manifest_sha256':PUBLIC_MANIFEST,'dependency_pins_sha256':api.sha(members['DEPENDENCY_PINS.json']),
            'lean_executable_sha256':api.LEAN_SHA,'qualification':'REQUIRES_D03_VALIDATED_RECEIPT_AND_CAPTURE_JOIN','new_kernel_checks_from_reuse':0}


def validate_call(api,event,argv,args,kwargs,cwd):
    api.require(isinstance(argv,list) and argv==event['argv'] and all(isinstance(x,str) for x in argv) and not args,'G1 original argv/order differs')
    if event['profile']=='INHERITED_STDOUT_CHECK':
        api.require(set(kwargs)=={'check'} and kwargs['check'] is True,'G1 source-only preflight keyword differs')
        api.require(str(Path(cwd).resolve())==event['cwd'],'G1 inherited preflight cwd differs');return True
    if event['readonly']:
        allowed={'stdout','check','timeout'}|({'text'} if event['text'] else set())
        api.require(set(kwargs)<=allowed and kwargs.get('stdout')==subprocess.PIPE and kwargs.get('check') is True and kwargs.get('timeout') is None and (kwargs.get('text') is True if event['text'] else 'text' not in kwargs),'G1 read-only keyword differs');return True
    api.require(set(kwargs)=={'env','stdout','stderr','text','timeout'},'G1 original child keyword differs')
    api.require(str(Path(cwd).resolve())==event['cwd'],'G1 inherited child cwd differs')
    api.require(type(kwargs['timeout']) is int and kwargs['timeout']==180 and kwargs['stdout']==subprocess.PIPE and kwargs['stderr']==subprocess.STDOUT and kwargs['text'] is True,'G1 child capture/budget differs')
    env=kwargs['env'];api.require(isinstance(env,dict) and env.get('LEAN_PATH')==event['lean_path'] and 'LEAN_SRC_PATH' not in env,'G1 isolated environment differs')
    if event['review']:api.require('LEAN_SYSROOT' not in env and not any(k.startswith('LD_') for k in env),'G1 review environment differs')
    api.require(api.sha(api.no_symlinks(event['source_path']).read_bytes())==event['source_sha256'],'G1 actual child source changed')
    for path in (event['object_path'],event['c_output']):
        if path is not None:api.require(not api.no_symlinks(path).exists(),'G1 original output already exists')
    return True


def classify_stage(api,event,capture,raw,original_log,accepted_positive_ids):
    api.require(capture['argv']==event['argv'] and capture['cwd']==event['cwd'] and capture['log_sha256']==api.sha(raw),'G1 actual child capture differs')
    terminal=capture['terminal'];code=capture['exit_code'];api.require(terminal in {'COMPLETED','TIMEOUT','INTERRUPTED'},'Unknown G1 child terminal')
    api.require(type(code) is int and 0<=code<124 if terminal=='COMPLETED' else code is None,'Invalid G1 child exit')
    expected_log=raw+(event['timeout_marker'].encode() if terminal=='TIMEOUT' else b'');api.require(original_log==expected_log,'G1 source-owned log augmentation differs')
    text=original_log.decode('utf8');resource=terminal!='COMPLETED' or RESOURCE.search(text) is not None
    if resource:outcome='RESOURCE_INCONCLUSIVE'
    elif event['expected_exit']==1:
        matched=code==1 and event['diagnostic_literal'] in text and INFRASTRUCTURE.search(text) is None
        if matched:api.require(set(event['positive_prerequisites'])<=set(accepted_positive_ids),'G1 rejection lacks required positive children')
        outcome='REJECT' if matched else 'FAILED'
    else:outcome='ACCEPT' if code==0 and 'error:' not in text and 'sorryAx' not in text and "declaration uses 'sorry'" not in text else 'FAILED'
    return {'id':event['id'],'terminal':terminal,'exit_code':code,'outcome':outcome,'semantic_outcome':outcome if outcome in {'ACCEPT','REJECT'} else None,
            'scope':'SOURCE_CHILD_ONLY_NOT_QUALIFICATION','original_log_sha256':api.sha(original_log),'captured_log_sha256':api.sha(raw),'full_original_collector_required':True}
