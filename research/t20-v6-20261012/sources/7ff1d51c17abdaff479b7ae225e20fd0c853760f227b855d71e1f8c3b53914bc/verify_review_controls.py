from pathlib import Path
import sys,importlib.util,json,os,subprocess,re,datetime,tempfile
sys.dont_write_bytecode=True
W=Path.cwd();R=W/'hase-certificate-domain-independent-review-20261010';C=W/'hase-certificate-code-validity-20261010'
spec=importlib.util.spec_from_file_location('candidate',C/'verify.py');p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
core=json.loads((R/'GLOBAL_CANDIDATE_REPLAY_RECEIPT.json').read_text()); core_out=W/core['fresh_output'];V=Path(tempfile.mkdtemp(prefix='global-review-controls-',dir=R))
src=R/'GlobalReviewControls.lean';pins=[p.b.rec(src),p.b.rec(R/'verify_review_controls.py')]+[entry['object'] for entry in core['positive']]+json.loads((C/'validation/FINAL_FREEZE.json').read_text())['files'];p.b.check(pins)
env=dict(os.environ,LEAN_PATH=':'.join(map(str,[V,core_out]+p.b.inherited_paths())))
obj=V/(src.stem+'.olean');run=subprocess.run([str(p.b.LEAN),'--trust=0','-s','65536','-o',str(obj),str(src)],cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=V/(src.stem+'.log');log.write_text(run.stdout)
assert run.returncode==0 and not any(x in run.stdout for x in ['sorryAx','error:','warning:']),str(log)
ax=re.findall(r'depends on axioms: \[([^]]*)\]',run.stdout);noax=run.stdout.count('does not depend on any axioms');assert len(ax)+noax==11
assert all(set(filter(None,x.split(', ')))-{'propext','Classical.choice','Quot.sound'}==set() for x in ax)
p.b.check(pins)
author=json.loads((C/'validation/AUTHOR_REPLAY.json').read_text()); bymodule={e['module']:e for e in author['positive']};same=[e['module'] for e in core['positive'] if e['object']['sha256']==bymodule[e['module']]['object']['sha256']]
receipt={'status':'PASS_ADDITIONAL_GLOBAL_REVIEW_CONTROLS','timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'trust':0,'thread_stack_kb':65536,'source':p.b.rec(src),'object':p.b.rec(obj),'log':p.b.rec(log),'exit_code':run.returncode,'axiom_audits':11,'fresh_candidate_modules':len(core['positive']),'independent_objects_identical_to_author':same,'pins_verified_before_after':len(pins),'core_replay':p.b.rec(R/'GLOBAL_CANDIDATE_REPLAY_RECEIPT.json'),'baseline_rebuilt':False,'candidate_mutated':False}
(R/'GLOBAL_REVIEW_CONTROLS_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print('PASS11 additional symbolic audits;',len(same),'of41 objects identical to author')
