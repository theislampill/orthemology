# PMR-007 Deep Round AU V1 — Synchronization, innovation, and provenance-root rank

## Status

```text
identity: PMR-007-SIER-1-CANDIDATE-V1
provenance: POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
general mathematical novelty: NOT CLAIMED
```

## 1. Typed finite linear model

Fix a field `F`.  A declared old acquisition-root space is `V = F^r`; its
coordinates are assumed, for this model only, to be authenticated, mutually
independent acquisition roots and relevant to the frozen claim family.  Agent
or artifact evidence rows form a matrix `A` with row space `E <= V`.

A deterministic linear synchronization/copying operator is a matrix `B`; the
post-synchronization visible evidence is `BA`, with row space `S <= E`.

Later acquisitions are rows of

```text
C = [C_old | C_fresh]
```

in `V direct-sum W`, where `W = F^s` is a declared fresh-root space.  The
post-acquisition evidence matrix is the stack of `[BA | 0]` and `C`.

Define:

```text
rho_before = rank(A)
rho_sync   = rank(BA)
delta_sync = rho_before - rho_sync
rho_after  = rank(stack([BA|0], C))
```

`rho` is a **declared linear root-span rank**.  It is not testimonial warrant,
tawatur, truth, recipient authorization, common knowledge, numerical identity,
or a general measure of epistemic independence.

## 2. V1 candidate claims

### SIER-1A — synchronization monotonicity

```text
rank(BA) <= rank(A).
```

Thus deterministic linear copying or synchronization cannot create a new
linear acquisition-root direction.

### SIER-1B — copied multiplicity

Duplicating any row of `A` leaves `rank(A)` unchanged.  Apparent witness count
can grow while declared root-span rank remains fixed.

### SIER-1C — proposed fresh-root balance law

V1 proposes:

```text
rho_after = rho_before - delta_sync + rank(C_fresh).
```

The intended reading is that synchronization loses `delta_sync` dimensions and
only fresh independent roots can restore them.

### SIER-1D — root contraction

For any declared linear root-identification/contraction map `Q`,

```text
rank(AQ) <= rank(A).
```

Merging two displayed labels into one authenticated root cannot increase the
rank.

## 3. Intended applications and ceilings

The candidate is intended to connect:

- TAC/SAC copying and synchronization;
- false-tawatur/common-source controls;
- AR2/AR3 reason-bearing synchronization;
- Deep AR provenance-root evidence conservation;
- Round 19 authenticated-root query access;
- theorem-origin false multiplicity; and
- meta-noetic synchronization versus future repair diversity.

No historical TAC/SAC term is assigned.  No claim is made that linear rank is
the complete criterion for real evidential independence.
