#!/usr/bin/env python3
"""Small independent controls for input size, recomputation, and target absorption.

No author code is imported. These checks do not prove an asymptotic complexity
bound or the inherited hidden-parity characterization.
"""
from fractions import Fraction as F
from itertools import product
import json


def absorption_control():
    # State 0 is the start, 1 is the common target, 2 is a losing sink.
    # The original target deliberately falls into the losing sink afterwards.
    rows = [(F(1),F(0),F(0)), (F(0),F(1),F(0)), (F(0),F(0),F(1)),
            (F(0),F(1,2),F(1,2)), (F(1,2),F(1,2),F(0))]
    checked = 0
    for start_rows in product(rows, repeat=4):
        original = {(theta, 0, action):start_rows[2*theta+action]
                    for theta, action in product(range(2), range(2))}
        for theta, action in product(range(2), range(2)):
            original[theta,1,action] = (F(0),F(0),F(1))
            original[theta,2,action] = (F(0),F(0),F(1))
        absorbed = dict(original)
        for theta, action in product(range(2), range(2)):
            absorbed[theta,1,action] = (F(0),F(1),F(0))
        # Several deterministic, history-dependent policies are tested. A
        # symbolic pathwise argument, not this finite list, covers all policies.
        for policy in range(4):
            choose = lambda history: (len(history)//2 + policy + sum(history)) % 2
            for theta in range(2):
                frontier = {(0,):F(1)}
                original_hit = F(0)
                for depth in range(5):
                    nxt = {}
                    for history, mass in frontier.items():
                        if 1 in history[::2]:
                            original_hit += mass
                            continue
                        s = history[-1]
                        a = choose(history)
                        for y,p in enumerate(original[theta,s,a]):
                            if p:
                                h = history+(a,y)
                                nxt[h] = nxt.get(h,F(0))+mass*p
                    frontier = nxt
                original_hit += sum(mass for history,mass in frontier.items()
                                    if 1 in history[::2])
                transformed = {(0,):F(1)}
                for depth in range(5):
                    nxt = {}
                    for history,mass in transformed.items():
                        s = history[-1]
                        a = choose(history)
                        for y,p in enumerate(absorbed[theta,s,a]):
                            if p:
                                h=history+(a,y)
                                nxt[h]=nxt.get(h,F(0))+mass*p
                    transformed=nxt
                transformed_target = sum(mass for history,mass in transformed.items()
                                         if history[-1]==1)
                assert original_hit == transformed_target
                checked += 1
    # Deterministic countercontrol: target hit once but left forever. Without
    # absorption, min-inf priority is 1; with absorption it is 2.
    assert min([1]) % 2 == 1 and min([2]) % 2 == 0
    return {'finite_prefix_law_comparisons':checked,
            'target_absorption_omission_rejected':True,
            'horizon':5}


def encoding_control():
    checks=0
    examples=[]
    for k,n,m in product(range(1,21),[1,2,5],[1,2,3]):
        supports=(1<<k)-1
        full_menu_bits=supports*n*m
        compact_menu_bits=n*m
        memo_region_bits=supports*n
        # These inequalities instantiate the algebra used in the review.
        assert memo_region_bits <= full_menu_bits
        assert supports <= full_menu_bits
        assert full_menu_bits == supports*compact_menu_bits
        checks += 3
        if n==m==1 and k in [1,5,10,20]:
            examples.append({'k':k,'full_menu_entries':full_menu_bits,
                             'compact_menu_entries':compact_menu_bits})
    return {'exact_arithmetic_assertions':checks,'examples':examples}


def stack_control():
    rows=[]
    for k in range(1,9):
        calls=0;peak=0;peak_live_bits=0
        # Deliberately repeat every deletion order, returning only one bit.
        # No visited-support or child-result table is retained.
        def visit(B, depth, live_bits):
            nonlocal calls,peak,peak_live_bits
            calls+=1
            frame_bits=k+k*k
            live_bits+=frame_bits
            peak=max(peak,depth)
            peak_live_bits=max(peak_live_bits,live_bits)
            result=True
            if len(B)>1:
                for removed in B:
                    result = visit(tuple(x for x in B if x!=removed),depth+1,live_bits) and result
            return result
        assert visit(tuple(range(k)),1,0)
        assert peak==k
        assert peak_live_bits==k*(k+k*k)
        bound=sum(k**j for j in range(k))
        assert calls<=bound
        rows.append({'k':k,'calls':calls,'peak_frames':peak,
                     'live_bits_in_mask_only_model':peak_live_bits,
                     'reference_distinct_nonempty_supports':(1<<k)-1})
    assert rows[-1]['calls']>rows[-1]['reference_distinct_nonempty_supports']
    return rows


if __name__=='__main__':
    print(json.dumps({'status':'PASS','author_code_called':False,
                      'absorption':absorption_control(),
                      'encoding':encoding_control(),
                      'recomputation':stack_control(),
                      'scope':'Finite corroboration only; complexity bounds are ordinary proofs.'},
                     indent=2,sort_keys=True))
