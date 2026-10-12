#!/usr/bin/env python3
"""Exact retained-object replay of only the frozen closed-Church additions.
No prerequisite rebuild, historical receipt overwrite, or source-hash rebinding.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
STRUCTURAL = 'hase-church-structural-20261010'
IDENTITY = 'hase-closed-church-identity-20261010'
REVIEW = 'hase-closed-church-completeness-review-20261010'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
read = lambda p: json.loads(p.read_text())


def load_predecessor(args):
    # Authenticate the module before importing/executing its verification helpers.
    c = read(ROOT / 'REUSE_CONTRACT.json')['dependencies']['extractor']
    assert sha(args.extractor_archive) == c['archive_sha256'], 'Wrong extractor archive'
    import zipfile
    with zipfile.ZipFile(args.extractor_archive) as z:
        name = c['root'] + '/replay_extractor.py'
        assert z.read(name) == (args.extractor / 'replay_extractor.py').read_bytes()
    spec = importlib.util.spec_from_file_location('frozen_extractor_replay', args.extractor / 'replay_extractor.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def verify(args, previous):
    c = read(ROOT / 'REUSE_CONTRACT.json')
    counts = {'addition': previous.verify_index(ROOT)}
    # The current ZIP is optionally verified; its public SHA must be checked externally.
    if args.archive:
        counts['addition_archive_entries'] = previous.archive_matches(args.archive, ROOT, sha(args.archive))
    for key in ['v3', 'continuation', 'extractor']:
        dep = c['dependencies'][key]
        root = getattr(args, key)
        counts[key] = previous.verify_index(root, dep['index_sha256'])
        counts[key + '_archive_entries'] = previous.archive_matches(getattr(args, key + '_archive'), root, dep['archive_sha256'])
    for row in c['frozen_manifests'] + [c['review_receipt']]:
        assert sha(previous.inside(ROOT, row['path'])) == row['sha256'], row['path']
    omissions = {r['path']: r for r in c['new_snapshot_omissions']}
    for name in [STRUCTURAL, IDENTITY, REVIEW]:
        for row in read(ROOT / name / 'MANIFEST.json')['files']:
            key = name + '/' + row['path']
            if key in omissions:
                assert row['path'].endswith('.olean')
                assert omissions[key]['sha256'] == row['sha256'] and omissions[key]['bytes'] == row['bytes']
                assert not (ROOT / key).exists()
            else:
                path = previous.inside(ROOT / name, row['path'])
                assert sha(path) == row['sha256'], str(path)
    bindings = []
    locations = {'addition': ROOT, 'v3': args.v3, 'continuation': args.continuation, 'extractor': args.extractor}
    for row in c['source_and_evidence_bindings']:
        m = row['mapping']
        path = args.lean if m['location'] == 'lean' else previous.inside(locations[m['location']], m['path'])
        assert sha(path) == row['sha256'] and path.stat().st_size == row['bytes'], row['path']
        bindings.append({'original_path': row['path'], 'sha256': row['sha256'], 'resolved': str(path)})
    # This verifies compiler/source/package pins and the 92 baseline + 2 author scalar objects.
    # It does NOT invoke predecessor compilation, Python tests, or scientific campaigns.
    inherited = previous.verify(args)
    extra = []
    source_bindings = {r['original_path']: r for r in bindings}
    for row in c['extra_runtime_objects']:
        path = getattr(args, row['group']) / (row['module'] + '.olean')
        assert sha(path) == row['sha256'] and path.stat().st_size == row['bytes'], str(path)
        assert source_bindings[row['source_path']]['sha256'] == row['source_sha256'], row['source_path']
        extra.append({**row, 'path': str(path)})
    assert len(inherited['objects']) == 94 and len(extra) == 7
    # Bind every repeated reviewer source literally to the frozen author source.
    for module in c['fresh_compilation_scope']['author']:
        name = STRUCTURAL if module.startswith('HasE') else IDENTITY
        assert (ROOT / name / (module + '.lean')).read_bytes() == (ROOT / REVIEW / 'sources' / (module + '.lean')).read_bytes()
    return {'counts': counts, 'inherited': inherited, 'bindings': bindings, 'extra_runtime_objects': extra,
            'unique_project_runtime_objects': 101, 'historical_input_bindings': c['historical_review_binding_count'],
            'historical_object_records_not_replayed': len([r for r in c['inherited_object_omissions'] if r['classification'] == 'historical_evidence_not_replayed'])}


def coverage(before):
    mapping = {r['original_path']: Path(r['resolved']) for r in before['bindings']}
    source = mapping['hase-imported-compiler-transport-20261010/sources/ExtensionalRepairSyntax.lean'].read_text()
    main = source.split('mutual', 1)[1].split('\nend', 1)[0]
    grammar = {}
    for name in ['CtxE', 'FormE', 'HasE']:
        body = main.split('inductive ' + name, 1)[1].split('  inductive ', 1)[0]
        grammar[name] = re.findall(r'^\s*\|\s+(\w+)\s*:', body, re.M)
    assert [len(grammar[x]) for x in ['CtxE', 'FormE', 'HasE']] == [2, 7, 20]
    expected = sum(grammar.values(), [])
    ports = []
    for file, thm in [('HasEStructuralBase.lean', 'form_trename'), ('HasEStructuralRename.lean', 'form_rename')]:
        txt = (ROOT / REVIEW / 'sources' / file).read_text().split('theorem ' + thm, 1)[1].split('\ntheorem ', 1)[0]
        branches = re.findall(r'^\s*\|\s*@?(\w+)', txt, re.M)
        assert set(expected) <= set(branches)
        ports.append({'file': file, 'theorem': thm, 'constructors_covered': expected, 'branch_labels': branches, 'omitted': []})
    result = {'status': 'PASS', 'actual_grammar': grammar, 'ports': ports}
    assert result == read(ROOT / REVIEW / 'SOURCE_CONSTRUCTOR_COVERAGE.json')
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for flag in ['v3', 'v3-archive', 'continuation', 'continuation-archive', 'extractor', 'extractor-archive',
                 'lean', 'packages', 'prerequisite-objects', 'closed-objects', 'author-extractor-objects',
                 'reviewer-closed-objects', 'reviewer-extractor-objects']:
        parser.add_argument('--' + flag, required=True, type=Path)
    parser.add_argument('--archive', type=Path, help='Optional exact-byte check against this supplement ZIP; independently check its published SHA-256.')
    parser.add_argument('--out', type=Path)
    parser.add_argument('--verify-only', action='store_true')
    args = parser.parse_args()
    for name, value in vars(args).items():
        if isinstance(value, Path): setattr(args, name, value.resolve())
    previous = load_predecessor(args)
    before = verify(args, previous)
    result_coverage = coverage(before)
    if args.verify_only:
        print(json.dumps({'status': 'PASS_EXACT_RETAINED_PREREQUISITES', 'verified_project_objects': 101,
                          'source_constructor_coverage': [2, 7, 20], 'counts': before['counts']}, indent=2))
        return
    assert args.out and not args.out.exists(), 'Use a new, absent output directory'
    for root in [ROOT, args.v3, args.continuation, args.extractor, args.packages, args.lean.parent.parent,
                 args.prerequisite_objects, args.closed_objects, args.author_extractor_objects,
                 args.reviewer_closed_objects, args.reviewer_extractor_objects]:
        assert not args.out.is_relative_to(root), 'Output must be outside every frozen input tree'
    args.out.mkdir(parents=True)
    c = read(ROOT / 'REUSE_CONTRACT.json')
    records = []
    copies = []
    # Import only exact rehashed project objects, in separate author/reviewer environments.
    # No broad historical fresh-lib directory can shadow a newly compiled addition.
    baseline = args.out / 'baseline-lib'; baseline.mkdir()
    author_prereq = args.out / 'author-prerequisite-lib'; author_prereq.mkdir()
    reviewer_prereq = args.out / 'reviewer-prerequisite-lib'; reviewer_prereq.mkdir()
    def copy_object(src, dest, digest):
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)
        assert sha(dest) == digest
        copies.append({'path': str(dest), 'sha256': digest})
    for row in before['inherited']['objects']:
        dest = author_prereq if row['module'] in {'ClosedProofCanonicalisation', 'ClosedScalarInstances'} else baseline
        copy_object(Path(row['path']), dest / Path(*row['module'].split('.')).with_suffix('.olean'), row['sha256'])
    for row in before['extra_runtime_objects']:
        dest = author_prereq if row['group'] == 'author_extractor_objects' else reviewer_prereq
        copy_object(Path(row['path']), dest / (row['module'] + '.olean'), row['sha256'])
    packages = [args.packages / p['name'] / '.lake/build/lib/lean' for p in before['inherited']['pinned_packages']]
    packages = [p for p in packages if p.is_dir()]
    # Lean resolves the first library root containing a namespace as a unit.
    # Our two exact Mathlib objects create that namespace, so fill its other
    # entries from the pinned external build without replacing either object.
    mathlib = args.packages / 'mathlib' / '.lake/build/lib/lean/Mathlib'
    assert mathlib.is_dir()
    def fill_external_namespace(source, target):
        for entry in source.iterdir():
            dest = target / entry.name
            if not dest.exists():
                dest.symlink_to(entry, target_is_directory=entry.is_dir())
            elif entry.is_dir() and dest.is_dir():
                fill_external_namespace(entry, dest)
    fill_external_namespace(mathlib, baseline / 'Mathlib')
    for row in copies: assert sha(Path(row['path'])) == row['sha256']
    logpath = args.out / 'REPLAY.log'
    with logpath.open('w') as combined:
        for role, prereq in [('author', author_prereq), ('reviewer', reviewer_prereq)]:
            stage = args.out / role; stage.mkdir()
            lib = args.out / (role + '-lib'); lib.mkdir()
            env = {**os.environ, 'LEAN_PATH': ':'.join(map(str, [lib, prereq, baseline] + packages))}
            for module in c['fresh_compilation_scope'][role]:
                if role == 'author': source = ROOT / (STRUCTURAL if module.startswith('HasE') else IDENTITY) / (module + '.lean')
                else:
                    source = ROOT / REVIEW / 'sources' / (module + '.lean')
                    if not source.exists(): source = ROOT / REVIEW / (module + '.lean')
                target = stage / source.name; shutil.copy2(source, target)
                assert sha(target) == sha(source)
                code = previous.clean_code(target.read_text())
                assert not re.findall(r'\b(?:sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b', code), module
                output = lib / (module + '.olean')
                command = [str(args.lean), '--trust=0', '-o', str(output), str(target)]
                started = time.monotonic()
                p = subprocess.run(command, env=env, cwd=stage, capture_output=True, text=True, timeout=600)
                text = p.stdout + p.stderr
                log = stage / (module + '.log'); log.write_text(text)
                combined.write('$ ' + ' '.join(command) + '\n' + text); combined.flush()
                assert p.returncode == 0, (role, module, text)
                assert not any(x in text for x in ['error:', 'warning:', 'sorryAx', 'Lean.ofReduceBool']), (module, text)
                allowed = {'propext', 'Quot.sound', ''} | (set() if module.startswith('HasE') else {'Classical.choice'})
                for match in re.findall(r'depends on axioms:\s*\[([^\]]*)\]', text, re.S):
                    assert set(re.sub(r'\s+', '', match).split(',')) <= allowed, (module, match)
                historical = ROOT / REVIEW / 'validation' / (module + '.log')
                assert log.read_bytes() == historical.read_bytes(), ('Changed audited output', role, module)
                records.append({'role': role, 'module': module, 'source_sha256': sha(target),
                                'object_sha256': sha(output), 'log_sha256': sha(log), 'command': command,
                                'exit_code': p.returncode, 'trust_zero': True,
                                'historical_log_byte_identical': True, 'seconds': round(time.monotonic() - started, 3)})
                print(role, module, 'PASS', flush=True)
    for row in copies: assert sha(Path(row['path'])) == row['sha256']
    assert verify(args, previous) == before, 'Frozen inputs or prerequisites changed during replay'
    receipt = {'status': 'PASS_FRESH_EXTRACTED_CLOSED_CHURCH_ADDITION_REPLAY', 'verification': before,
               'reused_checked_project_objects': 101, 'baseline_compilations': 0, 'predecessor_campaigns': 0,
               'author_trust_zero_compilations': 6, 'reviewer_trust_zero_compilations': 9,
               'all_15_logs_byte_identical_to_frozen_review': True, 'records': records,
               'source_constructor_coverage': result_coverage, 'distinct_author_executable_guards': 5,
               'distinct_reviewer_executable_guards': 6, 'runtime_counts': [2, 2, 3, 2],
               'copied_runtime_objects_rehashed_before_and_after': True,
               'external_mathlib_namespace_overlay': 'Pinned external build links; two verified local Mathlib objects preserved',
               'all_frozen_inputs_reverified_after': True, 'log_sha256': sha(logpath),
               'source_only_fresh_machine_rebuild_certified': False,
               'protected_repository_mutation': False, 'integration': False, 'T20_closure': False,
               'limitations': c['limitations']}
    (args.out / 'REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print('PASS: 101 checked objects reused; 6 author + 9 reviewer compilations; no baseline or campaign rerun.')

if __name__ == '__main__':
    main()
