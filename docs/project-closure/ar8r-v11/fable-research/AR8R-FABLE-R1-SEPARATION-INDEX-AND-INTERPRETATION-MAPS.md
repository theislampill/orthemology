# AR8R-FABLE-R1 — the separation index, three interpretation maps, and a split convergence verdict

Status: research candidate. Non-adopted. Zero general mathematical novelty is
claimed; see `AR8R-FABLE-R1-PRIOR-ART-AND-NOVELTY-CEILING.md`.

**Verification status (added after independent review).** No property stated as
"proved" in this packet is accompanied by a committed derivation, executable
check, or Lean theorem. Every such property is therefore downgraded to
`DERIVED_BUT_UNVERIFIED`: recorded as the author's derivation, checked by no one.
Exceptions, verified independently during review: the Domain 3 embedding's
transversal arithmetic (triangle and path countermodels, quorum range `n ≤ 7`)
via `checks/n1_transversal_packing_check.py`; and the Domain 1
characterization, which carries a Lean receipt. Nothing else in this packet is
citable as settled.

This packet answers the research prompt's step 3: whether any quantity survives in
at least three genuinely typed domains. The answer is a **split verdict**, and the
split is the finding.

## The hypothesis tested

Three of the program's results look like instances of one quantity — "how much
independent access to a system is required before a hidden, target-directed
structure becomes determinate, or stays determinate under damage":

- **Domain 1, profile certification (T299).** Does the current observation
  structure separate the target label's classes at all? A *feasibility* question.
- **Domain 2, hidden-matching information access (Candidate 1).** How many queries
  are needed to force separation? A *cost* question.
- **Domain 3, provenance-resilient restorative cutsets.** How much redundant
  separation survives damage? A *robustness* question.

## The invariant

A **resource-indexed observation system** is `S = (W, L, T, π, c, V, R)`: finite
worlds `W`, target `L`, an *indexed family* `T` of tests (each partitioning `W`,
duplicates allowed — essential, or redundancy is meaningless), costs `c`, resources
`V`, and `R` assigning each test its conjunctive resource dependencies.

Write `Q` for the set of *critical pairs* — pairs of worlds the target separates —
and, for each critical pair, `T(q)` for the tests that resolve it.

- **Lemma 1** (`DERIVED_BUT_UNVERIFIED`). A test set separates `L` iff it meets every `T(q)`. So the plain
  separation index is a minimum-weight hitting set.
- **Lemma 2** (`DERIVED_BUT_UNVERIFIED`). With private resources, `f`-robustness holds iff the test set meets
  every `T(q)` at least `f+1` times. So the robust index is a set multicover.
- **Theorem R** (`DERIVED_BUT_UNVERIFIED`; "Theorem" is the author's label,
  not a verification status). With *shared* resources, `f`-robustness holds iff the minimum
  transversal of the resource-sets of each critical pair's resolvers exceeds `f`.

Derived properties (all `DERIVED_BUT_UNVERIFIED`): monotone in the test family, in `f`, under target coarsening,
and in the world set; subadditive over *targets* but **not** over worlds; the
plausible bounds `sep_f ≤ (f+1)·sep_0` and `sep_{f+g+1} ≤ sep_f + sep_g` are both
**false**, with counterexamples; the valid bound is `sep_f ≥ sep_0 + f`. Feasibility
holds iff the transversal number exceeds `f` — which is exactly where Domain 3
lives. The transversal number is monotone but **neither sub- nor supermodular**.

The adaptive analogue (decision-tree depth) is a **separate index**, not a special
case. That turns out to matter.

## The three interpretation maps

### Domain 1 — exact instance, but degenerate

`W` is the background set, the test family is the single profile map, `f = 0`.
Certifiability is exactly Lemma 1 at a one-element test family.

**Correction to the natural guess** (`DERIVED_BUT_UNVERIFIED`): the right predicate is `sep < ∞`, not
`sep = 0`. `sep = 0` would mean the target is globally constant.

Verdict: **exact instance**, but with nothing to minimize and nothing to be robust
against, the invariant adds no mathematics here. It does supply one reframing: the
causal/spontaneous twin becomes an *infeasibility certificate* — the critical pair
has an empty resolver set.

### Domain 2 — guarded transfer, plus a derived partial nonidentity

Take worlds to be all partial matchings, the target to be the threshold predicate,
and the tests to be the edge indicators.

**Derived here (`DERIVED_BUT_UNVERIFIED`): the plain separation index is
exactly `mn`.** For each edge, build a
committed matching of size `t−1` avoiding that edge's endpoints inside the reduced
rectangle — possible because `t ≤ min(m,n)` — so that the edge alone resolves some
critical pair. Every edge is therefore essential. This independently re-derives the
packet's non-adaptive bound.

It is also derived (`DERIVED_BUT_UNVERIFIED`) to force `f`-robustness to fail for every `f ≥ 1`: the hidden-matching model
has **no fault tolerance at all**.

But Candidate 1's actual content is `mn − C(t,2)`, which is the *adaptive* index.
Five guards were identified; adaptivity was derived necessary
(`DERIVED_BUT_UNVERIFIED`) via a `2×2×2`
instance where the two indices are derived to differ (4 versus 3), and the
test-family guard was likewise derived necessary via subset-query collapse. The
exponential-gap claim and the consequent "no bridging theorem" conclusion are
also `DERIVED_BUT_UNVERIFIED`; no committed instance or checker reproduces any
of these.

Verdict: **guarded transfer with a derived-necessary hypothesis
(`DERIVED_BUT_UNVERIFIED`), plus a derived partial nonidentity.** The `C(t,2)` saving — all of Candidate 1's mathematical
interest — is invisible to the invariant.

### Domain 3 — exact instance of the generalized form, with its firewall recorded

An explicit faithful embedding (`DERIVED_BUT_UNVERIFIED`, except its transversal
arithmetic, which `checks/n1_transversal_packing_check.py` reproduces) sends
portfolio items to worlds, blockers to tests, and required-root sets to resource
dependencies. Under it, the program's cutset condition matches Theorem R, and
the program's robustness notion matches the invariant's.
Domain 3 is what forces the resource-indexed generalization in the first place —
the private-resource version is the special case where each test owns its resource.

Verdict: **exact instance of the generalized invariant** (`DERIVED_BUT_UNVERIFIED`
as above). The associated
transversal-versus-packing gap and exchange-axiom failure are recorded in
`AR8R-FABLE-R1-NEGATIVE-RESULTS.md`, item N1 — as an interpretation firewall and a
constraint on future definitions, **not** as refutations of program premises; the
original "premises the program had been assuming are false" framing, and the claim
of independent double derivation, were withdrawn after independent review.

## The convergence-gate verdict — split

**At the typed-model level: clears, weakly — author-recorded only, with no
verification status.** There is one typed object with three *recorded* interpretation maps:
Domain 1 an exact instance whose characterization is
`LEAN_FORMALIZED_SCOPED_RESULT` at the degenerate case, Domains 2 and 3
`DERIVED_BUT_UNVERIFIED` (including the guard-necessity derivation). On the
author's record that satisfies the prompt's "common typed formal model
with interpretation maps" clause on its face.

**At the theorem-transfer level: does not clear.** No nontrivial theorem transfers
between the domains. The invariant's entire general theory is Lemmas 1 and 2 plus
Theorem R, all of which are quantifier unfoldings, together with classical
NP-hardness results imported from elsewhere. It carries a **type, not a theorem**.

The honest disposition is that the gate stays closed, and the strongest result in
this domain is the principled nonidentity in Domain 3 rather than any positive
transfer. Recording the weak pass at the typed-model level without the failure at
the theorem-transfer level would be exactly the kind of overclaim the gate exists
to prevent.

## Nonclaims

- The invariant is not adopted, is not a milestone, and is not a meniscus result.
- It has zero general mathematical novelty.
- Candidate 1's value `mn − C(t,2)` is **not** adjudicated for novelty here; that
  still requires a real literature search, and its packet status is unchanged.
- Nothing here is kernel-checked except the Domain 1 characterization's Lean
  receipt (the degenerate case); the only executable check is the Domain 3
  transversal arithmetic via `checks/n1_transversal_packing_check.py`.
- No empirical, metaphysical, or theological content is touched.
