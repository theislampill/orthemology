"""Strict bounded transport; failure is an operational refusal, not logical falsity."""
from __future__ import annotations
import json
from fractions import Fraction
from typing import Any
MAX_BYTES=524288
MAX_DEPTH=100
MAX_NODES=20000
MAX_INT_BITS=256
class Rejection(ValueError):pass

def bound_tree(value:Any,*,nodes:int=MAX_NODES,depth:int=MAX_DEPTH,work:list[int]|None=None,fractions:bool=False)->int:
    stack=[(value,0,False)];active=set();count=0
    while stack:
        x,d,exit_=stack.pop()
        if exit_:active.remove(id(x));continue
        count+=1
        if work is not None:work[0]-=1
        if count>nodes or d>depth or (work is not None and work[0]<0):raise Rejection('resource: structural/aggregate budget')
        if type(x) in (list,tuple,dict):
            if id(x) in active:raise Rejection('encoding: cyclic object')
            if len(x)>nodes:raise Rejection('resource: container length')
            active.add(id(x));stack.append((x,d,True))
            if type(x) is dict:
                for k,v in x.items():
                    if type(k) is not str:raise Rejection('encoding: nontext key')
                    stack.extend([(k,d+1,False),(v,d+1,False)])
            else:stack.extend((v,d+1,False) for v in x)
        elif type(x) is int:
            if x.bit_length()>MAX_INT_BITS:raise Rejection('resource: integer bits')
        elif type(x) is str:
            if len(x)>4096:raise Rejection('resource: string size')
            if any(0xD800<=ord(c)<=0xDFFF for c in x):raise Rejection('encoding: unpaired surrogate')
        elif type(x) in (bool,type(None)):pass
        elif fractions and type(x) is Fraction:
            if max(x.numerator.bit_length(),x.denominator.bit_length())>4096:raise Rejection('resource: rational bits')
        else:raise Rejection('encoding: unsupported object')
    return count

def load_json(raw:bytes)->Any:
    if type(raw) is not bytes:raise Rejection('encoding: bytes required')
    if len(raw)>MAX_BYTES:raise Rejection('resource: byte limit')
    try:s=raw.decode('utf-8','strict')
    except UnicodeError as ex:raise Rejection('encoding: UTF-8 required') from ex
    depth=0;quoted=False;escape=False
    for c in s:
        if quoted:
            if escape:escape=False
            elif c=='\\':escape=True
            elif c=='"':quoted=False
        elif c=='"':quoted=True
        elif c in '[{':
            depth+=1
            if depth>MAX_DEPTH:raise Rejection('resource: JSON depth')
        elif c in ']}':depth-=1
    def pairs(rows):
        d={}
        for k,v in rows:
            if k in d:raise Rejection('encoding: duplicate key '+k)
            d[k]=v
        return d
    def integer(s):
        if len(s.lstrip('-'))>78:raise Rejection('resource: integer digits')
        n=int(s)
        if n.bit_length()>MAX_INT_BITS:raise Rejection('resource: integer bits')
        return n
    def noninteger(s):raise Rejection('encoding: integral JSON numbers only')
    try:x=json.loads(s,object_pairs_hook=pairs,parse_int=integer,parse_float=noninteger,parse_constant=noninteger)
    except (ValueError,RecursionError) as ex:
        if isinstance(ex,Rejection):raise
        raise Rejection('encoding: malformed JSON') from ex
    bound_tree(x);return x

def dump_json(x:Any)->bytes:
    bound_tree(x)
    # Streaming, bounded assembly: no complete oversize string is allocated.
    # Each emitted string chunk is bounded by the input's 4096-character cap.
    chunks=[];size=0
    try:
        encoder=json.JSONEncoder(sort_keys=True,separators=(',',':'),ensure_ascii=True,allow_nan=False)
        for text in encoder.iterencode(x):
            chunk=text.encode('ascii');size+=len(chunk)
            if size>MAX_BYTES:raise Rejection('resource: output bytes')
            chunks.append(chunk)
    except (ValueError,TypeError,RecursionError) as ex:
        if isinstance(ex,Rejection):raise
        raise Rejection('encoding: invalid output') from ex
    return b''.join(chunks)
