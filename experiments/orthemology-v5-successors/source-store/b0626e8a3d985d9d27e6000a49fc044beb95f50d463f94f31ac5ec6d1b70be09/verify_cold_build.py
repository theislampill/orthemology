from pathlib import Path
import hashlib,json,subprocess,shlex,datetime,collections
from context import context
A,D,P,T,E=context()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def git(d,*args):return subprocess.check_output(['git','-C',str(d),*args],text=True).strip()
build=json.loads((E/'DEPENDENCY_COLD_BUILD.json').read_text());assert build['status']=='PASS' and build['exit_code']==0
assert sha(E/'DEPENDENCY_COLD_BUILD.log')==build['log_sha256'],'Build log changed after its originating execution receipt'
start=datetime.datetime.fromisoformat(build['start_utc']).timestamp();end=datetime.datetime.fromisoformat(build['end_utc']).timestamp()
closure=json.loads((P/'DEPENDENCY_CLOSURE.json').read_text())['recorded_source_modules'];expected={(D/r['package']/r['object_relative_path']).as_posix() for r in []}
want={(D/r['package']/'.lake/build/lib/lean'/r['object_relative_path']).resolve():r for r in closure};got={f.resolve() for d in D.iterdir() for f in d.glob('.lake/build/lib/lean/**/*.olean')};assert got==set(want),{'missing':[str(p) for p in set(want)-got],'extra':[str(p) for p in got-set(want)]}
commands={};all_options=collections.defaultdict(set);log=(E/'DEPENDENCY_COLD_BUILD.log').read_text()
assert 'Build completed successfully.' in log
for line in log.splitlines():
 if not line.startswith('trace: .> LEAN_PATH=') or str(T/'bin/lean') not in line:continue
 tokens=shlex.split(line[len('trace: .> '):]);assert tokens[0].startswith('LEAN_PATH=');assert tokens[1]==str(T/'bin/lean')
 paths=[(A/'lake-driver'/p).resolve() for p in tokens[0].removeprefix('LEAN_PATH=').split(':')];assert all(p.is_relative_to(A) for p in paths),paths
 assert len(paths)==10 and set(paths[:-1])=={(d/'.lake/build/lib/lean').resolve() for d in D.iterdir()}
 assert paths[-1]==(A/'lake-driver/.lake/build/lib/lean').resolve()
 srcs=[t for t in tokens[2:] if t.endswith('.lean')];assert len(srcs)==1,srcs
 src=(A/'lake-driver'/srcs[0]).resolve();obj=(A/'lake-driver'/tokens[tokens.index('-o')+1]).resolve();assert obj in want
 row=want[obj];assert src==(D/row['package']/row['source_path']).resolve();assert obj not in commands,'Duplicate build '+str(obj)
 opts=[t for t in tokens if t.startswith('-D')]
 if row['package']=='mathlib':
  for op in ['-Dpp.unicode.fun=true','-DautoImplicit=false','-DmaxSynthPendingDepth=3']:assert op in opts,(row,opts)
 if row['package']=='batteries':assert '-Dlinter.missingDocs=true' in opts
 commands[obj]={'command':tokens,'effective_lean_path':[str(p) for p in paths],'options':opts};all_options[row['package']].add(tuple(opts))
assert set(commands)==got,(len(commands),len(got))
records=[]
for obj,row in sorted(want.items(),key=lambda kv:(kv[1]['package'],kv[1]['module'])):
 src=D/row['package']/row['source_path'];assert sha(src)==row['source_sha256'];assert start<=obj.stat().st_mtime<=end+1,(obj,obj.stat().st_mtime,start,end)
 records.append(dict(row,object_sha256=sha(obj),object_bytes=obj.stat().st_size,object_mtime_utc=datetime.datetime.fromtimestamp(obj.stat().st_mtime,datetime.timezone.utc).isoformat(),**commands[obj]))
(E/'FRESH_DEPENDENCY_SOURCE_OBJECT_INVENTORY.json').write_text(json.dumps(records,indent=2)+'\n')
restored=[];repos=[]
for pin in json.loads((P/'lean/lake-manifest.json').read_text())['packages']:
 name=pin['name'];d=D/name;rows=json.loads((E/f'{name}_source_inventory.json').read_text())
 assert git(d,'rev-parse','HEAD')==pin['rev']
 assert {r['path'] for r in rows}==set(git(d,'ls-files').splitlines())
 assert sha(E/f'{name}_source_inventory.json')==sha(P/'source-inventories'/f'{name}_source_inventory.json')
 for r in rows:
  f=d/r['path']
  if sha(f)!=r['sha256']:
   assert name=='proofwidgets' and r['path'] in ['widget/package-lock.json.hash','widget/package-lock.json.trace'],(name,r['path'])
   entry={'package':name,'path':r['path'],'generated_sha256':sha(f),'pinned_sha256':r['sha256']}
   (E/('generated-'+f.name)).write_bytes(f.read_bytes());f.write_bytes(subprocess.check_output(['git','-C',str(d),'show',pin['rev']+':'+r['path']]));assert sha(f)==r['sha256'];restored.append(entry)
 assert all(sha(d/r['path'])==r['sha256'] for r in rows);assert not git(d,'status','--porcelain','--untracked-files=no')
 repos.append({'name':name,'revision':pin['rev'],'pinned_tracked_file_inventory':len(rows),'isolated_tracked_files_match':len(rows),'fresh_proof_objects':sum(r['package']==name for r in records)})
for r in json.loads((E/'PLATFORM_TOOLS.json').read_text())['files']:assert sha(Path(r['path']))==r['sha256']
for r in json.loads((E/'COMPILER_PARSED_SOURCE_CLOSURE.json').read_text())['trusted_toolchain']:assert sha(Path(r['object_path']))==r['trusted_object_sha256']
for r in json.loads((E/'WIDGET_SOURCE_ASSETS.json').read_text())['fresh_source_built_assets']:assert sha(D/'proofwidgets'/r['path'])==r['sha256']
assert not list((A/'lake-driver/.lake/build/lib/lean').glob('**/*.olean'))
receipt={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_build_exit':build['exit_code'],'start_utc':build['start_utc'],'end_utc':build['end_utc'],'duration_seconds':build['seconds'],'fresh_third_party_modules':len(records),'modules_by_package':dict(collections.Counter(r['package'] for r in records)),'compiler_commands_bound_to_every_output':len(commands),'unexpected_dependency_proof_objects':0,'preexisting_dependency_proof_objects_used':0,'pinned_tracked_file_inventory':sum(r['pinned_tracked_file_inventory'] for r in repos),'isolated_tracked_sources_match_pins':sum(r['isolated_tracked_files_match'] for r in repos),'repositories':repos,'effective_options_by_package':{k:[list(v) for v in vs] for k,vs in all_options.items()},'generated_tracked_metadata_restored':restored,'inventory_sha256':sha(E/'FRESH_DEPENDENCY_SOURCE_OBJECT_INVENTORY.json'),'source_closure_sha256':sha(E/'COMPILER_PARSED_SOURCE_CLOSURE.json'),'build_log_sha256':sha(E/'DEPENDENCY_COLD_BUILD.log'),'build_receipt_sha256':sha(E/'DEPENDENCY_COLD_BUILD.json'),'official_toolchain_inputs_unchanged':True,'fresh_widget_assets_unchanged':True,'compiler_bootstrapped':False,'full_mathlib_built':False,'hase_replay_still_required':True,'provenance':'SOURCE_BUILD'}
(E/'COLD_DEPENDENCY_BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
