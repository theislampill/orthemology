#!/usr/bin/env python3
"""Independent byte-binding, stack, and access-state fixture review.

Executable checks corroborate a supplied annotation; they do not parse source
language or authenticate sources. Actual source bytes have one fixed role map.
"""
import argparse,hashlib,importlib,json,sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from independent_models import direct_stack,partition_minimax,subset_cover
HERE=Path(__file__).resolve().parent
LANE=HERE.parents[1]/'research'/'occurrence-continuation'

def require(v,m):
 if not v:raise AssertionError(m)

def fail_expected(fn):
 try:fn()
 except ValueError:return
 raise AssertionError('expected rejected partial identity map')

def main():
 p=argparse.ArgumentParser();p.add_argument('--candidate',type=Path,default=LANE/'checker');p.add_argument('--output',type=Path,default=HERE/'INDEPENDENT_SOURCE_FIXTURE.json');args=p.parse_args()
 sys.path.insert(0,str(args.candidate.resolve()));c=importlib.import_module('context_effects');r=importlib.import_module('read_cover')
 fixture=args.candidate/'fixtures/source_roles.json';spec=json.loads(fixture.read_text())
 raw=LANE/'source-records/corpus-thomisticum-sth1002.html';rendered=LANE/'SOURCE_WITNESS_RENDERED.txt'
 require(hashlib.sha256(raw.read_bytes()).hexdigest()==spec['latin_body_sha256'],'Latin snapshot binding')
 require(hashlib.sha256(rendered.read_bytes()).hexdigest()==spec['paired_rendered_sha256'],'paired rendered record binding')
 origins={k:c.Origin(spec['latin_body_sha256'],v) for k,v in spec['scope_keys'].items()}
 def events(seq):return [(op,origins[v] if op in ('enter','exit') else v) for op,v in seq]
 first=events(spec['first_fragment']);second=events(spec['second_fragment'])
 expected=direct_stack(first+second,[origins['a']])
 joined=c.compose(c.compile_effect(first),c.compile_effect(second))
 require(c.apply_effect(joined,[origins['a']])==expected,'source annotated direct stack mismatch')
 suffix=c.compile_effect(second)
 require(suffix.depth==3 and suffix.emissions==(('return-output',c.Ref(2)),),'two-return selected reference')
 missing={int(i):origins[k] for i,k in spec['missing_boundary'].items()}
 fail_expected(lambda:c.resolve_demands(suffix,missing))
 complete={int(i):origins[k] for i,k in spec['acquired_boundary'].items()}
 require(c.resolve_demands(suffix,complete)==frozenset({origins['a']}),'source resolved demand')
 # Fork two fresh target occurrences from the SAME fixed original context.
 fork1=c.rename_outputs(suffix,'carrier1');fork2=c.rename_outputs(suffix,'carrier2')
 require({t for t,_ in fork1.emissions}.isdisjoint(t for t,_ in fork2.emissions),'fork output freshness')
 require(c.resolve_demands(fork1,complete)|c.resolve_demands(fork2,complete)==frozenset({origins['a']}),'fork originals duplicated')
 known={origins[k]:v for k,v in spec['proposed_original_role_values'].items()}
 require(r.role_decision(c.resolve_demands(suffix,complete),known) is True,'fixed original role verdict')
 require(spec['current_carrier_force']=='report' and spec['original_role_query_only'] is True,'source/current-carrier distinction not preserved')
 require(spec['actual_full_page_alternative'] is True,'actual whole-page alternative omitted')
 # Separate opaque-handle synthetic family, no alternate actual-source worlds.
 worlds=tuple(dict(zip('abc',bits))|{'d':1} for bits in product([0,1],repeat=3))
 verdicts=tuple(all(w[k] for k in 'abc') for w in worlds)
 actions=[('left',frozenset('ab'),F(1)),('right',frozenset('bc'),F(1))]
 cols=[tuple(tuple(w[k] for k in sorted(cov)) for w in worlds) for _,cov,_ in actions]
 def knowledge_cost(metadata,columns=cols,costs=[F(1),F(1)]):
  blocks={}
  for i,w in enumerate(worlds):
   v=metadata(w);blocks[v]=blocks.get(v,0)|(1<<i)
  return partition_minimax(verdicts,columns,costs,tuple(blocks.values()))
 costs={'retired_source_no_retention':knowledge_cost(lambda w:None)}
 costs['old_service']=knowledge_cost(lambda w:None,cols+[tuple(tuple(w[k] for k in 'abc') for w in worlds)],[F(1)]*3)
 for k in 'abcd':costs['fixed_carry_'+k]=knowledge_cost(lambda w,k=k:(k,w[k]))
 costs['valid_fixed_query_verdict']=knowledge_cost(lambda w:all(w[k] for k in 'abc'))
 costs['agreed_label_dependent_identity_code']=knowledge_cost(lambda w:'a' if all(w[k] for k in 'abc') else 'b')
 expected_costs={'old_service':1,'retired_source_no_retention':2,'fixed_carry_a':1,'fixed_carry_b':2,'fixed_carry_c':1,'fixed_carry_d':2,'valid_fixed_query_verdict':0,'agreed_label_dependent_identity_code':0}
 require(costs==expected_costs,('independent release costs',costs))
 require(subset_cover('abc',actions)[0]==2,'synthetic card cover baseline')
 for k in 'abc':
  negative_worlds=[i for i,w in enumerate(worlds) if not w[k]]
  mask=sum(1<<i for i in negative_worlds)
  require(partition_minimax(verdicts,cols,[F(1),F(1)],[mask])==0,'known false not immediate')
 result={'status':'PASS','scope':'byte-binding and supplied-annotation consistency; independently inspected language roles remain ordinary source review','fixture_sha256':hashlib.sha256(fixture.read_bytes()).hexdigest(),'latin_sha256':spec['latin_body_sha256'],'paired_rendered_sha256':spec['paired_rendered_sha256'],'source_control':{'suffix_depth':3,'selected_input_reference':2,'missing_map_rejected':True,'fork_fresh_outputs':2,'fork_distinct_originals':1,'source_current_carrier_relations_separate':True,'actual_full_page_alternative_independently_observed':'2026-10-03 web and cloud browser reads; see SOURCE_INSPECTION.json','actual_source_counterfactual_worlds':0},'independent_synthetic_access_costs':{k:int(v) for k,v in costs.items()},'known_false_extra_cost':0,'optimized':not __debug__}
 args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
