#!/usr/bin/env python3
"""Verify frozen author/review evidence and replay in an isolated temporary tree."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
pins=json.loads((HERE/'AUTHOR_SNAPSHOT_BINDINGS.json').read_text())
author=ROOT/pins['author_directory']
assert sha(author/'FROZEN_MANIFEST.json')==pins['freeze_sha256']
for rel,want in pins['frozen_files'].items():assert sha(author/rel)==want,('author',rel)
for rel,want in pins['input_files'].items():assert sha(ROOT/rel)==want,('input',rel)
for rel,want in json.loads((HERE/'ANCESTOR_PINS.json').read_text()).items():assert sha(ROOT/rel)==want,('ancestor',rel)
receipt=json.loads((HERE/'REVIEW_RECEIPT.json').read_text())
for rel,want in receipt['review_files'].items():assert sha(HERE/rel)==want,('review',rel)
with tempfile.TemporaryDirectory(prefix='dissipative-gradient-review-') as temp:
    base=Path(temp)
    for rel in list(pins['frozen_files'])+['FROZEN_MANIFEST.json']:
        target=base/author.name/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(author/rel,target)
    for rel in pins['input_files']:
        target=base/rel;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,target)
    child=base/HERE.name;child.mkdir()
    for rel in ('check_independent.py','ANCESTOR_PINS.json'):
        shutil.copyfile(HERE/rel,child/rel)
    ar=subprocess.run([sys.executable,str(base/author.name/'check_exact.py')],capture_output=True,text=True,check=True)
    ir=subprocess.run([sys.executable,str(child/'check_independent.py')],capture_output=True,text=True,check=True)
    assert (base/author.name/'EXACT_CHECKS.json').read_bytes()==(author/'EXACT_CHECKS.json').read_bytes()
    assert (child/'INDEPENDENT_RESULTS.json').read_bytes()==(HERE/'INDEPENDENT_RESULTS.json').read_bytes()
    assert ar.stdout==(HERE/'author-replay.log').read_text()
    assert ir.stdout==(HERE/'independent-replay.log').read_text()
    aj=json.loads(ar.stdout);ij=json.loads(ir.stdout)
# Recheck after replay, guarding against checker mutation of external originals.
for rel,want in pins['frozen_files'].items():assert sha(author/rel)==want,('author-after',rel)
for rel,want in pins['input_files'].items():assert sha(ROOT/rel)==want,('input-after',rel)
print(json.dumps({'status':'PASS','author_checks':aj['exact_check_count'],'independent_checks':ij['checks'],'author_input_files':len(pins['input_files']),'author_frozen_files':len(pins['frozen_files']),'review_bound_files':len(receipt['review_files']),'fresh_replay_outputs_identical':True,'all_bound_sources_unchanged':True},indent=2))
