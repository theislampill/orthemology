# AR8R-FABLE-R1 — the separation index, three interpretation maps, and a split convergence verdict

Status: research candidate. Non-adopted. Zero general mathematical novelty is
claimed; see `AR8R-FABLE-R1-PRIOR-ART-AND-NOVELTY-CEILING.md`.

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

- **Lemma 1.** A test set separates `L` iff it meets every `T(q)`. So the plain
  separation index is a minimum-weight hitting set.
- **Lemma 2.** With private resources, `f`-robustness holds iff the test set meets
  every `T(q)` at least `f+1` times. So the robust index is a set multicover.
- **Theorem R.** With *shared* resources, `f`-robustness holds iff the minimum
  transversal of the resource-sets of each critical pair's resolvers exceeds `f`.

Proved properties: monotone in the test family, in `f`, under target coarsening,
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

**Correction to the natural guess:** the right predicate is `sep < ∞`, not
`sep = 0`. `sep = 0` would mean the target is globally constant.

Verdict: **exact instance**, but with nothing to minimize and nothing to be robust
against, the invariant adds no mathematics here. It does supply one reframing: the
causal/spontaneous twin becomes an *infeasibility certificate* — the critical pair
has an empty resolver set.

### Domain 2 — guarded transfer, plus a proven partial nonidentity

Take worlds to be all partial matchings, the target to be the threshold predicate,
and the tests to be the edge indicators.

**Proved here: the plain separation index is exactly `mn`.** For each edge, build a
committed matching of size `t−1` avoiding that edge's endpoints inside the reduced
rectangle — possible because `t ≤ min(m,n)` — so that the edge alone resolves some
critical pair. Every edge is therefore essential. This independently re-derives the
packet's non-adaptive bound.

It also forces `f`-robustness to fail for every `f ≥ 1`: the hidden-matching model
has **no fault tolerance at all**.

But Candidate 1's actual content is `mn − C(t,2)`, which is the *adaptive* index.
Five guards were identified; adaptivity was **proved necessary** by a `2×2×2`
instance where the two indices differ (4 versus 3), and the test-family guard was
proved necessary by showing subset queries collapse the value. In general the gap
between the two indices is exponential, so **no bridging theorem exists**.

Verdict: **guarded transfer with a proven-necessary hypothesis, plus a principled
partial nonidentity.** The `C(t,2)` saving — all of Candidate 1's mathematical
interest — is invisible to the invariant.

### Domain 3 — exact instance of the generalized form, with its risky premise refuted

An explicit faithful embedding sends portfolio items to worlds, blockers to tests,
and required-root sets to resource dependencies. Under it, the program's cutset
condition **is** Theorem R, and the program's robustness notion is the invariant's.
Domain 3 is what forces the resource-indexed generalization in the first place —
the private-resource version is the special case where each test owns its resource.

Verdict: **exact instance of the generalized invariant.** But the premises the
program had been assuming about it are false; see
`AR8R-FABLE-R1-NEGATIVE-RESULTS.md`, item N1, for the transversal-versus-packing
gap and the exchange-axiom failure. Both refutations were reached independently
from the certificate-calculus side as well.

## The convergence-gate verdict — split

**At the typed-model level: clears, weakly.** There is one typed object with three
verified interpretation maps — two exact instances and one guarded transfer whose
guard is proved necessary. That satisfies the prompt's "common typed formal model
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
- Nothing here is machine-checked. Only the Domain 1 characterization has a Lean
  receipt, and it is the degenerate case.
- No empirical, metaphysical, or theological content is touched.
