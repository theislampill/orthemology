#!/usr/bin/env python3
from __future__ import annotations
import hashlib, itertools, json
from pathlib import Path
import yaml
BASE=Path(__file__).resolve().parents[1]
MODEL=BASE/'models'/'PMR007_DEEP_R_R5_COMMON_UNION_MODEL_V2.yaml'
LEDGER=Path('REPOSITORY_RELATIVE:docs/project-closure/ar8r-v11/programs/AR8R-TRANSCENDENTAL-BRIDGE-AND-RIVAL-LEDGER-V11.yaml')
OUT=BASE/'rereviews'/'PMR-007_DEEP_R_DISTINCT_CONSTRAINT_AND_BRIDGE_REREVIEW_RESULTS.json'

def main():
    m=yaml.safe_load(MODEL.read_text())
    # Independent role-set enumeration: choose three nonempty bearer subsets.
    bearers=('a','b','c','d')
    nonempty=[set(b for i,b in enumerate(bearers) if (mask>>i)&1) for mask in range(1,16)]
    global_count=0; no_common=0; common=0; witness=None
    for W,P,K in itertools.product(nonempty, repeat=3):
        global_count += 1
        inter=W & P & K
        if inter: common += 1
        else:
            no_common += 1
            if witness is None:
                witness={'W_role':sorted(W),'P_role':sorted(P),'K_role':sorted(K)}

    # Link-graph reachability and typed component engagement.
    edges=[(x['from'],x['to']) for x in m['links']]
    graph={}
    for u,v in edges: graph.setdefault(u,set()).add(v)
    def reaches(start,target):
        seen={start}; stack=[start]
        while stack:
            u=stack.pop()
            for v in graph.get(u,()):
                if v==target: return True
                if v not in seen: seen.add(v); stack.append(v)
        return False
    reach_checks={
      'selection_to_effect': reaches('selection_coordinate_S','e'),
      'content_to_realizer': reaches('finite_content_class','a'),
      'norm_to_revision': reaches('exact_norm_potential_N','revision_and_selection_states'),
      'order_to_modal_profiles': reaches('o','modal_transition_profiles'),
      'translation_to_content': reaches('feag_translation','selected_finite_content'),
      'response_to_state': reaches('response_transducer','selected_finite_state'),
    }

    # Source-conditioned expansion is separate and leaves neutral links untouched.
    neutral_source=m['source_firewall']['neutral_model']['track_n_source_accepted']
    source_expansion=m['source_firewall']['source_conditioned_expansion']
    source_firewall_ok=(neutral_source is False and source_expansion['separate'] is True and source_expansion['neutral_entailment'] is False)

    # Verify current bridge ledger remains open at the target joints.
    ledger_bytes=LEDGER.read_bytes(); ledger_hash=hashlib.sha256(ledger_bytes).hexdigest(); L=yaml.safe_load(ledger_bytes)
    statuses={b['id']:b['status'] for b in L['bridges']}
    expected_open={
      'B4':'NOT_ENTAILED; RIVAL_SURVIVES',
      'B5':'NOT_ENTAILED; RIVAL_SURVIVES',
      'B6':'NOT_ENTAILED; DERIVATIONAL_PARITY_AND_R5_SURVIVE',
      'B7':'NOT_ENTAILED; CONDITIONAL_CONCEPTUALIST_BRIDGE',
      'B8':'NOT_ENTAILED; RIVAL_SURVIVES',
      'B11':'CONDITIONAL_ROLE_INTEGRATION_ONLY',
      'B15':'NOT_ENTAILED_BY_NATURAL_THEOLOGY; REVELATIONAL_CONCLUSION',
      'B16':'NOT_ENTAILED_BY_NATURAL_THEOLOGY',
    }
    bridge_checks={k:(statuses.get(k)==v) for k,v in expected_open.items()}

    withheld=m['withheld']
    withheld_ok=all(v is True for v in withheld.values())
    authority_ok=(m['authority_ceiling']['metaphysical_possibility']=='NOT_ESTABLISHED' and m['authority_ceiling']['world_actuality']=='NOT_ESTABLISHED')
    overall=(global_count==3375 and no_common==1680 and common==1695 and all(reach_checks.values()) and source_firewall_ok and all(bridge_checks.values()) and withheld_ok and authority_ok)
    res={
      'identity':'PMR-007-R5CU-1',
      'method':'nonempty-role-subset constraint enumeration plus YAML link reachability and live bridge-ledger status check',
      'role_set_triples':global_count,
      'with_common_bearer':common,
      'without_common_bearer':no_common,
      'first_no_common_witness':witness,
      'link_reachability':reach_checks,
      'source_firewall_pass':source_firewall_ok,
      'withheld_conclusions_pass':withheld_ok,
      'authority_ceiling_pass':authority_ok,
      'bridge_ledger_sha256':ledger_hash,
      'bridge_status_checks':bridge_checks,
      'overall':'PASS' if overall else 'FAIL',
      'scope_notes':[
        'Constraint satisfiability is not a metaphysical possibility proof.',
        'Role proxies are not Divine attribute predications.',
        'Bridge ledger remains current repository authority; no source premise migrated.'
      ]
    }
    OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+'\n'); print(json.dumps(res,indent=2,sort_keys=True))
if __name__=='__main__': main()
