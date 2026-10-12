#!/usr/bin/env python3
"""Replay both finite checkers in copies; never write into the frozen author/predecessors."""
import argparse,hashlib,json,shutil,subprocess,sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--workspace-root',type=Path,default=HERE.parent)
parser.add_argument('--output-dir',type=Path,required=True)
args=parser.parse_args(); root=args.workspace_root.resolve(); out=args.output_dir.resolve()
assert out!=HERE and out!=root
out.mkdir(parents=True,exist_ok=True)
hash_file=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
author=json.loads((HERE/'AUTHOR_SNAPSHOT_BINDINGS.json').read_text())
inputs=json.loads((HERE/'PREDECESSOR_BINDINGS.json').read_text())
for name,digest in {**author,**inputs}.items():
    src=root/name; assert hash_file(src)==digest,name
    dst=out/'workspace'/name; dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(src,dst)
source=HERE/'check_independent.py'; dst=out/'independent'/'check_independent.py';dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(source,dst)
author_check=out/'workspace'/'energy-controlled-gradient-reverse-lift-20261010'/'check_exact.py'
for name,script in [('author',author_check),('independent',dst)]:
    proc=subprocess.run([sys.executable,str(script)],capture_output=True,text=True)
    (out/f'{name}.stdout.log').write_text(proc.stdout)
    (out/f'{name}.stderr.log').write_text(proc.stderr)
    assert proc.returncode==0,(name,proc.returncode,proc.stderr)
actual_author=json.loads(author_check.with_name('EXACT_CHECKS.json').read_text())
actual_independent=json.loads(dst.with_name('INDEPENDENT_RESULTS.json').read_text())
assert actual_author['status']=='passed' and actual_author['checks']==279
assert actual_independent['passed'] and actual_independent['count']==130
for name,digest in {**author,**inputs}.items(): assert hash_file(root/name)==digest,name
record={'status':'PASS','author_checks':279,'independent_checks':130,'author_snapshot_files':len(author),'predecessor_files':len(inputs),'source_and_author_bytes_preserved':True,'scope':'Finite replay only; mathematical verdict is in REVIEW.md.'}
(out/'REPLAY_RESULTS.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
