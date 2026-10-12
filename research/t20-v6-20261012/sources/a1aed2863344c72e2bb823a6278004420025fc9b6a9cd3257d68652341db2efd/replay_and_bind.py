#!/usr/bin/env python3
"""Bind the separate review to the immutable author packet and fresh replay."""
from pathlib import Path
import datetime
import hashlib
import json
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parent
AUTHOR=ROOT.parent/'diffusive-coercive-realizability-20261010'
EXPECTED_RESULT='e8d83152032952fcba757d2d81c4d506a084c9eb75d9112f0e3e0f98c1ca1c75'
EXPECTED_RECEIPT='86c9810865625c09d801607db432fd0b6a08778a80853c89ed65a2e527f6eed2'
sha=lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(AUTHOR/'RESULT.md') == EXPECTED_RESULT
assert sha(AUTHOR/'AUTHOR_RECEIPT.json') == EXPECTED_RECEIPT
author_receipt=json.loads((AUTHOR/'AUTHOR_RECEIPT.json').read_text())
for row in author_receipt['files']:
    path=AUTHOR/row['path']
    assert path.stat().st_size == row['bytes']
    assert sha(path) == row['sha256']

REPLAY=ROOT/'author-replay'/AUTHOR.name
shutil.copytree(AUTHOR,REPLAY,dirs_exist_ok=True)
inherited=[]
for row in json.loads((AUTHOR/'INPUT_BINDINGS.json').read_text()):
    source=AUTHOR.parent/row['source']
    assert sha(source)==row['sha256']
    target=REPLAY.parent/row['source']
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,target)
    inherited.append({'path':str(source.relative_to(ROOT.parent)), 'sha256':sha(source)})

author_run=subprocess.run([sys.executable,str(REPLAY/'check_controls.py')],
                          capture_output=True,text=True)
(ROOT/'author_replay.stdout.log').write_text(author_run.stdout)
(ROOT/'author_replay.stderr.log').write_text(author_run.stderr)
assert author_run.returncode==0, author_run.stderr
results=json.loads((REPLAY/'CONTROL_RESULTS.json').read_text())
integrity=[x for x in results['checks'] if x.startswith(('snapshot hash ', 'unchanged inherited ', 'source hash '))]
algebra=[x for x in results['checks'] if x not in integrity]
assert results['exact_checks']==len(results['checks'])==685
assert len(integrity)==10 and len(algebra)==675

independent_run=subprocess.run([sys.executable,str(ROOT/'independent_controls.py')],
                               capture_output=True,text=True)
(ROOT/'independent_controls.log').write_text(independent_run.stdout+independent_run.stderr)
assert independent_run.returncode==0, independent_run.stderr
independent=json.loads((ROOT/'INDEPENDENT_RESULTS.json').read_text())
assert independent['exact_checks']==133

# Original author and inherited files are rechecked after both fresh executions.
assert sha(AUTHOR/'AUTHOR_RECEIPT.json')==EXPECTED_RECEIPT
for row in author_receipt['files']:
    assert sha(AUTHOR/row['path'])==row['sha256']
for row in inherited:
    assert sha(ROOT.parent/row['path'])==row['sha256']

receipt={
    'schema':'independent-ordinary-mathematical-review-v1',
    'reviewed_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'verdict':'accepted_within_stated_scope',
    'author_packet':AUTHOR.name,
    'author_result_sha256':EXPECTED_RESULT,
    'author_receipt_sha256':EXPECTED_RECEIPT,
    'author_bound_files_verified_before_and_after':len(author_receipt['files']),
    'inherited_originals_verified_before_and_after':inherited,
    'author_fresh_replay':{
        'exit_code':author_run.returncode,
        'total_controls':len(results['checks']),
        'algebraic_controls':len(algebra),
        'integrity_controls':len(integrity),
        'integrity_labels':integrity,
        'replay_control_results_sha256':sha(REPLAY/'CONTROL_RESULTS.json'),
        'original_control_results_sha256':sha(AUTHOR/'CONTROL_RESULTS.json'),
    },
    'independent_fresh_controls':{
        'exit_code':independent_run.returncode,
        'algebraic_controls':independent['exact_checks'],
        'script_sha256':sha(ROOT/'independent_controls.py'),
        'results_sha256':sha(ROOT/'INDEPENDENT_RESULTS.json'),
    },
    'review_sha256':sha(ROOT/'REVIEW.md'),
    'review_boundary':[
        'Entire frozen RESULT.md Sections 1-10, including converse and limitations',
        'Independently derived radial interpolation and zero-safe Riccati controls',
        'Independently checked Fourier differentiation, bounded-class uniqueness and zero-boundary recovery',
        'Putinar-Schmudgen arXiv:0810.0840v1 p24 Theorem25 and following Nussbaum statement',
        'Agrachev et al. arXiv:0806.0734v2 Section4.1.1 pp18-19 Mehler normalization',
        'Inherited result files are checksum-verified; no whole-baseline re-audit claimed',
    ],
    'no_substantive_defect_found':True,
    'limitations':[
        'Ordinary mathematical review, not Lean or formal-kernel verification',
        'Finite algebra controls do not establish the universal analytic theorem',
        'No general coercive-polynomial diffusion extension or finite-test cutoff',
        'No stable or computable inverse, priority conclusion, protected integration, or closure',
    ],
}
(ROOT/'REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
manifest=[]
for path in sorted(ROOT.rglob('*')):
    if path.is_file() and path.name!='MANIFEST.json':
        manifest.append({'path':str(path.relative_to(ROOT)),
                         'bytes':path.stat().st_size,'sha256':sha(path)})
(ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
print('PASS: author frozen16-file binding; fresh author675 algebra +10 integrity; independent133 algebra controls')
print('Original author and four inherited result files unchanged after replay.')
