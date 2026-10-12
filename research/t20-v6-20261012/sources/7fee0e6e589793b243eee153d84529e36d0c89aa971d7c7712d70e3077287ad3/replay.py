#!/usr/bin/env python3
"""Verify preserved bytes, then replay only in new isolated working trees.

Python >=3.10, standard library only. No network, compiler, Git, or Lean needed.
The evidence directory is never modified. Existing destinations are refused.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import shutil
import subprocess
import sys
import time

HERE = Path(__file__).resolve().parent
OLD_CONE = 'positive-instrument-cone-review-delta-20261010/PRE_PRECISION_RESULT.md'
CONE_RESULT = 'positive-instrument-cone-transport-20261010/RESULT.md'
OLD_HASH = 'e9f9a5465aa9f6f03f789f852e87a9847f4aa8b5641866b8c293ad2c9a1bb086'
CURRENT_HASH = '5c74c7086c038dce1be0e9098b42fce9cc4c7aee8670fe0ba682b50d780af5c0'

def digest(path):
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def load(path):
    return json.loads(path.read_text())

def save(path, value):
    path.write_text(json.dumps(value, indent=2) + '\n')

def tree_hashes(root):
    return {str(p.relative_to(root)): digest(p) for p in sorted(root.rglob('*')) if p.is_file()}

def verify_bundle():
    manifest = load(HERE/'MANIFEST.json')
    expected_paths = {item['path'] for item in manifest['files']}
    observed_paths = {str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file()} - {'MANIFEST.json'}
    assert expected_paths == observed_paths, {'missing': sorted(expected_paths-observed_paths), 'unexpected': sorted(observed_paths-expected_paths)}
    for item in manifest['files']:
        path = HERE/item['path']
        assert path.resolve().is_relative_to(HERE), 'Unsafe manifest path'
        assert digest(path) == {key: item[key] for key in ('bytes','sha256')}, item['path']
    return manifest

def packet_manifests(evidence):
    checks = []
    meta = load(HERE/'METADATA.json')
    for name in meta['manifest_packet_directories']:
        base = evidence/name
        manifest = load(base/'MANIFEST.json')
        for item in manifest['files']:
            assert digest(base/item['path']) == {key:item[key] for key in ('bytes','sha256')}, str(base/item['path'])
        checks.append({'packet':name,'manifest_sha256':digest(base/'MANIFEST.json')['sha256'],'listed_files_verified':len(manifest['files'])})
    return checks

def verify_bindings(evidence):
    checks = []
    for record in load(HERE/'SCOPED_INPUTS.json')['bindings']:
        got = digest(evidence/record['archived_workspace_path'])
        assert got == {key:record[key] for key in ('bytes','sha256')}, record
        checks.append({'binding_packet':record['binding_packet'], 'source_workspace_path':record['source_workspace_path'], 'archived_workspace_path':record['archived_workspace_path'], **got})
    assert digest(evidence/OLD_CONE)['sha256'] == OLD_HASH
    assert digest(evidence/CONE_RESULT)['sha256'] == CURRENT_HASH
    return checks

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true', help='Check all preservation hashes without running controls')
    parser.add_argument('--work-dir', type=Path, help='New nonexistent destination outside the evidence bundle')
    args=parser.parse_args()
    if not __debug__:
        parser.error('Run without -O: assertion-based evidence checks must remain enabled')
    if sys.version_info < (3,10):
        parser.error('Python 3.10 or later is required')
    if args.work_dir and args.work_dir.exists():
        parser.error('Refusing an existing --work-dir; select a new path')
    if args.work_dir and (args.work_dir.resolve() == HERE or args.work_dir.resolve().is_relative_to(HERE)):
        parser.error('--work-dir must be outside the immutable evidence bundle')
    manifest=verify_bundle()
    evidence=HERE/'workspace'
    before=tree_hashes(HERE)
    packets=packet_manifests(evidence)
    bindings=verify_bindings(evidence)
    if args.verify_only:
        print(json.dumps({'status':'PASS','preserved_files':len(manifest['files']), 'packet_manifests':len(packets),'direct_input_bindings':len(bindings)},indent=2))
        return
    if not args.work_dir:
        parser.error('--work-dir is required unless --verify-only is given')
    work=args.work_dir.resolve()
    work.mkdir(parents=True,exist_ok=False)
    current=work/'current-cone-5c74c708'
    historical=work/'historical-cone-e9f9a546'
    shutil.copytree(evidence,current)
    # Select the historical version while constructing a separate tree. Never
    # overwrite the current-cone tree or the preserved source payload.
    historical.mkdir()
    tensor_name='tensor-likelihood-closure-20261010'
    shutil.copytree(evidence/tensor_name,historical/tensor_name)
    for item in load(evidence/tensor_name/'INPUT_BINDINGS.json')['local_inputs']:
        rel=item['path']
        target=historical/rel
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(evidence/OLD_CONE if rel==CONE_RESULT else evidence/rel,target)
    assert digest(current/CONE_RESULT)['sha256']==CURRENT_HASH
    assert digest(historical/CONE_RESULT)['sha256']==OLD_HASH
    logs=work/'logs';logs.mkdir()
    records=[]
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONHASHSEED':'0','PYTHONOPTIMIZE':'0'}
    def run(label,tree,script,expected_exit=0,output=None,expected_output=None,arguments=()):
        started=time.monotonic()
        cp=subprocess.run([sys.executable,str(tree/script),*arguments],cwd=tree,env=env,capture_output=True,text=True)
        (logs/(label+'.stdout.txt')).write_text(cp.stdout)
        (logs/(label+'.stderr.txt')).write_text(cp.stderr)
        assert cp.returncode==expected_exit, (label,cp.returncode,cp.stderr)
        rec={'control':label,'script':script,'tree':tree.name,'exit_code':cp.returncode,'expected_exit_code':expected_exit,'seconds':round(time.monotonic()-started,3)}
        if output:
            expected=evidence/(expected_output or output)
            assert (tree/output).read_bytes()==expected.read_bytes(), (label,'Output changed',output)
            rec['output_byte_identical']=True
            rec['output']=output
            rec['output_sha256']=digest(tree/output)['sha256']
        records.append(rec)
        return cp
    run('fixed-channel-author',current,'repeatable-channel-constraints-20261010/verify.py',output='repeatable-channel-constraints-20261010/CHECK_RESULTS.json')
    run('fixed-channel-review',current,'fixed-channel-review-20261010/verify_review.py',output='fixed-channel-review-20261010/CHECK_RESULTS.json')
    assert (current/'fixed-channel-review-20261010/INPUT_HASHES.json').read_bytes()==(evidence/'fixed-channel-review-20261010/INPUT_HASHES.json').read_bytes()
    run('positive-cone-author',current,'positive-instrument-cone-transport-20261010/verify.py',output='positive-instrument-cone-transport-20261010/CHECK_RESULTS.json')
    run('positive-cone-reviewed-snapshot',current,'positive-instrument-review-20261010/author_snapshot/verify.py',output='positive-instrument-review-20261010/author_snapshot/CHECK_RESULTS.json')
    run('positive-cone-independent-review',current,'positive-instrument-review-20261010/independent_checks.py',output='positive-instrument-review-20261010/INDEPENDENT_CHECK_RESULTS.json')
    cp=run('tensor-current-path-expected-binding-failure',current,'tensor-likelihood-closure-20261010/verify.py',expected_exit=1)
    assert 'AssertionError: '+CONE_RESULT in cp.stderr
    run('tensor-historical-author',historical,'tensor-likelihood-closure-20261010/verify.py',output='tensor-likelihood-closure-20261010/CONTROL_RESULTS.json')
    run('tensor-review-portable-author-replay',current,'tensor-likelihood-review-20261010/replay_author.py',arguments=('--portable',),output='tensor-likelihood-review-20261010/author_replay/tensor-likelihood-closure-20261010/CONTROL_RESULTS.json')
    run('tensor-independent-review',current,'tensor-likelihood-review-20261010/independent_controls.py',output='tensor-likelihood-review-20261010/CONTROL_RESULTS.json')
    assert digest(current/CONE_RESULT)['sha256']==CURRENT_HASH
    assert digest(historical/CONE_RESULT)['sha256']==OLD_HASH
    assert before==tree_hashes(HERE), 'Preserved bundle changed during replay'
    receipt={'status':'PASS','checked_utc':datetime.now(timezone.utc).isoformat(),'bundle_manifest':digest(HERE/'MANIFEST.json'),'runtime':{'python':sys.version,'implementation':platform.python_implementation(),'platform':platform.platform(),'dependencies':'Python >=3.10 standard library only; no network, Git, Lean or third-party packages'},'isolated':True,'replay_uses_only_extracted_payload':True,'preserved_bundle_before_after_identical':True,'packet_manifests':packets,'direct_binding_checks':bindings,'historical_cone':{'workspace_path':CONE_RESULT,'tree':historical.name,'tree_scope':'Minimal tensor author packet and its nine direct inputs; not a reconstructed historical cone packet','sha256':OLD_HASH,'provenance':'Exact inverse-edit reconstruction matching the original tensor binding; not independently retained historical bytes'},'current_cone':{'workspace_path':CONE_RESULT,'tree':current.name,'sha256':CURRENT_HASH},'controls':records,'scope':'Ordinary preservation and finite exact replay; not a fresh universal proof, formal certificate, actual warrant, field-novelty or T20 closure.'}
    save(work/'REPLAY_RECEIPT.json',receipt)
    print(json.dumps({'status':'PASS','controls':len(records),'author_groups':[9,16,13],'independent_review_groups':[7,7,12],'current_path_drift_expected_and_verified':True,'preserved_bundle_unchanged':True,'receipt':str(work/'REPLAY_RECEIPT.json')},indent=2))

if __name__=='__main__':main()
