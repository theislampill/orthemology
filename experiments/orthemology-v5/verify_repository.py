#!/usr/bin/env python3
"""New repository-native integration adapter; NOT original-packet replay.

0 strict reference+kernel PASS; 1 failure; 2 reference PASS with formal OPEN.
--check checks static composition only and grants no runtime/kernel credit.
Evidence is always written outside the repository in a new directory.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[1]
BASE = 'f50dc1aee52356cc6adbef342387576b02afc124'
PROVENANCE = 'docs/provenance/v5-consolidation'
sys.path.insert(0, str(ROOT / 'source'))
import build_gate as gate

def require(ok, reason):
    if not ok: raise gate.GateError(reason)

def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def validate_ids(rows, expected):
    keys = [r['qualified_id'] for r in rows]
    require(len(keys) == len(set(keys)), 'duplicate origin-scoped ID')
    require(set(keys) == set(expected), 'missing or unexpected origin-scoped ID')

def validate_manifest(repo, manifest):
    require(manifest.get('base_commit') == BASE, 'stale or wrong composition base')
    entries = manifest['files']
    require(bool(entries), 'empty composition manifest')
    expected = set()
    for row in entries:
        rel = row['path']; pp = PurePosixPath(rel)
        require(not pp.is_absolute() and '..' not in pp.parts and '\\' not in rel and ':' not in rel, 'unsafe manifest path')
        require(rel not in expected, 'duplicate manifest member')
        expected.add(rel)
        p = repo / rel
        require(not p.is_symlink() and p.is_file(), 'missing/nonregular source: ' + rel)
        require(not any(q.is_symlink() for q in p.parents if q != repo.parent), 'symlink component')
        require(p.stat().st_size == row['bytes'] and file_hash(p) == row['sha256'], 'source tamper: ' + rel)
    actual = set(manifest['standalone_files'])
    for rel in manifest['managed_roots']:
        root = repo / rel
        require(root.is_dir() and not root.is_symlink(), 'missing managed source root')
        for p in root.rglob('*'):
            require(not p.is_symlink(), 'unexpected symlink')
            if p.is_file(): actual.add(p.relative_to(repo).as_posix())
    actual.discard('experiments/orthemology-v5/SOURCE_MANIFEST.json')
    require(actual == expected, 'omitted manifest member or undeclared file/import collision')
    return len(entries)

def privacy_check(paths):
    local = re.compile(r'/mnt/' + r'data|sandbox' + r':|[A-Za-z]:\\(?:Users|workspace)\\')
    credential = re.compile(r'ghp_' + r'[A-Za-z0-9]{30,}|github_pat_' + r'[A-Za-z0-9_]{40,}|-----BEGIN [A-Z ]*PRIVATE KEY-----')
    for p in paths:
        require(p.suffix.lower() not in {'.zip', '.sqlite', '.db'}, 'archive/private storage on public surface')
        text = p.read_text(encoding='utf-8')
        require(not local.search(text) and not credential.search(text), 'private locator or credential on public surface')

def integrity(check_git=True):
    manifest = gate.strict_json(ROOT / 'SOURCE_MANIFEST.json')
    count = validate_manifest(REPO, manifest)
    records = gate.strict_json(REPO / PROVENANCE / 'SOURCE_MAP.json')
    for name, key in [('THEOREM_LINEAGE.jsonl', 'theorem_ids'), ('CRITICISM_LINEAGE.jsonl', 'criticism_ids')]:
        rows = [json.loads(s) for s in (REPO / PROVENANCE / 'reconciliation' / name).read_text(encoding='utf-8').splitlines()]
        validate_ids(rows, records[key])
    privacy_check([REPO / x['path'] for x in manifest['files'] if x['path'] not in manifest['inherited_updates']])
    if check_git:
        result = subprocess.run(['git', 'merge-base', '--is-ancestor', BASE, 'HEAD'], cwd=REPO, capture_output=True)
        require(result.returncode == 0, 'checkout does not descend from frozen base')
    # This checks the independently labelled compact runtime surface, not 550
    # original packet members. Full original-packet custody is a separate mode.
    runtime = gate.verify_manifest(ROOT / 'source')
    return {'base_commit': BASE, 'files': count, 'manifest_sha256': file_hash(ROOT / 'SOURCE_MANIFEST.json'), 'runtime': runtime}

def baseline_summary(j: dict, process_exit: int) -> dict:
    require(j['scope'] == 'REFERENCE_AND_REQUIRED_FORMAL_TARGETS', 'reference-only is not strict acceptance')
    require(j['exit_code'] == process_exit, 'baseline process/receipt disagreement')
    for name in ('unit_tests','unit_tests_optimised'):
        require(j[name]['ok'] and j[name]['tests'] == 183, 'baseline tests incomplete: '+name)
    sizes = {}
    for name in ('census','census_optimised'):
        require(j[name]['ok'] and j[name]['results']['status'] == 'PASS', 'census failure: '+name)
        total = sum(row['cases'] for row in j[name]['results'].values()
                    if isinstance(row,dict) and 'cases' in row)
        require(total == 335744, 'census coverage changed: '+name)
        sizes[name] = total
    legacy = j['mutations']['results']; newer = j['v4_mutations']['results']
    require(j['mutations']['ok'] and legacy['mutants'] == legacy['detected'] == 6,
            'legacy mutation coverage/failure')
    require(len(legacy['results']) == 6 and all(x['positive_ok'] and x['one_named_test_executed'] and x['detected']
                                               for x in legacy['results']), 'legacy intended failure missing')
    require(j['v4_mutations']['ok'] and newer['mutants'] == 10 and len(newer['results']) == 10 and
            all(x['positive_ok'] and x['detected_by_intended_test'] for x in newer['results']),
            'v4 intended mutation failure missing')
    demo = j['positive_demonstration']['results']
    require(j['positive_demonstration']['ok'] and demo['status'] == 'PASS' and
            demo['positive_cases'] == 12 and demo['reject_all_fails'] is True,
            'positive specification/reject-all control failed')
    require(j['manifest'] == j['post_run_manifest'], 'source mutated during baseline')
    if process_exit == 2:
        require(j['overall'] == 'REFERENCE_PASS_KERNEL_UNAVAILABLE' and
                j['lean']['status'] == 'UNAVAILABLE' and j['lean']['kernel_verified'] is False,
                'exit 2 is not a missing real compiler result')
    else:
        require(process_exit == 0 and j['lean']['kernel_verified'] is True and
                j['overall'] == 'REFERENCE_AND_REQUIRED_FORMAL_TARGETS_PASS',
                'baseline strict gate did not pass')
    return {'normal_tests':183,'optimised_tests':183,'censuses':sizes,
            'legacy_intended_mutants':6,'v4_intended_mutants':10,'positive_scenarios':12,
            'reject_all_fails':True,'kernel_verified':j['lean']['kernel_verified']}

def accept_formal(receipt, code):
    require(receipt.get('exit_code') == code, 'formal receipt/process disagreement')
    if code == 2:
        require(receipt.get('status') == 'KERNEL_UNAVAILABLE' and receipt.get('kernel_verified') is False and
                (receipt['tools'].get('lean') is None or receipt['tools'].get('lake') is None), 'false missing-compiler success')
        return False
    require(code == 0 and receipt.get('status') == 'KERNEL_AND_INVENTORY_PASS' and receipt.get('kernel_verified') is True and
            len(receipt.get('axiom_audit', {})) == 146, 'required compiler/build/inventory failed')
    return True

def verify_result_binding(result, current):
    require(result.get('preflight') == current and result.get('postflight') == current, 'stale or foreign evidence')
    require(result.get('scope') == 'REPOSITORY_NATIVE_REFERENCE_AND_REQUIRED_FORMAL', 'wrong result scope')
    require(result.get('exit_code') in [0, 2], 'not an accepted native result')

def stage_formal(out):
    target = out / 'formal-input'
    require(not target.exists(), 'reused formal staging tree')
    shutil.copytree(ROOT / 'formal_project', target)
    names = ['build_gate.py', 'formal_targets.json', 'lean-toolchain']
    for name in names: shutil.copy2(ROOT / 'source' / name, target / name)
    lean = sorted((ROOT / 'source/lean').glob('*.lean'))
    require(len(lean) == 12, 'original formal source inventory changed')
    for p in lean:
        require(not (target / p.name).exists(), 'duplicate formal owner')
        shutil.copy2(p, target / p.name)
        require((target / p.name).read_bytes() == p.read_bytes(), 'staged formal source changed')
    return target

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    result = {'scope': 'REPOSITORY_NATIVE_REFERENCE_AND_REQUIRED_FORMAL', 'kernel_verified': False,
              'novelty_established': False, 'original_packet_replay': False, 'commands': []}
    out = args.output.resolve() if args.output else None
    if not args.check and (out is None or out.exists() or out == REPO or REPO in out.parents):
        print('A new evidence directory outside the repository is required.'); return 1
    if not args.check: out.mkdir(parents=True)
    def finish(status, code):
        result.update(overall=status, exit_code=code)
        if out and not args.check: (out / 'VERIFICATION.json').write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
        print(json.dumps(result, indent=2)); return code
    def run(label, command, cwd, timeout):
        env = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'PYTHONUTF8': '1'}
        env.pop('PYTHONPATH', None)
        rec = gate.run_bounded(command, cwd, timeout=timeout, output_limit=16*1024*1024, env=env)
        result['commands'].append(gate.write_run(out, label, rec))
        require(rec['status'] == 'EXIT', label + ' did not complete')
        return rec
    try:
        result['preflight'] = integrity()
        if args.check:
            result['scope'] = 'STATIC_COMPOSITION_ONLY'
            return finish('STATIC_IDENTITY_PASS_NO_EXECUTION_CREDIT', 0)
        v4 = run('v4', [sys.executable, '-B', 'verify.py', '--output-dir', str(out / 'v4')], ROOT / 'source', 1600)
        result['v4'] = baseline_summary(gate.strict_json(out / 'v4/VERIFICATION.json'), v4['exit_code'])
        result['probes'] = {}
        for label, pattern, count in [('mathematical', 'test_convergence.py', 9), ('build_staging', 'test_build_staging.py', 3)]:
            for suffix, flags in [('normal', []), ('optimised', ['-O'])]:
                name = label + '_' + suffix
                rec = run(name, [sys.executable, '-B', *flags, '-m', 'unittest', 'discover', '-s', 'experiments', '-p', pattern, '-v'], ROOT, 120)
                match = re.search(r'Ran (\d+) tests?', rec['stderr'])
                require(rec['ok'] and match is not None and int(match[1]) == count, 'probe count/result mismatch: ' + name)
                result['probes'][name] = {'tests': count, 'status': 'PASS', 'kernel_credit': False}
        project = stage_formal(out)
        formal = run('formal', [sys.executable, '-B', 'build.py', '--output', str(out / 'formal')], project, 3000)
        freceipt = gate.strict_json(out / 'formal/FORMAL_RECEIPT.json')
        fpass = accept_formal(freceipt, formal['exit_code'])
        result['formal'] = {'status': freceipt['status'], 'kernel_verified': fpass, 'actual_axiom_footprint': freceipt.get('actual_axiom_union')}
        result['postflight'] = integrity()
        require(result['postflight'] == result['preflight'], 'source mutation during replay')
        result['kernel_verified'] = bool(result['v4']['kernel_verified'] and fpass)
        return finish('NATIVE_REFERENCE_AND_KERNEL_PASS' if result['kernel_verified'] else 'NATIVE_REFERENCE_PASS_KERNEL_OPEN', 0 if result['kernel_verified'] else 2)
    except (gate.GateError, OSError, KeyError, ValueError) as exc:
        result['error'] = str(exc)
        return finish('FAIL', 1)

if __name__ == '__main__': raise SystemExit(main())
