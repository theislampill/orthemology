"""Source-specific private selector helper proposal; no recipe or qualification.

The caller must join current source/object facts to a D03-validated physical
receipt, capture and safe audit before allowing reuse. This module never does
that audit or executes an original driver. File capture is a guarded splice
primitive: call validate_call before installing it around an original child.
"""
from io import BytesIO, TextIOBase
from pathlib import Path
import ast
import json
import os
import re
import stat
import subprocess
import zipfile

SELECTOR_ARCHIVE = 'e2c40bb8b2612db8898cdea0db2c984c91edaa15122dd23cbfb16f33d3e98255'
CORE_ARCHIVE = 'bca5b48fbcbb65f032fb5b92f1cb9dec1e3bc3e340f424d0a2c6c2df54530da2'
LITERAL_ARCHIVE = 'b9c56f8b5cf7af600a4ce37903264808928f9490209d0fd4672c6f340d729f91'
CORE_MANIFEST = '8981fe18fb0d182dfbab01142f250354846dfb691c873d8d1ced71d3f1df3f4c'
DRIVER = 'a02ac9ee8c6108bd247c64c8a5fdfd66741dfdc24370600b90fe1ae15c2c6946'
PYTHON = 'd1483a82342508f2ec2b172b788d5b676a59eaf70ed01ae846a0f84f63a3a82a'
PREFIX = 'Ninth_Selector_Family_Source_Acceptance_v1/'
RESOURCE = re.compile(r'\btimeout\b|WALL_CLOCK_LIMIT|maximum number of heartbeats|maximum recursion depth|out of memory', re.I)


def _archive(api, path, digest):
    data=api.no_symlinks(path).read_bytes()
    api.require(api.sha(data)==digest,'Changed original archive')
    with zipfile.ZipFile(BytesIO(data)) as z:
        seen={}
        for info in z.infolist():
            api.relative(info.filename)
            api.require(info.filename not in seen and not info.is_dir() and stat.S_IFMT(info.external_attr>>16) in {0,stat.S_IFREG},'Nonregular/duplicate original archive member')
            seen[info.filename]=z.read(info)
    return seen


def _core(api, path):
    contents=_archive(api,path,CORE_ARCHIVE)
    api.require(api.sha(contents['SOURCE_MANIFEST.json'])==CORE_MANIFEST,'Changed core source manifest')
    manifest=json.loads(contents['SOURCE_MANIFEST.json'])
    sources={r['path'][12:-5].replace('/','.'):r for r in manifest['sources'] if r['path'].startswith('runtime/src/')}
    api.require(len(sources)==167,'Wrong core source census')
    for row in manifest['sources']:
        api.require(api.sha(contents[row['path']])==row['sha256'] and len(contents[row['path']])==row['bytes'],'Core archive source bytes differ')
    return contents,sources


def bind_core_objects(api, output, archive):
    """Source/object binding only. Never qualifies the failed core audit."""
    contents,sources=_core(api,archive);output=api.no_symlinks(output)
    receipt=api.read_json(output/'RESULT.json')
    api.require(receipt['status']=='COMPLETED_FRESH_REPLAY' and receipt['source_manifest_sha256']==CORE_MANIFEST,'Expected exact standard core runtime result')
    rows=receipt['runs'];runs={};readbacks=[]
    api.require(len(rows)==168,'Standard core runtime child census differs')
    for row in rows:
        api.require(row['suite']=='runtime','Non-runtime standard core child')
        name=row['module']
        api.require(type(row['exit_code']) is int and row['exit_code']==0,'Core child exit is not a successful integer')
        if name=='RuntimeReadback':readbacks.append(row)
        else:
            api.require(name not in runs,'Duplicate core module')
            runs[name]=row
    api.require(set(runs)==set(sources) and len(readbacks)==1 and type(receipt['runtime']['axiom_readbacks']) is int and receipt['runtime']['axiom_readbacks']==13,'Core module/readback census differs')
    build=api.no_symlinks(output/'runtime/build');actual=set()
    for path in build.rglob('*'):
        api.no_symlinks(path)
        api.require(path.is_dir() or path.is_file(),'Nonregular core build entry')
        if path.is_file():actual.add(path.relative_to(build).as_posix())
    expected={n.replace('.','/')+'.olean' for n in sources}
    api.require(actual==expected,'Core object or auxiliary file census differs')
    pairs=[]
    for name in sorted(sources):
        row=runs[name];api.require(row['source_sha256']==sources[name]['sha256'],'Core source binding differs')
        path=api.path_in(build,name.replace('.','/')+'.olean');digest=api.sha(path.read_bytes())
        api.require(digest==row['object_sha256'],'Core object digest differs')
        pairs.append({'module':name,'source_sha256':row['source_sha256'],'object_sha256':digest})
    pins=json.loads(contents['DEPENDENCY_PINS.json'])
    api.require(pins['lean_binary_sha256']==api.LEAN_SHA,'Core toolchain pin differs')
    return {'receipt_sha256':api.sha((output/'RESULT.json').read_bytes()),'objects_verified':167,
            'source_manifest_sha256':CORE_MANIFEST,'source_object_fingerprint':api.canonical(pairs),'pairs':pairs,
            'dependency_pins_sha256':api.sha(contents['DEPENDENCY_PINS.json']),'lean_executable_sha256':pins['lean_binary_sha256'],
            'qualification':'REQUIRES_D03_VALIDATED_RECEIPT_AND_CAPTURE_JOIN','new_kernel_checks_from_reuse':0}


def prepare(api, root, out, core_output, lean, mathlib, python, selector_zip, core_zip, literal_zip, cwd):
    """Read pinned sources and produce the original's explicit-reuse call plan."""
    selector=_archive(api,selector_zip,SELECTOR_ARCHIVE);core,_=_core(api,core_zip);literal=_archive(api,literal_zip,LITERAL_ARCHIVE)
    api.require(all(name.startswith(PREFIX) for name in selector),'Wrong selector archive root')
    members={name[len(PREFIX):]:data for name,data in selector.items()}
    api.require(api.sha(members['replay.py'])==DRIVER,'Wrong selector driver')
    root=api.no_symlinks(root).resolve();out=api.no_symlinks(out).absolute();co=api.no_symlinks(core_output).absolute()
    lean=api.no_symlinks(lean).resolve();mathlib=api.no_symlinks(mathlib).resolve();python=Path(python).absolute();cwd=api.no_symlinks(cwd).resolve()
    api.require(not out.exists(),'Original selector output must be absent')
    for protected in (root,co,mathlib,lean.parent):api.require(not out.is_relative_to(protected) and not protected.is_relative_to(out),'Output overlaps protected input')
    api.require(lean.is_file() and api.sha(lean.read_bytes())==api.LEAN_SHA and python.is_file() and api.sha(python.read_bytes())==PYTHON,'Wrong exact tool bytes')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file()}
    api.require(actual==set(members),'Selector full original file census differs')
    for name,data in members.items():api.require(api.path_in(root,name).read_bytes()==data,'Selector full original member differs')
    tree=ast.parse(members['replay.py'].decode());assignments={n.targets[0].id:n.value for n in tree.body if isinstance(n,ast.Assign) and len(n.targets)==1 and isinstance(n.targets[0],ast.Name)}
    order=ast.literal_eval(assignments['ORDER']);literal_names=ast.literal_eval(assignments['LITERAL_MODULES'])
    bound={r['module']:r for r in json.loads(members['PROOF_SOURCE_BINDINGS.json'])['files']}
    api.require(set(bound)|set(literal_names)==set(order) and len(order)==15,'Selector child source census differs')
    libs=[mathlib/'.lake/build/lib/lean']+sorted((mathlib/'.lake/packages').glob('*/.lake/build/lib/lean'))
    lean_path=':'.join(str(x) for x in [out/'build',co/'runtime/build',*libs])
    children=[];events=[{'readonly':True,'argv':[str(lean),'--version'],'text':True}]
    for package in json.loads(core['DEPENDENCY_PINS.json'])['packages']:
        path=mathlib if package['name']=='mathlib' else mathlib/'.lake/packages'/package['name']
        for tail,text in [(['rev-parse','HEAD'],True),(['status','--porcelain','--untracked-files=all'],True),(['ls-files','-z'],False)]:
            events.append({'readonly':True,'argv':['git','-C',str(path),*tail],'text':text})
    for name in order:
        if name in literal_names:
            member='src/'+name+'.lean';src=out/'dependencies/literal'/member;data=literal[member]
        else:
            row=bound[name];src=root/row['path'];data=members[row['path']];api.require(api.sha(data)==row['sha256'],'Bound selector source differs')
        obj=out/'build'/(name+'.olean')
        event={'readonly':False,'id':name,'argv':[str(lean),'-j1','--root='+str(src.parent),'-o',str(obj),str(src)],
               'source_path':str(src),'source_sha256':api.sha(data),'object_path':str(obj),'log':str(out/'logs'/(name+'.log')),
               'cwd':str(cwd),'explicit_cwd':False,'capture':'PIPE','timeout':180,'lean_path':lean_path,
               'timeout_marker':'\nWALL_CLOCK_LIMIT_180_SECONDS\n','extra_sources':{}}
        events.append(event);children.append(event)
    for name,member,destination,seconds in [('finite-controls','controls/finite_controls.py','finite-controls/finite_controls.py',60),('original-census-controls','controls/check_original_replay_guards.py','original-census-controls/check_replay_guards.py',30)]:
        src=out/destination;extra={}
        if name=='original-census-controls':extra[str(out/'original-census-controls/snapshot/replay.py')]=api.sha(members['historical/A2_replay.py'])
        event={'readonly':False,'id':name,'argv':[str(python),'-B',str(src)],'source_path':str(src),'source_sha256':api.sha(members[member]),
               'object_path':None,'log':str(src.parent/'stdout.log'),'cwd':str(cwd),'explicit_cwd':False,'capture':'FILE',
               'timeout':seconds,'lean_path':lean_path,'timeout_marker':None,'extra_sources':extra}
        events.append(event);children.append(event)
    api.require(len(events)==45 and len(children)==17,'Selector complete process census differs')
    return {'events':events,'children':children,'event_plan_sha256':api.canonical(events),'driver_sha256':DRIVER,
            'manifest_sha256':api.sha(members['MANIFEST.json']),'requires_existing_core_output':True,'new_core_kernel_checks':0}


def validate_call(api,event,argv,args,kwargs,cwd):
    api.require(isinstance(argv,list) and argv==event['argv'] and all(isinstance(x,str) for x in argv) and not args,'Original selector argv/order differs')
    if event['readonly']:
        allowed={'stdout','check','timeout'}|({'text'} if event['text'] else set())
        api.require(set(kwargs)<=allowed and kwargs.get('stdout')==subprocess.PIPE and kwargs.get('check') is True and kwargs.get('timeout') is None and (kwargs.get('text') is True if event['text'] else 'text' not in kwargs),'Original read-only keyword differs')
        return True
    expected={'env','stdout','stderr','timeout'}|({'text'} if event['capture']=='PIPE' else set())
    api.require(set(kwargs)==expected,'Original selector keyword set differs')
    api.require(str(Path(cwd).resolve())==event['cwd'],'Original inherited cwd differs')
    api.require(type(kwargs['timeout']) is int and kwargs['timeout']==event['timeout'],'Original selector budget differs')
    env=kwargs['env'];api.require(isinstance(env,dict) and env.get('LEAN_PATH')==event['lean_path'] and 'LEAN_SRC_PATH' not in env and 'PYTHONOPTIMIZE' not in env,'Original selector environment differs')
    api.require(kwargs['stderr']==subprocess.STDOUT,'Original selector stderr differs')
    if event['capture']=='PIPE':api.require(kwargs['stdout']==subprocess.PIPE and kwargs['text'] is True,'Original pipe capture differs')
    else:
        stream=kwargs['stdout'];api.require(isinstance(stream,TextIOBase) and stream.writable() and str(Path(stream.name).absolute())==event['log'],'Original file capture differs')
        path=api.no_symlinks(stream.name);descriptor=os.fstat(stream.fileno());named=path.stat()
        api.require((descriptor.st_dev,descriptor.st_ino)==(named.st_dev,named.st_ino) and named.st_size==0 and stream.tell()==0,'Original file handle is reused or redirected')
    api.require(api.sha(api.no_symlinks(event['source_path']).read_bytes())==event['source_sha256'],'Original selector child source changed')
    for name,digest in event['extra_sources'].items():api.require(api.sha(api.no_symlinks(name).read_bytes())==digest,'Original child helper source changed')
    if event['object_path']:api.require(not api.no_symlinks(event['object_path']).exists(),'Original selector object exists')
    return True


def capture_file_call(api, original_run, trace, index, argv, kwargs):
    """Capture the exact opened child log; caller validates its source recipe."""
    api.require(type(index) is int and index>=0 and isinstance(argv,list),'Wrong file capture identity')
    stream=kwargs['stdout'];api.require(isinstance(stream,TextIOBase) and stream.writable() and kwargs.get('stderr')==subprocess.STDOUT and 'text' not in kwargs and 'shell' not in kwargs,'Unreviewed file capture form')
    path=api.no_symlinks(stream.name);trace=api.no_symlinks(trace)
    destination=api.path_in(trace,f'{index:04}.json');log=api.path_in(trace,f'{index:04}.log')
    api.require(not destination.exists() and not log.exists(),'File capture would overwrite prior evidence')
    row={'index':index,'argv':[str(x) for x in argv],'cwd':str(Path(kwargs.get('cwd',Path.cwd())).absolute()),
         'started_at':api.utc(),'ended_at':None,'terminal':'RUNNING','exit_code':None,'log_sha256':None,'capture_kind':'SOURCE_PRESCRIBED_FILE'}
    api.write_json(destination,row)
    def terminal(kind,code):
        stream.flush();data=path.read_bytes();log.write_bytes(data)
        row.update(ended_at=api.utc(),terminal=kind,exit_code=code,log_sha256=api.sha(data));api.write_json(destination,row)
    try:result=original_run(argv,**kwargs)
    except (subprocess.TimeoutExpired,KeyboardInterrupt) as error:
        terminal('TIMEOUT' if isinstance(error,subprocess.TimeoutExpired) else 'INTERRUPTED',None);raise
    api.require(result.stdout is None,'Source-prescribed file child unexpectedly returned stdout')
    completed=type(result.returncode) is int and 0<=result.returncode<124
    terminal('COMPLETED' if completed else 'INTERRUPTED',result.returncode if completed else None)
    return result


def classify_stage(api,event,capture,raw,original_log):
    api.require(capture['argv']==event['argv'] and capture['cwd']==event['cwd'] and capture['log_sha256']==api.sha(raw),'Actual selector capture differs')
    terminal=capture['terminal'];code=capture['exit_code']
    api.require(terminal in {'COMPLETED','TIMEOUT','INTERRUPTED'},'Unknown selector child terminal')
    api.require(type(code) is int and 0<=code<124 if terminal=='COMPLETED' else code is None,'Invalid selector child exit')
    expected=raw+(event['timeout_marker'].encode() if terminal=='TIMEOUT' and event['timeout_marker'] else b'')
    api.require(original_log==expected,'Unreviewed selector diagnostic augmentation')
    text=original_log.decode('utf8');resource=terminal!='COMPLETED' or RESOURCE.search(text) is not None
    clean=code==0 and (event['capture']=='FILE' or ('error:' not in text and 'sorryAx' not in text and "declaration uses 'sorry'" not in text))
    outcome='RESOURCE_INCONCLUSIVE' if resource else 'ACCEPT' if clean else 'FAILED'
    return {'id':event['id'],'terminal':terminal,'exit_code':code,'outcome':outcome,'semantic_outcome':'ACCEPT' if outcome=='ACCEPT' else None,
            'maximum_scope':'FINITE_ONLY' if event['capture']=='FILE' else 'NO_FORMAL_QUALIFICATION',
            'captured_log_sha256':api.sha(raw),'original_log_sha256':api.sha(original_log),'full_original_collector_required':True}
