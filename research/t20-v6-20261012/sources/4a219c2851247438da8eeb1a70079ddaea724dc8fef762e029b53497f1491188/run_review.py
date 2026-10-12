#!/usr/bin/env python3
"""Read-only replay of bound sources; writes logs only beside this review."""
from pathlib import Path
import hashlib,json,subprocess,sys
HERE=Path(__file__).resolve().parent
WORK=HERE.parent
binding=json.loads((HERE/'REVIEW_BINDINGS.json').read_text())
def validate():
    for item in binding['reviewed_files']:
        data=(WORK/item['path']).read_bytes()
        if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:
            raise RuntimeError('INPUT_CHANGED: '+item['path'])
validate()
rows=[]
positive=(
 ('author','coupled-credal-inquiry-transport-20261011/verify.py'),
 ('root_l','credal-inquiry-root-controls-20261011/check.py'),
 ('root_kernel','credal-inquiry-root-controls-20261011/kernel_vertex_control.py'),
 ('root_unrestricted','credal-inquiry-root-controls-20261011/unrestricted_query_control.py'),
 ('root_zero_branch','credal-inquiry-root-controls-20261011/zero_branch_control.py'),
 ('independent','coupled-credal-inquiry-independent-review-20261011/check_independent.py'))
for optimized in (False,True):
    for name,script in positive:
        cmd=[sys.executable]+(['-O'] if optimized else [])+[str(WORK/script)]
        p=subprocess.run(cmd,text=True,capture_output=True,cwd=WORK)
        if p.returncode:raise RuntimeError(name+' failed: '+p.stdout+p.stderr)
        (HERE/(name+('_optimized' if optimized else '_normal')+'.log')).write_text(p.stdout+p.stderr)
        if name in ('author','independent'):
            result=json.loads(p.stdout)
            if result['status']!='PASS':raise RuntimeError('Nonpassing status')
            count=result.get('checks',result.get('active_checks'))
        else:
            import ast
            result=ast.literal_eval(p.stdout.strip())
            if result['status']!='PASS':raise RuntimeError('Nonpassing status')
            count=result['explicit_checks']
        rows.append({'script':script,'optimized':optimized,'kind':'positive','returncode':p.returncode,'checks':count})
    for name,script,arg,token in (
        ('author','coupled-credal-inquiry-transport-20261011/verify.py','--negative-control','ACTIVE_CHECK_FAILED'),
        ('independent','coupled-credal-inquiry-independent-review-20261011/check_independent.py','--negative','ACTIVE_REVIEW_FAILURE')):
        for negative in ('guard','scalar'):
            cmd=[sys.executable]+(['-O'] if optimized else [])+[str(WORK/script),arg,negative]
            p=subprocess.run(cmd,text=True,capture_output=True,cwd=WORK)
            if p.returncode==0 or token not in p.stderr:raise RuntimeError('Negative did not reject '+name+' '+negative)
            rows.append({'script':script,'optimized':optimized,'kind':'negative_'+negative,'returncode':p.returncode,'failure':p.stderr.splitlines()[-1]})
validate()
for name,script in positive:
    if (HERE/(name+'_normal.log')).read_bytes()!=(HERE/(name+'_optimized.log')).read_bytes():
        raise RuntimeError('Normal/optimized mismatch: '+name)
receipt={'status':'PASS','bound_inputs_unchanged':len(binding['reviewed_files']),'positive_runs':len(positive)*2,'required_negative_rejections':8,'runs':rows,'review_script_sha256':hashlib.sha256((HERE/'check_independent.py').read_bytes()).hexdigest(),'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
(HERE/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
