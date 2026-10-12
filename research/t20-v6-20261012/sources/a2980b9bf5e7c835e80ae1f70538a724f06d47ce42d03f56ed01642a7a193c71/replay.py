"""Standalone fail-closed source replay of shared-root typed safety refinement.
Pinned dependency bytes are verified read-only, never rebuilt or downloaded.
"""
from pathlib import Path
import argparse,datetime,hashlib,json,math,os,re,stat,subprocess,sys,time
ROOT=Path(__file__).resolve().parent
SCIENCE_SHA='77152f583a83f037a5c94392c71cf5f0674b4181dbf2c37b830a1a46e77d903c'
TYPED_SHA='1b88370e522b085349c6da4c0aab1b3763b557e02c3c4eb6d631f9d4ab4636d7'
PINS={
 'ORIGINAL_TO_PUBLIC.json':'66abd69890710f64d3625489f3ab6f3d31333f7ceae76763c28ea20f2251f6bd',
 'dependencies/MATHLIB_SOURCE_PIN.json':'c01c0b3cf6bed3a960794e7da55231e446c7622f9c953b5c0e82092d026bb431',
 'dependencies/MATHLIB_CACHE_PIN.json':'7dc08ad35391b67f1fb930b1315432ec17321dc6ecfad13b4689f32ade95d2f9',
 'dependencies/LEAN_DISTRIBUTION_PIN.json':'6f364a506b2b7bc8934b13ef50b296fd2047d9b7894a2b7f637ad44e4f8e52fb',
 'review/typed-v1-replay/RECEIPT.json':'35fcd339e0d61f1f4d0f5be78f9e481656a0b51d841db168c861be479f91a9a4',
 'review/TYPED_V1_REVIEW.md':'a59f02cfc93afbf8655b4345a72d0d2102f3be6f013b8ffbe9a44421ad68f1c4'}
LEAN_SHA='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
MATHLIB_COMMIT='c44e0c8ee63ca166450922a373c7409c5d26b00b'
COMMON=['TypedCriterionGuard','CriterionInstallation','DynamicInterlock','Composition',
 'HistoryModel','HistoryInvariant','HistorySafety','HistoryTrace','JoinModel','JoinInvariant',
 'JoinSafety','JoinTrace','OriginalTranslation','TypedInstantiation','JoinOperations',
 'TypedHistoryProperties','TypedExamples','TypedFixtureHelpers','TypedControls']
ATTRIBUTION=['RootImage','Availability','FixedFamilies','MapTransport']
SCIENCE=['AliasModel','AliasObstruction','ModelControls','AliasRelation','AliasExpansion',
 'AliasPreservation','AliasSimulation','SimulationControls','AliasTyped','AliasRuntime',
 'AliasTypedWitness','AliasTypedControls']
REVIEW=['ReviewerControls','ReviewerSimulationControls','ReviewerTypedControls']
CONTROLS=['ModelTargets','SimulationTargets','TypedTargets','SuiteAxioms']
MUTANTS={
 'actual_budget_as_label_budget':('AliasModel',['error: type mismatch','E.labelFaults.card ≤ E.budget','label_budget E']),
 'cancel_wrong_actual_store':('AliasModel',['error: unsolved goals',r'Function\.update C\.roots \(some i\)',r'\.cancelled']),
 'drop_selected_commitment_mask':('AliasRelation',['error: invalid constructor','commitments.val']),
 'invent_alias_acknowledgements':('AliasModel',['error: type mismatch',r'\(acknowledge E C i\)\.acks = insert i C\.acks']),
 'reverse_veto_inclusion':('AliasRelation',['error: application type mismatch','h.revoked','I.commandEpoch k ∈ z.revoked'])}

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

REVIEWER_LINT_SOURCE_SHA='db9737455bc7109fd40e7ff10812604000d18d650bb4868f1007790db1c9ebe8'

def positive_diagnostics_ok(name,source_sha,text,source_path):
    """Only two exact, source-bound historical lint messages may be removed."""
    if name=='ReviewerControls':
        if source_sha!=REVIEWER_LINT_SOURCE_SHA:return False
        note="note: this linter can be disabled with `set_option linter.unnecessarySimpa false`\n"
        allowed=[str(source_path)+":66:44: warning: try 'simp at quorum' instead of 'simpa using quorum'\n"+note,
                 str(source_path)+":75:8: warning: try 'simp at certificate' instead of 'simpa using certificate'\n"+note]
        for diagnostic in allowed:
            if text.count(diagnostic)!=1:return False
            text=text.replace(diagnostic,'',1)
    return not re.search(r'warning:|error:|sorryAx',text)

def valid_timeout(value):
    return math.isfinite(value) and 0 < value <= 600

def canonical_relative(relative):
    rel=Path(relative)
    require(not rel.is_absolute() and rel.parts and str(rel)==relative and
            all(p not in ('','.','..') for p in rel.parts) and '\\' not in relative,
            f'Unsafe manifest path: {relative}')
    return rel

def verify_tree_pin(base,pin):
    """Verify exact named trees, including library symlink targets and all bytes."""
    base=base.resolve();records=pin['entries'];names=[r['path'] for r in records]
    require(len(names)==len(set(names)),'Duplicate dependency path')
    expected=set(names);observed=set()
    for root in pin['roots']:
        tree=base if root=='' else base/canonical_relative(root)
        require(tree.is_dir() and not tree.is_symlink(),f'Missing or symlinked dependency tree: {root}')
        for item in ([tree] if root else [])+list(tree.rglob('*')):
            observed.add(str(item.relative_to(base)))
    require(observed==expected,f'Dependency inventory mismatch: extra={sorted(observed-expected)}, missing={sorted(expected-observed)}')
    for r in records:
        rel=canonical_relative(r['path']);item=base/rel
        current=base
        for part in rel.parts[:-1]:
            current=current/part
            require(not current.is_symlink(),f'Symlink ancestor in dependency path: {rel}')
        kind=r['kind']
        if kind=='symlink':
            require(item.is_symlink() and os.readlink(item)==r['target'],f'Dependency symlink mismatch: {rel}')
            require(item.resolve().is_relative_to(base),f'Dependency symlink escapes root: {rel}')
            require(item.exists(),f'Dangling dependency symlink: {rel}')
        elif kind=='directory':
            require(item.is_dir() and not item.is_symlink(),f'Dependency directory mismatch: {rel}')
        elif kind=='file': verify_record(base,r)
        else: raise RuntimeError(f'Unknown dependency entry kind: {kind}')

def verify_checkpoint():
    for name,expected in PINS.items():
        require(digest(regular_path(ROOT,name))==expected,f'Pinned input changed: {name}')
    require(digest(regular_path(ROOT,'SCIENCE_MANIFEST.json'))==SCIENCE_SHA,'Scientific source inventory changed')
    science=json.loads((ROOT/'SCIENCE_MANIFEST.json').read_text())
    require(science['typed_scientific_manifest_sha256']==TYPED_SHA,'Another scientific milestone')
    expected={f'imports/common/{n}.lean' for n in COMMON}|{f'imports/attribution/{n}.lean' for n in ATTRIBUTION}
    expected|={f'science/{n}.lean' for n in SCIENCE}|{f'review/{n}.lean' for n in REVIEW}|{f'controls/{n}.lean' for n in CONTROLS}
    expected|={f'mutants/{n}/{m}.lean' for n,(m,_) in MUTANTS.items()}
    require({r['path'] for r in science['files']}==expected and len(science['files'])==len(expected),'Incomplete or duplicate scientific inventory')
    for r in science['files']:verify_record(ROOT,r)
    mapping=json.loads((ROOT/'ORIGINAL_TO_PUBLIC.json').read_text())
    for checkpoint in mapping['milestones']:
        manifest=regular_path(ROOT,checkpoint['original_manifest_path'])
        require(digest(manifest)==checkpoint['original_manifest_sha256'],'Historical manifest identity changed')
        original=json.loads(manifest.read_text())['files'];mapped=checkpoint['files']
        require(len(mapped)==len(original) and {r['original_path'] for r in mapped}=={r['path'] for r in original},'Incomplete historical mapping')
        lookup={r['path']:r for r in original}
        for r in mapped:
            old=lookup[r['original_path']]
            require((old['bytes'],old['sha256'])==(r['bytes'],r['sha256']),'Historical record changed')
            verify_record(ROOT,{'path':r['public_path'],'bytes':r['bytes'],'sha256':r['sha256']})
    review=json.loads((ROOT/'review/typed-v1-replay/RECEIPT.json').read_text())
    require(review['checks']['typed-v1']['manifest_sha256']==TYPED_SHA,'Review applies to another milestone')
    public=json.loads(regular_path(ROOT,'PUBLIC_MANIFEST.json').read_text())
    exact_inventory(ROOT,public['files'],'PUBLIC_MANIFEST.json')
    for r in public['files']:verify_record(ROOT,r)
    return digest(ROOT/'PUBLIC_MANIFEST.json')

def run_compiler_stage(command,env,log,timeout):
    start=time.monotonic()
    try:
        r=subprocess.run(command,env=env,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
        text=r.stdout;rc=r.returncode;timed_out=False
    except subprocess.TimeoutExpired as error:
        text=error.stdout or ''
        if isinstance(text,bytes):text=text.decode('utf-8',errors='replace')
        text+=f'\nREPLAY_TIMEOUT after {timeout} seconds\n';rc=None;timed_out=True
    log.write_text(text)
    return {'exit_code':rc,'timed_out':timed_out,'seconds':round(time.monotonic()-start,3),
            'text':text,'command':command,'compiler_cwd':str(ROOT),'log_sha256':digest(log)}

def classify_mutant(returncode,text,timed_out,patterns):
    resource=r'maximum recursion depth|maximum number of heartbeats|out of memory|unknown module prefix|object file .* does not exist|file not found|cannot open|REPLAY_TIMEOUT|interrupted'
    if timed_out or returncode not in (0,1) or re.search(resource,text,re.I):
        return 'RESOURCE_OR_INFRASTRUCTURE_INCONCLUSIVE'
    if returncode==0:return 'UNEXPECTED_SUCCESS'
    if 'error:' in text and all(re.search(p,text,re.S) for p in patterns):return 'REJECTED_AS_EXPECTED'
    return 'UNCLASSIFIED_FAILURE'

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

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean-root',type=Path,required=True)
    parser.add_argument('--mathlib',type=Path,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--stage-timeout',type=float,default=300)
    args=parser.parse_args()
    require(valid_timeout(args.stage_timeout),'Stage timeout must be finite, positive and at most 600 seconds')
    leanroot,mathlib=args.lean_root.resolve(),args.mathlib.resolve();lean=leanroot/'bin/lean'
    output=require_fresh_output(args.output,[ROOT,leanroot,mathlib])
    # Invalid source packages and protected/existing outputs are refused without writes.
    public_identity=verify_checkpoint()
    output.mkdir(parents=True,exist_ok=False);(output/'build').mkdir();(output/'logs').mkdir()
    build,logs=output/'build',output/'logs';stages=[];status='FAIL'
    try:
        leanpin=json.loads((ROOT/'dependencies/LEAN_DISTRIBUTION_PIN.json').read_text())
        cachepin=json.loads((ROOT/'dependencies/MATHLIB_CACHE_PIN.json').read_text())
        mathpin=json.loads((ROOT/'dependencies/MATHLIB_SOURCE_PIN.json').read_text())
        require(leanpin['version']=='4.19.0' and leanpin['release_commit']=='6caaee842e94','Wrong Lean pin')
        require(cachepin['mathlib_commit']==mathpin['commit']==MATHLIB_COMMIT and len(mathpin['files'])==6816,'Wrong Mathlib pin')
        verify_tree_pin(leanroot,leanpin);verify_tree_pin(mathlib,cachepin)
        require(digest(lean)==LEAN_SHA,'Wrong compiler binary')
        for r in mathpin['files']:verify_record(mathlib,r)
        env=dict(os.environ,LEAN_PATH=os.pathsep.join(map(str,[build]+[mathlib/r for r in cachepin['roots']])),PYTHONDONTWRITEBYTECODE='1')
        for key in ['LEAN_SRC_PATH','LEAN_SYSROOT','LD_PRELOAD','LD_LIBRARY_PATH']:env.pop(key,None)
        version=run_compiler_stage([str(lean),'--version'],env,logs/'version.log',min(30,args.stage_timeout))
        stages.append({'stage':'compiler_version',**{k:v for k,v in version.items() if k!='text'}})
        if version['timed_out']:status='INCONCLUSIVE'
        require(not version['timed_out'] and version['exit_code']==0 and '4.19.0' in version['text'] and '6caaee842e94' in version['text'],'Compiler version probe failed')
        sources=[(n,ROOT/'imports/common'/f'{n}.lean') for n in COMMON]
        sources += [(n,ROOT/'imports/attribution'/f'{n}.lean') for n in ATTRIBUTION]
        sources += [(n,ROOT/'science'/f'{n}.lean') for n in SCIENCE]
        sources += [(n,ROOT/'review'/f'{n}.lean') for n in REVIEW]
        sources += [(n,ROOT/'controls'/f'{n}.lean') for n in CONTROLS]
        for name,source in sources:
            require(not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern)\b',proof_tokens(source.read_text())),f'Forbidden proof construct: {name}')
            result=run_compiler_stage([str(lean),'-j1','-o',str(build/f'{name}.olean'),str(source)],env,logs/f'{name}.log',args.stage_timeout)
            diagnostics_ok=positive_diagnostics_ok(name,digest(source),result['text'],source)
            stages.append({'stage':name,'source_sha256':digest(source),
                           'accepted_exact_historical_lint_count':2 if name=='ReviewerControls' and diagnostics_ok else 0,
                           **{k:v for k,v in result.items() if k!='text'}})
            if result['timed_out']:status='INCONCLUSIVE'
            require(not result['timed_out'] and result['exit_code']==0 and diagnostics_ok,f'Positive proof stage failed: {name}')
        namespaces={'ModelControls':'SharedAlias.ModelControls','SimulationControls':'SharedAlias.SimulationControls',
                    'AliasTyped':'SharedAlias.Typed','AliasRuntime':'SharedAlias.Typed',
                    'AliasTypedWitness':'SharedAlias.Typed.Witness','AliasTypedControls':'SharedAlias.Typed.Controls'}
        names=[]
        for name in SCIENCE:
            ns=namespaces.get(name,'SharedAlias')
            names += [ns+'.'+t for t in re.findall(r'\btheorem\s+([A-Za-z0-9_]+)',proof_tokens((ROOT/'science'/f'{name}.lean').read_text()))]
        require(len(names)==88,'Scientific theorem inventory changed')
        scientific_axioms=audit_axioms((logs/'SuiteAxioms.log').read_text(),names)
        reviewer_names=[]
        for name in REVIEW:
            ns='SharedAlias.'+name
            reviewer_names += [ns+'.'+t for t in re.findall(r'\btheorem\s+([A-Za-z0-9_]+)',proof_tokens((ROOT/'review'/f'{name}.lean').read_text()))]
        require(len(reviewer_names)==18,'Reviewer theorem inventory changed')
        reviewer_axioms={}
        for name in REVIEW:
            subset=[n for n in reviewer_names if n.startswith('SharedAlias.'+name+'.')]
            reviewer_axioms.update(audit_axioms((logs/f'{name}.log').read_text(),subset))
        for name,(module,patterns) in MUTANTS.items():
            source=ROOT/'mutants'/name/f'{module}.lean'
            result=run_compiler_stage([str(lean),'-j1',str(source)],env,logs/f'mutant-{name}.log',args.stage_timeout)
            classification=classify_mutant(result['exit_code'],result['text'],result['timed_out'],patterns)
            stages.append({'stage':'mutant-'+name,'classification':classification,'required_diagnostics':patterns,
                           'source_sha256':digest(source),**{k:v for k,v in result.items() if k!='text'}})
            if classification=='RESOURCE_OR_INFRASTRUCTURE_INCONCLUSIVE':status='INCONCLUSIVE'
            require(classification=='REJECTED_AS_EXPECTED',f'Mutant not semantically rejected: {name}: {classification}')
        require(verify_checkpoint()==public_identity,'Source package changed during replay')
        verify_tree_pin(leanroot,leanpin);verify_tree_pin(mathlib,cachepin)
        for r in mathpin['files']:verify_record(mathlib,r)
        receipt={'status':'PASS','completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
                 'public_manifest_sha256':public_identity,'science_manifest_sha256':SCIENCE_SHA,'scientific_milestone_sha256':TYPED_SHA,
                 'compiler_sha256':LEAN_SHA,'compiler_version':version['text'].strip(),'dependency_pin_sha256':PINS,
                 'pinned_dependency_bytes_checked_before_after':True,'precompiled_dependencies_rebuilt':False,
                 'exact_custom_and_predecessor_sources_compiled':len(sources),'scientific_theorems_audited':88,
                 'reviewer_theorems_audited':18,'mutants_semantically_rejected':5,
                 'exact_historical_lint_exception':{'stage':'ReviewerControls','source_sha256':REVIEWER_LINT_SOURCE_SHA,'locations':['66:44','75:8'],'kind':'two exact unnecessarySimpa advice diagnostics'},'stage_timeout_seconds':args.stage_timeout,
                 'stages':stages,'scientific_axioms':scientific_axioms,'reviewer_axioms':reviewer_axioms,
                 'claim':'Shared-store mathematical safety refinement and typed source-gate adapter. No whole controller, progress, opacity, optimality or physical-world claim.'}
        write_json(output/'RECEIPT.json',receipt)
        print(json.dumps({k:receipt[k] for k in ['status','public_manifest_sha256','scientific_theorems_audited','reviewer_theorems_audited','mutants_semantically_rejected']},indent=2))
    except BaseException as error:
        if isinstance(error,(KeyboardInterrupt,subprocess.TimeoutExpired)):status='INCONCLUSIVE'
        write_json(output/'REPLAY_FAILURE.json',{'status':status,'error':str(error),'stages':stages,
                   'public_manifest_sha256':public_identity,'no_success_receipt':True})
        raise
if __name__=='__main__':main()
