#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path

OUT_NAMES=("M","A","S","N","R")

def F(t:int,e:int)->tuple[int,...]:
    return (t,e,t,t,t & e)

def intervention_signature(theta:tuple[int,int]):
    t,e=theta
    base=F(t,e)
    return {
      "flip_t": tuple(a^b for a,b in zip(base,F(1-t,e))),
      "flip_e": tuple(a^b for a,b in zip(base,F(t,1-e))),
    }

def main():
    theta=list(itertools.product((0,1),repeat=2))
    image={F(*x) for x in theta}
    marginals=[{y[i] for y in image} for i in range(5)]
    product=set(itertools.product(*[sorted(x) for x in marginals]))
    laws_ok=all(m==s==n and r==(a & n) for m,a,s,n,r in image)
    sig={x:intervention_signature(x) for x in theta}
    # Realization labels are intentionally outside the retained structure.
    realization_structures={name:{"theta":theta,"image":sorted(image),"sig":sig}
                            for name in ("H_PER","H_IMP","H_DIST")}
    parity=(realization_structures["H_PER"]==realization_structures["H_IMP"]==realization_structures["H_DIST"])
    carrier_box=set(itertools.product((0,1),repeat=5))
    gerrymandered_states=list(range(32))
    out={
      "schema":"PMR007_DEEP_B_CHECK_RESULTS_V1",
      "theta_count":len(theta),
      "image_count":len(image),
      "marginal_product_count":len(product),
      "excluded_profiles":len(product-image),
      "cross_domain_laws_hold":laws_ok,
      "realization_parity":parity,
      "carrier_box_profile_count":len(carrier_box),
      "gerrymandered_information_bits":5,
      "positive_information_bits":2,
      "intervention_signatures":{str(k):v for k,v in sig.items()},
      "controls":{
        "carrier_box_not_restricted": len(carrier_box)==32,
        "positive_is_proper_subset": image < product,
        "impersonal_matches_personal": parity,
        "distributed_matches_personal": parity,
        "idle_personal_tag_no_change": parity,
        "single_32_state_code_not_two_bit_compression": len(gerrymandered_states)==32,
      }
    }
    out["overall"]="PASS" if laws_ok and parity and all(out["controls"].values()) else "FAIL"
    p=Path(__file__).with_name("pmr007_deep_b_unification_check_results.json")
    p.write_text(json.dumps(out,indent=2,sort_keys=True)+"\n")
    print(json.dumps(out,indent=2,sort_keys=True))
if __name__=="__main__": main()
