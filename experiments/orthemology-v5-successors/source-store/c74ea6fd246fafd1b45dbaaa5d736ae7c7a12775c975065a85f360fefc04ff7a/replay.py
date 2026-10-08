#!/usr/bin/env python3
"""Bounded fresh-object replay; existing official cache only, no writes to dependencies."""
import argparse, datetime, hashlib, json, os, pathlib, re, subprocess, sys
from pathlib import Path

def guarded_output(requested, protected):
    # Check both the user's lexical path and its actual filesystem destination.
    requested = Path(requested)
    if requested.exists() or requested.is_symlink():
        raise RuntimeError('Refusing an existing output path or symlink')
    lexical = Path(os.path.abspath(requested))
    output = requested.resolve()
    for raw in protected:
        raw = Path(raw)
        lexical_root = Path(os.path.abspath(raw))
        actual_root = raw.resolve()
        if lexical.is_relative_to(lexical_root) or output.is_relative_to(actual_root):
            raise RuntimeError('Output must be outside every protected input tree')
        # Internal cache aliases are allowed. Escaping aliases are unsupported,
        # including a dependency directory symlink into a separate object store.
        if actual_root.is_dir():
            for parent, directories, files in os.walk(actual_root, followlinks=False):
                for name in directories + files:
                    item = Path(parent) / name
                    if item.is_symlink() and not item.resolve().is_relative_to(actual_root):
                        raise RuntimeError('Escaping symlinked input layout is unsupported')
    if not output.parent.is_dir():
        raise RuntimeError('Output parent must already exist')
    return output

def verify_public_package(root):
    manifest = json.loads((root / 'SOURCE_PACKAGE.json').read_text())
    for row in manifest['files']:
        rel = Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts:
            raise RuntimeError('Unsafe package member')
        path = root / rel
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256'] or path.stat().st_size != row['bytes']:
            raise RuntimeError('Selected source package identity mismatch: ' + row['path'])
    return {'status': 'PASS', 'selected_files': len(manifest['files']), 'historical_raw_source_binding_replay': 'NOT_RUN; locator-only public source selection'}



HERE = pathlib.Path(__file__).resolve().parent
AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
ORIGINAL_HASH = '45ab18f7305033091f8fc31bb906d4c87866de47138df76637c6937440064503'
DAG_HASH = '796856c7de6d50d284a241a066ea9bdd6fb84409174329de6b81a16eb4572bb8'
LEAN_HASH = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
IMPORTS = ['Mathlib.Data.Bool.Basic', 'Mathlib.Data.Fintype.Basic', 'Mathlib.Tactic.ByContra']

def sha(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1024 * 1024), b''): h.update(b)
    return h.hexdigest()

def require(value, message):
    if not value: raise RuntimeError(message)

def dump(path, obj):
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False) + '\n')

def parse_readback(text, names):
    require(re.findall(r'^CONTINUATION_BEGIN (\S+)$', text, re.M) == names, 'Readback starts differ')
    require(re.findall(r'^CONTINUATION_END (\S+)$', text, re.M) == names, 'Readback ends differ')
    result = {}
    for name in names:
        blocks = re.findall(r'^CONTINUATION_BEGIN ' + re.escape(name) + r'\n(.*?)^CONTINUATION_END ' + re.escape(name) + '$', text, re.M | re.S)
        require(len(blocks) == 1, 'Readback block missing')
        block = blocks[0].strip()
        pivot = block.index("'" + name + "' ")
        typ, axtext = block[:pivot].strip(), block[pivot:]
        axes = [] if 'does not depend on any axioms' in axtext else sorted(x.strip() for x in re.search(r'\[([^]]*)\]', axtext, re.S)[1].split(','))
        require(set(axes) <= AXIOMS, 'Unexpected axiom in ' + name)
        result[name] = {'type': typ, 'type_sha256': hashlib.sha256(typ.encode()).hexdigest(), 'axioms': axes}
    return result

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output', type=pathlib.Path, help='A fresh, nonexistent output directory')
    ap.add_argument('--lean', type=pathlib.Path, required=True, help='Existing pinned official Lean 4.19.0 executable')
    ap.add_argument('--cache', type=pathlib.Path, required=True, help='Existing preparation root containing PREPARATION_RECEIPT.json and dependencies/')
    ap.add_argument('--predecessor', type=pathlib.Path, required=True, help='Existing predecessor repository root; read only')
    args = ap.parse_args()
    require(not args.output.is_symlink(), "Refusing an existing output symlink")
    out = args.output.resolve()
    require(not out.exists(), 'Output already exists; select a fresh path')
    require(out.parent.is_dir(), 'Output parent must exist')
    prep = args.cache.resolve()
    predecessor = args.predecessor.resolve()
    lean = args.lean.resolve()
    require(not any(out.is_relative_to(p) for p in [HERE, prep, predecessor, lean.parent.parent]), 'Output must be outside source, cache, predecessor and compiler trees')
    out = guarded_output(args.output, [HERE, args.cache, args.predecessor, args.lean.parent.parent, lean.parent.parent])
    verify_public_package(HERE)
    require(sha(prep / 'PREPARATION_RECEIPT.json') == '4b1c06c026eb6a7e15e6699e67b7322f8514f36fadba9c58e9975e5b0d0dfcf7', 'Expected existing preparation receipt differs')
    require(sha(lean) == LEAN_HASH, 'Compiler digest mismatch')
    # Original DAG seal is a custody reference, not a distributed body or a fresh source reread.
    original = HERE / 'inherited/SourceIdentity.original.lean'
    require(sha(original) == ORIGINAL_HASH, 'Exact historical original changed')
    derived = HERE / 'SourceIdentityDerived.lean'
    expected = ''.join('import ' + i + '\n' for i in IMPORTS).encode() + original.read_bytes().split(b'\n', 1)[1]
    require(derived.read_bytes() == expected, 'Derived source changed beyond approved imports')
    source_files = sorted(p for p in HERE.rglob('*.lean') if 'work-build' not in p.parts and not any(x.startswith('verification-') for x in p.parts))
    source_hashes = {str(p.relative_to(HERE)): sha(p) for p in source_files}
    for p in [HERE / 'OriginalBearerBridge.lean', HERE / 'BridgeControls.lean']:
        require(not re.search(r'^\s*(axiom|opaque)\b|\b(sorry|admit|native_decide)\b', p.read_text(), re.M), 'Forbidden authored admission: ' + p.name)
    out.mkdir()
    objects = out / 'objects'; objects.mkdir()
    packages = json.loads((prep / 'PREPARATION_RECEIPT.json').read_text())['source_revisions']
    paths = [objects] + [prep / 'dependencies' / r['name'] / '.lake/build/lib/lean' for r in packages]
    env = os.environ.copy(); env['LEAN_PATH'] = ':'.join(map(str, paths)); env['LEAN_NUM_THREADS'] = '1'
    commands = []
    def run(name, arguments, good=True):
        command = [str(lean), '-j1', '--trust=0'] + list(map(str, arguments))
        p = subprocess.run(command, env=env, cwd=HERE, text=True, capture_output=True, timeout=180)
        text = p.stdout + p.stderr; (out / name).write_text(text)
        commands.append({'command': command, 'exit_code': p.returncode, 'log': name, 'log_sha256': sha(out / name)})
        if good:
            require(p.returncode == 0 and not re.search(r'\berror:|\bPANIC\b|\bsorryAx\b', text), 'Compiler check failed: ' + name)
        return p.returncode, text
    run('toolchain.log', ['--version'])
    for module in ['SourceIdentityDerived', 'OriginalBearerBridge', 'BridgeControls']:
        run(module + '.log', ['-o', objects / (module + '.olean'), HERE / (module + '.lean')])
    run('contract-green.log', [HERE / 'tests/BridgeContract.lean'])
    red_code, red = run('contract-red.log', [HERE / 'tests/BridgeContract.before.lean'], good=False)
    require(red_code != 0 and red.count('error: unknown identifier') == 4 and red.count('error:') == 4, 'Invalid missing-feature red result')
    _, readback = run('readback.log', [HERE / 'ReadbackAudit.lean'])
    names = json.loads((HERE / 'DECLARATIONS.json').read_text())
    reads = parse_readback(readback, names); dump(out / 'READBACKS.json', reads)
    run('proof-readback.log', [HERE / 'ProofReadback.lean'])
    negative_code, negative = run('rejected.log', [HERE / 'negative-controls/RejectedClaims.lean'], good=False)
    require(negative_code != 0 and negative.count('error:') == 5 and negative.count("tactic 'decide' proved that the proposition") == 5, 'Negative result is not exactly five false-proposition rejections')
    old_path = predecessor / 'docs/provenance/v5-research-continuations/checks/db6ccdc793a0-orthability-core.json'
    require(sha(old_path) == '73dd81be434394a11406a045949151129ee43f71bb8c7b151ec40e801ed96950', 'Historical predecessor receipt differs')
    old = json.loads(old_path.read_text())['readbacks']
    comparisons = []
    for n in names:
        if not n.startswith('Orthemology.Tranche3.SourceIdentity.'): continue
        comparisons.append({'name': n, 'historical': old[n], 'current': {k: reads[n][k] for k in ['type_sha256','axioms']},
                            'match': old[n]['type_sha256'] == reads[n]['type_sha256'] and old[n]['axioms'] == reads[n]['axioms']})
    require(len(comparisons) == 18 and all(x['match'] for x in comparisons), 'Inherited type/axiom drift')
    dump(out / 'INHERITED_COMPARISON.json', {'historical_receipt': str(old_path), 'historical_receipt_sha256': sha(old_path), 'declarations': comparisons})
    all_paths = paths + [lean.parent.parent / 'lib/lean']
    closures = {}
    for label, file in [('all', 'ImportClosure.lean'), ('inherited_derived', 'InheritedImportClosure.lean')]:
        _, text = run(label + '-imports.log', [HERE / file])
        modules = re.findall(r'^KERNEL_IMPORT (\S+)$', text, re.M)
        require(modules and len(modules) == len(set(modules)), 'Empty or duplicate import closure')
        bindings = []
        for module in modules:
            matches = [root / (module.replace('.', '/') + '.olean') for root in all_paths if (root / (module.replace('.', '/') + '.olean')).is_file()]
            require(len(matches) == 1, 'Missing/ambiguous import object: ' + module)
            bindings.append({'module': module, 'object': str(matches[0]), 'sha256': sha(matches[0]), 'fresh_local': matches[0].is_relative_to(objects)})
        closures[label] = bindings
    dump(out / 'IMPORT_CLOSURES.json', closures)
    require(source_hashes == {str(p.relative_to(HERE)): sha(p) for p in source_files}, 'Source changed during replay')
    verify_public_package(HERE)
    receipt = {'schema': 't20-original-bearer-bridge-verification-v1', 'status': 'PASS',
      'executor_finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
      'scope': 'New typed A and explicit ABC composition plus models; import-adapted inherited source check only. Official cached imports trusted. No full historical suite or full Mathlib umbrella replay; no metaphysical premise verification.',
      'compiler_sha256': LEAN_HASH, 'approved_dag_manifest_sha256': DAG_HASH,
      'historical_source_sha256': ORIGINAL_HASH, 'derived_imports': IMPORTS,
      'historical_body_byte_identical_after_import': True, 'inherited_readback_matches': len(comparisons),
      'readback_declarations': len(reads), 'false_claims_rejected': 5,
      'source_hashes': source_hashes, 'object_hashes': {p.name: sha(p) for p in objects.glob('*.olean')},
      'official_dependency_packages': packages, 'commands': commands,
      'receipt_hashes': {p.name: sha(p) for p in out.iterdir() if p.is_file()},
      'source_or_dependency_mutations': 'NONE', 'raw_report_source_binding_replay': 'NOT_RUN; public locator projection only', 'network_or_installation': 'NONE'}
    dump(out / 'VERIFICATION.json', receipt)
    print(json.dumps({'status': 'PASS', 'receipt': str(out / 'VERIFICATION.json'), 'declarations': len(reads), 'historical_matches': len(comparisons), 'false_claims_rejected': 5}))

if __name__ == '__main__':
    try: main()
    except Exception as e:
        print('FAIL:', e, file=sys.stderr); sys.exit(1)
