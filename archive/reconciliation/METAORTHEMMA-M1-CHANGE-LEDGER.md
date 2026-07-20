# METAORTHEMMA M1 — CHANGE LEDGER

**Date:** 2026-07-19 · Claude Fable 5 (`claude-fable-5`), Thread A.
**Governing decision:** owner chose **(b) M1 — configuration-token**, under the owner's ten-point controlling interpretation (recorded verbatim in the owner's decision message; adjudication basis: `METAORTHEMMA-DISTINCTION-ASSESSMENT.md`).
**Status:** PROPOSED layer applied **on top of the validated D1 candidates**. Canonical parents untouched (re-hashed this gate — unchanged). The D1 layer remains separately reviewable: `D1-COMPLETE-DIFFS.patch` + the frozen copies in `candidates\d1-stage\`.

## Identities

| Artifact | SHA-256 |
|---|---|
| core candidate (now D1+M1) | `dab3a21b860a483adc3226690cdefd081c1cf95aca9e3465cf2a029f2b8cfdc9` (44,094 B) |
| draft candidate (now D1+M1) | `1a46764c1afcb75188de363fac6316af4d3561a292c9294b60276e6eb39f8d08` (88,637 B) |
| note candidate | `41111140184c6dbe0a7153bc08ebc93c897659c286462755757ea6c330f78adf` — **unchanged** (no metaorthemma content applies) |
| `METAORTHEMMA-M1-INCREMENTAL-DIFFS.patch` (D1-stage → current; 2 files, 9 hunks; core +46/−2, draft +4/−2) | `9cabc02851134199e8727833dabf589608c9e06568d65aa4639dfa616f48e195` |
| `CUMULATIVE-D1-M1-DIFFS.patch` (canonical → current; 3 files, 31 hunks) | `3a60cb698b5a832179b98cd7e9af9670b1ba3a68176cfe08280424415ef64570` |
| D1-stage frozen copies | core `6e123821…`, draft `82321a31…`, note `41111140…` (= D1 validation state) |

## Owner-point → edit map

| Owner point | Implemented by |
|---|---|
| 1. Token = episode-local, case-bound; not the episode, not the execution | Core §1 qualification paragraph; core §3 type-vs-token paragraph; §2.2/§8.2 record text |
| 2. Four layers (μ / π_μ / μ̄ / execution); M2 = derived view only | Core §3 paragraph; `ApplyEvent(μ̄, e) = ⟨μ̄, Trace_e|_μ̄⟩` stated as derived, not primitive (core §2.2 row) |
| 3. Token record/reference fields | Core §2.2 `MetaTok(e)` table row (full field list: identity/lineage, `(μ, ver)` via `MetaInst`, `(A(e), ver)` via `Compatible`, `(κ, v)`, `g`, binding map `B`, scope `σ` + dependent claims, policy/evidence-selector/instrument/calibration refs, binder + `w_bind`, designated executor, `t_bind`, validity); draft §8.2 prose (compressed) |
| 4. No absorption of evidence/trace/output | "references … never absorbs" clauses in both records |
| 5. Binder ≠ executor | Explicit in both records and the V3c isolation sentence |
| 6. `Compatible(μ̄, A(e))`; no hidden second analysis | Core §2.2 row + §3 paragraph ("references any value `A` fixes uniquely; never overrides `A` without an explicit new analysis version") |
| 7. Substantive V3c; per-token statuses; lettering deferred to D3 | Core §4.1 V3c bullet (full `TokenAdequate` conjunction, per-token statuses, ordering note); draft §8.3 V3c row; core status-ledger qualification |
| 8. Zero-burden rule | `MetaTok(e) = ∅ ⟹ V3c ∉ App(e)` in both records and both verdict entries |
| 9. Subobject of the sixth addition; not a seventh | No contributions/additions text changed anywhere; core §3 calls `MetaInst` "a typing of tokens, not a second ground-truth primitive" |
| 10. Word stays benchmark-gated candidate | Core §1 qualification closing sentence; draft glossary entry ("candidate term; object adopted"); no terminology file touched |

## Notation decision (documented deviation)

The owner offered `q_e^i / μ̄_e^i`. The candidates use **`μ̄`** (`MetaTok(e) = {μ̄_1,…,μ̄_j}`): lowercase `q` collides with Def 7's representation variable (`inf_{q ∈ Q} R*(q)`) and visually with the claim ledger `Q`. Final glyph revisable under the deferred symbol-table decision (D4).

## Deliberate no-changes

- **Note candidate:** zero metaorthemma content (multi-actor material does not use it).
- **Draft §8.4 matrix and §8.5 stopped-clock:** untouched — their cell labels are O2-contested territory; M1's effect on them is stated in the assessment and will be integrated with the O2 edit (E2/E3), not before.
- **Core lines 15–26 Gate-B provenance blockquote** (incl. its verdict-vector list without V3c): historical provenance body, not rewritten per the standing rule; the banner already directs readers to candidate status.
- **Six-additions count and §1.5/§14 contributions text:** unchanged (owner point 9).
- **Terminology spec/pilot files:** untouched; whether the *word* `metaorthemma` enters the benchmark's Arm-C/ablations is a separate future terminology-lane owner decision (same class as the raw-1070 orthing inclusion), deliberately not asked now.

## Validation notes

Canonical parents re-hashed after all edits: unchanged (`18a693c5…`, `7ac99acb…`, `53d347c8…`). Incremental patch reviewed: all 9 hunks trace to the ten owner points (no scope expansion; the D1 validation report's eight tests are unaffected — no D1 text was modified by this layer, only added to). Candidates remain PROPOSED; nothing promoted.
