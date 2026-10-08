#!/usr/bin/env python3
"""Runtime sensitivity checks, using disposable local copies with proofs erased.

The accepted source is untouched. A mutant is never a theorem or an alternate
policy. Erasing theorem declarations is necessary to ask what the independent
runtime assertions detect, rather than stopping at an intentionally broken proof.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess

BASE=None  # Explicit source root is supplied to main; original input stays immutable.
MUTATIONS={
 'ignore_compiled_successor':('({ w with plant := e.successor }, true)','(w, true)','FAIL landing stores exact Lean successor'),
 'bypass_installed_rule':('if decide (p.rule = .exact) && CriterionInstallation.accepts p.rule c.payload p.source.content then','if true then','FAIL C1 token cannot impersonate installed exact rule'),
 'cached_commitments_only':('decide (e ∈ root.commitments ∧ Eligible p now root e requester)','decide (e ∈ root.commitments)','FAIL replay has no second history/version effect'),
 'omit_revocation_memory':('e.action.epoch ∉ root.revoked ∧ ','','FAIL effective revocation blocks stale prepared install'),
 'omit_cancellation_memory':('e ∉ root.cancelled ∧','','FAIL cancelled command cannot land late'),
 'restore_actor_world_clock_oracle':('match propose trialActor a path with', 'match propose { trialActor with observedTime := current.now } a path with', 'FAIL stale actor time still proposes without a current-time oracle'),
}

def erase_theorems(text):
    matches=list(re.finditer(r'(?m)^(?:theorem |def |structure |inductive |instance |end |namespace |import |open |#print )',text))
    chunks=[text[:matches[0].start()]]
    for index,match in enumerate(matches):
        block=text[match.start():matches[index+1].start() if index+1<len(matches) else len(text)]
        if not block.startswith(('theorem ','#print ')):
            chunks.append(block)
    return ''.join(chunks)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--clean-build',type=Path,required=True)
    ap.add_argument('--output-dir',type=Path,required=True)
    ap.add_argument('--source-root',type=Path,required=True)
    ap.add_argument('--lean',type=Path,required=True)
    args=ap.parse_args();BASE=args.source_root.resolve();out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=False)
    clean=args.clean_build.resolve();lean=args.lean.resolve();leanc=lean.with_name('leanc')
    original=(BASE/'Composition.lean').read_bytes()
    def run_mutant(item):
        name,(old,new,expected)=item
        build=out/name;build.mkdir()
        for src in clean.iterdir():
            if src.suffix in ('.lean','.olean','.c') or src.name=='source.bin': shutil.copyfile(src,build/src.name)
        source=erase_theorems(original.decode())
        if source.count(old)!=1: raise RuntimeError(f'mutation target not unique: {name}')
        mutated=source.replace(old,new)
        (build/'Composition.lean').write_text(mutated)
        env=dict(os.environ,LEAN_PATH=str(build))
        modules=['Composition','Fixtures','LocalTests','DynamicTests','BatchTests','RaceTests','Artifacts','ClockTests','TestRunner']
        compiles=[]
        for module in modules:
            cp=subprocess.run([str(lean),'-o',module+'.olean','-c',module+'.c',module+'.lean'],cwd=build,env=env,capture_output=True,timeout=120)
            compiles.append(cp.stdout+cp.stderr)
            if cp.returncode: raise RuntimeError(f'mutant {name} compile {module}: '+(cp.stdout+cp.stderr).decode())
        (build/'compile.log').write_bytes(b''.join(compiles))
        sources=['TypedCriterionGuard','CriterionInstallation','DynamicInterlock']+modules
        cp=subprocess.run([str(leanc),'-O1','-o','mutant-tests']+[s+'.c' for s in sources],cwd=build,env=env,capture_output=True,timeout=300)
        (build/'link.log').write_bytes(cp.stdout+cp.stderr)
        if cp.returncode: raise RuntimeError(f'mutant {name} link failed')
        cp=subprocess.run([str(build/'mutant-tests'),str(build/'source.bin')],cwd=build,env=env,capture_output=True,timeout=120)
        data=cp.stdout+cp.stderr;(build/'runtime.log').write_bytes(data)
        if cp.returncode!=1 or expected not in data.decode():
            raise RuntimeError(f'mutant {name} failed sensitivity: '+data.decode())
        return {'mutation':name,'status':'DETECTED','exit_code':cp.returncode,'expected_failure':expected,
                'mutant_source_sha256':hashlib.sha256(mutated.encode()).hexdigest(),
                'runtime_log_sha256':hashlib.sha256(data).hexdigest()}
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        records=list(pool.map(run_mutant,MUTATIONS.items()))
    if (BASE/'Composition.lean').read_bytes()!=original: raise RuntimeError('accepted source changed')
    (out/'MUTATION_RESULTS.json').write_text(json.dumps({'status':'PASS','accepted_source_sha256':hashlib.sha256(original).hexdigest(),'records':records},indent=2)+'\n')
    print(json.dumps(records,indent=2))

if __name__=='__main__':main()
