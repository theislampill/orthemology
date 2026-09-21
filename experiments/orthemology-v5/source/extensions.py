"""Executable extensions and bounded checks for the v3 review response.

No function quantifies computationally over the full semantic Code universe.
Symbolic-selector certificates validate a concrete finite trace; the separate
substitution theorem is what generalises such a trace, not statistical testing.
Probabilities are exact Fractions. A mix is evaluated into a distribution of
raw deterministic terms before combinatory evaluation; distinct occurrences
are independent samples. Type abstractions/applications erase completely.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Any, Hashable, Iterable, Sequence
import reference as r

Program = tuple
Compiled = tuple
TypeCode = tuple
Distribution = dict[Program, Fraction]
I,K,S,Z,O = [(x,) for x in ['i','k','s','zero','one']]

def app(f: Program, x: Program) -> Program:
    return ('app', f, x)

def _program(t: Any) -> Program:
    t = r._freeze(t)
    r._wf_program(t)
    return t

def marker_free(t: Any) -> bool:
    t = _program(t)
    def go(a: Program) -> bool:
        return (go(a[1]) and go(a[2])) if a[0]=='app' else a not in (Z,O)
    return go(t)

def substitute_markers(t: Any, zero: Any, one: Any) -> Program:
    t,zero,one=map(_program,(t,zero,one))
    def go(a: Program) -> Program:
        if a==Z: return zero
        if a==O: return one
        if a[0]=='app': return app(go(a[1]),go(a[2]))
        return a
    return go(t)

def compatible_steps(t: Any) -> frozenset[Program]:
    """All one-step v2 reductions, including reductions inside arguments."""
    t=_program(t)
    def go(a: Program) -> set[Program]:
        if a[0]!='app': return set()
        f,x=a[1:]
        out=set()
        if f==I: out.add(x)
        if f[0]=='app' and f[1]==K: out.add(f[2])
        if f[0]=='app' and f[1][0]=='app' and f[1][1]==S:
            out.add(app(app(f[1][2],x),app(f[2],x)))
        out.update(app(g,x) for g in go(f))
        out.update(app(f,y) for y in go(x))
        return out
    return frozenset(go(t))

@dataclass(frozen=True)
class SelectorCertificate:
    program: Program
    trace: tuple[Program,...]
    selector: int

    @property
    def overhead(self) -> int:
        return len(self.trace)-1


def certify_selector(program: Any, trace: Sequence[Any]) -> SelectorCertificate:
    r.bound_tree(trace,nodes=200000)
    program=_program(program)
    if not marker_free(program):
        raise r.Rejection('probe markers must be fresh: the program contains a marker')
    if type(trace) not in (list,tuple) or not 1 <= len(trace) <= r.MAX_NODES:
        raise r.Rejection('a bounded nonempty trace is required')
    tr=tuple(_program(t) for t in trace)
    if tr[0] != app(app(program,Z),O):
        raise r.Rejection('trace does not begin with the two symbolic arguments')
    for left,right in zip(tr,tr[1:]):
        if r.head_step(left) != right:
            raise r.Rejection('invalid weak-head computation certificate')
    if tr[-1] not in (Z,O):
        raise r.Rejection('the probe must finish at exactly one fresh marker')
    return SelectorCertificate(program,tr,0 if tr[-1]==Z else 1)


def replay_selector(cert: SelectorCertificate, x: Any, y: Any) -> tuple[Program,...]:
    if type(cert) is not SelectorCertificate:raise r.Rejection("certificate: wrong object type")
    # Treat even a caller-constructed dataclass as untrusted input.
    good=certify_selector(cert.program,cert.trace)
    if good != cert: raise r.Rejection('inconsistent selector metadata')
    x,y=_program(x),_program(y)
    trace=tuple(substitute_markers(t,x,y) for t in good.trace)
    if trace[0] != app(app(good.program,x),y):
        raise AssertionError('fresh-marker substitution changed the program')
    for a,b in zip(trace,trace[1:]):
        if r.head_step(a) != b:
            raise AssertionError('symbolic head-step substitution failed')
    if trace[-1] != (x,y)[good.selector]:
        raise AssertionError('wrong selected argument')
    return trace


def _weight(value: Any) -> Fraction:
    if (type(value) not in (list,tuple) or len(value)!=2 or
        any(type(x) is not int for x in value) or value[1]<=0):
        raise r.Rejection('a probability must be an exact [integer, positive integer] pair')
    if max(abs(x).bit_length() for x in value)>r.MAX_INT_BITS:raise r.Rejection("resource: probability integer bits")
    p=Fraction(*value)
    if not 0 <= p <= 1: raise r.Rejection('probability outside [0,1]')
    return p


def compile_probability(p: Any, type_depth: int=0) -> tuple[Compiled,TypeCode]:
    """Finite proof-directed effect elaboration; quantifier nodes erase.

    The two mix branches must have the same type even at probability endpoints.
    Application samples its function and argument independently, exactly once
    each, then constructs the pure application of those sampled programs.
    This is not an evaluator with arbitrary run-time semantic type tests.
    """
    if not r._natural(type_depth): raise r.Rejection('invalid type depth')
    r.bound_tree(p)
    budget=[r.MAX_NODES]
    work=[2000000]
    def go(n: Any,d: int,h: int) -> tuple[Compiled,TypeCode]:
        result=raw_go(n,d,h)
        for part in result:r.bound_tree(part,work=work,fractions=True)
        return result
    def raw_go(n: Any,d: int,h: int) -> tuple[Compiled,TypeCode]:
        budget[0]-=1
        if h>r.MAX_DEPTH or budget[0]<0: raise r.Rejection('effect syntax resource limit')
        if type(n) is not dict or type(n.get('op')) is not str:
            raise r.Rejection('effect node must have a named operation')
        op=n['op']
        def fields(*keys: str) -> None:
            if set(n) != {'op',*keys}: raise r.Rejection(f'incorrect fields for {op}')
        if op=='pure':
            fields('proof'); t,a=r.check(n['proof'],d)
            return ('pure',t),a
        if op=='mix':
            fields('p','left','right'); q=_weight(n['p'])
            l,a=go(n['left'],d,h+1); rr,b=go(n['right'],d,h+1)
            if a!=b: raise r.Rejection('mixture branches have different types')
            return ('mix',q,l,rr),a
        if op=='app':
            fields('function','argument')
            f,a=go(n['function'],d,h+1); x,b=go(n['argument'],d,h+1)
            if a[0]!='arr' or a[1]!=b: raise r.Rejection('effect application domain mismatch')
            return ('app',f,x),a[2]
        if op=='all_i':
            fields('body'); t,a=go(n['body'],d+1,h+1)
            return t,('all',a)
        if op=='all_e':
            fields('polymorphic','type'); t,a=go(n['polymorphic'],d,h+1)
            b=r._freeze(n['type']); r._wf_type(b,d)
            if a[0]!='all': raise r.Rejection('effect type application requires all')
            out=r.instantiate_type(a[1],b); r._wf_type(out,d)
            return t,out
        raise r.Rejection(f'unknown effect operation: {op}')
    return go(p,type_depth,0)


def _add(out: Distribution,t: Program,p: Fraction) -> None:
    if max(p.numerator.bit_length(),p.denominator.bit_length())>4096:raise r.Rejection("resource: probability bits")
    if p:
        r.bound_tree(t)
        total=out.get(t,Fraction(0))+p
        if max(total.numerator.bit_length(),total.denominator.bit_length())>4096:raise r.Rejection("resource: probability sum bits")
        out[t]=total


def evaluate_probability(compiled: Compiled, *, max_outcomes: int=10000) -> Distribution:
    """Exact finite denotation. Exponential support is explicitly bounded."""
    if not r._natural(max_outcomes) or max_outcomes<1:
        raise r.Rejection('max_outcomes must be a positive integer')
    budget=[r.MAX_NODES]
    def go(c: Compiled,h: int) -> Distribution:
        budget[0]-=1
        if h>r.MAX_DEPTH or budget[0]<0: raise r.Rejection('compiled effect resource limit')
        if type(c) is not tuple or not c: raise r.Rejection('invalid compiled effect')
        if len(c)==2 and c[0]=='pure': return {_program(c[1]):Fraction(1)}
        out={}
        if len(c)==4 and c[0]=='mix':
            q=c[1]
            if type(q) is not Fraction or not 0<=q<=1: raise r.Rejection('invalid compiled probability')
            for t,p in go(c[2],h+1).items(): _add(out,t,q*p)
            for t,p in go(c[3],h+1).items(): _add(out,t,(1-q)*p)
        elif len(c)==3 and c[0]=='app':
            fs,xs=go(c[1],h+1),go(c[2],h+1)
            if len(fs)*len(xs)>max_outcomes: raise r.Rejection('application support bound exceeded')
            for f,p in fs.items():
                for x,q in xs.items(): _add(out,app(f,x),p*q)
        else: raise r.Rejection('invalid compiled operation')
        if len(out)>max_outcomes: raise r.Rejection('outcome bound exceeded')
        if sum(out.values(),Fraction(0))!=1: raise AssertionError('probability mass was not preserved')
        return out
    return go(compiled,0)


def normalise_probability(dist: Distribution, fuel: int=10000) -> Distribution:
    if not dist or any(type(p) is not Fraction or p<=0 for p in dist.values()):
        raise r.Rejection('expected a positive finite-support distribution')
    if sum(dist.values(),Fraction(0))!=1: raise r.Rejection('mass must equal one')
    out={}
    for t,p in dist.items():
        nf,_=r.normalize(t,fuel)
        _add(out,nf,p)
    return out


def saturated_masks(n: int, edges: Iterable[tuple[int,int]]) -> list[int]:
    if not r._natural(n) or n>20: raise r.Rejection('finite carrier size must be 0..20')
    es=list(edges)
    if any(not (r._natural(a) and r._natural(b) and a<n and b<n) for a,b in es):
        raise r.Rejection('edge outside finite carrier')
    return [m for m in range(1<<n) if all(((m>>a)&1)==((m>>b)&1) for a,b in es)]


def best_observation_approximation(observations: Sequence[Hashable], values: Sequence[Fraction]) -> tuple[dict[Hashable,Fraction],Fraction]:
    if len(observations)!=len(values) or not values or any(type(x) is not Fraction for x in values):
        raise r.Rejection('nonempty equal-length observations and exact Fraction values required')
    cells={}
    for o,v in zip(observations,values): cells.setdefault(o,[]).append(v)
    pred={o:(min(vs)+max(vs))/2 for o,vs in cells.items()}
    error=max(abs(v-pred[o]) for o,v in zip(observations,values))
    return pred,error


def named_instantiate(body: Any, argument: Any) -> TypeCode:
    """Independent substitution via unique names, not index shifting."""
    body,argument=r._freeze(body),r._freeze(argument)
    r._wf_type(body,None); r._wf_type(argument,None)
    serial=[0]
    def named(t: TypeCode,env: list[int]) -> tuple:
        if t[0]=='v':
            n=t[1]
            return ('bound',env[n]) if n<len(env) else ('free',n-len(env))
        if t[0]=='bottom': return t
        if t[0]=='arr': return ('arr',named(t[1],env),named(t[2],env))
        serial[0]+=1; name=serial[0]
        return ('forall',name,named(t[1],[name]+env))
    nb,na=named(body,[0]),named(argument,[])
    def replace(t: tuple) -> tuple:
        if t==('bound',0): return na
        if t[0]=='arr': return ('arr',replace(t[1]),replace(t[2]))
        if t[0]=='forall': return ('forall',t[1],replace(t[2]))
        return t
    def indexed(t: tuple,env: list[int]) -> tuple:
        if t[0]=='free': return ('v',t[1]+len(env))
        if t[0]=='bound': return ('v',env.index(t[1]))
        if t[0]=='bottom': return t
        if t[0]=='arr': return ('arr',indexed(t[1],env),indexed(t[2],env))
        return ('all',indexed(t[2],[t[1]]+env))
    return indexed(replace(nb),[])


def eval_type(t: TypeCode,env: Sequence[int],application: Sequence[int],n: int) -> int:
    """Finite algebra interpretation for bounded substitution tests only.

    Codes are all subset masks; these finite application algebras are NOT
    claimed to realise I/K/S or to model the full infinite program universe.
    """
    def go(a: TypeCode,rho: tuple[int,...]) -> int:
        if a[0]=='v': return rho[a[1]]
        if a[0]=='bottom': return 0
        if a[0]=='arr':
            dom,cod=go(a[1],rho),go(a[2],rho)
            return sum(1<<f for f in range(n) if all(
                not ((dom>>x)&1) or ((cod>>application[f*n+x])&1)
                for x in range(n)))
        if a[0]=='all':
            ans=(1<<n)-1
            for x in range(1<<n): ans &= go(a[1],(x,)+rho)
            return ans
        raise r.Rejection('invalid finite-model type')
    return go(t,tuple(env))


def threshold_allows(outcome: Fraction, threshold: Fraction, response: Fraction) -> bool:
    if not all(type(v) is Fraction and 0<=v<=1 for v in (outcome,threshold,response)):
        raise r.Rejection('threshold comparison needs exact probabilities')
    return (response==1 if outcome>threshold else response==0 if outcome<threshold else True)


def quadratic_response(p: Fraction) -> Fraction:
    """Outcome probability: a fair bit AND NOT(two independent p-bits).

    The fixed point solves p = (1-p*p)/2, hence p = sqrt(2)-1 on [0,1].
    This is distributional self-consistency, not a theorem of iteration or
    proof reflection. The exact fixed point is not a finite rational mixture.
    """
    if type(p) is not Fraction or not 0 <= p <= 1:
        raise r.Rejection('response parameter must be an exact probability')
    return (1-p*p)/2


def irrational_selector_prefix(bits: Sequence[int]) -> int | None:
    """Finite execution prefix of an exact fair-coin selector sampler.

    Returns 0 for the first selector K, 1 for the second selector K I, or None
    when the supplied random prefix has not yet settled the comparison. This
    finite routine does NOT assert total termination on every infinite stream.
    For i.i.d. fair bits the unique unresolved dyadic cell has mass 2**(-n),
    so the productive stream algorithm terminates almost surely, uses exactly
    two fair bits in expectation, and chooses K with probability sqrt(2)-1.
    All comparisons are integers: sign(k*k + 2*k*d - d*d) compares k/d to
    sqrt(2)-1. No float, sqrt approximation, or irrational coin primitive.
    """
    if type(bits) not in (tuple,list) or len(bits)>10000 or any(type(b) is not int or b not in (0,1) for b in bits):
        raise r.Rejection('a bounded sequence of literal fair bits is required')
    k,d=0,1
    for bit in bits:
        k,d=2*k+bit,2*d
        upper=k+1
        if upper*upper+2*upper*d-d*d < 0:
            return 0
        if k*k+2*k*d-d*d > 0:
            return 1
    return None


def irrational_prefix_mass(depth: int) -> dict[str,Fraction | int]:
    """Exact n-bit truncation certificate without enumerating 2**n paths.

    The unresolved cell index k=floor((sqrt(2)-1)*2**n) is obtained by exact
    integer square root. Return unconditional masses already decided by n
    bits, and the still unresolved mass. This includes early stopping paths.
    """
    from math import isqrt
    if not r._natural(depth) or depth>10000:
        raise r.Rejection('prefix depth must be an integer in 0..10000')
    d=1<<depth
    k=isqrt(2*d*d)-d
    if not k*k+2*k*d-d*d < 0:raise RuntimeError("sampler lower bound")
    if not (k+1)*(k+1)+2*(k+1)*d-d*d > 0:raise RuntimeError("sampler upper bound")
    return {'first':Fraction(k,d), 'second':Fraction(d-k-1,d),
            'unresolved':Fraction(1,d), 'cell_index':k, 'depth':depth}
