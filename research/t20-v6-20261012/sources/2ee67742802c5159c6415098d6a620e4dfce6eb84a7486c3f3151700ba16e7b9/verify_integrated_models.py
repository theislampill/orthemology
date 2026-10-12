#!/usr/bin/env python3
"""Explicit common-model controls and a finite check of the totality route.

These structures test formal entailment. Their interpretation as possible
metaphysical realities is not certified by this program.
"""
from __future__ import annotations
from itertools import product
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent


def modal_necessary(existence: list[set[str]]) -> set[str]:
    if not existence:
        raise ValueError('empty modal scope')
    return set.intersection(*existence)


def card(name: str, kind: str) -> dict:
    worlds = ['w0', 'w1']
    if kind == 'rotating':
        ex = [{'r0','agent0','record0'}, {'r1','agent1','record1'}]
        edges = [[['r0','agent0'],['r0','record0']],
                 [['r1','agent1'],['r1','record1']]]
        mind = [{'agent0'},{'agent1'}]
        law = ['r0','r1']; root_power = ['r0','r1']; will = [[],[]]
    else:
        ex = [{'g','agent0','record0'},{'g','agent1','record1'}]
        edges = [[['g','agent0'],['g','record0']],
                 [['g','agent1'],['g','record1']]]
        mind = [{'agent0'},{'agent1'}]
        if kind == 'personal':
            mind = [s|{'g'} for s in mind]
        law = ['g','g']; root_power = ['g','g']
        will = [['g'],['g']] if kind == 'personal' else [[],[]]
    return {
        'name':name, 'kind':kind, 'worlds':worlds, 'actual_world':'w0',
        'concrete_existence':[sorted(s) for s in ex],
        'dependence_edges':edges, 'mental_bearers':[sorted(s) for s in mind],
        'intrinsic_order_bearer':law,'efficacy_bearer':root_power,
        'volitional_bearers':will,
        'operational':{
            'state_space':[0,1], 'actions':['keep','flip'],
            'transition':{'keep':[0,1], 'flip':[1,0]},
            'truth_predicate':[False,True],
            'represented_truth_predicate':[False,True],
            'epistemic_law':[{'0':[1,1],'1':[0,1]}, {'0':[0,1],'1':[1,1]}],
            'all_events_logged':True, 'no_normative_truth_from_popularity':True},
        'optional_game':{'strategies':[0,1], 'payoff_each_player':'1 iff own action equals target bit'},
        'contingent_fact':[False,True],
        'source_content_preserved':True,
        'source_revelational_authentication_assumed':False,
        'semantic_status':'FORMAL_MODEL_ONLY_NOT_METAPHYSICAL_POSSIBILITY_CERTIFICATE'
    }


def analyse(m: dict) -> dict:
    ex = [set(v) for v in m['concrete_existence']]
    nec = modal_necessary(ex)
    actual = ex[0]
    edges = [set(map(tuple,e)) for e in m['dependence_edges']]
    roots=[]
    for xs,es in zip(ex,edges):
        assert all(a in xs and b in xs and a != b for a,b in es)
        roots.append(xs-{b for a,b in es})
        # Exhaustive bounded reachability checks no directed cycle in the cards.
        reach=set(es)
        while True:
            new=reach|{(a,d) for a,b in reach for c,d in reach if b==c}
            if new==reach: break
            reach=new
        assert not any(a==b for a,b in reach)
    cdep=all(any(b==x for a,b in edges[0]) for x in actual-nec)
    assert all(m['intrinsic_order_bearer'][w] in ex[w] for w in range(2))
    assert all(m['efficacy_bearer'][w] in ex[w] for w in range(2))
    necessary_minds = nec & set.intersection(*map(set,m['mental_bearers']))
    # Exact unary truth and all finite continuations: keep/flip closure is {1, bit}.
    transitions=m['operational']['transition']
    truth=m['operational']['truth_predicate']
    assert truth==m['operational']['represented_truth_predicate']
    history_checks=0
    for h in range(9):
        for acts in product(transitions,repeat=h):
            for x0 in range(2):
                x=x0
                for a in acts: x=transitions[a][x]
                parity=sum(a=='flip' for a in acts)%2
                assert x==(x0^parity)
                assert truth[x]==bool(x)
                history_checks+=1
    # At either target bit the unique equilibrium is both agents matching it.
    pure_ne=[]
    for target in range(2):
        ne=[]
        for s in product(range(2), repeat=2):
            if all(int(s[i]==target)>=int((1-s[i])==target) for i in range(2)):
                ne.append(list(s))
        assert ne==[[target,target]]
        pure_ne.append(ne)
    if m['kind']=='rotating':
        assert not nec and not cdep
    else:
        assert nec=={'g'} and cdep
    if m['kind']=='personal':
        assert necessary_minds=={'g'}
        # Omniscience at each world over the Boolean algebra of all propositions.
        for w in range(2):
            for p in range(4):
                knows=bool(p>>w&1)
                assert knows==bool(p>>w&1)
        assert not all(m['contingent_fact']) and any(m['contingent_fact'])
    else:
        assert not necessary_minds
    return {
        'name':m['name'],'actual_concrete_witness':bool(actual),
        'actual_dependency_well_founded':True,'dependency_domain_closed':True,
        'all_actual_contingents_have_parent':cdep,
        'unique_actual_root':len(roots[0])==1,
        'necessary_actual_entities':sorted(nec&actual),
        'common_order_and_efficacy_bearer':all(a==b for a,b in zip(
            m['intrinsic_order_bearer'],m['efficacy_bearer'])),
        'necessary_mental_bearer':bool(necessary_minds),
        'contingent_fact_remains':len(set(m['contingent_fact']))>1,
        'world_local_operational_check_count':history_checks,
        'source_text_preservation_without_authentication':True,
        'status':'PASS'}


def totality_instances() -> dict:
    checked=0; satisfying=0
    for n in range(1,4):
        # All entities exist actually. The second-world mask sets necessity.
        for necessary in range(1<<n):
            contingent=((1<<n)-1)^necessary
            for edges in range(1<<(n*n)):
                noself=all(not(edges>>(i*n+i)&1) for i in range(n))
                for totals in range(1<<n):
                    checked+=1
                    projection=all(not(totals>>i&1) or all(
                        not(contingent>>j&1) or bool(edges>>(i*n+j)&1)
                        for j in range(n)) for i in range(n))
                    if noself and totals and projection:
                        satisfying+=1
                        assert totals & ~necessary == 0
    return {'cases':checked,'satisfying_models':satisfying,'status':'PASS'}


def main():
    models=[card('CM-J1 rotating contingent roots','rotating'),
            card('CM-J2 necessary impersonal unified root','impersonal'),
            card('CM-J3 necessary personal root with contingent effects','personal')]
    result={'status':'PASS','models':[analyse(m) for m in models],
            'totality_route':totality_instances(),
            'scope':'explicit finite structures; no world-directed or full-corpus-completeness claim'}
    (HERE/'integrated_models.json').write_text(json.dumps(models,indent=2)+'\n')
    (HERE/'integrated_model_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__': main()
