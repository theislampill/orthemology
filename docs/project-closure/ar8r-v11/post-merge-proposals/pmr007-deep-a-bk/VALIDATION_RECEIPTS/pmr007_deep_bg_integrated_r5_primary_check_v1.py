from itertools import product
import json
from pathlib import Path

OUT = Path(__file__).with_name(Path(__file__).stem + '_results.json')
conclusions = [
    'Intellect','Personal','Agentic','IntentionalUptake','BecauseFitting',
    'Wisdom','SpeechCapacity','ActualSpeech','CreatorClass'
]

neutral = {
    'worlds': ('w0','w1'),
    'bearer': 'g',
    'exists_all_worlds': True,
    'underived_all_worlds': True,
    'external_actual_all_worlds': True,
    'causally_effective': True,
    'one_bearer_all_structural_roles': True,
    'truth_anchor': 'c1',
    'target_key': 'c1',
    'norm': (0,1),
    'selection': ('a0','a1'),
    'effects': ('e0','e1'),
    'fitting_action': 'a1',
    'expression': ('t0','t1'),
    'faithful_expression': True,
    'joint_law': ((0.5,0.0),(0.0,0.5)),
    'latent_width': 2,
    'source_functional_bearer': 'g',
}

def neutral_ok(n):
    return all([
        len(n['worlds']) == 2,
        n['exists_all_worlds'],
        n['underived_all_worlds'],
        n['external_actual_all_worlds'],
        n['causally_effective'],
        n['one_bearer_all_structural_roles'],
        n['truth_anchor'] == n['target_key'],
        n['norm'] == (0,1),
        n['selection'][1] == n['fitting_action'],
        n['faithful_expression'],
        n['latent_width'] == 2,
        n['source_functional_bearer'] == n['bearer'],
    ])

res = {
    'identity':'PMR-007-IR5CM-1',
    'checker':'PRIMARY_V1',
    'neutral_model_pass': neutral_ok(neutral),
    'expansions_checked':0,
    'neutral_reduct_failures':0,
    'all_false_witnesses':0,
    'all_true_twins':0,
    'single_deletion_models':{},
    'carrier_boxing_structural_profiles':0,
    'aligned_structural_profiles':0,
}

# All personal/theological expansions have exactly the same neutral reduct.
for bits in product([False,True], repeat=len(conclusions)):
    expansion = dict(zip(conclusions,bits))
    res['expansions_checked'] += 1
    if not neutral_ok(neutral): res['neutral_reduct_failures'] += 1
    if not any(bits): res['all_false_witnesses'] += 1
    if all(bits): res['all_true_twins'] += 1

for target in conclusions:
    expansion = {c: True for c in conclusions}
    expansion[target] = False
    res['single_deletion_models'][target] = {
        'neutral_model_pass': neutral_ok(neutral),
        'target_false': not expansion[target],
        'all_other_conclusions_true': all(expansion[c] for c in conclusions if c != target),
    }

# Same bearer can merely box independently recombinable primitive coordinates.
# Five binary structural choices: truth anchor, target key, selector, efficacy, expression.
for profile in product([0,1], repeat=5):
    res['carrier_boxing_structural_profiles'] += 1
    if len(set(profile)) == 1:
        res['aligned_structural_profiles'] += 1

failed = (
    not res['neutral_model_pass'] or res['neutral_reduct_failures'] or
    res['all_false_witnesses'] != 1 or res['all_true_twins'] != 1 or
    any(not all(v.values()) for v in res['single_deletion_models'].values()) or
    res['carrier_boxing_structural_profiles'] != 32 or
    res['aligned_structural_profiles'] != 2
)
res['result'] = 'FAIL' if failed else 'PASS'
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
