#!/usr/bin/env python3
"""Cold independent review replay. Standard library only; no installation."""
import argparse,hashlib,importlib.util,json,os,re,subprocess,sys
from pathlib import Path
sys.dont_write_bytecode=True
os.environ['PYTHONDONTWRITEBYTECODE']='1'

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(p,j):Path(p).write_text(json.dumps(j,indent=2,sort_keys=True)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--env',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 base=Path(__file__).resolve().parents[1];out=a.out.resolve();envroot=a.env.resolve();candidate=base/'candidate-v1'
 if out.exists() or out.is_relative_to(candidate):raise SystemExit('Output must be fresh and outside candidate')
 def verify_review():
  if not (base/'MANIFEST.json').exists():return
  manifest=json.loads((base/'MANIFEST.json').read_text());expected={'MANIFEST.json'}
  for item in manifest['files']:
   p=base/item['path'];assert p.resolve().is_relative_to(base) and p.is_file() and not p.is_symlink() and sha(p)==item['sha256'],p
   assert item['path'] not in expected;expected.add(item['path'])
  actual={str(p.relative_to(base)) for p in base.rglob('*') if p.is_file() or p.is_symlink()}
  assert actual==expected,actual^expected
 if (base/'MANIFEST.json').exists() and out.is_relative_to(base):raise SystemExit('A sealed review requires output outside its immutable packet')
 verify_review()
 out.mkdir(parents=True)
 result={'status':'RUNNING','candidate_manifest_sha256':sha(candidate/'MASTER_MANIFEST.json'),'review_manifest_sha256':sha(base/'MANIFEST.json') if (base/'MANIFEST.json').exists() else None,'review_sources':{str(p.relative_to(base)):sha(p) for p in sorted((base/'src').glob('Reviewer*Controls.lean'))},'review_checks':{str(p.relative_to(base)):sha(p) for p in sorted((base/'checks').glob('*.py'))},'stages':[]}
 save(out/'RESULT.json',result)
 leanbin=envroot/'toolchain/lean-4.19.0-linux/bin';math=envroot/'mathlib4';lean=leanbin/'lean'
 def run(label,cmd,env=None):
  p=subprocess.run(list(map(str,cmd)),env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  log=out/(label+'.log');log.write_text(p.stdout)
  result['stages'].append({'stage':label,'exit':p.returncode,'log_sha256':sha(log)});save(out/'RESULT.json',result)
  if p.returncode:raise RuntimeError(label+' failed; see '+str(log))
  print(label,'PASS',flush=True)
  return p.stdout
 try:
  run('candidate_replay',[sys.executable,candidate/'tooling/replay_lean.py','--root',candidate,'--lean-bin',leanbin,'--mathlib',math,'--out',out/'cold','--suites','global_parity_necessity','--no-reuse'])
  spec=importlib.util.spec_from_file_location('review_portable_core',candidate/'tooling/portable_core.py');core=importlib.util.module_from_spec(spec);spec.loader.exec_module(core)
  receipt=json.loads((out/'cold/REPLAY_RESULT.json').read_text());assert receipt['status']=='PASS' and receipt['fresh_custom_objects']==66
  build=out/'cold/global_parity_necessity/build';src=out/'reviewer-source';src.mkdir()
  libs=[math/'.lake/build/lib/lean']+sorted(math.glob('.lake/packages/*/.lake/build/lib/lean'))
  env=dict(os.environ);env.pop('LEAN_SRC_PATH',None);env['LEAN_PATH']=':'.join(map(str,[build]+libs));env['PYTHONDONTWRITEBYTECODE']='1'
  targets=[]
  for mod,ns in [('ReviewerAdaptiveControls','HiddenParity.IndependentAdaptive'),('ReviewerGlobalControls','HiddenParity.IndependentGlobal')]:
   text=(base/'src'/f'{mod}.lean').read_text();core.check_source(text);target=src/f'{mod}.lean';target.write_text(text)
   output=run(mod,[lean,'-j1','--root='+str(src),'-o',build/f'{mod}.olean',target],env);core.check_diagnostics(output)
   targets += [ns+'.'+n for n in re.findall(r'^theorem\s+(\w+)',text,re.M)]
  targets += ['HiddenParity.IndependentGlobal.revealingWinning']
  readback=src/'Readback.lean';readback.write_text('import ReviewerAdaptiveControls\nimport ReviewerGlobalControls\n'+''.join(f'#check @{t}\n#print axioms {t}\n' for t in targets))
  output=run('reviewer_readback',[lean,'-j1',readback],env);core.check_diagnostics(output);axioms=core.parse_readback(output,targets);save(out/'REVIEWER_AXIOMS.json',axioms)
  result['reviewer_theorems']=len(targets)
  run('prefix_controls',[sys.executable,base/'checks/prefix_controls.py','--out',out/'prefix'])
  run('oracle_generate',[sys.executable,base/'checks/region_oracle.py','--out',out/'oracle'])
  oracle=run('oracle_lean',[lean,'-j1','--run',out/'oracle/Oracle.lean'],env)
  cases=json.loads((out/'oracle/CASES.json').read_text());expected=[[i]+c['expected'] for i,c in enumerate(cases)]
  actual=[list(map(int,line.split(','))) for line in oracle.splitlines()];assert actual==expected
  save(out/'ORACLE_RESULT.json',{'status':'PASS','systems':len(cases),'support_comparisons':4*len(cases),'output_sha256':sha(out/'oracle_lean.log')})
  run('core_mutations',[sys.executable,base/'checks/core_mutations.py','--env',envroot,'--baseline',out/'cold','--out',out/'core-mutants'])
  core.verify(candidate);verify_review()
  for rel,h in dict(result['review_sources'],**result['review_checks']).items():assert sha(base/rel)==h
  result['status']='PASS_SCOPED_COLD_REVIEW_REPLAY';result['source_module_count']=66;result['author_readbacks']=720;result['core_mutations']=5;result['prefix_controls']=json.loads((out/'prefix/RESULT.json').read_text());result['oracle_cases']=len(cases)
  save(out/'RESULT.json',result);print(result['status'],flush=True)
 except BaseException as e:
  result['status']='FAIL_CLOSED';result['error']=repr(e);save(out/'RESULT.json',result);raise
if __name__=='__main__':main()
