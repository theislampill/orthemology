#!/usr/bin/env python3
"""Fresh read-only-input replay of independent reviewer Lean controls."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, re, subprocess
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
LEAN = ROOT/'hase-positive-research/toolchain-preparation/toolchains/lean-4.19.0-linux/bin/lean'
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--output',default='fresh-check-v3')
args=parser.parse_args()
OUT = HERE/args.output
OUT.mkdir(exist_ok=False)
(OUT/'objects').mkdir()
(OUT/'inputs').mkdir()
dependencies=['ExplanatoryGeneration','ActualUseControls']
owned=['ActualProvisionReview','BeginninglessProvision','BeginninglessJointProvision','IntegratedActualUseReview']
modules=dependencies+owned
def source(name):
    return (HERE/'reviewed-snapshots-v2' if name in dependencies else HERE)/(name+'.lean')
env=dict(os.environ, LEAN_PATH=str(OUT/'objects'))
env.pop('LEAN_SRC_PATH',None)
record={'started_utc':datetime.now(timezone.utc).isoformat(),'scope':'Kernel checks of declared controls, not premise warrant, metaphysical possibility, or closure.','modules':[]}
def digest(path): return hashlib.sha256(path.read_bytes()).hexdigest()
for name in modules:
    src=source(name)
    (OUT/'inputs'/(name+'.lean')).write_bytes(src.read_bytes())
    cmd=[str(LEAN),'--trust=0','-o',str(OUT/'objects'/(name+'.olean')),str(OUT/'inputs'/(name+'.lean'))]
    run=subprocess.run(cmd,env=env,text=True,capture_output=True)
    (OUT/(name+'.log')).write_text(run.stdout+run.stderr)
    record['modules'].append({'name':name,'sha256':digest(src),'command':cmd,'exit_code':run.returncode})
    if run.returncode: raise SystemExit(run.stdout+run.stderr)
theorems=[]
for name in modules:
    ns=[]
    for line in source(name).read_text().splitlines():
        if m:=re.match(r'^namespace (\S+)',line): ns.append(m.group(1))
        elif re.match(r'^end(?:\s|$)',line): ns.pop()
        elif m:=re.match(r'^theorem ([A-Za-z0-9_.]+)',line): theorems.append('.'.join(ns+[m.group(1)]))
audit='\n'.join('import '+n for n in modules)+'\n\n'+'\n'.join('#print axioms '+t for t in theorems)+'\n'
(HERE/'Readback.lean').write_text(audit)
(OUT/'inputs/Readback.lean').write_text(audit)
run=subprocess.run([str(LEAN),'--trust=0',str(OUT/'inputs/Readback.lean')],env=env,text=True,capture_output=True)
(OUT/'readback.log').write_text(run.stdout+run.stderr)
if run.returncode: raise SystemExit(run.stdout+run.stderr)
if 'sorryAx' in run.stdout: raise SystemExit('Untrusted placeholder axiom found')
record.update({'finished_utc':datetime.now(timezone.utc).isoformat(),'lean_sha256':digest(LEAN),'version':subprocess.check_output([str(LEAN),'--version'],text=True).strip(),'theorem_count':len(theorems),'reviewer_theorem_count':sum(len(re.findall(r'^theorem ',source(n).read_text(),re.M)) for n in owned),'theorems':theorems,'axiom_readback_sha256':digest(OUT/'readback.log'),'axiom_readback':run.stdout,'status':'Fresh --trust=0 module and theorem readback success'})
(HERE/'VERIFICATION.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps({k:record[k] for k in ['version','theorem_count','status']},indent=2))
