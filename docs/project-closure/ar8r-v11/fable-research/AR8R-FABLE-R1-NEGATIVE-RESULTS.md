# AR8R-FABLE-R1 — negative results, refutations, and failed candidates

Status: research findings. Non-adopted. These are the most load-bearing outputs
of round 1: they close off routes the program's documents currently leave open.

Under the program's own semantics a principled nonidentity is a positive result.
Four of the five items below are refutations of premises the program had been
treating as available.

## N1 — "provenance independence" is not a matroid rank, and the cutset condition is not a Menger theorem

**This was derived twice, independently, by two lines of work that did not share
intermediate results** (a proof-theoretic certificate calculus, and a
model-theoretic separation index). Both reached the same refutation.

The program's milestone candidate MEN-2 names a "provenance-independence **rank**",
and the Round-20 restorative-cutset result is naturally read as "a target survives
`f` corruptions iff there are more than `f` independent provenance routes". Both
readings are false as stated.

**Refutation 1 — the transversal/packing gap.** Let three blockers carry required
root-sets `{r₁,r₂}`, `{r₂,r₃}`, `{r₁,r₃}`. The maximum number of pairwise
root-disjoint blockers is 1, but the minimum transversal has size 2. So the
portfolio is 1-root-robust while possessing **zero** root-disjoint routes. The
exact condition is `τ > f` (minimum transversal), not `ν > f` (maximum packing).
`ν > f` is sufficient only.

A Menger-type theorem asserts `τ = ν`. Here `τ ≠ ν`. The correct statement is a
quantifier unfolding, not a duality theorem.

**Refutation 2 — the exchange axiom fails.** On the path `r₁—r₂—r₃—r₄` with
required root-sets `{r₁,r₂}`, `{r₂,r₃}`, `{r₃,r₄}`: take `J₁ = {e₂}` and
`J₂ = {e₁,e₃}`. Then `|J₁| < |J₂|` but no element of `J₂ \ J₁` can be added to
`J₁` while preserving independence. The exchange axiom fails, so there is no rank
function, no greedy guarantee, and no matroid union.

**Sharp threshold.** Both premises hold **iff** every item requires at most one
root — in which case the structure is a partition matroid and `τ = ν`. Both fail
as soon as some item requires two. The program's own positive witness for the
cutset result lives entirely in the single-root regime, which is exactly why the
matroid intuition looked sound.

**Independent confirmation from the certificate side.** The same phenomenon
appears as quorum gates. For a `k`-of-`n` quorum, the survival radius is
`n − k + 1` while the maximum root-disjoint derivation count is `⌊n/k⌋`. Menger
holds iff `k = 1` (pure OR) or `k = n` (pure AND), and the gap is unbounded in
between. Diagnosis: **the equivalence holds for AND/OR provenance structures and
fails exactly at quorum gates.** Coverage is strictly supermodular there, so
submodularity-based methods do not apply either.

**Consequence for the program.** MEN-2 cannot be stated as a rank. Any milestone,
flywheel edge, or future theorem that assumes independent-route counting computes
robustness is unsound outside the single-root regime. The correct invariant is the
transversal number.

## N2 — the OSM paper does not clear the formal convergence gate, and the gate should stay closed

Disposition: **principled nonidentity at the section/warrant layer, boundary-only
elsewhere.** The repository's existing `formal_convergence_gate:
REQUIRED_NOT_SATISFIED_BY_THIS_SOURCE` is correct and is reaffirmed, not relaxed.

The close call is worth recording because it is genuinely close. The clone-structured
model's emission map **is** a fibration whose fibres are the observation-indistinguishability
classes — structurally what the typed core asks for. It fails at three nameable places:

1. it admits **no global section by construction** — that is the entire point of
   clone structure; what it supplies is measure-weighted path lifting, a different
   structure;
2. its base is a stipulated symbol alphabet, not a base of targets;
3. there is no warrant layer at all, and a likelihood is not a warrant.

The countermodel-architecture clause also fails, on transportability: the paper's
constructions are algebraic (linear kernel, additive perturbation) while the
program's correctness predicate is factive with no kernel. Only the moral
transports, and a shared moral is the already-rejected `COMMON_INTUITIVE_METAPHOR`.

## N3 — a source-internal qualification of the paper's headline trajectory claim

Recorded as a reading of the published source, not as a criticism of the authors,
and not as a project claim about the hippocampus.

The paper's supplementary material reports that the model's decorrelation **order**
flips depending on how a simultaneous visual-cue-and-reward event is serialized
into the model's one-symbol-per-step input. One serialization matches the animals;
two others give the reverse order. All variants reach the **same** final transition
graph.

So the unique trajectory match is a property of the pair (model, encoding
convention), where the encoding convention is an unmeasured modelling choice — not
a property of the algorithm, and not a fact about the biology.

Second: for a clone-structured model with disjoint clone support, the centred
correlation at the reported clone count is forced to approximately `−1/(d−1)`,
i.e. essentially zero, analytically. The endpoint match is therefore closer to a
corollary of the architecture meeting a deterministic sequence structure than to a
prediction, and carries correspondingly little confirmatory weight.

**Consequence.** Any future use of this source must not treat trajectory-order
agreement as mechanism identification.

## N4 — the naive repair-budget invariant is not monotone (failed candidate)

The obvious measure of "how much refinement is still needed" — the number of
profile blocks that must be split — is **not** monotone under refinement of the
profile map. A four-world counterexample raises it from 1 to 2 when the profile is
refined. Any budget or progress metric built on it would report regress where there
is progress. Rejected.

The monotone replacement is the covering-style refinement cost, which is
well-behaved but NP-hard to compute exactly (it is Set-Cover-equivalent in both
directions).

## N5 — cut is not admissible in the certificate calculus without root tracking

Naive cut fails under transport: a two-root countermodel derives a judgment
whose inlined form is not derivable. Even root-tracking cut fails in the presence
of a corroboration guard ("at least two distinct roots"), because monotone guards
break under inlining.

A repaired rule, admissible under support-locality and guard antitonicity, exists:
inlining never widens the provenance footprint. But the repair carries a permanent
declared tension with corroboration guards.

**Consequence for the program's notion of closure.** "Closure" cannot be assumed
to compose. A system that closes over a lemma and then reuses it may lose
provenance guarantees the original derivation had.

## Failed candidates ledger

| Candidate | Disposition |
|---|---|
| provenance-independence as a matroid rank (MEN-2 as stated) | **REFUTED** — exchange axiom fails at multi-root items |
| cutset robustness as a Menger duality | **REFUTED** — `τ ≠ ν`; correct condition is transversal, not packing |
| split-number as a repair-budget invariant | **REJECTED** — not monotone under refinement |
| OSM paper as a convergence-gate-clearing source | **REJECTED** — no global section, stipulated base, no warrant layer |
| naive cut in the certificate calculus | **REJECTED** — inadmissible; repaired form has declared residual tension |
| Candidate 1's `mn − C(t,2)` as an instance of the separation index | **REJECTED** — different index (adaptive vs non-adaptive); see the separation-index packet |

## What none of this establishes

- No theorem is adopted, no champion is selected, no milestone is completed.
- The refutations are about *the program's stated premises*, not about the
  historical theorems' own internal correctness, which is unchanged.
- No empirical or metaphysical claim is made or withdrawn.
- No novelty is claimed for any refutation; each is an application of standard
  combinatorics (transversal vs packing, matroid exchange, supermodularity).
