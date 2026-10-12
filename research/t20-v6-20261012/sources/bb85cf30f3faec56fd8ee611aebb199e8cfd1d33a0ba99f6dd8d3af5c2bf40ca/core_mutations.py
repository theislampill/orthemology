#!/usr/bin/env python3
"""Fresh affected-source compile controls. Mutants never touch the candidate."""
import argparse,hashlib,json,os,shutil,subprocess
from pathlib import Path

def main():
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--env',type=Path,required=True);p.add_argument('--baseline',type=Path);a=p.parse_args()
 base=Path(__file__).resolve().parents[1];candidate=base/'candidate-v1'
 if a.out.exists():raise SystemExit('Output must be absent')
 a.out.mkdir(parents=True)
 envroot=a.env.resolve();lean=envroot/'toolchain/lean-4.19.0-linux/bin/lean';math=envroot/'mathlib4'
 libs=[math/'.lake/build/lib/lean']+sorted(math.glob('.lake/packages/*/.lake/build/lib/lean'))
 order=['PruningKernel','EndComponents','FiniteReachability','ExecutablePruning','CoBuchiSpecialisation','MarkovSupportAdapter','ControlTests','AdapterTests']
 baseline_root=a.baseline.resolve() if a.baseline else base/'full-cold-v1'
 baseline=baseline_root/'hidden_parity_pruning/build'
 receipt=json.loads((baseline_root/'REPLAY_RESULT.json').read_text())
 manifest_hash=hashlib.sha256((candidate/'MASTER_MANIFEST.json').read_bytes()).hexdigest()
 assert receipt['status']=='PASS' and receipt['input_manifest_sha256']==manifest_hash
 for row in receipt['suites'][0]['modules']:
  obj=baseline/(row['module']+'.olean')
  assert row['status']=='FRESH_COMPILE' and hashlib.sha256(obj.read_bytes()).hexdigest()==row['olean_sha256']
 assert hashlib.sha256(lean.read_bytes()).hexdigest()==receipt['lean_sha256']
 mutations=[
  ('even_layer_deleted','PruningKernel','priority σ e % 2 = 1\n\nnoncomputable def step','priority σ e % 2 = 0\n\nnoncomputable def step'),
  ('insufficient_pair_fuel','PruningKernel','maximalComponents C (iterate C B row priority θ U.card U)','maximalComponents C (iterate C B row priority θ (U.card - 1) U)'),
  ('zero_reachability_fuel','FiniteReachability','saturate r (Fintype.card State) {s}','saturate r 0 {s}'),
  ('union_instead_of_live_intersection','MarkovSupportAdapter','fun y => ∀ σ ∈ B, 0 < P.row σ e y','fun y => ∃ σ ∈ B, 0 < P.row σ e y'),
  ('swapped_cobuchi_encoding','CoBuchiSpecialisation','if good e then 2 else 1','if good e then 0 else 1'),
 ]
 results=[]
 for name,start,old,new in mutations:
  d=a.out/name;src=d/'src';build=d/'build';src.mkdir(parents=True);build.mkdir()
  for m in order:shutil.copy2(candidate/'src'/f'{m}.lean',src/f'{m}.lean')
  target=src/f'{start}.lean';raw=target.read_text();assert raw.count(old)>=1,(name,raw.count(old))
  target.write_text(raw.replace(old,new,1))
  changed={start};failed=None;steps=[]
  for m in order:
   imports=[s.split()[1] for s in (src/f'{m}.lean').read_text().splitlines() if s.startswith('import ')]
   affected=m in changed or any(i in changed for i in imports)
   if not affected:
    shutil.copy2(baseline/f'{m}.olean',build/f'{m}.olean');continue
   changed.add(m)
   env=dict(os.environ);env.pop('LEAN_SRC_PATH',None);env['LEAN_PATH']=':'.join(map(str,[build]+libs))
   cmd=[str(lean),'-j1','--root='+str(src.resolve()),'-o',str((build/f'{m}.olean').resolve()),str((src/f'{m}.lean').resolve())]
   run=subprocess.run(cmd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
   (d/f'{m}.log').write_text(run.stdout);steps.append({'module':m,'exit':run.returncode})
   if run.returncode:failed=m;break
  assert failed is not None,f'Mutation not rejected: {name}'
  results.append({'mutation':name,'mutated_module':start,'source_sha256':hashlib.sha256(target.read_bytes()).hexdigest(),'first_rejected_module':failed,'steps':steps,'status':'REJECTED'})
  print(name,failed,flush=True)
 result={'status':'PASS_ALL_FIVE_CORE_MUTATIONS_REJECTED','mutations':results,'policy':'Only unaffected reviewer-fresh predecessor objects reused; affected source and downstream never reused'}
 (a.out/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
if __name__=='__main__':main()
