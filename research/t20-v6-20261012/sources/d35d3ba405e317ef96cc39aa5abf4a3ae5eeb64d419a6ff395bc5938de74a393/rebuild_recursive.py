import pathlib,os,subprocess,json,hashlib,re
R=pathlib.Path('private-locator:4bb2f72cdc070f304a86');E=R/'evidence';B=R/'recursive-fresh';paths=json.loads((E/'EXTENSION_REPLAY.json').read_text())['external_lean_path'];base='private-locator:053d4a5d3baa0e7b417c';T=pathlib.Path('private-locator:d97af50b47918e94879b');env={**os.environ,'LEAN_PATH':':'.join([str(B),base]+paths)};env.pop('LEAN_SYSROOT',None);rows=[];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for m in ['P01RecursiveModel','P01RecursiveAssertions','FrontierAudit','IndependentRecursiveControls']:
 p=subprocess.run([str(T/'lean'),'-j1','-o',m+'.olean',m+'.lean'],cwd=B,env=env,capture_output=True,timeout=180)
 (E/('recursive-'+m+'.stdout')).write_bytes(p.stdout);(E/('recursive-'+m+'.stderr')).write_bytes(p.stderr)
 rows.append({'module':m,'source_sha256':sha(B/(m+'.lean')),'exit_code':p.returncode,'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_sha256':hashlib.sha256(p.stderr).hexdigest(),'artifact_sha256':sha(B/(m+'.olean')) if (B/(m+'.olean')).exists() else None});(E/'RECURSIVE_REPLAY.json').write_text(json.dumps({'status':'IN_PROGRESS' if p.returncode==0 else 'FAIL_CLOSED','modules':rows},indent=2)+'\n');print(m,p.returncode,flush=True)
 if p.returncode:print(p.stdout.decode());raise SystemExit(1)
text=(E/'recursive-FrontierAudit.stdout').read_text();names=re.findall(r'^AUDIT_BEGIN (.+)$',text,re.M);assert len(names)==len(set(names));assert 'sorryAx' not in text
(E/'RECURSIVE_REPLAY.json').write_text(json.dumps({'status':'PASS_BOUNDED_RECURSIVE_AUDIT','modules':rows,'audited_target_count':len(names)},indent=2)+'\n')
