#!/usr/bin/env python3
"""Fresh extracted finite computational replay for the control and source/norm bundles."""
from pathlib import Path
import argparse,datetime,json,os,subprocess,sys,zipfile
from portable_core import sha,extract_zip,write_json,verify_manifest
from verify import verify

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--package-root',type=Path,default=Path(__file__).resolve().parents[1]);ap.add_argument('--out',type=Path,required=True)
 a=ap.parse_args();root=a.package_root.resolve();out=a.out.resolve()
 if out.exists() or out.is_relative_to(root):raise SystemExit('Output must be absent and outside the package')
 verification=verify(root);out.mkdir(parents=True)
 record={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_sha256':verification['manifest_sha256'],'commands':[],'scope':'Finite executable tests/probes; not kernel proofs of infinite-horizon claims, philosophical premises, or normative authority'}
 def save():write_json(out/'PYTHON_REPLAY_RESULT.json',record)
 def run(cwd,args,pythonpath=None):
  env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(pythonpath or cwd)}
  p=subprocess.run([sys.executable,'-B']+args,cwd=cwd,env=env,capture_output=True,text=True,timeout=900)
  label=str(len(record['commands']));(out/(label+'.stdout')).write_text(p.stdout);(out/(label+'.stderr')).write_text(p.stderr)
  record['commands'].append({'cwd':str(cwd.relative_to(out)),'args':args,'exit_code':p.returncode,'stdout_sha256':sha(out/(label+'.stdout')),'stderr_sha256':sha(out/(label+'.stderr'))});save()
  if p.returncode:raise ValueError('Python replay failed: '+str(cwd)+' '+repr(args))
 try:
  ctrl=extract_zip(root/'archives/Control_Restoration_Research_Return.zip',out/'control')/'Control_Restoration_Research_Return'
  run(ctrl,['verify_tranche.py'])
  # Independently verify every declared canonical source reference without requiring a .git checkout.
  source=json.loads((ctrl/'source_identity.json').read_text())
  with zipfile.ZipFile(root/'canonical/Orthemology_Canonical_Source_03e2604d.zip') as z:
   import hashlib
   for row in source['sources']:
    if hashlib.sha256(z.read(row['path'])).hexdigest()!=row['sha256']:raise ValueError('Control canonical source binding mismatch')
  record['control_source_bindings_verified']=len(source['sources']);save()
  norm=extract_zip(root/'archives/Source_Intentionality_Norm_Fixing_Research_Tranche.zip',out/'norm')/'Source_Intentionality_Norm_Fixing_Research_Tranche'
  for script in ['bridge_models.py','team_concavity_check.py']:run(norm,[script])
  nested=[('P15/P15_Completed_Research_Return.zip','p15',['research_probes.py']),('polytope-successor/Rational_Polytope_Disclosure_Research_Return.zip','polytope',['exact_reference_probes.py']),('accuracy-bridge/Accuracy_Norm_Fixing_and_Source_Research_Return.zip','accuracy',['exact_probes.py'])]
  for rel,label,scripts in nested:
   extracted=extract_zip(norm/rel,out/label);children=list(extracted.iterdir());work=children[0] if len(children)==1 and children[0].is_dir() else extracted
   run(work,['-m','unittest','discover','-v'])
   for script in scripts:
    if not (work/script).is_file():raise ValueError('Missing nested probe '+script)
    run(work,[script])
  verify_manifest(root,verification['manifest_sha256']);verify(root);record['status']='PASS';record['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
 except Exception as ex:record['status']='FAIL_CLOSED';record['error']=repr(ex);save();raise
 print(json.dumps({'status':record['status'],'receipt':str(out/'PYTHON_REPLAY_RESULT.json'),'sha256':sha(out/'PYTHON_REPLAY_RESULT.json')}))
if __name__=='__main__':main()
