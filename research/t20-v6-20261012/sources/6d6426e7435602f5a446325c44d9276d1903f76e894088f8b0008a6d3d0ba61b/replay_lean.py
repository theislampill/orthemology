#!/usr/bin/env python3
"""Replay the source-specific Lean certificate with explicitly supplied pinned dependencies.
No installation, dependency compilation, or writes to frozen inputs. Not self-contained.
"""
from pathlib import Path
from datetime import datetime,timezone
import argparse,hashlib,json,os,shutil,subprocess,tempfile
ROOT=Path(__file__).resolve().parents[1]
AUTHOR=ROOT/'t20-next-frontier-20261008/retained-interior-certificate'
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  while b:=f.read(1<<20):h.update(b)
 return h.hexdigest()
p=argparse.ArgumentParser();p.add_argument('--external-research-root',required=True);p.add_argument('--output',required=True);a=p.parse_args()
external=Path(a.external_research_root).resolve();out=Path(a.output).resolve()
assert out!=ROOT and ROOT not in out.parents and out!=external and external not in out.parents,'Use output outside checkpoint and external source tree'
out.mkdir(parents=True,exist_ok=True);assert not (out/'LEAN_REPLAY_RECEIPT.json').exists(),'Refuse existing receipt'
deps=json.loads((AUTHOR/'KERNEL_DEPENDENCIES.json').read_text());mods=json.loads((AUTHOR/'IMPORTED_MODULE_BINDINGS.json').read_text())
assert sha(AUTHOR/'IMPORTED_MODULE_BINDINGS.json')==deps['imported_module_manifest_sha256']
bindings={}
for r in mods:
 for key in ['source','olean']:bindings[r[key]]=r[key+'_sha256']
for path,digest in deps['files'].items():bindings[path]=digest
# Included component identities use the frozen source copy, not the original research file.
def resolve(path):
 if path.startswith('retained-interior-certificate/'):return AUTHOR/path.split('/',1)[1]
 return external/path
for path,digest in bindings.items():assert sha(resolve(path))==digest,(path,'external dependency identity mismatch')
formal=external/'formal-identification';tool=formal/'toolchain/lean-4.19.0-linux';mathlib=formal/'mathlib'
commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=mathlib,text=True).strip();assert commit==deps['mathlib_commit']
paths=[]
for entry in (AUTHOR/'LEAN_PATH.txt').read_text().strip().split(':'):
 paths.append(str(tool/'lib/lean') if Path(entry).is_absolute() else str((mathlib/entry).resolve()))
env=dict(os.environ,LEAN_PATH=':'.join(paths));compiler=tool/'bin/lean';runs=[]
# Temporary location is independent of both dependency and checkpoint trees.
with tempfile.TemporaryDirectory(prefix='t20-ninth-lean-') as tmp:
 work=Path(tmp);src=(AUTHOR/'RetainedInterior.lean').read_text();assert 'sorry' not in src and '\naxiom ' not in src
 shutil.copy2(AUTHOR/'RetainedInterior.lean',work/'RetainedInterior.lean');shutil.copy2(AUTHOR/'ImportInventory.lean',work/'ImportInventory.lean')
 def run(name,extra,expected_success):
  command=[str(compiler),'-t','0','-DwarningAsError=true',*extra,str(work/(name+'.lean'))]
  proc=subprocess.run(command,cwd=work,env=env,capture_output=True,timeout=600)
  log=proc.stdout+proc.stderr;(out/(name+'.log')).write_bytes(log)
  ok=proc.returncode==0 if expected_success else proc.returncode!=0 and b'error:' in log
  if expected_success:ok=ok and not any(t in log for t in [b'sorryAx',b'error:',b'warning:'])
  row={'id':name,'flags':['-t','0','-DwarningAsError=true'],'expected_success':expected_success,'exit_code':proc.returncode,'status':'PASS' if ok else 'FAIL','log_sha256':hashlib.sha256(log).hexdigest()};runs.append(row);assert ok,row
  return log
 accepted=run('RetainedInterior',['--root='+str(work),'-o',str(work/'RetainedInterior.olean')],True)
 historical_log_match=accepted==(AUTHOR/'kernel-replay/TRUST_ZERO.log').read_bytes()
 built_sha=sha(work/'RetainedInterior.olean')
 log=run('ImportInventory',[],True);names=[line.removeprefix('IMPORT ') for line in log.decode().splitlines() if line.startswith('IMPORT ')]
 assert len(names)==len(mods) and set(names)=={r['module'] for r in mods}
 mutations={'FalseConnectorPremise':src.replace('¬ Hit GA GB (a i) (b (i + 1))','Hit GA GB (a i) (b (i + 1))'),'FalseCountBound':src.replace('m ≤ Fintype.card R','m + 1 ≤ Fintype.card R')}
 for name,text in mutations.items():
  assert text!=src;(work/(name+'.lean')).write_text(text);run(name,[],False)
 version=subprocess.check_output([str(compiler),'--version'],env=env,text=True).strip();assert version==deps['lean_version']
# Verify the exact input files again after replay. Dependency packages were read, not rebuilt.
for path,digest in bindings.items():assert sha(resolve(path))==digest,(path,'mutated during replay')
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'status':'PASS','scope':'Only source-specific deterministic connector/injection/cardinality certificate. Not probability, KL/asymptotic, minimality, reconstruction, physical semantics, or whole project verification.','compiler_version':version,'mathlib_commit':commit,'imported_module_count':len(mods),'import_source_and_olean_hash_checks':2*len(mods),'additional_declared_bindings':len(deps['files']),'external_inputs_unchanged':True,'import_names_reproduced':True,'historical_axiom_log_byte_match':historical_log_match,'fresh_olean_sha256':built_sha,'runs':runs,'self_contained':False,'fresh_upstream_rebuild':False,'research_duration_credit_seconds':0}
(out/'LEAN_REPLAY_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
