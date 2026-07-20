# Decision 0017 — Private design records and the public evidence boundary

**Date:** 2026-07-20 · **Authority:** R5 owner authorization (final public-state/evidence-boundary tie-off) · **Status:** adopted · **Reopens nothing:** Decisions 0001–0016 stand; no theory content changes.

## Problem

The public README and STATUS correctly said the private casebook and internal longitudinal record "motivate the design and validate nothing" — while the manuscript simultaneously used those same records as *corroboration*, *observational support*, evidence that failure patterns are "real and recurrent", a 33-case observational tier, and a transcript-verified longitudinal case (independent post-merge audit, finding B3). An unpublished, non-rights-cleared, independently unauditable record cannot carry public argumentative weight while the public state says no claim rests on it.

## Decision (governing rule)

An unpublished, non-rights-cleared, independently unauditable internal record MAY, in this project's public materials:

- explain design history;
- motivate a question;
- supply private provenance;
- suggest a future benchmark.

It may NOT, in publication-facing prose (`manuscript/`, `theory/`, `companion/`):

- corroborate the theory;
- establish existence, recurrence, or base rates of a failure pattern;
- support novelty or defeat the redundancy objection;
- count as observational evidence or occupy an evidential tier;
- support "real and recurrent" or any cross-domain claim.

## Consequences (implemented in R5)

1. Every evidential use in the manuscript was removed or rewritten: §1.4 (redundancy answer), §2.5/§3/§5.1/§7.3/§7.4/§7.6 (record-as-evidence asides), §11.4 (converted to an explicitly **synthetic composite worked example** assembled from the generic failure classes the public schemas/fixtures represent — illustrative only, not evidence), §12 (union residual restated without the record), §13/§13.4 (evidence status), §14, §15.2 (evidence tiers now: conceptual/definitional — machine-checked conformance, not a consistency proof; public observational — **none currently supplied**; experimental — none run), §16, §17 (availability: no public observational dataset; the private records are non-evidential design provenance on which no claim rests).
2. The novelty claim is bounded (audit B4): a custom composite could represent the architecture; the contribution is a common occurrence-centered lifecycle, a shared episode/verdict record contract, and the hypothesis that standardizing the integration improves auditability or practice — adjudicated only by the unrun benchmark. Impossibility-like language ("has no object", "the union is not free") is withdrawn from the redundancy answer.
3. Fixture claims are bounded (audit B5): "consistency shown by construction" and "formal coherence established analytically … observational support" are replaced with *machine-checked internal agreement over the declared definitions, schemas, examples, and adversarial fixtures — no proof of mathematical consistency, completeness, or utility, and no empirical result*.
4. `scripts/validate_evidence_boundary.py` (CI) fails if publication-facing prose reintroduces the private-evidence vocabulary (casebook, Branch 11, transcript-verified, real and recurrent, observational support, observational record, the 33-case/fifty-stops counts, internal longitudinal) and requires the standing no-public-dataset statements. STATUS/README honesty notes (which state the records are private and carry no weight) remain in place and in scope of the review-state contract, not this ban (their role is the boundary statement itself).
5. No private material is published; no owner decision is required. Actual empirical validation remains open.
