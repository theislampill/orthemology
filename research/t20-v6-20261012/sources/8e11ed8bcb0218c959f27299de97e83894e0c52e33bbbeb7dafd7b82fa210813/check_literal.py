"""Bounded exact trace audit of the original literal compiler. No source writes."""
import sys, json, hashlib, importlib.util
from pathlib import Path
from fractions import Fraction as Q
from itertools import product
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'user-checkpoints/extracted/P02/code/prcodec.py'
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('literal_prcodec',SRC)
m=importlib.util.module_from_spec(spec);sys.modules[spec.name]=m;spec.loader.exec_module(m)
C,V,E,Set,Seq,Loop,If,Program=(getattr(m,s) for s in ('C','V','E','Set','Seq','Loop','If','Program'))
BEFORE=hashlib.sha256(SRC.read_bytes()).hexdigest()
COUNTS=Counter(); MODES=Counter()
def require(condition, context):
    if not condition: raise RuntimeError(context)
if "--false-check" in sys.argv:
    require(False, "deliberate false-check control")
BASES={
'zero':m.pr_zero(2),
'index_output':Program(2,0,Seq()),
'word_output':Program(2,1,Seq()),
'first_tail_bit':Program(2,2,Set(2,E('div',V(1),E('pow2',V(0))))),
'sentinel_and_length':Program(2,9,Set(9,E('add',V(0),E('div',V(1),E('pow2',E('add',V(0),C(1))))))),
'scratch_and_arguments':Program(2,3,Seq(Set(3,E('add',V(3),V(0))),Set(0,E('mod',V(1),C(5))),Set(1,E('add',V(3),V(0))),Set(3,E('add',V(1),V(11))))),
'loop_snapshot_alias':Program(2,4,Seq(Loop(0,V(0),Seq(Set(1,E('add',V(1),C(1))),Set(4,E('add',V(4),V(1))))))),
'unset_high_output':Program(2,103,Set(99,E('add',V(99),C(1)))),
}

def expected(base,bits,a,b):
    """Independent rational-cell scan, then original base on freshly encoded suffix.
    Returns output, full set-event trace, and semantic mode. Registers are bound
    to the inspected literal Builder allocation, not a substitute compiler.
    """
    q=Q(a,b); v=0;stop=0;branch=0
    events=[(4,0),(5,0),(6,0)]
    for j,bit in enumerate(bits,1):
        v=v*2+bit; events += [(8,2**j),(7,v)]
        if Q(v+1,2**j)<=q:stop=j;branch=0
        elif q<=Q(v,2**j):stop=j;branch=1
        if stop:
            events += [(4,1),(5,branch),(6,stop)];break
    out=bits[-1];events += [(2,out)]
    mode='unresolved' if not stop else ('below' if not branch else ('at_above_stop' if stop==len(bits) else 'base'))
    if mode=='base':
        tail=bits[stop:];n=len(tail)-1;w=m.word_code(tail)
        events += [(9,len(tail)),(10,w)]
        regs=sorted(m.registers(base));mapping={r:12+i for i,r in enumerate(regs)}
        events += [(mapping[r],0) for r in regs]
        events += [(mapping[0],n),(mapping[1],w)]
        value,_,be=m.run(base,(n,w),trace=True)
        events += [(mapping[r],v) for r,v in be]
        events += [(11,value),(2,value%2)];out=value%2
    return out,events,mode

def check(base,bits,a,b,kind,p=None):
    p=p or m.compile_shift(base,a,b)
    actual,_,events=m.run(p,(len(bits)-1,m.word_code(bits)),trace=True)
    out,wanted,mode=expected(base,bits,a,b)
    require((actual,events)==(out,wanted),(kind,bits,a,b,actual,out,events,wanted))
    COUNTS[kind]+=1;MODES[mode]+=1
    return actual

for name,base in BASES.items():
    for b in range(1,9):
        for a in range(b+1):
            p=m.decode(m.encode(m.compile_shift(base,a,b)))
            for width in range(1,8):
                for bits in product((0,1),repeat=width):check(base,bits,a,b,'exhaustive',p)
# Exact equivalence of unreduced and reduced ratios: compare literal output and
# entire trace (constants differ, but all actual register writes should agree).
for a,b in [(0,1),(1,1),(1,2),(1,3),(2,3),(3,7),(7,8)]:
    base=BASES['scratch_and_arguments'];p=m.compile_shift(base,a,b)
    for scale in [2,7,2**80+1]:
        ps=m.compile_shift(base,a*scale,b*scale)
        for bits in product((0,1),repeat=8):
            args=(7,m.word_code(bits))
            x=m.run(p,args,trace=True);y=m.run(ps,args,trace=True)
            require((x[0],x[2])==(y[0],y[2]),('ratio equivalence',a,b,scale,bits));COUNTS['unreduced_equivalence']+=1
# Concolic boundary generation: rational binary digits, and neighbours on both
# sides of every dyadic cut; verify every finite observation independently.
for a,b in [(1,3),(2,3),(1,5),(3,7),(127,257)]:
    bits=[];rem=a; p=m.compile_shift(BASES['zero'],a,b)
    for depth in range(1,129):
        rem*=2;digit,rem=divmod(rem,b);bits.append(digit)
        check(BASES['zero'],tuple(bits),a,b,'nondyadic_boundary',p)
        require(expected(BASES['zero'],tuple(bits),a,b)[2]=='unresolved',('non-dyadic boundary',a,b,depth))
        # branch away at this depth, then force actual tail delegation/copy.
        for suffix in [(0,1),(1,0)]:
            away=tuple(bits[:-1]+[1-digit])+suffix
            check(BASES['sentinel_and_length'],away,a,b,'boundary_neighbour')
for depth in range(1,33):
    for a in sorted({1,2**depth//2,2**depth-1}):
        b=2**depth
        for v in [a-1,a]:
            prefix=tuple((v>>j)&1 for j in range(depth-1,-1,-1))
            for suffix in [(),(0,),(1,),(0,1,0)]:
                check(BASES['scratch_and_arguments'],prefix+suffix,a,b,'dyadic_boundary')
# Negative controls on copied AST only: each guard must detect a relevant bug.
base=BASES['first_tail_bit'];p=m.compile_shift(base,1,2)
def transform(t,rule):
    if not isinstance(t,tuple):return t
    z=tuple(transform(v,rule) for v in t)
    return rule(z)
controls={
'omit_explicit_resets':lambda t: Seq() if t[:1]==('set',) and t[1]>=12 and t[2]==C(0) else t,
'early_base':lambda t: ('le',V(6),E('add',V(0),C(1))) if t==('le',V(6),V(0)) else t,
'wrong_tail_index':lambda t: V(9) if t==E('sub',V(9),C(1)) else t,
'omit_tail_sentinel':lambda t: Set(10,E('mod',V(1),E('pow2',V(9)))) if t[:2]==('set',10) else t,
'wrong_equality_boundary':lambda t: E('le',E('add',t[1],C(1)),t[2]) if t[0]=='le' and t[1][:1]==('mul',) else t,
}
negative={}
for name,rule in controls.items():
    mutant=Program(p.arity,p.output,transform(p.body,rule));witness=None
    for width in range(1,6):
        for bits in product((0,1),repeat=width):
            out,ev,_=expected(base,bits,1,2)
            val,_,actual=m.run(mutant,(width-1,m.word_code(bits)),trace=True)
            if (val,actual)!=(out,ev):witness={'bits':bits,'actual':val,'expected':out,'output_differs':val!=out};break
        if witness:break
    require(witness,name)
    negative[name]=witness
require(hashlib.sha256(SRC.read_bytes()).hexdigest()==BEFORE,'original source changed')
result={'status':'PASS','source_sha256':BEFORE,'counts':dict(COUNTS),'modes':dict(MODES),'negative_controls':negative,'base_names':list(BASES),'original_unchanged':True,'scope':'Bounded exact trace/finite-output evidence, not universal Python/compiler or infinite-law verification.'}
(Path(__file__).parent/'RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
