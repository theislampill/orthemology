#!/usr/bin/env python3
"""Integrity-check and replay both control suites in new isolated directories."""
from pathlib import Path
import argparse, hashlib, json, os, shutil, subprocess, sys
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser()
p.add_argument('output_dir',type=Path)
p.add_argument('--verify-original-inputs',type=Path)
a=p.parse_args();target=a.output_dir.resolve()
assert not target.exists(), 'Output already exists'
assert target!=HERE and HERE not in target.parents, 'Output must be outside review packet'
manifest=json.loads((HERE/'MANIFEST.json').read_text())
for item in manifest['files']:
    rel=Path(item['path']);assert not rel.is_absolute() and '..' not in rel.parts
    b=(HERE/rel).read_bytes()
    assert len(b)==item['bytes'] and hashlib.sha256(b).hexdigest()==item['sha256'],str(rel)
assert hashlib.sha256((HERE/'isolated-author-copy/MANIFEST.json').read_bytes()).hexdigest()=='1a55afdd82a820d8006a23a3133a53e35737e1cae91b528f657ac227b04618b5'
target.mkdir(parents=True)
shutil.copytree(HERE/'isolated-author-copy',target/'author-copy')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
cmd=[sys.executable,str(target/'author-copy/replay.py'),str(target/'author-replay')]
if a.verify_original_inputs is not None:cmd+=['--verify-original-inputs',str(a.verify_original_inputs.resolve())]
author=subprocess.run(cmd,env=env,capture_output=True,text=True)
(target/'author-replay-command.stdout').write_text(author.stdout)
(target/'author-replay-command.stderr').write_text(author.stderr)
assert author.returncode==0,'Author replay failed'
ind=target/'independent';ind.mkdir();shutil.copyfile(HERE/'independent_checks.py',ind/'independent_checks.py')
run=subprocess.run([sys.executable,str(ind/'independent_checks.py')],env=env,capture_output=True,text=True)
(ind/'independent-verification.txt').write_text(run.stdout)
(ind/'stderr.txt').write_text(run.stderr)
assert run.returncode==0,'Independent controls failed'
for name in ['INDEPENDENT_RESULTS.json','independent-verification.txt']:
    assert (ind/name).read_bytes()==(HERE/name).read_bytes(),'Independent replay mismatch: '+name
receipt={'status':'PASS','review_manifest_sha256':hashlib.sha256((HERE/'MANIFEST.json').read_bytes()).hexdigest(),'review_manifest_files_verified':len(manifest['files']),'author_assertion_groups':35,'independent_assertion_groups':20,'independent_outputs_byte_identical':True,'scope':'Exact replay and integrity only; no automated theorem certification, fresh source reading, transitive inherited replay, integration, or programme closure.'}
(target/'REVIEW_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
