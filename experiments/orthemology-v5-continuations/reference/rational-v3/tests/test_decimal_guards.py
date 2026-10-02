#!/usr/bin/env python3
from pathlib import Path
import json,os,subprocess,sys
P=Path(__file__).resolve().parents[1]/'reference.py'
checks=0
cases=[['--summary','1'+'0'*1000,'0'],
 ['--word','0000000000000001','--epsilon','1/'+'1'+'0'*1000,'--mode','uniform_critical'],
 ['--summary','1'+'0'*1000,'9'*1000],
 ['--word','0','--epsilon',('1'+'0'*1000)+'/'+('4'+'0'*1000)]]
for guard in ['640','4300','0']:
 for args in cases:
  result=subprocess.run([sys.executable,'-B',str(P)]+args,text=True,capture_output=True,env=dict(os.environ,PYTHONINTMAXSTRDIGITS=guard))
  checks+=1;assert result.returncode==0,(guard,result.stderr)
  result=json.loads(result.stdout);checks+=1;assert result['family']=='dyadic_square'
print(json.dumps({'status':'PASS','exact_assertions':checks,'host_guards':[640,4300,0],'in_range_cli_cases':12,
 'scope':'Chunked input parsing and output formatting under supported host digit guards.'},indent=2))
