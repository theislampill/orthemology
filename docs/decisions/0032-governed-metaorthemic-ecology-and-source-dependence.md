# Decision 0032 — Governed metaorthemic ecology and source dependence

**Date:** 2026-07-21 · **Authority:** R7D owner authorization (Opus candidate pass) · **Status:** proposed-candidate · **Reopens nothing:** Decisions 0001–0031 stand (amends Decision 0028's ecology + tawātur model).

**Provenance:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE.

## Problem

The R7C ecology had a typed vocabulary but not graph semantics (B17–B20, probes
P5/P8): the schema accepted duplicate node IDs (a `set` silently deduped them),
endorsement between two artifact nodes, and a transmission edge that named no
transmitted standard; a `mutation_identity` enum asserted a mutation without a witness;
and the truth firewall was prose only. The tawātur rule was indefensible (B21–B23,
probe P6): the function returned `tawatur-like-independence` whenever the independent-
route count was two or more with no dependence — so two routes became tawātur. It also
permitted more independent routes than apparent witnesses, and empty qualitative
indicants.

## Decision

**1. Graph semantics.** `validate_memetic_ecology.py` enforces unique node and edge
IDs; typed endpoints per `edge_type` (e.g. endorsement targets a represented standard;
application maps a represented standard to an episode; copying-dependence is
artifact→artifact); a `transmission` edge must name a `transmitted_standard` resolving
to a represented-standard node; and a `mutation` edge must carry a structured
`mutation_identity` witness (compared versions, preserved invariants, changed fields,
an ablation/functional witness, evidence, assessor) — not a bare enum.

**2. Truth firewall (machine-readable).** No node or edge may assert warrant from
propagation, popularity, institutional stabilization, or degree. Propagation ⇏ truth
or normative adequacy is a machine check, not only prose.

**3. Independence vs tawātur warrant (the F split).** The **machine** conclusion is
source-safe and is one of `dependence-detected` (any common source or copying),
`source-independence-supported` (≥2 independent routes), or
`origin-analysis-underdetermined`. It **never** concludes tawātur warrant;
`tawatur-like-independence` is removed from the machine vocabulary. Creed-internal
tawātur **warrant** is a separate, school-labeled `TAWATUR-WARRANT` record making
origin, path independence, qualitative/circumstantial indicants, no-collusion, content
coherence, mutation lineage, defeaters, and source status load-bearing; it encodes no
universal numerical threshold and treats the Taymiyyan material as secondary
reconstruction until primary loci are verified. The schema also enforces that
independent routes never exceed apparent witnesses, and requires non-empty qualitative
indicants.

## Non-claims

Graph and source-dependence discipline only; reopens no settled Decision, adopts no
terminology, runs no experiment, and asserts no interior/soul claim. Number, degree,
popularity, and institutional prevalence are never epistemic warrant.
