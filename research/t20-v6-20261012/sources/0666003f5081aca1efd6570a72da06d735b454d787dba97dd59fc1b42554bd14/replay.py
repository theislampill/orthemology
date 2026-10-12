#!/usr/bin/env python3
"""Replay only bundled custom Lean sources, against explicit exact-pinned prerequisites."""
from pathlib import Path
import argparse,datetime,json,os,re,shutil,subprocess,sys,time
from portable_core import sha,validate_files,order_modules,parse_audit,strip_comments,write_json,verify_manifest,reject_custom_shadows,check_fixture_stdout

def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--package-root',type=Path,default=Path(__file__).resolve().parents[1])
 ap.add_argument('--out',type=Path,required=True,help='New absent output directory; must be outside the package')
 ap.add_argument('--lean',type=Path,required=True,help='Official Linux x86_64 Lean 4.19.0 executable')
 ap.add_argument('--mathlib',type=Path,required=True,help='Exact git mathlib checkout with compiled official dependencies')
 ap.add_argument('--suite',action='append',help='Repeat to select suites; default is all included Lean suites')
 a=ap.parse_args();root=a.package_root.resolve();out=a.out.resolve();lean=a.lean.resolve();mathlib=a.mathlib.resolve()
 if out.exists() or out.is_relative_to(root):raise SystemExit('Output must be absent and outside the immutable package')
 # Verify integrity before creating the output or invoking any bundled source.
 manifest=root/'MASTER_MANIFEST.json'
 if not manifest.is_file():raise SystemExit('MASTER_MANIFEST.json is absent; package is not sealed for replay')
 expected=(root/'MASTER_MANIFEST.sha256').read_text().split()[0]
 if sha(manifest)!=expected:raise SystemExit('Master manifest seal mismatch')
 initial_manifest_digest=verify_manifest(root)
 defs=json.loads((root/'SUITES.json').read_text())['suites'];requested=a.suite or [s['id'] for s in defs]
 if not requested or len(set(requested))!=len(requested) or set(requested)-{s['id'] for s in defs}:raise SystemExit('Unknown or duplicate suite')
 pins=json.loads((root/'pins/TOOLCHAIN.json').read_text());deps=json.loads((root/'pins/lake-manifest.json').read_text())['packages']
 if sha(lean)!=pins['linux_x86_64_binary_sha256']:raise SystemExit('Wrong compiler binary hash')
 env=dict(os.environ);env.pop('LEAN_PATH',None);env.pop('LEAN_SYSROOT',None);env['LEAN_NUM_THREADS']='1';env['PYTHONDONTWRITEBYTECODE']='1'
 version=subprocess.check_output([str(lean),'--version'],env=env,text=True).strip()
 if version!='Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)':raise SystemExit('Wrong compiler version')
 dependency_readbacks=[];official_paths=[]
 for d in deps:
  p=mathlib if d['name']=='mathlib' else mathlib/'.lake/packages'/d['name']
  actual=subprocess.check_output(['git','-C',str(p),'rev-parse','HEAD'],text=True).strip()
  dirty=subprocess.check_output(['git','-C',str(p),'status','--porcelain','--untracked-files=no'],text=True)
  if actual!=d['rev'] or dirty:raise SystemExit('Wrong/dirty official dependency: '+d['name'])
  lib=p/'.lake/build/lib/lean'
  if lib.is_dir():official_paths.append(lib)
  dependency_readbacks.append({'name':d['name'],'revision':actual,'tracked_clean':True,'compiled_library':str(lib),'compiled_library_present':lib.is_dir()})
 out.mkdir(parents=True);record={'schema':'portable-custom-source-replay-v1','status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'manifest_sha256':initial_manifest_digest,'driver_sha256':sha(Path(__file__)),'compiler':version,'compiler_binary_sha256':sha(lean),'official_dependencies':dependency_readbacks,'external_build_scope':'Exact pinned official source revisions checked; prebuilt official .olean caches are reused. This is not a cold-network or full official-dependency rebuild.','custom_cache_policy':'All custom modules compiled from bundled byte-bound source into initially absent suite outputs. No historical custom .olean is imported.','suites':[]}
 def save():write_json(out/'REPLAY_RESULT.json',record)
 save()
 try:
  for suite in defs:
   if suite['id'] not in requested:continue
   sr=root/suite['source_root'];work=out/suite['id'];src=work/'sources';lib=work/'lib';logs=work/'logs';src.mkdir(parents=True);lib.mkdir();logs.mkdir()
   texts={m:(sr/Path(*m.split('.')).with_suffix('.lean')).read_text() for m in suite['module_order']}
   reject_custom_shadows(official_paths,suite['module_order'])
   if order_modules(texts,suite['module_order'])!=suite['module_order']:raise ValueError('Source dependency order differs from sealed graph')
   srec={'id':suite['id'],'status':'RUNNING','sources':{},'modules':[],'claim_sets':{},'historical_receipts':suite['historical_receipts']};record['suites'].append(srec);save()
   def run(label,args):
    start=time.monotonic();p=subprocess.run(args,cwd=src,env={**env,'LEAN_PATH':os.pathsep.join(map(str,[lib]+official_paths))},capture_output=True,text=True,timeout=900)
    (logs/(label+'.stdout')).write_text(p.stdout);(logs/(label+'.stderr')).write_text(p.stderr)
    rec={'module':label,'exit_code':p.returncode,'seconds':round(time.monotonic()-start,3),'command':args,'stdout_sha256':sha(logs/(label+'.stdout')),'stderr_sha256':sha(logs/(label+'.stderr'))};srec['modules'].append(rec);save()
    if p.returncode or re.search(r'\bsorryAx\b|\berror:|declaration uses .sorry.',p.stdout+p.stderr):raise ValueError('Compile failure: '+suite['id']+'/'+label)
    return p.stdout
   for m in suite['module_order']:
    rel=Path(*m.split('.')).with_suffix('.lean');original=sr/rel;copied=src/rel;copied.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(original,copied)
    clean=strip_comments(texts[m])
    if re.search(r'^\s*(?:axiom|constant)\s|\b(?:sorry|admit)\b',clean,re.M):raise ValueError('Unproved declaration/proof placeholder: '+m)
    srec['sources'][str(rel)]={'sha256':sha(copied),'bytes':copied.stat().st_size}
    target=lib/rel.with_suffix('.olean');target.parent.mkdir(parents=True,exist_ok=True)
    raw=run(m,[str(lean),'-j1','--root='+str(src),'-o',str(target),str(copied)])
    if m in suite.get('stdout_expectations',{}):srec['modules'][-1]['fixture_output']=check_fixture_stdout(raw,suite['stdout_expectations'][m])
    if not target.is_file() or not target.stat().st_size:raise ValueError('Missing custom compiled artifact '+m)
    srec['modules'][-1]['olean_sha256']=sha(target);save();print(suite['id'],m,flush=True)
   # Each historical claim set is audited independently; overlap is preserved, never added up.
   for claim,targets in suite['targets'].items():
    name='PortableAudit_'+re.sub('[^A-Za-z0-9_]','_',claim)
    audit='\n'.join('import '+m for m in suite['module_order'])+'\nset_option pp.universes true\nset_option format.width 120\n'
    audit+='\n'.join('#check @'+n+'\n#print axioms '+n for n in targets)+'\n'
    f=src/(name+'.lean');f.write_text(audit);raw=run(name,[str(lean),'-j1','--root='+str(src),'-o',str(lib/(name+'.olean')),str(f)])
    srec['claim_sets'][claim]={'target_count':len(targets),'declarations':parse_audit(raw,targets),'audit_source_sha256':sha(f)};save()
   for rel,binding in srec['sources'].items():
    if sha(src/rel)!=binding['sha256'] or sha(sr/rel)!=binding['sha256']:raise ValueError('Source changed during replay: '+rel)
   srec['status']='FRESH_CUSTOM_SOURCE_BUILD_AND_TYPE_AXIOM_READBACK_PASS';save()
  verify_manifest(root,initial_manifest_digest)
  record['status']='PASS';record['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();save()
 except Exception as e:
  record['status']='FAIL_CLOSED';record['error']=repr(e);save();raise
 print(json.dumps({'status':record['status'],'receipt':str(out/'REPLAY_RESULT.json'),'receipt_sha256':sha(out/'REPLAY_RESULT.json'),'suites':[s['id'] for s in record['suites']]}))
if __name__=='__main__':main()
