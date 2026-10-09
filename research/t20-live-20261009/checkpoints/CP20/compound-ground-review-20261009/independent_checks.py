#!/usr/bin/env python3
"""Independent read-only review: Hasse-edge lattice, primary table, parsed proofs.

Does not import or execute the author's checker. Only its public proof text and
reported results are loaded for comparison after independent computations.
"""
from itertools import product
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
AUTHOR = ROOT / 'compound-ground-necessity-20261009'
V = ('-3', '-2', '-1', '-0', '+0', '+1', '+2', '+3')
D = frozenset(v for v in V if v.startswith('+'))
# Transcribed from Standefer (2020), printed 271, not from the author's bit map.
COVERS = (
    ('-3', '-1'), ('-3', '+0'), ('-3', '-2'),
    ('-1', '+1'), ('-1', '-0'), ('+0', '+1'), ('+0', '+2'),
    ('-2', '-0'), ('-2', '+2'), ('+1', '+3'), ('-0', '+3'), ('+2', '+3'),
)
LE = set(COVERS) | {(v, v) for v in V}
while True:
    extended = LE | {(a, d) for a, b in LE for c, d in LE if b == c}
    if extended == LE:
        break
    LE = extended
assert all(a == b or (b, a) not in LE for a, b in LE)

def meet(a, b):
    bounds = [x for x in V if (x, a) in LE and (x, b) in LE]
    best = [x for x in bounds if all((y, x) in LE for y in bounds)]
    assert len(best) == 1
    return best[0]

def join(a, b):
    bounds = [x for x in V if (a, x) in LE and (b, x) in LE]
    best = [x for x in bounds if all((x, y) in LE for y in bounds)]
    assert len(best) == 1
    return best[0]

NEG = {'-3': '+3', '-2': '+2', '-1': '+1', '-0': '+0',
       '+0': '-0', '+1': '-1', '+2': '-2', '+3': '-3'}
# Exact row/column order as the primary Table 2.
ROW_TEXT = (
    '+3 +3 +3 +3 +3 +3 +3 +3',
    '-3 +2 -3 +2 -3 -3 +2 +3',
    '-3 -3 +1 +1 -3 +1 -3 +3',
    '-3 -3 -3 +0 -3 -3 -3 +3',
    '-3 -2 -1 -0 +0 +1 +2 +3',
    '-3 -3 -1 -1 -3 +1 -3 +3',
    '-3 -2 -3 -2 -3 -3 +2 +3',
    '-3 -3 -3 -3 -3 -3 -3 +3',
)
TABLE = dict(zip(V, [dict(zip(V, row.split())) for row in ROW_TEXT]))
def imp(a, b):
    return TABLE[a][b]

def parse(text):
    tokens = re.findall(r'→R|→|[¬∧∨()]|[A-Za-z][A-Za-z0-9_]*', text)
    pos = 0
    def take():
        nonlocal pos
        tok = tokens[pos]
        pos += 1
        if tok == '¬':
            return ('not', take())
        if tok == '(':
            left = take()
            op = {'→R': 'imp', '→': 'imp', '∧': 'and', '∨': 'or'}[tokens[pos]]
            pos += 1
            right = take()
            assert tokens[pos] == ')'
            pos += 1
            return (op, left, right)
        assert re.fullmatch(r'[A-Za-z][A-Za-z0-9_]*', tok)
        return tok
    out = take()
    assert pos == len(tokens), (text, tokens[pos:])
    return out

def variables(f):
    if isinstance(f, str):
        return {f}
    return set().union(*(variables(x) for x in f[1:]))

def value(f, assignment):
    if isinstance(f, str):
        return assignment[f]
    if f[0] == 'not':
        return NEG[value(f[1], assignment)]
    return {'and': meet, 'or': join, 'imp': imp}[f[0]](
        value(f[1], assignment), value(f[2], assignment))

# Independently transcribed Bimbo/Dunn/Ferenz 2018 pp.176-177 A1-A16.
SCHEMES = [parse(s) for s in (
    '(A → A)',
    '((A → B) → ((C → A) → (C → B)))',
    '((A → (A → B)) → (A → B))',
    '((A → (B → C)) → (B → (A → C)))',
    '((A → ((B → D) → C)) → ((B → D) → (A → C)))',
    '((A ∧ B) → A)',
    '((A ∧ B) → B)',
    '(((C → A) ∧ (C → B)) → (C → (A ∧ B)))',
    '((((A → A) ∧ (B → B)) → C) → C)',
    '(A → (A ∨ B))',
    '(A → (B ∨ A))',
    '(((A → C) ∧ (B → C)) → ((A ∨ B) → C))',
    '((A ∧ (B ∨ C)) → ((A ∧ B) ∨ (A ∧ C)))',
    '((A → ¬A) → ¬A)',
    '((A → ¬B) → (B → ¬A))',
    '(¬¬A → A)',
)]

axiom_results = []
for number, formula in enumerate(SCHEMES, 1):
    names = sorted(variables(formula))
    failures = []
    for vals in product(V, repeat=len(names)):
        a = dict(zip(names, vals))
        if value(formula, a) not in D:
            failures.append(a)
    axiom_results.append({'axiom': number, 'assignments': 8 ** len(names), 'failures': failures})
assert not any(r['failures'] for r in axiom_results)
mp_fail = [(a, b) for a, b in product(V, repeat=2) if a in D and imp(a, b) in D and b not in D]
adj_fail = [(a, b) for a, b in product(V, repeat=2) if a in D and b in D and meet(a, b) not in D]
assert not mp_fail and not adj_fail

# Structural/source consistency, rather than just reproducing target numbers.
assert all(NEG[NEG[x]] == x for x in V)
assert all(join(a, b) == NEG[meet(NEG[a], NEG[b])] for a, b in product(V, repeat=2))
assert all((meet(a, b) in D) == (a in D and b in D) for a, b in product(V, repeat=2))
assert all((join(a, b) in D) == (a in D or b in D) for a, b in product(V, repeat=2))
assert all((NEG[a] in D) != (a in D) for a in V)

forms = {k: parse(s) for k, s in {
    'P': 'P', 'N': '(Q → Q)', 'not_P': '¬P', 'not_N': '¬(Q → Q)',
    'M': '(¬P ∨ (Q → Q))',
    'B': '(P ∧ (¬P ∨ (Q → Q)))',
    'not_M': '¬(¬P ∨ (Q → Q))',
    'not_B': '¬(P ∧ (¬P ∨ (Q → Q)))',
    'B_arrow_N': '((P ∧ (¬P ∨ (Q → Q))) → (Q → Q))',
    'sensitivity_B': '(¬(Q → Q) → ¬(P ∧ (¬P ∨ (Q → Q))))',
    'sensitivity_P': '(¬(Q → Q) → ¬P)',
    'sensitivity_M': '(¬(Q → Q) → ¬(¬P ∨ (Q → Q)))',
    'C': '(P ∧ ¬P)',
    'C_arrow_B': '((P ∧ ¬P) → (P ∧ (¬P ∨ (Q → Q))))',
    'C_arrow_N': '((P ∧ ¬P) → (Q → Q))',
    'relevant_conditional': '(P → (Q → Q))',
    'relevant_compound': '(P ∧ (P → (Q → Q)))',
    'relevant_compound_arrow_N': '((P ∧ (P → (Q → Q))) → (Q → Q))',
    'relevant_compound_sensitivity': '(¬(Q → Q) → ¬(P ∧ (P → (Q → Q))))',
    'add_target': '((P ∧ (¬P ∨ (Q → Q))) ∧ (Q → Q))',
    'add_noncontradiction': '((P ∧ (¬P ∨ (Q → Q))) ∧ ¬(P ∧ ¬P))',
    'classically_equivalent_P_and_N': '(P ∧ (Q → Q))',
}.items()}
witness_assignment = {'P': '+1', 'Q': '+2'}
witness = {k: value(f, witness_assignment) for k, f in forms.items()}
assert all(witness[k] in D for k in ('P', 'N', 'M', 'B'))
assert all(witness[k] not in D for k in ('not_P', 'not_N', 'not_M', 'not_B', 'B_arrow_N', 'sensitivity_B'))
assert witness['B_arrow_N'] == witness['sensitivity_B'] == '-3'

all_assignments = []
for p, q in product(V, repeat=2):
    a = {'P': p, 'Q': q}
    vals = {k: value(f, a) for k, f in forms.items()}
    assert vals['N'] in D and vals['not_N'] not in D
    assert vals['relevant_compound_arrow_N'] in D
    assert vals['relevant_compound_sensitivity'] in D
    all_assignments.append({'assignment': a, **vals})
material_actual = [r for r in all_assignments if r['P'] in D and r['M'] in D]
material_failures = [r for r in material_actual if r['sensitivity_B'] not in D]
assert material_failures

# Strongest immediate repair: retain the whole compound and test all 32
# designated P / theorem N cases; also test what adding a target or an
# independently supplied relevant conditional changes at the witness.
repair_values = {}
for key in ('B', 'P', 'M', 'add_target', 'add_noncontradiction', 'classically_equivalent_P_and_N', 'relevant_compound'):
    b = witness[key]
    repair_values[key] = {'ground': b, 'ground_designated': b in D,
                         'arrow_to_N': imp(b, witness['N']),
                         'sensitivity': imp(NEG[witness['N']], NEG[b])}

# Counterexample persists under redundant regrouping/repetition of the full
# material premises, but adding N changes the epistemic ground.
assert meet(witness['B'], witness['M']) == witness['B']
assert meet(witness['B'], witness['P']) == witness['B']
assert repair_values['add_noncontradiction']['sensitivity'] not in D
assert repair_values['add_target']['sensitivity'] in D
assert repair_values['relevant_compound']['ground_designated'] is False

# Classical entailment remains intact: material modus ponens over placeholders
# p,n has no counterexample. It does not license replacing a classical
# consequence assertion with the internal R arrow.
classical_mp_failures = [dict(P=p, N=n) for p, n in product((False, True), repeat=2)
                        if (p and ((not p) or n)) and not n]
assert not classical_mp_failures

# Independent schema matcher for the actual delivered derivation text.
def matches(schema, formula, env=None):
    if env is None:
        env = {}
    if isinstance(schema, str):
        if schema in env:
            return env[schema] == formula
        env[schema] = formula
        return True
    return (not isinstance(formula, str) and len(schema) == len(formula)
            and schema[0] == formula[0]
            and all(matches(a, b, env) for a, b in zip(schema[1:], formula[1:])))

def read_proof(path):
    out = []
    for line in path.read_text().splitlines():
        m = re.fullmatch(r'(\d+)\.\s+(.*?)\s+\[(.*?)\]', line)
        if m:
            assert int(m[1]) == len(out) + 1
            out.append((parse(m[2]), m[3]))
    return out

def check_proof(lines, allow_hypothesis=None):
    results = []
    for index, (formula, reason) in enumerate(lines, 1):
        valid = False
        if re.fullmatch(r'A\d+', reason):
            n = int(reason[1:])
            valid = 1 <= n <= 16 and matches(SCHEMES[n - 1], formula)
        elif reason.startswith('MP '):
            major, minor = map(int, reason[3:].split(','))
            valid = (0 < major < index and 0 < minor < index
                     and lines[major - 1][0] == ('imp', lines[minor - 1][0], formula))
        elif reason.startswith('Adjunction '):
            left, right = map(int, reason[len('Adjunction '):].split(','))
            valid = (0 < left < index and 0 < right < index
                     and formula == ('and', lines[left - 1][0], lines[right - 1][0]))
        elif reason.startswith('H:'):
            valid = allow_hypothesis is not None and formula == allow_hypothesis
        results.append({'line': index, 'reason': reason, 'valid': valid})
    return results

conditional = read_proof(AUTHOR / 'VARIABLE_SHARING_REDUCTION.md')
conditional_results = check_proof(conditional, forms['B_arrow_N'])
assert len(conditional) == 13 and all(r['valid'] for r in conditional_results)
assert conditional[8][0] == forms['C_arrow_B']
assert conditional[-1][0] == forms['C_arrow_N']
assert variables(forms['C']).isdisjoint(variables(forms['N']))
assert not all(r['valid'] for r in check_proof(conditional))
mutant = conditional[:-1] + [(('imp', forms['N'], forms['C']), conditional[-1][1])]
assert not all(r['valid'] for r in check_proof(mutant, forms['B_arrow_N']))

positive = read_proof(ROOT / 'necessary-truth-operative-basing-20261009/RELEVANT_PROOF.md')
positive_results = check_proof(positive)
assert len(positive) == 19 and all(r['valid'] for r in positive_results)

# Variable-sharing metatheorem: closure enables structural induction for
# arbitrary formulas on disjoint variable sets; cross condition blocks arrows.
subalgebras = [frozenset(('-1', '+1')), frozenset(('-2', '+2'))]
for s in subalgebras:
    assert all(NEG[x] in s for x in s)
    assert all(f(x, y) in s for x, y in product(s, repeat=2) for f in (meet, join, imp))
cross_results = [{'a': a, 'b': b, 'value': imp(a, b)} for a, b in product(*subalgebras)]
assert all(r['value'] not in D for r in cross_results)

# Compare only now, without importing the author's implementation.
author = json.loads((AUTHOR / 'CHECK_RESULTS.json').read_text())
assert author['table'] == [[TABLE[x][y] for y in V] for x in V]
assert author['negation'] == NEG
for x, y in product(V, repeat=2):
    xb, yb = author['lattice_bits'][x], author['lattice_bits'][y]
    assert author['lattice_bits'][meet(x, y)] == xb & yb
    assert author['lattice_bits'][join(x, y)] == xb | yb
assert author['total_axiom_assignments'] == sum(r['assignments'] for r in axiom_results)

# Mutation control genuinely reevaluates the independently transcribed A1.
original_entry = TABLE['+0']['+0']
TABLE['+0']['+0'] = '-3'
assert value(SCHEMES[0], {'A': '+0'}) not in D
TABLE['+0']['+0'] = original_entry
assert value(SCHEMES[0], {'A': '+0'}) in D

out = {
    'independent_implementation': 'Primary table transcription and Hasse-edge transitive closure; no author code import or execution',
    'axioms': axiom_results,
    'axiom_assignment_total': sum(r['assignments'] for r in axiom_results),
    'modus_ponens_pairs': 64, 'modus_ponens_failures': mp_fail,
    'adjunction_pairs': 64, 'adjunction_failures': adj_fail,
    'lattice_covers': COVERS, 'order_pairs': len(LE),
    'negation_involution_and_de_morgan': True,
    'designation_boolean_for_and_or_negation': True,
    'target': 'Q →R Q is A1; syntactic theorem, not just finite-algebra validity',
    'identity_all_eight_Q_values_designated_and_negation_undesignated': True,
    'witness_assignment': witness_assignment, 'witness': witness,
    'material_actual_assignments': len(material_actual),
    'material_actual_sensitivity_failures': len(material_failures),
    'material_actual_failure_witnesses': material_failures,
    'repair_values': repair_values,
    'classical_material_modus_ponens_failures': classical_mp_failures,
    'conditional_derivation': conditional_results,
    'conditional_derivation_rejected_without_H': True,
    'wrong_final_consequent_rejected': True,
    'corrupt_table_entry_rejected_by_recomputed_A1': True,
    'positive_relevant_derivation': positive_results,
    'variable_sharing_closed_subalgebras': [sorted(s) for s in subalgebras],
    'variable_sharing_cross_values': cross_results,
    'source_and_author_table_and_lattice_agree': True,
    'scope_warning': 'B entails N because N is already an R theorem. Failure is of the internal relevant arrow and of deriving relevant sensitivity from designated material grounds. No epistemic-model construction is supplied.'
}
(HERE / 'INDEPENDENT_RESULTS.json').write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({k: out[k] for k in ('axiom_assignment_total', 'witness', 'material_actual_assignments', 'material_actual_sensitivity_failures', 'repair_values')}, ensure_ascii=False, indent=2))
print('PASS: independent source table, lattice, 16 axioms, 2 rules, witness, 13-line conditional proof and 19-line positive proof.')
