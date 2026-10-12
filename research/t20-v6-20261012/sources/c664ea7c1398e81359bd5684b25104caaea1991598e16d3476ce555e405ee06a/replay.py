#!/usr/bin/env python3
"""Portable replay of unchanged, reviewed dynamic-V2 history-safety sources.

Run with Python. No archive file is executed as a shell script and no archive
permission bit is trusted. Dependencies are supplied explicitly and hash-pinned.
"""
from pathlib import Path
import argparse, ast, datetime, hashlib, json, os, re, subprocess, sys

ROOT = Path(__file__).resolve().parent
KERNEL = ROOT / 'tranche7-restart/formal/interlock-history-kernel'
MODULES = ['HistoryModel', 'HistoryInvariant', 'HistorySafety', 'HistoryTrace', 'NegativeControls']
FIXTURES = ['Targets', 'MultiEpoch']

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def verify_record(base, rec):
    path = base / rec['path']
    require(path.is_file(), f'Missing required file: {rec["path"]}')
    require(path.stat().st_size == rec['size'] and digest(path) == rec['sha256'],
            f'Hash/size mismatch: {rec["path"]}')

def verify_projection():
    manifest = json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text())
    for rec in manifest['files']:
        verify_record(ROOT, rec)
    mapping = json.loads((ROOT/'ORIGINAL_TO_PUBLIC.json').read_text())
    for rec in mapping['entries']:
        if rec['disposition'] in ['omitted_process_body', 'omitted_generated_object']:
            if rec['disposition'] == 'omitted_process_body':
                require(rec['original_path'].endswith('/PLAN.md'), 'Unexpected process omission')
            else:
                require(rec['original_path'].endswith('.olean') and any(
                    '/'+review+'/replay/build/' in rec['original_path']
                    for review in ['independent-review-v1', 'independent-review-v2']),
                    'Unexpected generated-object omission')
            require(rec['public_path'] is None, 'Omitted body has a public destination')
            require(not (ROOT/rec['original_path']).exists(), 'Omitted body was reintroduced')
        else:
            verify_record(ROOT, {'path': rec['public_path'], 'size': rec['size'], 'sha256': rec['sha256']})
    binding = json.loads((KERNEL/'SOURCE_BINDING.json').read_text())
    for rec in binding['files']:
        verify_record(ROOT, rec)
    return manifest, mapping, binding

def compiler_run(lean, source, log, env, output=None):
    command = [str(lean), '-j1']
    if output is not None:
        command += ['-o', str(output)]
    command.append(str(source))
    result = subprocess.run(command, env=env, text=True, capture_output=True)
    text = result.stdout + result.stderr
    log.write_text(text)
    return result.returncode, text, command

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', required=True, type=Path, help='Official Lean 4.19.0 compiler executable')
    parser.add_argument('--mathlib', required=True, type=Path, help='Mathlib c44e0c8 source root with its compiled cache')
    parser.add_argument('--output', required=True, type=Path, help='A new or empty replay output directory')
    args = parser.parse_args()
    lean, mathlib, output = args.lean.resolve(), args.mathlib.resolve(), args.output.resolve()
    initial_manifest_sha = digest(ROOT/'PUBLIC_MANIFEST.json')
    initial_mapping_sha = digest(ROOT/'ORIGINAL_TO_PUBLIC.json')
    manifest, mapping, binding = verify_projection()
    require(lean.is_file() and digest(lean) == binding['lean_executable_sha256'],
            'Compiler does not match the exact official Lean 4.19.0 executable pin')
    version = subprocess.run([str(lean), '--version'], capture_output=True, text=True, check=True).stdout.strip()
    require('version 4.19.0' in version and '6caaee842e94' in version, 'Unexpected compiler version')
    dependency = json.loads((ROOT/'MATHLIB_SOURCE_PIN.json').read_text())
    for rec in dependency['files']:
        verify_record(mathlib, rec)
    cache = mathlib/'.lake/build/lib/lean'
    require((cache/'Mathlib.olean').is_file(), 'Mathlib compiled cache is absent')
    packages = sorted((mathlib/'.lake/packages').glob('*/.lake/build/lib/lean'))
    require(packages, 'Compiled Mathlib package dependency caches are absent')
    require(not output.exists() or not any(output.iterdir()), 'Output directory must be new or empty')
    output.mkdir(parents=True, exist_ok=True)
    build, logs, controls = output/'build', output/'logs', output/'controls'
    for directory in [build, logs, controls]:
        directory.mkdir()
    env = dict(os.environ)
    env['LEAN_PATH'] = ':'.join(map(str, [build, cache] + packages))
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    (logs/'toolchain.log').write_text(version+'\n'+digest(lean)+'\n')
    source_files = [KERNEL/(name+'.lean') for name in MODULES]
    source_files += [KERNEL/'tests'/(name+'.lean') for name in FIXTURES]
    for source in source_files:
        require(not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide)\b', source.read_text()),
                f'Forbidden proof construct in {source.name}')
    stages = []
    for name in MODULES:
        rc, text, command = compiler_run(lean, KERNEL/(name+'.lean'), logs/(name+'.log'),
                                        env, build/(name+'.olean'))
        require(rc == 0 and not re.search(r'sorryAx|warning:|error:', text), f'Positive compile failed: {name}')
        stages.append({'stage': name, 'exit_code': rc, 'command': command})
    for name in FIXTURES:
        rc, text, command = compiler_run(lean, KERNEL/'tests'/(name+'.lean'), logs/(name+'.log'), env)
        require(rc == 0 and not re.search(r'sorryAx|warning:|error:', text), f'Fixture failed: {name}')
        stages.append({'stage': name, 'exit_code': rc, 'command': command})
    # Consume the original unchanged control generator's literal claim table;
    # do not duplicate, weaken or execute its workspace-dependent launcher.
    tree = ast.parse((KERNEL/'check_controls.py').read_text())
    tables = [ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
              and any(isinstance(target, ast.Name) and target.id == 'claims' for target in node.targets)]
    require(len(tables) == 1 and len(tables[0]) == 7, 'Unexpected original control table')
    control_results = []
    for name, claim in tables[0].items():
        source = controls/(name+'.lean')
        source.write_text('import NegativeControls\nopen InterlockHistory InterlockHistory.Controls\n'
                          +'example : '+claim+' := by decide\n')
        rc, text, command = compiler_run(lean, source, controls/(name+'.log'), env)
        require(rc != 0 and "tactic 'decide' proved that the proposition" in text and 'is false' in text,
                f'Control did not reject its intended false claim: {name}')
        control_results.append({'control': name, 'exit_code': rc, 'expected_false_claim_rejected': True})
    (controls/'RESULTS.json').write_text(json.dumps(control_results, indent=2)+'\n')
    result = subprocess.run([sys.executable, str(KERNEL/'source_replay.py')], env=env,
                            text=True, capture_output=True)
    (logs/'source-replay.json').write_text(result.stdout)
    (logs/'source-replay.stderr').write_text(result.stderr)
    require(result.returncode == 0, 'Accepted-source scenario replay failed')
    scenarios = json.loads(result.stdout)
    require(scenarios['status'] == 'PASS' and len(scenarios['cases']) == 7, 'Unexpected source scenario result')
    for review_name in ['ReviewChallenges', 'ReservationDomain']:
        challenge = KERNEL/'independent-review-v2'/(review_name+'.lean')
        rc, text, command = compiler_run(lean, challenge, logs/(review_name+'.log'), env)
        require(rc == 0 and not re.search(r'sorryAx|warning:|error:', text),
                f'Independent V2 reviewer check failed: {review_name}')
        stages.append({'stage': review_name, 'exit_code': rc, 'command': command})
    require(digest(ROOT/'PUBLIC_MANIFEST.json') == initial_manifest_sha and
            digest(ROOT/'ORIGINAL_TO_PUBLIC.json') == initial_mapping_sha,
            'Public manifest or source mapping changed during replay')
    verify_projection()
    require(digest(ROOT/'PUBLIC_MANIFEST.json') == initial_manifest_sha and
            digest(ROOT/'ORIGINAL_TO_PUBLIC.json') == initial_mapping_sha,
            'Public manifest or source mapping changed during final verification')
    receipt = {
        'status': 'PASS_PORTABLE_SOURCE_REPLAY',
        'completed_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'public_manifest_sha256': initial_manifest_sha,
        'original_to_public_sha256': initial_mapping_sha,
        'source_archive_sha256': mapping['source_archive_sha256'],
        'scientific_candidate_snapshot_sha256': digest(KERNEL/'REVIEW_SNAPSHOT_V2.json'),
        'scientific_review_receipt_sha256': digest(KERNEL/'independent-review-v2/RECEIPT.json'),
        'compiler_sha256': digest(lean), 'compiler_version': version,
        'mathlib_commit': dependency['commit'], 'mathlib_source_files_verified': len(dependency['files']),
        'compiled_cache_used_read_only': True, 'independent_cache_rebuild_claimed': False,
        'compiled_stages': stages, 'false_claim_rejections': len(control_results),
        'accepted_source_scenarios': len(scenarios['cases']),
        'archive_executable_modes_required': False, 'shell_scripts_executed': [],
        'all_projected_inputs_unchanged': True,
        'claim_ceiling': 'Original dynamic V2 conditional finite-history safety, durable cancellation, and stable-epoch goal preservation only.'}
    (output/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print('PASS: 5 modules, 2 fixtures, 7 false-claim controls, 7 original-source scenarios, and both V2 reviewer check files.')
    print('All projected scientific bytes unchanged. No archive executable permissions used.')
    print('Receipt:', output/'REPLAY_RECEIPT.json')

if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('REPLAY FAILED:', error, file=sys.stderr)
        raise SystemExit(1)
