from pathlib import Path
import re,os,subprocess,json,hashlib,sys
A=Path(sys.argv[1]).resolve();prefix=sys.argv[2];B=A.parents[2];L=B/'tranche2/toolchain/lean-4.19.0-linux/bin/lean';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip())
text=(A/'Controls.lean').read_text();targets=[prefix+t for t in re.findall(r'^theorem\s+(\w+)',text,re.M)]
r=subprocess.run([str(L),'-j1','--root='+str(A),'-o',str(A/'build/Controls.olean'),str(A/'Controls.lean')],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(A/'logs/Controls.log').write_text(r.stdout);assert r.returncode==0,r.stdout
p=A/'ControlsReadback.lean';p.write_text('import Controls\n'+''.join('#check '+t+'\n#print axioms '+t+'\n' for t in targets))
r2=subprocess.run([str(L),'-j1',str(p)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);(A/'logs/ControlsReadback.log').write_text(r2.stdout)
entries=re.findall(r"'([^']+)' (depends on axioms: \[[^\]]*\]|does not depend on any axioms)",r2.stdout)
assert r2.returncode==0 and [x for x,_ in entries]==targets,(r2.returncode,r2.stdout)
assert 'sorryAx' not in r2.stdout
for _,x in entries:
 if '[' in x:assert set(a.strip() for a in x.split('[')[1].strip(']').split(','))<=set(['propext','Classical.choice','Quot.sound'])
rec={'status':'PASS','targets':targets,'count':len(targets),'source_sha256':sha(A/'Controls.lean'),'olean_sha256':sha(A/'build/Controls.olean'),'compile_exit':r.returncode,'compile_log_sha256':sha(A/'logs/Controls.log'),'readback_exit':r2.returncode,'readback_log_sha256':sha(A/'logs/ControlsReadback.log'),'allowed_axioms':['propext','Classical.choice','Quot.sound']};(A/'CONTROL_RESULT.json').write_text(json.dumps(rec,indent=2)+'\n');print(json.dumps(rec))
