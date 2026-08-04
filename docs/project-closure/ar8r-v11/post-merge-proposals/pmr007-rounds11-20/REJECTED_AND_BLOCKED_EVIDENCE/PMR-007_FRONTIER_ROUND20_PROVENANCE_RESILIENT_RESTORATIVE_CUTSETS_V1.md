# PMR-007 Frontier Round 20 V1 — provenance-resilient restorative cutsets

```text
round: PMR-007-FRONTIER-ROUND20
candidate identity: PMR-007-PRRC-1-V1
provenance: NEW_POST_MERGE_RESEARCH_CANDIDATE
historical identity: NONE
current disposition: FROZEN_PENDING_COLD_AUDIT
repository mutation: NONE
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
```

## 1. Central Candidate-A/B burden

T351 and T352 characterize pathway interception under path completeness,
local effectiveness, local soundness, no-new-path, target-adequacy, custody,
and reread guards.  They do not ask whether the apparent multiplicity of
available blockers survives corruption of a common provenance source.

Round 19 separates action-support multiplicity from canonical-root
multiplicity.  Round 20 asks the next exact question:

> When does a fixed restorative portfolio continue to block every declared
> error-effective target path after an adversary corrupts up to `f`
> provenance roots?

The candidate is initially scoped to a finite, static, fixed-path model.  It is
not a theorem about adaptive execution, dynamic rerouting, root
authentication, human restoration, or world truth.

## 2. Frozen V1 model

Let:

```text
P:
  a nonempty finite and complete registry of target-error paths;

I:
  a finite restorative portfolio chosen before corruption;

B(a) subseteq P:
  the paths blocked by action a;

R(a) subseteq U:
  the provenance-root set attached to action a;

F subseteq U:
  a static corruption set selected after I is visible, with |F| <= f.
```

A corrupted root disables every descendant action that depends on it.  An
action is available after `F` exactly when

```text
F intersect R(a) = empty.
```

The current V1 wording treats `R(a)` as the action's provenance-root support,
without yet separately naming the conjunctive-dependency reading versus a
redundant-alternative-support reading.  This semantic point is a required
cold-audit target.

The fixed portfolio survives `F` pathwise when

```text
for every p in P,
there exists a in I such that p in B(a) and F intersect R(a) = empty.
```

This is a certification/existence statement.  It assumes that all actions in
`I` are mutually compatible or that pathwise availability is the only target.
It does not yet certify a jointly executable schedule under action conflicts.

For each path `p`, define the blocker-root family

\[
\mathcal H_p(I)=\{R(a):a\in I,\ p\in B(a)\}.
\]

For a finite family `H` of subsets of `U`, let `tau(H)` be the minimum size of
`F subseteq U` that intersects every member of `H`.  Use the boundary
conventions:

```text
tau(empty family) = 0;

tau(H) = infinity if H contains the empty set.
```

Define

\[
\kappa(I)=\min_{p\in P}\tau(\mathcal H_p(I)).
\]

## 3. Candidate characterization PRRC-1-V1

### Candidate theorem

Under the frozen finite, static, fixed-path assumptions,

\[
I\text{ survives every corruption }F\text{ with }|F|\le f
\quad\Longleftrightarrow\quad
\kappa(I)>f.
\]

### Proof

Fix a path `p`.  A corruption `F` disables every blocker of `p` exactly when
it intersects every set in `H_p(I)`.  Therefore the minimum number of roots
whose corruption can leave `p` unblocked is `tau(H_p(I))`.

If `kappa(I) <= f`, choose a path `p` and a transversal `F` of size at most
`f`.  Every blocker of `p` is disabled, so the portfolio does not survive.

Conversely, if `kappa(I)>f`, then for every corruption set `F` with
`|F|<=f` and every path `p`, `F` is too small to hit every member of
`H_p(I)`.  Some blocker root set is disjoint from `F`, so some blocker of `p`
remains available.  Since `p` was arbitrary, the portfolio survives. ∎

## 4. Derived monotonicity controls

At the frozen static semantics:

```text
copied-action duplication:
  duplicating an action with the same path and root sets does not change kappa;

portfolio enlargement:
  adding blockers weakly increases kappa;

action deletion:
  deleting blockers weakly decreases kappa;

root contraction:
  identifying displayed roots can only weakly decrease kappa;

root refinement:
  splitting an actual root into merely displayed aliases cannot be credited
  unless the authentication map proves that the aliases are distinct roots.
```

## 5. Required positive witness

Let `P={p1,p2}`, `f=1`, and use four actions:

```text
a1 blocks p1 with R(a1)={r1};
a2 blocks p1 with R(a2)={r2};
a3 blocks p2 with R(a3)={r2};
a4 blocks p2 with R(a4)={r3}.
```

Each path's root family has transversal number `2`, so `kappa=2>1`.  Every
single-root corruption leaves at least one blocker on each path.

## 6. Required adversarial cases

### R20-CM-COPIED-ROOT

Arbitrarily many apparent blockers of one path all use `{r}`.  Their root
family has transversal number `1`; one corruption disables every copy.

### R20-CM-COMMON-BOTTLENECK

Blockers have root sets `{r,x1}`, `{r,x2}`, ..., so action count and displayed
root count are large while `tau=1` because all actions depend on `r`.

### R20-CM-INCOMPATIBLE-REPAIRS

Path `p1` is blocked only by `a`; path `p2` only by `b`; the roots are distinct,
but `a` and `b` cannot be jointly executed.  The pathwise theorem reports
robust availability at `f=0`, while an executable-portfolio claim fails.  Joint
compatibility is therefore outside V1 or must be added as a guard.

### R20-CM-DYNAMIC-REROUTING

The registry contains only `p_old`, which is blocked robustly.  Executing the
repair activates `p_new`, absent from `P`.  The fixed-path certificate passes
while dynamic restoration fails.  T352's path-completeness and no-new-path
guards remain load-bearing.

### R20-CM-ADAPTIVE-ONE-SHOT

Two one-root blockers protect one path, so `kappa=2`.  A one-shot controller
selects one blocker, after which an adaptive adversary corrupts that blocker's
root before execution.  Static set robustness does not imply robustness in
this sequential game.

### R20-CM-UNAUTHENTICATED-ROOTS

Displayed labels `r1` and `r2` are aliases of one actual root `r`.  Displayed
`kappa=2`, actual `kappa=1`.  Authentication is a precondition for applying the
theorem to displayed labels.

### R20-CM-PARTIAL-PATH-REGISTRY

Every registered path is robustly blocked, but an omitted error-effective path
has no blocker.  The theorem certifies only the declared complete registry.

### R20-CM-REDUNDANT-SUPPORT-SEMANTICS

One action has displayed support `{r1,r2}` and remains available whenever at
least one support survives.  Under this alternative semantics one corruption
does not disable the action, while the transversal formula gives `tau=1`.
The candidate therefore requires an exact dependency interpretation for
`R(a)` and does not automatically cover redundant alternative supports.

## 7. Ancestry and theorem-family ceiling

```text
T351:
  supplies path-interception necessity;

T352:
  supplies guarded sufficiency and the path-completeness/no-new-path firewall;

T353:
  supplies the output-correction/self-sealing control;

Round 15:
  supplies the distinction between event-local closure and model-bound
  temporal stability;

Round 19:
  supplies the canonical-root multiplicity/query interface;

false-tawatur and memetic-ecology records:
  supply the copying/common-source distinction but no creed-internal warrant;

hypergraph transversal theory:
  supplies the mathematical mechanism.
```

The candidate is a provenance-indexed compositional corollary/application of
standard transversal theory and T351/T352.  It receives no independent general
mathematical novelty credit merely because roots replace ordinary vertices.

## 8. Authority ceiling and nonclaims

Even if admitted, PRRC-1-V1 would establish only a fixed-model robustness
certificate.  It would not establish:

```text
that the path registry is complete;
that root identities are authentic;
that different roots are evidentially independent;
that repairs are compatible or executable;
that corruption is static;
that no new path appears;
that the target is correct;
that local repair is sound;
that burden landing or whole-field reread occurred;
that human or fitri restoration occurred;
or that a creed-internal tawatur warrant holds.
```
