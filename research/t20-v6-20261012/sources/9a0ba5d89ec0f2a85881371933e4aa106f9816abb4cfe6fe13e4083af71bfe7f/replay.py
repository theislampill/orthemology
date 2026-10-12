import pathlib, hashlib,json,os,subprocess,time
R=pathlib.Path(__file__).resolve().parent; W=R.parent; A=W/'hase-graph-bridge-assembly-20261010'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def rec(p):return {'path':str(p.relative_to(W)),'sha256':sha(p),'bytes':p.stat().st_size}
def check_records(x):
 if isinstance(x,dict):
  if 'path' in x and 'sha256' in x:
   p=W/x.get('local_path',x['path']); assert sha(p)==x['sha256'],p
   if 'bytes' in x:assert p.stat().st_size==x['bytes'],p
  for y in x.values():check_records(y)
 elif isinstance(x,list):
  for y in x:check_records(y)
assert sha(A/'MANIFEST.json')=='0b9a10ae696e1bc443aca343bf0db46f38d1f4c722f3425abb95a623539d8a9d'
frozen={p:sha(p) for p in A.rglob('*') if p.is_file()}
for n,h in json.loads((A/'MANIFEST.json').read_text())['files'].items():assert sha(A/n)==h,n
P=W/'hase-full-per-review-20261010'; prp=P/'PREREQUISITE_REBUILD.json'
assert sha(prp)=='7960ee87b94726090cd2c9f2ddd5abe7c99b9fb29b72abea7302847cdf4e52d1'
pr=json.loads(prp.read_text())
for b in pr['build_records']:
 assert b['trust_zero'] and b['exit_code']==0
 p=P/'fresh-lib'/pathlib.Path(*b['module'].split('.')).with_suffix('.olean');assert sha(p)==b['object_sha256'],p
for s in pr['source_checks']:
 p=W/'hase-imported-compiler-transport-20261010/sources'/f"{s['module']}.lean";assert sha(p)==s['sha256'],p
for m in pr['manifest_checks']:
 p=W/m['package'];assert sha(p/'MANIFEST.json')==m['manifest_sha256']
 for f in json.loads((p/'MANIFEST.json').read_text())['files']:assert sha(p/f['path'])==f['sha256']
refs=[]
for n in ['hase-full-per-review-20261010','hase-internal-graph-review-20261010']:
 p=W/n/'REVIEW_RECEIPT.json';check_records(json.loads(p.read_text()));refs.append(rec(p))
p=W/'hase-internal-graph-20261010/MANIFEST.json'
for n,h in json.loads(p.read_text())['files'].items():assert sha(p.parent/n)==h
for s in json.loads((W/'identity-frontier-inspection-20261009/SOURCE_BINDINGS.json').read_text())['sources']:assert sha(W/s['local_path'])==s['sha256']
lean=W/'.toolchains/lean-4.19.0-linux/bin/lean';assert sha(lean)==pr['lean_binary_sha256']
lp=(A/'lean_path.txt').read_text().strip().split(':');assert lp[0]==str(A);lp[0]=str(R/'fresh-lib')
env={**os.environ,'LEAN_PATH':':'.join(lp)};(R/'lean_path.txt').write_text(env['LEAN_PATH']+'\n')
replays=[]
for module in ['GraphBridgeAssembly','AssemblyControls','IndependentControls']:
 src=R/'sources'/f'{module}.lean'
 if module!='IndependentControls':src.write_bytes((A/f'{module}.lean').read_bytes())
 out=R/'fresh-lib'/f'{module}.olean';cmd=[str(lean),'--trust=0','-o',str(out),str(src)]
 t=time.time();res=subprocess.run(cmd,cwd=W,env=env,text=True,capture_output=True)
 log=R/f'{module}_REPLAY.log';log.write_text('$ '+' '.join(cmd)+'\n'+res.stdout+res.stderr)
 assert res.returncode==0,res.stdout+res.stderr
 assert 'sorryAx' not in res.stdout+res.stderr
 replays.append({'module':module,'source':rec(src),'object':rec(out),'log':rec(log),'trust_zero':True,'exit_code':0,'seconds':round(time.time()-t,3)})
 print(module,'PASS',flush=True)
assert all(sha(p)==h for p,h in frozen.items())
receipt={'status':'PASS_INDEPENDENT_CONDITIONAL_ASSEMBLY_REVIEW','literal_target':'OPEN_UNCONDITIONALLY','bridge_inhabitants':'NOT_PROVED','source_pin':'7efc6217c090b92d65f2c4cb8b011c18eb96bf7c','author_manifest':rec(A/'MANIFEST.json'),'author_source':rec(A/'GraphBridgeAssembly.lean'),'prerequisite_receipt':rec(prp),'prior_review_receipts':refs,'prerequisite_objects_rehashed':len(pr['build_records']),'pinned_sources_rehashed':len(pr['source_checks']),'source_replays':replays,'lean_version':subprocess.check_output([str(lean),'--version'],text=True).strip(),'lean_binary_sha256':sha(lean),'lean_bootstrap_verified':False,'full_83_module_rebuild_repeated':False,'author_package_unchanged':True,'protected_mutations':False,'third_party_objects_reused':True}
(R/'REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
