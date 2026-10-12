#!/usr/bin/env python3
"""Packaging smoke replay of exact included Python science in a disposable copy.

This is a new packaging check, not a substitute for the historical independent
reviews, a Lean replay, or proof of source/application premises.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output', help='Optional new JSON receipt path; must not already exist')
    args = p.parse_args()
    here = Path(__file__).resolve().parents[1]
    original = {str(x.relative_to(here)): hashlib.sha256(x.read_bytes()).hexdigest()
                for x in (here/'tranche20').rglob('*') if x.is_file()}
    records = []
    with tempfile.TemporaryDirectory(prefix='t20-python-replay-') as tmp:
        tmp = Path(tmp)
        shutil.copytree(here/'tranche20', tmp/'tranche20')
        res = tmp/'tranche20/research-resumption'
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        def run(rel, script, parse=False):
            cwd = tmp/rel
            start = time.monotonic()
            proc = subprocess.run([sys.executable, '-B', script], cwd=cwd,
                                  env=env, text=True, capture_output=True)
            record = dict(cwd=rel, script=script, exit_code=proc.returncode,
                          elapsed_seconds=time.monotonic()-start,
                          stdout=proc.stdout, stderr=proc.stderr)
            records.append(record)
            if proc.returncode:
                raise RuntimeError(json.dumps(record, indent=2))
            return json.loads(proc.stdout) if parse else None
        coop='tranche20/research-resumption/cooperation'
        run(coop, 'src/test_search.py')
        run(coop, 'src/search.py')
        expected=json.loads((here/coop/'results/SEARCH_RESULT.json').read_text())
        actual=json.loads((tmp/coop/'results/SEARCH_RESULT.json').read_text())
        expected.pop('run_utc'); actual.pop('run_utc')
        assert actual==expected, 'cooperation semantic result mismatch'
        run('tranche20/research-resumption/cooperation-independent-review', 'src/independent_checks.py')
        c='tranche20/research-resumption/testimony-continuation'
        run(c,'test_models.py')
        for script, result in [('occurrence_model.py','OCCURRENCE_RESULTS.json'),
                               ('continuation_model.py','CONTINUATION_RESULTS.json')]:
            actual=run(c,script,True)
            expected=json.loads((here/c/'validation'/result).read_text())
            assert actual==expected, result
        rev='tranche20/research-resumption/continuation-independent-review'
        for script in ['independent_checks.py','identity_ownership_checks.py',
                       'mutation_checks.py','veracity_scope_checks.py']:
            run(rev,script)
        audit='tranche20/research-closure-audit/continuation/replay'
        for script in ['test_grounded_support.py','independent_finite_checks.py','search_cut_order.py']:
            run(audit,script)
    after={str(x.relative_to(here)):hashlib.sha256(x.read_bytes()).hexdigest()
           for x in (here/'tranche20').rglob('*') if x.is_file()}
    assert after==original, 'sealed science changed'
    result=dict(status='PASS', scope='Exact included Python source replay in disposable extraction copy; no Lean replay or native integration rebuild',
                commands=len(records), source_tree_unchanged=True,
                semantic_result_comparisons=['cooperation, ignoring run_utc only','occurrence, exact','continuation, exact'],
                receipts=records)
    if args.output:
        with open(args.output,'x') as f: json.dump(result,f,indent=2); f.write('\n')
    print(json.dumps({k:v for k,v in result.items() if k!='receipts'},indent=2))


if __name__=='__main__': main()
