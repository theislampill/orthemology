#!/usr/bin/env python3
"""Portable frozen-correlated-target replay; no inherited packet rebuild."""
import argparse,hashlib,json,os,platform,subprocess,sys
from pathlib import Path
P=Path;ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=P,required=True);args=ap.parse_args();R=P(__file__).resolve().parent;O=args.output_dir.resolve()
if O==R or R in O.parents:raise SystemExit('Output must be outside frozen bundle.')
O.mkdir(parents=True,exist_ok=True);h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();checks=[]
def check(name,value):
 checks.append({'name':name,'passed':bool(value)})
 if not value:raise RuntimeError(name)
M=json.loads((R/'COLLECTION_MANIFEST.json').read_text())
for row in M['files']:
 p=R/row['path'];check('collection payload '+row['path'],p.stat().st_size==row['bytes'] and h(p)==row['sha256'])
check('exact collection file set',{str(p.relative_to(R)) for p in R.rglob('*') if p.is_file()}=={r['path'] for r in M['files']}|{'COLLECTION_MANIFEST.json'})
A=R/'correlated-target-marginal-correction-20261011';V=R/'correlated-target-independent-review-20261011';T=R/'correlated-target-root-check-20261011'
check('supplied final review pin',h(V/'REVIEW.md')=='a59613dd465514cc85d0f7f17a61f23863cae62a280b1bf03b90562f6c67d67f')
for base,freeze_name,result_key,result_name in [(A,'AUTHOR_FREEZE.json','result_sha256','RESULT.md'),(V,'REVIEW_FREEZE.json','review_sha256','REVIEW.md')]:
 f=json.loads((base/freeze_name).read_text());check('frozen result '+result_name,h(base/result_name)==f[result_key]);check('frozen manifest '+base.name,h(base/'MANIFEST.json')==f['manifest_sha256'])
 for row in json.loads((base/'MANIFEST.json').read_text())['files']:
  p=base/row['path'];check('component manifest '+str(p.relative_to(R)),p.stat().st_size==row['bytes'] and h(p)==row['sha256'])
frozen=json.loads((A/'author-run/CHECKS.json').read_text());expected=[r for r in frozen['checks'] if not r['name'].startswith('original binding ')];check('frozen historical author checks 64',len(frozen['checks'])==64);check('portable expected count55',len(expected)==55)
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
def run(script,label,optimized=False,extra=(),expect_success=True):
 cmd=[sys.executable]+(['-O'] if optimized else [])+[str(script)]+list(extra);p=subprocess.run(cmd,capture_output=True,text=True,env=env);(O/(label+'.log')).write_text(p.stdout+p.stderr)
 check(label+' return status',(p.returncode==0) if expect_success else (p.returncode!=0));return p
for mode in ['normal','optimized']:
 op=mode=='optimized';d=O/('author-'+mode);run(A/'verify.py','author-'+mode,op,['--output-dir',str(d)])
 q=json.loads((d/'CHECKS.json').read_text());check('author portable exact checks '+mode,q['check_count']==55 and q['checks']==expected)
 binds=[r for r in q['checks'] if r['name'].startswith(('snapshot binding ','earlier author result ','earlier review result '))];check('author44math11binding '+mode,len(binds)==11 and len(q['checks'])-len(binds)==44)
 d=O/('independent-'+mode);run(V/'check_independent.py','independent-'+mode,op,['--output-dir',str(d)]);q=json.loads((d/'CHECKS.json').read_text());check('independent36 exact controls '+mode,q['count']==36 and all(r['passed'] for r in q['checks']));check('independent frozen receipt exact replay '+mode,(d/'CHECKS.json').read_bytes()==(V/'independent-normal/CHECKS.json').read_bytes())
 p=run(T/'check.py','participating-root-'+mode,op);q=json.loads(p.stdout);check('eight participating root controls '+mode,q['count']==8 and q==json.loads((T/'CHECKS.json').read_text()))
 run(V/'verify_bindings.py','review-bindings-'+mode,op,['--output-dir',str(O/('review-bindings-'+mode))])
check('author normal optimized equality',(O/'author-normal/CHECKS.json').read_bytes()==(O/'author-optimized/CHECKS.json').read_bytes());check('reviewer normal optimized equality',(O/'independent-normal/CHECKS.json').read_bytes()==(O/'independent-optimized/CHECKS.json').read_bytes())
s=(V/'check_independent.py').read_text();neg=[]
for name,old,new,expected_failure in [
 ('h_only_multiplier','phi=d*(b-3*beta)*(y*y-1)/(6*tau)','phi=d*d*(y*y-1)/(6*tau)','horizontal_multiplier_equation'),
 ('fixed_e_derivative','def dy(f):return S.diff(f,y)-b*S.diff(f,e)','def dy(f):return S.diff(f,y)','conditional_y_score_nonzero')]:
 check('unique mutation target '+name,s.count(old)==1);p=O/(name+'.py');p.write_text(s.replace(old,new));r=run(p,'negative-'+name,True,['--output-dir',str(O/('negative-'+name))],False);check('expected negative failure '+name,expected_failure in r.stdout+r.stderr);neg.append({'name':name,'detected':True,'expected_failure':expected_failure})
for row in M['files']:check('payload post-replay unchanged '+row['path'],h(R/row['path'])==row['sha256'])
receipt={'status':'PASS','python':platform.python_version(),'portable_author_mathematical_controls':44,'portable_author_binding_controls':11,'portable_author_total':55,'frozen_historical_total_with_live_bindings':64,'live_original_bindings_not_needed_for_portable_replay':9,'independent_exact_controls':36,'participating_root_controls':8,'negative_controls':neg,'normal_optimized_equal':True,'previous43check_packet_rerun':False,'checks':checks,'scope':'Preservation replay only. Exact controls supplement ordinary proofs; no new geometry, general PDE, formal-kernel, target warrant, integration or closure.'}
(O/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({k:v for k,v in receipt.items() if k!='checks'},indent=2))
