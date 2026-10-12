#!/usr/bin/env python3
"""Separate supplementary diagonal control; never modifies the matrix subject."""
import pathlib,json,os,subprocess,hashlib,sys,re,shutil
root=pathlib.Path(__file__).resolve().parent;receipt=pathlib.Path(sys.argv[1]).resolve();r=json.loads(receipt.read_text());assert r['status']=='PASS'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
assert sha(root/'NonPRBoundary.lean')=='23bb1d13eade0f4370c034224a6ca2afb4115e8fb784d9140d2bb4a09ed29857'
out=receipt.parent/'sharpness';out.mkdir(exist_ok=True);shutil.copy2(root/'NonPRBoundary.lean',out/'NonPRBoundary.lean')
env={**os.environ,'LEAN_PATH':str(out)+':'+':'.join(r['LEAN_PATH'])};lean=r['builds'][0]['command'][0]
names=['P02.Codec.NonPRBoundary.evaluateIndex_lt_two','P02.Codec.NonPRBoundary.evaluateIndex_not_primrec']
(out/'SharpnessTypes.lean').write_text('import NonPRBoundary\nset_option pp.explicit true\nset_option pp.fullNames true\n'+''.join('#check @'+n+'\n#print axioms '+n+'\n' for n in names))
commands=[]
for m in ['NonPRBoundary','SharpnessTypes']:
 cmd=[lean,'-j1','--root='+str(out),'-o',str(out/(m+'.olean')),str(out/(m+'.lean'))]
 p=subprocess.run(cmd,cwd=out,env=env,text=True,capture_output=True,timeout=120);log=p.stdout+p.stderr;(out/(m+'.log')).write_text(log);commands.append({'module':m,'command':cmd,'exit':p.returncode});assert p.returncode==0,log
text=(out/'SharpnessTypes.log').read_text();ax={n:[v.strip() for v in vs.split(',') if v.strip()] for n,vs in re.findall(r"'(.*)' depends on axioms:\s*\[([^\]]*)\]",text)}
ax.update({n:[] for n in re.findall(r"'(.*)' does not depend on any axioms",text)})
assert set(ax)==set(names) and all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in ax.values())
result={'status':'PASS','scope':'Separate two-theorem diagonal sharpness control for exact evaluateIndex; not a non-Primrec theorem for membershipMatrix','source_sha256':sha(out/'NonPRBoundary.lean'),'independent_matrix_receipt_sha256':sha(receipt),'axioms':ax,'commands':commands}
(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
