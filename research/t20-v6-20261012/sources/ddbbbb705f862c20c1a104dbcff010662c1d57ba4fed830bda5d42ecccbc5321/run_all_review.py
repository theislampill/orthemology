#!/usr/bin/env python3
"""Run the exact-hash independent review on an admitted candidate copy."""
import argparse,hashlib,json,subprocess,sys,time
from datetime import datetime,timezone
from pathlib import Path
HERE=Path(__file__).resolve().parent

def hashes(base):return {str(p.relative_to(base)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(base.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and 'logs' not in p.parts}

def main():
 p=argparse.ArgumentParser();p.add_argument('--candidate',type=Path,default=HERE/'inputs/release-candidate-v1/checker');args=p.parse_args();candidate=args.candidate.resolve()
 before=hashes(candidate);start=datetime.now(timezone.utc).isoformat();records=[]
 commands=[
 ('independent-reference-selftest',[sys.executable,str(HERE/'independent_models.py')],HERE),
 ('candidate-unit-normal',[sys.executable,'-m','unittest','discover','-s','tests','-v'],candidate),
 ('candidate-unit-optimized',[sys.executable,'-O','-m','unittest','discover','-s','tests','-v'],candidate),
 ('independent-normal',[sys.executable,str(HERE/'run_independent_review.py'),'--candidate',str(candidate),'--output',str(HERE/'INDEPENDENT_RESULTS.json')],HERE),
 ('independent-optimized',[sys.executable,'-O',str(HERE/'run_independent_review.py'),'--candidate',str(candidate),'--output',str(HERE/'INDEPENDENT_RESULTS_OPTIMIZED.json')],HERE),
 ('source-fixture-normal',[sys.executable,str(HERE/'run_source_fixture_review.py'),'--candidate',str(candidate),'--output',str(HERE/'INDEPENDENT_SOURCE_FIXTURE.json')],HERE),
 ('source-fixture-optimized',[sys.executable,'-O',str(HERE/'run_source_fixture_review.py'),'--candidate',str(candidate),'--output',str(HERE/'INDEPENDENT_SOURCE_FIXTURE_OPTIMIZED.json')],HERE),
 ('independent-mutations',[sys.executable,str(HERE/'run_independent_mutations.py'),'--candidate',str(candidate),'--directory',str(HERE/'mutation-copies-final')],HERE),
 ]
 for name,cmd,cwd in commands:
  now=time.time();proc=subprocess.run(cmd,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True);log=HERE/(name+'.log');log.write_text(proc.stdout)
  records.append({'name':name,'command':cmd,'cwd':str(cwd),'exit':proc.returncode,'seconds':round(time.time()-now,4),'log':log.name,'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()})
  print(name,proc.returncode,flush=True)
 after=hashes(candidate)
 result={'status':'PASS' if all(r['exit']==0 for r in records) and before==after else 'FAIL','started_utc':start,'completed_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'candidate_path':str(candidate),'candidate_file_hashes':before,'candidate_unchanged_during_review':before==after,'commands':records}
 (HERE/'FINAL_EXECUTION_RECORD.json').write_text(json.dumps(result,indent=2)+'\n')
 if result['status']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
