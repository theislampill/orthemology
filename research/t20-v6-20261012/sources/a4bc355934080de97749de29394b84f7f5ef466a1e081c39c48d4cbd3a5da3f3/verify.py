#!/usr/bin/env python3
"""Rehash frozen inputs and replay only this new conditional-assembly package."""
import hashlib,json,os,pathlib,re,subprocess,time
O=pathlib.Path(__file__).resolve().parent; W=O.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def record(p): return {'path':str(p.relative_to(W)),'sha256':sha(p),'bytes':p.stat().st_size}
prpath=W/'hase-full-per-review-20261010/PREREQUISITE_REBUILD.json'
pr=json.loads(prpath.read_text()); P=W/'hase-full-per-review-20261010'
assert sha(prpath)=='7960ee87b94726090cd2c9f2ddd5abe7c99b9fb29b72abea7302847cdf4e52d1'
for r in pr['build_records']:
 assert r['trust_zero'] and r['exit_code']==0
 assert sha(P/'fresh-lib'/pathlib.Path(*r['module'].split('.')).with_suffix('.olean'))==r['object_sha256']
for r in pr['source_checks']:
 assert sha(W/'hase-imported-compiler-transport-20261010/sources'/f"{r['module']}.lean")==r['sha256']
for r in pr['manifest_checks']:
 root=W/r['package'];assert sha(root/'MANIFEST.json')==r['manifest_sha256']
 for x in json.loads((root/'MANIFEST.json').read_text())['files']:
  assert sha(root/x['path'])==x['sha256']
review_records=[]
def check_records(j):
 if isinstance(j,dict):
  if 'path' in j and 'sha256' in j:
   p=W/j.get('local_path',j['path']);assert sha(p)==j['sha256'],p
   if 'bytes' in j:assert p.stat().st_size==j['bytes'],p
  for x in j.values():check_records(x)
 elif isinstance(j,list):
  for x in j:check_records(x)
for name in ['hase-full-per-review-20261010','hase-internal-graph-review-20261010']:
 path=W/name/'REVIEW_RECEIPT.json';j=json.loads(path.read_text());check_records(j)
 review_records.append(record(path))
graph=W/'hase-internal-graph-20261010'
for p,h in json.loads((graph/'MANIFEST.json').read_text())['files'].items():assert sha(graph/p)==h
lean=W/'.toolchains/lean-4.19.0-linux/bin/lean';assert sha(lean)==pr['lean_binary_sha256']
for r in json.loads((W/'identity-frontier-inspection-20261009/SOURCE_BINDINGS.json').read_text())['sources']:
 assert sha(W/r['local_path'])==r['sha256']
reuse={'status':'PASS_HASH_VERIFIED_REUSE','prerequisite_receipt':record(prpath),
 'review_receipts':review_records,'prerequisite_objects_rehashed':len(pr['build_records']),
 'pinned_sources_rehashed':len(pr['source_checks']),'prior_review_objects_and_sources_rehashed':True,
 'predecessor_manifests_rehashed':True,'graph_manifest':record(graph/'MANIFEST.json'),
 'lean_version':subprocess.check_output([str(lean),'--version'],text=True).strip(),
 'lean_binary_sha256':sha(lean),'lean_bootstrap_verified':False,
 'full_83_module_rebuild_repeated':False,'third_party_library_objects_reused':True}
(O/'validation/PREREQUISITE_REUSE.json').write_text(json.dumps(reuse,indent=2)+'\n')
expected={'GraphBridgeAssembly':'0dd6090f8cde9debb2bb58b921bac52c9bd6dd058cece3d2b09fc8f501d1b8e3',
 'AssemblyControls':'2167a1b555d9b8a1446e2fda736e6ffa7dc869d05049b3f225ff51529c2ce0eb'}
env={**os.environ,'LEAN_PATH':(O/'lean_path.txt').read_text().strip()};replays=[]
for module,h in expected.items():
 src=O/f'{module}.lean';assert sha(src)==h
 cmd=[str(lean),'--trust=0','-o',str(O/f'{module}.olean'),str(src)]
 start=time.time();r=subprocess.run(cmd,cwd=W,env=env,capture_output=True,text=True)
 log=O/'validation'/f'{module}_FINAL.log';log.write_text('$ '+' '.join(cmd)+'\n'+r.stdout+r.stderr)
 assert r.returncode==0,r.stdout+r.stderr
 assert not re.search(r'error:|sorryAx|declaration uses',r.stdout+r.stderr)
 if module=='AssemblyControls':
  assert r.stdout.count('PASS source-only:')==7
  assert r.stdout.count('PASS required actual dependency:')==6
 assert sha(src)==h
 replays.append({'module':module,'source':record(src),'object':record(O/f'{module}.olean'),
  'log':record(log),'trust_zero':True,'exit_code':r.returncode,'seconds':round(time.time()-start,3)})
 print(module,'PASS',flush=True)
result={'status':'PASS_CONDITIONAL_ASSEMBLY_AUTHOR_VERIFICATION','literal_target':'OPEN',
 'bridge_inhabitants':'NOT_PROVED','bridge_hypotheses':'arbitrary actual HasE derivations',
 'replays':replays,'prerequisite_reuse':record(O/'validation/PREREQUISITE_REUSE.json'),
 'standard_axioms_only':['propext','Classical.choice','Quot.sound'],
 'positive_source_dependency_audits':7,'required_actual_rule_and_frozen_dependency_checks':6,
 'frozen_predecessors_unchanged':True,'protected_mutations':False,'independent_review':'PENDING'}
(O/'validation/REPLAY_RECEIPT.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS frozen prerequisites, conditional assembly, normalization/abstraction controls, dependency audit')
