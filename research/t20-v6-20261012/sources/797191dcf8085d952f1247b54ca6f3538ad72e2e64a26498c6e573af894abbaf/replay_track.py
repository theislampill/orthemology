from pathlib import Path
import subprocess, shutil, tempfile, json, hashlib, sys, datetime, os
HERE=Path(__file__).resolve().parent
WS=HERE.parents[1]
OUT=HERE/'fresh-replay'; OUT.mkdir(exist_ok=True)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(name,src,commands):
 src=WS/src
 bindings={str(p.relative_to(src)):digest(p) for p in src.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
 rec={'name':name,'source':str(src.relative_to(WS)),'source_files':len(bindings),'commands':[],'start_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
 with tempfile.TemporaryDirectory(prefix='t20-evidence-consolidation-') as tmp:
  dst=Path(tmp)/'source';shutil.copytree(src,dst,symlinks=False,ignore=shutil.ignore_patterns('__pycache__'))
  for i,args in enumerate(commands):
   cmd=[sys.executable,*args]; start=datetime.datetime.now(datetime.timezone.utc).isoformat()
   p=subprocess.run(cmd,cwd=dst,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
   log=OUT/f'{name}-{i}.log';log.write_text(p.stdout+'\nSTDERR\n'+p.stderr)
   rec['commands'].append({'command':['python',*args],'exit_code':p.returncode,'start_utc':start,'log':str(log.relative_to(WS)),'log_sha256':digest(log)})
 rec['source_bytes_unchanged']=all(digest(src/p)==h for p,h in bindings.items())
 rec['status']='PASS' if all(c['exit_code']==0 for c in rec['commands']) and rec['source_bytes_unchanged'] else 'FAIL'
 (OUT/f'{name}.json').write_text(json.dumps(rec,indent=2)+'\n')
 print(name,rec['status'],[(c['exit_code'],c['log']) for c in rec['commands']],flush=True)
 return rec
jobs=[
 ('original-26','t20-consolidation-20261011/catalogue/archive-views/Orthemology_T20_Whole_Corpus_Synthesis_20261010_1_.zip--38ed92bbec08/Orthemology_T20_Whole_Corpus_Synthesis_20261010', [['-B','verification/verify_packet.py','.'],['-B','-m','unittest','discover','-s','research','-p','test_contracts.py','-v'],['-O','-B','-m','unittest','discover','-s','research','-p','test_contracts.py','-v'],['-B','research/exhaustive_oracle.py']]),
 ('response-33-8','recovery-20261011/remaining-archives/safe-extracts/synthesis-additive-response-20261011/synthesis-additive-response-20261011',[['-B','verification/verify_response.py'],['-O','-B','verification/verify_response.py']]),
 ('daee-integrity-only','t20-consolidation-20261011/catalogue/archive-views/noetic-recognition-guard-intermediate-20261009.zip--0d59830133a1/noetic-recognition-guard-intermediate-20261009',[['-B','verify_and_replay.py','--verify-only']]),
 ('fixed-model-inquiry','recovery-20261011/extracted/fixed-inquiry-guide-source-checkpoint-20261011/fixed-inquiry-guide-source-checkpoint-20261011',[['-B','replay.py']]),
 ('credal-geometric','recovery-20261011/remaining-archives/safe-extracts/credal-coupling-geometric-final-delivery-20261011/credal-coupling-geometric-final-delivery-20261011',[['-B','replay.py']])]
receipts=[run(*job) for job in jobs]
(OUT/'REPLAY_RECEIPT.json').write_text(json.dumps({'scope':'Targeted finite-control and byte-integrity replays; no Lean or source-warrant proof; no DAEE patch applied','python':sys.version,'prior_failed_attempt':{'description':'Direct DAEE --verify-only execution through content-address symlink resolved __file__ to object store; missing SHA256SUMS. Corrected by materialized disposable package copy. No source mutation.'},'receipts':receipts},indent=2)+'\n')
