from pathlib import Path
import datetime,hashlib,json,os,subprocess,sys,tempfile
R=Path(__file__).resolve().parent;W=R.parent
mods=['RationalThresholdCuts','RationalThresholdComputable','RationalThresholdUniform','RationalThresholdDefect','RationalThresholdControls']
OUT=Path(tempfile.mkdtemp(prefix='candidate-',dir=R));(OUT/'sources').mkdir()
env=dict(os.environ,LEAN_PATH=str(OUT)+':'+(R/'lean_path.txt').read_text())
rec=[]
for m in mods:
 src=R/(m+'.lean');(OUT/'sources'/src.name).write_bytes(src.read_bytes())
 cmd=[str(W/'.toolchains/lean-4.19.0-linux/bin/lean'),'--trust=0','-o',str(OUT/(m+'.olean')),str(src)]
 p=subprocess.run(cmd,cwd=W,env=env,capture_output=True,text=True);log=OUT/(m+'.log');log.write_text(p.stdout+p.stderr)
 rec.append({'module':m,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'exit_code':p.returncode,'log':str(log.relative_to(R))})
 print(m,p.returncode,flush=True)
 if p.returncode: print(p.stdout+p.stderr,flush=True); break
receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trust':0,'status':'PASS' if len(rec)==len(mods) and not rec[-1]['exit_code'] else 'FAIL','output':str(OUT),'modules':rec}
(OUT/'RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
(R/'LATEST_CANDIDATE.json').write_text(json.dumps(receipt,indent=2)+'\n')
sys.exit(0 if receipt['status']=='PASS' else 1)
