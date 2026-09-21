#!/usr/bin/env python3
"""Real pinned build + mandatory audit. Missing tools never count as success.

This is a standalone driver, not a compiler fixture. It trusts the selected real
Lean/Lake executables and OS, and requires actual compilation and readback.
"""
from __future__ import annotations
import argparse
import json
import os
from pathlib import Path
import re
import shutil
import sys
from datetime import datetime, timezone
sys.dont_write_bytecode=True
if not (Path(__file__).resolve().parent / 'build_gate.py').is_file():
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'source'))
import build_gate as gate

ROOT=Path(__file__).resolve().parent
MATHLIB='c44e0c8ee63ca166450922a373c7409c5d26b00b'
EXTRA='OrthemologyConvergence.upstreamGirard'

def stage_build(source: Path, destination: Path) -> Path:
    """Copy only regular source into a fresh external build tree.

    Compilation may create .lake caches and rewrite Lake metadata; neither is
    allowed to mutate the frozen source packet. This is filesystem isolation,
    not a sandbox against a malicious compiler or build dependency.
    """
    source = source.resolve()
    destination = destination.resolve()
    if destination == source or source in destination.parents:
        raise gate.GateError('build tree must be outside source')
    if destination.exists():
        raise gate.GateError('build tree must be fresh')
    paths = list(source.rglob('*'))
    if any(path.is_symlink() for path in paths):
        raise gate.GateError('source symlink in build input')
    destination.mkdir(parents=True)
    for path in paths:
        target = destination / path.relative_to(source)
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, target)
        else:
            raise gate.GateError('nonregular build input')
    return destination


def main() -> int:
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args();out=args.output.resolve()
    if out==ROOT or ROOT in out.parents:
        raise SystemExit('Use an output directory outside the project.')
    out.mkdir(parents=True,exist_ok=True)
    receipt={'timestamp_utc':datetime.now(timezone.utc).isoformat(),
             'kernel_verified':False,'status':'NOT_STARTED','commands':[],
             'expected_lean':'4.19.0','expected_mathlib':MATHLIB}
    def finish(status:str,code:int) -> int:
        receipt.update(status=status,exit_code=code)
        (out/'FORMAL_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
        print(json.dumps(receipt,indent=2));return code
    work = ROOT
    def run(label:str,cmd:list[str],timeout:float=180) -> dict:
        rec=gate.run_bounded(cmd,work,timeout=timeout,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        receipt['commands'].append(gate.write_run(out,label,rec))
        return rec
    try:
        if (ROOT/'lean-toolchain').read_text().strip()!=gate.PIN:raise gate.GateError('toolchain file mismatch')
        lock=gate.strict_json(ROOT/'lake-manifest.json')
        packages=lock['packages']
        ml=[p for p in packages if p['name']=='mathlib']
        if len(ml)!=1 or ml[0]['rev']!=MATHLIB:raise gate.GateError('Mathlib lock mismatch')
        if any(not re.fullmatch('[0-9a-f]{40}',p['rev']) for p in packages):raise gate.GateError('unpinned transitive dependency')
        contract=gate.strict_json(ROOT/'formal_targets.json')
        actual={r['name']:gate.declared_theorems((ROOT/(r['name']+'.lean')).read_text()) for r in contract['modules']}
        rows=gate.validate_inventory(contract,actual)
        targets=[name for r in rows for name in r['targets']]
        if len(rows)!=12 or len(targets)!=145:raise gate.GateError('v4 inventory changed')
        audit='import CrossCheck\n'+gate.render_required_audit(rows)
        audit+=f'#eval IO.println "AUDIT_BEGIN {EXTRA}"\n#check {EXTRA}\n#ortho_audit {EXTRA}\n#print axioms {EXTRA}\n#eval IO.println "AUDIT_END {EXTRA}"\n'
        if (ROOT/'Verification.lean').read_text()!=audit:raise gate.GateError('audit source inventory mismatch')
        for path in ROOT.glob('*.lean'):
            text=gate.strip_comments(path.read_text())
            if re.search(r'\b(sorry|admit|axiom|native_decide|unsafe)\b',text):raise gate.GateError('forbidden source token: '+path.name)
        receipt['static_inventory']={'required_existing':len(targets),'additional_crosscheck':EXTRA,'source_modules':len(rows),
                                     'meaning':'Static source/configuration checks only; not elaboration.'}
        receipt['source_digests']={p.name:gate.digest(p) for p in ROOT.glob('*.lean')}
        lake=shutil.which('lake');lean=shutil.which('lean')
        receipt['tools']={'lake':lake,'lean':lean}
        if not lake or not lean:return finish('KERNEL_UNAVAILABLE',2)
        version=run('lean_version',[lean,'--version'],60)
        if not version['ok']:raise gate.GateError('compiler identity command failed')
        gate.enforce_version('4.19.0',version['stdout'])
        work = stage_build(ROOT, out/'build_tree')
        receipt['build_tree'] = str(work)
        built=run('lake_build',[lake,'build'],1800)
        if not built['ok']:raise gate.GateError('complete project build failed')
        head=run('mathlib_head',['git','-C',str(work/'.lake/packages/mathlib'),'rev-parse','HEAD'],30)
        if not head['ok'] or head['stdout'].strip()!=MATHLIB:raise gate.GateError('installed Mathlib identity mismatch')
        receipt['installed_dependencies'] = {}
        for dependency in packages:
            name = dependency['name']
            dephead = run('dependency_' + name,
                ['git', '-C', str(work/'.lake/packages'/name), 'rev-parse', 'HEAD'], 30)
            if not dephead['ok'] or dephead['stdout'].strip() != dependency['rev']:
                raise gate.GateError('installed dependency identity mismatch: ' + name)
            receipt['installed_dependencies'][name] = dephead['stdout'].strip()
        receipt['artifacts']={r['name']:gate.check_artifact(work/'.lake/build/lib/lean'/(r['name']+'.olean')) for r in rows}
        for module in ['CrossCheck','Verification']:
            receipt['artifacts'][module]=gate.check_artifact(work/'.lake/build/lib/lean'/(module+'.olean'))
        # Fresh real compiler invocation, even when Lake targets were cached.
        raw=run('mandatory_audit',[lake,'env','lean','-o',str(out/'Verification.olean'),'Verification.lean'],600)
        if not raw['ok']:raise gate.GateError('fresh audit compilation failed')
        receipt['audit_artifact']=gate.check_artifact(out/'Verification.olean')
        receipt['axiom_audit']=gate.parse_audit(raw['stdout']+'\n'+raw['stderr'],targets+[EXTRA])
        receipt['actual_axiom_union']=sorted({a for v in receipt['axiom_audit'].values() for a in v['axioms']})
        receipt['kernel_verified']=True
        return finish('KERNEL_AND_INVENTORY_PASS',0)
    except (gate.GateError,KeyError,ValueError,OSError) as exc:
        receipt['diagnostic']=str(exc)
        return finish('FORMAL_GATE_FAIL',1)

if __name__=='__main__':raise SystemExit(main())
