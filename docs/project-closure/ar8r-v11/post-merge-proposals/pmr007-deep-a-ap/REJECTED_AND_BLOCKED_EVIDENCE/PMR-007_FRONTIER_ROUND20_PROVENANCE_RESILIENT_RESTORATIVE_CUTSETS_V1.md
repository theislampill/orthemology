# PMR-007 Frontier Round 20 V1 — provenance-resilient restorative cutsets

```text
round: PMR-007-FRONTIER-ROUND20
candidate identity: PMR-007-PRRC-1
provenance: NEW_POST_MERGE_RESEARCH
historical identity: NONE
current disposition: FROZEN_PENDING_COLD_AUDIT
repository mutation: NONE
integrated champion: NONE
meniscus: MENISCUS_NOT_REACHED
```

## 1. Central burden

T351 establishes that a stable restorative intervention must intersect, disable,
or semantically neutralize every registered error-effective deformation path.
T352 makes sufficiency conditional on path completeness, local effectiveness and
soundness, no new path, target adequacy, custody, and reread. T353 shows why a
correct output may coexist with an unrepaired self-sealing governor.

Those results do not yet measure resilience to common-source corruption. A
portfolio may display many blockers while all blockers inherit one acquisition,
source, version, authority, or provenance root. Round 20 isolates the exact
finite static support-level invariant.

## 2. Frozen model

A **finite static fixed-path provenance-cutset instance** is

```text
N = <R,P,A,I,Block,Dep>
```

where:

- `R` is a finite set of authenticated canonical provenance roots;
- `P` is a finite nonempty and complete registry of target-relevant paths for
  the declared case class;
- `A` is a finite set of restorative actions;
- `I subseteq A` is the frozen portfolio;
- `Block(a,p)` says that action `a`, if operative, blocks path `p`;
- `Dep(a)` is a nonempty subset of `R` containing every root whose integrity is
  conjunctively required for `a` to remain operative.

A static corruption set `C subseteq R` disables `a` exactly when

```text
Dep(a) intersects C.
```

Thus corruption of any required root disables the action. This is not the
alternative redundancy semantics under which all roots must be corrupted.

For each path `p`, define the blocker-root hypergraph

```text
H_p(I) = { Dep(a) : a in I and Block(a,p) }.
```

Duplicate actions with the same root support and path role do not create a new
hyperedge. Set

```text
tau(empty hypergraph) = 0,
```

because a path with no blocker already fails under the empty corruption. For a
nonempty hypergraph `H`, `tau(H)` is the minimum cardinality of a root set that
intersects every hyperedge.

Define

```text
kappa(I) = min over p in P of tau(H_p(I)).
```

For an integer `f >= 0`, the portfolio is **static support-robust through f** iff

```text
for every C subseteq R with |C| <= f,
for every p in P,
there exists a in I such that Block(a,p) and Dep(a) is disjoint from C.
```

The quantifier order is `for every static corruption, there exists a surviving
blocker`. The theorem does not permit an adversary to wait for one committed
action and then choose its root, and it does not model repeated corruption with
a replenished budget.

## 3. PRRC-1 — exact static characterization

### Theorem

For every finite static fixed-path provenance-cutset instance and every
`f >= 0`,

```text
I is static support-robust through f
iff
kappa(I) > f.
```

### Proof

Assume first that `kappa(I) <= f`. Choose a registered path `p` with
`tau(H_p(I)) <= f`, and let `C` be a minimum transversal of `H_p(I)`. Every
portfolio action that blocks `p` has a required-root set intersecting `C`, so
every such action is disabled. The portfolio fails on `p` under a corruption of
at most `f` roots.

Conversely, suppose the portfolio fails static support robustness through `f`.
Then some corruption set `C`, `|C| <= f`, and some registered path `p` have no
surviving blocker. Hence `C` intersects `Dep(a)` for every portfolio action that
blocks `p`: `C` is a transversal of `H_p(I)`. Therefore

```text
tau(H_p(I)) <= |C| <= f,
```

and `kappa(I) <= f`. Taking contraposition yields the result. QED.

## 4. Exact monotonicity and multiplicity consequences

Under the same frozen semantics:

1. **Copied-action invariance.** Adding another action with the same path roles
   and the same actual root set does not change `kappa`.
2. **Portfolio enlargement.** Adding genuinely available blocker actions can
   only weakly increase `kappa`.
3. **Action deletion.** Deleting blocker actions can only weakly decrease
   `kappa`.
4. **Root contraction.** If displayed roots are identified by a map
   `q:R -> R'`, replacing every support `E` by `q(E)` can only weakly decrease
   `kappa`.
5. **Apparent multiplicity boundary.** Action count, graph degree, copied
   availability, or distinct displayed labels do not lower-bound actual
   resilience without authenticated root identity.

These are support-level facts. They do not establish source truth, evidential
independence, recipient warrant, or execution authorization.

## 5. Strongest positive construction

Fix `f >= 0`. For every registered path `p`, provide `f+1` compatible blockers

```text
a_{p,0}, ..., a_{p,f}
```

with pairwise distinct singleton root supports

```text
Dep(a_{p,i}) = {r_{p,i}}.
```

Then `tau(H_p)=f+1` for every path, so `kappa(I)=f+1`; every corruption of at
most `f` roots leaves at least one blocker per path. If the actions are also
jointly executable and satisfy T352's semantic guards, this support certificate
can contribute to an execution-level restoration certificate. PRRC-1 alone does
not supply those additional guards.

## 6. Mandatory countermodels and scope boundaries

### R20-CM1 — copied-root false multiplicity

One path has many blockers, all with support `{r0}`. The portfolio size is
arbitrarily large but `kappa=1`. One root corruption disables every copy.

### R20-CM2 — common bottleneck

Blockers have supports `{r0,r1}`, `{r0,r2}`, ..., `{r0,rn}`. Every action has a
second distinct root, yet `{r0}` hits them all and `kappa=1`.

### R20-CM3 — incompatible repairs

Two paths have blockers `a` and `b` on independent roots, so `kappa=1` and the
portfolio is support-robust through `f=0`. But `a` and `b` cannot be jointly
executed: each disables a prerequisite of the other. Pathwise support existence
therefore does not establish executable restoration.

### R20-CM4 — dynamic rerouting

The complete frozen registry contains only `p0`, blocked by `a`. Executing `a`
changes the system and creates a new path `p1` not in the frozen registry.
PRRC-1 certifies the declared fixed-path model, while real restoration fails.
This is T352's no-new-path and completeness burden, not a contradiction of
PRRC-1.

### R20-CM5 — adaptive corruption after commitment

One path has two blockers on `{r1}` and `{r2}`, so `kappa=2` and static support
robustness through `f=1` holds: after any fixed one-root corruption, one blocker
survives. If the controller must commit to one blocker before the adversary
chooses a root, the adversary corrupts the chosen blocker's root. The changed
quantifier order is not characterized by `kappa`.

### R20-CM6 — unauthenticated-root ambiguity

Displayed supports `{x}` and `{y}` appear independent, but both labels resolve
to one actual root `r`. Apparent `kappa=2`; actual `kappa=1`. Authentication and
alias resolution are load-bearing.

### R20-CM7 — partial path registry

The registered path `p0` has `f+1` independent blockers, while an omitted path
`p1` has none. The registry certificate passes and the operative system fails.
Path completeness is load-bearing.

### R20-CM8 — positive independent-root construction

For every path, `f+1` compatible singleton-root blockers give `kappa=f+1` and
survive every static corruption through `f` under the frozen assumptions.

## 7. Support, certification, and execution are distinct

```text
support existence:
  the frozen exact model contains a surviving path blocker;

model-relative certification:
  an authenticated complete registry plus a verified kappa computation
  certifies support robustness in that model;

execution-level restoration:
  additionally requires compatibility, local effectiveness and soundness,
  no new path, target adequacy, authorization, custody, and whole-field reread;

world-directed or human restoration:
  requires the declared model, roots, paths, target, and causal intervention
  to be adequate to the operative world and intended noetic target.
```

## 8. Ancestry and theorem-family disposition

- `AR8R-T351`: PRRC-1 refines path interception by root-corruption tolerance.
- `AR8R-T352`: all six sufficiency guards remain; PRRC-1 supplies neither path
  completeness nor semantic repair.
- `AR8R-T353`: output-local success and self-sealing governance remain possible.
- daee false-tawatur: apparent count is replaced by actual root-dependence.
- `TAWATUR-WARRANT`: root multiplicity remains separate from creed-internal
  warrant.
- Round 15: temporal model binding and future stability remain additional.
- Round 19: canonical-root access supplies a possible information interface but
  not authenticity or independence.
- AR2/AR3 and AGCOM: copied artifacts do not create new reason or acquisition
  roots.
- Candidate G theorem-family control: substituting roots for ordinary
  hypergraph vertices does not create a new general combinatorial origin.

```text
theorem-family relation:
STANDARD_HYPERGRAPH_TRANSVERSAL_CHARACTERIZATION_APPLIED_TO_PROVENANCE_CUTSETS

orthemological contribution:
EXACT_STATIC_PROVENANCE_RESILIENCE_INTERFACE_AND_FALSE_MULTIPLICITY_BOUNDARY

general mathematical novelty:
ZERO
```

## 9. Nonclaims

PRRC-1 does not establish:

- adaptive or mobile-adversary robustness;
- dynamic-rerouting robustness;
- joint executability or action compatibility;
- path completeness or root authentication;
- source truth or evidential independence;
- causal efficacy, target adequacy, or human restoration;
- one canonical scalar route-gradient;
- a new general theorem about hypergraphs;
- owner adoption or repository integration.
