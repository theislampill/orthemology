# AR8R-FABLE-R1 — negative results, refutations, and failed candidates

Status: research findings. Non-adopted. Item N1 was **substantially withdrawn and
rewritten** after independent review; the withdrawal record is
`AR8R-FABLE-R1-CORRECTION-RECEIPT-V1.md`.

None of the items below refutes an adopted premise of the program. They are
interpretation firewalls, constraints on proposed future definitions, failed
candidates generated inside round 1, and one reaffirmed gate. Round 1's original
framing — that four of five were "refutations of premises the program had been
treating as available" — was not supported by the repository and is withdrawn.

## N1 — transversal and packing can differ, and the root-set independence family need not be a matroid

**Scope correction (withdrawal).** Round 1 originally presented this item as a
refutation of the Round-20 restorative-cutset result and of milestone candidate
MEN-2. That attribution was false and is withdrawn:

- The proposed Round-20 result
  (`../post-merge-proposals/pmr007-rounds11-20/PROPOSED_THEOREM_FILES/PMR-007_FRONTIER_ROUND20_PROVENANCE_RESILIENT_RESTORATIVE_CUTSETS_V2.md`)
  defines the minimum transversal number `τ(H)` and `κ_root(I) = min_p τ(H_p(I))`,
  and proves `f`-root-robust ⟺ `κ_root(I) > f`. It cites standard hypergraph
  transversal theory as its exact mechanism.
- The rejected V1
  (`../post-merge-proposals/pmr007-rounds11-20/REJECTED_AND_BLOCKED_EVIDENCE/PMR-007_FRONTIER_ROUND20_PROVENANCE_RESILIENT_RESTORATIVE_CUTSETS_V1.md`)
  also uses the transversal number throughout, and the V1→V2 repair log records no
  change of criterion.
- Neither version uses maximum root-disjoint packing as the exact criterion,
  asserts a Menger equality, or assumes the independence family is a matroid.

**The Round-20 statement is not corrected and is not altered by this item.**

What survives is a valid negative result with a narrower role.

**Valid result 1 — `τ` and `ν` can differ.** Let three blockers carry required
root-sets `{r₁,r₂}`, `{r₂,r₃}`, `{r₁,r₃}`. The maximum number of pairwise
root-disjoint blockers is 1, but the minimum transversal has size 2. So a
portfolio can be 1-root-robust while possessing **zero** root-disjoint routes.

*Role: interpretation firewall.* A minimum transversal cannot in general be
replaced by a maximum root-disjoint packing; `ν > f` is sufficient but not
necessary. This forbids a future misreading. It corrects no existing statement.

**Valid result 2 — the exchange axiom can fail.** On the path `r₁—r₂—r₃—r₄` with
required root-sets `{r₁,r₂}`, `{r₂,r₃}`, `{r₃,r₄}`: take `J₁ = {e₂}` and
`J₂ = {e₁,e₃}`. Then `|J₁| < |J₂|` but no element of `J₂ \ J₁` can be added to
`J₁` while preserving independence. So "pairwise root-disjoint" is not in general
the independence family of a matroid, and no rank function, greedy guarantee, or
matroid union is available for it in general.

*Role: constraint on any future MEN-2 definition.* MEN-2 is `NOT_ADOPTED`, is
stated as a *proposed target* ("define an independent-acquisition rank"), and
carries the explicit nonclaim `NOT_A_THEOREM`. It does not currently assert matroid
axioms, so nothing in it is refuted. The constraint is that any future definition
must state explicitly whether it is a transversal quantity, a packing quantity, a
matroid rank, a polymatroid quantity, or another invariant — and, if a rank, must
establish the exchange axiom for the structure it is defined on.

**No sharp threshold is claimed.** Round 1 originally asserted that both properties
hold iff every item requires at most one root, and fail as soon as one item
requires two. That is **false** and is withdrawn. Counterexamples, all verified by
`checks/n1_transversal_packing_check.py`:

| Structure | Exchange axiom | `τ` | `ν` |
|---|---|---|---|
| one item with root-set `{r₁,r₂}` | holds | 1 | 1 |
| two disjoint two-root items | holds | 2 | 2 |
| `{r₁,r₂}`, `{r₁,r₃}` — intersecting, multi-root | holds | 1 | 1 |

Multi-root structure alone therefore does not establish failure of either property.
The surviving bounded statement is one-directional: **the single-root regime is
sufficient** for partition-matroid structure and `τ = ν`; **it is not necessary.**
No replacement `iff` characterization is offered, because none has been proved and
adversarially checked.

**Quorum arithmetic, within its declared range.** For a `k`-of-`n` quorum read as
conjunctive `k`-subsets, the minimum transversal is `n − k + 1` while the maximum
root-disjoint derivation count is `⌊n/k⌋`; these coincide iff `k = 1` or `k = n`,
and the gap grows in between. Checked exhaustively for `2 ≤ n ≤ 7` only; no claim
is made beyond that range. The further claim that coverage is *strictly
supermodular* at quorum gates is recorded as `DERIVED_BUT_UNVERIFIED` — no
derivation or executable check accompanies it.

**Derivation-independence claim withdrawn as unverifiable.** Round 1 asserted this
item was derived twice by two lines of work that did not share intermediate
results. That is a claim about process, not about the repository, and no committed
artifact can confirm it. It is withdrawn from the evidential record.

## N2 — the OSM paper does not clear the formal convergence gate, and the gate should stay closed

Disposition: **principled nonidentity at the section/warrant layer, boundary-only
elsewhere.** The repository's existing `formal_convergence_gate:
REQUIRED_NOT_SATISFIED_BY_THIS_SOURCE` is correct and is reaffirmed, not relaxed.

The close call is worth recording because it is genuinely close. The clone-structured
model's emission map **is** a fibration whose fibres are the observation-indistinguishability
classes — structurally what the typed core asks for. It fails at three nameable places:

1. it admits **no canonical, transition-compatible section**, and no unique latent
   state is identifiable from an observation symbol. What the model supplies is
   measure-weighted path lifting, a different structure.

   *Correction (independent review).* Round 1 originally wrote that the emission
   map "admits no global section by construction". That is false as stated: the
   emission map is a finite surjection onto its attained image, so a set-theoretic
   section exists by selecting one preimage from each attained fibre. The
   established limitation is nonidentifiability and the absence of a *canonical*
   or *transition-compatible* choice — not the nonexistence of every section.
   Distinctions collapsed inside a fibre are not recoverable from the observation
   symbol alone; that is the actual obstruction, and it is weaker than what the
   original wording asserted;
2. its base is a stipulated symbol alphabet, not a base of targets;
3. there is no warrant layer at all, and a likelihood is not a warrant.

**Source-level status.** The independent review of round 1 excluded the source paper
from its boundary, so no reviewer has checked these three points against the
paper's own text. Points 1–3 are therefore marked `SOURCE_LEVEL_UNVERIFIED`: they
describe the typed reading recorded in
`AR8R-FABLE-R1-OSM-TYPED-EXTRACTION.md`, and neither pass nor reject the source
itself. The gate disposition below does not depend on them — it is the repository's
pre-existing disposition, reaffirmed.

The countermodel-architecture clause also fails, on transportability: the paper's
constructions are algebraic (linear kernel, additive perturbation) while the
program's correctness predicate is factive with no kernel. Only the moral
transports, and a shared moral is the already-rejected `COMMON_INTUITIVE_METAPHOR`.

## N3 — a source-internal qualification of the paper's headline trajectory claim

Recorded as a reading of the published source, not as a criticism of the authors,
and not as a project claim about the hippocampus.

**Status: `SOURCE_LEVEL_UNVERIFIED`.** The independent review of round 1 excluded
the source paper from its boundary. Every statement in this item is a reading of
the source recorded by round 1 and checked by no reviewer. It is neither a pass nor
a rejection of the source.

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
| provenance-independence defined as a matroid rank over root-disjointness | **CONSTRAINED** — the exchange axiom can fail, so any future MEN-2 definition must name its invariant class. MEN-2 as written asserts no matroid axioms and is *not* refuted |
| replacing a minimum transversal by a maximum packing | **FIREWALLED** — `τ ≠ ν` in general, so the substitution is invalid. No repository statement made this substitution; Round 20 V1 and V2 both use the transversal |
| split-number as a repair-budget invariant | **REJECTED** — not monotone under refinement |
| OSM paper as a convergence-gate-clearing source | **REJECTED** (`SOURCE_LEVEL_UNVERIFIED`) — no canonical, transition-compatible section; stipulated base; no warrant layer |
| naive cut in the certificate calculus | **REJECTED** — inadmissible; repaired form has declared residual tension |
| Candidate 1's `mn − C(t,2)` as an instance of the separation index | **REJECTED** — different index (adaptive vs non-adaptive); see the separation-index packet |

## What none of this establishes

- No theorem is adopted, no champion is selected, no milestone is completed.
- **No adopted or proposed program statement is refuted by N1.** The Round-20
  result and MEN-2 are unaltered. N1's surviving content is an interpretation
  firewall and a constraint on future definitions.
- The historical theorems' own internal correctness is unchanged and was never at
  issue.
- No empirical or metaphysical claim is made or withdrawn. In particular, nothing
  here bears on the separate historical internal synthetic T299/T300 pilot recorded
  at `../experiments/t299-t300-negative-synthetic-pilot.md`, whose negative
  disposition at its own evidential class stands.
- No novelty is claimed for any item; each is an application of standard
  combinatorics (transversal vs packing, matroid exchange).
- Items N2 and N3 are `SOURCE_LEVEL_UNVERIFIED`: the source paper was outside the
  independent review boundary.
