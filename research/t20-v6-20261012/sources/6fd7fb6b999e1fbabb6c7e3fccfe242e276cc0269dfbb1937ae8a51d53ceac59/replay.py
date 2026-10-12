"""Portable source-only replay of the Orthemology v5 operational-model checkpoint, artifact revision 6."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, stat, subprocess

ROOT = Path(__file__).resolve().parent
SCIENCE_SHA = '58798e94a43d42595c58f61de8c0ec42be89275530d00b52e4f31024b4e7f611'
MANIFESTS = {
 'MANIFEST.json': SCIENCE_SHA,
 'PREDECESSOR_MANIFEST_V5.json': 'bc52d02249a41172488dc7caa34844802eeec4df811f644e4888ad2f412792d5',
 'PREDECESSOR_MANIFEST_V4.json': '86e13c356edcd1485f69e907329f7883e17bcb57ee19b98307a80ed6d601b896',
 'lineage/core-v1-MANIFEST.json': 'a54653b4207b15fcb2079f6bc3094a71cf026aeee9a56d8426f05ac604862b98',
 'lineage/typed-history-v2-MANIFEST.json': '8fef9a6bca00d9cfaeb4dda16dceb441307e90341de2ef96f0900bf001ab2f82',
}
REVIEWS = {
 'REFERENCE_CLOCK_V6_RECEIPT.json': ('6246f237935644a88efe04a14ec2ce5d33e20884edc9603bf4dba4176b39bfcb',SCIENCE_SHA),
 'CORE_V1_RECEIPT.json': ('9f273de804295580208cea40f3a72ce4215f9c3ab078d96d787332dd82f973a3','a54653b4207b15fcb2079f6bc3094a71cf026aeee9a56d8426f05ac604862b98'),
 'TYPED_V2_RECEIPT.json': ('b7b51227add21bf5f45718b6e9cede7a0aa159d3d3cbc50cc9b7404202b78585','8fef9a6bca00d9cfaeb4dda16dceb441307e90341de2ef96f0900bf001ab2f82'),
 'RUNTIME_V4_RECEIPT_CORRECTED_V1.json': ('0e3e2e6cfb8cfde7be91871b4decd40e437b1f05b9bdd766c0d8878921ea2dbe','86e13c356edcd1485f69e907329f7883e17bcb57ee19b98307a80ed6d601b896'),
 'CANCELLATION_V5_RECEIPT.json': ('a76354ecb7aafebc3396839ba78f3f593e4803a50fcfa791360388755260115b','bc52d02249a41172488dc7caa34844802eeec4df811f644e4888ad2f412792d5'),
}
MATHLIB_PIN_SHA = 'c01c0b3cf6bed3a960794e7da55231e446c7622f9c953b5c0e82092d026bb431'
MATHLIB_FILES = 6816
LEAN_SHA = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
THEOREM_COUNT = 312
EXPECTED_CACHE_PACKAGES = ('LeanSearchClient','Qq','aesop','batteries','importGraph','plausible','proofwidgets')
UNUSED_PINNED_PACKAGES = ('Cli',)
NATIVE_SOURCE_SHA = 'e4ae2e2751535e625f245a1bb2f2e4f2f4c447a55c859e1b1c94dbbf48adf359'
CHALLENGES = [
 ('CoreChallenges','CommonModelReview'),
 ('TypedV2Challenges','TypedV2Review'),
 ('RuntimeV4Challenges','RuntimeV4Review'),
 ('CancellationV5Challenges','CancellationV5Review'),
 ('ReferenceClockV6Challenges','ReferenceClockV6Review'),
]

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

def verify_source_embedding():
    raw=regular_path(ROOT,'imports/proper-function-and-candidate-e.md').read_bytes()
    require(len(raw)==3013 and hashlib.sha256(raw).hexdigest()==NATIVE_SOURCE_SHA,
            'Exact native source identity mismatch')
    source=regular_path(ROOT,'PinnedSource.lean').read_text()
    match=re.search(r'def sourceBytes : List Nat := \[([0-9,\s]+)\]',source)
    require(match is not None,'Native source embedding shape changed')
    embedded=bytes(int(value) for value in re.findall(r'\d+',match.group(1)))
    require(embedded==raw,'Native source byte embedding differs from the bound input')

def verify_checkpoint():
    for relative,expected in MANIFESTS.items():
        path=regular_path(ROOT,relative)
        require(digest(path)==expected, f'Accepted scientific manifest changed: {relative}')
        for record in json.loads(path.read_text())['files']: verify_record(ROOT,record)
    verify_source_embedding()
    projection=json.loads(regular_path(ROOT,'PROJECTION_MAP.json').read_text())['maps']
    omitted={record['source']:record for record in projection if 'omitted_reason' in record}
    for relative,(expected,candidate) in REVIEWS.items():
        path=regular_path(ROOT/'review',relative)
        require(digest(path)==expected,f'Independent review receipt changed: {relative}')
        review=json.loads(path.read_text())
        require(review['candidate_manifest_sha256']==candidate,'Review binds a different scientific candidate')
        for record in review['bound_review_artifacts']:
            if record['path'] in omitted:
                entry=omitted[record['path']]
                require(record['path'].endswith('.py') and record['sha256']==entry['sha256'] and
                        record.get('bytes',record.get('size'))==entry['bytes'],
                        'Only identified historical drivers may be omitted from the public projection')
            else: verify_record(ROOT/'review',record)
    for record in projection:
        if 'public_path' in record:
            verify_record(ROOT,dict(record,path=record['public_path']))
    require(digest(regular_path(ROOT,'MATHLIB_SOURCE_PIN.json'))==MATHLIB_PIN_SHA,
            'Independently pinned Mathlib source manifest changed')
    public=json.loads(regular_path(ROOT,'PUBLIC_MANIFEST.json').read_text())
    exact_inventory(ROOT,public['files'],'PUBLIC_MANIFEST.json')
    for record in public['files']: verify_record(ROOT,record)
    return digest(ROOT/'PUBLIC_MANIFEST.json')

def source_order():
    original=json.loads((ROOT/'SOURCE_ORDER.json').read_text())
    new=original['new']
    new+=json.loads((ROOT/'CANCELLATION_SOURCE_ORDER.json').read_text())['additional_modules']
    new+=json.loads((ROOT/'REFERENCE_CLOCK_SOURCE_ORDER.json').read_text())['additional_modules']
    require(len(original['imports'])==9 and len(new)==32,'Unexpected source-order inventory')
    return original['imports'],new

def theorem_names(source,namespace):
    return [namespace+'.'+name for name in re.findall(r"\btheorem\s+([A-Za-z_][A-Za-z0-9_']*)",
                                                     proof_tokens(source.read_text()))]

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
                              stderr=subprocess.STDOUT,timeout=timeout,cwd=ROOT)
        log.write_text(result.stdout)
        return result.returncode,result.stdout
    except subprocess.TimeoutExpired as error:
        partial=error.stdout or ''
        if isinstance(partial,bytes): partial=partial.decode('utf-8',errors='replace')
        log.write_text(partial+f'\nREPLAY_TIMEOUT after {timeout} seconds\n')
        raise RuntimeError(f'Stage timed out; partial diagnostics preserved at {log.name}') from error

def check_stage_result(code, text, name):
    require(code==0 and not re.search(r'sorryAx|warning:|error:',text),
            f'Compilation failed or emitted a forbidden diagnostic: {name}')

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

def pinned_dependency_caches(mathlib):
    records=json.loads((mathlib/'lake-manifest.json').read_text())['packages']
    names=[record['name'] for record in records]
    require(len(names)==len(set(names)) and
            set(names)==set(EXPECTED_CACHE_PACKAGES)|set(UNUSED_PINNED_PACKAGES),
            'Pinned dependency package set differs from the explicit expected set')
    roots=[mathlib/'.lake/packages'/name for name in sorted(names)]
    required=[mathlib/'.lake/packages'/name/'.lake/build/lib/lean' for name in EXPECTED_CACHE_PACKAGES]
    require(all(cache.is_dir() for cache in required),'Required pinned package cache is missing')
    unused={name:{'cache_present':(mathlib/'.lake/packages'/name/'.lake/build/lib/lean').is_dir(),
                  'reason':'Not in this proof import closure; deliberately excluded from LEAN_PATH'}
            for name in UNUSED_PINNED_PACKAGES}
    return roots,required,unused

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
    package_roots,packages,unused_package_caches=pinned_dependency_caches(mathlib)
    require((cache/'Mathlib.olean').is_file() and packages,
            'Required Mathlib/dependency cache inputs are missing')
    require_fresh_output(output,package_roots+packages+[cache])
    output.mkdir(parents=True,exist_ok=False)
    build,logs=output/'build',output/'logs';build.mkdir();logs.mkdir()
    env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,[build,cache]+packages)),PYTHONDONTWRITEBYTECODE='1')
    env.pop('LEAN_SRC_PATH',None)
    env.pop('LEAN_SYSROOT',None)
    stages=[]
    try:
        imports,new=source_order()
        sources=[(entry['module'],ROOT/entry['path']) for entry in imports+new]
        scientific_theorems=[]
        for entry in new:
            scientific_theorems+=theorem_names(ROOT/entry['path'],entry['namespace'])
        require(len(scientific_theorems)==THEOREM_COUNT and len(set(scientific_theorems))==THEOREM_COUNT,
                'Comment-aware theorem enumeration disagrees with the scientific receipt')
        challenge_theorems=[]
        for name,namespace in CHALLENGES:
            source=ROOT/'review'/f'{name}.lean'
            sources.append((name,source))
            challenge_theorems+=theorem_names(source,namespace)
        require(len(set(challenge_theorems))==len(challenge_theorems),'Duplicate review theorem name')
        audit=output/'AllAxioms.lean'
        audit.write_text('\n'.join(['import '+name for name,_ in sources]+
                        ['#print axioms '+name for name in scientific_theorems+challenge_theorems])+'\n')
        sources.append(('AllAxioms',audit))
        for name,source in sources:
            require(not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b',proof_tokens(source.read_text())),
                    f'Forbidden proof construct in {name}')
            command=[str(lean),'-j1','-s65536',f'--root={source.parent}','-o',str(build/f'{name}.olean'),str(source)]
            log=logs/f'{name}.log'
            rc,text=run_stage(command,env,log,args.stage_timeout)
            check_stage_result(rc,text,name)
            stages.append({'module':name,'source_sha256':digest(source),'exit_code':rc,
                           'command':command,'log_sha256':digest(log)})
        axiom_text=(logs/'AllAxioms.log').read_text()
        require(len(re.findall(r"depends on axioms:|does not depend on any axioms",axiom_text))==THEOREM_COUNT+len(challenge_theorems),
                'Incomplete all-theorem axiom audit')
        for closure in re.findall(r'depends on axioms:\s*\[([^]]*)\]',axiom_text,re.S):
            names={name.strip() for name in closure.split(',') if name.strip()}
            require(names <= {'propext','Classical.choice','Quot.sound'},'Unexpected theorem axiom')
        require(verify_checkpoint()==public_identity,'Distribution identity changed during replay')
        receipt={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 'scientific_manifest_sha256':SCIENCE_SHA,'review_receipts':{name:pair[0] for name,pair in REVIEWS.items()},
                 'public_manifest_sha256':public_identity,'compiler_version':version,'compiler_sha256':LEAN_SHA,
                 'mathlib_source_commit':dependency['commit'],'mathlib_source_files':len(dependency['files']),
                 'trusted_dependency_packages':[path.parents[3].name for path in packages],
                 'unused_pinned_packages':unused_package_caches,
                 'native_source_bytes':3013,'native_source_sha256':NATIVE_SOURCE_SHA,'source_embedding_verified':True,
                 'custom_sources_compiled':len(sources),'new_theorems_audited':THEOREM_COUNT,'review_theorems_audited':len(challenge_theorems),'stage_timeout_seconds':args.stage_timeout,
                 'stages':stages,'claim':'Source-only replay of bounded operational history, cancellation and NEW monotone reference-clock extension; no runBatch/progress/physical claim.'}
        (output/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps({key:receipt[key] for key in ['status','scientific_manifest_sha256',
              'custom_sources_compiled','new_theorems_audited','mathlib_source_files']},indent=2))
    except BaseException as error:
        (output/'REPLAY_FAILURE.json').write_text(json.dumps({'status':'FAIL','error':str(error),'completed_stages':stages},indent=2)+'\n')
        raise

if __name__=='__main__':
    main()
