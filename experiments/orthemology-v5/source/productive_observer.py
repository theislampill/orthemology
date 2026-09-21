"""Bounded implementation of productive binary-tape observation descriptions.

The ordinary undecidability theorem in PROOFS_V4.md concerns UNBOUNDED finite
program descriptions and infinite stream observations, not this 64-state/128-bit
API. Prefix termination does not decide the full-stream point defect. A finite
closed-control-state invariant is a sound sufficient positive certificate.
"""
import hashlib
from boundaries import Rejection,load_json,dump_json,bound_tree
MAX_STATES=64
MAX_PREFIX=128

def check(source):
    s=load_json(dump_json(source))
    if type(s) is not dict or set(s)!={'kind','transitions'} or s['kind']!='binary-tape-observer':raise Rejection('observer: exact finite source grammar')
    table=s['transitions']
    if type(table) is not list or not 1<=len(table)<=MAX_STATES:raise Rejection('observer: control-state bound')
    for row in table:
        if type(row) is not list or len(row)!=2:raise Rejection('observer: binary transition pair')
        for t in row:
            if type(t) is not list or len(t)!=3 or any(type(x) is not int for x in t):raise Rejection('observer: transition shape')
            state,write,move=t
            if not -1<=state<len(table) or write not in (0,1) or move not in (-1,1):raise Rejection('observer: transition range')
    return s

def prefix(source,bits):
    s=check(source);bound_tree(bits)
    if type(bits) not in (tuple,list) or len(bits)>MAX_PREFIX or any(type(x) is not int or x not in (0,1) for x in bits):raise Rejection('observer: bounded literal input bits')
    state=0;head=0;tape={};out=[];halt=None
    for n,bit in enumerate(bits,1):
        if state!=-1:
            state,write,move=s['transitions'][state][tape.get(head,0)]
            if write:tape[head]=1
            else:tape.pop(head,None)
            head+=move
            if state==-1:halt=n
        out.append(bit if state==-1 else 0)
    return {'output':out,'halt_step':halt,'steps':len(bits),
        'finite_prefix_defect':[0,1],
        'full_stream_defect':[1,1] if halt is not None else 'UNKNOWN',
        'law_assumption':'IID fair infinite input bits; full measurable stream events',
        'scope':'bounded productive prefix, not a general nonhalting decision'}

def certify_constant(source,invariant):
    s=check(source);bound_tree(invariant)
    if type(invariant) not in (tuple,list) or not 1<=len(invariant)<=len(s['transitions']) or any(type(x) is not int or not 0<=x<len(s['transitions']) for x in invariant) or len(set(invariant))!=len(invariant) or 0 not in invariant:raise Rejection('observer: finite initial-state invariant')
    inv=set(invariant)
    for state in inv:
        for dest,_,_ in s['transitions'][state]:
            if dest not in inv:raise Rejection('observer: invariant is not closed or permits halt')
    return {'status':'FINITE_INVARIANT_CHECKED','source_sha256':hashlib.sha256(dump_json(s)).hexdigest(),
        'invariant':sorted(inv),'full_stream_defect':[0,1],
        'reason':'all reachable control states remain in the supplied nonhalting closed set',
        'kernel_verified':False}
