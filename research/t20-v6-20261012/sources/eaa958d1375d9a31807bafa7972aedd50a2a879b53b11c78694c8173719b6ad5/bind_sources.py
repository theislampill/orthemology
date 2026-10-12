from pathlib import Path
import hashlib,json,shutil
BASE=Path(__file__).resolve().parent
ROOT=BASE.parents[1]
inputs=[
('reconstruction','cooperation-reassessment/SOURCE_ARGUMENT.md','Complete 198-line source reconstruction'),
('prior_warrant','cooperation-reassessment/independent-warrant-review/REVIEW.md','Complete 181-line independent warrant review'),
('MF','targeted-final-loci/causal-action/web/mf_extended.txt','Unique authorial L906–928 in continuous displays'),
('M2A','cooperation-reassessment/islamweb-vol2.txt','Arabic lines8–24 and38–41; intrinsic attributes/concomitance and efficacy context'),
('M2B','cooperation-reassessment/islamweb-item157.txt','Complete four paragraphs'),
('M2C','cooperation-reassessment/islamweb-item158.txt','Opening paragraphs1–5; perfection continuation'),
('M2_body','arabic-volume-study/minhaj-2-3/volume02/body.txt','V02L0109–0115 and0181–0185; electronic locators, no new print mapping'),
('M3_body','arabic-volume-study/minhaj-2-3/volume03/body.txt','V03L0260–0276 continuous context, with truncated intervals redisplayed'),
('Saf_genus','targeted-final-loci/causal-action/receipts/saf2-L0574-L0636.txt','Labelled L0623–0627 genus/token control'),
('T17','recovered-inputs/text/Orthemology_Seventeenth_Research_Final_v1_20261005.txt','P65–68,P74–81,P85,P92; earlier report, not a new primary witness'),
('HP','research-frontier-continuation/causal-abstraction/sources/modified-HPdef.txt','Definition2.1,AC1/AC2(am)/AC3 and cause/part-of-cause distinction; targeted excerpt'),
('abstraction','research-frontier-continuation/causal-abstraction/sources/abstraction.txt','Abstract,introduction,opening model/intervention definitions and targeted locator search; not whole-paper reading'),
]
for n in range(521,525): inputs.append((f'Asbahani_scan_{n}',f'research-frontier/inspection/asbahani/p-{n}.png',f'Direct visual reread; visible printed page{n-100}; modern apparatus distinguished. No new scan acquisition or manuscript collation.'))
records=[]
for ident,rel,scope in inputs:
 p=ROOT/rel
 b=p.read_bytes()
 records.append({'id':ident,'path':str(p.relative_to(ROOT.parent)),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'read_scope':scope,'status':'PRESERVED_INPUT'})
evolving=[
('causal_code','causal-abstraction/causal_transfer.py'),('causal_tests','causal-abstraction/test_causal_transfer.py'),('causal_report','causal-abstraction/RESULT.md'),
('provision_report','provision-identity/RESULT.md'),('provision_code','provision-identity/src/provision_semantics.py'),('provision_tests','provision-identity/src/test_provision_semantics.py'),
('willing_code','intrinsic-willing/src/experiment.py'),('intentions_code','intrinsic-willing/src/intentions.py'),('relational_good_code','intrinsic-willing/src/relational_good.py'),('willing_report','intrinsic-willing/RESULT.md')]
S=BASE/'reviewed-snapshots';S.mkdir(exist_ok=True)
for ident,rel in evolving:
 p=BASE.parent/rel;b=p.read_bytes();s=S/(ident+p.suffix);shutil.copyfile(p,s)
 records.append({'id':ident,'path':str(p.relative_to(ROOT.parent)),'snapshot':str(s.relative_to(ROOT.parent)),'sha256':hashlib.sha256(b).hexdigest(),'bytes':len(b),'read_scope':'Direct source/code/report inspection described in REVIEW.md; evolving snapshot only','status':'REVIEWED_SNAPSHOT_NOT_FUTURE_CHANGES'})
report={'schema':'source-fidelity-review-bindings/1','binding_time_marker_utc':'2026-10-07T21:21:56Z','witness_limit':'Direct retained sources; no fresh network or new print collation claim. Minhaj new power passage is electronic-locator-only. Asbahani printed numbers directly visible in retained scans.','sources':records,'authorization_limit':'Scientific review only; no closure authority or archive modification','research_time_limit':'Snapshot preparation is bookkeeping, not research duration.'}
(BASE/'SOURCE_BINDINGS.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(len(records),'sources bound')
