# Orthemic Terminology & Distinction Evaluation Spec

> **Provenance.** Draft lineage: Opus 4.8 (owner/harness report). An
> attempted review pass also ran under Opus 4.8 while falsely
> self-identifying as Fable 5 (its §B.8 addition is part of the draft
> lineage and itself contained a tie/retire contradiction). Genuine Fable 5
> Gate A (read-only dispositions): `fable-independent-review-v2.md` §7.4,
> 2026-07-16. Genuine Fable 5 Gate B (this text), 2026-07-16: B.6 fully
> normalized to the three-outcome rule (no "abandon otherwise" anywhere);
> construct families term-mapped with ≥3 variants each; heterogeneous
> pooled primary replaced by two construct-specific co-primaries with
> gatekeeping; carryover, stochasticity/versioning, blinding limits,
> simulation-based power, Pareto compression with primer cost, margins,
> and the preregistration hash specified. **Final Fable disposition:
> decision-grade preregistration DRAFT — normalized, canonical, NOT RUN.**
> Provenance authority is the owner-observed UI/harness.

> **Status ledger.** Accepted: arm structure (A/B/C + exploratory
> ablations); fixture list B.4; measures B.5. Revised: B.6 and B.8 as
> above. Rejected: two-outcome abandonment language; single-fixture
> endpoints; pooled heterogeneous primaries; "ties ⇒ retire" without
> powered equivalence. Unresolved: exact n (needs the pilot); rater pool
> composition. Experimental gate: the whole document — designed, not run;
> no term is adopted or retired today. Evidence tier: design only.

**Date:** 2026-07-16. **Status:** DESIGNED, NOT RUN. Two evaluations are kept
strictly separate: a **product fixture** (already in the #9 harness) and a
**theory/terminology benchmark** (below). No external usage of any coined term
is researched.

---

## Part A — Product fixture (already implemented; reference only)

#9 fixture **E5** (`eval/fixtures/E5/`) is a product fixture and carries **no
theory vocabulary**: a weak rule (pass iff output contains a marker) returns
the correct current result; paired neighboring perturbations (correct-without-
marker; incorrect-with-marker) expose the rule; scoring records two distinct
properties — current-answer correctness and pathway adequacy. It is complete
and kept out of the terminology benchmark entirely.

---

## Part B — Theory/terminology benchmark (design only, do not run)

### B.1 Purpose and the fallacy it avoids
Test whether the coined vocabulary earns keep — via **compression,
coordination, or prediction** — even granting full paraphrasability. "Can be
said in ordinary words" does NOT settle the question ("Gettier case" is fully
paraphrasable and permanently useful). Equally, the words are not adopted for
elegance. The benchmark measures behavioral and communicative deltas under
matched conditions.

### B.2 Arms (counterbalanced)
- **Arm A — ordinary baseline:** case-handling with no framework language.
- **Arm B — distinctions without neologisms:** the operational distinctions
  (occurrence identity/version; plural profile; candidate set; route-
  sufficient vs identity-complete; evidence property/scope; false closure;
  correct-by-luck/pathway adequacy; governing-rule revision) expressed in
  ordinary words.
- **Arm C — coordinated vocabulary:** orthemma / ortheme / metaortheme /
  orthing (+ the episode/pathway constructs), defined once in a short primer.
- **Term-level ablations (where practical):** C-minus-orthing;
  C-minus-metaortheme; C-with-orthing-only — to isolate each term's marginal
  contribution rather than only the bundle.

### B.3 Held constant
Model, evidence provided, example set, time budget, output permissions,
scoring rubric, and rater pool. Arm order counterbalanced across items;
primer-reading time for Arm C is added to Arms A/B as matched filler reading so
total exposure is equal.

### B.4 Fixtures (each rendered once per arm, semantically identical)
1. correct-by-luck validator (weak rule, right answer);
2. stale/wrong occurrence-version (same signal, different commit/copy);
3. plural profile (one occurrence, two independent defects);
4. open-but-adjudicable candidate set (several causes, discriminating test available);
5. route-sufficient action before complete diagnosis (safe containment);
6. false closure (residuals undisposed under completion language);
7. verified handoff (packet claims vs live state mismatch);
8. live-readback (repo-green, surface-broken);
9. lesson-lift / governing-rule revision (recurring class → rule defect);
10. simple negative controls (single-fault; trivial fix) — must add ~zero
    overhead in every arm;
11. mechanical/delegated orthing (a validator/pipeline executes rule-governed
    resolution with no conscious judgment) — tests whether the vocabulary
    helps describe non-agent executors.
12. multi-actor competitive scenario (one shared game-like occurrence, two
    actors with opposed task-indexed targets) — tests whether the arm keeps
    apart: shared occurrence / actor-relative TARGET profile / current
    descriptive profile / objective / policy / metaorthemic distinction.
    The owner's zero-sum screenshots are the standing NEGATIVE calibration
    example for objective-vs-policy-vs-metaortheme conflation (alongside
    the Grok example); see `orthemic-multi-actor-conflict-note.md`.

### B.5 Measures
Behavioral: correct occurrence identification; plural-profile preservation;
candidate adjudication; pathway-defect detection; neighboring-case failure
prediction; false-closure detection; governing-rule revision; cross-domain
transfer (train on one domain, apply to another). Communicative: inter-rater
agreement (do two readers reach the same placement); **compression** (output
length at equal accuracy — a genuine win condition); operator burden
(subjective load + time). Cost/harm: terminology-caused execution errors
(a model misuses a term and acts wrongly); over-segmentation on the negative
controls.

### B.6 Pre-registered decision criteria (three outcomes per target — NO two-outcome "abandon otherwise" language anywhere)
Every criterion below resolves to exactly one of: **ADOPT** (adequately
powered win at the pre-registered effect size); **DO NOT ADOPT YET**
(insufficient evidence — including every underpowered null and every
ordinary nonsignificant tie); **RETIRE/REJECT** (only on adequately
powered equivalence/noninferiority evidence of no benefit, or a
harm-ceiling breach).

Construct families, term-mapped (≥3 independent item variants per family;
one fixture is never a decision-grade endpoint):
- **orthemma → occurrence/version-identity family** (fixtures 2, 7-adjacent
  variants): adopt only if it beats "occurrence/case/version" on
  identification or inter-rater agreement at equal length.
- **ortheme → plural-profile/candidate family** (fixtures 3, 4 + variants):
  adopt only if it beats "state-type/label" on profile preservation or
  candidate adjudication.
- **metaortheme → governing-distinction/rule-defect family** (fixtures 1, 9
  + variants): adopt only if it beats "governing rule / evidence standard /
  policy" on rule-defect detection or coordination; the Grok exchange
  remains the standing negative example of a vague objective mislabeled a
  metaortheme.
- **orthing → episode/pathway family** (fixtures 1, 8, 11 + variants):
  adopt only if it beats the matched no-term arm on compression (at equal
  correctness) OR coordination OR neighboring-case failure prediction.
- **coordinated vocabulary as a system → cross-domain integration +
  compression/burden**: adopt only if **Arm C beats Arm B** per the exact
  B.8 definition; a tie means DO NOT ADOPT YET unless the tie is an
  adequately powered equivalence result, in which case retire the words
  for interface use (distinctions stay in ordinary language; internal
  shorthand remains permitted).
- **The operational distinctions themselves:** Arm B vs Arm A per family —
  same three outcomes; a distinction is never abandoned on an underpowered
  miss.
- **Harm stop (overriding):** if any arm's terminology-caused execution
  errors or negative-control over-segmentation exceed the pre-set ceiling,
  that term/vocabulary is REJECTED regardless of other gains.

Primary confirmatory comparisons: **Arm B vs A** (distinctions) and
**Arm C vs B** (vocabulary). Term-level ablations (B.2) are EXPLORATORY;
a bundle win triggers a separate confirmatory ablation study rather than
post-hoc per-term conclusions.

### B.7 Non-goals / guards
Do not run yet. Do not search external usage of any coined term. Do not let a
distinction's Arm-B success be counted as vocabulary (Arm-C) success or vice
versa. Do not declare a term useless because a small underpowered study
failed to detect a benefit — see the three-outcome rule below.

### B.8 Decision-grade parameters (pre-register before any run)
- **Primary endpoints — two construct-specific co-primaries, never pooled
  across heterogeneous constructs:** (1) false-closure detection rate over
  the false-closure item FAMILY (≥3 independent variants of fixture 6);
  (2) pathway-defect detection rate over the correct-by-luck item FAMILY
  (≥3 independent variants of fixture 1). Fixture 9 (rule revision) is
  scored in its own family as a key secondary — the earlier pooling of
  fixtures 1/6/9 into one "false-closure rate" mixed three constructs and
  is corrected. **Co-primary multiplicity:** hierarchical gatekeeping
  (test (1) at α=0.05; test (2) only if (1) is significant) or a
  pre-registered alpha split — declared before the run.
- **Secondary endpoint families:** occurrence/version identification;
  plural-profile preservation; candidate adjudication; governing-rule
  revision; neighboring-case failure prediction; cross-domain transfer
  (held-out domain); inter-rater agreement (Krippendorff α on independent
  double-scoring); compression at equal correctness; operator burden
  (timing + a standardized load scale); terminology-caused execution
  errors. Negative-control burden is a GUARD/cost endpoint, not an
  efficacy endpoint.
- **Minimum important effect (pre-registered):** +15 percentage points on a
  primary rate, or a ≥0.5 SD shift on a continuous secondary; smaller
  effects are "do not adopt yet," never "harm."
- **Noninferiority/harm margins (pre-registered):** −5 pp noninferiority
  margin on primaries; harm ceiling on terminology-caused execution errors
  and negative-control over-segmentation declared in absolute counts.
- **Power:** pilot first; then **simulation-based power** from the pilot's
  mixed-model estimates (closed-form power is wrong for this crossed
  random-effects design); target ≥0.8 at the MIE. If the feasible n is
  underpowered, declare it *in advance* and downgrade every conclusion to
  "indicative — cannot support adoption OR retirement."
- **Model executors:** ≥2 model families; **pinned model versions and
  decoding settings**; repeated runs per model×arm×item with run as a
  random effect; **fresh context per item** so vocabulary exposure cannot
  carry across items or arms.
- **Human raters:** ≥3; **between-subject assignment for the
  vocabulary-exposure comparison** (or first-exposure-only primary
  analysis) because a rater who has seen the Arm-C primer is contaminated
  for later Arm-A/B judgments; Latin-square counterbalancing for item
  order within arm; report within-session drift (early vs late items).
- **Blinding limits (stated honestly):** Arm-C outputs contain the coined
  words, so raters cannot be fully blind. Mitigations: deterministic
  rubric scoring wherever the endpoint permits; lexical scrubbing of
  coinages before human rating where meaning survives; every endpoint
  scored unblinded is reported as such.
- **Analysis:** mixed-effects model with random effects for item, rater,
  and executor-run; arm as fixed effect; Holm–Bonferroni across secondary
  families; primaries handled by the gatekeeping/alpha-split rule above.
- **Compression at equal correctness:** defined by constrained/Pareto
  comparison — token counts compared only among accuracy-matched
  responses (or an accuracy-adjusted regression reported alongside); and
  **primer cost is charged**: report per-item compression AND amortized
  compression (primer tokens + N items), so a heavy primer cannot be
  hidden.
- **"Arm C beats Arm B overall" — exact definition:** Arm C wins iff it is
  non-inferior on every primary (−5 pp margin) AND superior by the MIE on
  at least one primary or on compression-at-equal-correctness, with no
  secondary regressing beyond the harm ceiling. **An ordinary
  nonsignificant tie ⇒ DO NOT ADOPT YET; only an adequately powered
  equivalence result retires the words for interface use** (distinctions
  stay in ordinary language). This supersedes any earlier "ties go to Arm
  B ⇒ retire" reading.
- **Three-outcome rule (per target):** *adopt* only on an adequately
  powered win; *do not adopt yet* on insufficient evidence (including
  underpowered nulls and ordinary ties); *retire/reject* only on an
  adequately powered equivalence/null or a harm-ceiling breach. A term is
  never called useless on an underpowered miss.
- **Preregistration artifact:** freeze the protocol, the scoring manual,
  and the adjudication procedure; **publish a SHA-256 of the frozen
  packet before any run**; deviations are reported against the hash.

---

**DESIGN-FREEZE-V0 (Phase D, 2026-07-17; versioned in Phase E).** NOT the final confirmatory preregistration (n, item variants, rater composition unresolved; see orthemic-terminology-pilot-protocol.md). Any change is a superseding version, never a silent edit. Original text: Protocol + scoring rules above are frozen after the three-way review. SHA-256 of this document at freeze (everything above this block): `ff68084f61933912aef3830fca7c1a3bb2f2142ed34c2c86285276bfb57967b5`. Any run must cite this hash; deviations are reported against it. The benchmark remains UNRUN.
