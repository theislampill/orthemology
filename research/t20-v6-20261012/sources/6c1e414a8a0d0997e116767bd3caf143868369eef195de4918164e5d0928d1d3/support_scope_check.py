#!/usr/bin/env python3
"""Source-bound dependency-scope controls, not a warrant classifier.

Reads the actual unchanged OriginalBearerBridge declarations. The checks below
identify assumptions consumed by selected existing derivations and preserve
their output-specific scope. They do not run Lean, assert semantic minimality,
set philosophical confidence, or decide whether any challenge is justified.
"""
from pathlib import Path
import hashlib
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BRIDGE = ROOT / 'intrinsic-necessity-bridge-20261009/sources/OriginalBearerBridge.lean'
source = BRIDGE.read_text()


def declaration(name):
    match = re.search(r'^theorem ' + re.escape(name) + r'\b', source, re.M)
    if match is None:
        raise RuntimeError('Missing actual declaration: ' + name)
    next_decl = re.search(r'^theorem |^end ', source[match.end():], re.M)
    stop = match.end() + next_decl.start() if next_decl else len(source)
    return source[match.start():stop]


checks = []


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    checks.append(name)


check('bridge_matches_previously_bound_original', hashlib.sha256(BRIDGE.read_bytes()).hexdigest()
      == '086fb3bb7d7cd152b19ee2e6af47c25b92bd5b7825b0bfb9ee16a9ef7a56ba99')
original = declaration('original_bearer_of_completion')
essential = declaration('essential_nonreceipt_of_actual_original')
combined = declaration('abc_same_witness')
for name in ('occurrence', 'completion', 'realisation', 'support'):
    check('original_interface_contains_' + name, re.search(r'\(' + name + r'\s*:', original) is not None)
for omitted in ('ContingencyNeed', 'ConstitutiveReception', 'ReceiptRepresentation', 'Necessary'):
    check('original_interface_omits_' + omitted, omitted not in original)
for name in ('original', 'constitution'):
    check('essential_interface_contains_' + name, re.search(r'\(' + name + r'\s*:', essential) is not None)
for omitted in ('ContingencyNeed', 'ReceiptRepresentation', 'Necessary'):
    check('essential_interface_omits_' + omitted, omitted not in essential)
check('essential_body_uses_actual_original_and_constitution',
      'original.2 (constitution g' in essential and 's.actual original.1' in essential)
check('combined_necessity_is_existing_inherited_call',
      'SourceIdentity.necessary_of_actual_root' in combined)
check('combined_necessity_uses_need_adapter',
      '(need_to_inherited s premises.representation premises.need)' in combined)
check('combined_uniform_uses_constitution_adapter',
      '(constitution_to_inherited s premises.representation premises.constitution)' in combined)
check('combined_keeps_existing_essential_projection',
      'essential_nonreceipt_of_actual_original s g witness.2.2.2.2 premises.constitution' in combined)

# Route-specific consumed-premise sets, not semantically necessary grounds.
# Necessary's representation entry records this actual adapter-based proof.
# A direct proof could avoid that adapter; no minimality claim is made here.
base = {'occurrence', 'completion', 'realisation', 'support'}
routes = {
    'OriginalWitness': base,
    'Necessary_via_existing_adapter': base | {'need', 'representation'},
    'EssentialNonreceipt_via_existing_direct_projection': base | {'constitution'},
    'UniformRoot_via_existing_adapter': base | {'need', 'representation', 'constitution'},
}


def affected(challenged):
    return sorted(output for output, consumed in routes.items() if consumed & set(challenged))


cases = {
    'need': ['Necessary_via_existing_adapter', 'UniformRoot_via_existing_adapter'],
    'constitution': ['EssentialNonreceipt_via_existing_direct_projection', 'UniformRoot_via_existing_adapter'],
    'representation': ['Necessary_via_existing_adapter', 'UniformRoot_via_existing_adapter'],
    'completion': sorted(routes),
    'realisation': sorted(routes),
    'support': sorted(routes),
    'occurrence': sorted(routes),
}
for premise, expected in cases.items():
    check('selective_revalidation_' + premise, affected([premise]) == expected)

# Discriminating adverse controls: neither an all-or-nothing package dependency
# nor dropping constitutive dependence reproduces the inspected proof scopes.
collapsed = set().union(*routes.values())
check('bundled_all_outputs_overpropagates_need',
      sorted(output for output in routes if 'need' in collapsed) != cases['need'])
check('bundled_all_outputs_overpropagates_constitution',
      sorted(output for output in routes if 'constitution' in collapsed) != cases['constitution'])
damaged = dict(routes)
damaged['EssentialNonreceipt_via_existing_direct_projection'] = base
check('erasing_constitution_misses_actual_dependency',
      sorted(output for output, consumed in damaged.items() if 'constitution' in consumed)
      != cases['constitution'])

cp23_path = ROOT / 'intrinsic-necessity-bridge-20261009/sources/CP23__affirmative-intrinsic-necessity-20261009__REPORT.md'
cp23 = cp23_path.read_text()
check('cp23_prohibits_independent_neutral_axiom_reconstruction',
      'They should not be represented as a newly proved chain of logically independent neutral axioms.' in cp23)
check('cp23_philosophical_ground_is_not_author_assertion_alone',
      'The judgment is not being accepted merely because the author announces it.' in cp23)
check('cp23_does_not_certify_constitutive_reception',
      'or `ConstitutiveReception`.' in cp23)
cnd_path = ROOT / 'intrinsic-necessity-bridge-20261009/sources/735eaf9802be4e21c4bb97cca13f469ed1611a51c1bdf731dadf79e6f0fd2f74__CND_ESSENTIAL_INDEPENDENCE_PUBLIC.md'
cnd = cnd_path.read_text()
check('t17_positive_scope_survives_failed_new_cnd_route',
      'A proposed additional argument can fail to improve that warrant without withdrawing it.' in cnd)

result = {
    'status': 'PASS',
    'check_count': len(checks),
    'kind': 'Read-only source identity, declaration-scope and selective-revalidation controls',
    'not_claimed': ['Lean replay', 'mathematical support minimality', 'actual challenge or defeater',
                    'human warrant classification', 'new philosophical proof', 'minimum sidecar bits'],
    'checks': checks,
    'actual_derivation_consumed_premises': {k: sorted(v) for k, v in routes.items()},
    'challenge_targets_for_revalidation_only': cases,
}
(HERE / 'CHECK_RESULTS.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': result['status'], 'checks': len(checks), 'kind': result['kind']}))
