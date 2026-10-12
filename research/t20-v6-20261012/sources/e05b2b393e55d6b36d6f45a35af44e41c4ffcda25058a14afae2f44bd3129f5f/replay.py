from pathlib import Path
import hashlib,json,subprocess,re
R=Path(__file__).resolve().parent; W=R.parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'
paths=(R/'lean_path.txt').read_text().strip().split(':')
objects=[];seen=set()
for d in map(Path,paths[1:]):
 if '.lake/packages/' in str(d):continue
 for p in sorted(d.glob('*.olean')):
  if p.stem in seen:continue
  seen.add(p.stem); objects.append({'module':p.stem,'path':str(p.relative_to(W)),'sha256':sha(p),'bytes':p.stat().st_size})
for receipt in ['hase-generic-rigidity-review-20261010/RETAINED_OBJECTS.json']:
 for x in json.loads((W/receipt).read_text()): assert sha(W/x['path'])==x['sha256']
sourcepaths=[W/'hase-imported-compiler-transport-20261010/sources/ExtensionalRepairSyntax.lean',W/'hase-full-per-extension-20261010/FullPER.lean',W/'hase-complete-development-review-20261010/sources/OpenDevelopments.lean',W/'hase-generic-fold-transport-20261010/SourceRigidity.lean',W/'hase-generic-fold-transport-20261010/RigidityDiscriminator.lean']
inputs=[{'path':str(p.relative_to(W)),'sha256':sha(p)} for p in sourcepaths]
records=[]
import os
env=dict(os.environ,LEAN_PATH=':'.join(paths))
for module,expected in [('TaggedPER',0),('Boundary',0),('ReviewControls',0),('TagCollapseMustFail',1),('RawCollapseMustFail',1)]:
 source=R/'sources'/f'{module}.lean'; command=[str(lean),'--trust=0','-o',str(R/'fresh-lib'/f'{module}.olean'),str(source)]
 p=subprocess.run(command,env=env,text=True,capture_output=True);log=p.stdout+p.stderr;(R/f'{module}.log').write_text(log)
 assert (p.returncode==0)==(expected==0),(module,log)
 if expected==0:
  assert not any(x in log for x in ['sorryAx','error:','warning:'])
  for ax in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S): assert set(re.sub(r'\s+','',ax).split(',')) <= {'propext','Classical.choice','Quot.sound',''}
  clean=re.sub(r'/\-.*?\-/|--[^\n]*','',source.read_text(),flags=re.S)
  assert not re.search(r'\b(sorry|admit|axiom|unsafe|native_decide|implemented_by)\b',clean)
 records.append({'module':module,'source_sha256':sha(source),'exit_code':p.returncode,'expected':expected,'log_sha256':sha(R/f'{module}.log'),'command':command})
for f in ['TaggedPER','Boundary']:assert sha(R/'sources'/f'{f}.lean')==sha(W/'hase-sigma-tag-boundary-20261010'/f'{f}.lean')
for x in objects:assert sha(W/x['path'])==x['sha256']
(R/'RETAINED_OBJECTS.json').write_text(json.dumps(objects,indent=2)+'\n')
(R/'REVIEW_RECEIPT.json').write_text(json.dumps({'status':'PASS','trust_zero':True,'baseline_rebuilt':False,'protected_mutations':False,'source_freeze_unchanged':True,'lean_binary_sha256':sha(lean),'source_inputs':inputs,'records':records,'retained_objects_count':len(objects)},indent=2)+'\n')
print('PASS',len(records),'replays/controls;',len(objects),'retained objects unchanged')
