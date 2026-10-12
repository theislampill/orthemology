#!/usr/bin/env python3
from pathlib import Path
import json,hashlib,subprocess,sys,tempfile,shutil,concurrent.futures,datetime
D=Path(__file__).resolve().parent;P=D.parents[1]/'t20-consolidation-20261011/projection/package-v4'
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
snapshot={x.relative_to(P).as_posix():{'sha256':h(x),'bytes':x.stat().st_size} for x in P.rglob('*') if x.is_file()}
(D/'EXECUTED_CANDIDATE_FILES.json').write_text(json.dumps(snapshot,indent=2)+'\n')
with tempfile.TemporaryDirectory(prefix='independent-t20-v4-') as temp:
 q=Path(temp)/'package';shutil.copytree(P,q)
 def run(name,argv):
  r=subprocess.run([sys.executable,'-B',*argv],cwd=q,capture_output=True,text=True,timeout=600)
  (D/(name+'.stdout')).write_text(r.stdout);(D/(name+'.stderr')).write_text(r.stderr)
  print(name,r.returncode,flush=True)
  return {'name':name,'argv':argv,'exit_code':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr.encode()).hexdigest()}
 rows=[run('validator',['validate_package.py']),run('tool-tests',['-m','unittest','discover','-s','tool-tests','-v'])]
 names=json.loads((q/'depth/PORTABLE_TARGETS.json').read_text())['suites']
 with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:rows+=list(ex.map(lambda n:run(n,['replay_selected.py','--suite',n]),names))
 after={x.relative_to(P).as_posix():{'sha256':h(x),'bytes':x.stat().st_size} for x in P.rglob('*') if x.is_file()}
 result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_sha256':snapshot['PACKAGE_CONTENTS.json']['sha256'],'candidate_unchanged_during_execution':snapshot==after,'runs':rows,'scope':'Independent disposable-copy selected new targets and delivery tools, no historical all-suite or Lean/CI execution.'}
 (D/'EXECUTION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
 sys.exit(any(r['exit_code'] for r in rows) or snapshot!=after)
