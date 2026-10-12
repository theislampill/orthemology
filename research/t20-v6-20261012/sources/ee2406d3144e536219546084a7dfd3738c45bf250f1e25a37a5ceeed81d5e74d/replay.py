from pathlib import Path
import os,sys,json,re,hashlib,subprocess
R=Path(__file__).resolve().parent; W=R.parent
L=W/'.toolchains/lean-4.19.0-linux/bin/lean'
env={**os.environ,**json.loads((R/'lean_env.json').read_text())}
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
records=json.loads((R/'REPLAY_RECORDS.json').read_text()) if (R/'REPLAY_RECORDS.json').exists() else {}
for mod in sys.argv[1:]:
    src=R/'sources'/(mod+'.lean')
    if not src.exists(): src=R/(mod+'.lean')
    obj=R/'fresh-lib'/(mod+'.olean'); log=R/'validation'/(mod+'.log')
    code=re.sub(r'/\-.*?\-/','',src.read_text(),flags=re.S)
    code=re.sub(r'--[^\n]*','',code); code=re.sub(r'"(?:\\.|[^"\\])*"','""',code)
    assert not re.findall(r'\b(sorry|admit|axiom|unsafe|implemented_by|native_decide|extern|skipKernelTC)\b',code),mod
    cmd=[str(L),'--trust=0','-o',str(obj),str(src)]
    p=subprocess.run(cmd,env=env,capture_output=True,text=True,cwd=W)
    out=p.stdout+p.stderr; log.write_text(out)
    print(mod,p.returncode,out,flush=True)
    assert p.returncode==0,(mod,out)
    assert not any(s in out for s in ['error:','warning:','sorryAx','Lean.ofReduceBool']),(mod,out)
    for ax in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',out,re.S):
        assert set(re.sub(r'\s+','',ax).split(','))<={'','propext','Classical.choice','Quot.sound'},(mod,ax)
    records[mod]={'source':str(src.relative_to(W)),'source_sha256':sha(src),
       'object':str(obj.relative_to(W)),'object_sha256':sha(obj),
       'log':str(log.relative_to(W)),'log_sha256':sha(log),
       'command':cmd,'exit_code':p.returncode,'trust_zero':True}
    (R/'REPLAY_RECORDS.json').write_text(json.dumps(records,indent=2)+'\n')
