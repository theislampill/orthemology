#!/usr/bin/env python3
"""Later-executor driver, not evidence of a successful Lean run.
Requires a user-supplied native pinned Lean executable; downloads nothing.
Output is a NEW directory. Successful graph checks would not close VCT/TRC.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

TARGETS = ['P03Q1f.Chain.mapEdge','P03Q1f.walkRank','P03Q1f.Hom.mapWalk',
           'P03Q1f.noClosedWalk','P03Q1f.Hom.noCollapseOfWalk']

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--lean', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[1]
    out = args.out.expanduser().absolute()
    if out.exists():
        raise SystemExit('Refusing existing output directory; fresh build evidence is required')
    out.mkdir(parents=True, exist_ok=False)
    lean = args.lean.expanduser().resolve()
    env = os.environ.copy()
    env['LEAN_PATH'] = str(out)
    receipt = {'scope':'P03_NEW_GRAPH_ONLY', 'status':'STARTED',
       'started_utc':datetime.now(timezone.utc).isoformat(),
       'python':sys.version, 'platform':platform.platform(),
       'lean_executable':str(lean), 'LEAN_PATH':env['LEAN_PATH'],
       'targets':TARGETS, 'commands':[], 'canonical_mutation':False,
       'full_vct_credit':False, 'trc_credit':False, 'kernel_acceptance_credit':False,
       'compiler_origin_verification':'REQUIRED_INDEPENDENTLY; version text alone is insufficient'}
    def save() -> None:
        receipt['updated_utc'] = datetime.now(timezone.utc).isoformat()
        (out/'RUN_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    def run(label: str, argv: list[str]) -> subprocess.CompletedProcess:
        start = datetime.now(timezone.utc).isoformat()
        try:
            p = subprocess.run(argv,cwd=out,env=env,capture_output=True,timeout=120,check=False)
        except (OSError, subprocess.TimeoutExpired) as exc:
            (out/f'{label}.stderr').write_text(repr(exc)+'\n')
            receipt['commands'].append({'label':label,'argv':argv,'started_utc':start,
                 'launch_or_timeout_error':repr(exc)})
            save()
            raise
        (out/f'{label}.stdout').write_bytes(p.stdout)
        (out/f'{label}.stderr').write_bytes(p.stderr)
        receipt['commands'].append({'label':label,'argv':argv,'cwd':str(out),
          'started_utc':start,'ended_utc':datetime.now(timezone.utc).isoformat(),
          'exit_code':p.returncode, 'stdout_bytes':len(p.stdout),'stderr_bytes':len(p.stderr),
          'stdout_sha256':sha(p.stdout),'stderr_sha256':sha(p.stderr)})
        save()
        if p.returncode != 0:
            raise RuntimeError(f'{label}: nonzero exit {p.returncode}')
        return p
    try:
        if not lean.is_file() or not os.access(lean,os.X_OK):
            raise RuntimeError('A real executable was not supplied')
        receipt['lean_executable_sha256'] = sha(lean.read_bytes())
        v = run('version',[str(lean),'--version'])
        vt = (v.stdout+v.stderr).decode('utf-8','replace')
        if not re.search(r'\bversion 4\.19\.0\b',vt) or '6caaee842e94' not in vt:
            raise RuntimeError('Wrong Lean pin: require 4.19.0 / commit 6caaee842e94; no substitution')
        run('prefix',[str(lean),'--print-prefix'])
        expected = json.loads((root/'proposal/lean/EXPECTED_TARGETS.json').read_text())
        sources = {}
        for name, expected_sha in expected['source_sha256'].items():
            b = (root/'proposal/lean'/name).read_bytes()
            if sha(b) != expected_sha:
                raise RuntimeError(f'Source identity mismatch: {name}')
            (out/name).write_bytes(b)
            sources[name] = {'bytes':len(b),'sha256':sha(b)}
        receipt['sources'] = sources
        run('build-graph',[str(lean),'-o','P03GuardedGraph.olean','P03GuardedGraph.lean'])
        audit = run('build-audit',[str(lean),'-o','P03GuardedGraphAudit.olean','P03GuardedGraphAudit.lean'])
        text = (audit.stdout+audit.stderr).decode('utf-8','replace')
        # This proposal predicts no axioms. Unexpected dependencies require review,
        # not automatic broadening to the accepted main project's axiom allowance.
        for target in TARGETS:
            if f"'{target}' does not depend on any axioms" not in text:
                raise RuntimeError(f'Missing expected axiom readback: {target}')
        if re.search(r'\bsorryAx\b|declaration uses .?sorry|\berror:',text,re.I):
            raise RuntimeError('Forbidden proof/error marker in audit')
        artifacts = {}
        for name in ('P03GuardedGraph.olean','P03GuardedGraphAudit.olean'):
            b = (out/name).read_bytes()
            if not b:
                raise RuntimeError(f'Empty artifact: {name}')
            artifacts[name] = {'bytes':len(b),'sha256':sha(b)}
        receipt['artifacts'] = artifacts
        receipt['status'] = 'GRAPH_ONLY_BUILD_AND_READBACK_PASS_PENDING_TYPE_REVIEW'
        receipt['note'] = ('Inspect every #check/#print type against EXPECTED_TARGETS. '
             'This is graph transport only, not full guarded warrant/version transport or TRC.')
        save()
        return 0
    except Exception as exc:
        receipt['status'] = 'NOT_ACCEPTED'
        receipt['error'] = repr(exc)
        save()
        print(str(exc),file=sys.stderr)
        return 1

if __name__ == '__main__':
    raise SystemExit(main())
