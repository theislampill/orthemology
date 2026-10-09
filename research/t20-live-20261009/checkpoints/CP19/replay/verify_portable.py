#!/usr/bin/env python3
"""Bounded checkpoint19 transport qualification. No downloads, builds or original writes."""
from pathlib import Path
from datetime import datetime, timezone
from itertools import combinations
import argparse,hashlib,importlib.util,json,os,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent.parent
G='graph-constrained-continuation-20261009'
R='recognition-operative-content-20261009'
REVIEW='graph-continuation-review-20261009'
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,obj):p.write_text(json.dumps(obj,indent=2)+'\n')
def execute(cmd,cwd,env=None):return subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True)
def verify_payload():
 data=json.loads((ROOT/'PRESERVED_INPUTS.json').read_text())
 for f in data['files']:
  p=ROOT/f['path'];assert p.is_file() and not p.is_symlink() and p.stat().st_size==f['bytes'] and digest(p)==f['sha256'],f['path']
 if (ROOT/'MANIFEST.json').exists():
  for f in json.loads((ROOT/'MANIFEST.json').read_text())['files']:
   p=ROOT/f['path'];assert p.is_file() and not p.is_symlink() and p.stat().st_size==f['bytes'] and digest(p)==f['sha256'],f['path']
 return len(data['files'])
p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--output',required=True,help='New absolute output directory; must not exist')
p.add_argument('--lean',help='Explicit absolute installed Lean4.19.0 binary')
p.add_argument('--mathlib',help='Explicit absolute existing mathlib checkout at retained pin, with cached imports')
p.add_argument('--python-only',action='store_true',help='Run only minimal finite transport checks; no Lean claim')
a=p.parse_args();out=Path(a.output)
if not out.is_absolute() or out.exists():p.error('--output must be new and absolute')
if a.python_only and (a.lean or a.mathlib):p.error('Do not combine --python-only with Lean arguments')
if not a.python_only and not (a.lean and a.mathlib):p.error('Both --lean and --mathlib are required, or explicitly use --python-only')
selected=verify_payload();pins=json.loads((ROOT/'DEPENDENCY_PINS.json').read_text())
out.mkdir(parents=True,exist_ok=False)
receipt={'created_utc':datetime.now(timezone.utc).isoformat(),'scope':'Transport qualification only; no source reading, metaphysical assessment, research-duration credit, integration, acceptance or T20 closure.','selected_hashes_verified_before':selected,'python':sys.version,'checks':[]}
# Run unchanged copies, because both historical scripts write next to __file__.
for group,script,results in [(G,'controls.py',['CONTROL_RESULTS.json']),(R,'check_selective_channel.py',['MODEL_RESULTS.json']),('necessary-truth-operative-basing-20261009','check_relevant_bridge.py',['CHECK_RESULTS.json','RELEVANT_PROOF.md']),('relevant-closure-review-20261009','review_checks.py',['INDEPENDENT_CHECK_RESULTS.json'])]:
 work=out/group;work.mkdir();source=ROOT/group/script;copied=work/script;shutil.copyfile(source,copied)
 run=execute([sys.executable,'-B',str(copied)],work);log=work/'replay.log';log.write_text(run.stdout+run.stderr)
 checked=[]
 for result in results:
  got=work/result;ok=run.returncode==0 and got.is_file() and digest(got)==digest(ROOT/group/result)
  checked.append({'result':result,'byte_matches_historical':ok,'sha256':digest(got) if got.exists() else None})
  assert ok,(group,result,'portable Python result mismatch')
 receipt['checks'].append({'kind':'unchanged_python_copy','source':group+'/'+script,'source_sha256':digest(source),'exit_code':run.returncode,'results':checked,'log':str(log),'epistemic_scope':'Relevant proof checks are syntactic Python and finite matrix checks only, not Lean/kernel or a cognition model.' if 'relevant' in script or 'closure' in group else 'Declared original finite-control scope only.'})
# Import the unchanged independent review functions without executing its hardcoded main.
# The minimal n<=4 repeat is transport qualification; historical n<=6 receipt is retained only.
work=out/REVIEW;work.mkdir();copied=work/'verify_formula.py';shutil.copyfile(ROOT/REVIEW/'verify_formula.py',copied)
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('checkpoint19_independent_formula',copied);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
graphs=pairs=fixed_pairs=0
for n in range(1,5):
 for code in range(1 << (n*(n-1)//2)):
  adj=module.graph_data(n,code);d=module.bfs(adj);tau=module.connected_tau(adj);assert d[0]==-1
  for mask in range(1,1<<n):
   expected=2*tau[mask]-mask.bit_count()-1 if tau[mask]<10**9 else -1
   assert d[mask]==expected;(pairs:=pairs+1)
  for r in range(n):
   fixed=module.bfs(adj,[1<<r])
   for mask in range(1,1<<n):
    t=tau[mask|(1<<r)];expected=2*t-mask.bit_count()-1 if t<10**9 else -1
    assert fixed[mask]==expected;(fixed_pairs:=fixed_pairs+1)
  graphs+=1
small={'graphs':graphs,'graph_mask_pairs':pairs,'fixed_root_mask_pairs':fixed_pairs,'maximum_vertices':4,'passed':True,'historical_n6_test_results_replayed':False}
dump(work/'MINIMAL_REPLAY.json',small);receipt['checks'].append({'kind':'independent_formula_minimal',**small})
if not a.python_only:
 lean=Path(a.lean);mathlib=Path(a.mathlib)
 assert lean.is_absolute() and lean.is_file() and os.access(lean,os.X_OK),'Absolute executable --lean required'
 assert mathlib.is_absolute() and mathlib.is_dir(),'Absolute existing --mathlib required'
 lean=lean.resolve();mathlib=mathlib.resolve()
 version=execute([str(lean),'--version'],out);assert version.returncode==0
 assert re.match(r'^Lean \(version 4\.19\.0,',version.stdout.strip()),version.stdout
 assert pins['lean_commit'] in version.stdout,version.stdout
 head=execute(['git','rev-parse','HEAD'],mathlib);assert head.returncode==0 and head.stdout.strip()==pins['mathlib_commit'],'mathlib commit mismatch'
 assert digest(mathlib/'lake-manifest.json')==pins['mathlib_lake_manifest_sha256'],'mathlib lake-manifest mismatch'
 assert (mathlib/'lean-toolchain').read_text().strip()==pins['mathlib_lean_toolchain'],'mathlib Lean toolchain mismatch'
 manifest=json.loads((mathlib/'lake-manifest.json').read_text())
 prefix=execute([str(lean),'--print-prefix'],out);assert prefix.returncode==0
 # Explicit cache paths reproduce Lake's inherited path order without running Lake.
 deps=[mathlib/manifest['packagesDir']/item['name']/'.lake/build/lib/lean' for item in reversed(manifest['packages'])]
 deps += [mathlib/'.lake/build/lib/lean',Path(prefix.stdout.strip())/'lib/lean']
 assert all(d.is_dir() for d in deps[-2:]),'Mathlib or Lean base cache missing; no download/build attempted'
 # Lake's inherited path includes optional unused package directories (e.g. Cli).
 # Keep those path entries; actual missing imports are rejected by Lean itself.
 absent_cache_paths=[str(d) for d in deps if not d.is_dir()]
 for imp in ['Mathlib.Algebra.BigOperators.Group.Finset.Piecewise','Mathlib.Data.Finset.Card','Mathlib.Data.Finset.Lattice.Basic','Mathlib.Tactic.FinCases','Mathlib.Tactic.NormNum']:
  assert (mathlib/'.lake/build/lib/lean'/Path(*imp.split('.'))).with_suffix('.olean').is_file(),('missing cached import',imp)
 work=out/'lean';work.mkdir();env=os.environ.copy();env['LEAN_PATH']=os.pathsep.join(map(str,[work]+deps))
 source=ROOT/G/'GraphContinuation.lean';assert digest(source)==pins['portable_replay_source']['sha256']
 assert not re.search(r'\b(sorry|admit|axiom|native_decide)\b',source.read_text()),'Unfinished/assumed declaration marker'
 copied=work/source.name;shutil.copyfile(source,copied)
 cmd=[str(lean),'-t0','-DwarningAsError=true','--root='+str(work),'-o',str(work/'GraphContinuation.olean'),str(copied)]
 run=execute(cmd,work,env);log=work/'KERNEL.log';log.write_text(run.stdout+run.stderr)
 assert run.returncode==0 and not re.search(r'sorryAx|error:|warning:',log.read_text()),log.read_text()
 assert digest(log)==digest(ROOT/G/'verified/KERNEL.log'),'Successful kernel axiom readback differs from retained exact receipt'
 negatives=[]
 for name in ['FalseSteinerCost','FalsePreservation']:
  bad=ROOT/G/'verified'/(name+'.lean');dst=work/bad.name;shutil.copyfile(bad,dst)
  badrun=execute([str(lean),'-t0','-DwarningAsError=true','--root='+str(work),str(dst)],work,env)
  badlog=work/(name+'.log');badlog.write_text(badrun.stdout+badrun.stderr)
  rejected=badrun.returncode!=0 and 'error:' in badlog.read_text();assert rejected,('False claim was not rejected',name)
  negatives.append({'file':G+'/verified/'+bad.name,'sha256':digest(bad),'exit_code':badrun.returncode,'rejected':rejected,'log_sha256':digest(badlog),'comparison':'Error paths differ after relocation; preserved historical negative log is unchanged.'})
 receipt['lean']={'passed':True,'command':cmd,'source_sha256':digest(copied),'version':version.stdout.strip(),'lean_binary_sha256':digest(lean),'historical_linux_binary_hash_matches':digest(lean)==pins['historical_linux_lean_sha256'],'mathlib_commit':head.stdout.strip(),'lake_manifest_sha256':digest(mathlib/'lake-manifest.json'),'kernel_log_sha256':digest(log),'kernel_log_exact_historical_match':True,'negative_controls':negatives,'dependency_paths':list(map(str,deps)),'absent_optional_cache_path_entries':absent_cache_paths,'dependency_scope':'Commit, manifest, toolchain and import presence checked. Existing compiled caches trusted; no rebuild, download or whole transitive cache hash audit.'}
else:receipt['lean']={'replayed':False,'reason':'Explicit --python-only selected; historical kernel receipts preserved, not newly certified.'}
receipt['selected_hashes_verified_after']=verify_payload();receipt['passed']=True
dump(out/'QUALIFICATION.json',receipt);print(json.dumps(receipt,indent=2))
