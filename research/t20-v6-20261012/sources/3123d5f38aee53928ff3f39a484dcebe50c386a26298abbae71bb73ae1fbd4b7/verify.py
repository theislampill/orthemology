#!/usr/bin/env python3
"""Fresh replay of only the three additive modules, with retained-input pins."""
from pathlib import Path
import hashlib, json, os, subprocess, sys
ROOT = Path(__file__).resolve().parent
W = ROOT.parent
V = ROOT / 'validation'
MODULES = ['FullESigmaElimination', 'FullESigmaScopeControls', 'FullESigmaBoundary']
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def verify(manifest):
    pins = json.loads(manifest.read_text())
    bad = [{'path': p, 'expected': h, 'actual': digest(W/p) if (W/p).exists() else None}
           for p,h in pins.items() if not (W/p).exists() or digest(W/p) != h]
    if bad: raise RuntimeError(json.dumps(bad, indent=2))
    return len(pins)
def retained_paths():
    heads = ['hase-sigma-elimination-equivalence-20261010/validation',
      'hase-full-e-dependent-induction-20261010/validation',
      'hase-rigidity-initiality-20261010/validation',
      'hase-type-parameter-substitution-20261010/validation',
      'hase-dependent-substitution-20261010/validation',
      'hase-church-structural-20261010/validation']
    tails = ['hase-closed-church-completeness-review-20261010/fresh-lib',
      'hase-complete-development-review-20261010/fresh-lib',
      'hase-effective-instance-assessment-20261010/validation',
      'hase-sigma-tag-independent-review-20261010/fresh-lib']
    return [W/p for p in heads] + [Path(p) for p in
      (W/'hase-generic-rigidity-review-20261010/lean_path.txt').read_text().strip().split(':')] + [W/p for p in tails]
def main():
    before = {name: verify(V/name) for name in ['SOURCE_HASHES.json','RETAINED_OBJECTS.json']}
    fresh = V/'author-fresh'
    fresh.mkdir(exist_ok=True)
    env = dict(os.environ, LEAN_PATH=':'.join(map(str,[fresh]+retained_paths())))
    lean = W/'.toolchains/lean-4.19.0-linux/bin/lean'
    records = []
    for module in MODULES:
        cmd = [str(lean),'--trust=0','-o',str(fresh/f'{module}.olean'),str(ROOT/f'{module}.lean')]
        proc = subprocess.run(cmd,cwd=W,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        log = V/f'{module}.fresh.log'
        log.write_text(proc.stdout)
        print(proc.stdout,end='')
        if proc.returncode or any(x in proc.stdout for x in ['sorryAx','error:', 'warning:']):
            raise RuntimeError(f'{module} did not pass a clean trust-zero replay')
        records.append({'module':module,'command':cmd,'exit_code':proc.returncode,
          'source_sha256':digest(ROOT/f'{module}.lean'),'object_sha256':digest(fresh/f'{module}.olean'),
          'log_sha256':digest(log)})
    after = {name: verify(V/name) for name in before}
    receipt = {'status':'PASS','lean_version':subprocess.check_output([str(lean),'--version'],text=True).strip(),
      'lean_sha256':digest(lean),'trust':0,'baseline_rebuilt':False,'protected_inputs_mutated':False,
      'pinned_counts_before':before,'pinned_counts_after':after,'records':records}
    (V/'AUTHOR_REPLAY.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':'PASS','modules':len(records),'unchanged_pins':after}))
if __name__ == '__main__': main()
