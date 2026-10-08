#!/usr/bin/env python3
"""Replay the exact accepted author packet, then independent reviewer controls and five mutations. No downloads."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,subprocess,sys,time
if sys.flags.optimize:raise RuntimeError('Optimized Python is refused')
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
SOURCE_SHA='5a5e4e8a129b70fe713e76f7b24a97823751264fe4bd67a280682b09a407979f'
PUBLIC_SHA='9d8675b5d180d35651ee3a95aec28b3a977f52c0a46b7e9831ca88366736cfbd'
SOURCE_IDENTICAL_V2_PUBLIC_SHA='0e72d20f3467905fbf63bddf45531a5d63e4b975bc86a855bf92523477f33475'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--author-packet',type=Path,required=True);ap.add_argument('--verify-only',action='store_true');ap.add_argument('--lean-bin',type=Path);ap.add_argument('--mathlib',type=Path);ap.add_argument('--mathlib-archive',type=Path);ap.add_argument('--out',type=Path);ap.add_argument('--core-replay',type=Path,help='Optional already successful consumer-local cold core replay; all 95 source/object bindings are rechecked.');a=ap.parse_args()
 author=a.author_packet.resolve();need(sha(author/'SOURCE_MANIFEST.json')==SOURCE_SHA,'Wrong source packet');need(sha(author/'PUBLIC_MANIFEST.json')==PUBLIC_SHA,'Wrong complete public packet')
 manifest=json.loads((ROOT/'REVIEW_MANIFEST.json').read_text());expected={r['path']:r for r in manifest['files']}
 actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p!=ROOT/'REVIEW_MANIFEST.json'}
 need(actual==set(expected),'Reviewer file census mismatch')
 for p in ROOT.rglob('*'):need(not p.is_symlink(),'Reviewer symlinks refused')
 for name,r in expected.items():need(sha(ROOT/name)==r['sha256'] and (ROOT/name).stat().st_size==r['bytes'],'Reviewer file changed: '+name)
 source_manifest=json.loads((ROOT/'REVIEW_SOURCE_MANIFEST.json').read_text())
 for row in source_manifest['sources']:
  need(not Path(row['path']).is_absolute() and '..' not in Path(row['path']).parts,'Unsafe review source path')
  need(sha(ROOT/row['path'])==row['sha256'],'Review source identity mismatch')
 subprocess.run([sys.executable,str(author/'replay.py'),'--verify-only'],check=True)
 if a.verify_only:print('PASS_EXACT_AUTHOR_AND_REVIEW_SOURCE_FREEZES; no proof replay performed');return
 need(all(x is not None for x in [a.lean_bin,a.mathlib,a.out]),'Provide --lean-bin, --mathlib, --out')
 lean=(a.lean_bin/'lean').resolve();math=a.mathlib.resolve();out=a.out.resolve();need(not out.exists(),'Output must be absent')
 for protected in [ROOT,author,math,lean.parent.parent]:need(not out.is_relative_to(protected),'Output must not be inside protected inputs')
 pins=json.loads((author/'DEPENDENCY_PINS.json').read_text());need(sha(lean)==pins['lean_binary_sha256'],'Wrong Lean binary')
 need(subprocess.check_output([str(lean),'--version'],text=True).strip()==pins['lean_version'],'Wrong Lean version')
 env=dict(os.environ)
 for k in list(env):
  if k.startswith('LD_') or k in ['LEAN_SRC_PATH','LEAN_SYSROOT','LEAN_PATH']:env.pop(k)
 out.mkdir(parents=True)
 core=a.core_replay.resolve() if a.core_replay else out/'core'
 if a.core_replay is None:
  cmd=[sys.executable,str(author/'replay.py'),'--lean-bin',str(a.lean_bin.resolve()),'--mathlib',str(math),'--out',str(core)]
  if a.mathlib_archive:cmd+=['--mathlib-archive',str(a.mathlib_archive.resolve())]
  with (out/'core-driver.log').open('w') as f:subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
 cr=json.loads((core/'RESULT.json').read_text());need(cr['status']=='PASS_FRESH_CLOSURE_CONTROLS_AXIOMS_AUDIT_CODEGEN_AND_MUTATIONS','Core did not finish successfully');need(cr['source_manifest_sha256']==SOURCE_SHA and cr['public_manifest_sha256'] in [PUBLIC_SHA,SOURCE_IDENTICAL_V2_PUBLIC_SHA],'Core belongs to another packet');need(cr['custom_objects_reused'] is False,'Core must be a cold custom-source replay')
 rows=json.loads((author/'SOURCE_MANIFEST.json').read_text())['sources'];runs={r['label']:r for r in cr['runs']}
 checked=[]
 for r in rows:
  if r['group'] not in ['own','inherited-cost']:continue
  name=r['module'];label=('cost-' if r['group']=='inherited-cost' else '')+name;run=runs[label];p=core/'build'/Path(*name.split('.')).with_suffix('.olean')
  need(run['exit_code']==0 and run['source_sha256']==r['sha256'] and sha(p)==run['object_sha256'],'Core source/object mismatch: '+name);checked.append(name)
 need(len(checked)==95,'Incorrect production closure count')
 build=out/'review-build';build.mkdir();logs=out/'logs';logs.mkdir()
 env['LEAN_PATH']=':'.join(map(str,[build,core/'build',math/'.lake/build/lib/lean']+sorted((math/'.lake/packages').glob('*/.lake/build/lib/lean'))))
 result={'status':'RUNNING','review_source_manifest_sha256':sha(ROOT/'REVIEW_SOURCE_MANIFEST.json'),'review_driver_sha256':sha(Path(__file__)),'source_manifest_sha256':SOURCE_SHA,'public_manifest_sha256':PUBLIC_SHA,'qualified_cold_core_result_sha256':sha(core/'RESULT.json'),'core_packet_public_manifest_sha256':cr['public_manifest_sha256'],'source_identical_command_preserving_v2_bridge':cr['public_manifest_sha256']==SOURCE_IDENTICAL_V2_PUBLIC_SHA,'qualified_production_object_count':95,'author_custom_objects_reused':False,'prior_core_replay_explicitly_qualified':a.core_replay is not None,'jobs':1,'added_heartbeat_overrides':False,'new_module_heartbeat_budget':'default','preserved_inherited_heartbeat_settings':{'FiniteChainTrajectory':800000,'GeneratedParitySuccess':800000},'wall_seconds_per_module':180,'runs':[]}
 def save():(out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 def run(label,source,target,expected_exit=0,runenv=env):
  cmd=[str(lean),'-j1','--root='+str(source.parent),'-o',str(target),str(source)];t=time.monotonic()
  try:p=subprocess.run(cmd,env=runenv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180);text=p.stdout;code=p.returncode
  except subprocess.TimeoutExpired as e:text=(e.stdout.decode() if isinstance(e.stdout,bytes) else e.stdout or '')+'\nWALL_CLOCK_LIMIT_180_SECONDS';code=None
  log=logs/(label+'.log');log.write_text(text);row={'label':label,'source_sha256':sha(source),'exit_code':code,'expected_exit':expected_exit,'seconds':round(time.monotonic()-t,3),'log_sha256':sha(log),'log':str(log.relative_to(out))}
  if code==0:row['object_sha256']=sha(target)
  result['runs'].append(row);save();print(label,code,flush=True);need(code==expected_exit,'Unexpected result: '+label)
  if expected_exit==1:need('did not evaluate to `true`' in text,'Not a concrete guard failure: '+label)
  else:need('error:' not in text and "declaration uses 'sorry'" not in text,'Invalid positive result: '+label)
  for b in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',text):need(set(x.strip() for x in b.split(',') if x.strip())<={'propext','Classical.choice','Quot.sound'},'Nonstandard axiom')
 save()
 try:
  for mod in ['ReviewerControls','ReviewerCompositionControls','ReviewerPathReadback','ReviewerFullDependencies','ReviewerSemanticReadback']:run(mod,ROOT/'tests'/(mod+'.lean'),build/(mod+'.olean'))
  source=(author/'src/CertificateSyntax.lean').read_text()
  closure='''∀ y, (I.live N.support e y).Nonempty →
      if I.live N.support e y = N.support then y ∈ N.states
      else I.live N.support e y ⊂ N.support ∧
        ∃ child ∈ c, child.support = I.live N.support e y ∧ y ∈ child.states'''
  parity='''∀ σ ∈ B, (∀ e ∈ c.pairs, ∀ y, I.row σ e y = I.row θ e y) →
    ∃ e ∈ c.pairs, I.priority σ e % 2 = 0 ∧ ∀ f ∈ c.pairs, I.priority σ e ≤ I.priority σ f'''
  keys='(N.obligations.map (fun o => (o.state,o.candidate))).toFinset = N.states ×ˢ N.support'
  need(source.count(closure)==1 and source.count(parity)==2 and source.count(keys)==1,'Mutation anchor mismatch')
  mutants=[('AllReceiptsRemoved',source.replace(closure,'True')),('RivalParityRemoved',source.replace(parity,'True',1)),('SupportOnlyMatching',source.replace('∀ y, I.row σ e y = I.row θ e y','∀ y, (0 < I.row σ e y ↔ 0 < I.row θ e y)')),('MenuGrantRemoved',source.replace('e.2 ∈ I.menu N.support e.1','True')),('ExactKeysRemoved',source.replace(keys,'True'))]
  for label,text in mutants:
   m=out/'mutations'/label;(m/'src').mkdir(parents=True);(m/'build').mkdir();(m/'src/CertificateSyntax.lean').write_text(text);(m/'src/ReviewerControls.lean').write_bytes((ROOT/'tests/ReviewerControls.lean').read_bytes());me=dict(env);me['LEAN_PATH']=str(m/'build')+':'+env['LEAN_PATH']
   run(label+'-Syntax',m/'src/CertificateSyntax.lean',m/'build/CertificateSyntax.olean',runenv=me);run(label+'-Controls',m/'src/ReviewerControls.lean',m/'build/ReviewerControls.olean',1,me)
  result['status']='PASS_INDEPENDENT_CONTROLS_READBACKS_DEPENDENCIES_AND_FIVE_MUTATIONS';save()
 except Exception as e:result.update(status='FAILED_CLOSED',error=str(e));save();raise
if __name__=='__main__':main()
