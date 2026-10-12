#!/usr/bin/env python3
"""Fresh-output, trust-zero replay of only the ten additive modules."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, sys, tempfile
ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent
MODULES = ['JointInductionSupport', 'JointInductionInitiality', 'JointInductionSectionCorollaries', 'JointInductionUniformSection', 'JointInductionComputationLaws', 'JointInductionSectionApplication', 'JointInductionLaws', 'JointInductionControls', 'JointInductionRawBoundary', 'JointInductionAudit']

def digest(path):
    p = Path(path)
    return hashlib.sha256(p.read_bytes()).hexdigest()

def checked(entries):
    for item in entries:
        p = WORK / item['path']
        actual = digest(p)
        if actual != item['sha256']:
            raise RuntimeError(f"Changed pinned input: {item['path']}")

def record(path):
    p = Path(path)
    return {'path': str(p.relative_to(WORK)), 'sha256': digest(p), 'bytes': p.stat().st_size}

def main():
    frozen = json.loads((ROOT / 'validation/CANDIDATE_FREEZE.json').read_text())
    retained = json.loads((ROOT / 'validation/RETAINED_INPUTS.json').read_text())
    checked(frozen['files'])
    checked(retained['sources'])
    checked(retained['objects'])
    # Use the retained search path; prefix a new directory so no candidate object is reused.
    raw = subprocess.check_output(['bash', '-c', f'source "{ROOT}/env.sh"; printf "\\n__PATH__%s" "$LEAN_PATH"'], text=True)
    lean_path = raw.split('__PATH__', 1)[1]
    out = Path(tempfile.mkdtemp(prefix='fresh-output-', dir=ROOT / 'validation'))
    env = os.environ.copy()
    env['LEAN_PATH'] = str(out) + ':' + ':'.join(x for x in lean_path.split(':') if Path(x).resolve() != (ROOT / 'validation').resolve())
    lean = WORK / '.toolchains/lean-4.19.0-linux/bin/lean'
    logs = []
    for module in MODULES:
        cmd = [str(lean), '--trust=0', '-o', str(out / (module + '.olean')), str(ROOT / (module + '.lean'))]
        result = subprocess.run(cmd, cwd=WORK, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        logs.append('$ ' + ' '.join(cmd) + '\n' + result.stdout)
        (ROOT / 'validation/author-replay.log').write_text('\n'.join(logs))
        print(result.stdout, end='')
        if result.returncode:
            raise RuntimeError(f'{module} exited {result.returncode}')
        if 'sorryAx' in result.stdout or ': error:' in result.stdout or ': warning:' in result.stdout:
            raise RuntimeError(f'{module} produced an error, warning or admitted proof')
    checked(frozen['files'])
    checked(retained['sources'])
    checked(retained['objects'])
    log = '\n'.join(logs)
    receipt = {
        'status': 'PASS', 'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'lean_version': subprocess.check_output([str(lean), '--version'], text=True).strip(),
        'trust_level': 0, 'fresh_output': str(out.relative_to(WORK)),
        'sources': [record(ROOT / (x + '.lean')) for x in MODULES],
        'compiled': [record(out / (x + '.olean')) for x in MODULES],
        'retained_source_count': len(retained['sources']), 'retained_object_count': len(retained['objects']),
        'retained_pins_verified_before_and_after': True,
        'candidate_freeze': record(ROOT / 'validation/CANDIDATE_FREEZE.json'),
        'log': record(ROOT / 'validation/author-replay.log'),
        'standard_axioms_only': True, 'source_construction_audit': True,
        'actual_source_constructor_audit': False, 'baseline_rebuilt': False,
        'scope': 'Actual Joint dependent induction zero/successor computation, explicit comparison-family extensionality, new-family scope controls, and typed-versus-Raw successor separation.'
    }
    (ROOT / 'validation/AUTHOR_REPLAY.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'PASS: 10 fresh modules; {len(retained["sources"])} source pins and {len(retained["objects"])} object pins unchanged.')

if __name__ == '__main__':
    main()
