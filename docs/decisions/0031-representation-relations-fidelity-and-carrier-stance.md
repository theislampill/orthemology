# Decision 0031 — Representation relations, fidelity, and carrier stance

**Date:** 2026-07-21 · **Authority:** R7D owner authorization (Opus candidate pass) · **Status:** proposed-candidate · **Reopens nothing:** Decisions 0001–0030 stand (amends Decision 0028's represented-standard model).

**Provenance:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE.

## Problem

The R7C audit (B13–B16, probe P4) found the represented-standard record under-typed:
its example referenced a metaortheme type (`mu-type-corroboration`) absent from the
ecology (a ghost type); the schema accepted a standard listing its own id in its
lineage (self-lineage); and both `stance` and `fidelity_status` were single global
fields, so a `quotes` stance could be globally labeled `faithful`. But one represented
standard may faithfully represent one type, distort a second, and oppose a third —
fidelity and stance are properties of a **representation relation**, not of the whole
record.

## Decision

**1. Type resolution and lineage.** `validate_memetic_ecology.py` now resolves every
`represented_metaortheme_types` entry against the ecology's `metaortheme-type` nodes
(a ghost type fails) and rejects a standard that lists its own id in `lineage`.

**2. Relation-level assessment.** `REP-META-ASSESSMENT.schema.json` records fidelity
and stance per `(represented_standard, metaortheme_type)` pair: standard id/version,
type id/version, stance, fidelity, assessor, evidence, scope, uncertainty, validity.
Each type a standard represents must have an assessment row; when per-type fidelities
differ, the coarse `fidelity_status` rollup on the standard must be `partial` (never a
uniform `faithful`). The example shows `mutilde-X` faithful+endorses to `mu-type-A`
and distorted+distorts to `mu-type-corroboration`.

**3. Carrier relation.** `CARRIER-RELATION.schema.json` types carrier stance per
`(carrier, represented_standard)`: content/scope, mode (expresses, quotes, endorses,
embodies, applies, opposes, distorts, transmits), evidence, time, validity. Quotation
is not endorsement; endorsement is not faithful embodiment; application is not identity
with the represented standard.

## Non-claims

Adds relation-level typing over the existing bearers; reopens no settled Decision,
adopts no terminology, runs no experiment, asserts no soul-state, motive, or
culpability. A represented standard remains distinct from the metaortheme type, the
case-bound metaorthemma, and the execution event.
