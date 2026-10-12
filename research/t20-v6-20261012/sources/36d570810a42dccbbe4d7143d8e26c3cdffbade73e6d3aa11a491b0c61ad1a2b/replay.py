#!/usr/bin/env python3
"""Verify preserved evidence and replay the two finite moving-objective suites.

The switching note's recorded controls are retained as separately scoped history;
this script verifies their input and correction hashes, not a universal theorem.
"""
from pathlib import Path
import argparse, datetime, hashlib, json, platform, shutil, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parent
AUTHOR='time-varying-square-positivity-20261010'
REVIEW='time-varying-square-positivity-independent-review-20261010'
NOTE='tensor-objective-switching-20261010'
CANDIDATE_SHA='7ffed76cdfb23ee725bd4030c22dd03bb1f66934d885a6800caf260fdb0741bd'
REVIEW_SHA='df593fc0a261960f59510937cd1642417797f654fb1461beed3b11c6416ad998'
NOTE_SHA='4192d9c6bd5020a34b5da8f307531effb8fd7d46a2371f836a77e14d962c9528'
PRIOR_NOTE_SHA='da47c304f36047f4263af46553ecf685fc264c88ec16580c55d9794990fc863c'
RECEIPTS=[(AUTHOR,'AUTHOR_RECEIPT.json'),(REVIEW,'REVIEW_RECEIPT.json'),
 ('tensor-realizability-extension-20261010','AUTHOR_RECEIPT.json'),
 ('coercive-square-positivity-20261010','AUTHOR_RECEIPT.json')]

def require(ok,message):
    if not ok:raise RuntimeError(message)
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def verify_row(base,row):
    p=base/row['path']
    require(p.is_file() and p.stat().st_size==row['bytes'] and digest(p)==row['sha256'],
            'Size/hash mismatch: '+str(p))

def verify():
    rows=load(ROOT/'INTEGRITY.json')['files']
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}
    require(actual=={row['path'] for row in rows}|{'INTEGRITY.json'},'Archive file set differs from integrity manifest')
    require(not any(p.is_symlink() for p in ROOT.rglob('*')),'Symlinks are not allowed')
    for row in rows:verify_row(ROOT,row)
    evidence=ROOT/'evidence'
    require(digest(evidence/AUTHOR/'RESULT.md')==CANDIDATE_SHA,'Wrong reviewed successor')
    require(digest(evidence/REVIEW/'REVIEW.md')==REVIEW_SHA,'Wrong independent review')
    for directory,name in RECEIPTS:
        for row in load(evidence/directory/name)['files']:verify_row(evidence/directory,row)
    review=load(evidence/REVIEW/'REVIEW_RECEIPT.json')
    require(review['status']=='PASS_ORDINARY_INDEPENDENT_REVIEW','Wrong review status')
    require(review['reviewed_candidate_sha256']==CANDIDATE_SHA,'Review/candidate mismatch')
    require(review['author_replay_exact_checks']==23 and review['independent_exact_checks']==36,'Wrong recorded check totals')
    bindings=load(evidence/AUTHOR/'INPUT_BINDINGS.json')
    require(len(bindings)==5,'Expected five direct prerequisite files')
    for row in bindings:
        original=evidence/row['source'];b=original.read_bytes()
        require(len(b)==row['bytes'] and hashlib.sha256(b).hexdigest()==row['sha256'],'Direct source binding differs: '+row['source'])
        require(b==(evidence/AUTHOR/row['copy']).read_bytes()==(evidence/REVIEW/'author-snapshot'/row['copy']).read_bytes(),
                'Inherited frozen copies differ: '+row['source'])
    snapshot=evidence/REVIEW/'author-snapshot'
    for p in snapshot.rglob('*'):
        if p.is_file():require(p.read_bytes()==(evidence/AUTHOR/p.relative_to(snapshot)).read_bytes(),'Author snapshot differs: '+str(p))
    correction=load(evidence/NOTE/'REVIEW_CORRECTION.json')
    require(correction['status']=='CORRECTED_ROOT_NOTE','Wrong switching-note correction state')
    require(digest(evidence/NOTE/'RESULT.md')==correction['corrected_sha256']==NOTE_SHA,'Corrected note binding differs')
    require(digest(evidence/NOTE/'RESULT.before-time-change-correction.md')==correction['prior_sha256']==PRIOR_NOTE_SHA,'Historical note binding differs')
    note_receipt=load(evidence/NOTE/'CONTROL_RECEIPT.json')
    require(note_receipt['kernel_verified'] is False,'Unexpected switching-note kernel claim')
    require(len(note_receipt['inputs'])==4,'Expected four switching-note input anchors')
    for name,sha in note_receipt['inputs'].items():require(digest(evidence/name)==sha,'Switching-note input differs: '+name)
    sources=load(ROOT/'SOURCE_BINDINGS.json')['files']
    require(len(sources)==59,'Expected the 59-file source-bound union')
    for row in sources:verify_row(evidence,row)
    return {'status':'PASS','manifest_bound_files':len(rows),'source_bound_evidence_files':len(sources),
      'direct_successor_prerequisites':5,'complete_source_receipts_verified':4,
      'switching_note_input_anchors':4,'switching_note_correction_and_precorrection_hashes_verified':True,
      'candidate_sha256':CANDIDATE_SHA,'review_sha256':REVIEW_SHA,'corrected_switching_note_sha256':NOTE_SHA}

def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--verify-only',action='store_true')
    ap.add_argument('--output-dir',type=Path,help='A new or empty directory outside this package')
    args=ap.parse_args();before=verify()
    if args.verify_only:print(json.dumps(before,indent=2));return
    import sympy
    require(sympy.__version__=='1.14.0','Reference replay requires SymPy 1.14.0; no dependency installation is performed')
    out=args.output_dir.resolve() if args.output_dir else Path(tempfile.mkdtemp(prefix='t20-moving-replay-'))
    require(out!=ROOT and ROOT not in out.parents,'Replay output must be outside the preserved package')
    if out.exists():require(not any(out.iterdir()),'Replay output directory must be empty')
    else:out.mkdir(parents=True)
    shutil.copytree(ROOT/'evidence',out/'evidence');runs=[]
    specs=[(AUTHOR,'check_controls.py','CONTROL_RESULTS.json',23,5),
           (REVIEW,'check_independent.py','INDEPENDENT_RESULTS.json',36,10)]
    for directory,script,result_name,total,integrity_count in specs:
        cwd=out/'evidence'/directory;command=[sys.executable,script]
        r=subprocess.run(command,cwd=cwd,capture_output=True,text=True,timeout=300)
        stdout=out/(directory+'.stdout.log');stderr=out/(directory+'.stderr.log')
        stdout.write_text(r.stdout,encoding='utf-8');stderr.write_text(r.stderr,encoding='utf-8')
        require(r.returncode==0,'Finite replay failed: '+directory+'; see '+str(stderr))
        result=load(cwd/result_name);frozen=load(ROOT/'evidence'/directory/result_name)
        require(result==frozen and json.loads(r.stdout)==frozen,'Finite results differ from preserved results')
        require(result['status']=='PASS' and result['total_exact_checks']==total,'Wrong fresh total')
        checks=result['checks'];require(len(checks)==total,'Wrong check label count')
        prefixes=('input: ',) if directory==AUTHOR else ('unchanged bytes: ','unchanged hash: ')
        observed_integrity=sum(label.startswith(prefixes) for label in checks)
        require(observed_integrity==integrity_count,'Wrong integrity/algebraic partition')
        require((cwd/result_name).read_bytes()==(ROOT/'evidence'/directory/result_name).read_bytes(),'Fresh result bytes differ')
        runs.append({'directory':directory,'command':command,'exit_code':r.returncode,
          'total_exact_checks':total,'input_integrity_checks':integrity_count,'focused_algebraic_checks':total-integrity_count,
          'result_sha256':digest(cwd/result_name),'stdout_sha256':digest(stdout),'stderr_sha256':digest(stderr),
          'result_matches_preserved_bytes':True})
    after=verify();require(before==after,'Preserved package changed during replay')
    receipt={'status':'PASS_SOURCE_BOUND_FINITE_CONTROL_REPLAY',
     'completed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
     'python':platform.python_version(),'sympy':sympy.__version__,'packet_root':str(ROOT),'replay_root':str(out),
     'integrity_manifest_sha256':digest(ROOT/'INTEGRITY.json'),'integrity_before_and_after':after,'runs':runs,
     'scope':{'author_total':23,'author_algebraic':18,'author_integrity':5,
      'independent_total':36,'independent_algebraic':26,'independent_integrity':10,
      'universal_ordinary_proof_and_review_preserved':True,'uniform_local_window_SOS_domination_required':True,
      'arbitrary_time_varying_coercivity_not_sufficient_for_stated_theorem':True,
      'future_continuation_requires_supplied_energy_schedule':True,
      'switching_note_scope':'Elementary finite-switch corollary and proof-route countercontrol; correction and superseded version retained.',
      'switching_note_historical_arithmetic_reexecuted':False,
      'switching_note_source_and_correction_hashes_freshly_verified':True,
      'active_moment_evolution_source_comparison_included':False,
      'generic_detector_or_measure_reconstruction_implemented':False,
      'formal_kernel_or_Lean_certification':False,'field_novelty_claim':False,'empirical_claim':False,
      'final_integration':False,'T20_closure_claim':False}}
    (out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(receipt,indent=2))

if __name__=='__main__':main()
