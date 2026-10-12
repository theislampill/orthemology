#!/usr/bin/env python3
"""Verify a source-bound ordinary-proof packet and replay its finite controls.

This does not implement abstract representation or generic negative-square search.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, platform, shutil, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parent
AUTHOR = 'coercive-square-positivity-20261010'
REVIEW = 'coercive-square-positivity-independent-review-20261010'
PRE_AUTHOR = 'tensor-realizability-extension-20261010'
PRE_REVIEW = 'tensor-realizability-independent-review-20261010'
CANDIDATE_SHA = '204f63e544b1afd9538230f95f8ebfbc613b9847c579dfb901de6d10e40ebb10'
REVIEW_SHA = '1428a820718c4ae109e17bdc6c42827ae9a4faea85c56041572736ecdaffbc96'
PREDECESSOR_SHA = '449a28007af5a4d372d95be4d8f961a3ac577e723760f7a352327a05d4b6e17a'

def require(ok, message):
    if not ok: raise RuntimeError(message)

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def verify_row(base,row):
    p=base/row['path']
    require(p.is_file() and p.stat().st_size==row['bytes'] and digest(p)==row['sha256'],
            'Size/hash mismatch: '+str(p))

def verify():
    rows=load(ROOT/'INTEGRITY.json')['files']
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    expected={row['path'] for row in rows}|{'INTEGRITY.json'}
    require(actual==expected,'Archive file set differs from integrity manifest')
    require(not any(p.is_symlink() for p in ROOT.rglob('*')),'Symlinks are not allowed')
    for row in rows: verify_row(ROOT,row)
    evidence=ROOT/'evidence'
    require(digest(evidence/AUTHOR/'RESULT.md')==CANDIDATE_SHA,'Wrong accepted successor')
    require(digest(evidence/REVIEW/'REVIEW.md')==REVIEW_SHA,'Wrong accepted review')
    require(digest(evidence/PRE_AUTHOR/'RESULT.md')==PREDECESSOR_SHA,'Wrong frozen predecessor')
    receipts=[(AUTHOR,'AUTHOR_RECEIPT.json'),(REVIEW,'REVIEW_RECEIPT.json'),
              (PRE_AUTHOR,'AUTHOR_RECEIPT.json'),(PRE_REVIEW,'REVIEW_RECEIPT.json')]
    for directory,name in receipts:
        for row in load(evidence/directory/name)['files']:
            verify_row(evidence/directory,row)
    review=load(evidence/REVIEW/'REVIEW_RECEIPT.json')
    require(review['status']=='PASS_ORDINARY_INDEPENDENT_REVIEW','Wrong review status')
    require(review['reviewed_candidate_sha256']==CANDIDATE_SHA,'Review/candidate mismatch')
    require(review['author_replay_exact_checks']==761 and review['independent_exact_checks']==394,
            'Wrong recorded control counts')
    source_paths=set()
    for directory in (AUTHOR,REVIEW):
        for row in load(evidence/directory/'INPUT_BINDINGS.json'):
            p=evidence/row['source'];b=p.read_bytes()
            require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],
                    'Direct inherited binding differs: '+row['source'])
            require(b==(evidence/directory/row['copy']).read_bytes(),
                    'Direct inherited copy differs: '+row['source'])
            source_paths.add(row['source'])
    require(len(source_paths)==6,'Expected six distinct direct prerequisite files')
    for author,reviewer in [(AUTHOR,REVIEW),(PRE_AUTHOR,PRE_REVIEW)]:
        snapshot=evidence/reviewer/'author-snapshot'
        for p in snapshot.rglob('*'):
            if p.is_file():
                require(p.read_bytes()==(evidence/author/p.relative_to(snapshot)).read_bytes(),
                        'Reviewer snapshot differs from author: '+str(p.relative_to(evidence)))
    sources=load(ROOT/'SOURCE_BINDINGS.json')['files']
    require(len(sources)==67,'Expected the 67-file source-bound union')
    for row in sources:
        verify_row(evidence,row)
    return {'status':'PASS','manifest_bound_files':len(rows),'source_bound_evidence_files':len(sources),
            'distinct_direct_prerequisite_files':6,'complete_source_receipts_verified':4,
            'candidate_sha256':CANDIDATE_SHA,'review_sha256':REVIEW_SHA,
            'predecessor_sha256':PREDECESSOR_SHA}

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--verify-only',action='store_true')
    ap.add_argument('--output-dir',type=Path,help='A new or empty directory outside this extracted package')
    args=ap.parse_args(); before=verify()
    if args.verify_only:
        print(json.dumps(before,indent=2));return
    import sympy
    require(sympy.__version__=='1.14.0','Reference replay requires SymPy 1.14.0; no installation is performed')
    out=args.output_dir.resolve() if args.output_dir else Path(tempfile.mkdtemp(prefix='t20-coercive-replay-'))
    require(out!=ROOT and ROOT not in out.parents,'Replay output must be outside the preserved package')
    if out.exists():require(not any(out.iterdir()),'Replay output directory must be empty')
    else:out.mkdir(parents=True)
    shutil.copytree(ROOT/'evidence',out/'evidence')
    runs=[]
    for directory,script,result_name,count in [
        (AUTHOR,'check_controls.py','CONTROL_RESULTS.json',761),
        (REVIEW,'check_independent.py','INDEPENDENT_RESULTS.json',394)]:
        cwd=out/'evidence'/directory;command=[sys.executable,script]
        r=subprocess.run(command,cwd=cwd,capture_output=True,text=True,timeout=300)
        stdout=out/(directory+'.stdout.log');stderr=out/(directory+'.stderr.log')
        stdout.write_text(r.stdout,encoding='utf-8');stderr.write_text(r.stderr,encoding='utf-8')
        require(r.returncode==0,'Finite replay failed: '+directory+'; see '+str(stderr))
        result=load(cwd/result_name);frozen=load(ROOT/'evidence'/directory/result_name)
        require(result==frozen and json.loads(r.stdout)==frozen,'Finite results differ from preserved results: '+directory)
        require(result['status']=='PASS' and result['total_exact_checks']==count,'Wrong fresh check count')
        require((cwd/result_name).read_bytes()==(ROOT/'evidence'/directory/result_name).read_bytes(),
                'Fresh result bytes differ from preserved result')
        runs.append({'directory':directory,'command':command,'exit_code':r.returncode,
                     'exact_checks':count,'result_sha256':digest(cwd/result_name),
                     'stdout_sha256':digest(stdout),'stderr_sha256':digest(stderr),
                     'result_matches_preserved_bytes':True})
    after=verify();require(before==after,'Preserved package changed during replay')
    receipt={'status':'PASS_SOURCE_BOUND_FINITE_CONTROL_REPLAY',
        'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'python':platform.python_version(),'sympy':sympy.__version__,
        'packet_root':str(ROOT),'replay_root':str(out),
        'integrity_manifest_sha256':digest(ROOT/'INTEGRITY.json'),
        'integrity_before_and_after':after,'runs':runs,
        'scope':{'author_exact_controls':761,'independent_exact_controls':394,
            'ordinary_universal_proof_and_independent_review_preserved':True,
            'classical_primary_representation_theorems_imported':True,
            'representation_theorems_implemented_by_finite_controls':False,
            'generic_negative_square_detector_implemented':False,
            'conditional_negative_square_semidecision_only':True,
            'general_coercive_extension_accepted_in_this_packet':True,
            'formal_kernel_or_Lean_certification':False,'field_novelty_claim':False,
            'empirical_claim':False,'final_integration':False,'T20_closure_claim':False}}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
