#!/usr/bin/env python3
"""Run only two inspected portable controls in disposable per-script directories."""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile
R=Path(__file__).resolve().parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
plan=json.loads((R/'PACKING/CONTROL_PLAN.json').read_text());out=[]
for row in plan['commands']:
 script=R/row['script'];assert sha(script)==row['script_sha256']
 expected=(R/row['expected_stdout']).read_bytes()
 with tempfile.TemporaryDirectory(prefix='t20-thirteenth-control-') as t:
  p=Path(t)/script.name;p.write_bytes(script.read_bytes())
  proc=subprocess.run([sys.executable,'-I','-B',str(p)],cwd=t,capture_output=True,timeout=180)
  assert proc.returncode==0,(row['id'],proc.stderr.decode())
  assert proc.stdout==expected,(row['id'],'stdout bytes differ')
  d=json.loads(proc.stdout);assert d['status']=='PASS'
  assert d.get('total_assertions',d.get('assertions'))==row['assertions']
  if 'generated_output' in row:assert (Path(t)/row['generated_output']).read_bytes()==expected
  assert sha(script)==row['script_sha256']
  out.append({'id':row['id'],'status':'PASS','script_sha256':row['script_sha256'],'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),'stdout_bytes':len(proc.stdout),'exact_saved_output_match':True,'assertions':row['assertions'],'external_source_read':False,'prior_code_executed':False})
print(json.dumps({'status':'PASS','python':sys.version,'runs':out,'scope':'Fresh finite executable controls only, not general proof, source-reading, metaphysical warrant or closure.'},indent=2))
