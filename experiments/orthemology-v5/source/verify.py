#!/usr/bin/env python3
"""Exact-custody, reference and mandatory Lean build gate.

Exit 0: requested scope passed (reference-only never claims a kernel proof).
Exit 1: a required check failed. Exit 2: reference passed, no Lean toolchain.
Receipts must be written OUTSIDE the frozen source tree. No installation or
network side effects. Mocked policy output never substitutes for this build.
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
import build_gate as gate

ROOT=Path(__file__).resolve().parent

def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--reference-only',action='store_true')
    ap.add_argument('--output-dir',type=Path,default=ROOT.parent/(ROOT.name+'_verification'))
    args=ap.parse_args();dest=args.output_dir.resolve();report={
        'timestamp_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,
        'scope':'REFERENCE_ONLY' if args.reference_only else 'REFERENCE_AND_REQUIRED_FORMAL_TARGETS',
        'lean':{'kernel_verified':False,'status':'NOT_ATTEMPTED'},'novelty_established':False,
        'trust_boundary':'Real selected compiler/OS/filesystem trusted; pure policy fixtures are not kernel evidence.'}
    failed=False
    if dest==ROOT or ROOT in dest.parents:
        print(json.dumps({'overall':'FAIL','error':'output directory must be outside frozen source tree','exit_code':1}));return 1
    dest.mkdir(parents=True,exist_ok=True)
    try:
        report['manifest']=gate.verify_manifest(ROOT)
        pin=(ROOT/'lean-toolchain').read_text().strip()
        if pin!=gate.PIN:raise gate.GateError('unapproved toolchain change: '+pin)
        lock=gate.strict_json(ROOT/'TOOLCHAIN_LOCK.json')
        if lock.get('lean')!=pin or lock.get('compiler_version')!=gate.VERSION:raise gate.GateError('toolchain lock mismatch')
        report['toolchain_lock']=lock
        contract=gate.strict_json(ROOT/'formal_targets.json');actual={};hygiene=[]
        for path in sorted((ROOT/'lean').glob('*.lean')):
            src=path.read_text();clean=gate.strip_comments(src)
            forbidden=re.findall(r'\b(?:sorry|admit|axiom|native_decide|unsafe)\b',clean)
            if forbidden:raise gate.GateError('unfinished/unapproved active source '+path.name+': '+repr(forbidden))
            actual[path.stem]=gate.declared_theorems(src)
            hygiene.append({'module':path.stem,**gate.digest(path),'theorems_static':len(actual[path.stem]),'status':'STATIC_HYGIENE_NOT_KERNEL'})
        rows=gate.validate_inventory(contract,actual)
        report['source_hygiene']=hygiene
        report['required_inventory']={'modules':len(rows),'targets':sum(len(r['targets']) for r in rows),'status':'STATIC_COMPLETE_NOT_READBACK'}
    except (gate.GateError,OSError,ValueError) as e:
        report['preflight_error']=str(e)
        report.update(exit_code=1,overall='FAIL',reference_execution='NOT_RUN_UNVERIFIED_CUSTODY_OR_SPEC')
        (dest/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
        print(json.dumps(report,indent=2));return 1
    env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
    cmds=[('unit_tests',[sys.executable,'-B','-m','unittest','discover','-s','tests','-v']),
          ('unit_tests_optimised',[sys.executable,'-B','-O','-m','unittest','discover','-s','tests','-v']),
          ('census',[sys.executable,'-B','census.py']),
          ('census_optimised',[sys.executable,'-B','-O','census.py']),
          ('mutations',[sys.executable,'-B','check_mutations.py','--output-dir',str(dest/'mutations')]),
          ('v4_mutations',[sys.executable,'-B','v4_mutations.py','--output-dir',str(dest/'v4_mutations')]),
          ('positive_demonstration',[sys.executable,'-B','demonstrate.py'])]
    for name,cmd in cmds:
        rec=gate.run_bounded(cmd,ROOT,timeout=180,env=env);row=gate.write_run(dest,name,rec);report[name]=row
        failed |= not rec['ok']
        if name.startswith('unit_tests'):
            m=re.search(r'Ran (\d+) tests?',rec['stderr']);row['tests']=int(m[1]) if m else None
            if not m:failed=True;row['ok']=False;row['error']='missing test census'
        elif rec['ok']:
            try:row['results']=json.loads(rec['stdout'])
            except ValueError:failed=True;row.update(ok=False,error='missing machine-readable result')
    lean=shutil.which('lean')
    if args.reference_only:
        report['lean']={'kernel_verified':False,'status':'EXPLICITLY_NOT_ATTEMPTED','available':bool(lean)}
    elif lean is None:
        report['lean']={'kernel_verified':False,'status':'UNAVAILABLE','available':False,'required_targets':sum(len(r['targets']) for r in rows)}
    elif rows and not report.get('preflight_error'):
        try:
            report['lean']['executable']=str(Path(lean).resolve())
            report['lean']['executable_digest']=gate.digest(Path(lean).resolve())
            ver=gate.run_bounded([lean,'--version'],ROOT,timeout=15,env=env)
            report['lean']['version_process']=gate.write_run(dest,'LEAN_VERSION',ver)
            if not ver['ok']:raise gate.GateError('Lean identity process failed')
            gate.enforce_version(gate.VERSION,ver['stdout'])
            # A new empty directory prevents old .olean files satisfying a missing build.
            import tempfile
            build=Path(tempfile.mkdtemp(prefix='real-lean-build-',dir=dest))
            lenv={**env,'LEAN_PATH':str(build)}
            builds=[]
            for row in rows:
                name=row['name'];artifact=build/(name+'.olean')
                rec=gate.run_bounded([lean,'-o',str(artifact),name+'.lean'],ROOT/'lean',timeout=180,env=lenv)
                info=gate.write_run(dest,'LEAN_'+name,rec);builds.append(info)
                if not rec['ok']:raise gate.GateError('Lean compilation failed: '+name)
                info['artifact']=gate.check_artifact(artifact)
            report['lean']['builds']=builds
            targets=[x for r in rows for x in r['targets']]
            audit=gate.render_required_audit(rows)
            (build/'RequiredAudit.lean').write_text(audit)
            rec=gate.run_bounded([lean,'-o',str(build/'RequiredAudit.olean'),'RequiredAudit.lean'],build,timeout=180,env=lenv)
            report['lean']['audit_process']=gate.write_run(dest,'LEAN_REQUIRED_AUDIT',rec)
            if not rec['ok']:raise gate.GateError('required audit did not compile')
            gate.check_artifact(build/'RequiredAudit.olean')
            audits=gate.parse_audit(rec['stdout'],targets)
            report['lean'].update(status='ALL_REQUIRED_DECLARATIONS_KERNEL_CHECKED',kernel_verified=True,
                declarations=audits,actual_axioms=sorted({a for t in audits.values() for a in t['axioms']}))
        except (gate.GateError,OSError,ValueError) as e:
            failed=True;report['lean'].update(status='FAIL',kernel_verified=False,error=str(e))
    # Recheck source custody after executing every tool, not only before.
    try:report['post_run_manifest']=gate.verify_manifest(ROOT)
    except (gate.GateError,OSError) as e:failed=True;report['post_run_manifest']={'status':'FAIL','error':str(e)}
    if failed:code=1;overall='FAIL'
    elif args.reference_only:code=0;overall='REFERENCE_ONLY_PASS'
    elif report['lean']['kernel_verified']:code=0;overall='REFERENCE_AND_REQUIRED_FORMAL_TARGETS_PASS'
    else:code=2;overall='REFERENCE_PASS_KERNEL_UNAVAILABLE'
    report.update(exit_code=code,overall=overall)
    (dest/'VERIFICATION.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2));return code

if __name__=='__main__':raise SystemExit(main())
