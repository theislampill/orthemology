#!/usr/bin/env python3
"""Bounded deterministic runtime comparison; not a formal refinement proof.

Usage: python check_runtime_agreement.py CHECKER.py OUTPUT_DIRECTORY
Then run the generated RuntimeAgreement.lean in an accepted Lean environment,
save stdout to lean-output.txt, and rerun with --verify-lean.
"""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import random

SEED = 151005

def lean(e):
    tag = e[0]
    if tag == 'c': return f'(.constant {e[1]})'
    if tag == 'v': return f'(.variable ⟨{e[1]}, by decide⟩)'
    name = {'add':'add', 'mul':'mul', 'if0':'ifZero'}[tag]
    return '(.' + name + ' ' + ' '.join(lean(x) for x in e[1:]) + ')'

def generate(rng, r, depth):
    if depth == 0 or rng.randrange(4) == 0:
        if r and rng.randrange(2): return ['v', rng.randrange(r)]
        return ['c', rng.choice([0, 0, 1, 2, 3, 7, 17])]
    tag = rng.choice(['add', 'mul', 'if0', 'if0'])
    return [tag] + [generate(rng, r, depth-1) for _ in range(3 if tag == 'if0' else 2)]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('checker', type=Path)
    parser.add_argument('output', type=Path)
    parser.add_argument('--verify-lean', action='store_true')
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    spec = importlib.util.spec_from_file_location('reference', args.checker)
    reference = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(reference)
    rng = random.Random(SEED)
    cases = []
    evaluated = 0
    for r in range(6):
        for i in range(120):
            a, b, c = [generate(rng,r,3) for _ in range(3)]
            kind = i % 8
            if kind == 0: e,f = a,['add',a,['c',0]]
            elif kind == 1: e,f = a,['mul',['c',1],a]
            elif kind == 2: e,f = ['add',a,b],['add',b,a]
            elif kind == 3: e,f = ['mul',a,['add',b,c]],['add',['mul',a,b],['mul',a,c]]
            elif kind == 4: e,f = ['if0',['mul',a,['c',0]],b,c],b
            elif kind == 5: e,f = ['if0',['add',a,['c',1]],b,c],c
            elif kind == 6: e,f = a,b
            else: e,f = ['if0',a,b,c],['if0',a,c,b]
            result = reference.equivalent(r,e,f)
            if kind < 6: assert result, (r,i,'manufactured identity')
            witness = reference.distinguish(r,e,f)
            assert (witness is None) == result
            if witness is not None:
                assert reference.evaluate(e,witness) != reference.evaluate(f,witness)
            if result:
                assert reference.verify_positive(reference.certify(r,e,f))
            # Direct values independently exercise normalisation on small tuples.
            for v in itertools.product(range(3), repeat=r):
                s = tuple(x != 0 for x in v)
                for expr in (e,f):
                    assert reference.evaluate(expr,v) == reference.eval_poly(reference.normalise(r,expr,s),v)
                    evaluated += 1
                if result: assert reference.evaluate(e,v) == reference.evaluate(f,v)
            cases.append({'r':r,'left':e,'right':f,'equal':result,'witness':witness})
    header = ('import IdentityChecker\nopen P01AC.RestrictedIdentity P01AC.RestrictedIdentityV2\n'
              'set_option maxRecDepth 100000\nset_option maxHeartbeats 0\n')
    source = [header]
    for n,case in enumerate(cases):
        r,e,f = case['r'],lean(case['left']),lean(case['right'])
        source.append(f'def e{n} : Expr {r} := {e}\ndef f{n} : Expr {r} := {f}\n')
        source.append(f'#eval [identityCheck e{n} f{n}, verifyCertificate e{n} f{n} (makeCertificate e{n}), verifyCertificate e{n} e{n} (makeCertificate e{n})]\n')
    source = ''.join(source)
    source_path = args.output/'RuntimeAgreement.lean'
    if args.verify_lean:
        assert source_path.read_text() == source, 'generated source changed'
        rows = [json.loads(line) for line in (args.output/'lean-output.txt').read_text().splitlines() if line.startswith('[')]
        assert len(rows) == len(cases), (len(rows),len(cases))
        for n,(row,case) in enumerate(zip(rows,cases)):
            assert row == [case['equal'],case['equal'],True], (n,row,case)
    else:
        source_path.write_text(source)
        (args.output/'cases.json').write_text(json.dumps(cases,indent=2)+'\n')
    receipt = {
        'seed':SEED,'arities':list(range(6)),'expression_pairs':len(cases),
        'equal_pairs':sum(c['equal'] for c in cases),'unequal_pairs':sum(not c['equal'] for c in cases),
        'direct_expression_evaluations':evaluated,
        'negative_witnesses_checked':sum(c['witness'] is not None for c in cases),
        'checker_sha256':hashlib.sha256(args.checker.read_bytes()).hexdigest(),
        'lean_source_sha256':hashlib.sha256(source.encode()).hexdigest(),
        'lean_runtime_rows_verified':len(cases) if args.verify_lean else 0,
        'formal_refinement_claim':False,
        'scope':'Bounded runtime agreement on deterministic generated well-formed AST pairs; no parser or wire-format correspondence theorem.'}
    (args.output/('VERIFIED_RESULT.json' if args.verify_lean else 'PREPARED_CASES.json')).write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))

if __name__ == '__main__': main()
