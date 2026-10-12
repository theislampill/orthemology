#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,tempfile,shutil,subprocess,sys
B=Path(__file__).resolve().parent
m=json.loads((B/'MANIFEST.json').read_text())
def verify():
 for p,h in m['files'].items():assert hashlib.sha256((B/p).read_bytes()).hexdigest()==h,p
verify()
subprocess.run([sys.executable,str(B/'checks/interval_mass.py')],check=True)
with tempfile.TemporaryDirectory() as td:
 T=Path(td)/'author';shutil.copytree(B/'author-source',T)
 subprocess.run([sys.executable,str(T/'controls/check_endpoint_rates.py')],check=True)
 assert (T/'controls/RESULT.json').read_bytes()==(B/'author-source/controls/RESULT.json').read_bytes()
verify()
print('PASS: independent endpoint-density review payload and exact portable replays')
