#!/usr/bin/env python3
"""Bounded complete-development producer plus separate finite address checker.

Input is the actual P01D.Poly constructor tree: var/atom/app; an atom holds an
actual OrthemologyV2.Term tree (i/k/s/zero/one/app). Variables are never inserted
inside Term atoms. originalQ is exported by Lean from its frozen source symbol.
The producer does not typecheck HasE. Its output certifies concrete conversion
only; a Lean HasE premise is a separate obligation. Exhaustion is inconclusive.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
CONSTANTS = {'i', 'k', 's', 'zero', 'one'}
SCHEMA = 'source-poly-open-ski-address-v1'


def canonical(value):
    return json.dumps(value, separators=(',', ':'), ensure_ascii=True)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def _node(value):
    if type(value) is not list or not value or type(value[0]) is not str:
        raise ValueError('constructor must be a nonempty JSON list')
    return value[0]


def validate_term(value):
    tag = _node(value)
    if tag in CONSTANTS and len(value) == 1:
        return value
    if tag == 'app' and len(value) == 3:
        validate_term(value[1]); validate_term(value[2]); return value
    raise ValueError('invalid literal Term constructor')


def validate_poly(value):
    tag = _node(value)
    if tag == 'var' and len(value) == 2 and type(value[1]) is int and value[1] >= 0:
        return value
    if tag == 'atom' and len(value) == 2:
        validate_term(value[1]); return value
    if tag == 'app' and len(value) == 3:
        validate_poly(value[1]); validate_poly(value[2]); return value
    raise ValueError('invalid literal Poly constructor')


def validate_open(value):
    tag = _node(value)
    if tag in CONSTANTS and len(value) == 1:
        return value
    if tag == 'var' and len(value) == 2 and type(value[1]) is int and value[1] >= 0:
        return value
    if tag == 'app' and len(value) == 3:
        validate_open(value[1]); validate_open(value[2]); return value
    raise ValueError('invalid open T constructor')


def freeze(value):
    return tuple(freeze(v) if type(v) is list else v for v in value)


def thaw(value):
    return [thaw(v) if type(v) is tuple else v for v in value]


def interpret(poly):
    """Literal mirror of ImportedOpenTermTransport.interp at T.var."""
    validate_poly(poly)
    def go(p):
        if p[0] == 'atom': return freeze(p[1])
        if p[0] == 'var': return ('var', p[1])
        return ('app', go(p[1]), go(p[2]))
    return go(poly)


def pack_closed(poly):
    """Expose a fixture's closed raw tree; the returned Poly atom is not hidden."""
    validate_poly(poly)
    if poly[0] == 'var': raise ValueError('cannot pack an open polynomial')
    if poly[0] == 'atom': return poly[1]
    return ['app', pack_closed(poly[1]), pack_closed(poly[2])]


SOURCE = json.loads((HERE / 'source_ast.json').read_text())
ORIGINAL_Q = validate_poly(SOURCE['originalQ'])
Q_DIGEST = digest(ORIGINAL_Q)


def endpoints(n):
    # Preserve all source atom/application boundaries before interpretation.
    return (['app', ['app', n, ['var', 1]], ['var', 0]],
            ['app', ['app', ['app', ORIGINAL_Q, n], ['var', 1]], ['var', 0]])


def iteration(k):
    result = ('var', 0)
    for _ in range(k): result = ('app', ('var', 1), result)
    return result


def iteration_count(t):
    k = 0
    while t[0] == 'app' and t[1] == ('var', 1):
        k += 1; t = t[2]
    return k if t == ('var', 0) else None


class Exhausted(Exception):
    pass


class Budget:
    def __init__(self, max_steps, max_nodes):
        self.steps = 0
        self.max_steps = max_steps
        self.max_nodes = max_nodes
    def emit(self, paths, path):
        if self.steps >= self.max_steps: raise Exhausted('step budget')
        self.steps += 1; paths.append(path)
    def size(self, t):
        stack = [t]; n = 0
        while stack:
            v = stack.pop(); n += 1
            if n > self.max_nodes: raise Exhausted('node budget')
            if v[0] == 'app': stack.extend((v[1], v[2]))


def develop(t, budget):
    """One Takahashi complete development, with its finite compatible steps.

    The root pattern is inspected BEFORE recursive development; newly-created
    root redexes wait until the next round. K erases its unused argument first.
    This is deliberately not a normal-order or strong-normalization assertion.
    """
    trace = []
    def go(v, address):
        if v[0] != 'app': return v
        f, x = v[1], v[2]
        if f == ('i',):
            budget.emit(trace, address)
            return go(x, address)
        if f[0] == 'app' and f[1] == ('k',):
            budget.emit(trace, address)
            return go(f[2], address)
        if f[0] == 'app' and f[1][0] == 'app' and f[1][1] == ('s',):
            a = go(f[1][2], address + 'LLR')
            b = go(f[2], address + 'LR')
            c = go(x, address + 'R')
            budget.emit(trace, address)
            return ('app', ('app', a, c), ('app', b, c))
        a = go(f, address + 'L')
        b = go(x, address + 'R')
        return ('app', a, b)
    result = go(t, '')
    budget.size(result)
    return result, trace


# Checker below does not call develop, simulate rounds, or trust producer outputs.
def _contract_checked(t):
    if t[0] != 'app': raise ValueError('address is not a redex')
    left, arg = t[1:]
    if left == ('i',): return arg
    if left[0] == 'app':
        head, a = left[1:]
        if head == ('k',): return a
        if head[0] == 'app' and head[1] == ('s',):
            return ('app', ('app', head[2], arg), ('app', a, arg))
    raise ValueError('address is not an SKI redex')


def check_step_at(t, address):
    if type(address) is not str or any(c not in 'LR' for c in address):
        raise ValueError('invalid address alphabet')
    frames = []
    current = t
    for c in address:
        if current[0] != 'app': raise ValueError('address descends through a leaf')
        frames.append((c, current))
        current = current[1 if c == 'L' else 2]
    current = _contract_checked(current)
    for c, before in reversed(frames):
        current = ('app', current, before[2]) if c == 'L' else ('app', before[1], current)
    return current


def replay_checked(t, trace):
    if type(trace) is not list: raise ValueError('trace must be a list')
    for path in trace: t = check_step_at(t, path)
    return t


def is_normal(t):
    stack = [t]
    while stack:
        v = stack.pop()
        try: _contract_checked(v)
        except ValueError: pass
        else: return False
        if v[0] == 'app': stack.extend((v[1], v[2]))
    return True


def check_certificate(cert, expected_input=None):
    """Pure finite checker, independent of the complete-development producer.

    expected_input binds a caller's intended source. The Lean checker further
    uses literal originalQ, so editing the exported q cannot forge kernel proof.
    """
    try:
        if type(cert) is not dict or set(cert) != {'schema', 'input', 'original_q_sha256', 'count', 'left', 'right'}:
            return False
        if cert['schema'] != SCHEMA or cert['original_q_sha256'] != Q_DIGEST: return False
        n = validate_poly(cert['input'])
        if expected_input is not None and n != validate_poly(expected_input): return False
        k = cert['count']
        if type(k) is not int or k < 0: return False
        for side, source in zip(('left', 'right'), endpoints(n)):
            data = cert[side]
            if type(data) is not dict or set(data) != {'start', 'endpoint', 'steps', 'trace'}: return False
            validate_open(data['start']); validate_open(data['endpoint'])
            if type(data['steps']) is not int or data['steps'] != len(data['trace']): return False
            start = interpret(source)
            expected = freeze(data['endpoint'])
            if freeze(data['start']) != start or iteration_count(expected) != k: return False
            if replay_checked(start, data['trace']) != expected: return False
        return True
    except (ValueError, TypeError, KeyError, IndexError):
        return False


def _diagnose(n, max_rounds=500, max_steps=100000, max_nodes=200000):
    validate_poly(n)
    if any(type(x) is not int or x < 0 for x in (max_rounds, max_steps, max_nodes)):
        raise ValueError('budgets must be natural numbers')
    starts = [interpret(v) for v in endpoints(n)]
    current = starts[:]; traces = [[], []]; rounds = [0, 0]
    counts = [None, None]
    budget = Budget(max_steps, max_nodes)
    try:
        for side in range(2):
            budget.size(current[side])
            for round_index in range(max_rounds + 1):
                count = iteration_count(current[side])
                if count is not None:
                    counts[side] = count; break
                if is_normal(current[side]):
                    return {'status': 'normal_non_iteration', 'side': ['left', 'right'][side],
                            'endpoint': thaw(current[side]), 'meaning': 'No iteration certificate for this syntax; no HasE typing claim.'}
                if round_index == max_rounds: raise Exhausted('round budget')
                current[side], paths = develop(current[side], budget)
                traces[side].extend(paths); rounds[side] += 1
        if counts[0] != counts[1]:
            return {'status': 'different_iteration_endpoints', 'counts': counts,
                    'meaning': 'No scalar certificate produced; no general inequivalence decision.'}
        cert = {'schema': SCHEMA, 'input': n, 'original_q_sha256': Q_DIGEST,
                'count': counts[0]}
        for j, side in enumerate(('left', 'right')):
            cert[side] = {'start': thaw(starts[j]), 'endpoint': thaw(current[j]),
                          'steps': len(traces[j]), 'trace': traces[j]}
        if not check_certificate(cert, expected_input=n):
            raise RuntimeError('independent certificate checker rejected producer output')
        return {'status': 'certified_conversion', 'certificate': cert,
                'complete_development_rounds': rounds,
                'meaning': 'Concrete source PolyConvPlus conversion only. HasE typing is not inferred.'}
    except (Exhausted, RecursionError) as exc:
        return {'status': 'budget_exhausted', 'outcome': 'RESOURCE_INCONCLUSIVE', 'reason': str(exc), 'rounds': rounds,
                'steps': budget.steps, 'meaning': 'Inconclusive; neither inequivalence nor a typing failure.'}


def diagnose(n, max_rounds=500, max_steps=100000, max_nodes=200000):
    # Includes source validation/interpretation and certificate serialization in
    # the host-resource boundary; malformed finite constructors remain errors.
    try:
        return _diagnose(n, max_rounds, max_steps, max_nodes)
    except (RecursionError, MemoryError) as exc:
        return {'status': 'budget_exhausted', 'outcome': 'RESOURCE_INCONCLUSIVE', 'reason': type(exc).__name__,
                'meaning': 'Host resource exhaustion; inconclusive, never inequivalence or nonderivability.'}


def lean_poly(p):
    validate_poly(p)
    def term(t):
        if t[0] == 'app': return f'(.app {term(t[1])} {term(t[2])})'
        return '.' + t[0]
    def poly(v):
        if v[0] == 'var': return f'(.var {v[1]})'
        if v[0] == 'atom': return f'(.atom {term(v[1])})'
        return f'(.app {poly(v[1])} {poly(v[2])})'
    return poly(p)


def lean_paths(paths):
    # No external string is emitted as Lean source, only a fixed constructor.
    if type(paths) is not list: raise ValueError('invalid trace')
    for p in paths:
        if type(p) is not str or any(c not in 'LR' for c in p): raise ValueError('invalid path')
    return '[' + ','.join('[' + ','.join('.left' if c == 'L' else '.right' for c in p) + ']' for p in paths) + ']'


def closed_poly(p):
    validate_poly(p)
    stack = [p]
    while stack:
        v = stack.pop()
        if v[0] == 'var': return False
        if v[0] == 'app': stack.extend(v[1:])
    return True


def lean_certificate(cert, name='certificate'):
    if not check_certificate(cert): raise ValueError('refuse invalid certificate')
    if not name.isidentifier() or not name.isascii(): raise ValueError('invalid fixed declaration name')
    k = cert['count']
    output = (f'def {name}_n : P01D.Poly := {lean_poly(cert["input"])}\n'
              f'def {name}_l : List P01Certificate.Address := {lean_paths(cert["left"]["trace"])}\n'
              f'def {name}_r : List P01Certificate.Address := {lean_paths(cert["right"]["trace"])}\n'
              f'theorem {name}_iteration : P01AC.Intensional.Plus.PolyConvPlus\n'
              f'    (ClosedScalarInstances.scalarLeft {name}_n) (P01AC.EffectiveCompleteness.iterationPoly {k}) :=\n'
              f'  ScalarCertificates.checkedIteration {name}_n {k} {name}_l (by decide)\n'
              f'theorem {name}_right_iteration : P01AC.Intensional.Plus.PolyConvPlus\n'
              f'    (ClosedScalarInstances.scalarRight {name}_n) (P01AC.EffectiveCompleteness.iterationPoly {k}) :=\n'
              f'  ScalarCertificates.checkedRightIteration {name}_n {k} {name}_r (by\n'
              f'    unfold ClosedScalarInstances.scalarRight\n'
              f'    rw [ScalarCertificates.originalQ_expanded]\n'
              f'    decide)\n'
              f'theorem {name}_conversion : P01AC.Intensional.Plus.PolyConvPlus\n'
              f'    (ClosedScalarInstances.scalarLeft {name}_n) (ClosedScalarInstances.scalarRight {name}_n) :=\n'
              f'  {name}_iteration.trans {name}_right_iteration.symm\n'
              f'#print axioms {name}_conversion\n#print axioms {name}_iteration\n')
    if closed_poly(cert['input']):
        output += (f'theorem {name}_source_instance : P01AC.ExtensionalRepair.HasE []\n'
                   f'    (.app P01AC.ExtensionalRepair.ExactScalarFusion.c3 {name}_n)\n'
                   f'    (P01AC.inst (.all (.pi P01AC.ExtensionalRepair.ExactScalarFusion.End\n'
                   f'      (.pi P01AC.ExtensionalRepair.ExactScalarFusion.A\n'
                   f'        (P01AC.ExtensionalRepair.ExactScalarFusion.Leaf FullPER.Application.originalQ)))) {name}_n) :=\n'
                   f'  ScalarCertificates.exactSourceInstanceFromConversions\n'
                   f'    (by simp [P01AC.Scoped, {name}_n]) {k} {name}_iteration {name}_right_iteration\n'
                   f'#print axioms {name}_source_instance\n')
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path, help='JSON source Poly or certificate with --check')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--max-rounds', type=int, default=500)
    parser.add_argument('--max-steps', type=int, default=100000)
    parser.add_argument('--max-nodes', type=int, default=200000)
    parser.add_argument('--lean-output', type=Path)
    args = parser.parse_args()
    value = json.loads(args.input.read_text())
    if args.check:
        result = {'accepted': check_certificate(value)}
    else:
        result = diagnose(value, args.max_rounds, args.max_steps, args.max_nodes)
    if args.lean_output:
        cert = value if args.check else result.get('certificate')
        if cert is None: parser.error('no certificate to replay')
        args.lean_output.write_text('import LiteralSourceQ\nset_option maxRecDepth 16384\nset_option maxHeartbeats 8000000\n' + lean_certificate(cert))
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    try:
        main()
    except (RecursionError, MemoryError) as exc:
        print(json.dumps({'status': 'budget_exhausted', 'outcome': 'RESOURCE_INCONCLUSIVE', 'reason': type(exc).__name__,
                          'meaning': 'Host resource exhaustion; inconclusive.'}))
    except (ValueError, TypeError) as exc:
        print(json.dumps({'status': 'invalid_input', 'reason': str(exc)}))
        raise SystemExit(2)

