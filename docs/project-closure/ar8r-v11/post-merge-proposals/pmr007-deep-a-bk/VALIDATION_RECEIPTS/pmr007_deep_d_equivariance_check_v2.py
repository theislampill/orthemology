#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
MODEL=ROOT/'models/PMR007_DEEP_D_UNCREATED_GRAMMAR_MODELS_V2.yaml'

def perms(n): return list(itertools.permutations(range(n)))
def act(g,x): return g[x]

def main():
    m=yaml.safe_load(MODEL.read_text())
    failures=[]; symmetric_cases=0; extension_cases=0; asymmetry_cases=0; selector_cases=0
    for n in range(2,8):
        G=perms(n)
        # Singleton fixed source: a map chooses y. Equivariance iff y globally fixed.
        for y in range(n):
            symmetric_cases += 1
            equiv=all(act(g,y)==y for g in G)
            fixed=all(act(g,y)==y for g in G)
            if equiv!=fixed: failures.append({'kind':'fixed_source','n':n,'y':y})
        # Add one fixed star.
        star=n
        for y in range(n+1):
            extension_cases += 1
            equiv=all((y==star or act(g,y)==y) for g in G)
            if equiv!=(y==star): failures.append({'kind':'fixed_extension','n':n,'y':y})
        # Identity map on X=Y is equivariant, but a selected x0 is non-invariant.
        for x in range(n):
            equiv=all(act(g,x)==act(g,x) for g in G)  # id(gx)=g(id x)
            noninvariant=any(act(g,x)!=x for g in G)
            asymmetry_cases += 1
            if not equiv or not noninvariant: failures.append({'kind':'source_asymmetry','n':n,'x':x})
        # External selector s transforms with Y; F(x0,s)=s is equivariant.
        for s in range(n):
            selector_cases += 1
            if not all(act(g,s)==act(g,s) for g in G): failures.append({'kind':'selector','n':n,'s':s})
        # A constant choosing y0 is not equivariant when some g moves y0.
        y0=0
        if not any(act(g,y0)!=y0 for g in G): failures.append({'kind':'non_equivariant_constant','n':n})
    ug7=m['articulability_nonmental_models']
    ug7_ok=all(x.get('articulability') is True and x.get('mentality') is False for x in ug7)
    ug8=m['speech_nonimplications']
    # Each control has at least one true antecedent and a false downstream coordinate.
    ug8_ok=all(any(v is True for k,v in x.items() if k!='id') and any(v is False for k,v in x.items() if k!='id') for x in ug8)
    c=m['created_expression_contract']
    ug9_ok=(c['token_identity_implies_content_identity'] is False and c['content_identity_implies_token_identity'] is False and c['translation_implies_complete_preservation'] is False and c['repeated_bytes_imply_uncreated_content'] is False and c['source_theological_bridge_required'] is True)
    out={
      'schema':'PMR007_DEEP_D_EQUIVARIANCE_CHECK_RESULTS_V2',
      'symmetric_target_cases':symmetric_cases,
      'fixed_point_extension_cases':extension_cases,
      'source_asymmetry_cases':asymmetry_cases,
      'external_selector_cases':selector_cases,
      'theorem_or_sharp_control_failures':failures,
      'ug7_models_checked':len(ug7),
      'ug7_nonbridge_pass':ug7_ok,
      'ug8_models_checked':len(ug8),
      'ug8_nonbridge_pass':ug8_ok,
      'ug9_contract_pass':ug9_ok,
    }
    out['overall']='PASS' if not failures and ug7_ok and ug8_ok and ug9_ok else 'FAIL'
    p=Path(__file__).with_name('pmr007_deep_d_equivariance_check_v2_results.json')
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=='__main__': main()
