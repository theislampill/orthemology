from pathlib import Path
import os, subprocess, hashlib, json, shutil, sys
from datetime import datetime, timezone

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
sources = [
 ('SelfVerifyingSupport', 'common-observation-audit/snapshot/SelfVerifyingSupport.lean',
  '46643e3bd1194b699ffe67687dfba24761e2eb05ad750bae8b25d2f5fe96470b'),
 ('CommonObservationBoundary', 'root-research/lean/CommonObservationBoundary.lean',
  '8fdc8956bc6176f220dc6ec217aa2d3df5ce0c3c6c3ad2911523bb9198692fb4'),
 ('CommonObservationFiniteActions', 'root-research/lean/CommonObservationFiniteActions.lean',
  'e5b0b4c3152654377a4dfb7146039ccbdb4f4a1f54a89cab5ffae1e9647a8040'),
 ('CompactObservationBoundary', 'compact-observation/lean/CompactObservationBoundary.lean',
  '874ceabb1267306eaff41f28fa4e2450c47d6bc10cdde2e7cee4ce5819dd1b10')]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
lean = BASE / 'toolchain/lean-4.19.0-linux/bin/lean'
assert sha(lean) == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
revision = subprocess.check_output(['git','-C',str(BASE/'toolchain/mathlib4'),'rev-parse','HEAD'],text=True).strip()
assert revision == 'c44e0c8ee63ca166450922a373c7409c5d26b00b'
env = os.environ.copy()
env['LEAN_PATH'] = ':'.join(map(str,[HERE/'build',BASE/'toolchain/mathlib4/.lake/build/lib/lean',
  *sorted((BASE/'toolchain/mathlib4/.lake/packages').glob('*/.lake/build/lib/lean'))]))
rows=[]
for name, relative, expected in sources:
    original=BASE/relative
    assert sha(original)==expected, name
    target=HERE/'source'/f'{name}.lean'
    shutil.copyfile(original,target)
    output=HERE/'build'/f'{name}.olean'
    assert not output.exists(), 'Fresh local outputs required'
    run=subprocess.run([str(lean),'-R',str(HERE/'source'),'-o',str(output),str(target)],env=env,text=True,capture_output=True)
    log=HERE/'logs'/f'{name}.log';log.write_text(run.stdout+run.stderr)
    rows.append({'module':name,'source_sha256':expected,'returncode':run.returncode,'log_sha256':sha(log)})
    print(name,'PASS' if run.returncode==0 else 'FAIL',flush=True)
    if run.returncode or 'sorryAx' in log.read_text():
        print(log.read_text());sys.exit(1)
(HERE/'REPLAY_RESULT.json').write_text(json.dumps({'status':'PASS_FRESH_FOUR_MODULE_REPLAY',
 'timestamp_utc':datetime.now(timezone.utc).isoformat(),'lean_sha256':sha(lean),'mathlib_revision':revision,
 'modules':rows},indent=2)+'\n')
