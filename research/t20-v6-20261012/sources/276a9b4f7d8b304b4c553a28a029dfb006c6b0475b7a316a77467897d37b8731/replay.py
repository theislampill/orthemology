"""Standalone, source-only replay of the accepted actual batch/controller proofs.
No dependency download/rebuild and no reused custom scientific objects.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,math,os,re,stat,subprocess,sys,time
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
SCIENCE_SHA='186281d14d0ea41e7ac49aa7a392a6cf05cb92047670f7d639420720785ecf0e'
SOURCE_INDEX_SHA='554021bf9747278bc4a2280a9aba32bb48b010ab06234ad5992706482fb61040'
PIN_SHA={
 'LEAN_DISTRIBUTION_PIN.json':'6f364a506b2b7bc8934b13ef50b296fd2047d9b7894a2b7f637ad44e4f8e52fb',
 'MATHLIB_CACHE_PIN.json':'7dc08ad35391b67f1fb930b1315432ec17321dc6ecfad13b4689f32ade95d2f9',
 'MATHLIB_SOURCE_PIN.json':'c01c0b3cf6bed3a960794e7da55231e446c7622f9c953b5c0e82092d026bb431',
 'CACHE_METADATA_RELOCATION.json':'d14ffdea106264773d5b708b765a078e1a8a3f529bd909c08dcc806c3d4c446b'}
LEAN_SHA='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
MATHLIB_COMMIT='c44e0c8ee63ca166450922a373c7409c5d26b00b'
NATIVE_SOURCE_SHA='e4ae2e2751535e625f245a1bb2f2e4f2f4c447a55c859e1b1c94dbbf48adf359'
TRACE_FILES={f'.lake/build/lib/lean/Cache/{name}.trace' for name in ['Hashing','IO','Lean','Main','Requests']}
FORBIDDEN=r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern|partial)\b'
RESOURCE=r'maximum recursion depth|maximum number of heartbeats|out of memory|unknown module prefix|object file .* does not exist|file not found|cannot open|REPLAY_TIMEOUT|interrupted'

def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def regular_path(base, relative):
    rel=Path(relative)
    require(not rel.is_absolute() and rel.parts and all(part not in ('','.','..') for part in rel.parts),
            f'Unsafe manifest path: {relative}')
    require(str(rel)==relative, f'Noncanonical manifest path: {relative}')
    current=base
    for part in rel.parts:
        current=current/part
        require(not current.is_symlink(), f'Symlink in source path: {relative}')
    require(current.is_file() and stat.S_ISREG(current.stat().st_mode), f'Not a regular source file: {relative}')
    return current

def verify_record(base, record):
    path=regular_path(base,record['path'])
    require(path.stat().st_size == record.get('bytes',record.get('size')) and
            digest(path) == record['sha256'], f'Identity mismatch: {record["path"]}')

def exact_inventory(base, records, self_name):
    names=[record['path'] for record in records]
    require(len(names)==len(set(names)), 'Duplicate public manifest path')
    expected=set(names)|{self_name}
    directories={str(parent) for name in expected for parent in Path(name).parents if str(parent)!='.'}
    observed=set()
    for item in base.rglob('*'):
        relative=str(item.relative_to(base))
        require(not item.is_symlink(), f'Symlink in checkpoint: {relative}')
        if item.is_dir():
            require(relative in directories, f'Unlisted checkpoint directory: {relative}')
        else:
            require(item.is_file() and stat.S_ISREG(item.stat().st_mode), f'Nonregular checkpoint item: {relative}')
            observed.add(relative)
    require(observed==expected, f'Public inventory mismatch: extra={sorted(observed-expected)}, missing={sorted(expected-observed)}')

def require_fresh_output(output, protected):
    require(not output.exists() and not output.is_symlink(), 'Output path must be absent')
    resolved=output.resolve()
    for tree in protected:
        root=tree.resolve()
        require(resolved!=root and root not in resolved.parents,
                f'Output is inside a protected input/dependency tree: {tree}')
    return resolved

def proof_tokens(text):
    # Remove nested Lean comments and string literals before token auditing.
    output=[]; i=0; depth=0; quoted=False
    while i < len(text):
        pair=text[i:i+2]
        if depth:
            if pair=='/-': depth+=1; i+=2
            elif pair=='-/': depth-=1; i+=2
            else: output.append('\n' if text[i]=='\n' else ' '); i+=1
        elif quoted:
            if text[i]=='\\': i+=2
            elif text[i]=='"': quoted=False; output.append(' '); i+=1
            else: output.append('\n' if text[i]=='\n' else ' '); i+=1
        elif pair=='/-': depth=1; output.append(' '); i+=2
        elif pair=='--':
            end=text.find('\n',i)
            if end<0: break
            output.append('\n');i=end+1
        elif text[i]=='"': quoted=True;output.append(' ');i+=1
        else: output.append(text[i]);i+=1
    require(depth==0 and not quoted,'Unclosed source comment/string')
    return ''.join(output)

def valid_timeout(value):
    return math.isfinite(value) and 0 < value <= 600

def canonical_relative(relative):
    rel=Path(relative)
    require(not rel.is_absolute() and rel.parts and str(rel)==relative and
            all(p not in ('','.','..') for p in rel.parts) and '\\' not in relative,
            f'Unsafe manifest path: {relative}')
    return rel

def run_compiler_stage(command,env,log,timeout):
    start=time.monotonic()
    try:
        r=subprocess.run(command,env=env,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
        text=r.stdout;rc=r.returncode;timed_out=False
    except subprocess.TimeoutExpired as error:
        text=error.stdout or ''
        if isinstance(text,bytes):text=text.decode('utf-8',errors='replace')
        text+=f'\nREPLAY_TIMEOUT after {timeout} seconds\n';rc=None;timed_out=True
    except OSError as error:
        text=f'COMPILER_OS_ERROR: {type(error).__name__}: {error}\n';rc=None;timed_out=False
    log.write_text(text)
    return {'exit_code':rc,'timed_out':timed_out,'seconds':round(time.monotonic()-start,3),
            'text':text,'command':command,'compiler_cwd':str(ROOT),'log_sha256':digest(log)}

def audit_axioms(text,names):
    observed={}
    for name,closure in re.findall(r"'([^']+)' depends on axioms:\s*\[([^]]*)\]",text,re.S):
        vals={s.strip() for s in closure.split(',') if s.strip()}
        require(vals<={'propext','Classical.choice','Quot.sound'},f'Unexpected axiom in {name}: {vals}')
        require(name not in observed,'Duplicate axiom audit declaration');observed[name]=sorted(vals)
    for name in re.findall(r"'([^']+)' does not depend on any axioms",text):
        require(name not in observed,'Duplicate axiom audit declaration');observed[name]=[]
    require(set(observed)==set(names) and len(observed)==len(names),'Incomplete or unexpected theorem axiom audit')
    return observed

def write_json(path,value):path.write_text(json.dumps(value,indent=2)+'\n')

def verify_tree_pin(base,pin,relocation=None,launcher=None):
    """Exact tree/byte pinning; only explicitly supplied exact metadata alternatives."""
    base=base.resolve();records=pin['entries'];names=[r['path'] for r in records]
    require(len(names)==len(set(names)),'Duplicate dependency path')
    observed=set()
    for root in pin['roots']:
        tree=base if root=='' else base/canonical_relative(root)
        require(tree.is_dir() and not tree.is_symlink(),f'Missing/symlinked dependency tree: {root}')
        for item in ([tree] if root else [])+list(tree.rglob('*')):observed.add(str(item.relative_to(base)))
    require(observed==set(names),f'Dependency inventory mismatch: extra={sorted(observed-set(names))}, missing={sorted(set(names)-observed)}')
    alternatives={} if relocation is None else {r['path']:r for r in relocation['files']}
    used=[]
    for record in records:
        rel=canonical_relative(record['path']);item=base/rel;current=base
        for part in rel.parts[:-1]:
            current=current/part
            require(not current.is_symlink(),f'Symlink ancestor in dependency path: {rel}')
        kind=record['kind']
        if kind=='directory':require(item.is_dir() and not item.is_symlink(),f'Wrong dependency directory: {rel}')
        elif kind=='symlink':
            require(item.is_symlink() and os.readlink(item)==record['target'],f'Wrong dependency symlink: {rel}')
            require(item.exists() and item.resolve().is_relative_to(base),f'Escaping/dangling dependency symlink: {rel}')
        elif kind=='file':
            item=regular_path(base,str(rel));actual=digest(item)
            size=record.get('bytes',record.get('size'))
            if item.stat().st_size==size and actual==record['sha256']:continue
            require(str(rel) in alternatives and str(rel) in TRACE_FILES,f'Dependency bytes differ: {rel}')
            alternative=alternatives[str(rel)];data=item.read_bytes()
            require(alternative['original_pin_sha256']==record['sha256'] and alternative['original_pin_bytes']==size,f'Metadata alternative binds wrong original: {rel}')
            suffix='lean-toolchain-4.19.0/lean-4.19.0-linux/bin/lean'
            historical=(relocation['historical_prefix']+suffix).encode()
            if actual==alternative['current_sha256'] and len(data)==alternative['current_bytes']:
                source=(relocation['current_prefix']+suffix).encode();mode='known_restored_launcher'
            else:
                require(launcher is not None,f'Undeclared metadata bytes: {rel}')
                source=str(Path(launcher).resolve()).encode();mode='supplied_pinned_launcher'
            require(source!=historical and data.count(source)==1,f'Unexpected compiler-path occurrence count: {rel}')
            normalized=data.replace(source,historical,1)
            require(len(normalized)==size and hashlib.sha256(normalized).hexdigest()==record['sha256'],f'Metadata change is not launcher-path-only: {rel}')
            used.append({'path':str(rel),'mode':mode,'raw_sha256':actual,'raw_bytes':len(data),
                'replaced_compiler_path':source.decode(),'historical_compiler_path':historical.decode(),
                'replacement_count':1,'normalized_sha256':record['sha256'],'normalized_bytes':size,
                'actual_file_mutated':False})
        else:raise RuntimeError(f'Unknown dependency entry kind: {kind}')
    return used

def named_declarations(text,namespace):
    tokens=proof_tokens(text)
    require(not re.search(FORBIDDEN,tokens),'Forbidden proof construct in compiled source')
    namespaces=re.findall(r'^namespace\s+(\S+)',tokens,re.M)
    require(namespaces==([namespace] if namespace else []),'Unexpected source namespace layout')
    rows=[]
    for kind,name in re.findall(r'\b(theorem|lemma|def|abbrev|structure|inductive)\s+([A-Za-z_][A-Za-z0-9_\x27.]*)',tokens):
        rows.append({'kind':kind,'name':namespace+'.'+name if namespace else name})
    require(len({r['name'] for r in rows})==len(rows),'Duplicate named source declaration')
    return rows

def verify_checkpoint():
    science=ROOT/'science';manifest=regular_path(science,'MANIFEST.json')
    require(digest(manifest)==SCIENCE_SHA,'Wrong scientific milestone')
    data=json.loads(manifest.read_text());exact_inventory(science,data['files'],'MANIFEST.json')
    for record in data['files']:verify_record(science,record)
    for name,expected in PIN_SHA.items():
        require(digest(regular_path(ROOT,'dependencies/'+name))==expected,f'Pinned dependency inventory changed: {name}')
    require(digest(regular_path(ROOT,'SOURCE_INDEX.json'))==SOURCE_INDEX_SHA,'Source/declaration order changed')
    index=json.loads((ROOT/'SOURCE_INDEX.json').read_text())
    require(index['scientific_manifest_sha256']==SCIENCE_SHA and len(index['modules'])==61,'Wrong module inventory')
    require(len({r['module'] for r in index['modules']})==61,'Duplicate custom module')
    all_names=[];author=[]
    for row in index['modules']:
        source=regular_path(ROOT,row['path'])
        require(digest(source)==row['sha256'],'Custom source differs from the named declaration inventory')
        declarations=named_declarations(source.read_text(),row['namespace'])
        require(declarations==row['declarations'],'Named declaration inventory differs')
        all_names += [r['name'] for r in declarations]
        if row['author_science']:author += [r['name'] for r in declarations if r['kind']=='theorem']
    require(len(all_names)==len(set(all_names)) and len(author)==476,'Duplicate declarations or wrong author theorem count')
    require(all_names==index['named_declarations'] and author==index['author_theorems'],'Audit targets changed')
    native=regular_path(science,'imports/proper-function-and-candidate-e.md').read_bytes()
    require(len(native)==3013 and hashlib.sha256(native).hexdigest()==NATIVE_SOURCE_SHA,'Pinned full native source changed')
    embedded=(science/'PinnedSource.lean').read_text().split('def sourceBytes : List Nat := [',1)[1].split(']',1)[0]
    require(bytes(map(int,re.findall(r'\d+',embedded)))==native,'Native source embedding differs')
    public=json.loads(regular_path(ROOT,'PUBLIC_MANIFEST.json').read_text())
    exact_inventory(ROOT,public['files'],'PUBLIC_MANIFEST.json')
    for record in public['files']:verify_record(ROOT,record)
    return digest(ROOT/'PUBLIC_MANIFEST.json'),index

def verify_dependencies(leanroot,mathlib):
    leanpin=json.loads((ROOT/'dependencies/LEAN_DISTRIBUTION_PIN.json').read_text())
    cachepin=json.loads((ROOT/'dependencies/MATHLIB_CACHE_PIN.json').read_text())
    mathpin=json.loads((ROOT/'dependencies/MATHLIB_SOURCE_PIN.json').read_text())
    relocation=json.loads((ROOT/'dependencies/CACHE_METADATA_RELOCATION.json').read_text())
    require(leanpin['version']=='4.19.0' and leanpin['release_commit']=='6caaee842e94','Wrong compiler pin')
    require(cachepin['mathlib_commit']==mathpin['commit']==MATHLIB_COMMIT and len(mathpin['files'])==6816,'Wrong Mathlib source pin')
    require(len(relocation['files'])==5 and {r['path'] for r in relocation['files']}==TRACE_FILES,'Metadata exception scope differs')
    require(relocation['original_cache_manifest_sha256']==PIN_SHA['MATHLIB_CACHE_PIN.json'] and
            relocation['historical_prefix']=='private-locator:d4fa495667be7b34388a' and relocation['actual_files_mutated'] is False,
            'Wrong metadata restoration provenance')
    verify_tree_pin(leanroot,leanpin)
    used=verify_tree_pin(mathlib,cachepin,relocation,leanroot/'bin/lean')
    for record in mathpin['files']:verify_record(mathlib,record)
    require(digest(leanroot/'bin/lean')==LEAN_SHA,'Compiler launcher differs')
    return cachepin,used

def verified_build_inventory(build,objects):
    actual={p.name for p in build.iterdir()}
    require(actual==set(objects),'Unexpected or missing file in isolated custom build')
    for name,sha in objects.items():
        path=regular_path(build,name)
        require(digest(path)==sha,'A previously built custom object changed')

def sanitized_env(builds,mathlib,cachepin):
    env=dict(os.environ)
    for key in list(env):
        if key.startswith('LEAN_') or key.startswith('DYLD_') or key.startswith('LD_'):
            env.pop(key,None)
    env['LEAN_PATH']=os.pathsep.join(map(str,list(builds)+[mathlib/r for r in cachepin['roots']]))
    env['PYTHONDONTWRITEBYTECODE']='1'
    return env

def failure_classification(result):
    if result['timed_out'] or result['exit_code'] not in (0,1) or re.search(RESOURCE,result['text'],re.I):
        return 'INCONCLUSIVE'
    return 'FAIL'

def clean_positive_result(result):
    return (failure_classification(result)!='INCONCLUSIVE' and result['exit_code']==0 and
        not re.search(r'error:|warning:|sorryAx',result['text'],re.I))

def record_failure(output,status,error,stages,public_identity):
    (output/'RECEIPT.json').unlink(missing_ok=True)
    write_json(output/'REPLAY_FAILURE.json',{'status':status,'error':str(error),'stages':stages,
        'public_manifest_sha256':public_identity,'no_success_receipt':True})

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean-root',type=Path,required=True)
    parser.add_argument('--mathlib',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--stage-timeout',type=float,default=300)
    args=parser.parse_args()
    require(valid_timeout(args.stage_timeout),'Stage timeout must be finite, positive, and at most 600 seconds')
    leanroot,mathlib=args.lean_root.resolve(),args.mathlib.resolve()
    output=require_fresh_output(args.output,[ROOT,leanroot,mathlib])
    identity,index=verify_checkpoint()
    output.mkdir(parents=True,exist_ok=False);build=output/'build';logs=output/'logs';build.mkdir();logs.mkdir()
    stages=[];objects={};status='FAIL'
    try:
        cachepin,relocated_before=verify_dependencies(leanroot,mathlib)
        lean=leanroot/'bin/lean';env=sanitized_env([build],mathlib,cachepin)
        version=run_compiler_stage([str(lean),'--version'],env,logs/'version.log',min(30,args.stage_timeout))
        status=failure_classification(version)
        stages.append({'module':'compiler_version',**{k:v for k,v in version.items() if k!='text'}})
        require(clean_positive_result(version) and '4.19.0' in version['text'] and '6caaee842e94' in version['text'],'Compiler version probe failed')
        sources=[(r['module'],ROOT/r['path']) for r in index['modules']]
        audit=output/'AllNamedDeclarations.lean'
        audit.write_text('\n'.join(['import '+name for name,_ in sources]+
            ['#print axioms '+name for name in index['named_declarations']])+'\n')
        sources.append(('AllNamedDeclarations',audit))
        for name,source in sources:
            verified_build_inventory(build,objects)
            require(not re.search(FORBIDDEN,proof_tokens(source.read_text())),f'Forbidden construct in {name}')
            result=run_compiler_stage([str(lean),'-j1','-s65536',f'--root={source.parent}',
                '-o',str(build/f'{name}.olean'),str(source)],env,logs/f'{name}.log',args.stage_timeout)
            status=failure_classification(result)
            require(clean_positive_result(result),f'Positive source stage failed: {name}')
            object_path=regular_path(build,f'{name}.olean');objects[object_path.name]=digest(object_path)
            stages.append({'module':name,'source_sha256':digest(source),'object_sha256':objects[object_path.name],
                **{k:v for k,v in result.items() if k!='text'}})
        axioms=audit_axioms((logs/'AllNamedDeclarations.log').read_text(),index['named_declarations'])
        verified_build_inventory(build,objects)
        require(verify_checkpoint()[0]==identity,'Source component changed during replay')
        _,relocated_after=verify_dependencies(leanroot,mathlib)
        require(relocated_before==relocated_after,'Dependency metadata variants changed during replay')
        receipt={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'scientific_manifest_sha256':SCIENCE_SHA,'public_manifest_sha256':identity,'compiler_sha256':LEAN_SHA,
            'compiler_version':version['text'].strip(),'dependency_inventory_sha256':PIN_SHA,
            'dependencies_checked_before_after':True,'dependencies_mutated':False,'metadata_relocations_used':relocated_after,
            'custom_source_modules':61,'prior_custom_objects_reused':0,'named_declarations_audited':len(axioms),
            'author_theorems_audited':476,'native_source_bytes':3013,'native_source_sha256':NATIVE_SOURCE_SHA,
            'stage_timeout_seconds':args.stage_timeout,'stages':stages,'declaration_axioms':axioms,
            'claim':'Exact source-model batch history/safety, fixed-withholding uniqueness, premise-dependent completion, exact selected-root availability iff and bound native controller/retry controls. No actor oracle, asynchronous/physical progress, alias lifecycle composition, or semantic deployment warrant.'}
        write_json(output/'RECEIPT.json',receipt)
        print(json.dumps({k:receipt[k] for k in ['status','scientific_manifest_sha256','custom_source_modules','named_declarations_audited','author_theorems_audited']},indent=2))
    except BaseException as error:
        if isinstance(error,(KeyboardInterrupt,subprocess.TimeoutExpired,OSError)):status='INCONCLUSIVE'
        record_failure(output,status,error,stages,identity)
        raise

if __name__=='__main__':main()
