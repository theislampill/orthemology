# Deep CN V1 cold audit

## Disposition

```text
REPAIR_REQUIRED
```

## Blocking findings

### CN-F01 — totality and semantic identity of anchors were unstated

The finite cover theorem assumes every eligible anchor has a total, stable value map on the frozen model class in that context. A same-named anchor with architecture-dependent semantics cannot be treated as one anchor.

### CN-F02 — context eligibility was at risk of self-authorization

`A_c` is externally supplied. The theorem does not prove that an anchor is authorized, source-faithful, version-valid, implementable, or world-adequate.

### CN-F03 — cardinality was at risk of being read as epistemic cost

`kappa` counts anchors in a frozen registry. It is not evidence strength, proof length, resource cost, or metaphysical complexity. A weighted variant requires independently warranted costs.

### CN-F04 — model-class and exact-evidence scope were unstated

The theorem is finite, deterministic, complete-profile, and class-relative. It does not cover noisy observations, statistical identification, unknown model classes, adaptive evidence acquisition, or actual-world selection.

### CN-F05 — cross-context monotonicity needs stable maps

Eligibility expansion is monotone only when old anchor value maps and meanings are preserved. Version drift or reinterpretation can invalidate the inclusion comparison.

### CN-F06 — transport between contexts needs its own typed contract

A Track-N source anchor, neutral experiment, or recipient-version certificate cannot migrate merely because the abstract partition is extensionally similar.

### CN-F07 — the three applications were at risk of false unification

Architecture classification, recipient adoption, and source-world reference have different target types and native guards. The common structure is a typed conflict-cover layer, not identity of the domains.

### CN-F08 — theorem-family ancestry and novelty were missing

The core is constrained set cover plus fibre constancy, extending Deep BX/CL and the AR8R-T294 family with an explicit context index. It receives no independent general novelty credit.

### CN-F09 — the first primary checker was defective

Its direct identification oracle wrongly required the number of joint signatures to equal the number of target values, thereby rejecting legitimate refinements that split one target class. Preserve that failed checker and use the corrected V2 only.

## Required repair

Type eligible anchors as total stable maps; make authority external; restrict `kappa` to registry cardinality; state finite exact scope; guard monotonicity by map preservation; require typed context transport; preserve domain nonidentity; classify ancestry; and retain the failed checker as negative evidence.
