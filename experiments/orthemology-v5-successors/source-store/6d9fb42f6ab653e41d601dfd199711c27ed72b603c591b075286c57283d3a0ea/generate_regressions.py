#!/usr/bin/env python3
"""Deterministic small-tree regressions; expected values use an independent evaluator."""
from pathlib import Path
import random
rng = random.Random(160510)

def gen(depth):
    if depth == 0:
        return ('x',) if rng.randrange(2) else ('c', rng.randrange(4))
    op = rng.choice(['add', 'mul', 'if', 'if', 'x', 'c'])
    if op == 'x': return ('x',)
    if op == 'c': return ('c', rng.randrange(4))
    return (op, *(gen(depth-1) for _ in range(4 if op == 'if' else 2)))

def value(e,n):
    if e[0]=='x': return n
    if e[0]=='c': return e[1]
    if e[0]=='add': return value(e[1],n)+value(e[2],n)
    if e[0]=='mul': return value(e[1],n)*value(e[2],n)
    return value(e[3] if value(e[1],n)==value(e[2],n) else e[4],n)

def lean(e):
    if e[0]=='x': return 'Expr.variable'
    if e[0]=='c': return f'(Expr.constant {e[1]})'
    name={'add':'add','mul':'mul','if':'ifEq'}[e[0]]
    return f'(Expr.{name} ' + ' '.join(lean(c) for c in e[1:]) + ')'

out=['/- Expected values produced by an independent finite-tree evaluator. -/',
     'import UnaryWitnesses', 'import UnaryExpressivity', 'open P01AC.UnaryIdentity',
     'set_option maxRecDepth 8192', 'set_option maxHeartbeats 2000000']
for i in range(64):
    e=gen(3)
    expr=lean(e)
    expected=str([value(e,n) for n in range(11)])
    out += [f'def regression_{i} : Expr := {expr}',
            f'example : (List.range 11).map (fun n => (normalise regression_{i}).denote n) = {expected} := by decide',
            f'example : identityCheck (.add regression_{i} (.constant 0)) regression_{i} = true := by decide',
            f'example : normalise (Expr.reify (normalise regression_{i})) = normalise regression_{i} := by decide']
Path(__file__).with_name('GeneratedUnaryRegressions.lean').write_text('\n'.join(out)+'\n')
print('Generated 64 trees, 704 direct expected values, 64 zero-addition identities, 64 canonical reification checks.')
