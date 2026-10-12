#!/usr/bin/env python3
"""Fail-closed wrapper tests. No mathematical program should execute in any case."""
from pathlib import Path
import argparse,hashlib,json,shutil,subprocess,sys
if not __debug__:raise SystemExit('Do not disable Python assertions for the guard driver.')
R=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--lean-home',type=Path,required=True);ap.add_argument('--packages-dir',type=Path,required=True);ap.add_argument('--output-dir',type=Path,required=True);a=ap.parse_args()
O=a.output_dir.resolve();assert not O.exists() and O!=R and R not in O.parents;O.mkdir(parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
base=[sys.executable,'-B',str(R/'replay.py')];args=['--lean-home',str(a.lean_home.resolve()),'--packages-dir',str(a.packages_dir.resolve())];results=[]
def run(name,cmd,code=None,status=None,needle=None,no_receipt=False,output=None):
 out=output or O/(name+'-output');p=subprocess.run(cmd+['--output-dir',str(out)],cwd=O,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=O/(name+'.log');log.write_text(p.stdout)
 assert p.returncode!=0 and (code is None or p.returncode==code),(name,p.returncode,p.stdout)
 rec=out/'REPLAY_RECEIPT.json'
 if no_receipt:assert not rec.exists(),name
 else:
  data=json.loads(rec.read_text());assert data['runs']==[],(name,data)
  if status:assert data['status']==status,(name,data)
 if needle:assert needle in p.stdout,(name,p.stdout)
 results.append({'name':name,'exit_status':p.returncode,'expected_rejection':True,'no_mathematical_program_executed':True,'log':log.name,'log_sha256':sha(log)})
run('missing-prerequisite-arguments',base,2,'BLOCKED_MISSING_EXTERNAL_PREREQUISITES')
missing=O/'empty-packages';missing.mkdir()
run('missing-external-files',base+['--lean-home',str(a.lean_home.resolve()),'--packages-dir',str(missing)],2,'BLOCKED_MISSING_EXTERNAL_PREREQUISITES')
# Corruption is confined to a packet clone. No retained dependency file is changed.
tampered=O/'tampered-packet';shutil.copytree(R,tampered)
p=tampered/'evidence/full-functional-lean-20261010/Countermodel.lean';p.write_bytes(p.read_bytes()+b'\nTAMPER\n')
run('tampered-packet',[sys.executable,'-B',str(tampered/'replay.py')]+args,status='FAIL',needle='Size mismatch')
# A recorded external hash changed in a disposable packet remains syntactically
# valid, but must reject the untouched actual external bytes before Lean executes.
wrong=O/'wrong-external-hash';shutil.copytree(R,wrong)
p=wrong/'prerequisites/EXTERNAL_DEPENDENCIES.json';j=json.loads(p.read_text());j['entries'][0]['source']['sha256']='0'*64;p.write_text(json.dumps(j,indent=2)+'\n')
m=wrong/'MANIFEST.json';j=json.loads(m.read_text())
for row in j['files']:
 if row['path']=='prerequisites/EXTERNAL_DEPENDENCIES.json':row.update(bytes=p.stat().st_size,sha256=sha(p))
m.write_text(json.dumps(j,indent=2)+'\n')
run('wrong-external-hash',[sys.executable,'-B',str(wrong/'replay.py')]+args,status='FAIL',needle='SHA-256 mismatch')
# Reproduce the original metadata failure class: a path-specific receipt binding
# is altered while the outer packet manifest is refreshed. It must fail before
# any compiler or exact checker runs, even though packet checksums are valid.
bad=O/'wrong-scalar-binding';shutil.copytree(R,bad)
p=bad/'HISTORICAL_OBJECT_NOTE.json';j=json.loads(p.read_text());j['bindings'][0]['expected_sha256']='0'*64;p.write_text(json.dumps(j,indent=2)+'\n')
m=bad/'MANIFEST.json';j=json.loads(m.read_text())
for row in j['files']:
 if row['path']=='HISTORICAL_OBJECT_NOTE.json':row.update(bytes=p.stat().st_size,sha256=sha(p))
m.write_text(json.dumps(j,indent=2)+'\n')
run('wrong-scalar-receipt-binding',[sys.executable,'-B',str(bad/'replay.py')]+args,status='FAIL',needle='Scalar object/receipt binding differs')
run('optimized-assertions',[sys.executable,'-O','-B',str(R/'replay.py')]+args,needle='Do not disable Python assertions',no_receipt=True)
stale=O/'reused-output';stale.mkdir();(stale/'sentinel').write_text('keep\n')
run('reused-output',base+args,needle='Refusing to reuse',no_receipt=True,output=stale);assert (stale/'sentinel').read_text()=='keep\n'
inside=O/'inside-packet';shutil.copytree(R,inside)
run('inside-packet-output',[sys.executable,'-B',str(inside/'replay.py')]+args,needle='Output must be outside',no_receipt=True,output=inside/'forbidden-output');assert not (inside/'forbidden-output').exists()
# This rejection is checked before any directory is created in the actual toolchain.
forbidden=a.lean_home.resolve()/'preservation-forbidden-output'
assert not forbidden.exists()
run('inside-external-output',base+args,needle='Output must be separate',no_receipt=True,output=forbidden);assert not forbidden.exists()
run('optimized-guard-driver',[sys.executable,'-O','-B',str(R/'test_guards.py')]+args,needle='Do not disable Python assertions for the guard driver',no_receipt=True)
result={'status':'PASS_FAIL_CLOSED_GUARDS','count':len(results),'guards':results,'scope':'Wrapper reliability controls only. No universal theorem, independent research, or research-time credit.'}
(O/'GUARD_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'count':len(results)},indent=2))
