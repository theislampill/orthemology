# Deep CQ V1 — robust restoration under proper-function and norm-source uncertainty

## Candidate

```text
identity: PMR-007-NURV-1
status: POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
```

Let `S` be a finite state space, `H` a finite nonempty set of live
proper-function or norm-source hypotheses, and `A` a finite action set. For each
`h in H`, let `T_h` be its target region, `A_h(s)` its eligible actions, and
`F_h(s,a)` its deterministic successor.

The controller sees the current state but not a privileged correct standard.
At every step an adversary may select any `h in H`. Define

```text
A_*(s) = intersection_h A_h(s)
T_*    = intersection_h T_h
Pre_H(X) = {s : exists a in A_*(s), forall h, F_h(s,a) in X}.
```

Define

```text
V_H = nu X. [T_* intersect Pre_H(X)]
W_H = mu Z. [V_H union Pre_H(Z)].
```

The candidate claims that `V_H` is exactly the robust stable-restoration region
and `W_H` exactly the robust finite reach-and-stay region under the declared
switching-standard semantics. It further claims that independently warranted
restriction of `H` can only enlarge those regions.

The candidate is intended to connect the proper-function target-fixing problem
to daee/restorative route selection. It does not decide which standard is true.
