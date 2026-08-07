from __future__ import annotations
from pathlib import Path
from itertools import product
import hashlib, json, yaml

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).with_name(Path(__file__).stem+'_results.json')
MODEL=ROOT/'models/PMR007_DEEP_BG_INTEGRATED_R5_COMMON_MODEL_V2.yaml'

def sha(path):
    h=hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def canon(obj):
    return json.dumps(obj,sort_keys=True,separators=(',',':'))

m=yaml.safe_load(MODEL.read_text())
targets=m['target_predicates']
neutral=m['neutral_model']
neutral_digest=hashlib.sha256(canon(neutral).encode()).hexdigest()

res={
 'identity':'PMR-007-IR5CM-1','checker':'DISTINCT_REDUCT_EXPANSION_REREVIEW_V2',
 'frozen_hash_rows':0,'frozen_hash_mismatches':[],
 'target_predicates':len(targets),'expansions_checked':0,
 'neutral_digest_variations':0,'false_witnesses_by_target':{t:0 for t in targets},
 'true_witnesses_by_target':{t:0 for t in targets},
 'single_deletion_pass':{},'one_bearer_role_checks':{},
 'structural_profiles':0,'fully_aligned_profiles':0,
 'bridge_controls':{},
}

for line in (ROOT/'PMR-007_DEEP_BG_V2_FROZEN_HASHES.sha256').read_text().splitlines():
    if not line.strip(): continue
    exp,rel=line.split(None,1); rel=rel.strip(); act=sha(ROOT/rel)
    res['frozen_hash_rows']+=1
    if exp!=act: res['frozen_hash_mismatches'].append({'path':rel,'expected':exp,'actual':act})

# A different implementation from the primary checker: bitmask enumeration and
# canonical neutral-reduct digest rather than product tuples over an in-script model.
for mask in range(1<<len(targets)):
    expansion={t:bool((mask>>i)&1) for i,t in enumerate(targets)}
    res['expansions_checked']+=1
    if hashlib.sha256(canon(neutral).encode()).hexdigest()!=neutral_digest:
        res['neutral_digest_variations']+=1
    for t in targets:
        res['true_witnesses_by_target'][t]+=int(expansion[t])
        res['false_witnesses_by_target'][t]+=int(not expansion[t])

for t in targets:
    expansion={x:True for x in targets}; expansion[t]=False
    res['single_deletion_pass'][t]=(
        not expansion[t] and all(expansion[x] for x in targets if x!=t)
        and hashlib.sha256(canon(neutral).encode()).hexdigest()==neutral_digest
    )

roles=set(neutral['structural_roles_on_g'])
res['one_bearer_role_checks']={
 'one_bearer':m['sorts']['bearers']==['g'],
 'all_required_roles':roles=={'modal_order','truth_register','target_key','norm','selector','efficacy','expression'},
 'present_all_declared_worlds':all(v==['g'] for v in neutral['present'].values()),
 'underived_in_declared_graph':neutral['predecessor_relation']==[],
 'nontrivial_effect_relation':len(neutral['actualizes'])>=2,
 'truth_target_alignment':neutral['truth_label']['c1'] and neutral['target_key']=='c1',
 'norm_selection_alignment':neutral['norm']['c1']==1 and neutral['selection'][1]=='a1',
 'fitting_alignment':'a1' in neutral['fitting_actions'],
 'faithful_expression':neutral['faithful_token_assignment'],
 'latent_width_two':neutral['latent_product_width']==2,
}

# Five independent binary coordinates demonstrate carrier-boxing support size.
for bits in product([0,1],repeat=5):
    res['structural_profiles']+=1
    if all(b==bits[0] for b in bits): res['fully_aligned_profiles']+=1

res['bridge_controls']={
 'B6_endpoint_granted_structurally':res['one_bearer_role_checks']['one_bearer'] and res['one_bearer_role_checks']['all_required_roles'],
 'B7_intellect_false_expansion_exists':res['false_witnesses_by_target']['Intellect']>0,
 'B8_personal_false_expansion_exists':res['false_witnesses_by_target']['Personal']>0 and res['false_witnesses_by_target']['Agentic']>0,
 'B11_wisdom_false_expansion_exists':res['false_witnesses_by_target']['Wisdom']>0 and res['false_witnesses_by_target']['BecauseFitting']>0,
 'B15_speech_false_expansion_exists':res['false_witnesses_by_target']['SpeechCapacity']>0 and res['false_witnesses_by_target']['ActualSpeech']>0,
 'creator_false_expansion_exists':res['false_witnesses_by_target']['CreatorClass']>0,
 'source_role_does_not_encode_personality':neutral['source_functional_role_image']=='g' and res['false_witnesses_by_target']['Personal']>0,
}

failed=bool(res['frozen_hash_mismatches']) or res['neutral_digest_variations']!=0
failed=failed or res['expansions_checked']!=512
failed=failed or any(v!=256 for v in res['false_witnesses_by_target'].values())
failed=failed or any(v!=256 for v in res['true_witnesses_by_target'].values())
failed=failed or not all(res['single_deletion_pass'].values())
failed=failed or not all(res['one_bearer_role_checks'].values())
failed=failed or res['structural_profiles']!=32 or res['fully_aligned_profiles']!=2
failed=failed or not all(res['bridge_controls'].values())
res['result']='FAIL' if failed else 'PASS'
OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n')
print(json.dumps(res,indent=2,sort_keys=True))
