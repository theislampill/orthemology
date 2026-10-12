"""Portable source-only replay of the accepted criterion/history core checkpoint."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, stat, subprocess

ROOT = Path(__file__).resolve().parent
CORE_SHA = 'a54653b4207b15fcb2079f6bc3094a71cf026aeee9a56d8426f05ac604862b98'
REVIEW_SHA = '9f273de804295580208cea40f3a72ce4215f9c3ab078d96d787332dd82f973a3'
MATHLIB_PIN_SHA = 'c01c0b3cf6bed3a960794e7da55231e446c7622f9c953b5c0e82092d026bb431'
MATHLIB_FILES = 6816
LEAN_SHA = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
IMPORTS = ['HistoryModel','HistoryInvariant','HistorySafety','HistoryTrace',
           'TypedCriterionGuard','CriterionInstallation','DynamicInterlock','Composition']
MODULES = ['JoinModel','JoinInvariant','JoinSafety','JoinTrace','OriginalTranslation','TypedInstantiation']

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

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

def verify_checkpoint():
    require(digest(regular_path(ROOT,'MANIFEST.json')) == CORE_SHA, 'Accepted core manifest changed')
    core=json.loads((ROOT/'MANIFEST.json').read_text())
    for record in core['files']: verify_record(ROOT,record)
    require(digest(regular_path(ROOT,'review/CORE_V1_RECEIPT.json')) == REVIEW_SHA, 'Review receipt changed')
    review=json.loads((ROOT/'review/CORE_V1_RECEIPT.json').read_text())
    require(review['candidate_manifest_sha256']==CORE_SHA, 'Review is bound to another core')
    for record in review['bound_review_artifacts']: verify_record(ROOT/'review',record)
    require(digest(regular_path(ROOT,'MATHLIB_SOURCE_PIN.json'))==MATHLIB_PIN_SHA,
            'Independently pinned Mathlib source manifest changed')
    public=json.loads(regular_path(ROOT,'PUBLIC_MANIFEST.json').read_text())
    exact_inventory(ROOT,public['files'],'PUBLIC_MANIFEST.json')
    for record in public['files']: verify_record(ROOT,record)
    return digest(ROOT/'PUBLIC_MANIFEST.json')

def require_fresh_output(output, protected):
    require(not output.exists() and not output.is_symlink(), 'Output path must be absent')
    resolved=output.resolve()
    for tree in protected:
        root=tree.resolve()
        require(resolved!=root and root not in resolved.parents,
                f'Output is inside a protected input/dependency tree: {tree}')
    return resolved

def run_stage(command, env, log, timeout):
    try:
        result=subprocess.run(command,env=env,text=True,stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,timeout=timeout)
        log.write_text(result.stdout)
        return result.returncode,result.stdout
    except subprocess.TimeoutExpired as error:
        partial=error.stdout or ''
        if isinstance(partial,bytes): partial=partial.decode('utf-8',errors='replace')
        log.write_text(partial+f'\nREPLAY_TIMEOUT after {timeout} seconds\n')
        raise RuntimeError(f'Stage timed out; partial diagnostics preserved at {log.name}') from error

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

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean',type=Path,required=True)
    parser.add_argument('--mathlib',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--stage-timeout',type=float,default=300,
                        help='Per-compiler-stage seconds, greater than zero and at most 600')
    args=parser.parse_args()
    require(0 < args.stage_timeout <= 600,'Stage timeout must be greater than zero and at most 600')
    lean,mathlib=args.lean.resolve(),args.mathlib.resolve()
    output=require_fresh_output(args.output,[ROOT,mathlib,lean.parent.parent])
    public_identity=verify_checkpoint()
    require(lean.is_file() and digest(lean)==LEAN_SHA,'Compiler differs from official pinned Lean 4.19.0')
    version=subprocess.run([str(lean),'--version'],capture_output=True,text=True,check=True,
                           timeout=30).stdout.strip()
    require('4.19.0' in version and '6caaee842e94' in version,'Unexpected compiler version')
    dependency=json.loads((ROOT/'MATHLIB_SOURCE_PIN.json').read_text())
    require(dependency['commit']=='c44e0c8ee63ca166450922a373c7409c5d26b00b','Unexpected Mathlib pin')
    require(len(dependency['files'])==MATHLIB_FILES and
            len({item['path'] for item in dependency['files']})==MATHLIB_FILES,'Unexpected dependency inventory')
    for record in dependency['files']: verify_record(mathlib,record)
    cache=mathlib/'.lake/build/lib/lean'
    packages=sorted((mathlib/'.lake/packages').glob('*/.lake/build/lib/lean'))
    require((cache/'Mathlib.olean').is_file() and packages,'Required dependency caches are missing')
    output.mkdir(parents=True,exist_ok=False)
    build,logs=output/'build',output/'logs';build.mkdir();logs.mkdir()
    env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,[build,cache]+packages)),PYTHONDONTWRITEBYTECODE='1')
    env.pop('LEAN_SRC_PATH',None)
    env.pop('LEAN_SYSROOT',None)
    stages=[]
    sources=[(name,ROOT/'imports'/f'{name}.lean') for name in IMPORTS]
    sources += [(name,ROOT/f'{name}.lean') for name in MODULES]
    sources += [('CoreChallenges',ROOT/'review/CoreChallenges.lean'),
                ('AllAxioms',ROOT/'review/core-v1-replay/AllAxioms.lean')]
    try:
        for name,source in sources:
            require(not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b',proof_tokens(source.read_text())),
                    f'Forbidden proof construct in {name}')
            command=[str(lean),'-j1','-o',str(build/f'{name}.olean'),str(source)]
            log=logs/f'{name}.log'
            rc,text=run_stage(command,env,log,args.stage_timeout)
            require(rc==0 and not re.search(r'sorryAx|warning:|error:',text),
                    f'Compilation failed or emitted a forbidden diagnostic: {name}')
            stages.append({'module':name,'source_sha256':digest(source),'exit_code':rc,
                           'command':command,'log_sha256':digest(log)})
        axiom_text=(logs/'AllAxioms.log').read_text()
        require(len(re.findall(r"depends on axioms:|does not depend on any axioms",axiom_text))==85,
                'Incomplete all-theorem axiom audit')
        for closure in re.findall(r'depends on axioms:\s*\[([^]]*)\]',axiom_text,re.S):
            names={name.strip() for name in closure.split(',') if name.strip()}
            require(names <= {'propext','Classical.choice','Quot.sound'},'Unexpected theorem axiom')
        require(verify_checkpoint()==public_identity,'Distribution identity changed during replay')
        receipt={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 'core_manifest_sha256':CORE_SHA,'review_receipt_sha256':REVIEW_SHA,
                 'public_manifest_sha256':public_identity,'compiler_version':version,'compiler_sha256':LEAN_SHA,
                 'mathlib_source_commit':dependency['commit'],'mathlib_source_files':len(dependency['files']),
                 'custom_sources_compiled':len(sources),'new_theorems_audited':85,'stage_timeout_seconds':args.stage_timeout,
                 'stages':stages,'claim':'Source-only replay of scoped core acceptance; no lifecycle/progress/physical claim.'}
        (output/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps({key:receipt[key] for key in ['status','core_manifest_sha256',
              'custom_sources_compiled','new_theorems_audited','mathlib_source_files']},indent=2))
    except BaseException as error:
        (output/'REPLAY_FAILURE.json').write_text(json.dumps({'status':'FAIL','error':str(error),'completed_stages':stages},indent=2)+'\n')
        raise

if __name__=='__main__':
    main()
