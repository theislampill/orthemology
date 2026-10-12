"""Adversarial source and semantic verification tests; never changes the delivered tree."""
from pathlib import Path
import importlib.util,tempfile,shutil,json,copy,contextlib,io
BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('supplement_tested_verifier',BASE/'historical_coverage/verify_supplement.py')
v=importlib.util.module_from_spec(spec);spec.loader.exec_module(v)
results=[]
def run():
 with contextlib.redirect_stdout(io.StringIO()):v.main()
def reject(name,expected,mode):
 try:run()
 except (RuntimeError,FileNotFoundError) as error:
  if expected not in str(error):raise RuntimeError('Wrong rejection category: '+name+': '+str(error))
  results.append({'case':name,'status':'REJECTED_AS_EXPECTED','required_reason':expected,'mode':mode})
 else:raise RuntimeError('Mutation survived: '+name)
run();results.append({'case':'unchanged_candidate','status':'PASS'})
with tempfile.TemporaryDirectory(prefix='t20-supplement-negative-') as t:
 root=Path(t)/'envelope';shutil.copytree(BASE,root);v.ROOT=root;v.H=root/'historical_coverage'
 for critical in ['FINAL_COVERAGE.json','review_early_math/FOLLOWUP_QUALIFICATION.json']:
  q=v.H/critical;saved=q.read_bytes();q.unlink()
  reject('missing_final_member_'+critical,'missing required final coverage/review member','Physical final-member removal; cannot pass by omitting final coverage or review.')
  q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(saved)
 resolver=json.loads((v.H/'SOURCE_PATH_RESOLVER.json').read_text());rel=resolver['source_objects'][0]['included_path'];p=root/rel;raw=p.read_bytes()
 p.write_bytes(raw+b'\nTAMPERED_SOURCE\n');reject('tampered_source_bytes','source digest mismatch','Physical source mutation in disposable envelope; checked before inventory validation.');p.write_bytes(raw)
 p.unlink();reject('missing_bound_local_source','missing source','Physical source removal in disposable envelope; checked before inventory validation.');p.write_bytes(raw)
 run()
v.ROOT=BASE;v.H=BASE/'historical_coverage';original_load=v.load
# Direct semantic-input fault injection bypasses file-integrity tests deliberately,
# demonstrating that metadata cannot pass merely because its file is rehashed.
def injected(rel):
 data=original_load(rel)
 if rel==target:
  data=copy.deepcopy(data);mutate(data)
 return data
v.load=injected
target='historical_coverage/REVIEW_DISPOSITIONS.json'
mutate=lambda d:d['items'][0].__setitem__('target_sha256','0'*64)
reject('mismatched_current_review_target','review disposition target drift','Loaded-metadata mutation after byte checks; specific currentness constraint tested.')
target='historical_coverage/FINAL_COVERAGE.json'
mutate=lambda d:d['early'][1].__setitem__('id',d['early'][0]['id'])
reject('duplicate_early_coverage_id','final early row join','Loaded-metadata mutation after byte checks; exact population constraint tested.')
mutate=lambda d:d['early'].pop()
reject('missing_early_coverage_id','final early row join','Loaded-metadata mutation after byte checks; exact population constraint tested.')
mutate=lambda d:d['later'][1].__setitem__('id',d['later'][0]['id'])
reject('duplicate_later_coverage_id','final later population','Loaded-metadata mutation after byte checks; exact population constraint tested.')
target='historical_coverage/SOURCE_PATH_RESOLVER.json'
mutate=lambda d:d['routes'][0].__setitem__('workspace_alias','../outside')
reject('unsafe_alias_traversal','unsafe relative locator','Loaded resolver mutation; path confinement tested.')
def badlocator(d):
 row=next(r for r in d['routes'] if r['locator_field']!='source_packet_member');row['original_locator']='invented-unbound-locator'
mutate=badlocator
reject('unowned_source_locator','source locator not present','Loaded resolver mutation; original exact ledger ownership checked.')
v.load=original_load;run()
print(json.dumps({'status':'PASS','cases':results,'scope':'Physical source corruption/removal in disposable copies plus explicit semantic metadata fault injection. Semantic cases bypass byte inventory deliberately to test independent constraints. No scientific source, repository or delivered member altered.'},indent=2))
