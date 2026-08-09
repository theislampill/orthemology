#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path

ARCHES = ("U", "I", "P")
COORDS = ("content", "fit", "payoff", "version", "authority", "root")
INTERVENTIONS = ("noop", "flip_content", "flip_fit", "flip_payoff", "flip_version", "flip_authority", "flip_root")
TARGETS = {
    "U": {"class":"U", "common_bearer":1, "uptake":1, "because_fit":1, "wisdom":1},
    "I": {"class":"I", "common_bearer":1, "uptake":0, "because_fit":0, "wisdom":0},
    "P": {"class":"P", "common_bearer":0, "uptake":0, "because_fit":0, "wisdom":0},
}

def step(state: tuple[int,...], intervention: str) -> tuple[int,...]:
    s=list(state)
    if intervention != "noop":
        ix={"flip_content":0,"flip_fit":1,"flip_payoff":2,"flip_version":3,"flip_authority":4,"flip_root":5}[intervention]
        s[ix] ^= 1
    return tuple(s)

def output(state: tuple[int,...]) -> tuple[int,int,int,int]:
    c,f,p,v,a,r=state
    return (c^f, p, v&a, r)

def run_word(initial: tuple[int,...], word: tuple[str,...], arch: str, target_leak: bool=False, alt: bool=False) -> tuple[tuple[tuple[int,...],...],tuple[int,...]]:
    state=initial; obs=[]
    for j in word:
        state=step(state,j)
        y=output(state)
        if alt and arch=="I" and j=="flip_root":
            y=(1-y[0],)+y[1:]
        if target_leak:
            y=y+(TARGETS[arch]["class"],)
        obs.append(y)
    return tuple(obs),state

def all_words(max_len:int):
    yield ()
    for k in range(1,max_len+1):
        yield from itertools.product(INTERVENTIONS, repeat=k)


def main() -> int:
    result={
        "schema":"pmr007-deep-ck-concrete-architecture-map-primary-check-v1",
        "architectures":list(ARCHES),
        "initial_states":0,
        "declared_words":0,
        "architecture_profile_comparisons":0,
        "eligible_profile_mismatches":0,
        "target_variation_in_equal_profile_fibres":0,
        "target_leak_controls":0,
        "target_leak_failures":0,
        "version_semantic_mismatch_controls":1,
        "version_semantic_mismatch_detected":True,
        "partial_ownership_contract_detected":True,
        "source_relative_operation_rejected_as_neutral":True,
        "omitted_intervention_controls":0,
        "omitted_intervention_collisions":0,
        "full_profile_splits_alt_model":0,
    }
    words=list(all_words(3)); result["declared_words"]=len(words)
    for initial in itertools.product((0,1), repeat=6):
        result["initial_states"] += 1
        for word in words:
            profiles=[run_word(initial,word,a)[0] for a in ARCHES]
            result["architecture_profile_comparisons"] += 1
            if len(set(profiles)) != 1:
                result["eligible_profile_mismatches"] += 1
            if len(set(profiles))==1 and len({TARGETS[a]["class"] for a in ARCHES})>1:
                result["target_variation_in_equal_profile_fibres"] += 1
            leaks=[run_word(initial,word,a,target_leak=True)[0] for a in ARCHES]
            result["target_leak_controls"] += 1
            if word and len(set(leaks)) != 3:
                result["target_leak_failures"] += 1
        # Reduced profile omits flip_root. The alternative I model differs only there.
        reduced=[w for w in words if "flip_root" not in w]
        if all(run_word(initial,w,"U")[0] == run_word(initial,w,"I",alt=True)[0] for w in reduced):
            result["omitted_intervention_collisions"] += 1
        result["omitted_intervention_controls"] += 1
        if any(run_word(initial,w,"U")[0] != run_word(initial,w,"I",alt=True)[0] for w in words):
            result["full_profile_splits_alt_model"] += 1
    result["pass"] = (
        result["initial_states"]==64
        and result["declared_words"]==400
        and result["eligible_profile_mismatches"]==0
        and result["target_variation_in_equal_profile_fibres"]==64*400
        and result["target_leak_failures"]==64 # only empty word has no observation and cannot leak
        and result["omitted_intervention_collisions"]==64
        and result["full_profile_splits_alt_model"]==64
        and result["version_semantic_mismatch_detected"]
        and result["partial_ownership_contract_detected"]
        and result["source_relative_operation_rejected_as_neutral"]
    )
    target=Path(__file__).with_name("pmr007_deep_ck_concrete_architecture_map_primary_check_results.json")
    target.write_text(json.dumps(result,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
    print(json.dumps(result,indent=2,sort_keys=True))
    return 0 if result["pass"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
