#!/usr/bin/env python3
"""Bounded joint-model replay using only the already prepared official Lean cache.

No downloads, installations, broad control-suite replay, or dependency writes.
The output must not exist. --check-inputs performs no Lean execution.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
WORKSPACE = HERE

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
        if rel.is_absolute() or '..' in rel.parts: raise RuntimeError('Unsafe package member')
        path = root / rel
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest() != row['sha256'] or path.stat().st_size != row['bytes']:
            raise RuntimeError('Selected source package identity mismatch: ' + row['path'])
    return manifest


ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
LOCAL_FILES = [
    'src/JointFiniteInterpretation.lean', 'tests/Acceptance.lean',
    'tests/RejectedClaims.lean', 'ReadbackAudit.lean', 'ProofReadback.lean',
    'ImportClosure.lean', 'DECLARATIONS.json', 'THEOREMS.json',
    'INPUT_BINDINGS.json', 'reproduce.py', 'harness/test_reproduce.py',
]


def require(value, message):
    if not value:
        raise RuntimeError(message)


def sha(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as source:
        for block in iter(lambda: source.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def text_sha(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()


def dump(path, value):
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')


def verify_bindings(root, entries):
    result = []
    seen = set()
    for item in entries:
        name = item['path']
        require(name not in seen, 'Duplicate input binding: ' + name)
        seen.add(name)
        path = (root / name).resolve()
        require(path.is_relative_to(root.resolve()), 'Input binding escapes root: ' + name)
        require(path.is_file(), 'Missing input binding: ' + name)
        current = {'path': name, 'sha256': sha(path), 'bytes': path.stat().st_size}
        require(current['sha256'] == item['sha256'] and current['bytes'] == item['bytes'],
                'Input binding mismatch: ' + name)
        result.append(current)
    return result


def strip_lean_comments(text):
    """Remove nested Lean comments and strings, preserving line boundaries."""
    output = []
    position = 0
    depth = 0
    string = False
    while position < len(text):
        pair = text[position:position + 2]
        char = text[position]
        if depth:
            if pair == '/-':
                depth += 1; position += 2; output.extend('  '); continue
            if pair == '-/':
                depth -= 1; position += 2; output.extend('  '); continue
            output.append('\n' if char == '\n' else ' ')
        elif string:
            if char == '\\' and position + 1 < len(text):
                output.extend('  '); position += 2; continue
            if char == '"':
                string = False
            output.append('\n' if char == '\n' else ' ')
        elif pair == '/-':
            depth = 1; position += 2; output.extend('  '); continue
        elif pair == '--':
            end = text.find('\n', position)
            if end == -1:
                output.extend(' ' * (len(text) - position)); break
            output.extend(' ' * (end - position)); position = end; continue
        elif char == '"':
            string = True; output.append(' ')
        else:
            output.append(char)
        position += 1
    require(depth == 0 and not string, 'Unclosed Lean comment or string')
    return ''.join(output)


def direct_imports(text):
    return re.findall(r'^\s*import\s+(\S+)\s*$', strip_lean_comments(text), re.M)


def check_authored_source(text):
    code = strip_lean_comments(text)
    require(not re.search(r'\b(sorry|admit|native_decide|sorryAx)\b|^\s*(axiom|opaque)\b', code, re.M),
            'Forbidden authored admission or opaque declaration')


def marker_blocks(text, names, prefix):
    require(names and len(names) == len(set(names)), 'Empty or duplicate requested markers')
    for edge in ['BEGIN', 'END']:
        actual = re.findall(r'^' + prefix + '_' + edge + r' (\S+)$', text, re.M)
        require(actual == names, prefix + ' ' + edge + ' markers differ')
    result = {}
    for name in names:
        pattern = (r'^' + prefix + '_BEGIN ' + re.escape(name) + r'\n(.*?)^' +
                   prefix + '_END ' + re.escape(name) + '$')
        matches = re.findall(pattern, text, re.M | re.S)
        require(len(matches) == 1, 'Missing or duplicate marker block: ' + name)
        result[name] = matches[0].strip()
    return result


def parse_readback(text, names, theorems):
    require(set(theorems) <= set(names), 'Theorem inventory exceeds declaration inventory')
    result = {}
    for name, block in marker_blocks(text, names, 'CONTINUATION').items():
        axiom_match = re.search(r"^'" + re.escape(name) + r"' (.*)$", block, re.M | re.S)
        axes = None
        typ = block
        if axiom_match:
            typ = block[:axiom_match.start()].strip()
            axtext = axiom_match[1].strip()
            if axtext == 'does not depend on any axioms':
                axes = []
            else:
                match = re.fullmatch(r'depends on axioms:\s*\[([^]]*)\]', axtext, re.S)
                require(match, 'Unparseable axiom readback: ' + name)
                axes = sorted(x.strip() for x in match[1].split(',') if x.strip())
            require(set(axes) <= ALLOWED_AXIOMS, 'Unexpected axiom in ' + name)
        require(name not in theorems or axes is not None, 'Missing theorem axiom audit: ' + name)
        require(typ and re.search(re.escape(name) + r'(?![\w.\'])', typ), 'Missing declaration type: ' + name)
        result[name] = {'type': typ, 'type_sha256': text_sha(typ), 'axioms': axes,
                        'axiom_audited': axes is not None, 'raw_block_sha256': text_sha(block)}
    return result


def parse_proofs(text, names, required_calls):
    blocks = marker_blocks(text, names, 'PROOF')
    proofs = {}
    for name, block in blocks.items():
        require(':=' in block, 'Missing printed proof body: ' + name)
        body = block.split(':=', 1)[1].strip()
        require(body and not re.search(r'\b(sorryAx|sorry|native_decide)\b', body),
                'Forbidden or empty printed proof: ' + name)
        kind = re.match(r'^(?:protected\s+)?(theorem|def|abbrev)\b', block)
        require(kind, 'Unrecognized printed declaration kind: ' + name)
        proofs[name] = {'declaration_kind': kind[1], 'declaration_and_body': block, 'sha256': text_sha(block),
                        'body': body, 'body_sha256': text_sha(body)}
    uses = {}
    for call in required_calls:
        pattern = r'(?<![\w.\'])' + re.escape(call) + r'(?![\w.\'])'
        users = [name for name, proof in proofs.items() if re.search(pattern, proof['body'])]
        require(users, 'Required component call missing from printed proof bodies: ' + call)
        uses[call] = users
    return {'proofs': proofs, 'component_uses': uses,
            'scope': 'Exact elaborated definition/theorem body readbacks and term-body constant occurrences, not an axiom-dependency inference. The proofs map contains both kinds, labeled by declaration_kind.'}


def verify_proof_map(proofs, required_map):
    for name, calls in required_map.items():
        require(name in proofs['proofs'], 'Mapped proof missing: ' + name)
        body = proofs['proofs'][name]['body']
        for call in calls:
            pattern = r"(?<![\w.'])" + re.escape(call) + r"(?![\w.'])"
            require(re.search(pattern, body), 'Required mapped component call missing: ' + name + ' -> ' + call)
    return required_map


def verify_cached_objects(bindings):
    result = []
    for item in bindings:
        if item['fresh_local']:
            continue
        path = pathlib.Path(item['object'])
        require(path.is_file() and sha(path) == item['sha256'], 'Cached object binding mismatch: ' + item['module'])
        result.append({'module': item['module'], 'object': str(path), 'sha256': item['sha256'],
                       'bytes': path.stat().st_size, 'fresh_local': False})
    require(result and len(result) == len({item['module'] for item in result}), 'Invalid cached object inventory')
    return result


def validate_rejections(code, text):
    errors = re.findall(r'^[^\n]*?:\d+:\d+: error: (.*?)(?=^[^\n]*?:\d+:\d+: error:|\Z)', text, re.M | re.S)
    require(code != 0 and text.count('error:') == 4 and len(errors) == 4,
            'Rejections must contain exactly four errors and a nonzero exit')
    require(all(re.fullmatch(r"tactic 'decide' proved that the proposition\n.+\nis false\s*", error, re.S)
                for error in errors), 'Rejection is not a semantic decide-false diagnostic')
    return [error.strip() for error in errors]


def bind_imports(text, roots, objects):
    names = re.findall(r'^KERNEL_IMPORT (\S+)$', text, re.M)
    require(names and len(names) == len(set(names)), 'Empty or duplicate imported-object closure')
    bindings = []
    for name in names:
        relative = name.replace('.', '/') + '.olean'
        candidates = [root / relative for root in roots if (root / relative).is_file()]
        require(len(candidates) == 1, 'Missing/ambiguous import object: ' + name)
        path = candidates[0].resolve()
        bindings.append({'module': name, 'object': str(path), 'sha256': sha(path),
                         'bytes': path.stat().st_size, 'fresh_local': path.is_relative_to(objects.resolve())})
    return bindings


def load_names(path):
    names = json.loads(path.read_text())
    require(isinstance(names, list) and names and all(isinstance(n, str) for n in names)
            and len(names) == len(set(names)), 'Invalid declaration inventory: ' + str(path))
    return names


def inventory(here, names, theorems):
    source = strip_lean_comments((here / 'src/JointFiniteInterpretation.lean').read_text())
    found = re.findall(r'^\s*(?:noncomputable\s+)?(?:private\s+)?(def|abbrev|theorem|lemma|inductive|structure)\s+(\w+)', source, re.M)
    declared = ['JointFinite.' + name for _, name in found]
    required_theorems = ['JointFinite.' + name for kind, name in found if kind in {'theorem', 'lemma'}]
    require(set(declared) <= set(names), 'Unlisted named joint declaration: ' + str(sorted(set(declared) - set(names))))
    require(set(required_theorems) <= set(theorems), 'Unlisted joint theorem axiom audit')
    require(set(theorems) <= set(names), 'Theorem outside declaration inventory')
    return {'joint_named_source_declarations': declared, 'joint_named_source_theorems': required_theorems}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', nargs='?', type=pathlib.Path, help='Fresh, nonexistent output directory')
    parser.add_argument('--cache', type=pathlib.Path, required=True, help='Existing pinned official preparation root')
    parser.add_argument('--lean', type=pathlib.Path, required=True, help='Existing official Lean4.19 executable')
    parser.add_argument('--check-inputs', action='store_true', help='Check frozen input hashes only; do not invoke Lean')
    args = parser.parse_args()
    prep = args.cache.resolve()
    lean = args.lean.resolve()
    if args.output is not None:
        require(not args.output.is_symlink(), 'Refusing existing output symlink')
        output = args.output.resolve()
        require(not output.exists(), 'Output already exists; select a fresh path')
        require(output.parent.is_dir(), 'Output parent must exist')
        require(not any(output.is_relative_to(p) for p in [HERE, prep, lean.parent.parent]), 'Output must be outside source, cache and compiler trees')
        output = guarded_output(args.output, [HERE, args.cache, args.lean.parent.parent, lean.parent.parent])
    elif not args.check_inputs:
        raise RuntimeError('A fresh output path is required')
    verify_public_package(HERE)
    contract = json.loads((HERE / 'INPUT_BINDINGS.json').read_text())
    require(contract['schema'] == 't20-joint-finite-input-bindings-v1', 'Unknown input-binding schema')
    bound = verify_bindings(WORKSPACE, contract['inputs'])
    require(lean.is_file() and sha(lean) == contract['compiler_sha256'], 'Compiler binding mismatch')
    require(sha(prep / 'PREPARATION_RECEIPT.json') == contract['preparation_receipt_sha256'],
            'Preparation receipt binding mismatch')
    original = WORKSPACE / contract['historical_source']
    derived = WORKSPACE / contract['derived_source']
    expected = ''.join('import ' + name + '\n' for name in contract['derived_imports']).encode() + original.read_bytes().split(b'\n', 1)[1]
    require(derived.read_bytes() == expected, 'Inherited derivative changed beyond approved import replacement')
    cache_receipt = json.loads((WORKSPACE / contract['cached_closure_receipt']).read_text())
    package_revisions = json.loads((prep / 'PREPARATION_RECEIPT.json').read_text())['source_revisions']
    external_roots = [prep / 'dependencies' / p['name'] / '.lake/build/lib/lean' for p in package_revisions] + [lean.parent.parent / 'lib/lean']
    relocated = []
    for row in cache_receipt['inherited_derived']:
        relative = row['module'].replace('.', '/') + '.olean'
        found = [root / relative for root in external_roots if (root / relative).is_file()]
        require(len(found) == 1, 'Missing or ambiguous bound cache module: ' + row['module'])
        relocated.append({**row, 'object': str(found[0])})
    cache_bindings = verify_cached_objects(relocated)
    if args.check_inputs:
        print(json.dumps({'status': 'PASS', 'scope': 'Frozen bindings and compiler identity only; no Lean execution',
                          'bound_inputs': len(bound), 'bound_cached_objects': len(cache_bindings), 'compiler_sha256': sha(lean)}))
        return
    require(args.output is not None, 'A fresh output path is required')
    out = args.output.resolve()
    require(not out.exists(), 'Output already exists; select a fresh path')
    require(out.parent.is_dir(), 'Output parent must exist')
    sources = {name: sha(HERE / name) for name in LOCAL_FILES}
    names = load_names(HERE / 'DECLARATIONS.json')
    theorems = load_names(HERE / 'THEOREMS.json')
    named_inventory = inventory(HERE, names, theorems)
    modules = contract['compile_modules'] + [{'module': 'JointFiniteInterpretation',
        'path': str((HERE / 'src/JointFiniteInterpretation.lean').relative_to(WORKSPACE)),
        'imports': ['OriginalBearerBridge', 'AnchoredSourceBridge', 'VeracityBoundary']}]
    for module in modules:
        path = WORKSPACE / module['path']
        require(direct_imports(path.read_text()) == module['imports'], 'Direct import mismatch: ' + module['module'])
        check_authored_source(path.read_text())
    for name in LOCAL_FILES:
        if name.endswith('.lean'):
            check_authored_source((HERE / name).read_text())
    proof_source = (HERE / 'ProofReadback.lean').read_text()
    proof_names = re.findall(r'PROOF_BEGIN (\S+)"', proof_source)
    require(proof_names and set(proof_names) <= set(names), 'Proof inventory missing or outside declarations')
    packages = json.loads((prep / 'PREPARATION_RECEIPT.json').read_text())['source_revisions']
    out.mkdir()
    objects = out / 'objects'; objects.mkdir()
    roots = [objects] + [prep / 'dependencies' / p['name'] / '.lake/build/lib/lean' for p in packages]
    all_roots = roots + [lean.parent.parent / 'lib/lean']
    env = os.environ.copy()
    env['LEAN_PATH'] = os.pathsep.join(map(str, roots))
    env['LEAN_NUM_THREADS'] = '1'
    commands = []

    def run(log, arguments, good=True, cwd=HERE):
        command = [str(lean), '-j1', '--trust=0', '--root=' + str(cwd)] + list(map(str, arguments))
        started = datetime.datetime.now(datetime.timezone.utc).isoformat()
        before = time.monotonic()
        result = subprocess.run(command, cwd=cwd, env=env, text=True, capture_output=True, timeout=600)
        output = result.stdout + result.stderr
        (out / log).write_text(output)
        commands.append({'command': command, 'cwd': str(cwd), 'started_utc': started,
                         'elapsed_seconds': round(time.monotonic() - before, 3), 'exit_code': result.returncode,
                         'log': log, 'log_sha256': sha(out / log)})
        dump(out / 'COMMANDS.json', commands)
        if good:
            require(result.returncode == 0 and not re.search(r'\berror:|\bPANIC\b|\bsorryAx\b|declaration uses .sorry.', output),
                    'Compiler check failed: ' + log)
        return result.returncode, output

    try:
        dump(out / 'CACHED_OBJECTS_BEFORE.json', cache_bindings)
        dump(out / 'SOURCE_BINDING_BEFORE.json', {'frozen_inputs': bound, 'local_sources': sources,
                                                 'compiler_sha256': sha(lean)})
        _, version = run('compiler-version.log', ['--version'])
        require('version 4.19.0' in version, 'Unexpected Lean version')
        for module in modules:
            path = WORKSPACE / module['path']
            run(module['module'] + '.log', ['-o', objects / (module['module'] + '.olean'), path], cwd=path.parent)
        run('Acceptance.log', [HERE / 'tests/Acceptance.lean'])
        code, rejected = run('RejectedClaims.log', [HERE / 'tests/RejectedClaims.lean'], good=False)
        rejects = validate_rejections(code, rejected)
        dump(out / 'REJECTIONS.json', {'count': len(rejects), 'diagnostics': rejects,
                                      'scope': 'Four designated semantic false-overclaim tests only'})
        _, readback = run('ReadbackAudit.log', [HERE / 'ReadbackAudit.lean'])
        reads = parse_readback(readback, names, theorems)
        dump(out / 'READBACKS.json', reads)
        dump(out / 'AXIOM_AUDIT.json', {name: reads[name]['axioms'] for name in theorems})
        _, proof_output = run('ProofReadback.log', [HERE / 'ProofReadback.lean'])
        proofs = parse_proofs(proof_output, proof_names, contract['required_component_calls'])
        proofs['required_proof_map'] = verify_proof_map(proofs, contract['required_proof_map'])
        dump(out / 'PROOF_READBACKS.json', proofs)
        _, imports = run('ImportClosure.log', [HERE / 'ImportClosure.lean'])
        closure = bind_imports(imports, all_roots, objects)
        require({b['module'] for b in closure if b['fresh_local']} == {m['module'] for m in modules},
                'Imported local-object closure differs from the five fresh sources')
        require({b['module']: b['sha256'] for b in closure if not b['fresh_local']} ==
                {b['module']: b['sha256'] for b in cache_bindings},
                'Trusted cached import closure differs from the bound inherited closure')
        dump(out / 'IMPORT_CLOSURE.json', closure)
        after = verify_bindings(WORKSPACE, contract['inputs'])
        require(bound == after and sources == {name: sha(HERE / name) for name in LOCAL_FILES},
                'Source or harness changed during replay')
        require(sha(lean) == contract['compiler_sha256'], 'Compiler changed during replay')
        require(all(sha(pathlib.Path(b['object'])) == b['sha256'] for b in closure),
                'Imported object changed during closure binding')
        dump(out / 'SOURCE_BINDING_AFTER.json', {'frozen_inputs': after, 'local_sources': sources,
                                                'compiler_sha256': sha(lean), 'unchanged': True})
        verify_public_package(HERE)
        receipt = {'schema': 't20-joint-finite-verification-v1', 'status': 'PASS',
            'finished_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'scope': 'Relative finite-model verification of the selected formal signature. Reviewed cores rebuilt unchanged; cached official imports remain trusted. No metaphysical actuality, premise warrant, revelation, or general Sixth-refinement claim.',
            'compiler_sha256': sha(lean), 'compiler_version': version.strip(), 'trust_level': 0,
            'frozen_inputs': bound, 'local_sources': sources, 'named_inventory': named_inventory,
            'declarations_read_back': len(reads), 'theorems_axiom_audited': len(theorems),
            'declaration_bodies_read_back': len(proofs['proofs']),
            'theorem_bodies_read_back': sum(p['declaration_kind'] == 'theorem' for p in proofs['proofs'].values()),
            'definition_bodies_read_back': sum(p['declaration_kind'] != 'theorem' for p in proofs['proofs'].values()),
            'required_component_calls': proofs['component_uses'],
            'false_claims_rejected': len(rejects), 'fresh_objects': {p.name: sha(p) for p in objects.glob('*.olean')},
            'imported_objects': len(closure), 'official_dependency_packages': packages,
            'lean_path': env['LEAN_PATH'], 'commands': commands,
            'source_or_dependency_mutations': 'NONE', 'network_or_installation': 'NONE',
            'evidence_hashes': {p.name: sha(p) for p in sorted(out.iterdir()) if p.is_file()}}
        dump(out / 'VERIFICATION.json', receipt)
        print(json.dumps({'status': 'PASS', 'receipt': str(out / 'VERIFICATION.json'),
                          'declarations': len(reads), 'theorems': len(theorems), 'false_claims_rejected': 4}))
    except Exception as error:
        dump(out / 'FAILURE.json', {'status': 'FAIL', 'error': str(error), 'commands': commands})
        raise


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('FAIL:', error, file=sys.stderr)
        sys.exit(1)
