# R4 PR #3 — Fresh Fable Hunk-by-Hunk Review of the Post-Substitution Range (Phase C)

Range reviewed: `00cf05d6..de19ccf4` — the two post-substitution commits
`b2742d1` (Phase E) and `de19ccf4` (Phase F), labeled POST-SUBSTITUTION
CANDIDATE work by the interruption record. Nothing here inherits that
session's conclusions: every hunk was re-derived against the tree and the
validators by this session. Session surfaced model at this phase boundary:
`claude-fable-5`; no substitution observed.

Change-kind legend: T = theory, S = source status, P = prose, R = repository
integration, G = generated surface, H = historical/provenance record.

## Commit b2742d1 (Phase E) — hunk dispositions

| File | Kind | Disposition | Evidence / notes |
|---|---|---|---|
| `references/latent-state-additions.bib` (deleted) | R | **keep** | fragment retired; content merged verbatim into the main bibliography; `validate_claim_sources.py` now fails on any stray `.bib` |
| `references/orthemology.bib` (+73) | S/R | **keep** | three records (sun2025orthogonalized, george2021clone, raju2024space) present with binding scope note; Raju/Rikhye author-conflation correction preserved; author-field guard green |
| `references/source-status.yaml` (LAT-1..LAT-3) | S | **keep** | rows exist, DOIs cross-checked by `validate_claim_sources.py`; statuses scoped to Crossref-record verification only |
| `docs/decisions/0015-…md` amendment | T/S | **keep** | A1.1–A1.7 verified against the machinery: six-objects-plus-index reading; non-identifiability conditional on absent anchoring; transport conditionally prohibited (validated alignment map licenses it); statability scoped to CORE claims (extension vocabulary not required to be core-expressible); rebinding categories may co-occur; model artifact identity distinct from analysis version; LS checks stated as contract assertions, not empirical validation |
| `manuscript/…revised-draft.md` §12.1 (+20) | P | **keep** | bounded related-work subsection; claims framed as the sources' reported findings; "among the compared models under the reported evaluation" scope preserved; no identification of latent states with orthemes; no empirical-validation claim; no fiṭrah / metaphysical orthability / Necessary Being / divine Speech inference |
| `theory/orthemic-core-formalization.md` (+13) | T | **keep** | bounded cross-reference only; latent layer optional and non-primitive; core claims statable without it; ProfileOf_A partial and exhibited-never-assumed |
| `docs/related-work/LATENT-STATE-…md` (1 line) | R | **keep** | bibliography pointer updated to the merged main bib + LAT rows |
| `docs/sourcing/SOURCING-LEDGER.md` rows 36–38 | S | **keep with repair** | REPAIR (this review): the rows were inserted after a blank line, severing them from the Markdown table — they rendered as literal pipe text with no header. Blank line removed; rows join the table. Content itself verified accurate |
| `docs/sourcing/CLAIM-SOURCE-MATRIX.md` (+1 row) | S | **keep** | inverse-view row consistent with ledger rows 36–38 and the 0015 boundary |
| `scripts/validate_claim_sources.py` (+35) | R | **keep** | stray-.bib guard, both re-orphaning directions, author-field-scoped erroneous-form ban. Accepted limitation (noted, non-blocking): the author-line heuristic joins continuation lines by trailing "and", so a wrapped final author line is outside the scanned set; the three shipped entries are fully covered |
| `docs/project-closure/r4-independent-review/LATENT-RELATED-WORK-INTEGRATION-REVIEW.md` | H | **keep with revision** | additive dated PROVENANCE QUALIFIER added by this review: authored in the post-substitution window; the "harness identity claude-fable-5" line is that session's internal claim only; owner observed claude-opus-4.8; unadjudicated; original text unmodified |
| `docs/current-state.yaml` | G | **keep (supersede)** | generated; regenerated again by this review in Phase D order |
| `docs/provenance/RELEASE-MANIFEST.sha256` | G | **keep (supersede)** | generated; regenerated last in Phase D order |

## Commit de19ccf4 (Phase F) — hunk dispositions

| File | Kind | Disposition | Evidence / notes |
|---|---|---|---|
| `docs/decisions/0013-…md` amendment | S | **keep** | registry rescope (honest coverage) + CIR-1 split rationale; verified against the registry and validator |
| `references/source-status.yaml` (scope + CIR-1W + ATH-3) | S | **keep** | see C2–C4 below |
| `scripts/validate_source_status.py` (+63) | R | **keep** | scope enforcement (family membership both directions), record-shape honesty statement, [via compilation] agreement guard; guard reviewed in C4 |
| `docs/project-closure/r4-independent-review/SOURCE-INTEGRITY-REVIEW.md` | H | **keep with revision** | same additive PROVENANCE QUALIFIER as the Phase E report |
| `docs/current-state.yaml`, `RELEASE-MANIFEST.sha256` | G | **keep (supersede)** | regenerated in Phase D order |

## C1. Decision 0015 — abstract integration only (scope boundary observed)

This review inspected only the repository's existing abstract
state-estimation/model-boundary text, source metadata, fixtures, and citation
integration. The underlying domain-specific experimental procedures were not
opened, summarized, reproduced, or operationalized, and no domain-specific
research lane was launched.

Verified: all three bibliography records live in `references/orthemology.bib`
(`ls references/*.bib` shows exactly one file); no orphan fragment; LAT-1..3
source-status rows and sourcing-ledger rows 36–38 plus a claim-source-matrix
row exist; manuscript §12.1 is bounded; the formal core carries only a bounded
cross-reference; source claims are framed as the sources' reported findings
with the "among compared models under the reported evaluation" scope; model-
state labels are non-identifiable absent declared anchoring; validated
transport maps license cross-version transport; extension-specific vocabulary
is not required to be core-expressible; rebinding categories may co-occur;
model artifact identity is distinct from analysis version; no model state,
posterior, cluster, or internal representation is identified with an ortheme;
no empirical validation of orthemology is claimed; no inference to fiṭrah,
metaphysical orthability, a Necessary Being, or divine Speech.
`validate_latent_state_fixtures.py` (LS-1..LS-7 + anti-conflation assertions)
green on this tree.

## C2. Source-status scope

The Phase F choice — **authoritative only for explicitly declared claim
families** (`CIR-*`, `ELT-*`, `ATH-*`, `LAT-*`, `EXT-*`) with a machine-declared
`not_covered` block — is the honest contract and is **adopted**. The validator
enforces the scope in both directions (no row outside a family; no declared
family empty) and states that a green run establishes record shape and
internal agreement, never worldly truth. Minor noted (non-blocking): the
header check that forbids reasserting whole-corpus coverage matches a
line-wrapped literal and is brittle against rewrapping; it is a redundant
negative guard on top of the real scope enforcement.

## C3. CIR-1/CIR-2 attribution chain

Verified as kept separate: CIR-1 bibliographic metadata for Doko & Turner
2023 (`SECONDARY_VERIFIED`, with `status_scope` restricting it to
bibliographic facts); CIR-1W exact in-chapter wording/application
(`COMPILATION_MEDIATED`, promotion trigger = direct publisher full-text
access, never load-bearing alone); Evans origin attribution as reported by
the chapter (CIR-2); Turner 2022 and Turner 2023 as distinct works; El-Tobgui
2013/2018/2020 as three distinct records (ELT rows). No wording claim was
upgraded from a compilation to direct publisher verification by that session
or by this one.

## C4. ATH-3 evidence-access adjudication

The conflict was reproduced from the tree: the R4 candidate registry carried
`PRIMARY_TEXT_EXACT` / `wording_directly_checked: true` for the *Majmūʿ
al-Fatāwā* vol. 12 formula while the companion labels the same locus
**[via compilation]** (companion line citing 12/98, similarly 12/53). Two
surfaces made incompatible evidence-access claims about one citation; the
Phase F downgrade takes the weaker claim.

This fresh session **did not** open a printed edition or demonstrate an
authoritative direct full-text rendering of *Majmūʿ al-Fatāwā* vol. 12, so no
upgrade is made from memory. Disposition: **retain `COMPILATION_MEDIATED`**,
with the edition/page residual (RR-1, pagination edition-dependent), the
recorded promotion trigger (direct edition or authoritative full-text access),
the explicit statement that the adopted Atharī doctrine is not altered, and
no load-bearing claim resting on this row alone (doctrine carried by
ATH-1/ATH-2 primary texts).

Guard review (Unicode/ASCII normalization and false matches): the `fold`
helper NFKD-normalizes, strips combining marks and non-ASCII, and lowercases,
so `Majmūʿ al-Fatāwā` (prose) and `Majmu' al-Fatawa` (registry) meet on the
`majmu` token — the unfolded mismatch is exactly why the original
contradiction survived. False-match risk: the token list includes generic
stems (`sharh`), so a future PRIMARY_TEXT_EXACT row citing a *different*
sharḥ could false-flag against a [via compilation] passage citing
al-Lālikāʾī's Sharḥ. This fails in the safe direction (it forces a
reconciliation rather than hiding one) and is accepted as a bounded guard
over the small fixed corpus. Tamper probe re-run by this session: restoring
`status: PRIMARY_TEXT_EXACT` on ATH-3 fails the guard; restoring the
downgrade returns 0 failures.

## C5. Internal-reference integration

`scripts/validate_internal_references.py` and `docs/reference-exemptions.yaml`
are **quarantine-only** (not in this range); they are reviewed in Phase D
(`QUARANTINE-PORT-REVIEW.md`).

## Validators after Phase C repairs

`validate_source_status.py`, `validate_claim_sources.py`,
`validate_cross_document_consistency.py`, `validate_latent_state_fixtures.py`,
`validate_quran_loci.py`: **0 failures** each on this tree (UTF-8 console).
