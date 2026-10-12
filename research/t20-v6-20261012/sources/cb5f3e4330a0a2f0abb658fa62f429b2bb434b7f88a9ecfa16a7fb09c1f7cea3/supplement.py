from pathlib import Path
import hashlib,json,subprocess,os,time
R=Path(__file__).resolve().parents[1];BASE=R.parents[1];ML=BASE/'tranche2/toolchain/mathlib4';LEAN=BASE/'tranche2/toolchain/lean-4.19.0-linux/bin/lean';main=json.loads((R/'evidence/REPLAY_RESULT.json').read_text());assert main['status']=='PASS';build=R/main['build_directory'];libs=[build,ML/'.lake/build/lib/lean',*sorted(ML.glob('.lake/packages/*/.lake/build/lib/lean'))];env=dict(os.environ,LEAN_PATH=':'.join(map(str,libs)))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compile(m,src,out):
 start=time.monotonic();p=subprocess.run([str(LEAN),'-j1','--root='+str(src),'-o',str(out/f'{m}.olean'),str(src/f'{m}.lean')],env=env,cwd=ML,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);return p,time.monotonic()-start
p,secs=compile('IndependentMixedAudit',R/'source',build);(R/'evidence/IndependentMixedAudit.log').write_text(p.stdout);ok=p.returncode==0 and not any(x in p.stdout for x in ['error:','sorryAx','PANIC']);print('IndependentMixedAudit',ok,p.stdout[-3000:] if not ok else '',flush=True)
result={'status':'PASS' if ok else 'FAIL','module':'IndependentMixedAudit','exit_code':p.returncode,'seconds':secs,'sha256':sha(R/'source/IndependentMixedAudit.lean')};(R/'evidence/SUPPLEMENT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');assert ok
changes=[('wrong_high_sign','MixedHull','p 4+eps*(h 4-kappa h)-eps^2*g/2','p 4+eps*(h 4-kappa h)+eps^2*g/2'),('dropped_high_energy','MixedScore','(truth i 2+truth i 3-p 2-p 3)*g+normalEnergy h+eps','(truth i 2+truth i 3-p 2-p 3)*g+eps'),('wrong_primal','CouplingLPValues','![12/41,12/41,3/328','![13/41,13/41,3/328'),('unbound_cubic_data','CouplingLPValues','1+9*(1/4-v 0)-3*(1/4-v 1)','1+8*(1/4-v 0)-3*(1/4-v 1)')]
results=[]
for name,m,old,new in changes:
 dest=R/'mutations'/name;dest.mkdir(parents=True,exist_ok=True);data=(R/'source'/f'{m}.lean').read_text();assert old in data;(dest/f'{m}.lean').write_text(data.replace(old,new));p,secs=compile(m,dest,dest);(dest/'compile.log').write_text(p.stdout);rejected=p.returncode!=0 and 'error:' in p.stdout;results.append({'name':name,'module':m,'rejected':rejected,'exit_code':p.returncode,'seconds':secs,'sha256':sha(dest/f'{m}.lean')});print(name,'REJECTED' if rejected else 'UNEXPECTED',flush=True)
out={'status':'PASS' if all(x['rejected'] for x in results) else 'FAIL','mutations':results};(R/'evidence/MUTATIONS.json').write_text(json.dumps(out,indent=2)+'\n');assert out['status']=='PASS'
