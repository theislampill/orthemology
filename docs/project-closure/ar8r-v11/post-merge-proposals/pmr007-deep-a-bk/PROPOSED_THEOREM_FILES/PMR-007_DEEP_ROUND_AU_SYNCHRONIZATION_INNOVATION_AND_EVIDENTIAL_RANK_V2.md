# PMR-007 Deep Round AU V2 — Synchronization deficit and provenance-innovation rank balance

## Disposition candidate

```text
identity: PMR-007-SIER-1
provenance: POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
general mathematical novelty: 0
external review: OPEN
owner adoption: PENDING
```

## 1. Frozen typed setting

Let `F` be a field.  Before applying the theorem, an independently warranted
root-authentication and claim-relevance contract supplies a finite-dimensional
root space `V`.  Equivalently, `V` may be the quotient of a raw root-label
space by a frozen claim-irrelevance/alias relation.  The theorem neither
constructs nor validates that contract.

Rows of a matrix `A` in `V` are declared linear root signatures of agents,
reports, artifacts, or evidence objects.  Define

```text
E = row(A)
rho_before = dim(E).
```

A deterministic linear synchronization/copying operator acts on rows by left
multiplication with `B`:

```text
S = row(BA) <= E
rho_sync = dim(S)
delta_sync = dim(E) - dim(S).
```

Later acquisitions live in `V direct-sum W`, where `W` is a separately
authenticated fresh-root space.  Let `Q = row(C)` for
`C=[C_old|C_fresh]`, and embed `S` as `S0=S direct-sum {0}`.  Put

```text
U = S0 + Q
rho_after = dim(U)
gamma_total = dim(U) - dim(S0)
gamma_fresh = dim(proj_W(U)) = rank(C_fresh)
gamma_old = dim(U intersect (V direct-sum {0})) - dim(S0).
```

`rho`, `delta_sync`, and the `gamma` coordinates are **scoped linear
provenance/root-span quantities**.  They are not truth, testimonial warrant,
tawatur, common knowledge, recipient authorization, numerical identity, or a
general causal-independence measure.

## 2. SIER-1A — deterministic linear synchronization monotonicity


a) `S <= E`, hence

```text
rank(BA) <= rank(A).
```

b) `delta_sync >= 0`, and `delta_sync=0` exactly when synchronization
preserves the full declared old-root span:

```text
row(BA)=row(A).
```

c) Duplicating rows, replaying the same artifact, or making additional exact
copies leaves the rank unchanged.

### Proof

Every row of `BA` is an `F`-linear combination of rows of `A`; therefore
`row(BA) <= row(A)`.  Dimension monotonicity gives (a), and equality of finite
subspaces gives (b).  A duplicate row lies in the existing row span, proving
(c).

## 3. SIER-1B — exact synchronization/innovation balance

There is a short exact-sequence decomposition of the post-synchronization
innovation quotient:

```text
0
→ ((U intersect (V direct-sum 0))/S0)
→ (U/S0)
→ proj_W(U)
→ 0.
```

Consequently,

```text
gamma_total = gamma_old + gamma_fresh
```

and the exact rank balance is

```text
rho_after
= rho_before - delta_sync + gamma_old + gamma_fresh.
```

### Proof

Projection `pi_W: U → W` has kernel `U intersect (V direct-sum 0)` and image
`proj_W(U)`.  Since `S0` lies in the kernel, projection descends to `U/S0`.
Rank-nullity yields the displayed dimension identity.  Substituting
`rho_sync=rho_before-delta_sync` gives the balance law.

## 4. Interpretation of the two innovation terms

```text
gamma_old:
  old-root directions erased or absent from the synchronized visible span but
  recovered by later acquisition;

gamma_fresh:
  dimension of genuinely fresh authenticated root directions exposed by the
  new acquisitions.
```

A new acquisition may increase rank with `gamma_fresh=0` by recovering old
information.  This is the defect in V1.  Conversely, nonzero fresh projection
forces at least that much total innovation:

```text
gamma_total >= gamma_fresh.
```

## 5. SIER-1C — root contraction and false multiplicity

Let `R: V → V'` be a declared linear root-identification/contraction map.  Then

```text
rank(A R) <= rank(A).
```

Thus alias resolution can lower displayed rank.  Forty copies of one row have
apparent multiplicity forty and root-span rank one.  Two independently rooted
rows may have the same current output under a lossy projection while retaining
rank two.

This separates:

```text
availability count;
root-span rank;
current-output equality;
lineage;
and claim-relative warrant.
```

## 6. Mandatory countermodels and controls

### AU-CM1 — old-root recovery refutes V1

```text
A = [[1,0],[0,1]]
B = [[1,0]]
C_old = [[0,1]]
C_fresh = [[0]].
```

Synchronization leaves rank one; later acquisition restores the second old
root direction.  `rho_after=2` while V1 predicted one.

### AU-CM2 — copied-root false multiplicity

Three or forty identical rows have rank one.  Copy count does not manufacture
an independent acquisition direction.

### AU-CM3 — unauthenticated label alias

Displayed labels may yield the identity matrix of rank two while the actual
root map contracts both labels to one root.  The displayed rank cannot certify
root authenticity.

### AU-CM4 — same output, independent convergence

Rows `e1` and `e2` have root-span rank two, although a projection such as
`x1+x2` can map both current episodes to the same registered output.  Output
identity does not settle root identity.

### AU-CM5 — total synchronization

A rank-two old evidence span can be mapped to a one-dimensional common summary,
creating `delta_sync=1`.  Availability at every recipient may increase while
registered root-direction diversity decreases.

### AU-CM6 — claim-irrelevant inflation

An independent coordinate irrelevant to the target can raise raw matrix rank.
This is why the claim-relevance quotient must be fixed before computing the
scoped invariant.

## 7. Program effects

### Candidate A / TAC–SAC

The result supplies a computable candidate invariant for the V11 milestone
`PROVENANCE_INDEPENDENCE_RANK` and a linear component of
`SYNCHRONIZATION_DIVERSITY_DEFICIT`.  It does not recover historical TAC/SAC
terms or decide Tachikoma identity.

### Candidate B / restoration

Synchronization can delete provenance directions needed for later diagnosis or
repair.  A restorative system that reports only copy count or current output
can miss `delta_sync`; later evidence can restore old directions
(`gamma_old`) or add genuinely fresh directions (`gamma_fresh`).  Turning this
into operational repair capacity needs an additional causal/route model.

### Candidate C / source and transcendental lanes

Multiple presentations of one source do not become independent support by
copying.  The rank theorem supplies no source truth, world bridge, or
metaphysical unity result.

### Theorem origin

Duplicated theorem files, paraphrases, or model restatements do not create new
origin directions unless a separately authenticated derivation/root enters the
model.  This is an application, not a theorem-origin assignment.

## 8. Ancestry, authority, and nonclaims

```text
mathematical family:
standard finite-dimensional rank, quotient, and rank-nullity identities

historical AR8R-T100:
ancestor/control for pure copying and provenance-root preservation

AR2/AR3:
application interface for reason-bearing synchronization and diversity loss

Deep AR:
information-theoretic/data-processing ancestor at distribution level

Round 19:
authenticated root-access interface

current false-tawatur fixtures:
implementation/source-status comparator only

historical TAC/SAC identity:
NONE ASSIGNED

general mathematical novelty:
0
```

The result does not establish probabilistic independence, honesty, competence,
tawatur warrant, truth, causal independence, common knowledge, numerical or
episode identity, or a complete nonlinear synchronization theorem.
