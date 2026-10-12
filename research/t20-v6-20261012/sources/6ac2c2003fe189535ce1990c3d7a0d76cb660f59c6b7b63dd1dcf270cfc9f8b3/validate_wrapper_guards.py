#!/usr/bin/env python3
"""Bounded identity/output guard controls. Does not run Lean proof checks."""
from pathlib import Path
import argparse, hashlib, importlib.util, json, shutil, subprocess, sys
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser()
    for name in ['packet','lean-bin','mathlib','mathlib-archive','scratch']:
        p.add_argument('--'+name,type=Path,required=True)
    a=p.parse_args();scratch=a.scratch.resolve()
    if scratch.exists():raise ValueError('Guard-control scratch must be absent')
    for root in [a.packet.resolve(),a.mathlib.resolve(),a.lean_bin.resolve().parent,HERE]:
        if scratch.is_relative_to(root):raise ValueError('Scratch must be outside immutable inputs')
    scratch.mkdir();rows=[]
    base=[sys.executable,str(HERE/'replay_with_archive.py'),'--packet',str(a.packet.resolve()),
      '--lean-bin',str(a.lean_bin.resolve()),'--mathlib',str(a.mathlib.resolve()),
      '--mathlib-archive',str(a.mathlib_archive.resolve()),'--out',str(scratch/'unused-output'),
      '--verify-dependencies-only']
    def run(name,command,expected_fragment,success=False):
        r=subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=60)
        if (r.returncode==0)!=success or expected_fragment not in r.stdout:raise RuntimeError(name+': '+r.stdout)
        (scratch/(name+'.log')).write_text(r.stdout)
        rows.append({'id':name,'exit_code':r.returncode,'status':'PASS_EXPECTED_BEHAVIOR',
                     'log_sha256':digest(scratch/(name+'.log'))})
    run('normal-archive-preflight',base,'PASS_PACKET_AND_DEPENDENCY_IDENTITIES',True)
    run('optimized-python-refused',[base[0],'-O',*base[1:]],'Optimized Python is refused')
    sentinel=scratch/'preexisting';sentinel.mkdir();receipt=sentinel/'RESULT.json'
    receipt.write_bytes(b'{"sentinel":"preserve exact existing evidence"}\n')
    before=digest(receipt);cmd=base.copy();cmd[cmd.index('--out')+1]=str(sentinel)
    run('existing-output-preserved',cmd,'Output must be absent')
    if digest(receipt)!=before:raise RuntimeError('Preexisting evidence was modified')
    rows[-1]['sentinel_sha256_before']=before;rows[-1]['sentinel_sha256_after']=digest(receipt)
    for name,protected in [('mathlib-output',a.mathlib.resolve()),('lean-output',a.lean_bin.resolve().parent)]:
        target=protected/'sixth-wrapper-must-not-create-output'
        if target.exists():raise RuntimeError('Unexpected guard target already exists')
        cmd=base.copy();cmd[cmd.index('--out')+1]=str(target)
        run(name,cmd,'Output cannot be inside')
        if target.exists():raise RuntimeError('Read-only dependency root was written')
    bad_archive=scratch/'wrong-archive.tar.gz';bad_archive.write_bytes(b'not the pinned source archive\n')
    cmd=base.copy();cmd[cmd.index('--mathlib-archive')+1]=str(bad_archive)
    run('wrong-archive-digest',cmd,'Mathlib archive digest mismatch')
    # Independently materialized source fixture; never mutate real dependencies.
    fixture=scratch/'source-copy'
    shutil.copytree(a.mathlib.resolve(),fixture,ignore=lambda directory,names: ['.lake','.git'] if Path(directory)==a.mathlib.resolve() else [])
    target=fixture/'Mathlib/Data/Real/Basic.lean';target.write_bytes(target.read_bytes()+b'\n-- source-integrity negative control\n')
    cmd=base.copy();cmd[cmd.index('--mathlib')+1]=str(fixture)
    run('changed-source-byte',cmd,'Extracted source mismatch: Mathlib/Data/Real/Basic.lean')
    # Pin guard is exercised read-only against a genuine dependency repository.
    spec=importlib.util.spec_from_file_location('identity',HERE/'verify_dependency_identity.py')
    helper=importlib.util.module_from_spec(spec);spec.loader.exec_module(helper)
    try:helper.verify_git(a.mathlib.resolve()/'.lake/packages/batteries','0'*40,'batteries')
    except ValueError as e:
        if 'Wrong Git revision' not in str(e):raise
        rows.append({'id':'wrong-dependency-revision','status':'PASS_EXPECTED_REJECTION'})
    else:raise RuntimeError('Wrong revision was accepted')
    result={'status':'PASS_GUARD_CONTROLS','proof_replays':0,'read_only_dependencies':True,
            'original_archive_modified':False,'tests':rows}
    (scratch/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
if __name__=='__main__':main()
