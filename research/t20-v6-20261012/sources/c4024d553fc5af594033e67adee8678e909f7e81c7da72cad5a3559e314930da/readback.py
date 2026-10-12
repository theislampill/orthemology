from pathlib import Path
import re,json,os,subprocess,hashlib,sys
A=Path(sys.argv[1]).resolve();base=A.parents[2];sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
mods=sys.argv[2:];targets=[]
for mod in mods:
 text=(A/'snapshot'/(mod+'.lean')).read_text()
 text=re.sub(r'/-[\s\S]*?-/|--[^\n]*','',text)
 prefix='Orthemology.Tranche3.PhysicalCost.' if mod=='PhysicalCostConservation' else 'Orthemology.Tranche3.'
 if mod in ['ObserverAbstraction','GuardedObserver']: prefix='Orthemology.CertifiedObserver.'
 if mod=='ContextualObserver': prefix='Orthemology.CertifiedObserver.ObserverFamily.'
 names=re.findall(r'^\s*(?:noncomputable\s+)?(?:def|lemma|theorem|instance)\s+([A-Za-z_][\w]*)',text,re.M)
 for name in names:targets.append(prefix+name)
 if mod=='ObserverAbstraction': targets.append('Orthemology.CertifiedObserver.Simulation')
 if mod=='GuardedObserver': targets.append('Orthemology.CertifiedObserver.GuardedSimulation')
 if mod=='ContextualObserver': targets.append('Orthemology.CertifiedObserver.ObserverFamily')
if A.name=='physical-budget':
 targets += ['Orthemology.Tranche2.'+t for t in ['guarded_live_stopped_controller_budget','recorded_nat_charge_transfer','recorded_expected_charge_bound','recursive_recorded_all_post_nonempty','recursivePhysicalAction_measurable','stopped_bad_count_le_planned','phaseNext_actual_support','phaseNext_rank_decreases']]
source='\n'.join('import '+m for m in mods)+'\nset_option pp.universes true\nset_option pp.explicit true\n'+''.join('#check '+t+'\n#print '+t+'\n#print axioms '+t+'\n' for t in targets)
p=A/'Readback.lean';p.write_text(source);env=dict(os.environ,LEAN_PATH=(A/'LEAN_PATH.txt').read_text().strip());r=subprocess.run([str(base/'tranche2/toolchain/lean-4.19.0-linux/bin/lean'),'-j1',str(p)],env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=A/'logs/Readback.log';log.write_text(r.stdout)
axiomlines=re.findall(r"'([^']+)' (depends on axioms: \[[^\]]*\]|does not depend on any axioms)",r.stdout)
assert r.returncode==0 and len(axiomlines)==len(targets),(r.returncode,len(axiomlines),len(targets),r.stdout[-2000:])
assert [name for name,_ in axiomlines]==targets
assert 'sorryAx' not in r.stdout
for name,line in axiomlines:
 if 'depends on axioms:' in line:
  axioms=line.split('depends on axioms:')[1].strip().strip('[]').split(',')
  assert all(a.strip() in ['propext','Classical.choice','Quot.sound'] for a in axioms),(name,line,axioms)
record={'status':'PASS','targets':targets,'target_count':len(targets),'axiom_readback_count':len(axiomlines),'axiom_free_count':sum('does not depend' in s for _,s in axiomlines),'source_sha256':sha(p),'log_sha256':sha(log),'exit':r.returncode,'allowed_axioms':['propext','Classical.choice','Quot.sound']}
(A/'READBACK_RESULT.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))
