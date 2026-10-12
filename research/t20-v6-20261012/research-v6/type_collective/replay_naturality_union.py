import pathlib,json,subprocess,hashlib,os,time
root=pathlib.Path(__file__).resolve().parent;ws=root.parents[1];out=root/'fresh_lean/naturality_union';stage=json.loads((out/'STAGING.json').read_text());assert not stage['obstructions'];lean=ws/'.toolchains/lean-4.19.0-linux/bin/lean';receipt={'scope':'Fresh exact-source union for SourceNaturalityNegative; external pinned Lean/Mathlib libraries retained; no original research olean reuse.','compiler':str(lean),'compiler_sha256':hashlib.sha256(lean.read_bytes()).hexdigest(),'modules':[],'status':'RUNNING'};env=dict(os.environ);env['LEAN_PATH']=str(out)+':'+env.get('LEAN_PATH','');modules=stage['order']+['SourceNaturalityNegative']
for name in modules:
 src=out/(name+'.lean');cmd=[str(lean),'--trust=0','-o',name+'.olean',name+'.lean'];start=time.time();p=subprocess.run(cmd,cwd=out,env=env,capture_output=True,text=True);log=out/(name+'.log');log.write_text(p.stdout+p.stderr);entry={'module':name,'source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'command':cmd,'exit_code':p.returncode,'seconds':time.time()-start,'log_path':str(log),'log_sha256':hashlib.sha256(log.read_bytes()).hexdigest()};obj=out/(name+'.olean')
 if obj.exists():entry['olean_sha256']=hashlib.sha256(obj.read_bytes()).hexdigest()
 receipt['modules'].append(entry);(out/'FRESH_COMPILATION.json').write_text(json.dumps(receipt,indent=2)+'\n');print(name,p.returncode,flush=True)
 if p.returncode:
  receipt['status']='STOPPED_AT_FIRST_FAILED_MODULE';(out/'FRESH_COMPILATION.json').write_text(json.dumps(receipt,indent=2)+'\n');break
else:
 receipt['status']='ALL_PASS';(out/'FRESH_COMPILATION.json').write_text(json.dumps(receipt,indent=2)+'\n')
