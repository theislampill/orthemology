from pathlib import Path
import json,hashlib,subprocess,sys,tempfile,shutil,datetime,re
D=Path(__file__).resolve().parent;P=D.parents[1]/'t20-consolidation-20261011/projection/package-v4';V=P.with_name('package-v3');h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
now={p.relative_to(P).as_posix():{'sha256':h(p),'bytes':p.stat().st_size} for p in P.rglob('*') if p.is_file()};before=json.loads((D/'EXECUTED_CANDIDATE_FILES.json').read_text());diff=sorted(p for p in set(before)|set(now) if before.get(p)!=now.get(p));specs=json.loads((P/'depth/PORTABLE_TARGETS.json').read_text())['suites'];continuity={}
for name,spec in specs.items():
 prefix='replay/'+spec['directory']+'/'
 closure={p:s for p,s in now.items() if p.startswith(prefix)};old={p:s for p,s in before.items() if p.startswith(prefix)}
 continuity[name]={'exact_closure_unchanged':closure==old,'runner_unchanged':now['replay_selected.py']==before['replay_selected.py'],'changed_paths':[p for p in diff if p.startswith(prefix)]}
rows=[]
with tempfile.TemporaryDirectory(prefix='t20-final-refresh-') as t:
 q=Path(t)/'package';shutil.copytree(P,q)
 for name,args in [('final-validator',['validate_package.py']),('final-depth-validator',['validate_depth.py']),('final-tool-tests',['-m','unittest','discover','-s','tool-tests','-v']),('final-occurrence',['replay_selected.py','--suite','depth-occurrence-warrant'])]:
  r=subprocess.run([sys.executable,'-B',*args],cwd=q,capture_output=True,text=True,timeout=90);(D/(name+'.stdout')).write_text(r.stdout);(D/(name+'.stderr')).write_text(r.stderr);rows.append({'name':name,'exit_code':r.returncode,'stdout_sha256':hashlib.sha256(r.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(r.stderr.encode()).hexdigest()});print(name,r.returncode,flush=True)
 # Actual final whitespace diagnostics, compared with disclosed preserved-source advisories.
 subprocess.run(['git','init','-q',str(q)],check=True);subprocess.run(['git','-C',str(q),'add','--all'],check=True);r=subprocess.run(['git','-C',str(q),'diff','--cached','--check'],capture_output=True,text=True)
 diagnostics=[]
 for line in r.stdout.splitlines():
  m=re.match(r'(.+):(\d+): (.+)',line)
  if m:diagnostics.append({'path':m[1],'line':int(m[2]),'diagnostic':m[3]})
 expected=json.loads((P/'depth/WHITESPACE_VERIFICATION.json').read_text());exp=[d for a in expected['advisories'] for d in a['diagnostics']];whitespace={'exit_code':r.returncode,'diagnostics':diagnostics,'exactly_disclosed':sorted(diagnostics,key=str)==sorted(exp,key=str)}
base=json.loads((D/'V3_BASELINE_FILES.json').read_text());flags=[]
for rel in now:
 if now[rel]==base.get(rel):continue
 p=P/rel
 if p.suffix not in ['.md','.json','.txt','.py']:continue
 text=p.read_text(errors='replace')
 for pat in [r'https?://[^\s"<>]*(?:X-Amz-|[?&]sig=|[?&]token=)[^\s"<>]*',r'/workspace/[^\s"<>]+',r'private-locator:b1f29effa90a29bba636[^\s"<>]+',r'-----BEGIN .*PRIVATE KEY',r'OWNER_PRO_THREAD_INSTRUCTIONS']:
  hits=re.findall(pat,text)
  if hits:flags.append({'file':rel,'pattern':pat,'count':len(hits)})
post={p.relative_to(P).as_posix():{'sha256':h(p),'bytes':p.stat().st_size} for p in P.rglob('*') if p.is_file()};ok=not any(r['exit_code'] for r in rows) and now==post and not flags and whitespace['exactly_disclosed'] and all(x['runner_unchanged'] and (x['exact_closure_unchanged'] or n=='depth-occurrence-warrant') for n,x in continuity.items())
res={'status':'PASS' if ok else 'FAIL','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_sha256':now['PACKAGE_CONTENTS.json']['sha256'],'unchanged_during_final_checks':now==post,'changed_since_initial_replay_snapshot':diff,'replay_continuity':continuity,'runs':rows,'privacy_scan_flags':flags,'whitespace':whitespace,'scope':'Seven unchanged new replay closures inherit this reviewer execution; occurrence rerun after omission of unused private-path red-stage log. No whole-corpus, fresh Lean, CI or all-OS qualification.'};(D/'FINAL_VERIFICATION.json').write_text(json.dumps(res,indent=2)+'\n');print(res['status'],res['manifest_sha256']);sys.exit(not ok)
