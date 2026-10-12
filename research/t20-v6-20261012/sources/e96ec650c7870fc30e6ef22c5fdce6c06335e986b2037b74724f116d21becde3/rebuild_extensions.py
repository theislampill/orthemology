import pathlib,os,subprocess,json,hashlib,datetime
R=pathlib.Path('private-locator:4bb2f72cdc070f304a86');F=pathlib.Path('private-locator:4b06887cf6b87610e5b8');T=F/'lean-4.19.0-linux/bin';sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();E=R/'evidence'
baseenv={**os.environ,'PATH':str(T)+':'+os.environ['PATH']};baseenv.pop('LEAN_SYSROOT',None);baseenv.pop('LEAN_PATH',None)
raw=subprocess.check_output([str(T/'lake'),'env','printenv','LEAN_PATH'],cwd=F,env=baseenv,text=True).strip()
paths=[str((F/pathlib.Path(p)).resolve()) if not pathlib.Path(p).is_absolute() else p for p in raw.split(':')]
paths=[p for p in paths if p!=str(F/'.lake/build/lib/lean')]
receipt={'scope':'Independent source-copy build of eight frontier modules and three law-stability modules','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'toolchain_sha256':sha(T/'lean'),'external_lean_path':paths,'modules':[]}
try:
 b=R/'frontier-fresh';b.mkdir(exist_ok=False)
 for m in ['RankTransport','LowerEnvelopeBudget','PERRefinement','PERPotentialFormula','MealyRefinement','MealySharpness','GuardedRefinement','BlockMismatch','Verification']:
  source=F/(m+'.lean');local=b/(m+'.lean');local.write_bytes(source.read_bytes())
  p=subprocess.run([str(T/'lean'),'-j1','-o',m+'.olean',m+'.lean'],cwd=b,env={**baseenv,'LEAN_PATH':':'.join([str(b)]+paths)},capture_output=True,timeout=240)
  (E/('frontier-'+m+'.stdout')).write_bytes(p.stdout);(E/('frontier-'+m+'.stderr')).write_bytes(p.stderr)
  receipt['modules'].append({'module':m,'source':str(source),'source_sha256':sha(source),'copy_sha256':sha(local),'exit_code':p.returncode,'stdout_sha256':sha(E/('frontier-'+m+'.stdout')),'stderr_sha256':sha(E/('frontier-'+m+'.stderr')),'artifact_sha256':sha(b/(m+'.olean')) if (b/(m+'.olean')).exists() else None})
  print(m,p.returncode,flush=True)
  if p.returncode:raise RuntimeError(p.stdout.decode()+p.stderr.decode())
 b=R/'measure-fresh';b.mkdir(exist_ok=False);M=pathlib.Path('private-locator:67a0368f452b0a176f36');P02=pathlib.Path('private-locator:41bb551746702dbd66a7')
 for m in ['TotalVariation','ResidualStability','AtomicPattern']:
  source=M/(m+'.lean');local=b/(m+'.lean');local.write_bytes(source.read_bytes())
  p=subprocess.run([str(T/'lean'),'-j1','-o',m+'.olean',m+'.lean'],cwd=b,env={**baseenv,'LEAN_PATH':':'.join([str(b),str(P02)]+paths)},capture_output=True,timeout=240)
  (E/('measure-'+m+'.stdout')).write_bytes(p.stdout);(E/('measure-'+m+'.stderr')).write_bytes(p.stderr)
  receipt['modules'].append({'module':m,'source':str(source),'source_sha256':sha(source),'copy_sha256':sha(local),'exit_code':p.returncode,'stdout_sha256':sha(E/('measure-'+m+'.stdout')),'stderr_sha256':sha(E/('measure-'+m+'.stderr')),'artifact_sha256':sha(b/(m+'.olean')) if (b/(m+'.olean')).exists() else None})
  print(m,p.returncode,flush=True)
  if p.returncode:raise RuntimeError(p.stdout.decode()+p.stderr.decode())
 receipt['status']='PASS_BOUNDED_EXTENSION_REPLAY'
except Exception as ex:receipt['status']='FAIL_CLOSED';receipt['failure']=repr(ex);raise
finally:
 receipt['ended_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();(E/'EXTENSION_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
