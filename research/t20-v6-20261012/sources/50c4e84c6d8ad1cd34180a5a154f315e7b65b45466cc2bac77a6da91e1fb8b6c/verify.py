from pathlib import Path
import os, json, subprocess, hashlib, tempfile, datetime
H=Path(__file__).resolve().parent; W=H.parent
B=W/'rational-threshold-formal-extension-20261011'
LEAN=W/'.toolchains/lean-4.19.0-linux/bin/lean'
O=Path(tempfile.mkdtemp(prefix='replay-', dir=H))
E=dict(os.environ,LEAN_PATH=str(O)+':'+(B/'lean_path.txt').read_text().strip())
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
sources=[H/'weights/BinaryWeights.lean',H/'compiler/UnaryPrefixRealisation.lean',H/'UnaryShiftLaw.lean',H/'RationalShiftRealisation.lean',H/'Sigma2ThresholdRealisation.lean']
rec=[]
for p in sources:
 r=subprocess.run([str(LEAN),'--trust=0','-o',str(O/(p.stem+'.olean')),str(p)],env=E,capture_output=True,text=True,cwd=W)
 log=r.stdout+r.stderr;(O/(p.stem+'.log')).write_text(log)
 assert r.returncode==0 and 'sorryAx' not in log and 'warning:' not in log,(p,log)
 rec.append({'module':p.stem,'source':str(p.relative_to(W)),'source_sha256':digest(p),'object_sha256':digest(O/(p.stem+'.olean')),'exit_code':r.returncode,'log':str((O/(p.stem+'.log')).relative_to(W))})
negative=[]
for label,p,old,new in [
 ('wrong_endpoint',sources[0],'if a = b then true else digit a b i','if a = b then false else digit a b i'),
 ('missing_zero_terminator_drop',sources[1],'(scannedBits n word).drop (i+1)','(scannedBits n word).drop i'),
 ('unreset_base_word',sources[1],'F a (n-i-1) (suffixWord n word i)','F a (n-i-1) word'),
 ('reversed_law_rows',sources[2],'if digits i then id else base','if digits i then base else id'),
 ('sigma_zero_threshold',sources[4],'0 < r → r ≤ 1 →','0 ≤ r → r ≤ 1 →'),
 ('sigma_threshold_above_one',sources[4],'0 < r → r ≤ 1 →','0 < r → r ≤ 2 →')]:
 s=p.read_text();assert s.count(old)==1,(label,s.count(old))
 q=O/(label+'.lean');q.write_text(s.replace(old,new))
 r=subprocess.run([str(LEAN),'--trust=0',str(q)],env=E,capture_output=True,text=True,cwd=W)
 log=r.stdout+r.stderr;(O/(label+'.log')).write_text(log)
 assert r.returncode!=0,(label,'mutant unexpectedly passed')
 negative.append({'control':label,'rejected':True,'exit_code':r.returncode,'log':str((O/(label+'.log')).relative_to(W))})
base=json.loads((B/'BASELINE_REBUILD.json').read_text())
for m in base['modules']:
 p=B/'baseline'/Path(m['module'].replace('.','/')+'.lean')
 assert digest(p)==m['source_sha256'],p
upper=json.loads((B/'AUTHOR_REPLAY.json').read_text())
for m in upper['positive']:
 p=W/m['source']['path'];assert digest(p)==m['source']['sha256'],p
receipt={'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lean_version':subprocess.check_output([str(LEAN),'--version'],text=True).strip(),'trust':0,'positive':rec,'negative':negative,'baseline_sources_unchanged':len(base['modules']),'frozen_upper_sources_unchanged':len(upper['positive']),'output':str(O.relative_to(W)),'scope':'Alternative unary-tag fixed-joint-PR-family rational shift, not literal Python compile_shift verification.'}
(H/'AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
