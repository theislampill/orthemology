# Decision 0027 — Multi-target noetic orthing and claim bearers

**Date:** 2026-07-21 · **Authority:** R7C owner authorization (Opus candidate pass) · **Status:** proposed-candidate (PR #9-child / R7C grandchild) · **Reopens nothing:** Decisions 0001–0026 stand; this extends the Decision 0021 daee application. daee pinned `c86b3c66`.

**Provenance:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE. No empirical or theological claim; asserts no soul access.

## Problem

The R7/R7B daee crosswalk typed the immediate `m` (this objection/utterance/
document) as the episode's orthemma and treated the person's interior condition
as `O*(m; A)` of that **same** `m` (audit B9). That is a category error: the
actual profile of an utterance is not the interior condition of the speaker. A
deformation ortheme, if anything, belongs to the **subject** under a declared
analysis — never to the utterance merely because the utterance is observed.

## Decision

**1. Five possible occurrence bearers per episode** (not automatically the same
orthemma):

```text
m_discourse  the concrete objection / utterance / document / engagement (observed)
m_subject    the person-at-time / noetic bearer — in scope only when legitimately
             targeted, and NOT directly observed (inferred under uncertainty)
m_runtime    the DAEE runtime / Diagnostic-IR control state
m_response   the released response artifact
m_uptake     a later, separately observed uptake / restoration occurrence, if any
```

**2. Every noetic claim names its target.** A claim records: target occurrence
(identity + version), target type, evidence IDs, evidence scope, analysis,
status (`asserted`/`held`/`underdetermined`/…), uncertainty, and explicit
non-claims — using the existing claim-ledger target fields where sufficient.
Machine form: `applications/daee-epistemics/NOETIC-TARGET-MAP.schema.json`
(+ `.example.json`).

**3. Observation bridge.** Discourse is **evidence about** a possible
subject-level target, never identical to it:

```text
ObservedFrom(h, m_discourse)   About_A(h, m_subject)
```

`About` does **not** establish that the evidence is true, sufficient, or
uniquely identifying (`observation_bridge[*].establishes_truth = false`).

**4. What "DAEE operates metaorthemes on orthemmata" decomposes to** — no rule
"operates on the soul":

1. a **discourse** orthemma enters the episode;
2. **metaorthemes** govern how the runtime distinguishes evidence, source
   status, noetic alternatives, routes, and closure;
3. **metaorthemmata** bind those governing standards to this case;
4. some claims may concern a linked **subject-level** target, only through
   appropriately scoped evidence;
5. the **executor** operates on records, claims, routes, evidence, and the
   response plan;
6. the episode produces a **response** orthemma;
7. the language-mediated relation to later **uptake** is partial and uncertain.

**5. Gate.** `scripts/validate_noetic_targets.py` (CI) schema-validates the
example and enforces, over fixtures NT1–NT10: **R1** no subject-interior type is
asserted of `m_discourse`; **R2** subject claims are held/underdetermined (or, if
asserted, claim no direct/unique interior access) and carry a no-soul-access
non-claim; **R3** every claim carries a non-claim.

## Non-claims

DAEE is a **multi-target, metaortheme-governed noetic orthing application** — not
a direct classifier or editor of hidden souls. No operation manipulates or
asserts an interior soul-state; every subject-level claim is inferential, scoped,
and held under uncertainty.
