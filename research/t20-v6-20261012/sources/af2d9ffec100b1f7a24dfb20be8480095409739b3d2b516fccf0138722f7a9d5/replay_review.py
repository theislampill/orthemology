#!/usr/bin/env python3
"""Replay the immutable author packet and independent finite controls."""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parent
AUTHOR=ROOT/'radial-quartic-gradient-reverse-lift-20261010'
EXPECTED_RECEIPT='13adda9b09b6f1464998755ac501cfc75694d754bbcf5cd8cf6c4c224baf090f'
EXPECTED_PROOF='35ecab255d407a8b8405471b60f52c8f37d35fae6cd5f2b9a4c16573926c4e26'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(p,o): p.write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
assert sha(AUTHOR/'AUTHOR_RECEIPT.json')==EXPECTED_RECEIPT
receipt=json.loads((AUTHOR/'AUTHOR_RECEIPT.json').read_text())
assert sha(AUTHOR/'RESULT.md')==EXPECTED_PROOF
for rel,digest in receipt['files'].items(): assert sha(AUTHOR/rel)==digest,rel
bindings=json.loads((AUTHOR/'INPUT_BINDINGS.json').read_text())
for rel,digest in bindings.items(): assert sha(ROOT/rel)==digest,rel
snapshot={'author_directory':AUTHOR.name,'receipt_sha256':EXPECTED_RECEIPT,'proof_sha256':EXPECTED_PROOF,'frozen_files':receipt['files'],'source_files':bindings}
write(HERE/'AUTHOR_SNAPSHOT_BINDINGS.json',snapshot)
# Create distinct author replay directory with copied exact frozen inputs.
replay=HERE/'isolated-replay'; replay.mkdir(exist_ok=True)
candidate=replay/AUTHOR.name; candidate.mkdir(exist_ok=True)
for rel in ('check_exact.py','INPUT_BINDINGS.json'): shutil.copyfile(AUTHOR/rel,candidate/rel)
for rel,digest in bindings.items():
    dest=replay/rel; dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/rel,dest)
    assert sha(dest)==digest
run=subprocess.run([sys.executable,str(candidate/'check_exact.py')],cwd=replay,capture_output=True,text=True)
(HERE/'author-replay.log').write_text(run.stdout)
(HERE/'author-replay.stderr').write_text(run.stderr)
assert run.returncode==0,run.stderr
assert (candidate/'EXACT_CHECKS.json').read_bytes()==(AUTHOR/'EXACT_CHECKS.json').read_bytes()
assert run.stdout.encode()==(AUTHOR/'check_exact.log').read_bytes()
# Independently authored controls, separately executed and compared.
independent_output=replay/'INDEPENDENT_RESULTS.json'
irun=subprocess.run([sys.executable,str(HERE/'check_independent.py'),'--output',independent_output.name],cwd=replay,capture_output=True,text=True)
(HERE/'independent-replay.log').write_text(irun.stdout)
(HERE/'independent-replay.stderr').write_text(irun.stderr)
assert irun.returncode==0,irun.stderr
assert independent_output.read_bytes()==(HERE/'INDEPENDENT_RESULTS.json').read_bytes()
independent=json.loads(independent_output.read_text())
assert independent['count']==106 and independent['pass']
for rel,digest in receipt['files'].items(): assert sha(AUTHOR/rel)==digest,rel
for rel,digest in bindings.items(): assert sha(ROOT/rel)==digest,rel
write(HERE/'REPLAY_RESULTS.json',{'status':'PASS','author_receipt_sha256':EXPECTED_RECEIPT,'author_proof_sha256':EXPECTED_PROOF,'author_check_count':receipt['exact_check_count'],'author_replay_byte_identical':True,'independent_check_count':independent['count'],'independent_replay_byte_identical':True,'formula_mutation_controls':sum('nonzero_residual' in q for q in independent['checks']),'bound_sources_preserved':len(bindings),'scope':'Finite checks and digest verification supplement the written ordinary proof review; no formal kernel, protected edits, integration or closure.'})
print(json.dumps(json.loads((HERE/'REPLAY_RESULTS.json').read_text()),sort_keys=True))
