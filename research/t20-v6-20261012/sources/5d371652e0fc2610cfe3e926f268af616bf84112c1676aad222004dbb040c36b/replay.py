from pathlib import Path
import hashlib,json,os,subprocess,re,datetime
R=Path(__file__).resolve().parent; W=R.parent; A=W/'rational-threshold-formal-extension-20261011'
O=R/'kernel';O.mkdir(exist_ok=True)
mods=['RationalThresholdCuts','RationalThresholdComputable','RationalThresholdUniform','RationalThresholdDefect','RationalThresholdControls']
env=dict(os.environ,LEAN_PATH=str(O)+':'+(A/'lean_path.txt').read_text().strip())
lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'
records=[];names=[]
for m in mods:
 p=A/(m+'.lean');h=hashlib.sha256(p.read_bytes()).hexdigest()
 r=subprocess.run([str(lean),'--trust=0','-o',str(O/(m+'.olean')),str(p)],cwd=W,env=env,text=True,capture_output=True)
 (O/(m+'.log')).write_text(r.stdout+r.stderr)
 assert r.returncode==0,(m,r.stdout,r.stderr)
 assert hashlib.sha256(p.read_bytes()).hexdigest()==h,'Source changed during replay'
 records.append({'module':m,'source_sha256':h,'object_sha256':hashlib.sha256((O/(m+'.olean')).read_bytes()).hexdigest(),'exit_code':r.returncode})
 names.extend(re.findall(r'^theorem\s+([A-Za-z0-9_]+)',p.read_text(),re.M))
 print('PASS',m,flush=True)
p=R/'InspectAxioms.lean'
p.write_text('import RationalThresholdControls\nimport RationalThresholdUniform\n'+''.join('#print axioms AtomicMembership.RationalThreshold.'+n+'\n' for n in names))
r=subprocess.run([str(lean),'--trust=0',str(p)],cwd=W,env=env,text=True,capture_output=True)
(O/'AXIOMS.log').write_text(r.stdout+r.stderr)
assert r.returncode==0,(r.stdout,r.stderr)
assert 'sorryAx' not in r.stdout and 'ofReduceBool' not in r.stdout
(R/'REPLAY.json').write_text(json.dumps({'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trust':0,'modules':records,'axiom_inspection_exit':r.returncode,'theorems_inspected':names,'baseline_rebuild_manifest_sha256':hashlib.sha256((A/'BASELINE_REBUILD.json').read_bytes()).hexdigest(),'dependency_search_path':env['LEAN_PATH']},indent=2)+'\n')
print('PASS AXIOMS',len(names),flush=True)
