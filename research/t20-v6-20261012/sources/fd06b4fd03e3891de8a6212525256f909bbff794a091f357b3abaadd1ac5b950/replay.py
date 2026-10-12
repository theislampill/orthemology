#!/usr/bin/env python3
"""Recompute exact diagnostics and tests without network or Lean dependencies.

Usage: python3 engineering/replay.py --output /absolute/path/to/new-output
The output must be new and outside this research tree.
"""
import argparse
from datetime import datetime, timezone
from fractions import Fraction as F
from itertools import product
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time

import diagnostics as d
from package_tools import verify_tree


def canonical_bytes(obj):
    return (json.dumps(obj,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()


def collect_results():
    tables={'or':[0,1,1,1],'and':[0,0,0,1],'projection_A':[0,1,0,1]}
    common_checked=0
    for ws in product(list(product((False,True),repeat=3)),repeat=3):
        if not d.common_requisite_check(ws)['implication_valid']:
            raise AssertionError('Common requisite counterexample')
        common_checked+=1
    graph_results=[]
    for mask in range(16):
        edges=[(a,b) for a,b in product(range(2),repeat=2) if mask&(1<<(2*a+b))]
        comp=d.compatibility_components(2,2,edges)
        actual=sum(all(f[a]==g[b] for a,b in edges)
                   for f in product(range(2),repeat=2) for g in product(range(2),repeat=2))
        if actual!=2**len(comp):raise AssertionError('Graph assignment count')
        graph_results.append({'edge_mask':mask,'edges':edges,'components':comp,'binary_assignments':actual})
    return {
      'schema':'t20-exact-diagnostic-results-v1',
      'scope':'Finite rational/model checks only. No metaphysical interpretation or actual cognitive warrant certified.',
      'D1_common_requisite':{'three_world_tables_exhausted':common_checked,'violations':0},
      'D2_rotating_witness':d.rotating_witness_model(),
      'D3_D4_boolean_explanation':d.audit_boolean_explanation_model(),
      'D4_source_padding_negative_control':d.audit_boolean_explanation_model(padded=True),
      'D4_restricted_reverse_part_gap':d.restricted_explanation_model(),
      'D5_bayes':{'e':'1/1000','d':'1/100','alpha_1':str(d.bayes_uncaused(F(1,1000),F(1,100),1)),
                  'alpha_1_over_1000':str(d.bayes_uncaused(F(1,1000),F(1,100),F(1,1000))),
                  'interval_example':[str(x) for x in d.posterior_interval(F(99,100),F(1,2),0,1)]},
      'D6_exchangeability':{'finite_anticorrelated_exchangeable':d.exchangeable(d.fixed_heads_law(2,1)),
                            'finite_anticorrelated_covariance':str(d.covariance(d.fixed_heads_law(2,1))),
                            'coherent_law_is_exchangeable':d.exchangeable({(0,0):F(1,8),(0,1):F(1,8),(1,0):F(3,8),(1,1):F(3,8)}),
                            'positive_mixture_covariance':str(d.covariance(d.bernoulli_mixture(2,[(F(1,2),F(1,4)),(F(1,2),F(3,4))]))),
                            'one_word_beta_probability_n2k1':str(d.uniform_beta_word(2,1))},
      'D7_compatibility_graphs':graph_results,
      'D8_knowledge_hierarchy':d.hierarchy_examples(),
      'D9_fact_attribute_transfer':d.semantic_transfer('fact_atomicity_to_attribute_identity'),
      'causal_supports':{**{name:d.minimal_supports(2,t) for name,t in tables.items()},
                        'or_with_background_L':d.minimal_supports(3,[bool((s&1 or s&2) and s&4) for s in range(8)])},
      'new_lean_run':False,
      'independent_external_review':False,
    }


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True,type=Path)
    args=parser.parse_args()
    root=Path(__file__).resolve().parent.parent
    out=args.output
    if not out.is_absolute():parser.error('--output must be an absolute path')
    if out.exists() or out.is_symlink():parser.error('--output must not already exist')
    resolved=out.resolve()
    if resolved==root or root in resolved.parents:parser.error('--output must be outside the research tree')
    if not out.parent.is_dir():parser.error('--output parent must already exist')
    before=verify_tree(root)
    out.mkdir()
    started=time.monotonic()
    results=canonical_bytes(collect_results())
    (out/'DIAGNOSTIC_RESULTS.json').write_bytes(results)
    expected=(root/'verification/DIAGNOSTIC_RESULTS.json').read_bytes()
    match=results==expected
    env=os.environ.copy();env['PYTHONDONTWRITEBYTECODE']='1'
    cmd=[sys.executable,'-B','-m','unittest','discover','-s','tests','-v']
    with (out/'TESTS.log').open('w') as f:
        run=subprocess.run(cmd,cwd=root/'engineering',env=env,stdout=f,stderr=subprocess.STDOUT,timeout=120,check=False)
    after=verify_tree(root)
    receipt={'schema':'t20-independent-replay-v1','utc':datetime.now(timezone.utc).isoformat(),
             'python':sys.version,'command':cmd,'test_exit_code':run.returncode,
             'canonical_results_match':match,'result_sha256':hashlib.sha256(results).hexdigest(),
             'tree_before':before,'tree_after':after,'tree_unchanged':before==after,
             'elapsed_seconds':round(time.monotonic()-started,3),
             'lean_run':False,'network_used':False,
             'scope':'Tests and exact finite/rational recomputation; no source authentication or metaphysical validation.'}
    receipt['passed']=run.returncode==0 and match and before==after
    (out/'REPLAY_RECEIPT.json').write_bytes(canonical_bytes(receipt))
    print(json.dumps(receipt,indent=2))
    if not receipt['passed']:raise SystemExit(1)

if __name__=='__main__':
    try:main()
    except (ValueError,OSError,AssertionError,subprocess.TimeoutExpired) as e:
        print('REPLAY FAILED: '+str(e),file=sys.stderr);raise SystemExit(1)
