#!/usr/bin/env python3
"""Finite-mask coefficient certificates for the declared expression fragment.

This checks semantic equality of fragment descriptions under the proved P01AC
compilation theorem. It is NOT a current-Has identity derivation checker, and
it does not recognize arbitrary P01AC polynomials as fragment members.

Only Python's standard library is needed. Mathematical termination assumes
unbounded memory/integers; real resource exhaustion is not a negative verdict.
"""
from itertools import product
import json
import sys


def _nat(n):
    return type(n) is int and n >= 0


def validate(r, e):
    if not _nat(r):
        raise ValueError('arity must be a natural number')
    if type(e) is not list or not e or type(e[0]) is not str:
        raise ValueError('an expression must be a finite tagged JSON array')
    tag = e[0]
    if tag == 'c' and len(e) == 2 and _nat(e[1]):
        return
    if tag == 'v' and len(e) == 2 and _nat(e[1]) and e[1] < r:
        return
    if (tag in ('add', 'mul') and len(e) == 3) or (tag == 'if0' and len(e) == 4):
        for child in e[1:]:
            validate(r, child)
        return
    raise ValueError('malformed or out-of-fragment expression')


def evaluate(e, v):
    """Direct natural semantics; caller validates the expression and tuple."""
    tag = e[0]
    if tag == 'c': return e[1]
    if tag == 'v': return v[e[1]]
    if tag == 'add': return evaluate(e[1], v) + evaluate(e[2], v)
    if tag == 'mul': return evaluate(e[1], v) * evaluate(e[2], v)
    if tag == 'if0': return evaluate(e[2] if evaluate(e[1], v) == 0 else e[3], v)
    raise ValueError('unknown expression tag')


def _add(p, q):
    result = p.copy()
    for exponent, coefficient in q.items():
        result[exponent] = result.get(exponent, 0) + coefficient
    return result


def _mul(p, q):
    result = {}
    for alpha, a in p.items():
        for beta, b in q.items():
            exponent = tuple(i+j for i, j in zip(alpha, beta))
            result[exponent] = result.get(exponent, 0) + a*b
    return result


def _normalise(r, e, mask):
    tag = e[0]
    zero = (0,) * r
    if tag == 'c': return {zero: e[1]} if e[1] else {}
    if tag == 'v':
        if not mask[e[1]]: return {}
        return {tuple(int(i == e[1]) for i in range(r)): 1}
    if tag == 'add': return _add(_normalise(r,e[1],mask), _normalise(r,e[2],mask))
    if tag == 'mul': return _mul(_normalise(r,e[1],mask), _normalise(r,e[2],mask))
    if tag == 'if0':
        test = _normalise(r,e[1],mask)
        return _normalise(r, e[2] if not test else e[3], mask)
    raise ValueError('unknown expression tag')


def normalise(r, e, mask):
    validate(r, e)
    if type(mask) not in (tuple, list) or len(mask) != r or any(type(b) is not bool for b in mask):
        raise ValueError('mask must have exactly arity many Boolean entries')
    return _normalise(r,e,mask)


def eval_poly(p, v):
    total = 0
    for exponent, coefficient in p.items():
        term = coefficient
        for n, k in zip(v, exponent):
            term *= n ** k  # Includes 0**0 = 1, as polynomial evaluation requires.
        total += term
    return total


def masks(r):
    return product((False, True), repeat=r)


def grid(r, p, q, mask):
    """Positive degree+1 grid on live coordinates; zero on the other ones."""
    coordinates = []
    for i in range(r):
        d = max((alpha[i] for alpha in p.keys() | q.keys()), default=0)
        coordinates.append(range(1, d+2) if mask[i] else (0,))
    return product(*coordinates)  # product() has the one empty tuple.


def equivalent(r, e, f):
    validate(r,e); validate(r,f)
    return all(_normalise(r,e,s) == _normalise(r,f,s) for s in masks(r))


def distinguish(r, e, f):
    """Return None for equality; otherwise a checked finite-grid counterexample."""
    validate(r,e); validate(r,f)
    for s in masks(r):
        p, q = _normalise(r,e,s), _normalise(r,f,s)
        if p != q:
            for v in grid(r,p,q,s):
                if evaluate(e,v) != evaluate(f,v):
                    return v
            raise AssertionError('finite-grid separation invariant failed')
    return None


def _encode(p):
    return [[list(alpha), n] for alpha,n in sorted(p.items())]


def certify(r, e, f):
    validate(r,e); validate(r,f)
    forms = []
    for s in masks(r):
        p, q = _normalise(r,e,s), _normalise(r,f,s)
        if p != q:
            raise ValueError('expressions are unequal; no positive certificate exists')
        forms.append({'mask': list(s), 'left': _encode(p), 'right': _encode(q)})
    return {'version': 1, 'arity': r, 'left': e, 'right': f, 'normal_forms': forms}


def _json_equal(a, b):
    """Strict structural equality: Python bool is not accepted as an integer."""
    if type(a) is not type(b): return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(_json_equal(a[k],b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(_json_equal(x,y) for x,y in zip(a,b))
    return a == b


def verify_positive(certificate):
    """Recompute every mask; accept exactly canonical genuine positive evidence.

    The declared endpoints are the fragment descriptions stored in the packet.
    A consumer checking a separate claim must additionally match those endpoints
    to that claim, rather than accepting an unrelated valid certificate.
    """
    if type(certificate) is not dict: return False
    if set(certificate) != {'version','arity','left','right','normal_forms'}: return False
    try:
        expected = certify(certificate['arity'],certificate['left'],certificate['right'])
    except (ValueError, TypeError, KeyError, IndexError):
        return False
    return _json_equal(certificate, expected)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1 or argv[0] not in ('decide','certify','verify'):
        raise SystemExit('usage: certificate_checker.py decide|certify|verify < input.json')
    data = json.load(sys.stdin)
    if argv[0] == 'verify':
        result = {'accepted': verify_positive(data)}
    else:
        r,e,f = data['arity'],data['left'],data['right']
        if argv[0] == 'certify': result = certify(r,e,f)
        else:
            witness = distinguish(r,e,f)
            result = {'equal': witness is None, 'counterexample': witness}
    json.dump(result,sys.stdout,sort_keys=True,indent=2)
    print()

if __name__ == '__main__': main()
