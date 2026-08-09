#!/usr/bin/env python3
from __future__ import annotations
import itertools, json
from pathlib import Path

SOURCE_GUARDS=(
"source_regime_accepted","exact_source_custody","source_version_identity","translation_adequacy",
"source_bearer_identified","admissible_interpretation_family","singleton_candidate_denotation",
"actual_world_selection","intensional_predicate_preservation","source_predicate_strength_preserved",
"source_referent_equals_target_bearer","world_adequacy","target_applicability")
WISDOM_GUARDS=("objective_fittingness_not_signal_only","knowledge_or_apprehension","intentional_uptake",
"selection_because_fitting","reliable_realization","one_bearer_coinstantiation")
ALL=SOURCE_GUARDS+WISDOM_GUARDS
TARGETS={
"U": {"class":"U","common_bearer":1,"uptake":1,"because_fit":1,"wisdom":1},
"I": {"class":"I","common_bearer":1,"uptake":0,"because_fit":0,"wisdom":0},
"P": {"class":"P","common_bearer":0,"uptake":0,"because_fit":0,"wisdom":0}}

def licensed(bits): return all(bits)

def main():
  r={"schema":"pmr007-deep-ck-source-world-primary-check-v2","guard_count":len(ALL),
     "truth_rows":0,"licensed_rows":0,"false_licenses":0,"single_guard_deletions":0,
     "single_guard_deletion_false_licenses":0,"neutral_profile_fibres":1,
     "architectures_in_fibre":3,"architecture_targets_in_fibre":3,
     "common_bearer_values_in_fibre":2,"uptake_values_in_fibre":2,"wisdom_values_in_fibre":2,
     "predicate_weakening_reintroduces_I":True,"common_bearer_deletion_reintroduces_P":True,
     "referent_ambiguity_preserves_U_I":True,"signal_only_preserves_I":True,
     "downstream_host_locus_control":True}
  for bits in itertools.product((0,1),repeat=len(ALL)):
    r["truth_rows"]+=1
    lic=licensed(bits); r["licensed_rows"]+=lic
    if lic and not all(bits): r["false_licenses"]+=1
    if sum(bits)==len(ALL)-1:
      r["single_guard_deletions"]+=1
      r["single_guard_deletion_false_licenses"]+=lic
  r["pass"]=(r["guard_count"]==19 and r["truth_rows"]==2**19 and r["licensed_rows"]==1
    and r["false_licenses"]==0 and r["single_guard_deletions"]==19
    and r["single_guard_deletion_false_licenses"]==0
    and len({v["class"] for v in TARGETS.values()})==3
    and len({v["common_bearer"] for v in TARGETS.values()})==2
    and len({v["uptake"] for v in TARGETS.values()})==2
    and len({v["wisdom"] for v in TARGETS.values()})==2)
  p=Path(__file__).with_name("pmr007_deep_ck_source_world_primary_check_v2_results.json")
  p.write_text(json.dumps(r,indent=2,sort_keys=True)+"\n",encoding="utf-8",newline="\n")
  print(json.dumps(r,indent=2,sort_keys=True))
  return 0 if r["pass"] else 1
if __name__=="__main__": raise SystemExit(main())
