#!/usr/bin/env python3
"""Bounded independent calculation on two exact exported SKI trees.

This is a review diagnostic, not a Lean kernel proof or a general calculus model.
Source syntax is exported by DumpExactPolynomials.lean. De Bruijn indices make
alpha-equivalence structural; capture-avoiding beta and eta contraction follow
the standard shift/substitution equations, tested below.
"""
import hashlib
import json
import pathlib
import re

HERE = pathlib.Path(__file__).resolve().parent
V = lambda n: ('v', n)
L = lambda b: ('l', b)
A = lambda f, x: ('a', f, x)
I = L(V(0))
K = L(L(V(1)))
S = L(L(L(A(A(V(2), V(0)), A(V(1), V(0))))))


def shift(t, amount, cutoff=0):
    if t[0] == 'v':
        n = t[1] + amount if t[1] >= cutoff else t[1]
        assert n >= 0
        return V(n)
    if t[0] == 'l':
        return L(shift(t[1], amount, cutoff + 1))
    return A(shift(t[1], amount, cutoff), shift(t[2], amount, cutoff))


def subst(t, index, replacement, depth=0):
    if t[0] == 'v':
        return shift(replacement, depth) if t[1] == index + depth else t
    if t[0] == 'l':
        return L(subst(t[1], index, replacement, depth + 1))
    return A(subst(t[1], index, replacement, depth),
             subst(t[2], index, replacement, depth))


def occurs(t, index, depth=0):
    if t[0] == 'v':
        return t[1] == index + depth
    if t[0] == 'l':
        return occurs(t[1], index, depth + 1)
    return occurs(t[1], index, depth) or occurs(t[2], index, depth)


def step(t):
    if t[0] == 'a':
        if t[1][0] == 'l':
            return shift(subst(t[1][1], 0, shift(t[2], 1)), -1), 'beta'
        f, kind = step(t[1])
        if kind:
            return A(f, t[2]), kind
        x, kind = step(t[2])
        return (A(t[1], x), kind) if kind else (t, None)
    if t[0] == 'l':
        b = t[1]
        if b[0] == 'a' and b[2] == V(0) and not occurs(b[1], 0):
            return shift(b[1], -1), 'eta'
        b, kind = step(b)
        return (L(b), kind) if kind else (t, None)
    return t, None


def normalize(t):
    counts = {'beta': 0, 'eta': 0}
    for _ in range(10000):
        t, kind = step(t)
        if kind is None:
            return t, counts
        counts[kind] += 1
    raise AssertionError('Review computation exceeded its explicit fuel bound.')


def parse_ski(source):
    tokens = re.findall(r'[()]|[a-z]+[0-9]*', source)
    pos = 0

    def parse():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        if tok in ('i', 'k', 's'):
            return {'i': I, 'k': K, 's': S}[tok]
        assert tok == '(', ('Unexpected non-SKI atom or free variable', tok)
        f, x = parse(), parse()
        assert tokens[pos] == ')'
        pos += 1
        return A(f, x)

    result = parse()
    assert pos == len(tokens)
    return result


def pretty(t, names=()):
    if t[0] == 'v':
        return names[t[1]] if t[1] < len(names) else 'free' + str(t[1] - len(names))
    if t[0] == 'l':
        name = 'x' + str(len(names))
        return '(lambda ' + name + '. ' + pretty(t[1], (name,) + names) + ')'
    return '(' + pretty(t[1], names) + ' ' + pretty(t[2], names) + ')'


def expected(second):
    z = L(L(V(0)))
    pair = L(A(A(V(0), z), second))
    return L(A(A(A(V(0), I), pair), K))


tests = [
    (A(I, V(0)), V(0)),
    (A(A(K, V(0)), V(1)), V(0)),
    (A(A(A(S, V(0)), V(1)), V(2)), A(A(V(0), V(2)), A(V(1), V(2)))),
    (L(A(V(1), V(0))), V(0)),
    (A(L(L(V(1))), V(0)), L(V(1))),  # free argument stays free
    (A(L(L(V(0))), V(0)), L(V(0))),  # bound variable is not substituted
    (L(A(V(0), V(0))), L(A(V(0), V(0)))),  # invalid eta is refused
]
for source, target in tests:
    assert normalize(source)[0] == target

export = HERE / 'DumpExactPolynomials.log'
sources = [json.loads(line) for line in export.read_text().splitlines() if line.startswith('"')]
assert len(sources) == 2
expectations = [expected(L(L(V(0)))), expected(L(L(L(V(1)))))]
records = []
normal_forms = []
for name, source, target in zip(('Fp', 'Fq'), sources, expectations):
    nf, counts = normalize(parse_ski(source))
    assert nf == target, (name, pretty(nf), pretty(target))
    assert step(nf)[1] is None
    normal_forms.append(nf)
    records.append({'endpoint': name, 'exported_ski': source,
                    'contractions': counts, 'normal_form_de_bruijn': nf,
                    'normal_form': pretty(nf), 'matches_displayed_form': True,
                    'no_beta_or_eta_redex': True})
assert normal_forms[0] != normal_forms[1]
result = {'status': 'PASS: separate diagnostic, not a kernel proof',
          'export_log_sha256': hashlib.sha256(export.read_bytes()).hexdigest(),
          'normalizer_self_tests': len(tests),
          'distinct_alpha_classes': True, 'endpoints': records}
(HERE / 'LAMBDA_NORMAL_FORM_CHECK.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
