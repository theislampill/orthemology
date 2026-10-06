"""P02-L1: concrete, syntactically total LOOP observer codec and reductions.

Research implementation, not canonical adoption or a Lean verification.
Invalid *syntax* denotes zero. Resource exhaustion NEVER denotes zero.
For each fixed well-formed program evaluation is primitive recursive; the
universal evaluator is total computable, not uniformly primitive recursive.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterable, Sequence

Expr = tuple
Stmt = tuple
MAGIC = b'P02L\x01'
EXPR = {'c':1,'v':2,'add':3,'sub':4,'mul':5,'div':6,'mod':7,'le':8,'eq':9,'pow2':10}
STMT = {'set':16,'seq':17,'loop':18,'if':19}
INV_E = {v:k for k,v in EXPR.items()}

class InvalidCode(ValueError): pass
class ResourceLimit(RuntimeError): pass

def nat(x: int) -> int:
    if type(x) is not int or x < 0: raise ValueError('Natural integer required; booleans refused')
    return x

def C(x:int)->Expr:return ('c',nat(x))
def V(x:int)->Expr:return ('v',nat(x))
def E(op:str,*xs:Expr)->Expr:return (op,*xs)
def Set(r:int,e:Expr)->Stmt:return ('set',nat(r),e)
def Seq(*ss:Stmt)->Stmt:return ('seq',*ss)
def Loop(r:int,bound:Expr,body:Stmt)->Stmt:return ('loop',nat(r),bound,body)
def If(c:Expr,y:Stmt,n:Stmt= ('seq',))->Stmt:return ('if',c,y,n)

def _uv(n:int)->bytes:
    nat(n);out=bytearray()
    while n>=128:out.append((n%128)|128);n//=128
    out.append(n);return bytes(out)

@dataclass(frozen=True)
class Program:
    arity:int
    output:int
    body:Stmt

    def __post_init__(self):
        nat(self.arity);nat(self.output)

# The recursive serializer/parser traverses finite trees. The mathematical
# codec uses the equivalent bounded-stack traversal described in the proof.
def _enc_e(e:Expr)->bytes:
    if not isinstance(e,tuple) or not e or e[0] not in EXPR:raise InvalidCode('Expression tag')
    k=e[0];arity=1 if k in ('c','v','pow2') else 2
    if len(e)!=arity+1:raise InvalidCode('Expression arity')
    if k in ('c','v'):return bytes([EXPR[k]])+_uv(e[1])
    return bytes([EXPR[k]])+b''.join(_enc_e(x) for x in e[1:])

def _enc_s(s:Stmt)->bytes:
    if not isinstance(s,tuple) or not s or s[0] not in STMT:raise InvalidCode('Statement tag')
    k=s[0]
    if k=='set' and len(s)==3:return b'\x10'+_uv(s[1])+_enc_e(s[2])
    if k=='seq':return b'\x11'+_uv(len(s)-1)+b''.join(_enc_s(t) for t in s[1:])
    if k=='loop' and len(s)==4:return b'\x12'+_uv(s[1])+_enc_e(s[2])+_enc_s(s[3])
    if k=='if' and len(s)==4:return b'\x13'+_enc_e(s[1])+_enc_s(s[2])+_enc_s(s[3])
    raise InvalidCode('Statement arity')

def encode_bytes(p:Program)->bytes:
    try:return MAGIC+_uv(p.arity)+_uv(p.output)+_enc_s(p.body)
    except RecursionError as e:raise ResourceLimit('Host serializer stack exhausted') from e

def encode(p:Program)->int:
    return int.from_bytes(b'\x01'+encode_bytes(p),'big')

class Reader:
    def __init__(self,b:bytes):self.b=b;self.i=0
    def byte(self)->int:
        if self.i>=len(self.b):raise InvalidCode('Truncated code')
        n=self.b[self.i];self.i+=1;return n
    def uv(self)->int:
        start=self.i;n=0;shift=0
        while True:
            b=self.byte();n|=(b&127)<<shift
            if b<128:
                if self.b[start:self.i]!=_uv(n):raise InvalidCode('Noncanonical varint')
                return n
            shift+=7
    def expr(self)->Expr:
        t=self.byte()
        if t not in INV_E:raise InvalidCode('Unknown expression')
        k=INV_E[t]
        if k in ('c','v'):return (k,self.uv())
        if k=='pow2':return (k,self.expr())
        return (k,self.expr(),self.expr())
    def stmt(self)->Stmt:
        t=self.byte()
        if t==16:return Set(self.uv(),self.expr())
        if t==17:
            length=self.uv()
            if length>len(self.b)-self.i:raise InvalidCode('Impossible child count')
            return Seq(*(self.stmt() for _ in range(length)))
        if t==18:return Loop(self.uv(),self.expr(),self.stmt())
        if t==19:return If(self.expr(),self.stmt(),self.stmt())
        raise InvalidCode('Unknown statement')

def decode_bytes(b:bytes)->Program|None:
    if not isinstance(b,bytes):raise TypeError('Bytes required')
    if not b.startswith(MAGIC):return None
    r=Reader(b);r.i=len(MAGIC)
    try:
        p=Program(r.uv(),r.uv(),r.stmt())
        if r.i!=len(b):return None
        return p
    except (InvalidCode,ValueError):return None
    except RecursionError as e:raise ResourceLimit('Host parser stack exhausted; not invalid syntax') from e

def decode(index:int)->Program|None:
    nat(index)
    if index==0:return None
    b=index.to_bytes((index.bit_length()+7)//8,'big')
    if b[:1]!=b'\x01':return None
    return decode_bytes(b[1:])

@dataclass
class Meter:
    limit:int|None=2_000_000
    max_bits:int|None=1_000_000
    steps:int=0
    def tick(self)->None:
        self.steps+=1
        if self.limit is not None and self.steps>self.limit:raise ResourceLimit('Step limit; no semantic value returned')
    def check(self,x:int)->int:
        if self.max_bits is not None and x.bit_length()>self.max_bits:raise ResourceLimit('Integer storage bound')
        return x

def eval_expr(e:Expr,regs:dict[int,int],meter:Meter)->int:
    stack=[(e,False)];vals=[]
    while stack:
        t,ready=stack.pop();meter.tick();k=t[0]
        if k=='c':vals.append(meter.check(t[1]));continue
        if k=='v':vals.append(regs.get(t[1],0));continue
        if not ready:
            stack.append((t,True))
            for c in reversed(t[1:]):stack.append((c,False))
            continue
        if k=='pow2':
            a=vals.pop()
            if meter.max_bits is not None and a+1>meter.max_bits:raise ResourceLimit('Exponent storage bound')
            vals.append(1<<a);continue
        b=vals.pop();a=vals.pop()
        if k=='add':v=a+b
        elif k=='sub':v=max(0,a-b)
        elif k=='mul':v=a*b
        elif k=='div':v=a//b if b else 0
        elif k=='mod':v=a%b if b else a
        elif k=='le':v=int(a<=b)
        elif k=='eq':v=int(a==b)
        else:raise InvalidCode('Unknown executable expression')
        vals.append(meter.check(v))
    if len(vals)!=1:raise InvalidCode('Expression stack invariant')
    return vals[0]

def run(p:Program,args:Sequence[int],*,step_limit:int|None=2_000_000,max_bits:int|None=1_000_000,trace:bool=False):
    if len(args)!=p.arity:raise ValueError('Arity mismatch')
    regs={i:nat(v) for i,v in enumerate(args)};meter=Meter(step_limit,max_bits);stack=[('stmt',p.body)];events=[]
    while stack:
        task=stack.pop();meter.tick()
        if task[0]=='repeat':
            _,r,count,k,body=task
            if k<count:
                regs[r]=k
                stack.append(('repeat',r,count,k+1,body));stack.append(('stmt',body))
            continue
        s=task[1];tag=s[0]
        if tag=='set':
            regs[s[1]]=eval_expr(s[2],regs,meter)
            if trace:events.append((s[1],regs[s[1]]))
        elif tag=='seq':
            for t in reversed(s[1:]):stack.append(('stmt',t))
        elif tag=='loop':
            count=eval_expr(s[2],regs,meter);stack.append(('repeat',s[1],count,0,s[3]))
        elif tag=='if':stack.append(('stmt',s[2] if eval_expr(s[1],regs,meter) else s[3]))
        else:raise InvalidCode('Statement tag')
    value=regs.get(p.output,0)
    return (value,meter.steps,events) if trace else value

def evaluate_index(index:int,n:int,word:int,**limits)->int:
    p=decode(index)
    if p is None or p.arity!=2:return 0
    return run(p,(nat(n),nat(word)),**limits)%2

def word_code(bits:Sequence[int])->int:
    w=1
    for b in bits:
        if type(b) is not int or b not in (0,1):raise ValueError('Binary word required')
        w=2*w+b
    return w

def output_prefix(p:Program,bits:Sequence[int],**limits)->tuple[int,...]:
    if p.arity!=2:raise ValueError('Observer arity must be two')
    w=1;out=[]
    for n,b in enumerate(bits):
        if type(b) is not int or b not in (0,1):raise ValueError('Binary input')
        w=2*w+b;out.append(run(p,(n,w),**limits)%2)
    return tuple(out)

def _regs_expr(e:Expr)->set[int]:
    if e[0]=='v':return {e[1]}
    if e[0]=='c':return set()
    return set().union(*(_regs_expr(x) for x in e[1:]))

def registers(p:Program)->set[int]:
    out=set(range(p.arity))|{p.output};stack=[p.body]
    while stack:
        s=stack.pop();tag=s[0]
        if tag=='set':out.add(s[1]);out|=_regs_expr(s[2])
        elif tag=='seq':stack.extend(s[1:])
        elif tag=='loop':out.add(s[1]);out|=_regs_expr(s[2]);stack.append(s[3])
        elif tag=='if':out|=_regs_expr(s[1]);stack.extend(s[2:])
        else:raise InvalidCode('Bad statement')
    return out

def rename_expr(e:Expr,m:dict[int,int])->Expr:
    if e[0]=='v':return V(m[e[1]])
    if e[0]=='c':return e
    return E(e[0],*(rename_expr(x,m) for x in e[1:]))

def rename_stmt(s:Stmt,m:dict[int,int])->Stmt:
    k=s[0]
    if k=='set':return Set(m[s[1]],rename_expr(s[2],m))
    if k=='seq':return Seq(*(rename_stmt(t,m) for t in s[1:]))
    if k=='loop':return Loop(m[s[1]],rename_expr(s[2],m),rename_stmt(s[3],m))
    return If(rename_expr(s[1],m),rename_stmt(s[2],m),rename_stmt(s[3],m))

class Builder:
    def __init__(self,start:int):self.next=start
    def fresh(self)->int:r=self.next;self.next+=1;return r
    def inline(self,p:Program,args:Sequence[Expr],out:int)->Stmt:
        if len(args)!=p.arity:raise ValueError('Inline arity')
        # Reset EVERY source-local register on EVERY invocation. Omitting this
        # makes repeated calls history-dependent and invalidates the compiler.
        m={r:self.fresh() for r in sorted(registers(p))}
        return Seq(*(Set(r,C(0)) for r in m.values()),
                   *(Set(m[i],e) for i,e in enumerate(args)),
                   rename_stmt(p.body,m),Set(out,V(m[p.output])))

def pr_zero(k:int)->Program:return Program(nat(k),k,Set(k,C(0)))
def pr_succ()->Program:return Program(1,1,Set(1,E('add',V(0),C(1))))
def pr_proj(k:int,i:int)->Program:
    if not 0<=i<k:raise ValueError('Projection index')
    return Program(k,k,Set(k,V(i)))
def compose(f:Program,gs:Sequence[Program],k:int)->Program:
    if f.arity!=len(gs) or any(g.arity!=k for g in gs):raise ValueError('Composition arity')
    b=Builder(k+1);vals=[b.fresh() for _ in gs];args=[V(i) for i in range(k)]
    return Program(k,k,Seq(*(b.inline(g,args,t) for g,t in zip(gs,vals)),b.inline(f,[V(t) for t in vals],k)))
def prim_rec(g:Program,h:Program)->Program:
    k=g.arity
    if h.arity!=k+2:raise ValueError('Recursor step arity')
    b=Builder(k+2);idx=b.fresh();acc=b.fresh();tmp=b.fresh();args=[V(i) for i in range(k)]
    body=Seq(b.inline(g,args,acc),Loop(idx,V(k),Seq(b.inline(h,args+[V(idx),V(acc)],tmp),Set(acc,V(tmp)))),Set(k+1,V(acc)))
    return Program(k+1,k+1,body)

def _candidate(matrix:Program,prefix:Sequence[Expr],stage:Expr,out:int,b:Builder)->Stmt:
    if matrix.arity!=len(prefix)+2:raise ValueError('Normal-form matrix arity')
    u=b.fresh();s=b.fresh();t=b.fresh();found=b.fresh();good=b.fresh();value=b.fresh()
    call=b.inline(matrix,list(prefix)+[V(s),V(t)],value)
    return Seq(Set(u,stage),Set(out,E('add',V(u),C(1))),Set(found,C(0)),
      Loop(s,E('add',V(u),C(1)),If(E('eq',V(found),C(0)),Seq(
        Set(good,C(1)),Loop(t,E('add',V(u),C(1)),Seq(call,If(E('eq',V(value),C(0)),Set(good,C(0))))),
        If(V(good),Seq(Set(out,V(s)),Set(found,C(1))))))))

def compile_sigma2(matrix:Program,parameter:int)->Program:
    """Matrix R(e,s,t): defect 0 iff exists s forall t R(e,s,t)!=0; else 1."""
    if matrix.arity!=3:raise ValueError('Sigma2 matrix has arity three')
    b=Builder(3);now=b.fresh();old=b.fresh()
    return Program(2,2,Seq(_candidate(matrix,[C(parameter)],V(0),now,b),
       Set(old,C(0)),If(V(0),_candidate(matrix,[C(parameter)],E('sub',V(0),C(1)),old,b)),
       Set(2,C(0)),If(E('eq',V(now),V(old)),Seq(),Set(2,E('mod',V(1),C(2))))))

def _bit(word:Expr,length:Expr,j:Expr)->Expr:
    return E('mod',E('div',word,E('pow2',E('sub',E('sub',length,C(1)),j))),C(2))

def compile_pi3(matrix:Program,parameter:int)->Program:
    """R(e,i,s,t): defect sum_i 2^(-i-1) [no s forall t R(e,i,s,t)]."""
    if matrix.arity!=4:raise ValueError('Pi3 matrix has arity four')
    b=Builder(3);j=b.fresh();found=b.fresh();sel=b.fresh();stage=b.fresh();now=b.fresh();old=b.fresh()
    cur=E('mod',V(1),C(2));length=E('add',V(0),C(1))
    scan=Loop(j,length,If(E('eq',V(found),C(0)),If(E('eq',_bit(V(1),length,V(j)),C(0)),Seq(Set(found,C(1)),Set(sel,V(j))))))
    tail=Seq(Set(stage,E('sub',E('sub',V(0),V(sel)),C(1))),
      _candidate(matrix,[C(parameter),V(sel)],V(stage),now,b),Set(old,C(0)),
      If(V(stage),_candidate(matrix,[C(parameter),V(sel)],E('sub',V(stage),C(1)),old,b)),
      Set(2,C(0)),If(E('eq',V(now),V(old)),Seq(),Set(2,cur)))
    return Program(2,2,Seq(Set(found,C(0)),Set(sel,C(0)),scan,Set(2,cur),If(V(found),If(E('eq',V(0),V(sel)),Seq(),tail))))

def compile_shift(observer:Program,a:int,bden:int)->Program:
    """d(new) = a/b + (1-a/b)*d(observer), for 0<=a<=b and b>0."""
    nat(a);nat(bden)
    if not bden or a>bden or observer.arity!=2:raise ValueError('Shift requires rational unit interval and binary observer')
    b=Builder(3);j=b.fresh();found=b.fresh();branch=b.fresh();stop=b.fresh();value=b.fresh();den=b.fresh();tail_len=b.fresh();tail_word=b.fresh();answer=b.fresh()
    L=E('add',V(0),C(1));cur=E('mod',V(1),C(2));jlen=E('add',V(j),C(1))
    # Prefix value deletes the high sentinel by reduction modulo 2^jlen.
    scan=Loop(j,L,If(E('eq',V(found),C(0)),Seq(
      Set(den,E('pow2',jlen)),Set(value,E('mod',E('div',V(1),E('pow2',E('sub',L,jlen))),V(den))),
      If(E('le',E('mul',C(bden),E('add',V(value),C(1))),E('mul',C(a),V(den))),
         Seq(Set(found,C(1)),Set(branch,C(0)),Set(stop,jlen)),
         If(E('le',E('mul',C(a),V(den)),E('mul',C(bden),V(value))),
            Seq(Set(found,C(1)),Set(branch,C(1)),Set(stop,jlen)))))))
    replay=Seq(Set(tail_len,E('sub',L,V(stop))),Set(tail_word,E('add',E('pow2',V(tail_len)),E('mod',V(1),E('pow2',V(tail_len))))),
      b.inline(observer,[E('sub',V(tail_len),C(1)),V(tail_word)],answer),Set(2,E('mod',V(answer),C(2))))
    # Newly completed stopping prefix is still copied, before branch execution.
    return Program(2,2,Seq(Set(found,C(0)),Set(branch,C(0)),Set(stop,C(0)),scan,Set(2,cur),
        If(V(found),If(V(branch),If(E('le',V(stop),V(0)),replay)))))

def compile_q8(machine:Sequence[tuple])->Program:
    """Finite two-counter machine -> bounded-halting observer (zero iff never halts).
    Instructions: ('H',), ('I',r,next), ('D',r,zero_target,nonzero_target).
    Both counters initially zero; falling off code is refused, not halting.
    """
    if not machine:raise ValueError('Nonempty machine required')
    for ins in machine:
        if not isinstance(ins,tuple) or not ins:raise ValueError('Malformed counter instruction')
        if ins==('H',):continue
        if ins[0]=='I' and len(ins)==3 and ins[1] in (0,1) and type(ins[1]) is int and type(ins[2]) is int and 0<=ins[2]<len(machine):continue
        if ins[0]=='D' and len(ins)==4 and ins[1] in (0,1) and type(ins[1]) is int and all(type(j) is int and 0<=j<len(machine) for j in ins[2:]):continue
        raise ValueError('Malformed counter machine')
    b=Builder(3);pc=b.fresh();oldpc=b.fresh();halt=b.fresh();t=b.fresh();c=[b.fresh(),b.fresh()];cases=[]
    for i,ins in enumerate(machine):
        if ins[0]=='H':body=Set(halt,C(1))
        elif ins[0]=='I':body=Seq(Set(c[ins[1]],E('add',V(c[ins[1]]),C(1))),Set(pc,C(ins[2])))
        else:body=If(E('eq',V(c[ins[1]]),C(0)),Set(pc,C(ins[2])),Seq(Set(c[ins[1]],E('sub',V(c[ins[1]]),C(1))),Set(pc,C(ins[3]))))
        cases.append(If(E('eq',V(oldpc),C(i)),body))
    return Program(2,2,Seq(Set(pc,C(0)),Set(halt,C(0)),*(Set(r,C(0)) for r in c),
        Loop(t,E('add',V(0),C(1)),If(E('eq',V(halt),C(0)),Seq(Set(oldpc,V(pc)),*cases))),
        Set(2,C(0)),If(V(halt),Set(2,E('mod',V(1),C(2))))))
