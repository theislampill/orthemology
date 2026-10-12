#!/usr/bin/env python3
"""Portable source-only reconstruction of the unchanged bounded seed review."""
from pathlib import Path
import argparse,subprocess,hashlib,json,zipfile,sys,os,re
p=argparse.ArgumentParser();p.add_argument('--environment',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
r=Path(__file__).resolve().parent;o=a.out.resolve();e=a.environment.resolve();assert not o.exists();o.mkdir(parents=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def extract(name,dest,digest):
 z=r/name;assert sha(z)==digest
 with zipfile.ZipFile(z) as f:
  for n in f.namelist():assert not Path(n).is_absolute() and '..' not in Path(n).parts
  f.extractall(dest)
def run(args,log,env=None):
 with log.open('w') as f:subprocess.run(list(map(str,args)),stdout=f,stderr=subprocess.STDOUT,env=env,check=True)
extract('Residual_Seed_Cancellation_Author_v1_20261001.zip',o/'author','c3f900fa367b76021116c5cad3d9e524c22a4af03a71de5db4eeee0dea42aeb1')
extract('Residual_Seed_Independent_Review_20261001.zip',o/'review','12596cc49d1871840895000719d495fb9e2804afd7fd1471c804b159384af89c')
author=o/'author';review=o/'review';lean=e/'toolchain/lean-4.19.0-linux/bin';mathlib=e/'mathlib4'
for row in json.loads((review/'MANIFEST.json').read_text())['files']:
 q=review/row['path'];assert q.stat().st_size==row['bytes'] and sha(q)==row['sha256']
run([sys.executable,'-B',author/'tooling/replay_lean.py','--root',author,'--lean-bin',lean,'--mathlib',mathlib,'--out',o/'cold','--suites','residual_seed','--no-reuse'],o/'COLD.log')
cold=json.loads((o/'cold/REPLAY_RESULT.json').read_text());assert cold['status']=='PASS' and cold['fresh_custom_objects']==28 and cold['suites'][0]['readback']['target_count']==361
run([sys.executable,'-B',review/'check_actual_oracles.py'],o/'INDEPENDENT_CONTROLS.json')
assert json.loads((o/'INDEPENDENT_CONTROLS.json').read_text())==json.loads((review/'INDEPENDENT_CONTROLS.json').read_text())
run([sys.executable,'-B',author/'controls/check_posterior.py'],o/'AUTHOR_CONTROLS.json')
assert json.loads((o/'AUTHOR_CONTROLS.json').read_text())==json.loads((review/'AUTHOR_CONTROLS_REPLAY.json').read_text())
le=os.environ.copy();le['LEAN_PATH']=':'.join(map(str,[o/'cold/residual_seed/build',mathlib/'.lake/build/lib/lean']+sorted((mathlib/'.lake/packages').glob('*/.lake/build/lib/lean'))))
run([lean/'lean','-j1',review/'probes/ResidualSeedContractProbes.lean'],o/'PROBES.log',le)
log=(o/'PROBES.log').read_text();assert 'error:' not in log and 'sorryAx' not in log
axs=re.findall(r"'([^']+)' depends on axioms: \[([^]]*)\]",log);empty=re.findall(r"'([^']+)' does not depend on any axioms",log);assert len(axs)+len(empty)==6
for _,v in axs:assert {x.strip() for x in v.split(',')}<={'propext','Classical.choice','Quot.sound'}
result={'status':'PASS_PORTABLE_BOUNDED_SEED_REVIEW','fresh_modules':28,'expanded_readbacks':361,'independent_kernel_probes':6,'independent_exact_assertions':1154755,'runner_sha256':sha(Path(__file__))}
(o/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
