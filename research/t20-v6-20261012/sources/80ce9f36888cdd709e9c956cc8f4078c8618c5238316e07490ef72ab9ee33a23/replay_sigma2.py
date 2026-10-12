from pathlib import Path
import json,os,subprocess,hashlib
R=Path(__file__).resolve().parent;W=R.parent;O=R/'kernel';B=W/'rational-threshold-formal-extension-20261011';A=W/'rational-shift-realisation-20261011'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
env=dict(os.environ,LEAN_PATH=str(O)+':'+(B/'lean_path.txt').read_text().strip());lean=W/'.toolchains/lean-4.19.0-linux/bin/lean'
for m in json.loads((R/'REPLAY.json').read_text())['modules']:assert sha(W/m['source'])==m['source_sha256']
p=A/'Sigma2ThresholdRealisation.lean';h=sha(p)
r=subprocess.run([str(lean),'--trust=0','-o',str(O/'Sigma2ThresholdRealisation.olean'),str(p)],cwd=W,env=env,text=True,capture_output=True)
(O/'Sigma2ThresholdRealisation.log').write_text(r.stdout+r.stderr)
assert r.returncode==0,(r.stdout,r.stderr)
assert sha(p)==h
assert 'sorryAx' not in r.stdout and '[propext, Classical.choice, Quot.sound]' in ' '.join(r.stdout.split())
results=[]
for name,statement in [('WrongZeroSigma2Threshold','(0 : ℝ) < 0 ↔ True'),('WrongAboveOneSigma2Threshold','(1 : ℝ) < 2 ↔ False')]:
 q=R/(name+'.lean');q.write_text('import Sigma2ThresholdRealisation\nexample : '+statement+' := by norm_num\n')
 s=subprocess.run([str(lean),'--trust=0',str(q)],cwd=W,env=env,text=True,capture_output=True)
 (O/(name+'.negative.log')).write_text(s.stdout+s.stderr)
 assert s.returncode!=0 and 'unsolved goals' in s.stdout,(name,s.stdout,s.stderr)
 results.append({'name':name,'source_sha256':sha(q),'exit_code':s.returncode})
(R/'SIGMA2_REPLAY.json').write_text(json.dumps({'module':'Sigma2ThresholdRealisation','source_sha256':h,'object_sha256':sha(O/'Sigma2ThresholdRealisation.olean'),'trust':0,'exit_code':r.returncode,'axiom_query':'OrthemologyRationalShift.exists_primrec_sigma2_threshold_reduction','axioms':['propext','Classical.choice','Quot.sound'],'negative_controls':results,'unchanged_four_source_hashes_rechecked':True},indent=2)+'\n')
print('PASS fifth module, axioms, two endpoint rejections')
