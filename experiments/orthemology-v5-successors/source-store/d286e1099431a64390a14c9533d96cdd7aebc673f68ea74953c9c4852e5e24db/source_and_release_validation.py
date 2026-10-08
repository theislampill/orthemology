"""Reproduce constructed source-binding and bounded-release controls.

All role maps and table observations are supplied model inputs. No natural
language parsing, real source authentication, or normative inference occurs.
"""
import json
from pathlib import Path
from fractions import Fraction as F
from itertools import product
from context_effects import Origin,MissingBinding,compile_effect,compose,resolve_demands,rename_outputs,apply_effect
from read_cover import Window,cover_dp,minimax_cost,star_locality,coverage_sufficiency,role_decision

def source_case():
    spec=json.loads(Path('fixtures/source_roles.json').read_text())
    os={k:Origin(spec['latin_body_sha256'],v) for k,v in spec['scope_keys'].items()}
    def parse(sequence):return [(op,os[x]) if op in ('enter','exit') else (op,x) for op,x in sequence]
    first=compile_effect(parse(spec['first_fragment']));second=compile_effect(parse(spec['second_fragment']))
    missing={int(i):os[k] for i,k in spec['missing_boundary'].items()}
    try:resolve_demands(second,missing)
    except MissingBinding:pass
    else:raise AssertionError('missing source boundary was manufactured')
    bound={int(i):os[k] for i,k in spec['acquired_boundary'].items()}
    assert resolve_demands(second,bound)=={os['a']}
    joined=compose(first,second)
    final,outs=apply_effect(joined,[os['a']])
    assert final==(os['a'],) and outs[-1]==('return-output',os['a'])
    copy1=rename_outputs(compile_effect([('emit','z')]),'carrier-1')
    copy2=rename_outputs(compile_effect([('emit','z')]),'carrier-2')
    emissions=apply_effect(compose(copy1,copy2),[os['a']])[1]
    assert len(emissions)==2 and len({o for _,o in emissions})==1
    known={os[k]:v for k,v in spec['proposed_original_role_values'].items()}
    assert role_decision({os['a']},known) is True
    assert spec['current_carrier_force']=='report' # no endorsement promotion
    assert spec['actual_full_page_alternative'] is True
    return {'status':'PASS','suffix_depth':second.depth,'selected_input_reference':2,
            'missing_identity_rejected':True,'identity_and_role_path_read_count':1,
            'path_read_phase':'separate from role-only cover optimum',
            'post_fork_carrier_occurrences':len(emissions),'original_dependencies':1,
            'actual_full_page_available':True,'proposition_preservation':'not certified',
            'scope':'Consistency of supplied source-linked extraction only'}

def release_case():
    a,b,c,d=[Origin('generated-role-family',s) for s in 'abcd']
    keys=[a,b,c];worlds=tuple(dict(zip(keys,bits))|{d:1} for bits in product((0,1),repeat=3))
    cards=[Window('left',frozenset([a,b]),F(1)),Window('right',frozenset([b,c]),F(1))]
    old=cards+[Window('source-ordered',frozenset(keys),F(1))]
    response=lambda x,w:tuple((k,x[k]) for k in sorted(w.coverage))
    target=lambda x:all(x[k] for k in keys)
    assert star_locality(worlds,keys,cards,response) and coverage_sufficiency(worlds,cards,response)
    # Each target comes from a post-return suffix; copying a does not add a root.
    outputs=[]
    for i,k in enumerate([c,a,b,a]):
        inner=Origin('generated-role-family',f'inner-{i}')
        e=compile_effect([('leave',),('emit',f't{i}')])
        outputs.extend(apply_effect(e,[inner,k,d])[1])
    assert {o for _,o in outputs}==set(keys) and len(outputs)==4
    costs={'old_service':minimax_cost(worlds,old,target,response),
           'retired_source_no_retention':minimax_cost(worlds,cards,target,response)}
    for key in [a,b,c,d]:
        # Fixed role-independent retention origin. Its value is observed.
        costs['fixed_carry_'+key.locus]=minimax_cost(worlds,cards,target,response,
            metadata=lambda x,key=key:(key,x[key]))
    costs['valid_fixed_query_verdict']=minimax_cost(worlds,cards,target,response,metadata=target)
    signal=lambda x:a if target(x) else b
    costs['agreed_label_dependent_identity_code']=minimax_cost(worlds,cards,target,response,metadata=signal)
    expected={'old_service':1,'retired_source_no_retention':2,'fixed_carry_a':1,'fixed_carry_b':2,'fixed_carry_c':1,'fixed_carry_d':2,'valid_fixed_query_verdict':0,'agreed_label_dependent_identity_code':0}
    assert costs=={k:F(v) for k,v in expected.items()},costs
    assert not star_locality(worlds,keys,cards,response,metadata=signal)
    return {'status':'PASS','selected_carrier_order':['c','a_1','b','a_2'],
            'distinct_originals':['a','b','c'],'future_request_budget':1,
            'exact_worst_case_costs':{k:int(v) for k,v in costs.items()},
            'known_negative_carry_extra_reads':0,
            'retention_policies':'fixed in advance except explicitly identified verdict-code alternative',
            'scope':'Synthetic operational calculation; no normative premise is proved'}

if __name__=='__main__':
    result={'source_fixture':source_case(),'release_fixture':release_case()}
    Path('logs/source_release_results.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
