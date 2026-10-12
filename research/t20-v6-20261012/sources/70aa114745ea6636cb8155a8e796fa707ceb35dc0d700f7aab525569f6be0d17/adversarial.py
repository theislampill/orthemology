#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,subprocess,sys,tempfile,shutil,datetime
D=Path(__file__).resolve().parent;P=D.parents[1]/'t20-consolidation-20261011/projection/package-v4';rows=[]
def run_case(name,edit,args):
 with tempfile.TemporaryDirectory(prefix='t20-v4-negative-') as temp:
  q=Path(temp)/'package';shutil.copytree(P,q);edit(q)
  r=subprocess.run([sys.executable,'-B','replay_selected.py',*args],cwd=q,capture_output=True,text=True,timeout=40)
  rows.append({'case':name,'exit_code':r.returncode,'rejected':r.returncode!=0,'stdout':r.stdout,'stderr':r.stderr})
run_case('altered checker rejected before execution',lambda q:(q/'replay/depth-decision-representation/check_exact.py').write_text("print('UNTRUSTED_CHECKER_RAN')\n"),['--suite','depth-decision-representation'])
run_case('missing fixture rejected before execution',lambda q:next((q/'replay/depth-joint-correction/inputs').iterdir()).unlink(),['--suite','depth-joint-correction'])
def link(q):
 f=q/'replay/depth-decision-representation/check_exact.py';f.unlink();f.symlink_to('/dev/null')
run_case('checker symlink rejected',link,['--suite','depth-decision-representation'])
run_case('extra unmanifested file rejected',lambda q:(q/'UNEXPECTED').write_text('x'),['--suite','depth-decision-representation'])
run_case('unknown suite rejected',lambda q:None,['--suite','../../outside'])
# Derived fixture tampering can be resealed mechanically, but the exact fixture registry still detects it.
def resealed(q):
 f=next((q/'replay/depth-joint-correction/inputs').iterdir());f.write_bytes(f.read_bytes()+b'\nchanged\n')
 m=json.loads((q/'PACKAGE_CONTENTS.json').read_text())
 for row in m['files']:
  if row['path']==f.relative_to(q).as_posix():row.update(sha256=hashlib.sha256(f.read_bytes()).hexdigest(),bytes=f.stat().st_size)
 (q/'PACKAGE_CONTENTS.json').write_text(json.dumps(m))
run_case('resealed fixture change rejected by source binding',resealed,['--suite','depth-joint-correction'])
ok=all(r['rejected'] for r in rows) and 'UNTRUSTED_CHECKER_RAN' not in rows[0]['stdout']
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS' if ok else 'FAIL','manifest_sha256':hashlib.sha256((P/'PACKAGE_CONTENTS.json').read_bytes()).hexdigest(),'cases':rows}
(D/'ADVERSARIAL.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k!='cases'},indent=2));sys.exit(not ok)
