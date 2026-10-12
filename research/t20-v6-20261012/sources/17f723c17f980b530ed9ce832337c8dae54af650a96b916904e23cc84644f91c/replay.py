#!/usr/bin/env python3
"""Verify the preserved bytes, then reproduce exact author controls off-packet."""
from pathlib import Path
import argparse
import hashlib
import json
import subprocess
import sys

HERE=Path(__file__).resolve().parent

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('output_dir',type=Path,help='New, nonexistent directory for replay outputs')
    parser.add_argument('--verify-original-inputs',type=Path,metavar='WORKSPACE',help='Optionally check direct original paths, not transitive dependencies')
    args=parser.parse_args()
    target=args.output_dir.resolve()
    if target.exists():
        raise RuntimeError('Replay output already exists: '+str(target))
    if target==HERE or HERE in target.parents:
        raise RuntimeError('Replay output must be outside the preserved packet')
    manifest=json.loads((HERE/'MANIFEST.json').read_text())
    for item in manifest['files']:
        rel=Path(item['path'])
        if rel.is_absolute() or '..' in rel.parts:
            raise RuntimeError('Unsafe manifest path: '+str(rel))
        path=HERE/rel
        b=path.read_bytes()
        if len(b)!=item['bytes'] or hashlib.sha256(b).hexdigest()!=item['sha256']:
            raise RuntimeError('Manifest mismatch: '+str(rel))
    originals_checked=0
    if args.verify_original_inputs is not None:
        bindings=json.loads((HERE/'INPUT_BINDINGS.json').read_text())
        for item in bindings['inputs']:
            b=(args.verify_original_inputs/item['original_path']).read_bytes()
            if len(b)!=item['bytes'] or hashlib.sha256(b).hexdigest()!=item['sha256']:
                raise RuntimeError('Original input mismatch: '+item['original_path'])
            originals_checked+=1
    target.mkdir(parents=True)
    run=subprocess.run([sys.executable,str(HERE/'verify.py'),'--output-dir',str(target)],capture_output=True,text=True)
    (target/'verification.txt').write_text(run.stdout)
    (target/'stderr.txt').write_text(run.stderr)
    if run.returncode:
        raise RuntimeError('Control run failed; see '+str(target))
    for name in ('CONTROL_RESULTS.json','verification.txt'):
        if (target/name).read_bytes()!=(HERE/name).read_bytes():
            raise RuntimeError('Replay output differs: '+name)
    result=json.loads((target/'CONTROL_RESULTS.json').read_text())
    receipt={'status':'PASS','scope':'Manifest integrity and exact author-control replay; no independent theorem review, transitive inherited replay, fresh source reading, integration, or programme closure.','manifest_sha256':hashlib.sha256((HERE/'MANIFEST.json').read_bytes()).hexdigest(),'manifest_files_verified':len(manifest['files']),'original_inputs_verified':originals_checked,'assertion_groups':result['assertion_groups'],'regenerated_control_json_and_stdout_byte_identical':True}
    (target/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':
    main()
