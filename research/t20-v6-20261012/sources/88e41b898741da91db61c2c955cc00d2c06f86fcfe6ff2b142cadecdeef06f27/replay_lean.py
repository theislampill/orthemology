#!/usr/bin/env python3
"""Opt-in replay of the four new Lean files only, with an explicit existing Lean4.19 executable."""
from pathlib import Path
import argparse,hashlib,json,re,subprocess
R=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser();p.add_argument('--lean',required=True,help='Path to an existing Lean4.19.0 executable; no automatic installation');a=p.parse_args()
lean=str(Path(a.lean).expanduser().resolve());v=subprocess.run([lean,'--version'],capture_output=True,text=True,check=True,timeout=30)
assert re.search(r'\bversion 4\.19\.0[, )]',v.stdout),'Expected Lean4.19.0, got '+v.stdout
receipt=json.loads((R/'t20-next-frontier-20261008/root-later-operations/PLURAL_EXPLANATION_ROOT_REPLAY_20261009.json').read_text());checks=[]
for prior in receipt['checks']:
 f=R/prior['file'];h=hashlib.sha256(f.read_bytes()).hexdigest();assert h==prior['sha256']
 code=f.read_text();assert re.findall(r'^import\s+(.+)$',code,re.M)==['Std']
 assert not re.search(r'\b(sorry|admit|native_decide)\b',code)
 r=subprocess.run([lean,str(f)],cwd=R,capture_output=True,text=True,timeout=120)
 assert r.returncode==0 and 'sorryAx' not in r.stdout+r.stderr,(prior['file'],r.stdout,r.stderr)
 checks.append({'file':prior['file'],'sha256':h,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
print(json.dumps({'status':'PASS','toolchain':v.stdout.strip(),'check_count':len(checks),'import':'Std','new_dependencies':False,'scope':'Disposable extracted-file package qualification only; no new scientific theorem or warrant credit; historical proofs not rerun; regular-open realization written-only.','checks':checks},indent=2))
