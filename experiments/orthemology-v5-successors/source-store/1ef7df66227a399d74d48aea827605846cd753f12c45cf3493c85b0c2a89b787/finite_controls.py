#!/usr/bin/env python3
"""Independent finite arithmetic controls; no opaque selector evaluation."""
import hashlib, json
from pathlib import Path
from itertools import product
ROOT=Path(__file__).resolve().parent
supports=[frozenset(i for i in range(2) if (mask>>i)&1) for mask in range(4)]
pairsets=[frozenset((state,action) for state,action in product(range(2),repeat=2) if (mask>>(2*state+action))&1) for mask in range(16)]
supportcode=lambda s:sum(2**x for x in s)
targetcode=lambda s:sum(2**(2*x+y) for x,y in s)
retained=[0]+[targetcode(s)+1 for s in pairsets]
assert retained==list(range(17))
assert len(set(map(supportcode,supports)))==4
assert len(set(map(targetcode,pairsets)))==16
indices=[4*supportcode(s)+2*a+b for s,a,b in product(supports,range(2),range(2))]
assert sorted(indices)==list(range(16))
assert list(map(supportcode,supports))==list(range(4))

def cycle_expected(o,s,f,r):
    if not s:return f
    if len(s)==1:return next(iter(s))
    return o if r==0 else 1-o

def target_expected(s,c):
    if not s:return 0
    a=next(iter(s)) if len(s)==1 else c
    return targetcode(frozenset((state,a) for state in range(2)))+1

def stage_expected(s):
    if not s:return 0
    if len(s)==2:return 15
    a=next(iter(s));return targetcode(frozenset((state,a) for state in range(2)))

records=[]
for o in range(2):
    cyc=sum(cycle_expected(o,s,f,r)*2**(4*supportcode(s)+2*f+r) for s,f,r in product(supports,range(2),range(2)))
    tar=sum(target_expected(s,c)*32**(4*supportcode(s)+2*c+st) for s,c,st in product(supports,range(2),range(2)))
    sta=sum(stage_expected(s)*16**supportcode(s) for s in supports)
    assert (cyc,tar,sta)==((44812,24332)[o],428783445879334172098560,64080)
    records.append((cyc,tar,sta))

digits=lambda value,base,width:tuple(value//base**i%base for i in range(width))
field_shapes=[(2,16),(32,16),(16,4)]
invalid_payload_cases=0
bit_mutation_cases=0
for o,record in enumerate(records):
    for value,(base,width) in zip(record,field_shapes):
        expected=digits(value,base,width)
        for k in (0,1,2,7,31,2**129+51):
            lifted=value+k*base**width
            assert digits(lifted,base,width)==expected
            assert lifted%base**width==value
        for bit in range({2:16,32:80,16:16}[base]):
            assert digits(value^(1<<bit),base,width)!=expected
            bit_mutation_cases+=1
    target=record[1]
    for i in range(16):
        old=target//32**i%32
        for bad in range(17,32):
            modified=target+(bad-old)*32**i
            assert modified//32**i%32==bad
            assert bad not in retained
            assert digits(modified,32,16)!=digits(target,32,16)
            invalid_payload_cases+=1
    # support4 is not a valid two-bit support mask. Its cycle call reads bit16.
    assert record[0]//2**(4*4)%2==0
    assert (record[0]+2**16)//2**(4*4)%2==1

# Exhaustive entire finite cycle and stage spaces, separate from opaque choice.
cycle_solutions=[];stage_solutions=[]
for n in range(2**16):
    if digits(n,2,16) in [digits(r[0],2,16) for r in records]:cycle_solutions.append(n)
    if digits(n,16,4)==digits(64080,16,4):stage_solutions.append(n)
assert cycle_solutions==[24332,44812]
assert stage_solutions==[64080]
result={
 'status':'PASS_FINITE_ARITHMETIC_CONTROLS',
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
 'cycle_target_indices':indices,'stage_indices':list(map(supportcode,supports)),
 'support_injective_on_carrier':True,'target_injective_on_carrier':True,
 'retained_codes':retained,'none_code':0,'some_empty_code':1,
 'literal_records':records,'used_bit_mutation_cases':bit_mutation_cases,
 'invalid_payload_cases':invalid_payload_cases,
 'bounded_cycle_full_space_solutions':cycle_solutions,
 'bounded_stage_full_space_solutions':stage_solutions,
 'malformed_support4_observes_high_cycle_bit':True,
 'opaque_initialCandidate_evaluated':False,
 'scope':'Finite arithmetic corroboration only; not a substitute for Lean theorems or Python-to-Lean refinement.'
}
(ROOT/'evidence/FINITE_CONTROLS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
