"""Read-only terminal custody checks; writes only the final detached receipt."""
from pathlib import Path
import argparse, datetime, hashlib, json, runpy, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p):return json.loads(Path(p).read_text())

def main():
    if sys.flags.optimize:raise ValueError('Assertions must be enabled')
    p=argparse.ArgumentParser();p.add_argument('--work',type=Path,required=True);a=p.parse_args()
    A=a.work.resolve();D=A/'dependencies';E=A/'evidence';bind=read(E/'SOURCE_BUILD_DERIVATION_RECEIPT.json')
    O=Path(bind['original_package']);N=Path(bind['derived_package']);replay=A/'hase-replay';H=replay/'hase'
    base=read(ROOT/'FINAL_BASE_BINDING.json')
    assert bind['original_manifest_sha256']==base['consumer_manifest_sha256']
    assert sha(ROOT/'tools/derive_final_package.py')==base['consumer_binder_sha256']
    assert sha(ROOT/'tools/derive_package.py')==base['frozen_v3_binder_sha256']
    assert (ROOT/'tools/derive_final_package.py').read_text()==(ROOT/'tools/derive_package.py').read_text().replace(base['retained_v3_manifest_sha256'],base['consumer_manifest_sha256'])
    assert sha(O/'MANIFEST.json')==bind['original_manifest_sha256']
    assert sha(N/'MANIFEST.json')==bind['derived_manifest_sha256']
    assert sha(O/'replay.py')==sha(N/'replay.py')==bind['unchanged_runner_sha256']
    f=runpy.run_path(str(N/'replay.py'));f['verify_manifest'](O);f['verify_manifest'](N)
    before={x.relative_to(O).as_posix():sha(x) for x in O.rglob('*') if x.is_file()}
    after={x.relative_to(N).as_posix():sha(x) for x in N.rglob('*') if x.is_file()}
    assert set(before)==set(after)
    assert sorted(k for k in before if before[k]!=after[k])==['MANIFEST.json','dependencies/hase.json']
    for row in bind['scientific_and_runner_source_files_unchanged']:
        assert sha(O/row['path'])==sha(N/row['path'])==row['sha256']
    source_build=read(E/'COLD_DEPENDENCY_BUILD_RECEIPT.json')
    assert sha(E/'COLD_DEPENDENCY_BUILD_RECEIPT.json')==bind['source_build_receipt_sha256']
    assert source_build['status']=='PASS' and source_build['provenance']=='SOURCE_BUILD'
    inv=read(E/'FRESH_DEPENDENCY_SOURCE_OBJECT_INVENTORY.json')
    assert sha(E/'FRESH_DEPENDENCY_SOURCE_OBJECT_INVENTORY.json')==source_build['inventory_sha256']
    assert sha(E/'DEPENDENCY_COLD_BUILD.log')==source_build['build_log_sha256']
    assert sha(E/'DEPENDENCY_COLD_BUILD.json')==source_build['build_receipt_sha256']
    assert read(E/'DEPENDENCY_COLD_BUILD.json')['log_sha256']==source_build['build_log_sha256']
    assert sha(E/'COMPILER_PARSED_SOURCE_CLOSURE.json')==source_build['source_closure_sha256']
    for row in inv:
        assert sha(D/row['package']/row['source_path'])==row['source_sha256']
        assert sha(D/row['package']/'.lake/build/lib/lean'/row['object_relative_path'])==row['object_sha256']
    tracked=0
    for pin in read(ROOT/'inputs/lean/lake-manifest.json')['packages']:
        d=D/pin['name']; rows=read(E/f"{pin['name']}_source_inventory.json")
        assert subprocess.check_output(['git','-C',str(d),'rev-parse','HEAD'],text=True).strip()==pin['rev']
        assert not subprocess.check_output(['git','-C',str(d),'status','--porcelain','--untracked-files=no'],text=True).strip()
        for row in rows:assert sha(d/row['path'])==row['sha256']
        tracked+=len(rows)
    assert tracked==7507
    for row in read(E/'PLATFORM_TOOLS.json')['files']:assert sha(Path(row['path']))==row['sha256']
    for row in read(E/'COMPILER_PARSED_SOURCE_CLOSURE.json')['trusted_toolchain']:assert sha(Path(row['object_path']))==row['trusted_object_sha256']
    for row in read(E/'WIDGET_SOURCE_ASSETS.json')['fresh_source_built_assets']:assert sha(D/'proofwidgets'/row['path'])==row['sha256']
    f['verify_environment'](N,read(A/'hase-environment.json'),'hase')
    summary=read(replay/'RESULT.json');result=read(H/'RESULT.json')
    assert summary['status']=='PASS_REQUESTED_REPLAY' and summary['action']=='lean-hase'
    assert result['status']=='PASS_FRESH_CUSTOM_SOURCES_AND_SELECTED_CONTROLS'
    assert result['production_modules']==84 and result['selected_control_files']==8 and len(result['runs'])==92
    plan=read(N/'lean/hase/REPLAY_PLAN.json');rules={(r['group'],r['module']):r for r in plan['controls']};seen=set();audits=0
    for row in result['runs']:
        key=(row['group'],row['module']);assert key not in seen;seen.add(key)
        assert sha(H/row['source'])==row['source_sha256'] and sha(H/row['log'])==row['log_sha256'] and row['qualified']
        if row['group']=='production':
            rule={'expected_exit':0};assert row['module'] in plan['modules']
            assert row['source_sha256']==plan['modules'][row['module']]['sha256']
        else:rule=rules[key];assert row['source_sha256']==rule['sha256']
        text=(H/row['log']).read_text();assert f['qualified_output'](row['exit_code'],text,rule)
        if 'axiom_count' in rule:
            got=f['audit_axioms'](text,rule['axiom_count']);assert got==row['axiom_audits'];audits+=len(got)
        if row['exit_code']==0:
            obj=Path(row['command'][row['command'].index('-o')+1]);assert obj.is_relative_to(H) and sha(obj)==row['object_sha256']
    assert seen=={('production',n) for n in plan['modules']}|set(rules)
    diag=result['ordinary_diagnostic'];ordinary=read(H/'ordinary-diagnostic/LAMBDA_NORMAL_FORM_CHECK.json')
    assert diag['exit_code']==0 and diag['result']==ordinary
    assert ordinary['normalizer_self_tests']==7 and ordinary['distinct_alpha_classes']
    assert all(r['matches_displayed_form'] and r['no_beta_or_eta_redex'] for r in ordinary['endpoints'])
    assert sha(H/'ordinary-diagnostic/diagnostic.log')==diag['log_sha256']
    assert sha(H/'ordinary-diagnostic/DumpExactPolynomials.log')==diag['export_sha256']==ordinary['export_log_sha256']
    assert sha(N/plan['ordinary_diagnostic']['script'])==diag['script_sha256']
    freeze=ROOT/'evidence/ADAPTER_SOURCE_FREEZE_v2.json'
    for row in read(freeze)['files']:assert sha(ROOT/row['path'])==row['sha256']
    for row in read(ROOT/'inputs/INPUT_MANIFEST.json')['files']:assert sha(ROOT/'inputs'/row['path'])==row['sha256']
    clean_start=read(E/'CLEAN_START.json')
    rec={'status':'PASS_SOURCE_BUILD_AND_UNCHANGED_HASE_REPLAY','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'qualification_platform':read(E/'PLATFORM_TOOLS.json'),'fresh_external_objects':len(inv),'source_files_rechecked':tracked,
        'custom_modules':84,'selected_controls':8,'axiom_audits':audits,'ordinary_diagnostic':{'scope':diag['scope'],'normalizer_self_tests':7,'distinct_alpha_classes':True},
        'source_build_receipt_sha256':sha(E/'COLD_DEPENDENCY_BUILD_RECEIPT.json'),'originating_build_receipt_sha256':sha(E/'DEPENDENCY_COLD_BUILD.json'),'derivation_receipt_sha256':sha(E/'SOURCE_BUILD_DERIVATION_RECEIPT.json'),
        'hase_result_sha256':sha(H/'RESULT.json'),'replay_result_sha256':sha(replay/'RESULT.json'),
        'source_object_inventory_sha256':sha(E/'FRESH_DEPENDENCY_SOURCE_OBJECT_INVENTORY.json'),
        'adapter_freeze_sha256':sha(freeze),'input_manifest_sha256':sha(ROOT/'inputs/INPUT_MANIFEST.json'),
        'final_base_binding_sha256':sha(ROOT/'FINAL_BASE_BINDING.json'),'consumer_binder_sha256':base['consumer_binder_sha256'],
        'final_verifier_sha256':sha(Path(__file__)),'original_manifest_sha256':bind['original_manifest_sha256'],
        'derived_manifest_sha256':bind['derived_manifest_sha256'],'changed_package_files':['MANIFEST.json','dependencies/hase.json'],
        'unchanged_scientific_and_runner_files':len(bind['scientific_and_runner_source_files_unchanged']),
        'source_acquisition':clean_start['source_acquisition'],'registry_acquisition':clean_start['npm_download_source'],
        'new_host_network_acquisition_test':False,'byte_reproducibility_claim':False,'compiler_bootstrapped':False,'full_mathlib_built':False,
        'independent_review_still_required':True,'eighteenth_tranche_complete':False}
    (E/'FINAL_SOURCE_BUILD_QUALIFICATION.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec,indent=2))

if __name__=='__main__':main()
