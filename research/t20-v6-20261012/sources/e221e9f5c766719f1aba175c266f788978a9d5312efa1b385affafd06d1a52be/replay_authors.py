#!/usr/bin/env python3
"""Replay byte-identical author code in isolated snapshots.
Only audit checker's fixture ROOT variable is rebound to the original workspace,
so source reads resolve; HERE and all writes remain in the snapshot directory.
"""
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

HERE=Path(__file__).resolve().parent
WORKSPACE=HERE.parent.parent
mode='optimized' if sys.flags.optimize else 'normal'
name='audit_symmetries'
path=HERE/'author_snapshots'/name/'check_exact.py'
spec=importlib.util.spec_from_file_location('frozen_audit_author',path)
mod=importlib.util.module_from_spec(spec)
sys.dont_write_bytecode=True
spec.loader.exec_module(mod)
mod.ROOT=WORKSPACE
sys.argv=[str(path),'--output','REPLAY_'+mode.upper()+'.json']
mod.main()
args=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(HERE/'author_snapshots/restricted_controls/verify.py')]
p=subprocess.run(args,capture_output=True,text=True)
if p.returncode:
    raise RuntimeError(p.stderr+p.stdout)
result=json.loads(p.stdout)
if result['status']!='PASS' or result['count']!=31:
    raise RuntimeError('unexpected restricted author result')
(HERE/'author_snapshots/restricted_controls'/('REPLAY_'+mode.upper()+'.json')).write_text(p.stdout)
print('RESTRICTED AUTHOR REPLAY:',result['status'],result['count'])
