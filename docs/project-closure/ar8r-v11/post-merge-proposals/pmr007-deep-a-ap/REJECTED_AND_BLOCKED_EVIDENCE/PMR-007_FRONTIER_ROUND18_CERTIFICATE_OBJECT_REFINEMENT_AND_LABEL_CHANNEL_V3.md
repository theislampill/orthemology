# PMR-007 Frontier Round 18 V3 — certificate-object refinement and exact-label channel

```text
version: V3
provenance: NEW_POST_MERGE_RESEARCH
status: FROZEN_BLOCKED_FORMAL_DEFECT
historical identity: NONE
```

V3 repairs the V1 action/object collapse.  Let `K` be a finite set of complete
certificate objects, `H(q) subseteq K` the objects admitted at concrete state
`q`, and `act : K -> A` the surface action projection.  For an observation cell
`C` and object `k`, put

```text
S_C(k) = {q in C : k in H(q)}
```

and let `rho_H(C)` be the minimum number of these supports covering `C`.
The exact-state deterministic minimum message alphabet is `rho_H(C)`.  The
surface-action cover can be strictly smaller because distinct complete objects
may project to one action.

V3 then proposed the following robust-channel claim:

```text
V3-LABEL-CHANNEL (OVERSTRONG):
under r adversarial symbol errors, a robust certificate selector exists exactly
when the transmitted selector labels form a code of minimum distance > 2r.
```

This claim identifies successful relation selection with exact recovery of a
preselected selector label.  It is frozen here solely so the defect and its
repair cannot disappear from custody.
