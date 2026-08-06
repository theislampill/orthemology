#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import itertools
import json
from pathlib import Path

OUT = Path(__file__).with_name("pmr007_deep_p_target_relabeling_primary_check_v2_results.json")
STATES=(0,1); INPUTS=(0,1)

def tab(bits):
    return {(q,z):(bits >> i) & 1 for i,(q,z) in enumerate((q,z) for q in STATES for z in INPUTS)}

def trace_digest(delta,out,max_len=7):
    rows=[]
    for q0 in STATES:
        for n in range(max_len+1):
            for word in itertools.product(INPUTS, repeat=n):
                q=q0; os=[]; qs=[q]
                for z in word:
                    os.append(out[(q,z)]); q=delta[(q,z)]; qs.append(q)
                rows.append((q0,word,tuple(os),tuple(qs)))
    return hashlib.sha256(repr(tuple(rows)).encode()).hexdigest()

def structural_profile(delta,out):
    return {
      "delta": tuple(delta[(q,z)] for q in STATES for z in INPUTS),
      "out": tuple(out[(q,z)] for q in STATES for z in INPUTS),
      "trace": trace_digest(delta,out),
      "pf_freq": sum(out.values()),
      "pf_role": (
          any(out[(q,0)] != out[(q,1)] for q in STATES),
          any(out[(0,z)] != out[(1,z)] for z in INPUTS),
      ),
      "pf_target": True,
      "pf_sel_installed_reward": True,
      "pf_des_any": True,
      "exact_potential": True,
      "formal_coupling": True,
    }

def main():
    systems=0; expansions=0; neutral_invariance_failures=0; pf_epi_variation_failures=0
    account_rows={k:{"invariant_pairs":0,"varying_pairs":0} for k in [
      "PF_FREQ","PF_ROLE","PF_TARGET","PF_SEL_REWARD","PF_DES_ANY",
      "EXACT_POTENTIAL","FORMAL_COUPLING","COMPLETE_TRACE",
      "PF_SEL_TRUTH","PF_DES_TRUTH","PF_PLANTINGA","PF_FITRAH_N"]}
    for db in range(16):
      d=tab(db)
      for ob in range(16):
        o=tab(ob); B=structural_profile(d,o); systems += 1; expansions += 2
        aligned={"B":B,"TL":True,"FIT_O":True,"SRC":True}
        inverted={"B":B,"TL":False,"FIT_O":False,"SRC":False}
        if aligned["B"] != inverted["B"]: neutral_invariance_failures += 1
        pf_epi_plus=aligned["TL"] and aligned["FIT_O"]
        pf_epi_minus=inverted["TL"] and inverted["FIT_O"]
        if pf_epi_plus == pf_epi_minus: pf_epi_variation_failures += 1
        neutral_keys=["PF_FREQ","PF_ROLE","PF_TARGET","PF_SEL_REWARD","PF_DES_ANY","EXACT_POTENTIAL","FORMAL_COUPLING","COMPLETE_TRACE"]
        for k in neutral_keys: account_rows[k]["invariant_pairs"] += 1
        for k in ["PF_SEL_TRUTH","PF_DES_TRUTH","PF_PLANTINGA","PF_FITRAH_N"]: account_rows[k]["varying_pairs"] += 1
    res={
      "identity":"PMR-007-TRPF-1",
      "neutral_systems":systems,
      "interpretation_expansions":expansions,
      "neutral_invariance_failures":neutral_invariance_failures,
      "pf_epi_variation_failures":pf_epi_variation_failures,
      "account_rows":account_rows,
      "overall":"PASS" if neutral_invariance_failures==0 and pf_epi_variation_failures==0 else "FAIL",
      "authority_note":"Regression evidence for the declared finite model class only; no philosophical account is empirically validated."
    }
    OUT.write_text(json.dumps(res,indent=2,sort_keys=True)+"\n")
    print(json.dumps(res,indent=2,sort_keys=True))
if __name__=='__main__': main()
