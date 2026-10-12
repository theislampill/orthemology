#!/usr/bin/env python3
"""Check the frozen independent review and optional candidate bindings."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path

def ident(p):return p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--workspace',type=Path);a=ap.parse_args();r=Path(__file__).resolve().parent
 m=json.loads((r/'REVIEW_MANIFEST.json').read_text());bad=[]
 expected={e['path'] for e in m['payloads']}|{'REVIEW_MANIFEST.json'}
 actual={p.relative_to(r).as_posix() for p in r.rglob('*') if p.is_file()}
 if actual!=expected:bad.append('review membership')
 for e in m['payloads']:
  if ident(r/e['path'])!=(e['bytes'],e['sha256']):bad.append('review identity '+e['path'])
 b=json.loads((r/'SOURCE_BINDING.json').read_text());count=0
 if a.workspace:
  candidate=a.workspace/b['candidate_workspace_path']
  for e in b['candidate_files']:
   if ident(candidate/e['path'])!=(e['bytes'],e['sha256']):bad.append('candidate identity '+e['path'])
   count+=1
 rr=json.loads((r/'evidence/REPLAY_RESULT.json').read_text())
 if rr['status']!='PASS' or rr['fresh_custom_objects']!=21:bad.append('cold replay result')
 if rr['suites'][0]['readback']['target_count']!=272:bad.append('declaration count')
 if rr['input_manifest_sha256']!=b['manifest_sha256']:bad.append('input manifest mismatch')
 if ident(r/'evidence/PortableReadback.log')[1]!=rr['suites'][0]['readback']['log_sha256']:bad.append('readback log')
 controls=json.loads((r/'evidence/RESULT.json').read_text())
 if ident(r/'controls/IndependentIndexControls.lean')[1]!=controls['source_sha256']:bad.append('control source')
 if ident(r/'evidence/CONTROL.log')[1]!=controls['control_log_sha256']:bad.append('control log')
 if ident(r/'evidence/NEGATIVE.log')[1]!=controls['negative_log_sha256']:bad.append('negative log')
 proc=subprocess.run([sys.executable,str(r/'controls/check_recurrence.py')],text=True,capture_output=True)
 if proc.returncode or json.loads(proc.stdout)!=json.loads((r/'evidence/FINITE_CONTROLS.json').read_text()):bad.append('finite control replay')
 print(json.dumps({'status':'PASS_REVIEW_IDENTITY_AND_FINITE_REPLAY' if not bad else 'FAIL','review_payloads':len(m['payloads']),'candidate_files_checked':count,'failures':bad,'scope':'Recorded kernel evidence identity and fresh finite controls; full kernel replay instructions are in the report'},indent=2));raise SystemExit(bool(bad))
if __name__=='__main__':main()
