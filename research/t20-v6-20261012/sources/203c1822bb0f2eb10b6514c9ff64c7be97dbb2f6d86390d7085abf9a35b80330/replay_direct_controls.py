#!/usr/bin/env python3
"""Cold compile only the independent batch source controls.

The unchanged 38 scientific dependencies are read-only prior reviewer objects.
Restored official Mathlib caches are verified, not called an independent rebuild.
"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
p = argparse.ArgumentParser()
p.add_argument('--restoration', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
restored, out = a.restoration.resolve(), a.output.resolve()


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''):
            h.update(b)
    return h.hexdigest()


def require(test, message):
    if not test:
        raise RuntimeError(message)


prior = ROOT / 'tranche8/reviews/criterion-history-join/reference-clock-v6-replay/RECEIPT.json'
require(sha(prior) == 'f830103361e30e56abd0b6f55632d470482b172c0c2de44d1f31a932cd4c5219',
        'Prior independently accepted receipt identity mismatch')
old = json.loads(prior.read_text())
objects = old['predecessor_objects_used_read_only']
require(len(objects) == 38, 'Incorrect inherited module count')
sources = [HERE / 'BatchSourceChallenges.lean', HERE / 'BatchHistoryPremiseChallenges.lean']
source_rows = [{'path': str(q), 'sha256': sha(q), 'bytes': q.stat().st_size} for q in sources]
lean = restored / 'lean-toolchain-4.19.0/lean-4.19.0-linux/bin/lean'
mathlib = restored / 'mathlib-c44e0c8'
require(sha(lean) == old['compiler_sha256'], 'Compiler differs from accepted Lean 4.19.0')
version = subprocess.check_output([str(lean), '--version'], text=True).strip()
require('4.19.0' in version and '6caaee842e94' in version, 'Compiler version mismatch')
pins = ROOT / 'tranche8/research/alias-runtime/public/source-v3/dependencies'
restoration_receipt = restored / 'restoration-verification.json'
require(restoration_receipt.is_file(), 'Restoration verification is not complete')
require(json.loads(restoration_receipt.read_text())['status'] ==
        'PASS_WITH_FIVE_PATH_ONLY_TRACE_DELTAS', 'Restoration verification did not pass')


def verify_old_inputs():
    for row in objects:
        q = Path(row['path'])
        require(q.is_file() and q.stat().st_size == row['bytes'] and sha(q) == row['sha256'],
                'Changed inherited object: ' + row['module'])
    for row in json.loads((HERE / 'PRE_AUTHOR_SOURCE_BINDING.json').read_text())['sources']:
        q = ROOT / row['path']
        require(q.stat().st_size == row['bytes'] and sha(q) == row['sha256'],
                'Changed source: ' + str(q))


verify_old_inputs()
# Re-run the non-mutating tree verifier, rather than relying solely on a receipt.
spec = importlib.util.spec_from_file_location('restoration_verifier', restored / 'verify_restoration.py')
verifier = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verifier)
lean_pin = json.loads((pins / 'LEAN_DISTRIBUTION_PIN.json').read_text())
lean_tree = verifier.check_tree(lean.parent.parent, lean_pin)
require(lean_tree['status'] == 'PASS', 'Restored Lean distribution differs from pin')
cache_pin = json.loads((pins / 'MATHLIB_CACHE_PIN.json').read_text())
cache = verifier.check_tree(mathlib, cache_pin)
relocation = json.loads((restored / 'CACHE_METADATA_RELOCATION.json').read_text())
allowed = {row['path']: row for row in relocation['files']}
require(len(allowed) == 5 and all(q.startswith('.lake/build/lib/lean/Cache/') and
        q.endswith('.trace') for q in allowed), 'Unbounded relocation exception')
require(not cache['extra'] and not cache['missing'] and
        {row['path'] for row in cache['mismatches']} == set(allowed), 'Unexpected cache delta')
pinrows = {row['path']: row for row in cache_pin['entries']}
for path, row in allowed.items():
    data = (mathlib / path).read_bytes()
    normalized = data.replace(relocation['current_prefix'].encode(),
                              relocation['historical_prefix'].encode())
    require(hashlib.sha256(data).hexdigest() == row['current_sha256'] and
            hashlib.sha256(normalized).hexdigest() == row['original_pin_sha256'] ==
            pinrows[path]['sha256'], 'Relocation comparison failed: ' + path)
source_pin = json.loads((pins / 'MATHLIB_SOURCE_PIN.json').read_text())
for row in source_pin['files']:
    q = mathlib / row['path']
    require(q.stat().st_size == row['size'] and sha(q) == row['sha256'],
            'Dependency source differs: ' + row['path'])
require(not out.exists() and out.is_relative_to(HERE), 'Output must be a new reviewer directory')
out.mkdir()
(out / 'build').mkdir()
dirs = list(dict.fromkeys(str(Path(row['path']).parent) for row in objects))
env = dict(os.environ, LEAN_PATH=':'.join([str(out / 'build')] + dirs +
           [str(mathlib / name) for name in cache_pin['roots']]))
stages = []
axioms = {}
for q in sources:
    command = [str(lean), '-j1', '-s65536', '-o', str(out / 'build' / (q.stem + '.olean')), str(q)]
    start = time.monotonic()
    result = subprocess.run(command, env=env, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=600)
    log = out / (q.stem + '.log')
    log.write_text(result.stdout)
    stages.append({'module': q.stem, 'command': command, 'exit_code': result.returncode,
                   'seconds': round(time.monotonic() - start, 3), 'source_sha256': sha(q),
                   'log_sha256': sha(log)})
    (out / 'STAGES.json').write_text(json.dumps(stages, indent=2) + '\n')
    print(q.stem, result.returncode, flush=True)
    require(result.returncode == 0 and not re.search(r'error:|warning:|sorryAx', result.stdout),
            'Compilation failed: ' + q.stem)
    for name, dependencies in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", result.stdout):
        values = [v.strip() for v in dependencies.split(',') if v.strip()]
        require(set(values) <= {'propext', 'Classical.choice', 'Quot.sound'}, 'Nonstandard axiom')
        axioms[name] = values
    for name in re.findall(r"'([^']+)' does not depend on any axioms", result.stdout):
        axioms[name] = []
    require(sum(1 for name in axioms if name.startswith(
        'BatchSourceReview.' if q.stem == 'BatchSourceChallenges' else 'BatchHistoryPremiseReview.')) ==
        len(re.findall(r'^theorem\s+', q.read_text(), re.M)), 'Not all theorem closures audited')
verify_old_inputs()
for row in source_rows:
    require(sha(Path(row['path'])) == row['sha256'], 'Control source changed during replay')
receipt = {'status': 'PASS_INDEPENDENT_SOURCE_CONTROLS',
           'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'claim': 'Independent direct-source controls, not candidate batch-extension acceptance',
           'compiler_version': version, 'compiler_sha256': sha(lean),
           'lean_distribution_entries_verified': len(lean_pin['entries']),
           'restoration_receipt_sha256': sha(restoration_receipt),
           'relocation_manifest_sha256': sha(restored / 'CACHE_METADATA_RELOCATION.json'),
           'mathlib_source_records_verified': len(source_pin['files']),
           'mathlib_cache_entries_verified': len(cache_pin['entries']),
           'cache_metadata_delta': 'Five trace compiler-path relocations, actual bytes preserved',
           'independent_full_mathlib_rebuild': False,
           'previous_reviewer_receipt_sha256': sha(prior),
           'inherited_objects_used_read_only': objects, 'control_sources': source_rows,
           'stages': stages, 'axiom_inventory': axioms, 'all_inputs_stable': True}
(out / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PASS', len(axioms), 'independent theorems', flush=True)
