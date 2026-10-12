from pathlib import Path
import os, subprocess, json, hashlib, shutil, re, datetime, time
W=Path(__file__).resolve().parent.parent; R=Path(__file__).resolve().parent; C=W/'hase-coded-rule-templates-20261010'; O=R/'output'; L=W/'.toolchains/lean-4.19.0-linux/bin/lean'
def rec(p):return {'path':str(p.relative_to(W)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}
def verify(pins):
 for v in pins: assert rec(W/v['path'])==v,v['path']
base=subprocess.check_output(['bash','-c','source hase-source-family-computability-20261010/env.sh; printf "__PATH__%s" "$LEAN_PATH"'],cwd=W,text=True).split('__PATH__',1)[1]
roots=[W/d/'validation' for d in ['hase-coded-rule-templates-20261010','hase-certificate-code-validity-20261010','hase-auxiliary-checker-computability-20261010','hase-telescope-code-validity-20261010','hase-coded-mixed-transformations-20261010','hase-exact-syntax-validity-20261010','hase-coded-poly-transformations-20261010','hase-coded-scope-computability-20261010']]+[Path(x) for x in base.split(':') if x]
roots=list(dict.fromkeys(roots));env={**os.environ,'LEAN_PATH':':'.join(map(str,[O]+roots))}
(R/'env.json').write_text(json.dumps({'lean':str(L),'LEAN_PATH':env['LEAN_PATH']},indent=2)+'\n')
manifest=R/'sources/ImportManifest.lean';manifest.write_text('import RuleConclusionCode\nimport RulePremisesCode\nimport RuleSideCode\nopen Lean in\nrun_cmd do\n  let env ← getEnv\n  for name in env.header.moduleNames do\n    logInfo m!"DEPENDENCY {name}"\n')
p=subprocess.run([str(L),'--trust=0',str(manifest)],cwd=W,env=env,capture_output=True,text=True);assert p.returncode==0,p.stdout+p.stderr;(O/'ImportManifest.baseline.log').write_text(p.stdout+p.stderr)
mods=re.findall(r'DEPENDENCY (\S+)',p.stdout);search=roots+[L.parent.parent/'lib/lean'];objects=[]
for m in mods:
 rel=Path(m.replace('.','/')+'.olean');f=next((d/rel for d in search if (d/rel).exists()),None);assert f,m;objects.append(rec(f))
core=json.loads((C/'validation/CORE_SOURCE_FREEZE.json').read_text())['files']; verify(core)
additional=[C/'validation/CORE_SOURCE_FREEZE.json',L,W/'hase-joint-certificate-checker-20261010/CertificateRules.lean',W/'hase-joint-certificate-checker-20261010/generated_rule_metadata.json']
selected=[W/'hase-telescope-code-validity-20261010'/f'{n}.lean' for n in ['TelescopeNatTransport','ListNatCodeTransport']]+[W/'hase-certificate-code-validity-20261010/CertificateDescriptions.lean']+[C/f'{n}.lean' for n in ['PolyTemplates','TypeTemplates','RuleCodeBasics','RuleConclusionCode','RulePremisesCode','RuleSideCode']]
pins=list({p['path']:p for p in core+objects+[rec(x) for x in additional+selected]}.values());verify(pins);(R/'REVIEW_INPUT_PINS.json').write_text(json.dumps(pins,indent=2)+'\n');print('PINS_BEFORE',len(pins),flush=True)
records=[]
for src in selected:
 copy=R/'sources'/src.name;shutil.copy2(src,copy);obj=O/(src.stem+'.olean');assert not obj.exists();t=time.monotonic();cmd=[str(L),'--trust=0','-o',str(obj),str(copy)];p=subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=O/(src.stem+'.log');log.write_text(p.stdout)
 records.append({'module':src.stem,'original':rec(src),'source':rec(copy),'object':rec(obj) if obj.exists() else None,'log':rec(log),'exit_code':p.returncode,'seconds':time.monotonic()-t,'command':cmd});(R/'PARTIAL_REPLAY.json').write_text(json.dumps(records,indent=2)+'\n')
 assert p.returncode==0 and not any(t in p.stdout for t in ['sorryAx','error:','warning:']),str(log);print('PASS',src.stem,flush=True)
verify(pins);(R/'SELECTIVE_REPLAY.json').write_text(json.dumps({'status':'PASS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'lean_version':subprocess.check_output([str(L),'--version'],text=True).strip(),'trust':0,'pins_before_after':len(pins),'baseline_rebuilt':False,'positive':records},indent=2)+'\n');print('PASS_REPLAY',flush=True)
