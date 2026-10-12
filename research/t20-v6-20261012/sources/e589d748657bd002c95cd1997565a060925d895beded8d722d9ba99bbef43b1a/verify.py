#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,sys
B=Path(__file__).resolve().parent
m=json.loads((B/'MANIFEST.json').read_text())
def check():
 for p,h in m['files'].items():
  assert hashlib.sha256((B/p).read_bytes()).hexdigest()==h,p
check()
subprocess.run([sys.executable,str(B/'checks/check_parity.py')],check=True)
check()
print('PASS: fresh parity author source hashes and exact finite controls')
