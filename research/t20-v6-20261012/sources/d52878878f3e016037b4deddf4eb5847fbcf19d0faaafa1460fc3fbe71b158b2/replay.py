#!/usr/bin/env python3
"""Fail-closed source replay. Dependencies verified read-only; no download/rebuild."""
from pathlib import Path
import argparse,datetime,hashlib,json,math,os,re,stat,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
SCIENCE_SHA='06a0c9a7158c4229e4130ed7afdd0c6116f8032481dd90660e77552f588c0b8f'
PIN_SHA={'dependencies/CACHE_METADATA_RELOCATION.json': 'd14ffdea106264773d5b708b765a078e1a8a3f529bd909c08dcc806c3d4c446b', 'dependencies/LEAN_DISTRIBUTION_PIN.json': '6f364a506b2b7bc8934b13ef50b296fd2047d9b7894a2b7f637ad44e4f8e52fb', 'dependencies/MATHLIB_CACHE_PIN.json': '7dc08ad35391b67f1fb930b1315432ec17321dc6ecfad13b4689f32ade95d2f9', 'dependencies/MATHLIB_SOURCE_PIN.json': 'c01c0b3cf6bed3a960794e7da55231e446c7622f9c953b5c0e82092d026bb431', 'ORIGINAL_TO_PUBLIC.json': 'dc642d38166c6284216a82f37c8e1e40759a0e88edef3a47574c234dbd49971a', 'history/controller-sharpness-v1-INPUT_BINDING.json': '1cd13387f8acf9b1dfdbd9a1488a684ab0e466f0cf580cb47534e6f9a32fcd2d', 'history/controller-sharpness-v1-MANIFEST.json': '2ec4b220e069c8a6c7321403c10185670d33bb93faed3362523bfdf42ef157c6', 'history/finite-corruption-v1-INPUT_BINDING.json': '3025db61b3794f1a90f617478722204a026f85f842fe75c683a7e969d156761e', 'history/finite-corruption-v1-MANIFEST.json': 'b763dd865ee497ab6c8cbe52e63bd5eefb00e4b5d8baa062b0d7cd106040395b', 'history/progress-core-v1-INPUT_BINDING.json': '296da61cf3564d2f8905668cb88400917d8176513455480c52eaa7650aa81ebf', 'history/progress-core-v1-MANIFEST.json': 'fffebbef80cac51557b7bcc7751b135999e5cd6f2dfe2eae816e447b624b403a'}
LEAN_SHA='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
MATHLIB_COMMIT='c44e0c8ee63ca166450922a373c7409c5d26b00b'

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

def canonical_relative(relative):
    rel=Path(relative)
    require(not rel.is_absolute() and rel.parts and str(rel)==relative and
            all(p not in ('','.','..') for p in rel.parts) and '\\' not in relative,
            f'Unsafe manifest path: {relative}')
    return rel

def compiler_subprocess_environment(env):
    """Remove every inherited dynamic-loader override from a fresh child map.
    This cannot sanitize the already-running Python launcher or host.
    """
    return {key:value for key,value in env.items() if not key.startswith('LD_')}

def run_compiler_stage(command,env,log,timeout):
    start=time.monotonic()
    try:
        r=subprocess.run(command,env=compiler_subprocess_environment(env),cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
        text=r.stdout;rc=r.returncode;timed_out=False
    except subprocess.TimeoutExpired as error:
        text=error.stdout or ''
        if isinstance(text,bytes):text=text.decode('utf-8',errors='replace')
        text+=f'\nREPLAY_TIMEOUT after {timeout} seconds\n';rc=None;timed_out=True
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

def verify_tree_pin(base,pin,relocation=None):
    base=base.resolve(); records=pin['entries'];names=[r['path'] for r in records]
    require(len(names)==len(set(names)),'duplicate dependency path')
    observed=set()
    for root in pin['roots']:
        tree=base if root=='' else base/canonical_relative(root)
        require(tree.is_dir() and not tree.is_symlink(),'missing/symlinked dependency tree '+root)
        for item in ([tree] if root else [])+list(tree.rglob('*')): observed.add(str(item.relative_to(base)))
    require(observed==set(names),'dependency inventory mismatch')
    changed=[]
    allow={} if relocation is None else {r['path']:r for r in relocation['files']}
    if relocation:
        expected={'.lake/build/lib/lean/Cache/'+n+'.trace' for n in ['Hashing','IO','Lean','Main','Requests']}
        require(set(allow)==expected and len(relocation['files'])==5,'wrong relocation allowlist')
        require(relocation['actual_files_mutated'] is False and relocation['normalization_for_comparison_only'] is True,'wrong relocation contract')
        require(relocation['original_cache_manifest_sha256']==PIN_SHA['dependencies/MATHLIB_CACHE_PIN.json'],'relocation pins another cache')
    for r in records:
        rel=canonical_relative(r['path']);item=base/rel; current=base
        for part in rel.parts[:-1]:
            current=current/part;require(not current.is_symlink(),'dependency symlink ancestor '+str(rel))
        kind=r['kind']
        if kind=='directory':require(item.is_dir() and not item.is_symlink(),'directory mismatch '+str(rel))
        elif kind=='symlink':
            require(item.is_symlink() and os.readlink(item)==r['target'],'symlink mismatch '+str(rel))
            require(item.exists() and item.resolve().is_relative_to(base),'escaping/dangling symlink '+str(rel))
        elif kind=='file':
            require(item.is_file() and not item.is_symlink() and stat.S_ISREG(item.stat().st_mode),'file type mismatch '+str(rel))
            if item.stat().st_size==r['bytes'] and digest(item)==r['sha256']:continue
            require(str(rel) in allow,'dependency identity mismatch '+str(rel))
            a=allow[str(rel)];data=item.read_bytes()
            require(len(data)==a['current_bytes'] and hashlib.sha256(data).hexdigest()==a['current_sha256'],'unrecognized relocated trace '+str(rel))
            old=relocation['historical_prefix'].encode();new=relocation['current_prefix'].encode()
            require(new!=old and data.count(new)==a['replacement_count']==1,'invalid path-only delta '+str(rel))
            normalized=data.replace(new,old)
            require(len(normalized)==r['bytes']==a['original_pin_bytes']==a['normalized_bytes'],'normalized trace length differs '+str(rel))
            require(hashlib.sha256(normalized).hexdigest()==r['sha256']==a['original_pin_sha256']==a['normalized_sha256'],'non-path trace content differs '+str(rel))
            changed.append(str(rel))
        else:raise RuntimeError('unknown dependency kind '+kind)
    return changed

def verify_package():
    for name,sha in PIN_SHA.items():require(digest(regular_path(ROOT,name))==sha,'bound input changed '+name)
    require(digest(regular_path(ROOT,'SCIENCE_INVENTORY.json'))==SCIENCE_SHA,'scientific inventory changed')
    science=json.loads((ROOT/'SCIENCE_INVENTORY.json').read_text())
    require(len(science['scientific_theorems'])==129 and len(set(science['scientific_theorems']))==129,'wrong science theorem inventory')
    require(len(science['modules'])==len({r['module'] for r in science['modules']}),'duplicate module')
    for r in science['modules']:verify_record(ROOT,r)
    for r in science['controls']:verify_record(ROOT,r)
    public=json.loads(regular_path(ROOT,'PUBLIC_MANIFEST.json').read_text())
    exact_inventory(ROOT,public['files'],'PUBLIC_MANIFEST.json')
    for r in public['files']:verify_record(ROOT,r)
    return science,digest(ROOT/'PUBLIC_MANIFEST.json')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean-root',type=Path,required=True)
    parser.add_argument('--mathlib',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--stage-timeout',type=float,default=300)
    args=parser.parse_args()
    require(math.isfinite(args.stage_timeout) and 0<args.stage_timeout<=600,'timeout must be finite, positive and <=600')
    leanroot=args.lean_root.resolve(); mathlib=args.mathlib.resolve();lean=leanroot/'bin/lean'
    output=require_fresh_output(args.output,[ROOT,leanroot,mathlib])
    science,identity=verify_package()
    output.mkdir(parents=True,exist_ok=False);(output/'build').mkdir();(output/'logs').mkdir()
    build=output/'build';logs=output/'logs';stages=[]
    try:
        leanpin=json.loads((ROOT/'dependencies/LEAN_DISTRIBUTION_PIN.json').read_text())
        cachepin=json.loads((ROOT/'dependencies/MATHLIB_CACHE_PIN.json').read_text())
        sourcepin=json.loads((ROOT/'dependencies/MATHLIB_SOURCE_PIN.json').read_text())
        relocation=json.loads((ROOT/'dependencies/CACHE_METADATA_RELOCATION.json').read_text())
        require(leanpin['version']=='4.19.0' and leanpin['release_commit']=='6caaee842e94','wrong Lean pin')
        require(cachepin['mathlib_commit']==sourcepin['commit']==MATHLIB_COMMIT and len(sourcepin['files'])==6816,'wrong Mathlib pin')
        verify_tree_pin(leanroot,leanpin)
        deltas_before=verify_tree_pin(mathlib,cachepin,relocation)
        require(digest(lean)==LEAN_SHA,'wrong Lean launcher')
        for r in sourcepin['files']:verify_record(mathlib,r)
        env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,[build]+[mathlib/r for r in cachepin['roots']])),PYTHONDONTWRITEBYTECODE='1')
        for key in ['LEAN_SRC_PATH','LEAN_SYSROOT','LD_PRELOAD','LD_LIBRARY_PATH']:env.pop(key,None)
        version=run_compiler_stage([str(lean),'--version'],env,logs/'version.log',min(30,args.stage_timeout))
        require(version['exit_code']==0 and not version['timed_out'] and '4.19.0' in version['text'] and '6caaee842e94' in version['text'],'wrong compiler version')
        for r in science['modules']:
            source=ROOT/r['path'];name=r['module']
            require(not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern)\b',proof_tokens(source.read_text())),'forbidden proof construct '+name)
            result=run_compiler_stage([str(lean),'-j1','-o',str(build/(name+'.olean')),str(source)],env,logs/(name+'.log'),args.stage_timeout)
            stages.append({'module':name,'source_sha256':r['sha256'],**{k:v for k,v in result.items() if k!='text'}})
            require(not result['timed_out'] and result['exit_code']==0 and not re.search(r'warning:|error:|sorryAx',result['text']),'source stage did not pass cleanly '+name)
            print(name,'PASS',flush=True)
        audits={}
        for r in science['controls']:
            name=r['module'];result=run_compiler_stage([str(lean),'-j1',str(ROOT/r['path'])],env,logs/(name+'.log'),args.stage_timeout)
            stages.append({'module':name,**{k:v for k,v in result.items() if k!='text'}})
            require(not result['timed_out'] and result['exit_code']==0 and not re.search(r'warning:|error:|sorryAx',result['text']),'axiom stage failed '+name)
            audits[name]=audit_axioms(result['text'],science[r['inventory_key']])
        require(verify_package()[1]==identity,'package changed during replay')
        verify_tree_pin(leanroot,leanpin);deltas_after=verify_tree_pin(mathlib,cachepin,relocation)
        require(deltas_after==deltas_before,'relocation status changed during replay')
        for r in sourcepin['files']:verify_record(mathlib,r)
        receipt={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
          'public_manifest_sha256':identity,'science_inventory_sha256':SCIENCE_SHA,
          'compiler_version':version['text'].strip(),'compiler_sha256':LEAN_SHA,
          'dependency_pins':PIN_SHA,'pinned_dependency_bytes_checked_before_after':True,
          'cache_trace_path_only_deltas':deltas_after,'dependency_files_mutated':False,
          'compiled_source_modules':len(science['modules']),'new_theorems':len(science['scientific_theorems']),
          'reviewer_theorems':len(science['reviewer_theorems']),'axiom_audits':audits,'stages':stages,
          'execution_boundary':'Kernel-checked noncomputable shared reference definitions; not native21-path execution.'}
        write_json(output/'REPLAY_RECEIPT.json',receipt);print(json.dumps({'status':'PASS','receipt':str(output/'REPLAY_RECEIPT.json')}),flush=True)
    except Exception as error:
        write_json(output/'REPLAY_RECEIPT.json',{'status':'FAIL','error':str(error),'stages':stages})
        raise

if __name__=='__main__':
    try:main()
    except Exception as error:print('REPLAY_FAILED:',error,file=sys.stderr);raise SystemExit(1)
