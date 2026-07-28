# Decision 0028 — Represented metaorthemes and memetic ecology

**Date:** 2026-07-21 · **Authority:** R7C owner authorization (Opus candidate pass) · **Status:** proposed-candidate (R7C grandchild) · **Reopens nothing:** Decisions 0001–0027 stand; this **types** what Decision 0025 sketched. daee pinned `c86b3c66`.

**Provenance:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE. No empirical or theological claim; asserts no soul access, no epistemic warrant from count.

## Problem

R7B (Decision 0025) introduced the represented-standard bearer `μ̃` and the
ecology `Γ^μ` but left `μ̃` under-typed (no identity/version/stance/fidelity/
lineage; audit B11) and the ecology a vocabulary list, not a governed graph
(B12), and reduced false tawātur to a "common upstream source" label without the
dependence structure the Taymiyyan material requires (B13).

## Decision

**1. Represented-standard record (`μ̃`).** `REPRESENTED-STANDARD.schema.json`
(+ `.example.json`): `⟨id, version, bearer, represented_content,
represented_metaortheme_types, stance, scope, provenance, validity,
fidelity_status, uncertainty, lineage⟩`. **RepMeta is many-to-many** — one
represented standard may combine several metaortheme types; one type may have
many faithful/partial/distorted/hostile representations.

**2. Carrier stance is explicit** (enum): `expresses`, `quotes`, `endorses`,
`embodies`, `applies`, `opposes`, `distorts`, `transmits`. Mention/quotation is
not endorsement; a carrier token is not automatically a faithful instance
(`fidelity_status`).

**3. Governed ecology graph.** `MEMETIC-ECOLOGY.schema.json` (+ `.example.json`):
typed, versioned, provenanced, status'd nodes (actor / institution / artifact /
represented-standard / metaortheme-type / episode) and edges (transmission,
copying-dependence, citation, endorsement, application, mutation, reinforcement,
rebuttal, replacement, supersession). **Mutation edges declare a
`mutation_identity`** — same-standard-new-token / new-version-same-standard /
mutation-preserving-function / new-governing-type — decided by ablation, not
wording similarity.

**4. False tawātur has dependence structure.** Each `tawatur_analysis` records
origin, independent routes, common source, copying dependence, mutation lineage,
and qualitative indicants. **Any common source or copying dependence forbids
`tawatur-like-independence`** — warrant never rests on count, graph degree,
popularity, or institutional prevalence (fixtures TW1–TW6).

**5. Gate.** `scripts/validate_memetic_ecology.py` (CI) schema-validates both
examples, checks graph integrity (endpoints resolve, mutation edges typed), and
enforces the tawātur warrant rule.

## Non-claims

No truth is created by social stabilization; the ecology models transmission and
mutation of **represented standards**, not any actor's interior state, motive, or
soul. No warrant follows from count or degree.
