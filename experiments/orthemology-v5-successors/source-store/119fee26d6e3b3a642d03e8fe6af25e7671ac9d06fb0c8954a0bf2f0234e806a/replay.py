#!/usr/bin/env python3
"""Portable source-only Orthemic existence-certificate replay; no downloads."""
from pathlib import Path
import argparse,datetime,hashlib,json,os,re,subprocess,sys,time
if sys.flags.optimize: raise RuntimeError('Optimized Python is refused, including --verify-only')
sys.dont_write_bytecode=True
from verify_dependency_identity import verify_dependencies
ROOT=Path(__file__).resolve().parent
SOURCE_MANIFEST_SHA256='5a5e4e8a129b70fe713e76f7b24a97823751264fe4bd67a280682b09a407979f'
sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest()
def fail(message):raise RuntimeError(message)
def require(condition,message):
 if not condition:fail(message)
def verify():
 require(sha(ROOT/'SOURCE_MANIFEST.json')==SOURCE_MANIFEST_SHA256,'Source manifest identity mismatch')
 manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
 expected={row['path']:row for row in manifest['sources']}
 actual={str(p.relative_to(ROOT)) for p in ROOT.rglob('*.lean')}
 require(actual==set(expected),'Lean source census mismatch')
 for path,row in expected.items():
  p=ROOT/path;require(not p.is_symlink() and p.is_file() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'Source changed: '+path)
 pub=json.loads((ROOT/'PUBLIC_MANIFEST.json').read_text())
 files={row['path']:row for row in pub['files']}
 for p in ROOT.rglob('*'):require(not p.is_symlink(),'Public symlinks are refused')
 actualfiles={str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and p!=ROOT/'PUBLIC_MANIFEST.json'}
 require(actualfiles==set(files),'Public file census mismatch')
 for path,row in files.items():
  p=ROOT/path;require(not p.is_symlink() and sha(p)==row['sha256'] and p.stat().st_size==row['bytes'],'Public file changed: '+path)
 by={row['module']:ROOT/row['path'] for row in manifest['sources'] if row['group']=='inherited-cost'}
 states={};order=[]
 def visit(name):
  if states.get(name)==2:return
  require(states.get(name)!=1,'Cyclic inherited import');states[name]=1
  for line in by[name].read_text().splitlines():
   if line.startswith('import '):
    for dep in line[7:].split():
     if dep in by:visit(dep)
     else:require(dep.startswith(('Mathlib','Lean','Std','Init')),'Missing custom dependency '+dep)
  states[name]=2;order.append(name)
 visit('GlobalParitySufficiency');require(set(order)==set(by) and len(order)==87,'Incorrect selected cost closure')
 return manifest,order

def main():
 ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--verify-only',action='store_true');ap.add_argument('--lean-bin',type=Path);ap.add_argument('--mathlib',type=Path);ap.add_argument('--mathlib-archive',type=Path);ap.add_argument('--out',type=Path);a=ap.parse_args()
 manifest,inherited=verify()
 if a.verify_only:print('PASS_SOURCE_FREEZE: 87 exact inherited cost modules; independent checker/proofs/controls. No proof replay performed.');return
 if any(x is None for x in [a.lean_bin,a.mathlib,a.out]):ap.error('--lean-bin, --mathlib and --out are required')
 lean=(a.lean_bin/'lean').resolve();math=a.mathlib.resolve();out=a.out.resolve()
 require(not out.exists(),'Output directory must be absent')
 for protected in [ROOT,math,lean.parent.parent]:require(not out.is_relative_to(protected),'Output is inside protected input')
 pins=json.loads((ROOT/'DEPENDENCY_PINS.json').read_text())
 require(sha(lean)==pins['lean_binary_sha256'],'Lean binary digest mismatch')
 require(subprocess.check_output([str(lean),'--version'],text=True).strip()==pins['lean_version'],'Lean version mismatch')
 identity=verify_dependencies(math,a.mathlib_archive,pins)
 out.mkdir(parents=True);build=out/'build';build.mkdir();logs=out/'logs';logs.mkdir()
 libs=[build,math/'.lake/build/lib/lean']+sorted((math/'.lake/packages').glob('*/.lake/build/lib/lean'))
 require((libs[1]/'Mathlib.olean').is_file(),'Official Mathlib object cache required')
 env=dict(os.environ);env.pop('LEAN_SRC_PATH',None);env['LEAN_PATH']=':'.join(map(str,libs))
 result={'status':'RUNNING','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'source_manifest_sha256':sha(ROOT/'SOURCE_MANIFEST.json'),'public_manifest_sha256':sha(ROOT/'PUBLIC_MANIFEST.json'),'dependency_identity':identity,'custom_objects_reused':False,'added_heartbeat_overrides':False,'new_module_heartbeat_budget':'default','inherited_source_heartbeat_overrides':{'FiniteChainTrajectory':800000,'GeneratedParitySuccess':800000},'jobs':1,'module_wall_seconds':180,'runs':[]}
 def save(): (out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
 def run(label,source,expected=0,runenv=env,obj=None,cfile=None,source_root=None):
  cmd=[str(lean),'-j1','--root='+str(source_root if source_root is not None else source.parent)]
  if obj is not None:obj.parent.mkdir(parents=True,exist_ok=True);cmd+=['-o',str(obj)]
  if cfile is not None:cmd+=['-c',str(cfile)]
  cmd+=[str(source)];t=time.monotonic()
  try:p=subprocess.run(cmd,env=runenv,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=180);txt=p.stdout;code=p.returncode
  except subprocess.TimeoutExpired as e:txt=(e.stdout.decode() if isinstance(e.stdout,bytes) else e.stdout or '')+'\nWALL_CLOCK_LIMIT_180';code=None
  log=logs/(label+'.log');log.write_text(txt)
  rec={'label':label,'source_sha256':sha(source),'exit_code':code,'expected_exit':expected,'elapsed_seconds':round(time.monotonic()-t,3),'log':str(log.relative_to(out)),'log_sha256':sha(log)}
  if code==0 and obj is not None:rec['object_sha256']=sha(obj)
  if cfile is not None and cfile.exists():rec.update(c_sha256=sha(cfile),c_bytes=cfile.stat().st_size)
  result['runs'].append(rec);save();print(label,code,flush=True)
  require(code==expected,'Unexpected Lean outcome '+label)
  if expected==0:require('error:' not in txt and "declaration uses 'sorry'" not in txt,'Invalid positive compilation '+label)
  else:require('did not evaluate to' in txt,'Expected concrete executable guard rejection '+label)
  for block in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',txt):
   require(set(x.strip() for x in block.split(',') if x.strip())<= {'propext','Classical.choice','Quot.sound'},'Nonstandard axiom '+label)
  return txt
 save()
 try:
  for mod in inherited:run('cost-'+mod,ROOT/'inherited/cost/src'/Path(*mod.split('.')).with_suffix('.lean'),obj=build/Path(*mod.split('.')).with_suffix('.olean'),source_root=ROOT/'inherited/cost/src')
  for mod in manifest['own_order']:run(mod,ROOT/'src'/(mod+'.lean'),obj=build/(mod+'.olean'))
  for mod in manifest['positive_controls']:run(mod,ROOT/'controls'/(mod+'.lean'),obj=build/(mod+'.olean'))
  for mod in ['CertificateData','CertificateOrder','CertificatePath','CertificateSyntax','CertificateComposition','CertificateBinding']:
   cg=out/'codegen';cg.mkdir(exist_ok=True);run('C-'+mod,ROOT/'src'/(mod+'.lean'),obj=cg/(mod+'.olean'),cfile=cg/(mod+'.c'))
  for mutant,control in [('PathLengthMutant','PathLengthMutationControl'),('PathEdgesMutant','PathEdgesMutationControl')]:
   run(mutant,ROOT/'mutations'/(mutant+'.lean'),obj=build/(mutant+'.olean'));run(control,ROOT/'mutations'/(control+'.lean'),expected=1)
  base=(ROOT/'src/CertificateSyntax.lean').read_text()
  old='''∀ y, (I.live N.support e y).Nonempty →
      if I.live N.support e y = N.support then y ∈ N.states
      else I.live N.support e y ⊂ N.support ∧
        ∃ child ∈ c, child.support = I.live N.support e y ∧ y ∈ child.states'''
  parity='''∀ σ ∈ B, (∀ e ∈ c.pairs, ∀ y, I.row σ e y = I.row θ e y) →
    ∃ e ∈ c.pairs, I.priority σ e % 2 = 0 ∧ ∀ f ∈ c.pairs, I.priority σ e ≤ I.priority σ f'''
  require(base.count(old)==1 and base.count(parity)==2,'Mutation derivation anchor mismatch')
  mutations=[('AllReceiptsRemoved',base.replace(old,'True'),'#guard !(bodyCheck reveal [child₀,parent])\n'),('RivalParityRemoved',base.replace(parity,'True',1),'#guard !(check latentEqualRows [latentNode] {0,1} 0)\n')]
  for label,text,test in mutations:
   m=out/'mutations'/label;(m/'build').mkdir(parents=True);(m/'src').mkdir()
   (m/'src/CertificateSyntax.lean').write_text(text);(m/'src/CertificateFixtures.lean').write_bytes((ROOT/'controls/CertificateFixtures.lean').read_bytes());(m/'src/MutationControl.lean').write_text('import CertificateFixtures\nopen OrthemicCertificate OrthemicCertificate.Fixtures\n'+test)
   menv=dict(env);menv['LEAN_PATH']=str(m/'build')+':'+env['LEAN_PATH']
   for mod in ['CertificateSyntax','CertificateFixtures','MutationControl']:run(label+'-'+mod,m/'src'/(mod+'.lean'),expected=1 if mod=='MutationControl' else 0,runenv=menv,obj=None if mod=='MutationControl' else m/'build'/(mod+'.olean'))
  result.update(status='PASS_FRESH_CLOSURE_CONTROLS_AXIOMS_AUDIT_CODEGEN_AND_MUTATIONS',finished_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),linked_standalone_execution_claimed=False);save()
 except Exception as exc:result.update(status='FAILED_CLOSED',error=str(exc));save();raise
if __name__=='__main__':main()
