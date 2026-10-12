#!/usr/bin/env python3
"""Cold source-only suite replay against explicit pinned external dependencies."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys
sys.dont_write_bytecode=True
from portable_core import verify,verify_pins,verify_official,sha,write_json,safe_path,check_source,check_diagnostics,parse_readback

def main():
 p=argparse.ArgumentParser(description=__doc__)
 p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--lean-bin',type=Path,required=True);p.add_argument('--mathlib',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--suites');p.add_argument('--verify-only',action='store_true');p.add_argument('--no-reuse',action='store_true');a=p.parse_args()
 root=a.root.resolve();out=a.out.resolve()
 if out.exists() or out.is_relative_to(root):p.error('Output must be absent and outside immutable input package')
 identity=verify(root);pins=json.loads((root/'replay/DEPENDENCY_PINS.json').read_text());suites=json.loads((root/'replay/SUITES.json').read_text())['suites']
 if a.suites:
  wanted=set(a.suites.split(','));known={s['id'] for s in suites}
  if not wanted or not wanted<=known:p.error('Unknown requested suite')
  suites=[s for s in suites if s['id'] in wanted]
 lean,libs,version,checks=verify_pins(a.lean_bin,a.mathlib,pins,{r['module'] for s in suites for r in s['modules']})
 official=verify_official(root,a.lean_bin.resolve(),a.mathlib.resolve(),pins,suites)
 out.mkdir(parents=True);cache=out/'current-run-cache';cache.mkdir()
 receipt={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'input_manifest_sha256':identity['manifest_sha256'],'lean_sha256':sha(lean),'lean_version':version,'dependency_checks':checks,'official_import_ownership':official,'driver_sha256':sha(Path(__file__)),'core_sha256':sha(Path(__file__).with_name('portable_core.py')),'scope':'Only this cold run may reuse exact transitive-source-fingerprint custom objects; official installed cache trusted','suites':[]}
 save=lambda:write_json(out/'REPLAY_RESULT.json',receipt)
 save();objects={};official_rows={r['module']:r for r in json.loads((root/'replay/OFFICIAL_IMPORTS.json').read_text())['imports']}
 try:
  if not a.verify_only:
   for suite in suites:
    d=safe_path(out,suite['id']);src=d/'source';build=d/'build';logs=d/'logs'
    for q in [src,build,logs]:q.mkdir(parents=True)
    by={r['module']:r for r in suite['modules']};keys={};rr={'id':suite['id'],'status':'RUNNING','modules':[]};receipt['suites'].append(rr)
    env=dict(os.environ);env.pop('LEAN_SRC_PATH',None);env['LEAN_PATH']=':'.join(map(str,[build]+libs));env['PATH']=str(lean.parent)+os.pathsep+env.get('PATH','')
    for mod in suite['module_order']:
     row=by[mod];raw=safe_path(root,row['source']).read_bytes();check_source(raw.decode());rel=Path(mod.replace('.','/')+'.lean');source=src/rel;source.parent.mkdir(parents=True,exist_ok=True);source.write_bytes(raw)
     if sha(source)!=row['sha256']:raise ValueError('Source changed before compile')
     deps=[{'module':i,'binding':keys[i] if i in by else official_rows[i]} for i in row['imports']]
     key=hashlib.sha256(json.dumps({'module':mod,'source':row['sha256'],'deps':deps,'pins':pins,'compiler_flags':['-j1','--root=isolated-suite-source']},sort_keys=True).encode()).hexdigest();keys[mod]=key
     obj=(build/rel).with_suffix('.olean');obj.parent.mkdir(parents=True,exist_ok=True)
     entry={'module':mod,'source':row['source'],'source_sha256':row['sha256'],'transitive_source_fingerprint':key}
     if not a.no_reuse and key in objects:
      previous=objects[key]
      if sha(previous['object'])!=previous['sha256']:raise ValueError('Current-run object changed')
      obj.write_bytes(previous['object'].read_bytes());entry.update({'status':'REUSED_CURRENT_COLD_RUN','built_in_suite':previous['suite'],'olean_sha256':sha(obj)})
     else:
      cmd=[str(lean),'-j1','--root='+str(src),'-o',str(obj),str(source)];run=subprocess.run(cmd,cwd=src,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=logs/(mod+'.log');log.write_text(run.stdout)
      entry.update({'status':'FRESH_COMPILE','exit':run.returncode,'log':str(log.relative_to(out)),'log_sha256':sha(log),'olean_sha256':sha(obj) if obj.exists() else None})
      rr['modules'].append(entry);save();print(suite['id'],mod,run.returncode,flush=True)
      if run.returncode:raise ValueError('Compile failed '+suite['id']+'/'+mod)
      check_diagnostics(run.stdout)
      target=cache/(key+'.olean');target.write_bytes(obj.read_bytes());objects[key]={'object':target,'sha256':sha(target),'suite':suite['id']}
     if entry not in rr['modules']:rr['modules'].append(entry)
    targets=suite['targets'];audit=src/'PortableReadback.lean';audit.write_text('\n'.join('import '+m for m in suite['module_order'])+'\nset_option pp.universes true\nset_option pp.explicit true\n'+''.join(f'#check @{t}\n#print axioms {t}\n' for t in targets))
    run=subprocess.run([str(lean),'-j1','--root='+str(src),str(audit)],cwd=src,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT);log=logs/'PortableReadback.log';log.write_text(run.stdout)
    if run.returncode:raise ValueError('Readback compile failed '+suite['id'])
    check_diagnostics(run.stdout);axioms=parse_readback(run.stdout,targets)
    rr['readback']={'source_sha256':sha(audit),'log':str(log.relative_to(out)),'log_sha256':sha(log),'target_count':len(targets),'axioms':axioms};rr['status']='PASS';save()
  if verify(root)['manifest_sha256']!=identity['manifest_sha256']:raise ValueError('Input changed during replay')
  receipt['status']='PRECHECK_PASS' if a.verify_only else 'PASS';receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();receipt['fresh_custom_objects']=len(objects);save();print(receipt['status'],len(objects),'fresh objects',flush=True)
 except BaseException as e:
  receipt['status']='FAIL_CLOSED';receipt['error']=repr(e);receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save();raise
if __name__=='__main__':main()
