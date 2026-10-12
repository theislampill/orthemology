from pathlib import Path
import sys,importlib.util,json,os,subprocess,datetime,re,tempfile
sys.dont_write_bytecode=True
W=Path.cwd();R=W/'hase-certificate-domain-independent-review-20261010';C=W/'hase-certificate-code-validity-20261010'
freeze_path=W/sys.argv[1];freeze=json.loads(freeze_path.read_text())
spec=importlib.util.spec_from_file_location('candidate',C/'verify.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
pins=json.loads((C/'validation/INPUT_PINS.json').read_text());desc=json.loads((C/'validation/DESCRIPTION_FREEZE.json').read_text())
coverage=json.loads((R/'SCHEMA_COVERAGE_RECEIPT.json').read_text())['sources']
coverage_pins=[dict(path=path,**info) for path,info in coverage.items()]
allpins=pins['inputs']+desc['files']+freeze['files']+coverage_pins;p.b.check(allpins)
V=Path(tempfile.mkdtemp(prefix='global-replay-',dir=R));env=dict(os.environ,LEAN_PATH=':'.join(map(str,[V]+p.b.inherited_paths())))
rows=[]
for src in p.SOURCES:
 obj=V/(src.stem+'.olean');run=subprocess.run([str(p.b.LEAN),'--trust=0','-s',str(p.STACK_KB),'-o',str(obj),str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=V/(src.stem+'.log');log.write_text(run.stdout)
 assert run.returncode==0 and not any(x in run.stdout for x in ['sorryAx','error:','warning:']),str(log)
 sizes={'ValidityControls':(20,7),'TelescopeValidityControls':(6,4),'CertificateControls':(96,8)}
 if src.stem in sizes:
  yes,no=sizes[src.stem];observed=[[x.strip() for x in row.split(',')] for row in re.findall(r'\[([^]]*)\]',run.stdout)];assert observed==[['true']*yes,['false']*no],str(log)
 if src.stem=='CertificateAudit':
  ax=re.findall(r'depends on axioms: \[([^]]*)\]',run.stdout);noax=run.stdout.count('does not depend on any axioms');expected=len(json.loads((C/'AUDIT_NAMES.json').read_text()));assert len(ax)+noax==expected
  assert all(set(filter(None,x.split(', ')))-{'propext','Classical.choice','Quot.sound'}==set() for x in ax)
 rows.append({'module':src.stem,'source':p.b.rec(src),'object':p.b.rec(obj),'log':p.b.rec(log),'exit_code':run.returncode});print('PASS '+src.stem,flush=True)
negative=[]
for m in p.MUTATIONS:
 src=C/'diagnostics'/(m+'.lean');run=subprocess.run([str(p.b.LEAN),'--trust=0','-s',str(p.STACK_KB),str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=V/(m+'.log');log.write_text(run.stdout)
 assert run.returncode!=0 and "tactic 'decide' proved that the proposition" in run.stdout and 'error:' in run.stdout,str(log)
 negative.append({'module':m,'source':p.b.rec(src),'log':p.b.rec(log),'exit_code':run.returncode});print('REJECTED '+m,flush=True)
actual=[line.split(' ',1)[1] for line in (V/'ImportManifest.log').read_text().splitlines() if line.startswith('DEPENDENCY ')];owned={s.stem for s in p.SOURCES};retained=[m for m in actual if m not in owned];assert retained==pins['retained_modules']
p.b.check(allpins)
receipt={'status':'PASS_FROZEN_GLOBAL_CERTIFICATE_CANDIDATE_REPLAY','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trust':0,'thread_stack_kb':p.STACK_KB,'lean_version':subprocess.check_output([str(p.b.LEAN),'--version'],text=True).strip(),'baseline_rebuilt':False,'protected_inputs_mutated':False,'input_pins_verified_before_after':len(pins['inputs']),'retained_import_objects':len(retained),'freeze_entries_verified_before_after':len(freeze['files']),'freeze':p.b.rec(freeze_path),'input_inventory':p.b.rec(C/'validation/INPUT_PINS.json'),'fresh_output':str(V.relative_to(W)),'positive':rows,'negative':negative,'axiom_audits':len(json.loads((C/'AUDIT_NAMES.json').read_text())),'certificate_runtime_controls':104,'all_runtime_controls':141,'sorts':15,'canonical_domain_PR_and_exact':True,'ordinary_decoder_equivalence':False,'source_Primcodable_assumed':False,'whole_semantic_checker_PR':False,'source_derivability_RE':False,'T20_closure':False}
(R/'GLOBAL_CANDIDATE_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS global candidate replay',flush=True)
