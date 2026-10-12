#!/usr/bin/env python3
"""Portable preservation replay; never writes frozen component files."""
import argparse,hashlib,json,os,pathlib,platform,shutil,subprocess,sys,tempfile
P=pathlib.Path
ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=P,required=True);ap.add_argument('--original-root',type=P);args=ap.parse_args()
root=P(__file__).resolve().parent;out=args.output_dir.resolve()
if out==root or root in out.parents:raise SystemExit('Choose output outside this frozen bundle.')
out.mkdir(parents=True,exist_ok=True)
h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
checks=[]
def check(name,value):
 checks.append({'name':name,'passed':bool(value)})
 if not value:raise RuntimeError(name)
def verify_manifest(base,name):
 doc=json.loads((base/name).read_text());rows=doc['files'] if isinstance(doc,dict) else doc
 for row in rows:
  p=base/row['path'];check('manifest bytes '+str(p.relative_to(root)),p.stat().st_size==row['bytes']);check('manifest SHA256 '+str(p.relative_to(root)),h(p)==row['sha256'])
 return len(rows)
if (root/'COLLECTION_MANIFEST.json').exists():verify_manifest(root,'COLLECTION_MANIFEST.json')
custody=json.loads((root/'ORIGINAL_CUSTODY.json').read_text())
for row in custody['files']:
 p=root/row['portable_path'];check('portable original '+row['portable_path'],p.stat().st_size==row['bytes'] and h(p)==row['sha256'])
 if args.original_root:
  q=args.original_root/row['path'];check('unchanged workspace original '+row['path'],q.stat().st_size==row['bytes'] and h(q)==row['sha256'])
a=root/'fixed-marginal-endpoint-action-20261011';r=root/'fixed-marginal-paths-independent-review-20261011'
check('frozen review manifest pin',h(r/'REVIEW_MANIFEST.json')=='2e7adb5b2bfb12b90b850760d9d169be4e547471cd28a8b82e940b277af9f9da')
na=verify_manifest(a,'MANIFEST.json');nr=verify_manifest(r,'REVIEW_MANIFEST.json')
freeze=json.loads((a/'AUTHOR_FREEZE.json').read_text());check('author frozen result pin',h(a/'RESULT.md')==freeze['result_sha256']);check('author frozen manifest pin',h(a/'MANIFEST.json')==freeze['manifest_sha256'])
review=json.loads((r/'REVIEW_RECEIPT.json').read_text())
for f,digest in review['author_pins'].items():check('review bound author '+f,h(a/f)==digest)
env=dict(os.environ);env['PYTHONDONTWRITEBYTECODE']='1'
for mode in ('normal','optimized'):
 cmd=[sys.executable]+(['-O'] if mode=='optimized' else [])+[str(a/'verify.py'),'--output-dir',str(out/('author-'+mode)),'--original-root',str(root/'portable-original-inputs')]
 proc=subprocess.run(cmd,capture_output=True,text=True,env=env);(out/('author-'+mode+'.log')).write_text(proc.stdout+proc.stderr);check('author replay '+mode,proc.returncode==0)
 data=json.loads((out/('author-'+mode)/'CHECKS.json').read_text());check('53 distinct author checks '+mode,data['check_count']==53)
 bindings=[x for x in data['checks'] if x['name'].startswith(('snapshot binding ','original binding ','prior frozen '))]
 check('16 binding controls '+mode,len(bindings)==16);check('37 mathematical controls '+mode,len(data['checks'])-len(bindings)==37);check('every author control passes '+mode,all(x['pass'] for x in data['checks']))
check('normal optimized equality',(out/'author-normal/CHECKS.json').read_bytes()==(out/'author-optimized/CHECKS.json').read_bytes())
rd=out/'reviewer-replay';rd.mkdir(exist_ok=True);shutil.copy2(r/'independent_controls.py',rd/'independent_controls.py')
proc=subprocess.run([sys.executable,str(rd/'independent_controls.py')],capture_output=True,text=True,env=env);(out/'reviewer.log').write_text(proc.stdout+proc.stderr);check('reviewer numerical replay',proc.returncode==0)
n=json.loads((rd/'independent_controls_results.json').read_text());check('104 finite fibre numerical cases',n['finite_fibre_cases']==104);check('reviewer numerical status',n['passed']);check('reviewer exact receipt reproduction',(rd/'independent_controls_results.json').read_bytes()==(r/'independent_controls_results.json').read_bytes())
if (root/'SOURCE_CUSTODY.json').exists():
 source=json.loads((root/'SOURCE_CUSTODY.json').read_text())
 for row in source['included_witnesses']:
  p=root/row['portable_path'];check('retained source witness '+row['portable_path'],p.stat().st_size==row['bytes'] and h(p)==row['sha256'])
 for row in source['deliberate_omissions']:
  check('excluded source body '+row['portable_exclusion_path'],not (root/row['portable_exclusion_path']).exists())
 if (root/'source_checks.py').exists():
  proc=subprocess.run([sys.executable,str(root/'source_checks.py'),'--output-dir',str(out/'source-replay')],capture_output=True,text=True,env=env);(out/'source-replay.log').write_text(proc.stdout+proc.stderr);check('source custody/context replay',proc.returncode==0)
if (root/'formal_checks.py').exists():
 proc=subprocess.run([sys.executable,str(root/'formal_checks.py'),'--output-dir',str(out/'formal-custody')],capture_output=True,text=True,env=env);(out/'formal-custody.log').write_text(proc.stdout+proc.stderr);check('formal source/receipt custody only',proc.returncode==0)
# Verify originals again after replay; do not count reruns as independent review.
for row in custody['files']:
 check('portable post-replay unchanged '+row['portable_path'],h(root/row['portable_path'])==row['sha256'])
 if args.original_root:check('workspace post-replay unchanged '+row['path'],h(args.original_root/row['path'])==row['sha256'])
receipt={'status':'PASS','python':platform.python_version(),'author_manifest_files':na,'review_manifest_files':nr,'author_mathematical_controls':37,'author_binding_controls':16,'author_total_controls':53,'author_normal_optimized_equal':True,'reviewer_finite_fibre_numerical_cases':104,'reviewer_numerical_not_proof':True,'original_root_checked':bool(args.original_root),'formal_fresh_kernel_replay_performed':False,'preservation_checks':checks,'scope':'Preservation, portable replay and custody only. No new mathematical/philosophical independent review, formal proof, integration or closure authority.'}
(out/'REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='preservation_checks'},indent=2))
