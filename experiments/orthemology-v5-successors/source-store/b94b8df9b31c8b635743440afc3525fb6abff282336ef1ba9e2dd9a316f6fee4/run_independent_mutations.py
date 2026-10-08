#!/usr/bin/env python3
"""Reproducible semantic mutants in reviewer-owned copies only."""
import argparse,hashlib,json,os,subprocess,sys,time
from pathlib import Path
HERE=Path(__file__).resolve().parent
DEFAULT=HERE.parents[1]/'research'/'occurrence-continuation'/'checker'
MUTATIONS=[
 ('current_only','context_effects.py',[("Ref(consumed)","Ref(0)")]),
 ('compose_depth_abs_shift','context_effects.py',[("depth=max(f.depth,g.depth-(p-f.consumed))","depth=max(f.depth,g.depth+abs(p-f.consumed))")]),
 ('drop_second_constraints','context_effects.py',[("constraints=f.constraints+tuple((subst(x),o) for x,o in g.constraints)","constraints=f.constraints")]),
 ('snapshot_blind_equality','context_effects.py',[("from dataclasses import dataclass","from dataclasses import dataclass, field"),("    snapshot: str","    snapshot: str = field(compare=False)")]),
 ('nonconvex_envelope','read_cover.py',[("if ix and ix!=list(range(ix[0],ix[-1]+1)):raise BadCoverage('justified role coverage is not convex on demanded origins')","if False:raise BadCoverage('justified role coverage is not convex on demanded origins')")]),
 ('retired_service_available','read_cover.py',[("if w.eligible and w.adequate","if w.adequate")]),
 ('locality_ignores_response','read_cover.py',[("if all(response(alt,w)==response(pos,w) for w in menu if o not in w.coverage):found=True;break","if True:found=True;break")]),
 ('adequacy_ignores_fibres','read_cover.py',[("if observation in seen and seen[observation]!=values:return False","if observation in seen and seen[observation]!=values:return True")]),
 ('replace_adaptive_with_cover','read_cover.py',[("return max(solve(p) for p in parts)","return cover_dp(tuple(worlds[0].keys()),menu).cost")]),
]

def main():
 p=argparse.ArgumentParser();p.add_argument('--candidate',type=Path,default=DEFAULT);p.add_argument('--directory',type=Path,default=HERE/'mutation-copies');args=p.parse_args()
 args.directory.mkdir(exist_ok=True)
 originals={name:(args.candidate/name).read_text() for name in ['context_effects.py','read_cover.py']}
 records=[]
 for name,filename,changes in MUTATIONS:
  target=args.directory/name;target.mkdir(exist_ok=True)
  for fn,source in originals.items():(target/fn).write_text(source)
  source=originals[filename]
  replacements=[]
  for before,after in changes:
   count=source.count(before)
   if not count:raise RuntimeError(f'mutation target changed: {name}: {before}')
   replacements.append({'old':before,'new':after,'occurrences':count})
   source=source.replace(before,after)
  (target/filename).write_text(source)
  command=[sys.executable,str(HERE/'run_independent_review.py'),'--candidate',str(target),'--output',str(target/'unexpected-pass.json')]
  start=time.time();run=subprocess.run(command,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
  (target/'run.log').write_text(run.stdout)
  killed=run.returncode!=0 and 'AssertionError:' in run.stdout
  records.append({'name':name,'candidate_file':filename,'mutated_sha256':hashlib.sha256((target/filename).read_bytes()).hexdigest(),'replacements':replacements,'exit':run.returncode,'killed_by_independent_assertion':killed,'last_line':run.stdout.strip().splitlines()[-1] if run.stdout.strip() else '', 'seconds':round(time.time()-start,4)})
  print(name,'KILLED' if killed else 'UNRESOLVED',flush=True)
  if not killed: print(run.stdout,flush=True)
 result={'status':'PASS' if all(r['killed_by_independent_assertion'] for r in records) else 'FAIL','count':len(records),'mutation_boundary':'only reviewer-owned file copies; original files unchanged','source_hashes':{n:hashlib.sha256(s.encode()).hexdigest() for n,s in originals.items()},'records':records}
 (HERE/'INDEPENDENT_MUTATION_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
 if result['status']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
