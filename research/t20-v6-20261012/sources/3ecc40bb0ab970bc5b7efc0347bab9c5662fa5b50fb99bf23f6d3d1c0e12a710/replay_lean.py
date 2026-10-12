#!/usr/bin/env python3
"""Cold first-party source replay against installed pinned official Linux dependencies."""
from pathlib import Path
import argparse,json,os,subprocess,datetime
import sys
sys.dont_write_bytecode=True
from portable_core import verify,verify_pins,sha,write_json,parse_readback,safe_path,strip_comments,validate_suite_id,validate_module,check_source,check_diagnostics,verify_official_ownership
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--lean-bin',type=Path,required=True);p.add_argument('--mathlib',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--suites',help='Comma-separated suite IDs; default all');a=p.parse_args();root=a.root.resolve();out=a.out.resolve()
if out.exists() or out.is_relative_to(root):p.error('Output must be absent and outside immutable package')
verified=verify(root);pins=json.loads((root/'replay/DEPENDENCY_PINS.json').read_text());suites=json.loads((root/'replay/SUITES.json').read_text())['suites'];ids={s['id'] for s in suites}
if a.suites:
 wanted=set(a.suites.split(','))
 if not wanted or not wanted<=ids:p.error('Unknown suite ID')
 suites=[s for s in suites if s['id'] in wanted]
lean,libs,version,checks=verify_pins(a.lean_bin,a.mathlib,pins,{r['module'] for s in suites for r in s['modules']});official=verify_official_ownership(root,a.mathlib);out.mkdir(parents=True)
receipt={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_manifest_sha256':verified['manifest_sha256'],'lean_sha256':sha(lean),'lean_version':version,'dependency_checks':checks,'official_import_ownership':official,'driver_sha256':sha(Path(__file__)),'core_sha256':sha(Path(__file__).with_name('portable_core.py')),'scope':'Every selected first-party custom object built fresh from bound source; installed official upstream objects reused','suites':[]};write_json(out/'REPLAY_RESULT.json',receipt)
try:
 for suite in suites:
  d=safe_path(out,validate_suite_id(suite['id']));src=d/'source';build=d/'build';logs=d/'logs'
  for q in [src,build,logs]:q.mkdir(parents=True)
  by={r['module']:r for r in suite['modules']}
  env=dict(os.environ);env.pop('LEAN_SRC_PATH',None);env['LEAN_PATH']=':'.join(map(str,[build]+libs));env['PATH']=str(lean.parent)+os.pathsep+env.get('PATH','')
  rr={'id':suite['id'],'status':'RUNNING','modules':[]};receipt['suites'].append(rr)
  for mod in suite['module_order']:
   validate_module(mod);row=by[mod];check_source(safe_path(root,row['source']).read_text());rel=Path(mod.replace('.','/')+'.lean');source=src/rel;source.parent.mkdir(parents=True,exist_ok=True);source.write_bytes(safe_path(root,row['source']).read_bytes());assert sha(source)==row['sha256'];obj=(build/rel).with_suffix('.olean');obj.parent.mkdir(parents=True,exist_ok=True);assert not obj.exists()
   cmd=[str(lean),'-j1','--root='+str(src),'-o',str(obj),str(source)];run=subprocess.run(cmd,cwd=a.mathlib.resolve(),env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=logs/(mod+'.log');log.write_text(run.stdout)
   rr['modules'].append({'module':mod,'input_source':row['source'],'source_sha256':sha(source),'exit':run.returncode,'log_path':str(log.relative_to(out)),'log_sha256':sha(log),'olean_sha256':sha(obj) if obj.exists() else None});write_json(out/'REPLAY_RESULT.json',receipt);print(suite['id'],mod,run.returncode,flush=True)
   if run.returncode:raise ValueError('Module failed '+mod)
   check_diagnostics(run.stdout)
  targets=[t for row in suite['modules'] for t in row['targets']]
  if len(targets)!=len(set(targets)):raise ValueError('Duplicate declarations across suite; isolate alias closures')
  audit=src/'PortableReadback.lean';audit.write_text('\n'.join('import '+m for m in suite['module_order'])+'\nset_option pp.universes true\n'+''.join(f'#check @{t}\n#print axioms {t}\n' for t in targets));cmd=[str(lean),'-j1','--root='+str(src),str(audit)];run=subprocess.run(cmd,cwd=a.mathlib.resolve(),env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=logs/'PortableReadback.log';log.write_text(run.stdout)
  if run.returncode:raise ValueError('Readback compile failed '+suite['id'])
  axioms=parse_readback(run.stdout,targets);rr['readback']={'source_sha256':sha(audit),'log_path':str(log.relative_to(out)),'log_sha256':sha(log),'target_count':len(targets),'axioms':axioms};rr['status']='PASS';write_json(out/'REPLAY_RESULT.json',receipt)
 if verify(root)['manifest_sha256']!=receipt['input_manifest_sha256']:raise ValueError('Input changed during replay')
 receipt['status']='PASS';receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();write_json(out/'REPLAY_RESULT.json',receipt)
except Exception as e:
 receipt['status']='FAIL_CLOSED';receipt['error']=str(e);receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();write_json(out/'REPLAY_RESULT.json',receipt);raise
