# PMR-007 Deep AU V1 cold audit

```text
audit disposition: REPAIR_REQUIRED
frozen packet: PMR-007_DEEP_AU_V1_FROZEN_HASHES.sha256
audit relation: same-session procedural cold audit over frozen bytes
external independence: NOT CLAIMED
```

## Blocking findings

### AU-F01 — the proposed fresh-root balance law is false

V1 claimed

```text
rho_after = rho_before - delta_sync + rank(C_fresh).
```

The primary checker found 375 counterexamples in the declared exhaustive
`GF(2)` class.  The minimal mechanism is old-root recovery: synchronization can
erase an old root direction and a later observation can recover that direction
while `C_fresh` has rank zero.  Preserve V1 as rejected evidence and replace the
claim by a quotient-space decomposition that separately records recovered old
root directions and genuinely fresh-root directions.

### AU-F02 — linear root-span rank was too close to unqualified evidential independence

A matrix rank counts independent directions only after an authenticated root
basis, root-independence model, and claim-relevance boundary have been supplied.
It does not establish testimonial independence, honesty, competence, truth,
tawatur warrant, recipient warrant, or causal independence.  The repaired
statement must call the quantity a scoped provenance/root-span rank and expose
the missing semantic guards.

### AU-F03 — claim relevance was stipulated but not typed

Irrelevant independent roots can raise raw rank without supplying evidence for
the target claim.  Require an independently frozen claim-relevance quotient (or
state that the displayed root space is already that quotient).  The theorem
must not define relevance by the result it is intended to support.

### AU-F04 — synchronization scope was overgeneralized

Left multiplication `BA` models a deterministic linear aggregation/copying
step.  It does not cover arbitrary nonlinear, stochastic, adaptive,
cryptographic, or history-dependent synchronization.  Restrict the theorem and
record the broader program as open.

### AU-F05 — rank loss was described as future-diversity loss without a bridge

`dim row(A)-dim row(BA)` is loss of declared linear root directions.  It may
correlate with reduced exploratory or policy diversity, but it is not itself a
general future-diversity, epistemic-diversity, or repair-capacity measure.
Rename it `linear synchronization deficit` and leave operational diversity to a
separate bridge.

### AU-F06 — displayed labels and actual roots were not sufficiently separated

A displayed two-label matrix can have rank two while both labels denote one
actual acquisition root.  Root authentication and alias resolution precede the
rank computation.  Add the alias countermodel to the theorem packet and forbid
machine rank from certifying root authenticity.

### AU-F07 — root contraction and copying need exact typed readings

Right multiplication by a root-identification map and row duplication are
standard rank-nonincreasing operations.  State which side acts on agents and
which side acts on root coordinates; otherwise the same notation can hide a
change of semantic object.

### AU-F08 — theorem-family and novelty ceilings were incomplete

The mathematics is standard finite-dimensional linear algebra.  Historical
AR8R-T100, AR2/AR3 synchronization work, current false-tawatur fixtures, Deep AR
data processing, and Round 19 authenticated-root access are ancestors or
interfaces.  Any value is an orthemological invariant/application, not new
general mathematics and not a recovered TAC/SAC theorem.

### AU-F09 — identity and episode overreads remain live

Equal, reduced, or increased root-span rank does not settle numerical identity,
carrier identity, episode identity, memory continuity, lineage identity, or a
Tachikoma verdict.  Preserve the historical TAC/SAC terminology gap.

## Required repair

1. Preserve V1 and its 375 counterexamples.
2. Define the old-root recovery term by a quotient/intersection dimension.
3. Prove an exact rank-balance identity.
4. Type claim relevance, root authentication, field, and linearity.
5. Retain copied-root, common-bottleneck, independent-convergence, alias, and
   total-synchronization controls.
6. Run a distinct rereview over a different field and a span-enumeration method.
