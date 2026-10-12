#!/usr/bin/env python3
"""Replay unmodified payload checkers; keep generated data outside this delivery."""
import argparse, hashlib, importlib.util, json, os, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE=Path(__file__).resolve().parent
p=argparse.ArgumentParser(); p.add_argument('--output-dir',type=Path,required=True); args=p.parse_args()
out=args.output_dir.resolve()
if out == HERE or HERE in out.parents: raise RuntimeError('Output must be outside the delivery tree')
out.mkdir(parents=True,exist_ok=False)
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def require(c,m):
    if not c: raise RuntimeError(m)
def inventory(): return {str(f.relative_to(HERE)):digest(f) for f in sorted(HERE.rglob('*')) if f.is_file()}
def verify_manifest():
    manifest=json.loads((HERE/'MANIFEST.json').read_text())
    expected={v['path']:v['sha256'] for v in manifest['files']}
    actual=inventory(); actual.pop('MANIFEST.json')
    require(actual==expected,'Delivery manifest mismatch')
    for v in manifest['files']: require((HERE/v['path']).stat().st_size==v['bytes'],'Size mismatch: '+v['path'])
verify_manifest(); before=inventory()
base=HERE/'payload'; author=base/'correction-audit-transport-20261011'; review=base/'correction-audit-transport-independent-review-20261011'; root=base/'correction-audit-root-controls-20261011'
freeze=json.loads((author/'AUTHOR_FREEZE.json').read_text())
for row in freeze['files']: require(digest(author/row['path'])==row['sha256'],'Author freeze mismatch')
receipt=json.loads((review/'REVIEW_RECEIPT.json').read_text())
for key,tree in [('review_files',review),('reviewed_files',author)]:
    for name,sha in receipt[key].items(): require(digest(tree/name)==sha,'Reviewer binding mismatch: '+name)
for name,sha in json.loads((root/'MANIFEST.json').read_text()).items(): require(digest(root/name)==sha,'Root binding mismatch: '+name)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'); executions=[]
for mode,flags in [('normal',[]),('optimized',['-O'])]:
    commands=[('author',[str(author/'verify.py'),'--output-dir',str(out/('author-'+mode))]),('reviewer',[str(review/'check_independent.py'),'--output',str(out/('reviewer-'+mode+'.json'))]),('root-domain',[str(root/'check_domain.py')])]
    for role,argv in commands:
        cmd=[sys.executable,*flags,*argv]; run=subprocess.run(cmd,env=env,text=True,capture_output=True,cwd=out)
        (out/(role+'-'+mode+'.stdout')).write_text(run.stdout); (out/(role+'-'+mode+'.stderr')).write_text(run.stderr)
        executions.append({'role':role,'mode':mode,'returncode':run.returncode,'command':cmd})
        require(run.returncode==0,role+' '+mode+' failed: '+run.stderr)
        print(role,mode,'PASS',flush=True)
for normal,optimized in [('author-normal/CONTROL_RESULTS.json','author-optimized/CONTROL_RESULTS.json'),('reviewer-normal.json','reviewer-optimized.json'),('root-domain-normal.stdout','root-domain-optimized.stdout')]:
    require((out/normal).read_bytes()==(out/optimized).read_bytes(),'Mode output mismatch: '+normal)
# Delivery-only rerun of the supplied floating-point scope discriminator.
import numpy as np
spec=importlib.util.spec_from_file_location('inherited',author/'inputs/gaussian_step.py'); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
def step(m,h): return module.gaussian_step(np.array([m]),np.array([[1.]]),np.array([1.]),np.array([[1.]]),h)
a,b=step(1.,20.),step(2.,20.); far=step(2.,1000.)
checks={'h20_final_mean_collision':np.array_equal(a['mean'],b['mean']),'h20_final_covariance_collision':np.array_equal(a['covariance'],b['covariance']),'h20_diffusion_mean_distinct':not np.array_equal(a['diffusion_mean'],b['diffusion_mean']),'h1000_diffusion_underflow':bool(np.all(far['diffusion_matrix']==0)),'h1000_reaction_underflow':bool(far['reaction_exponent']==0)}
require(all(checks.values()),'Floating scope probe failed')
(out/'floating-scope.json').write_text(json.dumps(checks,indent=2)+'\n')
verify_manifest(); require(inventory()==before,'Delivery changed during replay')
result={'status':'PASS','executions':executions,'payload_and_delivery_unchanged':True,'mode_outputs_identical':True,'author_portable_controls':65,'independent_reviewer_controls':32,'root_domain_controls':9,'floating_scope_checks':checks,'versions':{'python':sys.version,'numpy':np.__version__},'limits':'Repeat modes and packaging reruns do not multiply independent evidential credit. No integration or closure.'}
(out/'REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n'); print('PASS: delivery unchanged; repeat modes identical')
