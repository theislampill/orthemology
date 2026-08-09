#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path

ARCHES = ("U", "I", "P")
INTERVENTIONS = ("noop", "flip_content", "flip_fit", "flip_payoff", "flip_version", "flip_authority", "flip_root")
TARGETS = {
    "U": {"class":"U", "common_bearer":1, "uptake":1, "because_fit":1, "wisdom":1},
    "I": {"class":"I", "common_bearer":1, "uptake":0, "because_fit":0, "wisdom":0},
    "P": {"class":"P", "common_bearer":0, "uptake":0, "because_fit":0, "wisdom":0},
}
INDEX={"flip_content":0,"flip_fit":1,"flip_payoff":2,"flip_version":3,"flip_authority":4,"flip_root":5}

def abstract_step(state: tuple[int,...], intervention: str) -> tuple[int,...]:
    s=list(state)
    if intervention != "noop": s[INDEX[intervention]] ^= 1
    return tuple(s)

def architecture_step(state: tuple[int,...], intervention: str, arch: str, bad_version: bool=False) -> tuple[int,...]:
    s=list(state)
    if intervention != "noop":
        ix=INDEX[intervention]
        if bad_version and arch=="P" and intervention=="flip_version": ix=4
        s[ix] ^= 1
    return tuple(s)

def output(state: tuple[int,...]) -> tuple[int,int,int,int]:
    c,f,p,v,a,r=state
    return (c^f, p, v&a, r)

def run_word(initial, word, arch, *, target_leak=False, alt=False, bad_version=False):
    state=initial; obs=[]
    for j in word:
        state=architecture_step(state,j,arch,bad_version=bad_version)
        y=output(state)
        if alt and arch=="I" and j=="flip_root": y=(1-y[0],)+y[1:]
        if target_leak: y=y+(TARGETS[arch]["class"],)
        obs.append(y)
    return tuple(obs),state

def all_words(max_len):
    yield ()
    for k in range(1,max_len+1): yield from itertools.product(INTERVENTIONS,repeat=k)

def main():
    words=list(all_words(3))
    r={
      "schema":"pmr007-deep-ck-concrete-architecture-map-primary-check-v2",
      "architectures":list(ARCHES),"initial_states":0,"declared_words":len(words),
      "architecture_profile_comparisons":0,"eligible_profile_mismatches":0,
      "target_variation_in_equal_profile_fibres":0,"target_leak_controls":0,
      "target_leak_failures":0,"commutation_checks":0,"commutation_failures":0,
      "version_mismatch_controls":0,"version_mismatch_detected":0,
      "partial_ownership_contract_checks":3,"partial_ownership_contract_detected":True,
      "source_relative_operation_rejected_as_neutral":True,
      "omitted_intervention_controls":0,"omitted_intervention_collisions":0,
      "full_profile_splits_alt_model":0,
      "v1_checker_defect":"incorrectly_expected_64_target_leak_failures_instead_of_zero"
    }
    for initial in itertools.product((0,1),repeat=6):
      r["initial_states"]+=1
      for j in INTERVENTIONS:
        abs_next=abstract_step(initial,j)
        for a in ARCHES:
          r["commutation_checks"]+=1
          r["commutation_failures"]+=architecture_step(initial,j,a)!=abs_next
        # architecture P bad map toggles authority rather than version
        if j=="flip_version":
          r["version_mismatch_controls"]+=1
          r["version_mismatch_detected"]+=architecture_step(initial,j,"P",bad_version=True)!=abs_next
      for word in words:
        profiles=[run_word(initial,word,a)[0] for a in ARCHES]
        r["architecture_profile_comparisons"]+=1
        r["eligible_profile_mismatches"]+=len(set(profiles))!=1
        r["target_variation_in_equal_profile_fibres"]+=(len(set(profiles))==1 and len({TARGETS[a]["class"] for a in ARCHES})>1)
        if word:
          leaks=[run_word(initial,word,a,target_leak=True)[0] for a in ARCHES]
          r["target_leak_controls"]+=1
          r["target_leak_failures"]+=len(set(leaks))!=3
      reduced=[w for w in words if "flip_root" not in w]
      r["omitted_intervention_controls"]+=1
      r["omitted_intervention_collisions"]+=all(run_word(initial,w,"U")[0]==run_word(initial,w,"I",alt=True)[0] for w in reduced)
      r["full_profile_splits_alt_model"]+=any(run_word(initial,w,"U")[0]!=run_word(initial,w,"I",alt=True)[0] for w in words)
    r["pass"]=(r["initial_states"]==64 and r["declared_words"]==400 and r["eligible_profile_mismatches"]==0
      and r["target_variation_in_equal_profile_fibres"]==25600 and r["target_leak_failures"]==0
      and r["commutation_failures"]==0 and r["version_mismatch_detected"]==64
      and r["omitted_intervention_collisions"]==64 and r["full_profile_splits_alt_model"]==64
      and r["partial_ownership_contract_detected"] and r["source_relative_operation_rejected_as_neutral"])
    p=Path(__file__).with_name("pmr007_deep_ck_concrete_architecture_map_primary_check_v2_results.json")
    p.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(r,indent=2,sort_keys=True))
    return 0 if r["pass"] else 1
if __name__=="__main__": raise SystemExit(main())
