# PMR-007 Deep AR distinct-rereview harness repair log

```text
preserved failed harness: pmr007_deep_ar_distinct_joint_root_rereview_v2.py
preserved failed result: pmr007_deep_ar_distinct_joint_root_rereview_v2_results.json
disposition: HARNESS_DEFECT_NOT_THEOREM_DEFECT
```

The first distinct harness required `L² != L` as the common-cause overcount witness for every finite likelihood ratio. That is false at `L=0` (and also nondiagnostic at `L=1`; `∞` requires extended handling). The V2 theorem already restricted the naive-copy witness to finite informative ratios outside `{0,1}`.

The repaired V3 harness:

1. tests exact copy conservation for all support cases;
2. tests strict naive-exponentiation mismatch only for finite `L not in {0,1}`;
3. handles zero, undefined, and infinite ratios by support classification rather than arithmetic exponentiation;
4. independently checks two-root factorization, common-cause contraction, and alias partitions.

No theorem statement or model assumption changed because of this harness repair.
