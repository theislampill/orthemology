# Terminology Benchmark — Pilot Protocol (v0-pilot rev. Gate H; DO NOT RUN without owner approval)

> Restructured at **Gate H (Fable 5, 2026-07-17; owner decision 12)** into a
> two-stage pilot. Builds on **design-freeze-v0** (SHA recorded in
> `orthemic-terminology-evaluation-spec.md`) — that hash stays labeled
> design-freeze-v0, a DESIGN freeze, never a final confirmatory
> preregistration. The benchmark itself remains DEFERRED (owner decision).
> The previous single-stage plan (2 executors × 4 arms × 36 items × 2
> repetitions = 576 runs) was too large for a first pilot and is superseded.

## Arms (unchanged)

A (ordinary language); B (distinctions in ordinary words WITH a concise
**length-matched glossary** — matched to Arm C's primer length so
compression is not confounded by primer availability); C (coined
vocabulary); **C′ sham-label control** — the same distinctions under
invented labels matched to the coinages in **length, pronounceability,
memorability, morphology, mnemonic structure, semantic transparency,
syllable count, AND primer complexity** (never arbitrary K1/K2/K3 codes) —
otherwise Arm C wins merely because real terms are meaningful Greek-derived
labels while shams are noise. Isolates the value of THESE terms from the
value of any concise, learnable labels.

## Pilot 0 — rubric and item debugging (SMALL; no utility or variance claim)

- **Purpose:** detect broken items, ceiling/floor effects, scorer
  ambiguity, primer confusion, and sham-control defects. Nothing else.
- **Size:** a balanced subset — 1 variant from each of the 12 construct
  families (including the multi-actor family) + the negative controls;
  1 model executor; all 4 arms; 1 repetition. ≈ 48–60 runs.
- **Output:** corrected items/rubrics/primers/sham labels. **No
  adoption/retirement or variance conclusion may be drawn from Pilot 0**;
  its transcripts are RUBRIC/ITEM DEBUGGING ONLY.

## Pilot 1 — variance/power pilot (only after Pilot 0 corrections)

- **Items:** 3 variants per construct family (12 × 3 = 36). The **2
  held-out transfer domains are ADDITIONAL to the 36** (used only for the
  cross-domain transfer endpoint), never a subset.
- **Size:** 2 model executors × 4 arms × 36 items × **2 repetitions**
  (one repetition cannot identify an executor-run variance component).
  Fresh model context per run.
- **Raters:** 3 human raters double-scoring 20%; vocabulary-endpoint
  judgments use BETWEEN-ARM or first-exposure-only assignment (a rater who
  has seen the Arm-C primer is contaminated for later Arm-A/B judgments).
- **Scoring:** deterministic rubric per item; **term-swap/confusion
  scoring** (a misapplied coinage is its own error class); primer-learning
  check (early-vs-late accuracy per arm); carryover check across the
  counterbalanced Latin square.
- **Analysis:** variance components (item / rater / executor-run) feeding
  simulation-based power for the confirmatory study. **No
  adoption/retirement decision may be drawn from Pilot 1.**

## Then

Freeze confirmatory **v1** (exact n, item set, rater pool, scoring manual,
margins, analysis) as a superseding version citing design-freeze-v0. Any
change after a freeze is a superseding version, never a silent edit.
