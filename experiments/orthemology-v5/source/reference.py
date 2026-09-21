"""Reference proof checker for the finite polymorphic-combinatory source fragment.

This checks individual source derivations and computation traces. It does not
quantify over the infinite semantic Code universe, prove the metatheorems, or
replace Lean kernel checking. Only the rules listed below are accepted.
"""
from __future__ import annotations
from typing import Any
from boundaries import Rejection, bound_tree, load_json, MAX_INT_BITS

TypeCode = tuple
Program = tuple
MAX_DEPTH = 100
MAX_NODES = 20000


class FuelExhausted(RuntimeError):
    """Reduction did not reach a weak-head normal form within the given fuel."""


def _natural(n: Any) -> bool:
    return type(n) is int and n >= 0


def _freeze(value: Any, depth: int = 0, budget: list[int] | None = None) -> tuple:
    if budget is None:
        bound_tree(value)
        budget = [MAX_NODES]
    budget[0] -= 1
    if depth > MAX_DEPTH or budget[0] < 0:
        raise Rejection('expression exceeds the explicit structural resource limit')
    if not isinstance(value, (list, tuple)) or not value or type(value[0]) is not str:
        raise Rejection('an expression must be a nonempty tagged sequence')
    return tuple(_freeze(x, depth + 1, budget) if isinstance(x, (list, tuple)) else x
                 for x in value)


def _wf_type(t: tuple, depth: int | None) -> None:
    tag = t[0]
    if tag == 'v' and len(t) == 2 and _natural(t[1]) and (depth is None or t[1] < depth):
        return
    if tag == 'bottom' and len(t) == 1:
        return
    if tag == 'arr' and len(t) == 3 and all(isinstance(a, tuple) for a in t[1:]):
        _wf_type(t[1], depth); _wf_type(t[2], depth)
        return
    if tag == 'all' and len(t) == 2 and isinstance(t[1], tuple):
        _wf_type(t[1], None if depth is None else depth + 1)
        return
    raise Rejection(f'ill-scoped or malformed type at depth {depth}: {t!r}')


def _wf_program(t: tuple) -> None:
    if t in [('i',), ('k',), ('s',), ('zero',), ('one',)]:
        return
    if len(t) == 3 and t[0] == 'app' and all(isinstance(a, tuple) for a in t[1:]):
        _wf_program(t[1]); _wf_program(t[2]); return
    raise Rejection(f'malformed program: {t!r}')


def shift_type(t: Any, amount: int, cutoff: int = 0) -> TypeCode:
    """Capture-avoiding de Bruijn shift; validates structural tags and indices."""
    if type(amount) is not int or amount.bit_length()>MAX_INT_BITS or not _natural(cutoff) or cutoff>MAX_NODES:
        raise Rejection('shift parameters must be integers with nonnegative cutoff')
    t = _freeze(t)
    _wf_type(t, None)
    def go(a: tuple, c: int) -> tuple:
        if len(a) == 2 and a[0] == 'v' and _natural(a[1]):
            n = a[1] + amount if a[1] >= c else a[1]
            if n < 0:
                raise Rejection('de Bruijn shift underflow')
            return ('v', n)
        if len(a) == 1 and a[0] == 'bottom':
            return a
        if len(a) == 3 and a[0] == 'arr':
            return ('arr', go(a[1], c), go(a[2], c))
        if len(a) == 2 and a[0] == 'all':
            return ('all', go(a[1], c + 1))
        raise Rejection('malformed type during shifting')
    result=go(t,cutoff)
    bound_tree(result)
    return result


def instantiate_type(body: Any, argument: Any) -> TypeCode:
    """Capture-avoiding substitution with a construction-time output budget.

    Charge each occurrence of a substituted subtree BEFORE allocating its shifted
    copy. A final validator alone would allow work proportional to an oversized
    output before noticing it exceeds the public contract.
    """
    body, argument = _freeze(body), _freeze(argument)
    _wf_type(body, None); _wf_type(argument, None)
    remaining = [MAX_NODES]
    argument_nodes = bound_tree(argument)
    def charge(n: int) -> None:
        remaining[0] -= n
        if remaining[0] < 0:
            raise Rejection('resource: substitution output construction budget')
    def go(t: tuple, binders: int) -> tuple:
        if t[0] == 'v':
            n = t[1]
            if n == binders:
                charge(argument_nodes)
                return shift_type(argument, binders)
            charge(3)
            return ('v', n - 1 if n > binders else n)
        if t == ('bottom',):
            charge(2);return t
        if t[0] == 'arr':
            charge(2);return ('arr', go(t[1], binders), go(t[2], binders))
        if t[0] == 'all':
            charge(2);return ('all', go(t[1], binders + 1))
        raise Rejection('malformed type during instantiation')
    result=go(body,0)
    bound_tree(result)
    return result


def _head_step(t: Program) -> Program | None:
    if t[0] != 'app':
        return None
    f, x = t[1], t[2]
    if f == ('i',):
        return x
    if f[0] == 'app' and f[1] == ('k',):
        return f[2]
    if (f[0] == 'app' and f[1][0] == 'app' and f[1][1] == ('s',)):
        return ('app', ('app', f[1][2], x), ('app', f[2], x))
    new_f = _head_step(f)
    return None if new_f is None else ('app', new_f, x)


def head_step(term: Any) -> Program | None:
    term = _freeze(term); _wf_program(term)
    out=_head_step(term)
    return None if out is None else _freeze(out)


def normalize(term: Any, fuel: int = 10000) -> tuple[Program, list[Program]]:
    """Weak-head reduction, not full normalization or a termination assertion."""
    if not _natural(fuel) or fuel>MAX_NODES:
        raise Rejection('fuel must be a nonnegative integer, not Boolean')
    term = _freeze(term); _wf_program(term)
    trace = [term]
    work=[200000]
    bound_tree(term,work=work)
    for used in range(fuel + 1):
        next_term = _head_step(term)
        if next_term is None:
            return term, trace
        if used == fuel:
            raise FuelExhausted(f'weak-head reduction exhausted {fuel} steps')
        bound_tree(next_term,work=work)
        term = _freeze(next_term)
        trace.append(term)
    raise AssertionError('unreachable')


def check(proof: Any, type_depth: int = 0) -> tuple[Program, TypeCode]:
    """Validate a proof tree, returning its erased program and internal type code.

    all_i checks ONE body proof under an additional type variable. all_e permits
    any well-scoped code, including the polymorphic code being instantiated.
    There is no rule for arbitrary code-dependent families, admission markers,
    externally supplied semantic truths, or unrestricted untyped evaluation.
    """
    if not _natural(type_depth) or type_depth>MAX_DEPTH:
        raise Rejection('type depth must be a nonnegative integer')
    bound_tree(proof)
    budget = [MAX_NODES]
    work=[2000000]
    def go(p: Any, d: int, height: int) -> tuple[Program, TypeCode]:
        result=raw_go(p,d,height)
        for part in result:bound_tree(part,work=work)
        return result
    def raw_go(p: Any, d: int, height: int) -> tuple[Program, TypeCode]:
        budget[0] -= 1
        if height > MAX_DEPTH or budget[0] < 0:
            raise Rejection('proof exceeds the explicit structural resource limit')
        if type(p) is not dict or type(p.get('rule')) is not str:
            raise Rejection('proof node must be a dictionary with a named rule')
        rule = p['rule']
        def fields(*names: str) -> None:
            if set(p) != {'rule', *names}:
                raise Rejection(f'incorrect fields for rule {rule}')
        def typ(name: str) -> TypeCode:
            t = _freeze(p[name]); _wf_type(t, d); return t
        def arr(a: tuple, b: tuple) -> tuple:
            return ('arr', a, b)
        if rule == 'i':
            fields('A'); a = typ('A')
            return ('i',), arr(a, a)
        if rule == 'k':
            fields('A','B'); a,b=typ('A'),typ('B')
            return ('k',), arr(a,arr(b,a))
        if rule == 's':
            fields('A','B','C'); a,b,c=typ('A'),typ('B'),typ('C')
            return ('s',), arr(arr(a,arr(b,c)),arr(arr(a,b),arr(a,c)))
        if rule == 'app':
            fields('function','argument')
            f,ft=go(p['function'],d,height+1)
            x,xt=go(p['argument'],d,height+1)
            if ft[0] != 'arr' or ft[1] != xt:
                raise Rejection('application requires exactly the argument domain')
            return ('app',f,x),ft[2]
        if rule == 'all_i':
            fields('body')
            t,body=go(p['body'],d+1,height+1)
            return t,('all',body)
        if rule == 'all_e':
            fields('polymorphic','type')
            t,pt=go(p['polymorphic'],d,height+1)
            a=typ('type')
            if pt[0] != 'all':
                raise Rejection('type application requires a polymorphic type')
            result=instantiate_type(pt[1],a); _wf_type(result,d)
            return t,result
        if rule == 'reduce':
            fields('proof','trace')
            start,ty=go(p['proof'],d,height+1)
            trace=p['trace']
            if type(trace) not in (list,tuple) or not trace or len(trace)>MAX_NODES:
                raise Rejection('reduction trace must be a bounded nonempty sequence')
            trace=[_freeze(t) for t in trace]
            for t in trace: _wf_program(t)
            if trace[0] != start:
                raise Rejection('reduction trace does not start at the proved program')
            for left,right in zip(trace,trace[1:]):
                if _head_step(left) != right:
                    raise Rejection('invalid computation step')
            return trace[-1],ty
        raise Rejection(f'unknown rule: {rule}')
    return go(proof,type_depth,0)


def check_json(raw:bytes,type_depth:int=0)->tuple[Program,TypeCode]:
    return check(load_json(raw),type_depth)
