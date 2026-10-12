"""P01 attempt-0003 finite-evidence dependent frontend.

NEW proposal code, not recovered attempt-0002 material. Acceptance here is a
syntactic typing/certificate result, NEVER a Lean or empirical-authority result.
The exact canonical Cert export is partial and independently replayed by Lean.
"""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable

Node = tuple
class Refusal(ValueError):
    """Fail closed. A refusal is not a proof of inequivalence or untypability."""

@dataclass(frozen=True)
class Result:
    status: str
    reason: str = ''
    ty: Node | None = None
    term: Node | None = None
    context: tuple = ()
    type_depth: int = 0
    kernel_verified: bool = False

@dataclass
class Budget:
    left: int = 200000
    def tick(self) -> None:
        self.left -= 1
        if self.left < 0: raise Refusal('RESOURCE_CHECK_STEPS')

def natural(x: Any, label: str) -> int:
    if type(x) is not int or x < 0: raise Refusal('MALFORMED_'+label)
    return x

def freeze(x: Any, *, max_nodes: int=100000, max_depth: int=200) -> Any:
    natural(max_nodes,'MAX_NODES'); natural(max_depth,'MAX_DEPTH')
    active: set[int] = set(); count=0
    def go(y: Any, d: int) -> Any:
        nonlocal count
        count += 1
        if count > max_nodes or d > max_depth: raise Refusal('RESOURCE_AST_BOUND')
        if type(y) in (tuple,list):
            if id(y) in active: raise Refusal('MALFORMED_CYCLIC_INPUT')
            active.add(id(y))
            try: return tuple(go(a,d+1) for a in y)
            finally: active.remove(id(y))
        if type(y) is str: return y
        if type(y) is int: return y
        raise Refusal('MALFORMED_SCALAR')
    return go(x,0)

TYPE_TAGS={'tv','bot','pi','sig','id','all'}
TERM_TAGS={'var','I','K','S','zero','one','lam','app','pair','fst','snd','refl','eta','J','allI','allE','cast'}

def node(x: Any) -> str:
    if type(x) is not tuple or not x or type(x[0]) is not str: raise Refusal('MALFORMED_NODE')
    return x[0]

def arity(x: Node,n: int) -> None:
    if len(x)!=n+1: raise Refusal('MALFORMED_ARITY_'+str(x[0]))

def paths(ps: Any) -> None:
    if type(ps) is not tuple: raise Refusal('MALFORMED_PATHS')
    for p in ps:
        if type(p) is not tuple: raise Refusal('MALFORMED_PATH')
        for k in p: natural(k,'PATH_INDEX')

def validate_type(t: Node) -> None:
    tag=node(t)
    if tag=='tv': arity(t,1);natural(t[1],'TYPE_INDEX')
    elif tag=='bot': arity(t,0)
    elif tag in ('pi','sig'):
        arity(t,2);validate_type(t[1]);validate_type(t[2])
    elif tag=='id':
        arity(t,3);validate_type(t[1]);validate_term(t[2]);validate_term(t[3])
    elif tag=='all':arity(t,1);validate_type(t[1])
    else:raise Refusal('MALFORMED_TYPE_TAG')

def validate_term(t: Node) -> None:
    tag=node(t)
    if tag=='var':arity(t,1);natural(t[1],'TERM_INDEX')
    elif tag in ('I','K','S'):
        arity(t,{'I':1,'K':2,'S':3}[tag])
        for a in t[1:]:validate_type(a)
    elif tag in ('zero','one'):arity(t,0)
    elif tag=='lam':arity(t,2);validate_type(t[1]);validate_term(t[2])
    elif tag=='app':arity(t,2);validate_term(t[1]);validate_term(t[2])
    elif tag=='pair':
        arity(t,3);validate_type(t[1]);validate_term(t[2]);validate_term(t[3])
    elif tag in ('fst','snd','refl','eta','allI'):
        arity(t,1);validate_term(t[1])
    elif tag=='allE':arity(t,2);validate_term(t[1]);validate_type(t[2])
    elif tag=='J':
        arity(t,6);validate_type(t[1]);validate_term(t[2]);validate_type(t[3])
        for a in t[4:]:validate_term(a)
    elif tag=='cast':
        arity(t,4);validate_term(t[1]);validate_type(t[2]);paths(t[3]);paths(t[4])
    else:raise Refusal('MALFORMED_TERM_TAG')

ID=lambda n:n
VAR=lambda n:('var',n)
TV=lambda n:('tv',n)

def _lift(r: Callable[[int],int]) -> Callable[[int],int]:
    return lambda n: 0 if n==0 else r(n-1)+1

def _rename(t: Node, rt: Callable[[int],int], ry: Callable[[int],int]) -> Node:
    tag=t[0]
    if tag=='var':return VAR(rt(t[1]))
    if tag=='tv':return TV(ry(t[1]))
    if tag in ('bot','zero','one'):return t
    if tag in ('lam','pi','sig'):
        return (tag,_rename(t[1],rt,ry),_rename(t[2],_lift(rt),ry))
    if tag in ('all','allI'):return (tag,_rename(t[1],rt,_lift(ry)))
    if tag=='J':return (tag,_rename(t[1],rt,ry),_rename(t[2],rt,ry),
        _rename(t[3],_lift(_lift(rt)),ry),*(_rename(a,rt,ry) for a in t[4:]))
    if tag=='cast':return (tag,_rename(t[1],rt,ry),_rename(t[2],rt,ry),t[3],t[4])
    return (tag,*(_rename(a,rt,ry) for a in t[1:]))

def rename_term(t: Node,rt: Callable[[int],int]=ID,ry: Callable[[int],int]=ID) -> Node:
    return _rename(t,rt,ry)

def rename_type(t: Node,rt: Callable[[int],int]=ID,ry: Callable[[int],int]=ID) -> Node:
    return _rename(t,rt,ry)

def _lift_term(tm,ty):
    return (lambda n:VAR(0) if n==0 else _rename(tm(n-1),lambda k:k+1,ID),
            lambda n:_rename(ty(n),lambda k:k+1,ID))

def _lift_type(tm,ty):
    return (lambda n:_rename(tm(n),ID,lambda k:k+1),
            lambda n:TV(0) if n==0 else _rename(ty(n-1),ID,lambda k:k+1))

def substitute(t: Node,tm: Callable[[int],Node],ty: Callable[[int],Node]) -> Node:
    tag=t[0]
    if tag=='var':return tm(t[1])
    if tag=='tv':return ty(t[1])
    if tag in ('bot','zero','one'):return t
    if tag in ('lam','pi','sig'):
        lm,ly=_lift_term(tm,ty)
        return (tag,substitute(t[1],tm,ty),substitute(t[2],lm,ly))
    if tag in ('all','allI'):
        lm,ly=_lift_type(tm,ty);return(tag,substitute(t[1],lm,ly))
    if tag=='J':
        lm,ly=_lift_term(*_lift_term(tm,ty))
        return(tag,substitute(t[1],tm,ty),substitute(t[2],tm,ty),
            substitute(t[3],lm,ly),*(substitute(a,tm,ty) for a in t[4:]))
    if tag=='cast':return(tag,substitute(t[1],tm,ty),substitute(t[2],tm,ty),t[3],t[4])
    return (tag,*(substitute(a,tm,ty) for a in t[1:]))

def instantiate_term(body: Node,arg: Node) -> Node:
    return substitute(body,lambda n:arg if n==0 else VAR(n-1),TV)

def instantiate_type(body: Node,arg: Node) -> Node:
    return substitute(body,VAR,lambda n:arg if n==0 else TV(n-1))

def instantiate_motive(body: Node,y: Node,p: Node) -> Node:
    return substitute(body,lambda n:p if n==0 else y if n==1 else VAR(n-2),TV)

def _term_children(t: Node) -> tuple[int,...]:
    tag=t[0]
    if tag in ('var','tv','bot','zero','one'):return ()
    if tag=='cast':return(1,2)
    return tuple(range(1,len(t)))

def root_step(t: Node) -> Node:
    tag=t[0]
    if tag=='app':
        f,x=t[1:]
        if f[0]=='I':return x
        if f[0]=='lam':return instantiate_term(f[2],x)
        if f[0]=='app' and f[1][0]=='K':return f[2]
        if f[0]=='app' and f[1][0]=='app' and f[1][1][0]=='S':
            return ('app',('app',f[1][2],x),('app',f[2],x))
    elif tag=='fst' and t[1][0]=='pair':return t[1][2]
    elif tag=='snd' and t[1][0]=='pair':return t[1][3]
    elif tag=='J' and t[5]==t[2] and t[6]==('refl',t[2]):return t[4]
    elif tag=='allE' and t[1][0]=='allI':return instantiate_type(t[1][1],t[2])
    elif tag=='cast':return t[1]
    raise Refusal('NO_REDUCTION_AT_ADDRESS')

def step_at(t: Node,address: tuple[int,...]) -> Node:
    if type(address) is not tuple:raise Refusal('MALFORMED_ADDRESS')
    if not address:return root_step(t)
    i=natural(address[0],'ADDRESS_INDEX')
    if i not in _term_children(t):raise Refusal('INVALID_REDUCTION_ADDRESS')
    out=list(t);out[i]=step_at(t[i],address[1:]);return tuple(out)

def replay(t: Node,ps: tuple,limit: int=10000) -> Node:
    paths(ps)
    if len(ps)>limit:raise Refusal('RESOURCE_CERTIFICATE_STEPS')
    for p in ps:t=step_at(t,p)
    return t

def prove_conversion(a: Node,b: Node,left: tuple,right: tuple) -> bool:
    if replay(a,left)!=replay(b,right):raise Refusal('CERTIFICATE_ENDPOINT_MISMATCH')
    return True

def first_step(t: Node,prefix: tuple=()) -> tuple[Node,tuple] | None:
    try:return root_step(t),prefix
    except Refusal as e:
        if str(e)!='NO_REDUCTION_AT_ADDRESS':raise
    for i in _term_children(t):
        found=first_step(t[i],prefix+(i,))
        if found is not None:
            child,addr=found;out=list(t);out[i]=child;return tuple(out),addr
    return None

def normalise(t: Node,budget: int=10000) -> tuple[Node,tuple]:
    natural(budget,'NORMALISATION_BUDGET');trace=[]
    while True:
        step=first_step(t)
        if step is None:return t,tuple(trace)
        if len(trace)>=budget:raise Refusal('RESOURCE_NORMALISATION_REFUSED_NOT_INEQUALITY')
        t,addr=step;trace.append(addr)

def _shift(t:Node)->Node:return _rename(t,lambda n:n+1,ID)
def _tyshift(t:Node)->Node:return _rename(t,ID,lambda n:n+1)
def _extend(ctx:tuple,A:Node)->tuple:return (_shift(A),*(_shift(t) for t in ctx))
def _arr(A:Node,B:Node)->Node:return ('pi',A,_shift(B))
def _expect(got:Node,expected:Node)->None:
    if got!=expected:raise Refusal('NO_TYPE_EQUALITY_EVIDENCE')

def wf(T:Node,ctx:tuple,d:int,b:Budget)->None:
    b.tick();tag=T[0]
    if tag=='bot':return
    if tag=='tv':
        if T[1]>=d:raise Refusal('UNBOUND_TYPE_VARIABLE')
    elif tag in ('pi','sig'):
        wf(T[1],ctx,d,b);wf(T[2],_extend(ctx,T[1]),d,b)
    elif tag=='id':
        wf(T[1],ctx,d,b)
        _expect(synth(T[2],ctx,d,b),T[1]);_expect(synth(T[3],ctx,d,b),T[1])
    elif tag=='all':wf(T[1],tuple(_tyshift(A) for A in ctx),d+1,b)
    else:raise Refusal('MALFORMED_TYPE_TAG')

def synth(t:Node,ctx:tuple,d:int,b:Budget)->Node:
    b.tick();tag=t[0]
    if tag=='var':
        if t[1]>=len(ctx):raise Refusal('UNBOUND_TERM_VARIABLE')
        return ctx[t[1]]
    if tag in ('I','K','S'):
        for A in t[1:]:wf(A,ctx,d,b)
        if tag=='I':return _arr(t[1],t[1])
        if tag=='K':return _arr(t[1],_arr(t[2],t[1]))
        A,B,C=t[1:];return _arr(_arr(A,_arr(B,C)),_arr(_arr(A,B),_arr(A,C)))
    if tag=='lam':
        wf(t[1],ctx,d,b)
        return ('pi',t[1],synth(t[2],_extend(ctx,t[1]),d,b))
    if tag=='app':
        ft=synth(t[1],ctx,d,b)
        if ft[0]!='pi':raise Refusal('FUNCTION_TYPE_EVIDENCE_REQUIRED')
        _expect(synth(t[2],ctx,d,b),ft[1])
        return instantiate_term(ft[2],t[2])
    if tag=='pair':
        S=t[1];wf(S,ctx,d,b)
        if S[0]!='sig':raise Refusal('SIGMA_ANNOTATION_REQUIRED')
        _expect(synth(t[2],ctx,d,b),S[1])
        _expect(synth(t[3],ctx,d,b),instantiate_term(S[2],t[2]))
        return S
    if tag in ('fst','snd'):
        S=synth(t[1],ctx,d,b)
        if S[0]!='sig':raise Refusal('SIGMA_TYPE_EVIDENCE_REQUIRED')
        return S[1] if tag=='fst' else instantiate_term(S[2],('fst',t[1]))
    if tag=='refl':
        A=synth(t[1],ctx,d,b);return('id',A,t[1],t[1])
    if tag=='eta':
        S=synth(t[1],ctx,d,b)
        if S[0]!='sig':raise Refusal('SIGMA_TYPE_EVIDENCE_REQUIRED')
        return ('id',S,t[1],('pair',S,('fst',t[1]),('snd',t[1])))
    if tag=='J':
        A,x,C,base,y,p=t[1:]
        wf(A,ctx,d,b)
        _expect(synth(x,ctx,d,b),A);_expect(synth(y,ctx,d,b),A)
        _expect(synth(p,ctx,d,b),('id',A,x,y))
        ext=_extend(ctx,A)
        proofTy=('id',_shift(A),_shift(x),VAR(0))
        wf(C,_extend(ext,proofTy),d,b)
        _expect(synth(base,ctx,d,b),instantiate_motive(C,x,('refl',x)))
        return instantiate_motive(C,y,p)
    if tag=='allI':
        return ('all',synth(t[1],tuple(_tyshift(A) for A in ctx),d+1,b))
    if tag=='allE':
        ft=synth(t[1],ctx,d,b);wf(t[2],ctx,d,b)
        if ft[0]!='all':raise Refusal('ALL_TYPE_EVIDENCE_REQUIRED')
        return instantiate_type(ft[1],t[2])
    if tag=='cast':
        old=synth(t[1],ctx,d,b);wf(t[2],ctx,d,b)
        prove_conversion(old,t[2],t[3],t[4]);return t[2]
    raise Refusal('NO_TYPING_RULE_FOR_'+tag)

def check(term:Any,*,context:Any=(),type_depth:int=0,max_nodes:int=100000,max_depth:int=200,
          max_check_steps:int=200000)->Result:
    try:
        natural(type_depth,'TYPE_DEPTH');natural(max_check_steps,'CHECK_BUDGET')
        raw=freeze((term,context),max_nodes=max_nodes,max_depth=max_depth)
        t,decls=raw;validate_term(t)
        if type(decls) is not tuple:raise Refusal('MALFORMED_CONTEXT')
        b=Budget(max_check_steps);ctx=()
        for A in decls:validate_type(A);wf(A,ctx,type_depth,b);ctx=_extend(ctx,A)
        T=synth(t,ctx,type_depth,b);wf(T,ctx,type_depth,b)
        return Result('ACCEPTED','FINITE_SYNTACTIC_CERTIFICATE_ONLY',T,t,decls,type_depth)
    except Refusal as e:return Result('REFUSED',str(e))
    except RecursionError:return Result('REFUSED','RESOURCE_PYTHON_RECURSION')
    except (TypeError,ValueError,IndexError,KeyError) as e:
        return Result('REFUSED','MALFORMED_'+type(e).__name__)

# Actual finite SKI polynomial compiler. v is the only variable node.
def _pa(f,x):return('app',f,x)
def _free(p):return p[0]=='v' and p[1]==0 or p[0]=='app' and (_free(p[1]) or _free(p[2]))
def _drop(p):
    if p[0]=='v':return('v',max(p[1]-1,0))
    if p[0]=='app':return _pa(_drop(p[1]),_drop(p[2]))
    return p

def bracket(p):
    if not _free(p):return _pa(('k',),_drop(p))
    if p==('v',0):return('i',)
    if p[0]=='app':return _pa(_pa(('s',),bracket(p[1])),bracket(p[2]))
    raise Refusal('INTERNAL_POLYNOMIAL_SHAPE')

def compile_poly(t:Node)->Node:
    tag=t[0]
    if tag=='var':return('v',t[1])
    if tag in ('I','K','S'):return(tag.lower(),)
    if tag in ('zero','one'):return t
    if tag=='lam':return bracket(compile_poly(t[2]))
    if tag=='app':return _pa(compile_poly(t[1]),compile_poly(t[2]))
    if tag=='pair':
        a,c=compile_poly(t[2]),compile_poly(t[3]);i,k,s=('i',),('k',),('s',)
        return _pa(_pa(s,_pa(_pa(s,i),_pa(k,a))),_pa(k,c))
    if tag=='fst':return _pa(compile_poly(t[1]),('k',))
    if tag=='snd':return _pa(compile_poly(t[1]),_pa(('k',),('i',)))
    if tag in ('refl','eta'):return('i',)
    if tag=='J':
        d,y,p=map(compile_poly,(t[4],t[5],t[6]));k=('k',)
        return _pa(_pa(_pa(k,_pa(k,d)),y),p)
    if tag in ('allI','allE','cast'):return compile_poly(t[1])
    raise Refusal('COMPILER_TAG_REFUSED')

# Deliberately exact canonical TypeCode/Cert target. No encoding invents an Id
# or Sigma constructor in that unchanged target vocabulary.
def _tc(T:Node)->Node:
    tag=T[0]
    if tag in ('tv','bot'):return T
    if tag=='all':return('all',_tc(T[1]))
    if tag=='pi':return('arrow',_tc(T[1]),_tc(T[2]))
    raise Refusal('REFUSED_TARGET_VOCABULARY')

def _tcstr(T:Node)->str:
    tag=T[0]
    if tag=='tv':return f'(OrthemologyV2.TypeCode.var {T[1]})'
    if tag=='bot':return 'OrthemologyV2.TypeCode.bottom'
    if tag=='all':return f'(OrthemologyV2.TypeCode.all {_tcstr(T[1])})'
    if tag=='arrow':return f'(OrthemologyV2.TypeCode.arrow {_tcstr(T[1])} {_tcstr(T[2])})'
    raise Refusal('REFUSED_TARGET_VOCABULARY')

@dataclass(frozen=True)
class CT:
    rule:str
    ty:Node
    children:tuple=()
    args:tuple=()

def _ca(f:CT,x:CT)->CT:
    if f.ty[0]!='arrow' or f.ty[1]!=x.ty:raise Refusal('INTERNAL_FINITE_TYPE_MISMATCH')
    return CT('app',f.ty[2],(f,x))
def _ci(A):return CT('i',('arrow',A,A),args=(A,))
def _ck(A,B):return CT('k',('arrow',A,('arrow',B,A)),args=(A,B))
def _cs(A,B,C):return CT('s',('arrow',('arrow',A,('arrow',B,C)),('arrow',('arrow',A,B),('arrow',A,C))),args=(A,B,C))
def _contains(c:CT,n:int)->bool:return c.rule=='var' and c.args[0]==n or any(_contains(a,n) for a in c.children)
def _ctdrop(c:CT)->CT:
    return CT(c.rule,c.ty,tuple(_ctdrop(a) for a in c.children),
              (c.args[0]-1,) if c.rule=='var' else c.args)
def _abstract_cert(c:CT,A:Node)->CT:
    if not _contains(c,0):return _ca(_ck(c.ty,A),_ctdrop(c))
    if c.rule=='var':
        if c.args[0]!=0 or c.ty!=A:raise Refusal('INTERNAL_BINDER_TYPE')
        return _ci(A)
    if c.rule=='app':
        f,x=c.children;return _ca(_ca(_cs(A,x.ty,c.ty),_abstract_cert(f,A)),_abstract_cert(x,A))
    raise Refusal('REFUSED_POLYMORPHIC_ABSTRACTION_ENCODING')

def _encode(t:Node,ctx:tuple,d:int)->CT:
    tag=t[0]
    T=_tc(synth(t,ctx,d,Budget()))
    if tag=='var':return CT('var',T,args=(t[1],))
    if tag=='I':return _ci(_tc(t[1]))
    if tag=='K':return _ck(_tc(t[1]),_tc(t[2]))
    if tag=='S':return _cs(*map(_tc,t[1:]))
    if tag=='app':return _ca(_encode(t[1],ctx,d),_encode(t[2],ctx,d))
    if tag=='lam':return _abstract_cert(_encode(t[2],_extend(ctx,t[1]),d),_tc(t[1]))
    if tag=='allI':
        if ctx:raise Refusal('REFUSED_OPEN_POLYMORPHIC_ENCODING')
        c=_encode(t[1],(),d+1);return CT('allI',T,(c,))
    if tag=='allE':
        c=_encode(t[1],ctx,d);return CT('allE',T,(c,),(_tc(t[2]),))
    if tag=='cast':
        c=_encode(t[1],ctx,d)
        if c.ty!=T:raise Refusal('REFUSED_NONLITERAL_FINITE_TYPE_CAST')
        return c
    raise Refusal('REFUSED_TARGET_VOCABULARY')

def _certstr(c:CT)->str:
    if c.rule=='var':raise Refusal('REFUSED_OPEN_DERIVATION')
    args=[_certstr(a) for a in c.children]+[_tcstr(A) for A in c.args]
    return '(OrthemologyV3.Cert.'+c.rule+(' '+' '.join(args) if args else '')+')'

def _certterm(c:CT)->Node:
    if c.rule in ('i','k','s'):return(c.rule,)
    if c.rule=='app':return _pa(_certterm(c.children[0]),_certterm(c.children[1]))
    if c.rule in ('allI','allE'):return _certterm(c.children[0])
    raise Refusal('REFUSED_OPEN_DERIVATION')

def export_finite(r:Result)->dict:
    out={'kernel_verified':False,'target':'UNCHANGED_OrthemologyV3.Cert',
         'claim':'PARTIAL_RENDERER_REQUIRES_BOUND_KERNEL_REPLAY'}
    if not isinstance(r,Result) or r.status!='ACCEPTED':return dict(out,status='REFUSED_NOT_ACCEPTED')
    if r.context:return dict(out,status='REFUSED_OPEN_CONTEXT')
    fresh=check(r.term,type_depth=r.type_depth)
    if fresh.status!='ACCEPTED' or fresh.ty!=r.ty:return dict(out,status='REFUSED_RECHECK_MISMATCH')
    try:
        expected=_tc(r.ty);c=_encode(r.term,(),r.type_depth)
        if c.ty!=expected:raise Refusal('REFUSED_BINDING_MISMATCH')
        encoded=_certstr(c)
        if _certterm(c)!=compile_poly(r.term):raise Refusal('REFUSED_CODE_BINDING_MISMATCH')
        return dict(out,status='EXPORTABLE_FINITE',lean_certificate=encoded,
                    source_typecode=expected,compiled_term=_certterm(c),type_depth=r.type_depth)
    except Refusal as e:return dict(out,status=str(e))
