#!/usr/bin/env python3
"""Author verification; accepted typed cache is read-only, not a cold replay."""
from pathlib import Path
import hashlib,json,re,subprocess,time,sys
P=Path(__file__).resolve().parent
modules=['AliasModel','AliasObstruction','ModelControls','AliasRelation','AliasExpansion','AliasPreservation','AliasSimulation','SimulationControls']
if '--typed' in sys.argv: modules += ['AliasTyped','AliasRuntime']
base=P.parents[2]/'formal/criterion-history-join/milestones/typed-history-v2'
# Derive workspace path explicitly from this known research layout.
base=P.parent.parent/'formal/criterion-history-join/milestones/typed-history-v2'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def verify_inputs():
 assert sha(base/'MANIFEST.json')=='8fef9a6bca00d9cfaeb4dda16dceb441307e90341de2ef96f0900bf001ab2f82'
 for r in json.loads((base/'MANIFEST.json').read_text())['files']:
  q=base/r['path'];assert q.stat().st_size==r['bytes'] and sha(q)==r['sha256'],q
verify_inputs(); identities={m:sha(P/(m+'.lean')) for m in modules};rows=[]
for m in modules:
 cmd=[str(P/'lean.sh'),'-o',str(P/'build'/(m+'.olean')),str(P/(m+'.lean'))];start=time.monotonic()
 p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=300)
 log=P/'evidence'/('suite-'+m+'.log');log.write_text(p.stdout)
 rows.append({'module':m,'source_sha256':identities[m],'command':cmd,'exit_code':p.returncode,'seconds':round(time.monotonic()-start,3),'log_sha256':sha(log)})
 print(m,p.returncode,flush=True)
 assert p.returncode==0 and not re.search(r'warning:|error:|sorryAx',p.stdout),p.stdout
audit=['import SimulationControls']+(['import AliasRuntime'] if '--typed' in sys.argv else [])
for m in modules:
 ns={'ModelControls':'SharedAlias.ModelControls','SimulationControls':'SharedAlias.SimulationControls','AliasTyped':'SharedAlias.Typed','AliasRuntime':'SharedAlias.Typed'}.get(m,'SharedAlias')
 for n in re.findall(r'\btheorem\s+([A-Za-z0-9_]+)',(P/(m+'.lean')).read_text()):audit.append('#print axioms '+ns+'.'+n)
auditFile=P/'controls'/'SuiteAxioms.lean';auditFile.write_text('\n'.join(audit)+'\n')
p=subprocess.run([str(P/'lean.sh'),str(auditFile)],stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=300);(P/'evidence/suite-axioms.log').write_text(p.stdout)
assert p.returncode==0 and not re.search(r'warning:|error:|sorryAx',p.stdout),p.stdout
axioms={}
for name,dep in re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",p.stdout):
 vals=[s.strip() for s in dep.split(',') if s.strip()];assert set(vals)<={'propext','Classical.choice','Quot.sound'};axioms[name]=vals
for name in re.findall(r"'([^']+)' does not depend on any axioms",p.stdout):axioms[name]=[]
assert len(axioms)==len(audit)-1-('--typed' in sys.argv),(len(axioms),len(audit))
verify_inputs();assert all(sha(P/(m+'.lean'))==identities[m] for m in modules)
receipt={'status':'PASS_AUTHOR_BUILD_STANDARD_AXIOMS','independent_review':False,'uses_read_only_accepted_typed_cache':True,'stages':rows,'axioms':axioms,'all_inputs_stable':True}
name='TYPED_AUTHOR_RECEIPT.json' if '--typed' in sys.argv else 'SIMULATION_AUTHOR_RECEIPT.json'
(P/'evidence'/name).write_text(json.dumps(receipt,indent=2)+'\n')
print('PASS',len(modules),'modules;',len(axioms),'axiom closures',flush=True)
