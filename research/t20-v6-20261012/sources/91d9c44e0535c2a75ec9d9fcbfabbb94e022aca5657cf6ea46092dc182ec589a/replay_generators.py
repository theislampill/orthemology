from pathlib import Path
import json,hashlib,tempfile,shutil,subprocess,datetime
W=Path.cwd();R=W/'hase-certificate-domain-independent-review-20261010';C=W/'hase-certificate-code-validity-20261010';V=Path(tempfile.mkdtemp(prefix='generator-review-',dir=R))
def rec(p):return dict(path=str(p.relative_to(W)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size)
freeze=json.loads((C/'validation/FINAL_FREEZE.json').read_text());frozen={x['path']:x for x in freeze['files']}
inputs=[C/n for n in ['SCHEMA.json','generate_rules.py','generate_image.py','generate_rule_parts.py','generate_controls_release.py']]
for p in inputs:
 assert rec(p)==frozen[str(p.relative_to(W))]
 shutil.copyfile(p,V/p.name)
for p in inputs[1:]:
 run=subprocess.run(['python',str(V/p.name)],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(V/(p.stem+'.log')).write_text(run.stdout);assert run.returncode==0
matches=[]
for p in sorted(V.glob('*.lean')):
 src=C/p.name;assert p.read_bytes()==src.read_bytes(),p.name;assert rec(src)==frozen[str(src.relative_to(W))];matches.append({'module':p.stem,'candidate':rec(src),'regenerated':rec(p)})
assert len(matches)==21
ret=json.loads((C/'validation/RETAINED_SOURCE_CHECKS.json').read_text())
for x in ret['files']+ret['reference_manifests']:assert rec(W/x['path'])==x
receipt={'status':'PASS_GENERATOR_REPRODUCTION_AND_RETAINED_SOURCE_IDENTITIES','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'freeze':rec(C/'validation/FINAL_FREEZE.json'),'inputs':[rec(p) for p in inputs],'matches':matches,'retained_source_checks':rec(C/'validation/RETAINED_SOURCE_CHECKS.json'),'baseline_rebuilt':False,'candidate_mutated':False,'preserved_defective_draft':'generate_controls.py is not executed; generate_controls_release.py is authoritative.'}
(R/'GENERATOR_REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS 21 generated Lean modules and 8 retained source identities')
