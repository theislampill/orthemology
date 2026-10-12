from pathlib import Path
import subprocess, json, datetime
p=Path(__file__).resolve().parent
records=[]
def run(args,log,expected=0):
 start=datetime.datetime.now(datetime.timezone.utc).isoformat()
 with (p/log).open('w') as f:
  q=subprocess.run([str(p/'run-review.sh'),*args],cwd=p,stdout=f,stderr=subprocess.STDOUT)
 record={'started_at_utc':start,'finished_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'command':[str(p/'run-review.sh'),*args],'exit_code':q.returncode,'log':log}
 records.append(record); (p/'command_results.json').write_text(json.dumps(records,indent=2)+'\n')
 print(log, q.returncode,flush=True)
 if expected==0: assert q.returncode==0,record
 else:
  s=(p/log).read_text()
  assert q.returncode!=0 and 'unsolved goals' in s
  assert all(x not in s for x in ['unknown module','not found','maximum recursion','maximum number of heartbeats'])
run(['--version'],'toolchain.log')
for name in ['LocalFintypeProd','GuardedTree','Bound','Catalogue','Attainment','Candidates','Saturation','Stability','Executable','FiniteTable','Controls','Main']:
 run(['-o',str(p/(name+'.olean')),str(p/(name+'.lean'))],name+'.log')
run(['--run',str(p/'Main.lean')],'runtime.log')
for name in ['DropGuard','DropNullary','DropChildCosts']:
 run([str(p/'mutations'/(name+'.lean'))],'mutation-'+name+'.log',expected=1)
print('REVIEW REPLAY PASSED',flush=True)
