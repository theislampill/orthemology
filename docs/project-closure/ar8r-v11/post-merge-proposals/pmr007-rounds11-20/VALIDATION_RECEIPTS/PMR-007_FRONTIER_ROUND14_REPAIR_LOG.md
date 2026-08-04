# PMR-007 Frontier Round 14 blocking-repair log

```text
pre-repair packet:
  PMR-007_FRONTIER_ROUND14_LOCAL_PROTOCOL_REACH_AND_STAY_FIXED_POINT_V1.md

blocking finding:
  R14-F01

repair target:
  PMR-007_FRONTIER_ROUND14_LOCAL_PROTOCOL_REACH_AND_STAY_FIXED_POINT_V2.md
```

V1 conflated two objectives:

```text
CORE-ENTRY:
  force finite arrival at one declared target-invariant kernel;

CO-BUCHI TARGET:
  ensure that every path has only finitely many non-target visits.
```

The V1 greatest-kernel plus strict attractor exactly handles CORE-ENTRY but is
not complete for CO-BUCHI TARGET. V2 preserves the former as `W_core` and adds
the standard nested least/greatest fixed point for the latter. The countermodel
found by the rereview is retained as a strict-separation witness. No source,
causal, world-truth, novelty, or meniscus status is upgraded.
