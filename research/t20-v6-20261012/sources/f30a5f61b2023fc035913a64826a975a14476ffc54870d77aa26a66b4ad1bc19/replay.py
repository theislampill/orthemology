#!/usr/bin/env python3
"""Verify the preserved packet, then replay finite controls in a fresh copy.

This verifies finite exact controls and recorded source bindings. It is neither
an implementation of the conditional generic negative-square semidecision nor
a formal-kernel proof of the universal ordinary mathematics.
"""
from pathlib import Path
import argparse
import datetime
import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
AUTHOR = 'tensor-realizability-extension-20261010'
REVIEW = 'tensor-realizability-independent-review-20261010'
EXPECTED_RESULT = '449a28007af5a4d372d95be4d8f961a3ac577e723760f7a352327a05d4b6e17a'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path):
    return json.loads(path.read_text(encoding='utf-8'))

def verify():
    manifest = load(ROOT/'INTEGRITY.json')
    rows = manifest['files']
    expected_paths = {r['path'] for r in rows} | {'INTEGRITY.json'}
    actual_paths = {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    require(actual_paths == expected_paths, 'Archive file set differs from integrity manifest')
    require(not any(p.is_symlink() for p in ROOT.rglob('*')), 'Symlinks are not allowed')
    for row in rows:
        p = ROOT/row['path']
        require(p.stat().st_size == row['bytes'] and digest(p) == row['sha256'],
                'Integrity mismatch: '+row['path'])
    evidence = ROOT/'evidence'
    require(digest(evidence/AUTHOR/'RESULT.md') == EXPECTED_RESULT, 'Wrong candidate')
    for receipt_dir, name in [(AUTHOR, 'AUTHOR_RECEIPT.json'), (REVIEW, 'REVIEW_RECEIPT.json')]:
        receipt = load(evidence/receipt_dir/name)
        for row in receipt['files']:
            p = evidence/receipt_dir/row['path']
            require(p.stat().st_size == row['bytes'] and digest(p) == row['sha256'],
                    'Original receipt mismatch: '+receipt_dir+'/'+row['path'])
    review = load(evidence/REVIEW/'REVIEW_RECEIPT.json')
    require(review['status'] == 'PASS_ORDINARY_INDEPENDENT_REVIEW', 'Wrong review status')
    require(review['reviewed_candidate_sha256'] == EXPECTED_RESULT, 'Review/candidate mismatch')
    require(review['author_replay_exact_checks'] == 332 and review['independent_exact_checks'] == 147,
            'Wrong preserved control counts')
    bindings = load(evidence/AUTHOR/'INPUT_BINDINGS.json')
    require(len(bindings) == 7, 'Expected exactly seven inherited source anchors')
    for row in bindings:
        original = evidence/row['source']
        author_copy = evidence/AUTHOR/row['copy']
        reviewer_copy = evidence/REVIEW/'author-snapshot'/row['copy']
        b = original.read_bytes()
        require(len(b) == row['bytes'] and hashlib.sha256(b).hexdigest() == row['sha256'],
                'Source-anchor mismatch: '+row['source'])
        require(b == author_copy.read_bytes() == reviewer_copy.read_bytes(),
                'Inherited copies differ: '+row['source'])
    for p in (evidence/REVIEW/'author-snapshot').rglob('*'):
        if p.is_file():
            rel = p.relative_to(evidence/REVIEW/'author-snapshot')
            require(p.read_bytes() == (evidence/AUTHOR/rel).read_bytes(),
                    'Reviewer snapshot differs from author: '+str(rel))
    return {'status':'PASS', 'verified_manifest_files':len(rows),
            'inherited_source_anchors':len(bindings), 'candidate_sha256':EXPECTED_RESULT}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--verify-only', action='store_true')
    ap.add_argument('--output-dir', type=Path,
                    help='A new or empty directory outside this extracted package; default: a fresh temporary directory')
    args = ap.parse_args()
    before = verify()
    if args.verify_only:
        print(json.dumps(before, indent=2)); return
    import sympy
    require(sympy.__version__ == '1.14.0',
            'The exact reference replay requires SymPy 1.14.0; no dependency installation is performed')
    out = args.output_dir.resolve() if args.output_dir else Path(tempfile.mkdtemp(prefix='t20-tensor-replay-'))
    require(out != ROOT and ROOT not in out.parents,
            'Replay output must be outside the preserved package')
    if out.exists():
        require(not any(out.iterdir()), 'Replay output directory must be empty')
    else:
        out.mkdir(parents=True)
    shutil.copytree(ROOT/'evidence', out/'evidence')
    runs = []
    specs = [
        (AUTHOR, 'check_controls.py', 'CONTROL_RESULTS.json', 332),
        (REVIEW, 'check_independent.py', 'INDEPENDENT_RESULTS.json', 147),
    ]
    for directory, script, result_name, count in specs:
        cwd = out/'evidence'/directory
        command = [sys.executable, script]
        completed = subprocess.run(command, cwd=cwd, capture_output=True, text=True, timeout=300)
        log_path = out/(directory+'.stdout.log')
        error_path = out/(directory+'.stderr.log')
        log_path.write_text(completed.stdout, encoding='utf-8')
        error_path.write_text(completed.stderr, encoding='utf-8')
        require(completed.returncode == 0, 'Replay failed: '+directory+'; see '+str(error_path))
        generated = load(cwd/result_name)
        expected = load(ROOT/'evidence'/directory/result_name)
        require(generated == expected, 'Generated result differs from preserved result: '+directory)
        require(json.loads(completed.stdout) == expected, 'Replay stdout differs: '+directory)
        require(generated['status'] == 'PASS' and generated['total_exact_checks'] == count,
                'Wrong fresh control count: '+directory)
        require((cwd/result_name).read_bytes() == (ROOT/'evidence'/directory/result_name).read_bytes(),
                'Fresh result bytes differ: '+directory)
        runs.append({'directory':directory,'command':command,'exit_code':completed.returncode,
                     'exact_checks':count,'result_sha256':digest(cwd/result_name),
                     'stdout_sha256':digest(log_path),'stderr_sha256':digest(error_path),
                     'result_matches_preserved_bytes':True})
    after = verify()
    require(before == after, 'Preserved packet changed during replay')
    receipt = {
        'status':'PASS_SOURCE_BOUND_FINITE_CONTROL_REPLAY',
        'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'python':platform.python_version(),'sympy':sympy.__version__,
        'packet_root':str(ROOT),'replay_root':str(out),
        'integrity_manifest_sha256':digest(ROOT/'INTEGRITY.json'),
        'integrity_before_and_after':after,'runs':runs,
        'scope':{
            'author_exact_controls':332,'independent_exact_controls':147,
            'ordinary_proof_review_preserved':True,
            'generic_negative_square_detector_implemented':False,
            'conditional_negative_square_semidecision_only':True,
            'active_general_coercive_extension_included':False,
            'general_coercive_extension_accepted_in_this_packet':False,
            'formal_kernel_or_Lean_certification':False,'empirical_claim':False,
            'final_integration':False,'T20_closure_claim':False,
        },
    }
    receipt_path = out/'REPLAY_RECEIPT.json'
    receipt_path.write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))

if __name__ == '__main__':
    main()
