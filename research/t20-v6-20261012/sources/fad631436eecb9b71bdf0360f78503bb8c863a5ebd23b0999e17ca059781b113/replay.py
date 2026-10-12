#!/usr/bin/env python3
"""Portable additive full replay of the exact independently accepted source packet."""
from pathlib import Path
import argparse, datetime, hashlib, json, os, re, subprocess, sys

ROOT = Path(__file__).resolve().parent
CENTRAL_SHA = '2830c05f25dcda6f05617e6da58bac50eb3ea86cc9671f5b8301417bf2a1d295'
CONTROLS_SHA = 'f29de5f526216178d1925281eef35a8f8558dc15810b6f7e40428324963f93e4'
REVIEW_SHA = '59b6578ab2d25b7a5f00ba8cefc1777c23c4b59de95f9ba631c1109c80468de3'
STANDARD_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def checked_path(base, name):
    path = base / name
    if Path(name).is_absolute() or '..' in Path(name).parts or path.is_symlink():
        raise RuntimeError('Unsafe manifest path: ' + name)
    return path

def validate_entries(base, entries):
    for item in entries:
        path = checked_path(base, item['path'])
        if not path.is_file():
            raise RuntimeError('Missing file: ' + str(path))
        if path.stat().st_size != item['size'] or digest(path) != item['sha256']:
            raise RuntimeError('Digest mismatch: ' + str(path))

def verify_packet():
    manifest = json.loads((ROOT / 'PUBLIC_MANIFEST.json').read_text())
    validate_entries(ROOT, manifest['files'])
    expected = {x['path'] for x in manifest['files']} | {'PUBLIC_MANIFEST.json'}
    actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file()}
    if actual != expected:
        raise RuntimeError('Unmanifested or missing packet files: ' + repr(sorted(actual ^ expected)))
    for name, pinned in [('central-v1', CENTRAL_SHA), ('controls-v1', CONTROLS_SHA)]:
        base = ROOT / 'sources' / name
        if digest(base / 'MANIFEST.json') != pinned:
            raise RuntimeError('Frozen manifest changed: ' + name)
        validate_entries(base, json.loads((base / 'MANIFEST.json').read_text())['files'])
    review = ROOT / 'review'
    if digest(review / 'REVIEW_RECEIPT.json') != REVIEW_SHA:
        raise RuntimeError('Independent acceptance receipt changed')
    validate_entries(review, json.loads((review / 'REVIEW_RECEIPT.json').read_text())['artifacts'])
    for row in json.loads((ROOT / 'ORIGINAL_TO_PUBLIC.json').read_text())['copies']:
        if digest(checked_path(ROOT, row['public_path'])) != row['sha256']:
            raise RuntimeError('Original-to-public mismatch: ' + row['public_path'])
    return {'public_manifest_sha256': digest(ROOT / 'PUBLIC_MANIFEST.json'),
            'central_manifest_sha256': CENTRAL_SHA, 'controls_manifest_sha256': CONTROLS_SHA,
            'independent_acceptance_sha256': REVIEW_SHA, 'public_entries': len(manifest['files'])}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-only', action='store_true', help='Check exact packet bytes, without Lean')
    parser.add_argument('--lean', type=Path, help='Official Linux x86_64 Lean 4.19.0 executable')
    parser.add_argument('--mathlib', type=Path, help='Pinned Mathlib source tree with official compiled cache')
    parser.add_argument('--output', type=Path, help='New output directory outside this packet; must not exist')
    args = parser.parse_args()
    binding = verify_packet()
    if args.verify_only:
        print(json.dumps({'status': 'PASS', 'stage': 'packet-integrity', **binding}, indent=2))
        return
    if not args.lean or not args.mathlib or not args.output:
        parser.error('Full replay requires --lean, --mathlib and --output')
    lean, mathlib, output = args.lean.resolve(), args.mathlib.resolve(), args.output.resolve()
    if output.exists():
        raise RuntimeError('Refusing to overwrite existing output: ' + str(output))
    if output == ROOT or ROOT in output.parents:
        raise RuntimeError('Output must be outside the immutable packet')
    pins = json.loads((ROOT / 'DEPENDENCIES.json').read_text())
    if digest(lean) != pins['lean']['binary_sha256']:
        raise RuntimeError('Lean binary is not the pinned official Linux x86_64 executable')
    version = subprocess.check_output([str(lean), '--version'], text=True).strip()
    if '4.19.0' not in version or '6caaee842e94' not in version:
        raise RuntimeError('Lean version/commit mismatch: ' + version)
    if digest(mathlib / 'lake-manifest.json') != pins['mathlib']['lake_manifest_sha256']:
        raise RuntimeError('Mathlib lake-manifest does not match the pinned revision')
    deps = json.loads((ROOT / 'dependencies/SOURCE_MANIFEST.json').read_text())
    validate_entries(mathlib, deps['files'])
    lake = json.loads((mathlib / 'lake-manifest.json').read_text())
    libdirs = [mathlib / '.lake/build/lib/lean'] + [
        mathlib / '.lake/packages' / p['name'] / '.lake/build/lib/lean' for p in lake['packages']]
    if not (libdirs[0] / 'Mathlib.olean').is_file():
        raise RuntimeError('Pinned external compiled Mathlib cache is missing')
    output.mkdir(parents=True)
    (output / 'build').mkdir()
    (output / 'logs').mkdir()
    (output / 'mutants').mkdir()
    env = os.environ.copy()
    env['LEAN_PATH'] = os.pathsep.join(map(str, [output / 'build', *libdirs]))
    central, controls = ROOT / 'sources/central-v1', ROOT / 'sources/controls-v1'
    steps, axioms = [], {}

    def compile_file(path, name, make_object=False, expected_error=None):
        command = [str(lean), '-j1']
        if make_object:
            command += ['-o', str(output / 'build' / (name + '.olean'))]
        command += [str(path)]
        proc = subprocess.run(command, env=env, text=True, stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT, cwd=path.parent)
        folder = 'mutants' if expected_error else 'logs'
        (output / folder / (name + '.log')).write_text(proc.stdout)
        if expected_error:
            if proc.returncode == 0 or expected_error not in proc.stdout:
                raise RuntimeError('Expected diagnostic absent for mutant ' + name)
            status = 'EXPECTED_REJECTION'
        else:
            if proc.returncode != 0 or re.search(r'sorryAx|warning:|error:', proc.stdout):
                raise RuntimeError('Successful-stage compilation failed: ' + name)
            status = 'PASS'
            for theorem, raw in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", proc.stdout):
                used = {x.strip() for x in raw.split(',') if x.strip()}
                if not used <= STANDARD_AXIOMS:
                    raise RuntimeError('Unexpected axiom in ' + theorem + ': ' + repr(used))
                axioms[theorem] = sorted(used)
        steps.append({'name': name, 'source': str(path.relative_to(ROOT)), 'source_sha256': digest(path),
                      'exit_code': proc.returncode, 'status': status,
                      'log': folder + '/' + name + '.log'})
        print(status + ': ' + name, flush=True)

    positive_files = []
    for name in ['DynamicInterlock', 'CoveringCore', 'UnknownRootAttribution']:
        path = central / 'legacy' / (name + '.lean')
        positive_files.append(path); compile_file(path, name, True)
    for name in ['RootImage', 'Availability', 'FixedFamilies', 'Correspondence', 'ImageMinima', 'MapTransport']:
        path = central / (name + '.lean')
        positive_files.append(path); compile_file(path, name, True)
    for name in ['TargetA', 'TargetB', 'TargetC', 'Regression']:
        path = central / 'tests' / (name + '.lean')
        positive_files.append(path); compile_file(path, name)
    path = controls / 'RootCosts.lean'
    positive_files.append(path); compile_file(path, 'RootCosts', True)
    path = controls / 'tests/FamilyDeletionControls.lean'
    positive_files.append(path); compile_file(path, 'FamilyDeletionControls')
    for name in ['IndependentChecks', 'DeletionControls', 'AxiomAudit']:
        path = ROOT / 'review' / (name + '.lean')
        positive_files.append(path); compile_file(path, name)
    for name, diagnostic in [
        ('count_labels_as_roots', 'error: unsolved goals'),
        ('drop_positive_class_size', 'error: omega could not prove the goal'),
        ('drop_positive_fault_budget', 'error: omega could not prove the goal')]:
        compile_file(controls / 'mutation-controls' / (name + '.lean'), name, expected_error=diagnostic)
    for path in positive_files:
        if re.search(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by|extern)\b', path.read_text()):
            raise RuntimeError('Forbidden proof escape token in ' + str(path))
    audit_text = (output / 'logs/AxiomAudit.log').read_text()
    if len(re.findall(r'depends on axioms:', audit_text)) != 50:
        raise RuntimeError('Expected all 50 central theorem axiom reports')
    report = {'status': 'PASS', 'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
              **binding, 'lean_version': version, 'lean_sha256': digest(lean),
              'mathlib_revision': pins['mathlib']['commit'], 'external_source_files_verified': len(deps['files']),
              'fresh_build': True, 'custom_oleans_reused': False,
              'external_compiled_cache_trusted': True, 'central_theorems_axiom_audited': 50,
              'successful_stages': len([x for x in steps if x['status']=='PASS']),
              'expected_rejected_mutants': 3, 'steps': steps, 'axiom_audit': axioms}
    (output / 'REPLAY_RECEIPT.json').write_text(json.dumps(report, indent=2) + '\n')
    print('PASS: exact central targets, Regression, supplement, independent proofs, axiom audit, and three expected mutant diagnostics')

if __name__ == '__main__':
    try:
        main()
    except (RuntimeError, OSError, ValueError, KeyError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        sys.exit(1)
