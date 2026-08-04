# PMR-007 Frontier Round 14 V1 fresh rereview — blocking finding

```text
review relation: same-model procedurally distinct rereview over frozen V1 hashes
external human review: false
independent model-lineage review: false
disposition: REPAIR_REQUIRED
```

The rereview reproduced all frozen hashes, then checked V1 against a direct
co-Büchi (`eventually always Target`) temporal criterion using reachable SCCs.
It found a concrete countermodel to V1's claimed equivalence.

## R14-F01 — invariant-core attractor is too strong for general reach-and-stay

Use three safe states with `Target={0,2}` and locally admissible actions:

```text
state 0:
  {0}                 available

state 1:
  {0}                 available

state 2:
  {0,1,2}             the only available successor set
```

A memoryless strategy is forced at state 2 and can choose the displayed actions
at states 0 and 1. Every adversarial path from state 2 either:

```text
stays at target state 2 forever;

or

leaves 2 for transient non-target state 1 and then reaches invariant target
state 0 forever.
```

Hence every path is eventually always in `Target`. But state 2 is not in V1's
greatest target-invariant kernel because its action admits successor 1, and it
is not in the strict attractor to that kernel because its successor set also
contains itself. V1 therefore returns

```text
W_core={0,1}
```

while the exact co-Büchi winning region is

```text
W_coBuchi={0,1,2}.
```

The frozen rereview stopped after the first mismatch:

```text
games checked before mismatch:          506
memoryless strategies checked:        3,984
frozen-hash mismatches:                   0
```

## Scope diagnosis

V1's construction remains valid for the stronger objective:

```text
force finite entry into one controller-invariant target kernel K.
```

It is not complete for the weaker/general objective:

```text
eventually remain in Target,
```

which permits target-state stuttering and branch-dependent eventual target
components before the last non-target visit.

This distinction is substantively relevant to restoration:

```text
certified entry into one invariant core
!=
general eventual target persistence.
```

## Required repair

Preserve V1 and add a V2 that:

1. names the original set `W_core` and limits it to finite invariant-core entry;
2. supplies the exact nested fixed point for the co-Büchi region;
3. proves `W_core subseteq W_coBuchi` and preserves the strict counterexample;
4. distinguishes a common invariant-core certificate from branch-dependent
   eventual target persistence;
5. reruns executable checks against direct temporal/SCC semantics.
