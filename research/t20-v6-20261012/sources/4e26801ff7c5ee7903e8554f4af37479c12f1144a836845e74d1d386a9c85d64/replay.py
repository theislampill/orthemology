from pathlib import Path
import hashlib,json,os,subprocess,re,datetime
R=Path(__file__).resolve().parent; W=R.parent; A=W/'rational-shift-realisation-20261011'; B=W/'rational-threshold-formal-extension-20261011'; O=R/'kernel'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
base=json.loads((B/'BASELINE_REBUILD.json').read_text())
for m in base['modules']:
 p=m['module'].replace('.','/')
 assert sha(B/'baseline'/(p+'.lean'))==m['source_sha256']
 assert sha(B/'baseline-build'/(p+'.olean'))==m['object_sha256']
mods=[('BinaryWeights','weights/BinaryWeights.lean','RationalBinaryWeights'),('UnaryPrefixRealisation','compiler/UnaryPrefixRealisation.lean','OrthemologyTagged.UnaryPrefix'),('UnaryShiftLaw','UnaryShiftLaw.lean','OrthemologyRationalShift'),('RationalShiftRealisation','RationalShiftRealisation.lean','OrthemologyRationalShift')]
env=dict(os.environ,LEAN_PATH=str(O)+':'+(B/'lean_path.txt').read_text().strip());lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'; records=[];names=[]
for m,rel,ns in mods:
 p=A/rel; h=sha(p)
 r=subprocess.run([str(lean),'--trust=0','-o',str(O/(m+'.olean')),str(p)],cwd=W,env=env,text=True,capture_output=True)
 (O/(m+'.log')).write_text(r.stdout+r.stderr)
 assert r.returncode==0,(m,r.stdout,r.stderr)
 assert sha(p)==h,'Source changed during replay'
 records.append({'module':m,'source':str(p.relative_to(W)),'source_sha256':h,'object_sha256':sha(O/(m+'.olean')),'exit_code':r.returncode})
 names.extend(ns+'.'+n for n in re.findall(r'^(?:@\[simp\] )?theorem\s+([A-Za-z0-9_]+)',p.read_text(),re.M))
 print('PASS',m,flush=True)
p=R/'InspectAxioms.lean';p.write_text('import RationalShiftRealisation\n'+''.join('#print axioms '+n+'\n' for n in names))
r=subprocess.run([str(lean),'--trust=0',str(p)],cwd=W,env=env,text=True,capture_output=True);(O/'AXIOMS.log').write_text(r.stdout+r.stderr)
assert r.returncode==0,(r.stdout,r.stderr)
assert 'sorryAx' not in r.stdout and 'ofReduceBool' not in r.stdout
(R/'REPLAY.json').write_text(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trust':0,'modules':records,'axiom_inspection_exit':r.returncode,'theorems_inspected':names,'baseline_modules_hash_rechecked':len(base['modules']),'baseline_rebuild_manifest_sha256':sha(B/'BASELINE_REBUILD.json'),'dependency_search_path':env['LEAN_PATH']},indent=2)+'\n')
print('PASS AXIOMS',len(names),flush=True)
