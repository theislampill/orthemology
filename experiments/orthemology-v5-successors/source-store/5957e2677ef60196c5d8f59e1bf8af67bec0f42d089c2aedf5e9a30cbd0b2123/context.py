"""Explicit path context for the unchanged historical evidence contracts."""
from pathlib import Path
import argparse, json, os, sys

ROOT = Path(__file__).resolve().parents[1]

def context():
    if sys.flags.optimize:
        raise ValueError('Run without -O or -OO: verification assertions are required')
    parser = argparse.ArgumentParser()
    parser.add_argument('--work', type=Path, required=True)
    args = parser.parse_args()
    A = args.work.resolve()
    cfg = json.loads((A/'config.json').read_text())
    T = Path(cfg['toolchain'])
    return A, A/'dependencies', ROOT/'inputs', T, A/'evidence'

def isolated_environment(A):
    blocked = {'PYTHONPATH','PYTHONHOME','PYTHONOPTIMIZE','PYTHONUSERBASE',
               'LD_PRELOAD','LD_LIBRARY_PATH','LAKE_HOME','ELAN_TOOLCHAIN'}
    env = {k:v for k,v in os.environ.items() if not k.startswith('LEAN_') and k not in blocked}
    env.update(json.loads((A/'environment.json').read_text()))
    return env
