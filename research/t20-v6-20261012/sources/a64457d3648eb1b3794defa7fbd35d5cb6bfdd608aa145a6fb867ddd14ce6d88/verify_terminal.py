#!/usr/bin/env python3
"""Independent detached terminal verification. Never mutates inputs or builds."""
from pathlib import Path
from collections import Counter
import hashlib, json, subprocess, os, shlex, datetime, zipfile, sys
A=Path(__file__).resolve().parent.parent; W=A.parents[1];D=A/'dependencies';E=A/'evidence';R=A/'independent-review'
P=A/'immutable-extraction/Sixteenth_Orthemology_Proof_Source_Recovered_v1';T=W/'recovery-20261005-1330/environment/toolchain/lean-4.19.0-linux'
Z=W/'tranche16/proof-package-integration/releases/Sixteenth_Orthemology_Proof_Source_Recovered_v1.zip'
O=Path(sys.argv[1]).resolve()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())
assert sha(Z)=='40c77652d3938e95f832023f32f018e1e394ffbd57adcc7d918d07d578e8a3a2'
with zipfile.ZipFile(Z) as z:
 assert len(z.namelist())==376
 for n in z.namelist():
  f=A/'immutable-extraction'/n
  assert f.is_file() and not f.is_symlink() and z.read(n)==f.read_bytes(),n
 assert len([p for p in P.rglob('*') if p.is_file()])==376
pins=load(P/'lean/lake-manifest.json')['packages'];closure=load(P/'DEPENDENCY_CLOSURE.json')['recorded_source_modules']
repos=[]
for pin in pins:
 n=pin['name'];d=D/n
 assert subprocess.check_output(['git','-C',str(d),'rev-parse','HEAD'],text=True).strip()==pin['rev']
 count=0
 for ent in subprocess.check_output(['git','-C',str(d),'ls-tree','-rz','--full-tree',pin['rev']]).split(b'\0'):
  if not ent:continue
  meta,path=ent.split(b'\t',1);mode,typ,oid=meta.decode().split();rel=path.decode();assert typ=='blob'
  for base in [d,W/'recovery-20261005-1330/environment/dependencies'/n]:
   p=base/rel;blob=os.readlink(p).encode() if mode=='120000' else p.read_bytes();assert hashlib.sha1(b'blob '+str(len(blob)).encode()+b'\0'+blob).hexdigest()==oid,(base,rel)
  count+=1
 repos.append({'package':n,'revision':pin['rev'],'raw_git_blobs_match_original_and_isolated':count})
build=load(E/'DEPENDENCY_COLD_BUILD.json');assert build['status']=='PASS' and build['exit_code']==0
log=(E/'DEPENDENCY_COLD_BUILD.log').read_text(); assert sha(E/'DEPENDENCY_COLD_BUILD.log')==build['log_sha256']
assert 'Build completed successfully.' in log
expected={(D/r['package']/'.lake/build/lib/lean'/r['object_relative_path']).resolve():r for r in closure}
actual={p.resolve() for pin in pins for p in (D/pin['name']/'.lake/build/lib/lean').rglob('*.olean')}
assert actual==set(expected),(len(actual),len(expected))
allowedpaths={(D/pin['name']/'.lake/build/lib/lean').resolve() for pin in pins}|{(A/'lake-driver/.lake/build/lib/lean').resolve()}
commands={};options={};objrows=[]
for line in log.splitlines():
 if line.startswith('trace: .> LEAN_PATH='):
  tok=shlex.split(line[len('trace: .> '):]); assert tok[1]==str(T/'bin/lean'),tok
  paths={(A/'lake-driver'/p).resolve() for p in tok[0][len('LEAN_PATH='):].split(':')};assert paths==allowedpaths,tok
  src=[p for p in tok[2:] if p.endswith('.lean')];assert len(src)==1
  obj=(A/'lake-driver'/tok[tok.index('-o')+1]).resolve();assert obj in expected and obj not in commands
  row=expected[obj];assert (A/'lake-driver'/src[0]).resolve()==(D/row['package']/row['source_path']).resolve()
  # No import plugins, trust-level changes, or unexplained compiler flags.
  flags=[p for p in tok[2:] if p.startswith('-')]; assert all(p in ['-R','-o','-i','-c','--json'] or p.startswith('-D') for p in flags),flags
  opts=tuple(p for p in flags if p.startswith('-D'));options.setdefault(row['package'],set()).add(opts)
  commands[obj]=tok
assert set(commands)==actual
assert not list((A/'lake-driver/.lake/build/lib/lean').rglob('*.olean'))
assert {p.resolve().with_suffix('.olean') for pin in pins for p in (D/pin['name']/'.lake/build/lib/lean').rglob('*.ilean')}==actual
expected_mathlib_opts={'-Dpp.unicode.fun=true','-DautoImplicit=false','-DmaxSynthPendingDepth=3','-Dweak.linter.docPrime=false','-Dweak.linter.hashCommand=true','-Dweak.linter.oldObtain=true','-Dweak.linter.style.cases=true','-Dweak.linter.style.cdot=true','-Dweak.linter.style.docString=true','-Dweak.linter.style.dollarSyntax=true','-Dweak.linter.style.header=true','-Dweak.linter.style.lambdaSyntax=true','-Dweak.linter.style.longLine=true','-Dweak.linter.style.longFile=1500','-Dweak.linter.style.maxHeartbeats=true','-Dweak.linter.style.missingEnd=true','-Dweak.linter.style.multiGoal=true','-Dweak.linter.style.openClassical=true','-Dweak.linter.style.refine=true','-Dweak.linter.style.setOption=true'}
for package, variants in options.items():
 assert len(variants)==1
 actual_opts=set(next(iter(variants)))
 assert actual_opts==(expected_mathlib_opts if package=='mathlib' else {'-Dlinter.missingDocs=true'} if package=='batteries' else set()),(package,actual_opts)
for obj,row in sorted(expected.items(),key=lambda x:(x[1]['package'],x[1]['module'])):
 assert sha(D/row['package']/row['source_path'])==row['source_sha256']
 objrows.append({'package':row['package'],'module':row['module'],'source_sha256':row['source_sha256'],'object_sha256':sha(obj),'command_sha256':hashlib.sha256(json.dumps(commands[obj]).encode()).hexdigest()})
for rows in [load(E/'PLATFORM_TOOLS.json')['files'],load(E/'COMPILER_PARSED_SOURCE_CLOSURE.json')['trusted_toolchain']]:
 for r in rows:assert sha(Path(r.get('path',r.get('object_path'))))==r.get('sha256',r.get('trusted_object_sha256'))
project=load(O/'project-build/PROJECT_BUILD_RECEIPT.json');controls=load(O/'controls/CONTROL_REPLAY_RECEIPT.json');replay=load(O/'REPLAY_RECEIPT.json')
assert project['status']==controls['status']==replay['status']=='PASS'
locks=load(P/'MATHEMATICAL_SOURCE_LOCK.json');assert len(locks)==111
assert len(project['records'])==112 and project['fresh_mathematical_modules']==111 and not project['project_object_reuse']
for r in project['records']:
 obj=O/'project-build'/('inherited' if r['module'].startswith('verification.') else 'project')/(r['module'].replace('.','/')+'.olean')
 assert r['exit']==0 and sha(obj)==r['new_object_sha256'] and sha(O/'project-build/logs'/(r['module']+'.log'))==r['log_sha256']
assert len(controls['records'])==226 and controls['executed_control_files']==220 and controls['new_integration_controls']==4
assert controls['role_counts']=={'support':12,'positive':63,'negative':145}
for r in controls['records']:
 assert r['passed'] is True and sha(O/'controls/logs'/(r['label']+'.log'))==r['log_sha256']
assert controls['mathematical_build_receipt_sha256']==sha(O/'project-build/PROJECT_BUILD_RECEIPT.json')
pythonlog=(O/'controls/logs/PYTHON_REFERENCE.log').read_text();assert '\nOK\n' in pythonlog
assert replay['fresh_mathematical_sources']==111 and replay['controls_executed']==220 and not replay['project_object_reuse']
assert replay['new_dependency_cold_build'] is False and replay['prepared_dependency_object_reuse'] is True
inventory={(r['package'],r['module']):r['object_sha256'] for r in objrows}
for dep in replay['dependency_bindings']:
 for obj,digest in dep['object_hashes'].items():assert digest==inventory[(dep['package'],obj[:-6].replace('/','.'))]
assert sum(len(d['object_hashes']) for d in replay['dependency_bindings'])==1369
assert replay['proof_coverage']==controls['coverage']
assert replay['lean_binary_sha256']==project['lean_binary_sha256']==sha(T/'bin/lean')
assert replay['source_package_integrity_sha256']==sha(P/'FILE_INTEGRITY.json')
runner=load(E/'IMMUTABLE_CORE_REPLAY.json')
assert runner['status']=='PASS' and runner['exit_code']==0
assert runner['log_sha256']==sha(E/'IMMUTABLE_CORE_REPLAY.log')
samples=[json.loads(line) for line in (E/'IMMUTABLE_CORE_REPLAY_PROCESS_SAMPLES.jsonl').read_text().splitlines()]
processes=[p for sample in samples for p in sample['processes']]
assert processes
for p in processes:
 assert p['exe']==str(T/'bin/lean')
 assert p['environment']['LEAN_NUM_THREADS']=='1' and p['environment']['LEAN_SRC_PATH']==''
 assert all(Path(path).is_relative_to(O) or Path(path).is_relative_to(D) for path in p['environment']['LEAN_PATH'].split(':'))
prebuild=load(R/'PREBUILD_INDEPENDENT_OBSERVATION.json')
assert sha(A/'tools/run_step_source_build_v1.py')==prebuild['checked_input_sha256']['tools/run_step.py']
for row in load(E/'WRAPPER_VERSION_PROVENANCE.json')['files']:
 assert sha(A/row['path'])==row['sha256']
comparison=load(E/'COLD_VS_PREPARED_OBJECT_HASH_COMPARISON.json')
for row in comparison['rows']:
 rel=Path(row['module'].replace('.','/')+'.olean')
 fresh=D/row['package']/'.lake/build/lib/lean'/rel
 old=W/'recovery-20261005-1330/environment/dependencies'/row['package']/'.lake/build/lib/lean'/rel
 assert sha(fresh)==row['source_built_sha256'] and sha(old)==row['previous_prepared_sha256']
 assert (row['source_built_sha256']==row['previous_prepared_sha256'])==row['identical']
assert sum(row['identical'] for row in comparison['rows'])==1355 and len(comparison['rows'])==1369
for row in load(E/'WIDGET_SOURCE_ASSETS.json')['fresh_source_built_assets']:
 assert sha(D/'proofwidgets'/row['path'])==row['sha256']
author_final=load(E/'DETACHED_SOURCE_REBUILD_REPLAY_RECEIPT.json')
assert author_final['status']=='PASS'
for path,digest in author_final['evidence_sha256'].items():assert sha(A/path)==digest
# The local config artifacts are build-tool outputs, separately bounded.
config=[]
for p in A.rglob('lakefile.olean'):
 stage='WIDGET_SOURCE_BUILD2' if '/proofwidgets/' in str(p) else 'DEPENDENCY_COLD_BUILD'
 stage_record=load(E/(stage+'.json')); config_source=p.parent.parent/'lakefile.lean'
 assert datetime.datetime.fromisoformat(stage_record['start_utc']).timestamp()<=p.stat().st_mtime<=datetime.datetime.fromisoformat(stage_record['end_utc']).timestamp()
 config.append({'path':str(p.relative_to(A)),'sha256':sha(p),'source_path':str(config_source.relative_to(A)),'source_sha256':sha(config_source),'generating_lake_invocation':stage_record['command'],'generating_stage':stage,'mtime_within_generating_stage':True,'role':'Fresh Lake build configuration object, not imported third-party library proof object'})
receipt={'disposition':'DETACHED_SCOPE_ACCEPTED','verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'immutable_core_zip_sha256':sha(Z),'immutable_archive_files_byte_equal':376,'required_third_party_modules_freshly_source_built':1369,'source_modules_by_package':dict(Counter(r['package'] for r in closure)),'source_repositories':repos,'independent_root_closure_verified':load(R/'INDEPENDENT_SOURCE_CLOSURE.json')['exact_matches_immutable_manifest'],'one_source_compile_command_per_required_output':len(commands),'only_isolated_dependency_and_driver_paths':True,'compile_options_by_package':{k:[list(x) for x in v] for k,v in options.items()},'complete_core_replay':{'directory':str(O),'fresh_project_modules':111,'fresh_inherited_audit_support':1,'designated_control_files':220,'control_roles':controls['role_counts'],'new_integration_controls':4,'total_control_and_audit_invocations':226,'coverage':controls['coverage'],'python_reference_tests_pass':True},'config_build_tool_artifacts':config,'trust_scope':['Official Lean 4.19 compiler/runtime, Init/Lean/Std/Lake objects remain trusted and unbootstrapped','Operating-system runtime and npm-distributed JavaScript build tools remain trusted infrastructure','Only required third-party import closure rebuilt; not all Mathlib','Immutable replay retains historical static cache wording; its exact dependency object hashes match these newly source-built objects','No broader mathematical, artifact-release or audit-lifecycle completion claimed'],'bound_receipts':{str(p.relative_to(A)):sha(p) for p in [E/'DEPENDENCY_COLD_BUILD.json',E/'DEPENDENCY_COLD_BUILD.log',E/'COLD_DEPENDENCY_BUILD_RECEIPT.json',E/'FRESH_DEPENDENCY_SOURCE_OBJECT_INVENTORY.json',O/'REPLAY_RECEIPT.json',O/'project-build/PROJECT_BUILD_RECEIPT.json',O/'controls/CONTROL_REPLAY_RECEIPT.json',R/'INDEPENDENT_SOURCE_CLOSURE.json',R/'PREBUILD_INDEPENDENT_OBSERVATION.json']},'object_bindings':objrows}
receipt.update(replay_runner_exit=runner['exit_code'],sampled_actual_lean_processes_checked=len(processes),replay_process_sample_isolation_verified=True,preserved_source_build_runner_hash_matches_prebuild_observation=True,generated_widget_metadata_restoration=load(E/'COLD_DEPENDENCY_BUILD_RECEIPT.json')['generated_tracked_metadata_restored'],prepared_cache_comparison={'identical_objects':1355,'different_objects':14,'claim':'Read-only comparison only; prior prepared objects were never imported by source build or replay. No bit-for-bit cache reproducibility claim.'},python_reference_test_count=22)
for p in [E/'IMMUTABLE_CORE_REPLAY.json',E/'IMMUTABLE_CORE_REPLAY.log',E/'IMMUTABLE_CORE_REPLAY_PROCESS_SAMPLES.jsonl',E/'DETACHED_SOURCE_REBUILD_REPLAY_RECEIPT.json',E/'COLD_VS_PREPARED_OBJECT_HASH_COMPARISON.json',E/'WRAPPER_VERSION_PROVENANCE.json',E/'WIDGET_SOURCE_BUILD2.json',E/'WIDGET_SOURCE_BUILD2.log',E/'WIDGET_SOURCE_BUILD3.json',E/'WIDGET_SOURCE_BUILD3.log',E/'WIDGET_SOURCE_ASSETS.json',E/'PLATFORM_TOOLS.json',E/'OFFICIAL_TOOLCHAIN_ARCHIVE_BYTE_CHECK.json',Path(__file__)]:receipt['bound_receipts'][str(p.relative_to(A))]=sha(p)
f=R/'DETACHED_ACCEPTANCE.json';f.write_text(json.dumps(receipt,indent=2)+'\n');print('DETACHED_SCOPE_ACCEPTED',str(f),sha(f))
