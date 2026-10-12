from pathlib import Path
import datetime,hashlib,json,os,re,subprocess,sys,tempfile
R=Path(__file__).resolve().parent;W=R.parent;LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def rec(p):return {'path':str(p.relative_to(W)),'sha256':sha(p),'bytes':p.stat().st_size}
mods=['RationalThresholdCuts','RationalThresholdComputable','RationalThresholdUniform','RationalThresholdDefect','RationalThresholdControls','RationalThresholdAudit']
inputs=[R/(m+'.lean') for m in mods]+list((R/'negative-controls').glob('*.lean'))+[R/'verify_final.py']
acq=json.loads((R/'ACQUISITION.json').read_text());archive=W/acq['archive']
if sha(archive)!=acq['archive_sha256']:raise RuntimeError('Original archive changed')
for e in acq['source_members']:
 if sha(W/e['path'])!=e['sha256']:raise RuntimeError('Extracted baseline changed: '+e['path'])
deppath=R/'DEPENDENCY_OBJECT_PINS.json'
deps=json.loads(deppath.read_text())['objects']
for e in deps:
 if sha(W/e['path'])!=e['sha256']:raise RuntimeError('External dependency changed: '+e['path'])
base=json.loads((R/'BASELINE_REBUILD.json').read_text())
for e in base['modules']:
 p=R/'baseline-build'/Path(e['module'].replace('.','/')).with_suffix('.olean')
 if sha(p)!=e['object_sha256']:raise RuntimeError('Baseline object changed: '+str(p))
inputs += [W/e['path'] for e in acq['source_members']]
inputs += [R/'baseline-build'/Path(e['module'].replace('.','/')).with_suffix('.olean') for e in base['modules']]
inputs += [LEAN,R/'dependency-overlay/lake-manifest.json',R/'ARCHIVE_LAKE_MANIFEST.json',deppath]
pins=[rec(p) for p in inputs]
OUT=Path(tempfile.mkdtemp(prefix='verified-',dir=R));env=dict(os.environ,LEAN_PATH=str(OUT)+':'+(R/'lean_path.txt').read_text())
results=[]
for m in mods:
 p=subprocess.run([str(LEAN),'--trust=0','-o',str(OUT/(m+'.olean')),str(R/(m+'.lean'))],cwd=W,env=env,capture_output=True,text=True)
 log=OUT/(m+'.log');log.write_text(p.stdout+p.stderr)
 if p.returncode or any(t in p.stdout+p.stderr for t in ['sorryAx','error:','warning:']):raise RuntimeError('Positive verification failure: '+str(log))
 results.append({'module':m,'source':rec(R/(m+'.lean')),'object':rec(OUT/(m+'.olean')),'log':rec(log),'exit_code':0});print('PASS '+m,flush=True)
axioms=[]
audit=(OUT/'RationalThresholdAudit.log').read_text()
for name,body in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",audit,re.S):
 ax=[v.strip() for v in body.split(',') if v.strip()]
 if not set(ax)<={'propext','Classical.choice','Quot.sound'}:raise RuntimeError('Unapproved axioms: '+str(ax))
 axioms.append({'declaration':name,'axioms':ax})
for name in re.findall(r"'([^']+)' does not depend on any axioms",audit):axioms.append({'declaration':name,'axioms':[]})
names=json.loads((R/'TARGET_NAMES.json').read_text())
if len(axioms)!=len(names):raise RuntimeError('Axiom audit target count mismatch')
negative=[]
for src in sorted((R/'negative-controls').glob('*.lean')):
 p=subprocess.run([str(LEAN),'--trust=0',str(src)],cwd=W,env=env,capture_output=True,text=True)
 log=OUT/(src.stem+'.log');log.write_text(p.stdout+p.stderr)
 if p.returncode==0 or 'decide' not in p.stdout+p.stderr or 'false' not in p.stdout+p.stderr:raise RuntimeError('Negative control did not reject expected false proposition: '+str(log))
 negative.append({'source':rec(src),'log':rec(log),'exit_code':p.returncode,'expected_failure':'decide rejected false proposition'});print('REJECTED '+src.stem,flush=True)
for e in pins:
 if sha(W/e['path'])!=e['sha256']:raise RuntimeError('Input mutated during verification: '+e['path'])
for e in deps:
 if sha(W/e['path'])!=e['sha256']:raise RuntimeError('External dependency mutated during verification: '+e['path'])
if sha(archive)!=acq['archive_sha256']:raise RuntimeError('Original archive changed after replay')
receipt={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trust':0,'lean_version':subprocess.check_output([str(LEAN),'--version'],text=True).strip(),'output':str(OUT.relative_to(W)),'positive':results,'negative':negative,'axiom_audits':axioms,'pinned_before_after':pins,'original_archive_sha256':acq['archive_sha256'],'baseline_modules_freshly_rebuilt':len(base['modules']),'external_dependency_objects_pinned_before_after':len(deps),'mathlib_from_pinned_official_cache_not_rebuilt':True,'T20_closure':False,'formal_shift_hardness':False,'hierarchy_library_completeness':False}
(OUT/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');(R/'AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS '+str(len(names))+' axiom audits; '+str(len(negative))+' false-statement controls; '+str(len(pins))+' before/after pins',flush=True)
