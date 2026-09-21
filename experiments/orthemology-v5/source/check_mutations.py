#!/usr/bin/env python3
"""Run real regressions on isolated copies. Never alter the preserved input."""
from __future__ import annotations
import json, shutil, subprocess, sys, tempfile, re, os, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent

MUTATIONS=[
 ('remove_freshness','extensions.py',
  'if not marker_free(program):','if False:',
  'test_extensions.ExtensionTests.test_marker_capture_rejected'),
 ('wrong_probability_mass','extensions.py',
  '_add(out,t,(1-q)*p)','_add(out,t,q*p)',
  'test_extensions.ExtensionTests.test_probabilistic_application'),
 ('retain_type_instantiation_at_runtime','extensions.py',
  'return t,out','return (\'type_application\',t,b),out',
  'test_extensions.ExtensionTests.test_probabilistic_self_instantiation_is_erased'),
 ('accept_mismatched_mixture_types','extensions.py',
  "if a!=b: raise r.Rejection('mixture branches have different types')",
  "if False: raise r.Rejection('mixture branches have different types')",
  'test_extensions.ExtensionTests.test_probability_bad_typing'),
 ('wrong_irrational_threshold','extensions.py',
  'if upper*upper+2*upper*d-d*d < 0:',
  'if upper*upper+2*upper*d-d*d > 0:',
  'test_reflective_sampler.IrrationalReflectiveSampler.test_all_prefixes_through_twelve_bits'),
 ('unknown_probability_fields','extensions.py',
  "if set(n) != {'op',*keys}:","if False:",
  'test_extensions.ExtensionTests.test_probability_no_unknown_fields'),
]

def run(log_dir: Path | None = None)->dict:
    log_dir = log_dir or ROOT / "verification-run" / "mutations"
    log_dir.mkdir(parents=True, exist_ok=True)
    rows=[]
    for name,file,old,new,target in MUTATIONS:
        text=(ROOT/file).read_text()
        if text.count(old)!=1: raise RuntimeError(f'{name}: expected one exact mutation seam')
        with tempfile.TemporaryDirectory(prefix='orthemology_mutation_') as td:
            p=Path(td)
            for f in ('extensions.py','reference.py','boundaries.py'):
                shutil.copy2(ROOT/f,p/f)
            for f in (ROOT/'tests').glob('test_*.py'): shutil.copy2(f,p/f.name)
            command=[sys.executable,'-B','-m','unittest',target,'-v']
            env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
            normal=subprocess.run(command,cwd=p,env=env,text=True,capture_output=True,timeout=60)
            positive_ok=normal.returncode==0 and bool(re.search(r'Ran 1 test\b',normal.stderr))
            (log_dir/f'POSITIVE_{name}.txt').write_text(normal.stdout+normal.stderr)
            (p/file).write_text(text.replace(old,new,1))
            result=subprocess.run(command,cwd=p,env=env,text=True,capture_output=True,timeout=60)
            # Only an actual named assertion failure counts, never import/setup
            # errors or unrelated guards. Both sides and exact patch are retained.
            ran=bool(re.search(r'Ran 1 test\b',result.stderr))
            killed=(positive_ok and ran and result.returncode!=0 and
                    'AssertionError' in result.stderr and 'FAILED (failures=' in result.stderr and
                    'ModuleNotFoundError' not in result.stderr and 'Failed to import' not in result.stderr)
            log=log_dir/f'MUTATION_{name}.txt'
            log.write_text(result.stdout+result.stderr)
            row={'name':name,'test':target,'exit_code':result.returncode,
                 'positive_exit_code':normal.returncode,'positive_ok':positive_ok,
                 'one_named_test_executed':ran,'detected':killed,'log':log.name,
                 'source_sha256':hashlib.sha256(text.encode()).hexdigest(),
                 'patch':{'before':old,'after':new}}
            (log_dir/f'RECORD_{name}.json').write_text(json.dumps(row,indent=2)+'\n')
            rows.append(row)
    if not all(x['detected'] for x in rows): raise RuntimeError(rows)
    return {'status':'PASS','mutants':len(rows),'detected':sum(x['detected'] for x in rows),'results':rows}

if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--output-dir',type=Path)
    args=ap.parse_args();print(json.dumps(run(args.output_dir),indent=2))
