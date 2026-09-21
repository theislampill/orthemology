# Primary-source comparison and novelty status

**No global novelty, foundational breakthrough or expert endorsement is established.**
This is a bounded comparison, not an exhaustive historical review. The unchanged
intersection/realisability construction is standard. A useful operational
integration or sharper application boundary does not become a new foundational
calculus by being implemented or eventually compiled.

## Inspected primary statements

### P1 — Girard/Hurkens, Mathlib Counterexamples.Girard

Source: https://leanprover-community.github.io/mathlib4_docs/Counterexamples/Girard.html
The actual signature assumes a same-universe pi operation, lam, app and beta and
concludes False. The preserved `HurkensBoundary.lean` is an attributed adaptation,
not an installed current Mathlib module. Its source lineage is pinned separately.
The v4 addition extracts its full-section interface from two actual exported
operational handles and their totality/beta properties. This is a correspondence
application of a known obstruction, not a stronger inconsistency theorem.
Internal self-instantiation of the realisability All is not that full interface.

### P2 — Paolo Pistone, arXiv:1802.05143v5, LMCS 15(4), 2019

Sources: https://arxiv.org/abs/1802.05143 and https://arxiv.org/pdf/1802.05143
Theorem 5.21 establishes invariance for closed realisers under the stated
adequate-closure conditions. Theorem 7.1 relates typability, realisability and
invariance/dinaturality for positive types and closed normal terms, with the
specified beta/beta-eta qualifications. Section 5.3 distinguishes the needed
extensional structure for stronger Reynolds-style statements.

Our R1 starts from a finite **derivation**, not arbitrary unary semantic
membership, and proves a binary relation fundamental lemma for a pure closed
combinatory fragment. It is a concrete specialisation, not a new general
parametricity theorem. Our primitive-bottom divergent counterexample does not
contradict the positive-type/normal-term completeness hypotheses. A complete
formal transport to the paper's model has not been carried out.

Readback: relevant full-text theorem passages were read. PDF screenshots for
pages 33 and 44 were attempted but returned cache-miss errors. No visual-reading
credit is asserted; no figure-based claim is used.

### P3 — Thummala and Chase, SAFE, arXiv:1510.04629v2

Sources: https://arxiv.org/abs/1510.04629 and https://arxiv.org/pdf/1510.04629
The full-text revocation discussion describes issuer updates and cached
credential sets: an authorizer may retain the old set until refresh, with
expiration bounding validity. Its architecture separates credential discovery
from proof validation.

The v4 engine offers a narrower single-process property: after a relevant
revision returns under the same lock, stale local tickets cannot dispatch.
It does not solve distributed cache invalidation, authenticate remote issuers
or improve SAFE's distributed guarantees. Versioned proof contexts and cached
credentials are established prior art; our particular law-defect dependency
adapter is an implementation/application contribution. Full-text passages were
read; the requested PDF screenshot on page 10 failed, so no visual audit claim.

### P4 — Kaminski and Katoen, arXiv:1410.7225v1

Source: https://arxiv.org/html/1410.7225
Definitions 6–8 identify program termination probabilities and expected-outcome
comparison problems. Theorem 3 proves the exact expected-outcome problem
Pi^0_2-complete; Theorem 4 proves almost-sure termination Pi^0_2-complete by a
universal-halting reduction.

Our Q8 is a different, more restricted property: **every finite observation
prefix is produced in bounded time**, but whether its entire output-stream law
has zero point defect encodes non-halting. We prove non-enumerability for this
particular uniformly generated family, not a new full hierarchy classification
or a stronger hardness result than theirs. The reduction is an elementary
halting construction; an exact precedent for this defect formulation has not
been ruled out. The operational invariant checker deliberately accepts a sound,
incomplete fragment instead of claiming a complete decision procedure.

### P5 — Lean 4.19.0 collectAxioms implementation

Source: https://raw.githubusercontent.com/leanprover/lean4/v4.19.0/src/Lean/Util/CollectAxioms.lean
The actual API traverses values and types in the checked declaration environment.
The new `AuditSupport.lean` uses it and explicitly refuses missing declarations,
then refuses every transitive axiom outside the approved three-name ceiling.
Reading the API and testing emission does not establish that this new module
elaborates; that remains a mandatory formal target.

## Abstract-level leads, not full theorem review

Speight and van der Weide, *Impredicativity in Linear Dependent Type Theory*,
arXiv:2602.08846, https://arxiv.org/abs/2602.08846, reports a realisability model
with two decoders, large Cartesian and linear dependent products and a Rocq
formalisation. Only its abstract/metadata were revisited here. It is a relevant
and apparently stronger dependent-theory comparator, not something v4 subsumes.

The preserved v3 bibliography includes System F normalisation, effectful
polymorphism, reflective oracles and erasure/zero-cost work. Its historical
status is preserved; every such item has not been freshly read in full during
this continuation.

## Result-by-result classification

| Result | Honest classification | What is not established |
|---|---|---|
| Q1–Q4 positive-point decomposition and refinement transport | Ordinary countable-sum/measure arguments and a typing-certificate application | Historical novelty or formal measure proof |
| Q5 finite invariant extension | Standard relation/predicate induction, executable specialisation | New general logic or all-predicate decision procedure |
| Q6 exact rational/interval-law checker | Concrete verified-reference integration | Automatic identification of a real-world law |
| Q7 countable event-family distinction | Standard countable intersection fact correcting overbroad applications | Rich-event obstruction for a finite source vocabulary |
| Q8 productive-observer certificate boundary | Ordinary halting reduction for a precisely specified property | First publication or general hardness classification |
| O1–O3 operational licensing/revision | Tested local implementation and ordinary invariant proof | Fully verified Python, remote security or distributed revocation |
| O4 positive/negative conjunction | Candidate operational-to-known-Girard correspondence | Kernel acceptance or new Girard theorem |
| R1 finite logical relations | Candidate mechanisation of a standard fundamental induction | Full semantic Reynolds parametricity |
| R2 source proof export | Reproducible concrete bridge for checked certificates | Universal parser/compiler refinement |
| S1–S2 typed threshold and fixed-point source | Exact specified sampler and cost/application arguments | All-real-law realisability or general Kakutani selection |

A lack of an exact phrase match is not evidence of priority. None of these rows
has been submitted to or endorsed by an independent specialist in this execution.
