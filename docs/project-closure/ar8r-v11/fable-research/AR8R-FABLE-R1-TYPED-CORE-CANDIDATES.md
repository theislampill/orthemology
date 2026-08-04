# AR8R-FABLE-R1 — two rival typed cores and their discriminator

Status: research candidates. Neither core is adopted; there is no integrated
champion and this round does not create one. Both are strict fragments of the
program's declared vocabulary.

The research prompt's step 1 required two materially different candidate cores,
each attacked with the same countermodel battery, and forbade selecting a core
for having broader vocabulary coverage. This packet records both, their proved
properties, where each fails, and — the main output — a concrete finite scenario
where they disagree.

## Core A — profile / fibre / transport (model-theoretic)

**Signature.** A certification system is `S = (W, Λ, L, Π, P)` with `W` a set of
backgrounds, `Λ` labels, `L : W → Λ` the target, `Π` a profile space, and
`P : W → Π` the profile map. A morphism `(f,u) : S → S'` is a pair with
`P' ∘ f = u ∘ P` and `L' ∘ f = L`. These compose, giving a category.

**Proved.**

- **Fibre-constancy characterization.** `L` is certifiable by `P` iff `ker P ⊆ ker L`.
  The certificate is unique on the attained image. This is machine-checked in Lean
  (see `AR8R-FABLE-R1-LEAN-RECEIPTS.yaml`); AR8R-T299 is an exact instance of it.
- **Certifier lattice.** Certifying kernels form a principal down-set closed under
  both meets and joins — so two independent certifying audits can be coarsened to
  their agreement and still certify.
- **Refinement.** Refining the profile preserves certifiability; the converse
  fails, with a two-world countermodel.
- **Transport.** Certificates travel *backwards* along morphisms using only the
  two structural equations. Pushforward needs exactly surjectivity of `f` and
  injectivity of `u` on the attained image, and separate countermodels prove each
  hypothesis necessary.
- **Invariant.** A budgeted refinement cost: the minimum cost of instruments whose
  joint refinement makes `L` certifiable. It is 0 iff already certifiable, `+∞` iff
  the entire declared instrument suite fails (the formal version of "no evidence
  could resolve this"), monotone, kernel-invariant, and **Set-Cover-equivalent in
  both directions** — hence NP-hard and logarithmically inapproximable, with a
  greedy approximation available.

**Battery outcome.** Carrier: handled. Version and provenance: partial. Level
confusion, partial observation, and target mismatch: **failed**, with the failures
characterized rather than patched. Two are worth naming:

- *Partial observation.* The certificate type is scope-blind: a certificate can be
  green but mis-scoped, and scoped certificates provably do not compose across
  scopes.
- *Target mismatch.* Undetectable by construction, but boundedly so: a proved tight
  bound shows a single mislabelled world can take a system from perfectly
  certifiable to maximally defective.

A by-product worth recording: robustness can be defined as certifiability of the
perturbation-enlarged system, which yields a formal predicate for a *lucky*
certificate — one that is correct but would not survive a nearby perturbation.
This is the Gettier / stopped-clock case, made checkable.

**Known vulnerability.** False closure by coarsening is unconditionally free in
Core A: a constant profile certifies every system. Core A cannot forbid this
internally. Given that this program has a recorded false-closure incident, that is
a serious limitation, not a footnote.

## Core B — certificate / provenance calculus (proof-theoretic)

**Signature.** Judgments `Γ ⊢_S c : est(a,t)` — a certificate `c` establishes that
item `a` stands in the target-directed relation to target `t` — with every context
entry annotated by a provenance root. Rules: assumption, axiom instance,
composition along declared target combinations, weakening, transport along a
morphism of settings, and repair. Items form an idempotent monoid, so
corroboration by copying is not a new item.

The load-bearing rule is transport, whose side condition requires every root in
the derivation to lie in the domain of a **partial** root map. Uncarried roots are
*dropped*, not relabelled.

**Proved.**

- Survival under damage holds iff some derivation's support avoids the damage; the
  survival radius is the minimum transversal of the minimal-support hypergraph.
- **The MIN law:** a conjunctive burden is exactly as robust as its weakest
  conjunct. Adding guards to a multi-clause landing specification can only *lower*
  its radius — directly relevant to T299's six-clause conjunction.
- Deletion and corruption are indistinguishable exactly across transport and
  identical within a setting: a system that never transports cannot detect
  provenance corruption by survival testing alone.
- An unconditional sandwich `ν ≤ rad ≤ k·ν`, tight on both sides, with fractional
  exactness by LP duality.
- Repair buys damage-robustness at the cost of transport-fragility.
- Cut is inadmissible naively and under corroboration guards; a root-tracking
  repair is admissible under support-locality and guard antitonicity. Revocation
  must be modelled as damage, not as evidence.

**Battery outcome.** Level confusion and version: handled. Carrier: handled at the
calculus level only — no defence against badly declared axioms. Provenance,
partial observation, target mismatch, and closure: **succeeded** (closure twice).
Repairs exist for each: three-valuing the judgment (so a negative verdict is
*undetermined*, never *refuted*), declaring target-faithfulness explicitly, and
the root-tracking cut. Core B is a rival core, not a finished one.

## The discriminator — where the two cores disagree

This is the round's main step-1 output. A finite scenario, fully tabulated, in
which Core A certifies and Core B does not.

**Setup.** Three provenance roots (observation, calibration, custody), three
context entries, two composition rules mirroring T299's landing conditions, and
one version-bump morphism.

**The single datum that separates them.** The root map's domain omits the
*calibration* root: a field deployment re-acquires observations and re-runs custody
but has no counterpart acquisition for the lab calibration. The instrument still
prints its reading. What is missing is the acquisition root of the warrant to
*read* that string as a landed burden.

- **Core B:** transport is blocked, the calibration entry is dropped, and forward
  saturation never derives the landing judgment. **Not certified.**
- **Core A:** both backgrounds have identical six-coordinate matched profiles and
  identical labels, so the label is constant on the single attained fibre.
  **Certified.**

The reason is structural: a provenance root is not a profile coordinate. The
program's own coordinate registry already lists provenance root among the
forbidden collapses of the visible profile — this scenario is a concrete witness
for that prohibition.

**Independence.** All four verdict quadrants are realizable. Core A asks a
*uniformity* question about a class; Core B asks a *warrant-chain* question about
an item. **Neither refines the other.** A domain-stability check confirms this
from the other side: adjoining a calibration-decayed background with an identical
matched profile but a different label flips Core A's verdict while leaving Core B's
unchanged — Core B's verdict never mentions the domain.

Core B is repairable to reconverge with Core A here, at the permanent cost of a
fourth root. That cost is the point: the disagreement is not a bug in either core,
it is a real distinction between two notions of "established".

## Selection

**No core is selected.** The prompt forbids choosing on vocabulary coverage, and
neither core dominates: Core A has the machine-checked characterization and the
lattice structure but cannot forbid false closure by coarsening; Core B tracks
warrant chains and provenance but its negative verdicts are weaker than they look
and three battery attacks landed.

The honest disposition is that these are **two different questions**, and a common
core, if one exists, must answer both — which neither currently does.

## Nonclaims

- Neither core is adopted, integrated, or a champion.
- Neither is machine-checked except for Core A's central characterization.
- Neither expresses the full declared vocabulary: episodes, evidence typing,
  residual ledgers, and the program's verdict taxonomy are all outside both.
- No novelty is claimed. Core A's characterization is the quotient factorization
  lemma; its invariant is minimum test collection; Core B's radius is a hypergraph
  transversal.
