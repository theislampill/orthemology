#!/usr/bin/env python3
"""Adversarial preservation-wrapper controls; no mathematical programs should execute."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
if not __debug__:raise SystemExit('Do not disable Python assertions for the guard test driver.')
R=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--external-root',type=Path,required=True);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args()
O=a.output_dir.resolve();assert not O.exists() and O!=R and R not in O.parents;O.mkdir(parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
external=a.external_root.resolve();rows=json.loads((R/'EXTERNAL_PREREQUISITES.json').read_text())['sources'];results=[]
originals={str(external/r['path']):sha(external/r['path']) for r in rows}
def run(name,args,code=None,status=None,needle=None,no_receipt=False):
 out=O/(name+'-output');p=subprocess.run(args,cwd=O,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (O/(name+'.log')).write_text(p.stdout)
 assert p.returncode!=0 and (code is None or p.returncode==code),(name,p.returncode,p.stdout)
 rec=out/'REPLAY_RECEIPT.json'
 if no_receipt:assert not rec.exists(),name
 else:
  j=json.loads(rec.read_text());assert j['script_runs']==[],(name,j)
  if status:assert j['status']==status,(name,j)
 if needle:assert needle in p.stdout,(name,p.stdout)
 results.append({'name':name,'exit_code':p.returncode,'expected_rejection':True,'no_control_program_executed':True,'log':name+'.log','log_sha256':sha(O/(name+'.log')),'receipt':str(rec.relative_to(O)) if rec.exists() else None})
base=[sys.executable,'-B',str(R/'replay.py')]
run('missing-external',base+['--output-dir',str(O/'missing-external-output')],2,'BLOCKED_MISSING_EXTERNAL_PREREQUISITES')
missing=O/'partial-external';missing.mkdir()
for row in rows[1:]:p=missing/row['path'];p.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(external/row['path'],p)
run('missing-one-external',base+['--external-root',str(missing),'--output-dir',str(O/'missing-one-external-output')],2,'BLOCKED_MISSING_EXTERNAL_PREREQUISITES')
corrupt=O/'corrupt-external';shutil.copytree(missing,corrupt)
p=corrupt/rows[0]['path'];p.parent.mkdir(parents=True,exist_ok=True);data=(external/rows[0]['path']).read_bytes();p.write_bytes(bytes([data[0]^1])+data[1:])
run('corrupt-external',base+['--external-root',str(corrupt),'--output-dir',str(O/'corrupt-external-output')],status='FAIL',needle='SHA-256 mismatch')
tampered=O/'tampered-packet';shutil.copytree(R,tampered);p=tampered/'evidence/cumulative-square-positivity-20261010/RESULT.md';p.write_bytes(p.read_bytes()+b'\nTAMPER\n')
run('tampered-packet',[sys.executable,'-B',str(tampered/'replay.py'),'--external-root',str(external),'--output-dir',str(O/'tampered-packet-output')],status='FAIL',needle='Size mismatch')
run('missing-runtime',[sys.executable,'-S','-B',str(R/'replay.py'),'--external-root',str(external),'--output-dir',str(O/'missing-runtime-output')],2,'BLOCKED_MISSING_RUNTIME_PREREQUISITES')
run('optimized-assertions',[sys.executable,'-O','-B',str(R/'replay.py'),'--external-root',str(external),'--output-dir',str(O/'optimized-assertions-output')],needle='Do not disable Python assertions',no_receipt=True)
stale=O/'reused-output-output';stale.mkdir();(stale/'sentinel').write_text('keep\n')
run('reused-output',base+['--external-root',str(external),'--output-dir',str(stale)],needle='Refusing to reuse',no_receipt=True);assert (stale/'sentinel').read_text()=='keep\n'
# Use a disposable packet copy to test refusal before any inside-packet directory is created.
inside=O/'inside-packet';shutil.copytree(R,inside)
run('inside-packet-output',[sys.executable,'-B',str(inside/'replay.py'),'--external-root',str(external),'--output-dir',str(inside/'forbidden-output')],needle='Output must be outside',no_receipt=True);assert not (inside/'forbidden-output').exists()
run('optimized-guard-driver',[sys.executable,'-O','-B',str(R/'test_guards.py'),'--external-root',str(external),'--output-dir',str(O/'optimized-guard-driver-output')],needle='Do not disable Python assertions for the guard test driver',no_receipt=True)
for path,h in originals.items():assert sha(Path(path))==h
result={'status':'PASS','guard_tests':results,'count':len(results),'external_inputs_unchanged':True,'scope':'Wrapper fail-closed tests only, not mathematical negative controls or research credit.'}
(O/'GUARD_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','guards':len(results)},indent=2))
