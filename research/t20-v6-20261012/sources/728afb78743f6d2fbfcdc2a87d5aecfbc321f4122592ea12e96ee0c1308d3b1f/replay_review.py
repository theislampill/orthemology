#!/usr/bin/env python3
"""Portable isolated replay of author and independent controls; inputs are never modified."""
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser();p.add_argument('--author-dir',type=Path,default=HERE.parent/'nonautonomous-energy-drift-reverse-lift-20261010');p.add_argument('--output-dir',type=Path,required=True);p.add_argument('--original-workspace',type=Path);a=p.parse_args()
author=a.author_dir.resolve();out=a.output_dir.resolve();assert out!=author and out!=HERE
h=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
snapshot=json.loads((HERE/'AUTHOR_SNAPSHOT_BINDINGS.json').read_text());originals=json.loads((HERE/'ORIGINAL_SOURCE_BINDINGS.json').read_text())
for f,d in snapshot.items():assert h(author/f)==d,f
for f,d in originals.items():
 assert h(author/'inputs'/f)==d,f
 if a.original_workspace:assert h(a.original_workspace/f)==d,f
out.mkdir(parents=True,exist_ok=True)
for f in snapshot:
 dst=out/'author'/f;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(author/f,dst)
ind=out/'independent'/'check_independent.py';ind.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(HERE/'check_independent.py',ind)
for name,script in [('author',out/'author'/'check_exact.py'),('independent',ind)]:
 run=subprocess.run([sys.executable,str(script)],capture_output=True,text=True)
 (out/(name+'.stdout.log')).write_text(run.stdout);(out/(name+'.stderr.log')).write_text(run.stderr)
 assert run.returncode==0,(name,run.returncode,run.stderr)
ar=json.loads((out/'author'/'EXACT_CHECKS.json').read_text());ir=json.loads(ind.with_name('INDEPENDENT_RESULTS.json').read_text())
assert ar['status']=='passed' and ar['checks']==84
assert ir['status']=='PASS' and ir['checks']==56
assert h(out/'author'/'EXACT_CHECKS.json')==snapshot['EXACT_CHECKS.json']
for f,d in snapshot.items():assert h(author/f)==d,f
for f,d in originals.items():
 assert h(author/'inputs'/f)==d,f
 if a.original_workspace:assert h(a.original_workspace/f)==d,f
record={'status':'PASS','author_checks':84,'author_categories':ar['groups'],'independent_checks':56,'frozen_author_files_unchanged':len(snapshot),'packaged_source_files_matched':len(originals),'original_source_files_checked':len(originals) if a.original_workspace else 0,'portable_author_result_identical':True,'scope':'Finite exact replay; universal mathematical review is in REVIEW.md.'}
(out/'REPLAY_RESULTS.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
