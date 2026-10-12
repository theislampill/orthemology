from pathlib import Path
import hashlib,json,subprocess,os,time
R=Path(__file__).resolve().parents[1];BASE=R.parents[1];ML=BASE/'tranche2/toolchain/mathlib4';LEAN=BASE/'tranche2/toolchain/lean-4.19.0-linux/bin/lean';main=json.loads((R/'evidence/REPLAY_RESULT.json').read_text());assert main['status']=='PASS';build=R/main['build_directory'];libs=[build,ML/'.lake/build/lib/lean',*sorted(ML.glob('.lake/packages/*/.lake/build/lib/lean'))];env=dict(os.environ,LEAN_PATH=':'.join(map(str,libs)))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def compile(m,src,out):
 start=time.monotonic();p=subprocess.run([str(LEAN),'-j1','--root='+str(src),'-o',str(out/f'{m}.olean'),str(src/f'{m}.lean')],env=env,cwd=ML,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);return p,time.monotonic()-start
p,secs=compile('IndependentScaleAudit',R/'source',build);(R/'evidence/IndependentScaleAudit.log').write_text(p.stdout);ok=p.returncode==0 and not any(x in p.stdout for x in ['error:','sorryAx','PANIC']);print('IndependentScaleAudit',ok,p.stdout[-3000:] if not ok else '',flush=True)
result={'status':'PASS' if ok else 'FAIL','module':'IndependentScaleAudit','exit_code':p.returncode,'seconds':secs,'sha256':sha(R/'source/IndependentScaleAudit.lean')};(R/'evidence/SUPPLEMENT_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');assert ok
changes=[('missing_abs_budget','PolynomialBounds','∑ i, |c i|','∑ i, c i'),('inverted_head_scaling','ConstraintBounds','2*(B j+1)/head j','2*(B j+1)*head j'),('wrong_g_coefficient','PolynomialBounds','-(b^2+g^2)','(b^2+g^2)'),('wrong_bary_coefficient','ExplicitANDScale','![d.b-2*d.g,d.g-d.b','![d.b-d.g,d.g-d.b')]
results=[]
for name,m,old,new in changes:
 dest=R/'mutations'/name;dest.mkdir(parents=True,exist_ok=True);data=(R/'source'/f'{m}.lean').read_text();assert old in data;(dest/f'{m}.lean').write_text(data.replace(old,new));p,secs=compile(m,dest,dest);(dest/'compile.log').write_text(p.stdout);rejected=p.returncode!=0 and 'error:' in p.stdout;results.append({'name':name,'module':m,'rejected':rejected,'exit_code':p.returncode,'seconds':secs,'sha256':sha(dest/f'{m}.lean')});print(name,'REJECTED' if rejected else 'UNEXPECTED',flush=True)
out={'status':'PASS' if all(x['rejected'] for x in results) else 'FAIL','mutations':results};(R/'evidence/MUTATIONS.json').write_text(json.dumps(out,indent=2)+'\n');assert out['status']=='PASS'
