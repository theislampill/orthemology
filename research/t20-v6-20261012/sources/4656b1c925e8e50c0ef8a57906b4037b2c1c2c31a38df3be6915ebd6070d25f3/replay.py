#!/usr/bin/env python3
"""Hash-check, fresh native compilation and evidence capture, never a policy oracle."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time

BASE = Path(__file__).resolve().parent
DEFAULT_LEAN = Path('private-locator:cb50f30cfa35bdf3a0cf')

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def verify_file(path, expected_sha256, expected_bytes):
    data = Path(path).read_bytes()
    if len(data) != expected_bytes or digest(data) != expected_sha256:
        raise ValueError(f'input hash or size mismatch: {path}')

def verify_output(text):
    lines = text.splitlines()
    expected = json.loads((BASE/'tests/EXPECTED_PASS_LINES.json').read_text())
    actual = [line for line in lines if line.startswith('PASS ')]
    if actual != expected or not lines or lines[-1] != 'TERMINAL PASS':
        raise ValueError('compiled output missing/reordered/failed required scenarios')
    if lines[0] != 'SOURCE_BYTES 3013' or any('FAIL' in line for line in lines):
        raise ValueError('compiled output reports wrong source or failure')
    return len(actual)

def verify_inputs():
    binding = json.loads((BASE/'INPUT_BINDING.json').read_text())
    for item in binding['files']:
        verify_file(BASE/item['path'], item['sha256'], item['bytes'])
    return binding

def verify_predecessors(root):
    result = []
    for directory, name, pinned in [
        ('delivery/dynamic-repair-checkpoint-v2','PACKET_MANIFEST.json','3d620e425f85b9f99681be5ba95ab48f11c4ff9ed706cf56696184e5a9593f67'),
        ('formal/criterion-transport','REVIEW_SNAPSHOT_V3.json','bd349c1c91950f2ed2f1616656a5a5334a22ccdeaad52d4810c9a1e1ccbbc75f')]:
        folder = Path(root)/directory
        data=(folder/name).read_bytes()
        if digest(data) != pinned:
            raise ValueError(f'predecessor manifest changed: {folder/name}')
        manifest=json.loads(data)
        for item in manifest['files']:
            verify_file(folder/item['path'], item['sha256'], item.get('bytes',item.get('size')))
        result.append({'path':str(folder), 'manifest_sha256':pinned, 'files':len(manifest['files'])})
    return result

def verify_artifacts(build):
    source = (build/'source.bin').read_bytes()
    before, installed, repaired = [json.loads((build/f'{name}.json').read_text()) for name in ('before','installed','repaired')]
    expected_target=['theislampill/orthemology','19de267cd41d2a5eeeb3eaf0b91562f706e2a916',
                     'docs/project-closure/ar8r-v11/programs/proper-function-and-candidate-e.md']
    if before['source']['target'] != expected_target:
        raise ValueError('compiled source target differs from pinned identity')
    expected_installed = dict(before, rule='exact', rule_version=4, rule_history=['normalizedLF'])
    expected_repaired = dict(expected_installed, draft=list(source), draft_revision=9,
                             draft_history=[[88],list(source)+[10]])
    if before['source']['content'] != list(source) or installed != expected_installed or repaired != expected_repaired:
        raise ValueError('compiled full-state artifacts violate expected frame/effect')
    if (build/'preserved-source.bin').read_bytes() != source or (build/'repaired-draft.bin').read_bytes() != source:
        raise ValueError('compiled source or repaired draft differs from exact input')
    return {name: digest((build/name).read_bytes()) for name in
            ('before.json','installed.json','repaired.json','preserved-source.bin','repaired-draft.bin')}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--lean',type=Path,default=DEFAULT_LEAN)
    parser.add_argument('--output-dir',type=Path,required=True)
    parser.add_argument('--predecessor-root',type=Path)
    args=parser.parse_args()
    out=args.output_dir.resolve()
    # Refuse silent overwrite of evidence. Fresh, self-contained build only.
    out.mkdir(parents=True,exist_ok=False)
    binding=verify_inputs()
    predecessors=verify_predecessors(args.predecessor_root) if args.predecessor_root else None
    build=out/'build';build.mkdir()
    imports=['TypedCriterionGuard','CriterionInstallation','DynamicInterlock']
    modules=['Composition','Fixtures','LocalTests','DynamicTests','BatchTests','RaceTests','Artifacts','ClockTests','TestRunner']
    for name in imports:
        shutil.copyfile(BASE/'imports'/f'{name}.lean',build/f'{name}.lean')
    for name in modules:
        src=BASE/f'{name}.lean' if name in ('Composition','TestRunner') else BASE/'tests'/f'{name}.lean'
        shutil.copyfile(src,build/f'{name}.lean')
    shutil.copyfile(BASE/'imports/proper-function-and-candidate-e.md',build/'source.bin')
    env=dict(os.environ, LEAN_PATH=str(build))
    commands=[]
    def run(argv,name,timeout=300):
        started=time.time()
        completed=subprocess.run(list(map(str,argv)),cwd=build,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=timeout)
        data=completed.stdout
        (out/f'{name}.log').write_bytes(data)
        commands.append({'argv':list(map(str,argv)),'returncode':completed.returncode,'seconds':round(time.time()-started,3),'log':f'{name}.log','sha256':digest(data)})
        if completed.returncode:
            raise RuntimeError(f'{name} failed with {completed.returncode}; see {out/name}.log')
        return data.decode()
    lean=args.lean.resolve();leanc=lean.with_name('leanc')
    version=run([lean,'--version'],'toolchain-version').strip()
    for name in imports+modules:
        log=run([lean,'-o',f'{name}.olean','-c',f'{name}.c',f'{name}.lean'],f'compile-{name}')
        if 'sorryAx' in log or 'declaration uses' in log or 'warning:' in log:
            raise RuntimeError(f'proof build emitted forbidden placeholder/warning in {name}')
    executable=build/'composed-tests'
    run([leanc,'-O1','-o',executable]+[f'{name}.c' for name in imports+modules],'native-link')
    text=run([executable,build/'source.bin'],'native-run')
    count=verify_output(text)
    artifacts=verify_artifacts(build)
    # unittest imports this exact wrapper; tests never decide an authorization.
    unitEnv=dict(env,PYTHONPATH=str(BASE))
    completed=subprocess.run([sys.executable,'-m','unittest','discover','-s',str(BASE/'tests'),'-p','test_*.py'],cwd=build,env=unitEnv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    (out/'wrapper-tests.log').write_bytes(completed.stdout)
    if completed.returncode: raise RuntimeError('wrapper tests failed')
    verify_inputs()
    if args.predecessor_root: verify_predecessors(args.predecessor_root)
    source=(build/'source.bin').read_bytes()
    receipt={'status':'PASS','toolchain':version,'lean_sha256':digest(lean.read_bytes()),
      'executable_sha256':digest(executable.read_bytes()),'source_bytes':len(source),'source_sha256':digest(source),
      'input_binding_sha256':digest((BASE/'INPUT_BINDING.json').read_bytes()),'pass_assertions':count,
      'finite_cases':{'revocation':80,'cancellation':60,'open_withheld':20,'two_batch_taint_sets':5,'macro_attempts':40},
      'wrapper_tests':7,'wrapper_sha256':digest(Path(__file__).read_bytes()),
      'build_source_hashes':{f'{name}.lean':digest((build/f'{name}.lean').read_bytes()) for name in imports+modules},'output_artifact_hashes':artifacts,'commands':commands,'predecessor_verification':predecessors,
      'claim':'Native compiled Lean source decisions drive actual modeled successor admission; conditional mathematical model only.'}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({k:receipt[k] for k in ['status','toolchain','pass_assertions','source_sha256','finite_cases']},indent=2))

if __name__=='__main__':
    main()
