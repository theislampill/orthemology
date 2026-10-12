from pathlib import Path
import sys,importlib.util,json,hashlib,os,subprocess,datetime,re
sys.dont_write_bytecode=True
W=Path.cwd(); R=W/'hase-certificate-domain-independent-review-20261010'; V=R/'telescope-replay'; V.mkdir(exist_ok=False)
spec=importlib.util.spec_from_file_location('release',W/'hase-telescope-code-validity-20261010/verify_release.py'); p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
freeze=json.loads((p.V/'RELEASE_FREEZE.json').read_text()); pins=json.loads((p.V/'RELEASE_PINS.json').read_text()); allpins=pins+freeze['files']; p.b.check(allpins)
env=dict(os.environ,LEAN_PATH=':'.join(map(str,[V]+p.b.inherited_paths())))
rows=[]
for src in p.SOURCES:
 obj=V/(src.stem+'.olean'); run=subprocess.run([str(p.b.LEAN),'--trust=0','-o',str(obj),str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 log=V/(src.stem+'.log');log.write_text(run.stdout)
 assert run.returncode==0 and not any(x in run.stdout for x in ['sorryAx','error:','warning:']),str(log)
 if src.stem=='TelescopeValidityControls': assert run.stdout.strip().splitlines()==['[true, true, true, true, true, true]','[false, false, false, false]']
 if src.stem in ['TelescopeValidityAudit','TelescopeTransportAudit','ListNatTransportAudit']:
  ax=re.findall(r'depends on axioms: \[([^]]*)\]',run.stdout)
  assert len(ax)=={'TelescopeValidityAudit':8,'TelescopeTransportAudit':3,'ListNatTransportAudit':4}[src.stem]
  assert all(set(x.split(', '))-{'propext','Classical.choice','Quot.sound'}==set() for x in ax)
 rows.append({'module':src.stem,'source':p.b.rec(src),'object':p.b.rec(obj),'log':p.b.rec(log),'exit_code':run.returncode}); print('PASS '+src.stem,flush=True)
neg=[]
for m in p.MUTATIONS:
 src=p.R/'diagnostics'/(m+'.lean'); run=subprocess.run([str(p.b.LEAN),'--trust=0',str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT); log=V/(m+'.log');log.write_text(run.stdout)
 expected="tactic 'rfl' failed" if m=='WrongListCodecQualified' else "tactic 'decide' proved that the proposition"
 assert run.returncode!=0 and expected in run.stdout and 'error:' in run.stdout,str(log)
 neg.append({'module':m,'source':p.b.rec(src),'log':p.b.rec(log),'exit_code':run.returncode});print('REJECTED '+m,flush=True)
p.b.check(allpins)
receipt={'status':'PASS_TELESCOPE_LAYER_ONLY','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trust':0,'lean_version':subprocess.check_output([str(p.b.LEAN),'--version'],text=True).strip(),'baseline_rebuilt':False,'protected_inputs_mutated':False,'pins_verified_before_after':len(pins),'freeze_entries_verified_before_after':len(freeze['files']),'release_freeze':p.b.rec(p.V/'RELEASE_FREEZE.json'),'positive':rows,'negative':neg,'axiom_audits':15,'runtime_controls':10,'scope':'Exact retained Tel canonical validity; canonical decode2-reencode PR; generic ListNat transport. No ordinary source decoder equivalence or whole-checker PR or global certificate validity accepted.'}
(R/'TELESCOPE_REVIEW_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS telescope independent replay',flush=True)
