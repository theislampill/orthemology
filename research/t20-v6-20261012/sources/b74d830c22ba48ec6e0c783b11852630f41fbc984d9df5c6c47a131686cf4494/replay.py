"""Run unchanged exact-control scripts with all new output outside this delivery."""
from pathlib import Path
import argparse,sys,subprocess,json,hashlib,platform,os,importlib.util
ROOT=Path(__file__).resolve().parent
# Avoid writing __pycache__ in the frozen delivery.
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('delivery_integrity',ROOT/'verify_delivery.py');v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
p=argparse.ArgumentParser();p.add_argument('--output',required=True,help='New directory outside the extracted delivery');a=p.parse_args();out=Path(a.output).resolve()
if out==ROOT or ROOT in out.parents:raise SystemExit('Output must be outside the delivery directory')
if out.exists():raise SystemExit('Output must be a new directory (will not overwrite existing evidence)')
integrity=v.verify();out.mkdir(parents=True)
import sympy
cases=[('author','reference-bregman-classification-20261011/verify.py',26,'verification.txt','verification-optimized.txt'),('review','reference-bregman-independent-review-20261011/check_independent.py',22,'CONTROLS.json','CONTROLS_OPTIMIZED.json'),('root','reference-geometry-root-controls-20261011/check.py',13,'normal.json','optimized.json')]
runs=[];env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
for role,rel,count,normal,optimized in cases:
    script=ROOT/'payload'/rel
    for mode,flags,original in [('normal',[],normal),('optimized',['-O'],optimized)]:
        cmd=[sys.executable,'-B']+flags+[str(script)]
        cp=subprocess.run(cmd,cwd=out,env=env,text=True,capture_output=True)
        log=out/(role+'-'+mode+'.txt');log.write_text(cp.stdout)
        (out/(role+'-'+mode+'.stderr.txt')).write_text(cp.stderr)
        if cp.returncode:raise RuntimeError(f'{role} {mode} failed ({cp.returncode}); see {out}')
        if role=='author':
            if f'ALL {count} EXACT CHECKS PASSED' not in cp.stdout or sum(line.startswith('PASS ') for line in cp.stdout.splitlines())!=count:raise RuntimeError('Author count mismatch')
        else:
            data=json.loads(cp.stdout)
            if data['count']!=count or len(data['checks'])!=count:raise RuntimeError('Control count mismatch')
        if cp.stdout.encode()!=(script.parent/original).read_bytes():raise RuntimeError('Replay differs from frozen output: '+role+' '+mode)
        runs.append({'role':role,'mode':mode,'count':count,'evidence_class':'exact symbolic/rational controls','returncode':cp.returncode,'matches_frozen_output':True,'command':cmd,'stdout_sha256':hashlib.sha256(cp.stdout.encode()).hexdigest()})
# New gradient scripts contain removable asserts. Raw -O is execution-only.
# The additive AST adapter preserves their exact assertion predicates in both modes.
for mode,flags in [('normal',[]),('optimized',['-O'])]:
    test=subprocess.run([sys.executable,'-B']+flags+[str(ROOT/'assertion_preserving_runner.py'),'--self-test'],cwd=out,env=env,text=True,capture_output=True)
    if test.returncode:raise RuntimeError('Assertion adapter sentinel failed')
    (out/('assertion-adapter-'+mode+'.txt')).write_text(test.stdout)
for role,rel,count in [('gradient-author','reference-gradient-descent-classification-20261011/verify.py',28),('gradient-review','reference-gradient-descent-review-20261011/independent_controls.py',6)]:
    script=ROOT/'payload'/rel
    for adapter in [False,True]:
        for mode,flags in [('normal',[]),('optimized',['-O'])]:
            cmd=[sys.executable,'-B']+flags+([str(ROOT/'assertion_preserving_runner.py')] if adapter else [])+[str(script)]
            cp=subprocess.run(cmd,cwd=out,env=env,text=True,capture_output=True)
            label=role+('-assertions-preserved' if adapter else '-raw')+'-'+mode
            (out/(label+'.txt')).write_text(cp.stdout);(out/(label+'.stderr.txt')).write_text(cp.stderr)
            if cp.returncode:raise RuntimeError(label+' failed')
            if cp.stdout.encode()!=(script.parent/'verification.txt').read_bytes():raise RuntimeError(label+' output mismatch')
            if role=='gradient-author':
                if 'ALL 28 EXACT CONTROLS PASSED' not in cp.stdout or sum(t.startswith('PASS ') for t in cp.stdout.splitlines())!=28:raise RuntimeError('Gradient author count mismatch')
            elif cp.stdout.strip()!='PASS: six independent discriminator groups (exact SymPy).':raise RuntimeError('Gradient review group mismatch')
            runs.append({'role':role,'mode':mode,'assertion_preserving_adapter':adapter,'count':count,'unit':'controls' if role=='gradient-author' else 'discriminator groups','evidence_class':'execution/output only; assertions erased' if mode=='optimized' and not adapter else 'exact symbolic/rational controls, assertions active','returncode':cp.returncode,'matches_frozen_output':True,'command':cmd,'stdout_sha256':hashlib.sha256(cp.stdout.encode()).hexdigest()})
post=v.verify()
receipt={'status':'PASS','integrity':integrity,'post_replay_integrity':post,'python':platform.python_version(),'sympy':sympy.__version__,'runs':runs,'credit':'Prior classification: 26 author controls; 22 independent review controls; 13 root corroborating controls. Gradient successor: 28 author controls and 6 independent review discriminator groups; groups are not individual assertions. Raw -O successor runs erase asserts and have execution-only credit; the separately labelled AST-adapted runs keep assertions active. Normal/-O repetition adds no independent credit; fixture overlap across suites also prevents a summed novelty claim.','numerical_evidence':'None newly generated. These are symbolic/rational, not approximate numerical tests or proof-assistant certification.'}
(out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
