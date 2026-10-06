#!/usr/bin/env python3
"""Reference comparison of source-presented one-variable root extensions.

Import certificate_checker from the separately supplied restricted reference.
This implementation is tested reference code, not a kernel refinement theorem.
Inputs have tags ['old', expression] or ['test', pure_expression, pure_expression].
All source expressions have arity one. No new nested equality tests are allowed.
"""
import certificate_checker as restricted


def _pure(e):
    restricted.validate(1,e)
    if e[0] not in ('c','v','add','mul'):
        raise ValueError('test comparands must be pure arithmetic')
    if e[0] in ('add','mul'):
        _pure(e[1]); _pure(e[2])


def validate(s):
    if type(s) is not list or not s or type(s[0]) is not str:
        raise ValueError('root expression must be a tagged array')
    if s[0] == 'old' and len(s) == 2:
        restricted.validate(1,s[1])
    elif s[0] == 'test' and len(s) == 3:
        _pure(s[1]); _pure(s[2])
    else:
        raise ValueError('unknown or malformed root expression')


def _difference(p,q):
    keys = p.keys() | q.keys()
    return {k:p.get(k,0)-q.get(k,0) for k in keys if p.get(k,0)!=q.get(k,0)}


def root_bound(p):
    """Nonzero integer polynomial cannot vanish at n >= this bound.

    The zero polynomial is assigned 1 for bookkeeping only; it has no
    nonvanishing assertion. Exponent keys are validated nonnegative integers.
    """
    if type(p) is not dict or any(type(k) is not int or k<0 or type(v) is not int for k,v in p.items()):
        raise ValueError('expected finite integer coefficient map')
    p = {k:v for k,v in p.items() if v}
    if not p or max(p)==0: return 1
    degree = max(p)
    return 1+sum(abs(v) for k,v in p.items() if k<degree)


def _positive_polynomial(e):
    return {alpha[0]:value for alpha,value in restricted.normalise(1,e,[True]).items() if value}


def tail(s):
    validate(s)
    if s[0] == 'old': return 1,_positive_polynomial(s[1])
    d = _difference(_positive_polynomial(s[1]),_positive_polynomial(s[2]))
    return (root_bound(d),{}) if d else (1,{0:1})


def evaluate(s,n):
    validate(s)
    if type(n) is not int or n<0: raise ValueError('input must be natural')
    if s[0] == 'old': return restricted.evaluate(s[1],(n,))
    return int(restricted.evaluate(s[1],(n,)) == restricted.evaluate(s[2],(n,)))


def comparison_bound(s,t):
    bs,ps = tail(s)
    bt,pt = tail(t)
    return max(bs,bt,root_bound(_difference(ps,pt)))


def distinguish(s,t):
    """Return a checked natural counterexample, or None for universal equality.

    Equal tails require a finite prefix check. Different tails give the bound
    itself as a guaranteed witness. This does not claim the least witness.
    """
    bs,ps = tail(s)
    bt,pt = tail(t)
    d = _difference(ps,pt)
    if d:
        n = max(bs,bt,root_bound(d))
        if evaluate(s,n)==evaluate(t,n): raise AssertionError('tail separation failed')
        return n
    for n in range(max(bs,bt)):
        if evaluate(s,n)!=evaluate(t,n): return n
    return None


def equivalent(s,t):
    return distinguish(s,t) is None
