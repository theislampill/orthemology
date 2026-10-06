"""PRIVATE pure D04 output readers for adapter review; never execute or write.

This does not replace first-run child tracing, source prerequisite verification,
or the adapter's independent target/type/axiom/closure audit. Original records
that lack real child timestamps stay explicitly incomplete for that purpose.
"""
from pathlib import Path
import ast,json,re
from v5_d04_normalizers_base import require,sha,file_at,read_json,positive,rejected,audit_log,source_hashes,AXIOMS,LEAN_SHA

FIXTURE_SHA='e4ae2e2751535e625f245a1bb2f2e4f2f4c447a55c859e1b1c94dbbf48adf359'
PINNED={
 'criterion':{'source':'START_HERE.md','source_sha256':'066e051e6c68174e4af4726f0376040f8d8cf488a78e128510ef9338536ff320','translation_sha256':'bf523ead0857eb9d8b32df3ab6bd7cb318ea60cb647d4fd33d2ba8f3f2d22414'},
 'covering':{'source':'replay_public.py','source_sha256':'e9e76dc61e99b298c47d4a3a139916111ef5b04be42fb729d0ebc60be770e970','translation_sha256':'21159be0c2ac468d5d26f9a3d69f130c116bafc3c7c1b6659a000910e5c09607'},
 'composition-main':{'source':'replay.py','source_sha256':'4656b1c925e8e50c0ef8a57906b4037b2c1c2c31a38df3be6915ebd6070d25f3'},
 'composition-projection':{'source':'verify_projection.py','source_sha256':'33643c09fee29687c966f944b4fde3d91b480ca6547f2d6cca6cb7044c2eaae0'},
 'composition-packaging':{'source':'packaging-tests/test_projection.py','source_sha256':'ce95f6bb2ab3353ee4360b093700b7ba85c2817d962b5efe16b2408e41e31880','translation_sha256':'4b4ef1c26c2dcd63a23c73dfa89a9c43b7e80b94afd4837a8d7610673a6fad61'},
 'composition-review':{'source':'independent-review/verify_terminal.py','source_sha256':'877c22d3527b5b43925e01e68c727b1f38ba392d96e1d43b187c6d9ada4777b1','translation_sha256':'a11bf019baf01701b747cdf769063ac883e152ef5e0eb243e874e130f974903a'},
 'composition-mutations':{'source':'check_mutations.py','source_sha256':'b6b88d0afd88b33f489dfceb6521ccd0a44ca5781cd60e5031f8380433651b50','translation_sha256':'607b0b78739ad204edd8b91a9d963271a9f28048f23e9370e14f29686c21ba38'}}

def full_inventory(root):
    root=Path(root);values={}
    for p in sorted(root.rglob('*')):
        require(not p.is_symlink(),'Symlink in original source inventory')
        if p.is_file():values[p.relative_to(root).as_posix()]={'sha256':sha(p.read_bytes()),'bytes':p.stat().st_size}
    return values

def parent_ok(physical):
    require(physical['terminal']=='COMPLETED' and type(physical['exit_code']) is int and physical['exit_code']==0,'Physical parent not completed with exit 0')

def journal(output,expected):
    rows=read_json(output,'STAGES.json');require([r['id'] for r in rows]==list(expected),'Missing/reordered source-prescribed child')
    children=[]
    for row in rows:
        name=row['id'];contract=expected[name]
        require(row['terminal']=='COMPLETED' and type(row['exit_code']) is int and row['exit_code']==contract['exit_code'],'Wrong actual child terminal '+name)
        require(isinstance(row['argv'],list) and row['argv'] and all(isinstance(a,str) and a for a in row['argv']),'Missing actual child argument vector '+name)
        require(isinstance(row['cwd'],str) and row['cwd'],'Missing actual child cwd')
        require(isinstance(row['started_at'],str) and isinstance(row['ended_at'],str),'Missing measured child interval')
        relative=contract.get('log','logs/'+name+'.log')
        require(row.get('log',relative)==relative,'Child log association differs')
        data=file_at(output,relative).read_bytes();require(sha(data)==row['log_sha256'],'Child journal/log digest mismatch')
        text=data.decode()
        require(all(lit in text for lit in contract.get('diagnostics',[])),'Missing source diagnostic '+name)
        if row['exit_code']:
            require(not re.search(r'unknown (?:module|identifier|constant|namespace)|no such file|file not found|out of memory|maximum (?:recursion|heartbeats)|timed out',text,re.I),'Infrastructure failure cannot be a mutation rejection')
        else:require('sorryAx' not in text,'Proof hole in successful child')
        children.append({**row,'log_relative_path':relative,'expected_exit_code':contract['exit_code'],'expected_diagnostics':contract.get('diagnostics',[]),'mode':'ACTUAL_TRANSLATION_CHILD_JOURNAL'})
    return children

def mutation_table(path,var='mutations'):
    tree=ast.parse(Path(path).read_text())
    return next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id==var for t in n.targets))

def criterion(source_root,output,physical):
    parent_ok(physical);source_root=Path(source_root)
    require(sha(file_at(source_root,PINNED['criterion']['source']).read_bytes())==PINNED['criterion']['source_sha256'],'Wrong original criterion contract')
    names=['verify-bundle','python-tests','criterion-transport','typed-criterion','criterion-installation','bounded-audit','repair-fixtures-generate','repair-fixtures-lean','repair-fixtures-compare','install-fixtures-generate','install-fixtures-lean','install-fixtures-compare']
    children=journal(output,{n:{'exit_code':0} for n in names})
    receipt=read_json(output,'RECIPE_RECEIPT.json')
    require(receipt['status']=='PASS_ORIGINAL_CRITERION_V3_VECTORS' and receipt['source_recipe_sha256']==PINNED['criterion']['source_sha256'],'Criterion recipe incomplete')
    require(receipt['stages']==read_json(output,'STAGES.json'),'Criterion terminal journal differs')
    require(receipt['source_before']==receipt['source_after']==full_inventory(source_root),'Criterion source input changed')
    require(receipt['source_fixture_bytes']==3013 and receipt['source_fixture_sha256']==FIXTURE_SHA,'Criterion source fixture drift')
    test=file_at(output,'logs/python-tests.log').read_text();require(re.search(r'Ran 44 tests in ',test) and re.search(r'(?m)^OK\s*$',test),'Original 44 tests incomplete')
    for name,key in [('CROSS_LANGUAGE_GREEN.json','repair'),('RULE_INSTALL_CROSS_LANGUAGE.json','installation'),('RULE_INSTALL_BOUNDED_AUDIT.json','bounded_installation')]:
        require(read_json(output,'work/evidence/'+name)==receipt[key],'Criterion aggregate differs from actual generated output')
    repair=receipt['repair'];install=receipt['installation'];b=receipt['bounded_repair_product'];ib=receipt['bounded_installation']
    require(b['state_command_pairs']==393216 and b['applied']==480 and b['rejected']==392736,'Repair census differs')
    require(repair['passed'] is True and repair['compared']==393216 and repair['mismatches']==0,'Cross-language repair mismatch')
    require(install['passed'] is True and install['python_rows']==4096 and install['lean_rows']==4096 and install['mismatches']==0,'Cross-language installation mismatch')
    require(ib['cases']==4096 and ib['applied']==8 and ib['rejected']==4088,'Installation census differs')
    objects={n:sha(file_at(output,'build/'+n+'.olean').read_bytes()) for n in ['TypedCriterionGuard','CriterionInstallation']}
    return {'children':children,'objects':objects,'summary':{'tests':44,'repair_cases':393216,'installation_cases':4096,'source_bytes':3013},'scope':'Bounded original vectors. Additional fresh CriterionTransport object and exact target audit remain adapter stages.'}

def covering(source_root,output,physical):
    parent_ok(physical);source_root=Path(source_root);expected={}
    require(sha(file_at(source_root,'replay_public.py').read_bytes())==PINNED['covering']['source_sha256'],'Covering original wrapper differs')
    def add(name,log,code=0,diags=()):expected[name]={'log':log,'exit_code':code,'diagnostics':list(diags)}
    add('lean-version','kernel/logs/lean-version.log');add('verify-inputs-before','kernel/inputs-before.log')
    for n in ['RootImage','Availability']:add(n,'kernel/logs/dependency-'+n+'.log')
    science=['CoveringPortfolio','LabelTransport','OpaqueSearch','CanonicalReplies','RandomizedFinite','RandomizedSearch','SourceCorrespondence','ExactCap','OpaqueActions','FullCommandInterface','RepairStateBridge']
    for n in science:add(n,'kernel/logs/'+n+'.log')
    tests=['TargetCovering','TargetSearch','NegativeControls','Check']
    for n in tests:add(n,'kernel/logs/test-'+n+'.log')
    for suffix in ['', '_OPTIMIZED']:add('author-semantics'+suffix,'kernel/author-semantics'+suffix+'.log')
    for n,filename,old,new in mutation_table(file_at(source_root,'science/tests/mutation_controls.py')):
        add('author-'+n,'kernel/mutants/'+n+'.log',1,['error:']+(['application type mismatch'] if n=='missing_opacity' else []))
    add('verify-inputs-after','kernel/inputs-after.log');add('independent-proofs','independent-proofs.log');add('all-author-axioms','all-author-axioms.log')
    for n,filename,old,new in mutation_table(file_at(source_root,'review/check_primary_mutants.py')):add('primary-'+n,'primary-mutants/'+n+'.log',1,['error:'])
    for suffix in ['', '_OPTIMIZED']:add('review-semantics'+suffix,'independent-semantics'+suffix+'.log')
    children=journal(output,expected);receipt=read_json(output,'PUBLIC_REPLAY_RESULT.json')
    require(receipt['status']=='PASS' and receipt['author_mutations_rejected']==6 and receipt['independent_primary_mutations_rejected']==6,'Covering mutation census incomplete')
    for k in ['normal_and_optimized_semantic_results_match_archived_evidence','immutable_payload_before_after','successful_compiler_logs_clean']:require(receipt[k] is True,'Covering terminal condition missing '+k)
    require(receipt['lean_sha256']==LEAN_SHA and receipt['mathlib_revision']=='c44e0c8ee63ca166450922a373c7409c5d26b00b','Covering toolchain drift')
    for outputname,sourcefile in [('kernel/SEMANTIC_RESULTS.json','science/tests/SEMANTIC_RESULTS.json'),('kernel/SEMANTIC_RESULTS_OPTIMIZED.json','science/tests/SEMANTIC_RESULTS.json'),('INDEPENDENT_SEMANTICS.json','review/final-replay/SEMANTICS.json'),('INDEPENDENT_SEMANTICS_OPTIMIZED.json','review/final-replay/SEMANTICS.json')]:
        require(file_at(output,outputname).read_bytes()==file_at(source_root,sourcefile).read_bytes(),'Covering semantic golden bytes differ')
    require(file_at(output,'kernel/INPUT_VERIFICATION.json').read_bytes()==file_at(output,'kernel/INPUT_VERIFICATION_AFTER.json').read_bytes(),'Covering input verification differs')
    counts=read_json(source_root,'review/final-replay/FINAL_CHECKS.json')
    audit_log(output,'all-author-axioms.log',counts['author_declarations_axiom_checked']);audit_log(output,'independent-proofs.log',counts['reviewer_theorems_axiom_checked'])
    objects={n:sha(file_at(output,'kernel/'+n+'.olean').read_bytes()) for n in ['RootImage','Availability']+science+tests+['IndependentChecks']}
    return {'children':children,'objects':objects,'summary':receipt,'scope':'Source-bound complete covering vectors; exact target closure audit remains separate.'}

def composition_projection(source_root,physical,actual_stdout):
    parent_ok(physical)
    require(sha(file_at(source_root,'verify_projection.py').read_bytes())==PINNED['composition-projection']['source_sha256'],'Original projection verifier differs')
    manifest=read_json(source_root,'PROJECTION_MANIFEST.json');actual=json.loads(actual_stdout)
    require(actual=={'status':'PASS','scope':'Explicit public projection; no claim of full original-packet inclusion',
                    **{k:len(manifest[k]) for k in ['retained','independent_review','added','excluded']}},'Projection verifier terminal/census differs')
    return {'summary':actual,'scope':'Current public archive projection integrity only; no full upstream/freeze verification.'}

def composition_packaging(source_root,output,physical):
    parent_ok(physical)
    require(sha(file_at(source_root,'packaging-tests/test_projection.py').read_bytes())==PINNED['composition-packaging']['source_sha256'],'Original packaging test differs')
    children=journal(output,{'packaging-unittest':{'exit_code':0}});receipt=read_json(output,'PACKAGING_RECEIPT.json')
    expected=['test_exact_projection_passes','test_excluded_process_file_fails','test_missing_retained_file_fails','test_modified_science_fails']
    require(receipt['status']=='PASS_OPTIONAL_SOURCE_PACKAGING_TESTS' and receipt['tests']==expected and receipt['stages']==read_json(output,'STAGES.json'),'Packaging terminal/census differs')
    source_hashes(source_root,receipt['source_hashes']);source_hashes(Path(output)/'work',receipt['source_hashes'])
    text=file_at(output,'logs/packaging-unittest.log').read_text()
    require(re.search(r'Ran 4 tests in ',text) and re.search(r'(?m)^OK\s*$',text),'Original packaging test count incomplete')
    for name in expected:require(re.search(r'(?m)^'+re.escape(name)+r' \([^\n]+\) \.\.\. ok$',text),'Missing original packaging outcome '+name)
    return {'children':children,'summary':{'packaging_tests':4},'scope':'Optional packaging controls only; no semantic compiler rejection or new scientific credit.'}

def composition_main(source_root,output,physical):
    parent_ok(physical);source_root=Path(source_root);receipt=read_json(output,'REPLAY_RECEIPT.json')
    require(sha(file_at(source_root,'replay.py').read_bytes())==PINNED['composition-main']['source_sha256']==receipt['wrapper_sha256'],'Original composition driver differs')
    require(receipt['status']=='PASS' and receipt['lean_sha256']==LEAN_SHA and 'version 4.19.0,' in receipt['toolchain'],'Composition terminal/toolchain invalid')
    modules=['TypedCriterionGuard','CriterionInstallation','DynamicInterlock','Composition','Fixtures','LocalTests','DynamicTests','BatchTests','RaceTests','Artifacts','ClockTests','TestRunner']
    logs=['toolchain-version']+['compile-'+m for m in modules]+['native-link','native-run']
    require([r['log'] for r in receipt['commands']]==[n+'.log' for n in logs],'Composition physical command inventory differs')
    children=[]
    for name,row in zip(logs,receipt['commands']):
        child=positive(output,name,row['log'],row['returncode'],recorded_sha=row['sha256'])
        require(isinstance(row['argv'],list) and row['argv'],'Original composition argv absent')
        children.append({**child,'actual_argv':row['argv'],'measured_duration_seconds':row['seconds'],'actual_child_interval_requires_first_run_tracer':True})
    text=file_at(output,'native-run.log').read_text();expected=read_json(source_root,'tests/EXPECTED_PASS_LINES.json');lines=text.splitlines()
    require([x for x in lines if x.startswith('PASS ')]==expected and len(expected)==88 and lines[0]=='SOURCE_BYTES 3013' and lines[-1]=='TERMINAL PASS' and 'FAIL' not in text,'Composition native assertions incomplete')
    wt=file_at(output,'wrapper-tests.log').read_text();require(re.search(r'Ran 7 tests in ',wt) and re.search(r'(?m)^OK\s*$',wt),'Seven wrapper tests missing')
    require(receipt['pass_assertions']==88 and receipt['wrapper_tests']==7,'Composition count drift')
    require(receipt['finite_cases']=={'revocation':80,'cancellation':60,'open_withheld':20,'two_batch_taint_sets':5,'macro_attempts':40},'Composition finite source cases differ')
    source=file_at(output,'build/source.bin').read_bytes();require(len(source)==3013 and sha(source)==FIXTURE_SHA==receipt['source_sha256'] and receipt['source_bytes']==3013,'Composition fixture identity differs')
    before,installed,repaired=[read_json(output,'build/'+n+'.json') for n in ['before','installed','repaired']]
    require(before['source']['content']==list(source),'Composition source content differs')
    expected_installed=dict(before,rule='exact',rule_version=4,rule_history=['normalizedLF'])
    expected_repaired=dict(expected_installed,draft=list(source),draft_revision=9,draft_history=[[88],list(source)+[10]])
    require(installed==expected_installed and repaired==expected_repaired,'Composition full successor differs')
    for name,h in receipt['output_artifact_hashes'].items():require(sha(file_at(output,'build/'+name).read_bytes())==h,'Composition output hash drift')
    for name,h in receipt['build_source_hashes'].items():require(sha(file_at(output,'build/'+name).read_bytes())==h,'Fresh composition source drift')
    require(set(receipt['build_source_hashes'])=={n+'.lean' for n in modules},'Composition source census incomplete')
    require(sha(file_at(output,'build/composed-tests').read_bytes())==receipt['executable_sha256'],'Composition native artifact drift')
    objects={n:sha(file_at(output,'build/'+n+'.olean').read_bytes()) for n in modules}
    children.append({'id':'wrapper-tests','log_sha256':sha(file_at(output,'wrapper-tests.log').read_bytes()),'log_relative_path':'wrapper-tests.log','actual_argv_terminal_interval_requires_first_run_tracer':True})
    return {'children':children,'objects':objects,'summary':{'native_assertions':88,'wrapper_tests':7,'finite_cases':receipt['finite_cases'],'source_bytes':3013},'scope':'Original main compiled reference run; reviewer and six serial runtime mutations remain separate stages of this physical suite.'}

def composition_review(source_root,output,physical):
    parent_ok(physical);require(sha(file_at(source_root,'independent-review/verify_terminal.py').read_bytes())==PINNED['composition-review']['source_sha256'],'Review contract differs')
    names=['independent-compile','independent-link','independent-native','reviewer-monotonicity'];children=journal(output,{n:{'exit_code':0} for n in names})
    receipt=read_json(output,'REVIEW_COMPONENT_RECEIPT.json')
    require(receipt['status']=='PASS_SUPPLIED_REVIEW_COMPONENTS' and receipt['stages']==read_json(output,'STAGES.json'),'Reviewer terminal differs')
    source_hashes(source_root,receipt['source_contracts'])
    require(receipt['independent_native_assertions']==25 and receipt['reviewer_monotonicity_readbacks']==3 and receipt['source_before_after_unchanged'] is True and receipt['preceding_fresh_build_before_after_unchanged'] is True,'Reviewer components incomplete')
    text=file_at(output,'logs/independent-native.log').read_text();lines=text.splitlines()
    require(len([x for x in lines if x.startswith('PASS independent:')])==25 and lines[-1]=='INDEPENDENT TERMINAL PASS' and 'FAIL' not in text,'Reviewer native assertions incomplete')
    audit_log(output,'logs/reviewer-monotonicity.log',3)
    return {'children':children,'objects':{n:sha(file_at(output,'build/'+n+'.olean').read_bytes()) for n in ['IndependentTests','ReviewerMonotonicity']},'summary':{'native_assertions':25,'monotonicity_readbacks':3}}

def composition_mutations(source_root,output,physical,translation_path):
    parent_ok(physical);translation_path=Path(translation_path)
    require(sha(file_at(source_root,'check_mutations.py').read_bytes())==PINNED['composition-mutations']['source_sha256'],'Original mutation wrapper differs')
    require(sha(translation_path.read_bytes())==PINNED['composition-mutations']['translation_sha256'],'Unapproved serial mutation translation')
    table=mutation_table(translation_path,'MUTATIONS');require(len(table)==6,'Six serial controls required')
    receipt=read_json(output,'MUTATION_RESULTS.json');require(receipt['status']=='PASS' and [r['mutation'] for r in receipt['records']]==list(table),'Mutation census incomplete')
    original=file_at(source_root,'Composition.lean').read_bytes();require(sha(original)==receipt['accepted_source_sha256'],'Accepted source changed')
    # Identical theorem-erasure transformation to the inspected translation;
    # parsing source text is not importing or executing that archived program.
    text=original.decode();matches=list(re.finditer(r'(?m)^(?:theorem |def |structure |inductive |instance |end |namespace |import |open |#print )',text));chunks=[text[:matches[0].start()]]
    for i,m in enumerate(matches):
        block=text[m.start():matches[i+1].start() if i+1<len(matches) else len(text)]
        if not block.startswith(('theorem ','#print ')):chunks.append(block)
    erased=''.join(chunks);children=[]
    for row in receipt['records']:
        name=row['mutation'];old,new,diagnostic=table[name];require(erased.count(old)==1,'Mutation source match changed')
        mutant=erased.replace(old,new).encode();require(file_at(output,name+'/Composition.lean').read_bytes()==mutant and sha(mutant)==row['mutant_source_sha256'],'Mutation source differs')
        require(row['status']=='DETECTED' and row['expected_failure']==diagnostic,'Runtime mutant disposition differs')
        child=rejected(output,name+'/runtime',name+'/runtime.log',row['exit_code'],[diagnostic]);require(child['log_sha256']==row['runtime_log_sha256'],'Runtime mutant log differs')
        children.append({**child,'mutant_source_sha256':sha(mutant),'actual_argv_terminal_interval_requires_first_run_tracer':True})
    return {'children':children,'summary':{'runtime_mutants':6,'actual_driver_processes':66},'scope':'Six theorem-erased native sensitivity controls; actual compiler/link child journals require first-run tracing. Mutants are never accepted theorem sources.'}
