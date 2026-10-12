#!/usr/bin/env python3
"""Replay solely from this portable review and its embedded immutable author ZIP."""
from pathlib import Path
import argparse,hashlib,json,zipfile,subprocess,sys,os,re
p=argparse.ArgumentParser();p.add_argument('--environment',required=True,type=Path);p.add_argument('--out',required=True,type=Path);a=p.parse_args()
r=Path(__file__).resolve().parent;c=json.loads((r/'REPLAY_CONFIG.json').read_text());o=a.out.resolve();e=a.environment.resolve()
assert not o.exists(),'Output must be absent';o.mkdir(parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
z=r/c['archive'];assert sha(z)==c['archive_sha256'];assert sha(r/c['probe_file'])==c['probe_sha256']
with zipfile.ZipFile(z) as f:
 for n in f.namelist():assert not Path(n).is_absolute() and '..' not in Path(n).parts
 f.extractall(o/'author')
author=o/'author';lean=e/'toolchain/lean-4.19.0-linux/bin';mathlib=e/'mathlib4'
def run(args,log,env=None):
 with log.open('w') as f:subprocess.run(list(map(str,args)),stdout=f,stderr=subprocess.STDOUT,env=env,check=True)
run([sys.executable,'-B',author/'tooling/replay_lean.py','--root',author,'--lean-bin',lean,'--mathlib',mathlib,'--out',o/'cold','--suites',c['suite'],'--no-reuse'],o/'COLD.log')
cold=json.loads((o/'cold/REPLAY_RESULT.json').read_text());assert cold['status']=='PASS' and cold['fresh_custom_objects']==c['modules']
assert len(cold['suites'])==1 and cold['suites'][0]['readback']['target_count']==c['readbacks']
le=os.environ.copy();le['LEAN_PATH']=':'.join(map(str,[o/'cold'/c['suite']/'build',mathlib/'.lake/build/lib/lean']+sorted((mathlib/'.lake/packages').glob('*/.lake/build/lib/lean'))))
run([lean/'lean','-j1',r/c['probe_file']],o/'PROBES.log',le)
log=(o/'PROBES.log').read_text();assert 'error:' not in log and 'sorryAx' not in log
axs=re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",log);assert len(axs)==c['probe_count']
for _,v in axs:assert {x.strip() for x in v.split(',')}<={'propext','Classical.choice','Quot.sound'}
if 'controls_sha256' in c:
 assert sha(r/'check_markov_continuations.py')==c['controls_sha256']
 run([sys.executable,'-B',r/'check_markov_continuations.py'],o/'INDEPENDENT_CONTROLS.json')
 independent=json.loads((o/'INDEPENDENT_CONTROLS.json').read_text());assert independent==json.loads((r/'INDEPENDENT_CONTROLS.json').read_text())
 run([sys.executable,'-B',author/'controls/check_continuation.py'],o/'AUTHOR_CONTROLS.json')
 assert json.loads((o/'AUTHOR_CONTROLS.json').read_text())==json.loads((r/'AUTHOR_CONTROLS_REPLAY.json').read_text())
result={'status':'PASS_PORTABLE_REVIEW','suite':c['suite'],'fresh_modules':c['modules'],'expanded_readbacks':c['readbacks'],'independent_kernel_probes':c['probe_count'],'source_archive_sha256':c['archive_sha256'],'runner_sha256':sha(Path(__file__))}
if 'controls_sha256' in c:result['independent_exact_assertions']=independent['exact_assertions']
(o/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
