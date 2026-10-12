#!/usr/bin/env python3
"""Fresh-output trust-zero replay of five additive actual-HasJ modules."""
from pathlib import Path
import datetime, hashlib, json, os, subprocess, tempfile
ROOT = Path(__file__).resolve().parent
WORK = ROOT.parent
MODULES = ['JointRecursorCongruence', 'JointRecursorUniqueness', 'JointCanonicalRecursor', 'JointRecursorControls', 'JointRecursorAudit']

def digest(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def record(p):
    p = Path(p)
    return {'path': str(p.relative_to(WORK)), 'sha256': digest(p), 'bytes': p.stat().st_size}

def checked(entries):
    for entry in entries:
        if digest(WORK / entry['path']) != entry['sha256']:
            raise RuntimeError(f"Changed pinned input: {entry['path']}")

def main():
    freeze = json.loads((ROOT / 'validation/CANDIDATE_FREEZE.json').read_text())
    retained = json.loads((ROOT / 'validation/RETAINED_INPUTS.json').read_text())
    checked(freeze['files'])
    checked(retained['files'])
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
        if result.returncode or any(x in result.stdout for x in ['sorryAx', ': error:', ': warning:']):
            raise RuntimeError(f'{module} failed clean trust-zero replay, exit {result.returncode}')
    checked(freeze['files'])
    checked(retained['files'])
    receipt = {
        'status': 'PASS', 'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'lean_version': subprocess.check_output([str(lean), '--version'], text=True).strip(),
        'trust_level': 0, 'fresh_output': str(out.relative_to(WORK)),
        'sources': [record(ROOT / (m + '.lean')) for m in MODULES],
        'compiled': [record(out / (m + '.olean')) for m in MODULES],
        'retained_pin_count': len(retained['files']),
        'retained_pins_verified_before_and_after': True,
        'candidate_freeze': record(ROOT / 'validation/CANDIDATE_FREEZE.json'),
        'log': record(ROOT / 'validation/author-replay.log'),
        'standard_axioms_only': True, 'source_construction_audit': True,
        'actual_source_constructor_audit': True, 'baseline_rebuilt': False,
        'scope': 'Actual HasJ comparison-step derivation from shared recursion laws, dependent-recursor typed-function uniqueness, canonical sectionPoly corollary, and genuinely new-family controls.'
    }
    (ROOT / 'validation/AUTHOR_REPLAY.json').write_text(json.dumps(receipt, indent=2) + '\n')
    print(f'PASS: {len(MODULES)} fresh modules; {len(retained["files"])} retained pins unchanged.')

if __name__ == '__main__':
    main()
