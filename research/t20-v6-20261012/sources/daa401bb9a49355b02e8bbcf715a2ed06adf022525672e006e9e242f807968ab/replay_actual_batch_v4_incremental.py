#!/usr/bin/env python3
"""Independent incremental cold compilation of the additive immutable batch-v4 availability-iff sources.

The accepted cold-v1 plus incremental-v3 scientific builds are reused read-only
after exact identity checks. Three additions and ten new reviewer theorems are
freshly compiled. No author object directory enters LEAN_PATH.
"""
import argparse, datetime, hashlib, importlib.util, json, os, re, subprocess, sys, time
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
p = argparse.ArgumentParser()
p.add_argument('--candidate', type=Path, required=True)
p.add_argument('--restoration', type=Path, required=True)
p.add_argument('--output', type=Path, required=True)
p.add_argument('--resume', action='store_true')
a = p.parse_args()
candidate, restored, out = a.candidate.resolve(), a.restoration.resolve(), a.output.resolve()
EXPECTED = '186281d14d0ea41e7ac49aa7a392a6cf05cb92047670f7d639420720785ecf0e'
PREVIOUS = '58798e94a43d42595c58f61de8c0ec42be89275530d00b52e4f31024b4e7f611'

def sha(q):
    h = hashlib.sha256()
    with q.open('rb') as f:
        for b in iter(lambda: f.read(1048576), b''): h.update(b)
    return h.hexdigest()

def require(test, message):
    if not test: raise RuntimeError(message)

def strip(text):
    out = []; i = depth = 0
    while i < len(text):
        if text[i:i+2] == '/-': depth += 1; i += 2; continue
        if depth:
            if text[i:i+2] == '-/': depth -= 1; i += 2
            else: out.append('\n' if text[i] == '\n' else ' '); i += 1
            continue
        if text[i:i+2] == '--':
            j = text.find('\n', i); i = len(text) if j < 0 else j; continue
        if text[i] == '"':
            i += 1
            while i < len(text):
                if text[i] == '\\': i += 2
                elif text[i] == '"': i += 1; break
                else: i += 1
            out.append(' '); continue
        out.append(text[i]); i += 1
    require(depth == 0, 'Unterminated block comment')
    return ''.join(out)

def verify_candidate():
    require(sha(candidate / 'MANIFEST.json') == EXPECTED, 'Candidate manifest differs')
    manifest = json.loads((candidate / 'MANIFEST.json').read_text())
    previous = ROOT / 'tranche8/formal/criterion-history-join/milestones/monotone-reference-clock-v6'
    require(sha(previous / 'MANIFEST.json') == PREVIOUS, 'Accepted predecessor differs')
    old = json.loads((previous / 'MANIFEST.json').read_text())
    require((candidate / 'PREDECESSOR_MANIFEST_V6.json').read_bytes() ==
            (previous / 'MANIFEST.json').read_bytes(), 'Copied predecessor manifest differs')
    for row in manifest['files']:
        q = candidate / row['path']
        require(q.is_file() and not q.is_symlink() and q.stat().st_size == row['bytes'] and
                sha(q) == row['sha256'], 'Candidate file differs: ' + row['path'])
    for row in old['files']:
        require((candidate / row['path']).read_bytes() == (previous / row['path']).read_bytes(),
                'Inherited source changed: ' + row['path'])
    require({str(q.relative_to(candidate)) for q in candidate.rglob('*') if q.is_file()} ==
            {r['path'] for r in manifest['files']} | {'MANIFEST.json'}, 'Candidate inventory differs')
    native = candidate / 'imports/proper-function-and-candidate-e.md'
    require(native.stat().st_size == 3013 and sha(native) ==
            'e4ae2e2751535e625f245a1bb2f2e4f2f4c447a55c859e1b1c94dbbf48adf359',
            'Native source differs')
    payload = (candidate / 'PinnedSource.lean').read_text().split('def sourceBytes : List Nat := [', 1)[1].split(']', 1)[0]
    require(bytes(map(int, re.findall(r'\d+', payload))) == native.read_bytes(), 'Native source embedding differs')
    for ver, expected in [('actual-batch-v1', '83e6449ce32bb6ecd3688c33592c0357f014aa075eabffa9290f7fbca000af45'),
                          ('actual-batch-v2', '1b8cce197d5f5d6b9624d8576618a9c1ec71680f4ce33eb69d3a4ad2b2512333'),
                          ('actual-batch-v3', 'a9a96e455535805824db888adfadc06399a36a5efccd281346368bb4d57cb159')]:
        predecessor = candidate.parent / ver
        require(sha(predecessor / 'MANIFEST.json') == expected, 'Changed predecessor ' + ver)
        for row in json.loads((predecessor / 'MANIFEST.json').read_text())['files']:
            require((candidate / row['path']).read_bytes() == (predecessor / row['path']).read_bytes(),
                    'Changed inherited ' + ver + ' file: ' + row['path'])
    for row in json.loads((candidate / 'CONTROLLER_SOURCE_BINDING.json').read_text())['files']:
        require((candidate / row['path']).read_bytes() == (ROOT / row['source']).read_bytes() and
                sha(candidate / row['path']) == row['sha256'], 'Controller source binding differs')
    original_projection = json.loads((ROOT / 'tranche8/baseline/seventh-components/composition/PROJECTION_MANIFEST.json').read_text())
    bound = next(r for r in original_projection['retained'] if r['public_path'] == 'tests/BatchTests.lean')
    require(bound['sha256'] == bound['original_sha256'] == sha(candidate / 'provenance/BatchTests.lean'),
            'Accepted original controller provenance differs')
    return manifest

manifest = verify_candidate()
base = json.loads((candidate / 'SOURCE_ORDER.json').read_text())
cancel = json.loads((candidate / 'CANCELLATION_SOURCE_ORDER.json').read_text())['additional_modules']
clock = json.loads((candidate / 'REFERENCE_CLOCK_SOURCE_ORDER.json').read_text())['additional_modules']
batch = json.loads((candidate / 'BATCH_SOURCE_ORDER.json').read_text())['additional_modules']
successor = json.loads((candidate / 'BATCH_SUCCESSOR_SOURCE_ORDER.json').read_text())['additional_modules']
retry = json.loads((candidate / 'BATCH_RETRY_SOURCE_ORDER.json').read_text())['additional_modules']
v3_delta = successor + retry
delta = json.loads((candidate / 'BATCH_SURVIVAL_SOURCE_ORDER.json').read_text())['additional_modules']
old_custom = base['imports'] + base['new'] + cancel + clock + batch + v3_delta
custom = old_custom + delta
require(len(old_custom) == 58 and len(delta) == 3 and len(batch) == 9, 'Unexpected custom module count')
prior_receipt = HERE / 'actual-batch-v1-cold/RECEIPT.json'
require(sha(prior_receipt) == 'af48183cfef6ae23fc826524ad4bf6d63622f1ac4a9aec78665dace0bd4d0ee9', 'Cold-v1 receipt differs')
prior = json.loads(prior_receipt.read_text())
prior3_receipt = HERE / 'actual-batch-v3-incremental/RECEIPT.json'
require(sha(prior3_receipt) == '4d5b72f7827a93993a450329ce2d75273665c631ed0523c8a6b55a7626ee86f0', 'Accepted incremental-v3 receipt differs')
prior3 = json.loads(prior3_receipt.read_text())
prior3_build = HERE / 'actual-batch-v3-incremental/build'
prior_build = HERE / 'actual-batch-v1-cold/build'
old_objects = []
for row in prior['stages']:
    obj = prior_build / (row['module'] + '.olean')
    old_objects.append({'module': row['module'], 'path': str(obj), 'sha256': row['object_sha256']})
for row in prior3['stages']:
    obj = prior3_build / (row['module'] + '.olean')
    old_objects.append({'module': row['module'], 'path': str(obj), 'sha256': row['object_sha256']})
def verify_prior_objects():
    for row in old_objects:
        require(sha(Path(row['path'])) == row['sha256'], 'Preserved cold-v1 object differs: ' + row['module'])
    for row in prior3['review_sources']:
        require(sha(Path(row['path'])) == row['sha256'], 'Accepted reviewer source differs')
verify_prior_objects()

pins = ROOT / 'tranche8/research/alias-runtime/public/source-v3/dependencies'
lean = restored / 'lean-toolchain-4.19.0/lean-4.19.0-linux/bin/lean'
mathlib = restored / 'mathlib-c44e0c8'
require(sha(lean) == base['compiler_sha256'], 'Compiler differs')
version = subprocess.check_output([str(lean), '--version'], text=True).strip()
require('4.19.0' in version and '6caaee842e94' in version, 'Wrong compiler version')
spec = importlib.util.spec_from_file_location('restoration_verifier', restored / 'verify_restoration.py')
verifier = importlib.util.module_from_spec(spec); spec.loader.exec_module(verifier)
lean_pin = json.loads((pins / 'LEAN_DISTRIBUTION_PIN.json').read_text())
require(verifier.check_tree(lean.parent.parent, lean_pin)['status'] == 'PASS', 'Lean distribution differs')
cache_pin = json.loads((pins / 'MATHLIB_CACHE_PIN.json').read_text())
cache = verifier.check_tree(mathlib, cache_pin)
relocation = json.loads((restored / 'CACHE_METADATA_RELOCATION.json').read_text())
allowed = {row['path']: row for row in relocation['files']}
require(len(allowed) == 5 and all(q.startswith('.lake/build/lib/lean/Cache/') and q.endswith('.trace')
        for q in allowed), 'Unbounded relocation exception')
require(not cache['extra'] and not cache['missing'] and
        {r['path'] for r in cache['mismatches']} == set(allowed), 'Unexpected dependency cache delta')
pinrows = {r['path']: r for r in cache_pin['entries']}
for path, row in allowed.items():
    data = (mathlib / path).read_bytes()
    normalized = data.replace(relocation['current_prefix'].encode(), relocation['historical_prefix'].encode())
    require(hashlib.sha256(data).hexdigest() == row['current_sha256'] and
            hashlib.sha256(normalized).hexdigest() == row['original_pin_sha256'] == pinrows[path]['sha256'],
            'Invalid trace relocation: ' + path)
source_pin = json.loads((pins / 'MATHLIB_SOURCE_PIN.json').read_text())
for row in source_pin['files']:
    q = mathlib / row['path']
    require(q.stat().st_size == row['size'] and sha(q) == row['sha256'], 'Dependency source differs')

require(out.is_relative_to(HERE), 'Output must be in reviewer directory')
if a.resume:
    require(out.is_dir() and json.loads((out / 'COLD_BUILD_BINDING.json').read_text())['candidate_manifest_sha256'] == EXPECTED,
            'No matching cold build to resume')
else:
    require(not out.exists(), 'Cold output must be new')
    out.mkdir(); (out / 'build').mkdir(); (out / 'logs').mkdir()
    (out / 'COLD_BUILD_BINDING.json').write_text(json.dumps({
        'candidate_manifest_sha256': EXPECTED, 'initially_empty_custom_build': True,
        'started_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}, indent=2) + '\n')
env = dict(os.environ, LEAN_PATH=':'.join([str(out / 'build'), str(prior3_build), str(prior_build)] +
           [str(mathlib / name) for name in cache_pin['roots']]))
stages_file = out / 'STAGES.json'
stages = json.loads(stages_file.read_text()) if stages_file.exists() else []

def compile_one(module, q):
    obj = out / 'build' / (module + '.olean')
    previous = next((r for r in reversed(stages) if r['module'] == module), None)
    if a.resume and previous and previous['exit_code'] == 0 and previous['source_sha256'] == sha(q) and obj.is_file() and sha(obj) == previous['object_sha256']:
        print('Retain same-run cold object:', module, flush=True)
        return
    command = [str(lean), '-j1', '-s65536', '-o', str(obj), str(q)]
    start = time.monotonic()
    result = subprocess.run(command, env=env, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, timeout=900)
    log = out / 'logs' / (module + '-' + str(len(stages) + 1) + '.log')
    log.write_text(result.stdout)
    stage = {'module': module, 'command': command, 'exit_code': result.returncode,
             'seconds': round(time.monotonic() - start, 3), 'source_sha256': sha(q),
             'log': str(log), 'log_sha256': sha(log)}
    if result.returncode == 0 and obj.is_file(): stage['object_sha256'] = sha(obj)
    stages.append(stage); stages_file.write_text(json.dumps(stages, indent=2) + '\n')
    print(module, result.returncode, stage['seconds'], flush=True)
    require(result.returncode == 0 and not re.search(r'error:|warning:|sorryAx', result.stdout),
            'Compilation failed: ' + module)

for row in delta: compile_one(row['module'], candidate / row['path'])
review_names = ['BatchSourceChallenges', 'BatchHistoryPremiseChallenges', 'BatchAvailabilityChallenges',
                'BatchFaultSemanticsChallenges', 'BatchContractChallenges',
                'BatchFreshnessV2SourceChallenges', 'BatchV2ContractChallenges',
                'BatchAvailabilityIffSourceChallenges', 'BatchSurvivalContractChallenges']
for name in review_names[-2:]: compile_one(name, HERE / (name + '.lean'))
inventory = []
for row in base['new'] + cancel + clock + batch + v3_delta + delta:
    body = strip((candidate / row['path']).read_text())
    require(not re.search(r'\b(sorry|axiom|native_decide|unsafe)\b', body), 'Forbidden proof token: ' + row['module'])
    inventory += [row['namespace'] + '.' + name for name in re.findall(r'\btheorem\s+([A-Za-z0-9_]+)', body)]
inherited_count = sum(len(re.findall(r'\btheorem\s+([A-Za-z0-9_]+)', strip((candidate / row['path']).read_text())))
                      for row in base['new'] + cancel + clock)
require(inherited_count == 312, 'Inherited theorem census differs')
review_inventory = []
for name in review_names:
    body = strip((HERE / (name + '.lean')).read_text())
    require(not re.search(r'\b(sorry|axiom|native_decide|unsafe)\b', body), 'Forbidden reviewer proof token')
    namespace = re.search(r'namespace\s+([A-Za-z0-9_.]+)', body).group(1)
    review_inventory += [namespace + '.' + n for n in re.findall(r'\btheorem\s+([A-Za-z0-9_]+)', body)]
all_axioms = out / 'AllAxioms.lean'
all_axioms.write_text('\n'.join(['import ' + r['module'] for r in custom] +
    ['import ' + n for n in review_names] + ['#print axioms ' + n for n in inventory + review_inventory]) + '\n')
compile_one('AllAxioms', all_axioms)
last = next(r for r in reversed(stages) if r['module'] == 'AllAxioms')
log = Path(last['log']).read_text()
axioms = {n: [x.strip() for x in deps.split(',') if x.strip()]
          for n, deps in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", log)}
axioms.update({n: [] for n in re.findall(r"'([^']+)' does not depend on any axioms", log)})
require(set(axioms) == set(inventory + review_inventory), 'Missing or extra axiom closures')
require(all(set(v) <= {'propext', 'Classical.choice', 'Quot.sound'} for v in axioms.values()), 'Nonstandard axiom closure')
verify_candidate()
verify_prior_objects()
for row in delta:
    latest = next(r for r in reversed(stages) if r['module'] == row['module'])
    require(sha(out / 'build' / (row['module'] + '.olean')) == latest['object_sha256'], 'Cold object changed')
receipt = {'status': 'PASS_ADDITIVE_V4_IFF_REPLAY_AND_REVIEW_CHALLENGES',
    'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'candidate_manifest_sha256': EXPECTED,
    'candidate_immediate_predecessor_manifest_sha256': 'a9a96e455535805824db888adfadc06399a36a5efccd281346368bb4d57cb159',
    'accepted_scientific_predecessor_manifest_sha256': 'a9a96e455535805824db888adfadc06399a36a5efccd281346368bb4d57cb159',
    'inherited_v6_manifest_sha256': PREVIOUS,
    'all_inherited_source_bytes_unchanged': True, 'cold_new_custom_modules': len(delta),
    'total_custom_closure_modules': len(custom), 'fresh_additional_batch_modules': len(delta),
    'previous_scientific_objects_reused': len(old_custom),
    'accepted_cold_v1_receipt_sha256': sha(prior_receipt),
    'accepted_incremental_v3_receipt_sha256': sha(prior3_receipt),
    'prior_objects_verified_read_only': old_objects,
    'predecessor_scientific_objects_used_read_only': [r for r in old_objects if r['module'] in {q['module'] for q in old_custom}],
    'previous_reviewer_objects_used_read_only': [r for r in old_objects if r['module'] in set(review_names[:-2])],
    'prior_axiom_audit_objects_verified_not_imported': [r for r in old_objects if r['module'] == 'AllAxioms'],
    'lean_path': env['LEAN_PATH'], 'compiler_version': version, 'compiler_sha256': sha(lean),
    'lean_distribution_entries_verified': len(lean_pin['entries']),
    'mathlib_source_records_verified': len(source_pin['files']), 'mathlib_cache_entries_verified': len(cache_pin['entries']),
    'dependency_cache_rebuilt_independently': False,
    'relocation_manifest_sha256': sha(restored / 'CACHE_METADATA_RELOCATION.json'),
    'relocation_scope': 'Five preserved Cache/*.trace compiler-path-only metadata differences',
    'exact_native_source_bytes': 3013, 'author_theorems': len(inventory),
    'cumulative_batch_theorems': len(inventory) - inherited_count,
    'new_v4_theorems': len(inventory) - 445,
    'reviewer_theorems': len(review_inventory), 'axiom_inventory': axioms,
    'review_sources': [{'path': str(HERE / (n + '.lean')), 'sha256': sha(HERE / (n + '.lean'))} for n in review_names],
    'stages': stages, 'all_candidate_inputs_stable': True}
(out / 'RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
print('PASS', len(inventory), 'author theorems and', len(review_inventory), 'reviewer theorems', flush=True)
