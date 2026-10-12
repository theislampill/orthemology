from pathlib import Path
import json,hashlib,subprocess,os,re,zipfile,time
R=Path(__file__).resolve().parent; P=Path('private-locator:6e1cdd2685640ba2eef0');M=Path('private-locator:45dfd5c4544eed9a5f10')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=json.loads((R/'manifest.json').read_text());env={**os.environ};exec_env=subprocess.check_output(['bash','-c','source '+str(R/'env.sh')+'; env -0']);env.update(dict(v.decode().split('=',1) for v in exec_env.split(b'\0') if b'=' in v))
with zipfile.ZipFile(M.parent/'Mealy_Measure_Bridge_Stage1_20260930.zip') as z:
 for p in M.rglob('*'):
  if p.is_file():
   name=next((n for n in z.namelist() if n.endswith('/'+str(p.relative_to(M))) or n==str(p.relative_to(M))),None)
   assert name and z.read(name)==p.read_bytes(),str(p)
print('ARCHIVE_CONTENTS_MATCH_SEALED_DIRECTORY',flush=True)
controls=[]
for seal in ['receipts/loop-20260930T142933Z/LOOP_RESULT.json','receipts/sigma2-20260930T144631Z/SIGMA2_RESULT.json']:
 data=json.loads((P/seal).read_text());audit='LoopAudit' if 'loop-' in seal else 'Sigma2Audit'
 out=(R/'receipts'/(audit+'.log')).read_text();seen={n:[x.strip() for x in a.split(',') if x.strip()] for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",out)}
 for n in re.findall(r"'([^']+)' does not depend on any axioms",out):seen[n]=[]
 assert set(seen)=={t['declaration'] for t in data['targets']}
 assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in seen.values())
 print(audit,'TARGETS',len(seen),'AXIOM_CEILING_OK',flush=True)
 for c in data['negative_controls']:
  p=P/'negative-controls'/(c['name']+'.lean'); assert sha(p)==c['source_sha256']
  local=R/'sources'/'controls'/p.name;local.parent.mkdir(exist_ok=True);local.write_bytes(p.read_bytes())
  cmd=['lean','-j1','--root='+str(R/'sources'),str(local)];t=time.time();proc=subprocess.run(cmd,env=env,cwd=R/'sources',capture_output=True,text=True)
  (R/'receipts'/(c['name']+'.log')).write_text(proc.stdout+proc.stderr)
  assert proc.returncode==c['exit'],(c['name'],proc.stdout,proc.stderr)
  if proc.returncode:assert 'unsolved goals' in proc.stdout or 'proved that the proposition' in proc.stdout
  controls.append({'name':c['name'],'exit':proc.returncode,'command':cmd,'seconds':time.time()-t,'sha256':sha(local)})
  print('CONTROL_OK',c['name'],proc.returncode,flush=True)
vm=(R/'receipts'/'Verification.log').read_text();seen={n: [x.strip() for x in a.split(',') if x.strip()] for n,a in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",vm)}
for n in re.findall(r"'([^']+)' does not depend on any axioms",vm):seen[n]=[]
expected={'Orthemology.Frontier.MealyMeasure.'+l.removeprefix('#print axioms ') for l in (M/'Verification.lean').read_text().splitlines() if l.startswith('#print axioms ')}
assert set(seen)==expected;assert all(set(a)<={'propext','Classical.choice','Quot.sound'} for a in seen.values())
print('Mealy','TARGETS',len(seen),'AXIOM_CEILING_OK',flush=True)
(R/'CONTROL_RESULTS.json').write_text(json.dumps(controls,indent=2)+'\n')
