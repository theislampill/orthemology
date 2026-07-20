# Phase E — bounded sequential latent-variable related-work integration (R4 independent review)

**Date:** 2026-07-20 · **Session:** independent Fable review of PR #3 (harness identity `claude-fable-5`).

## Scope boundary observed

Per the controlling instruction, this review inspected **only** the repository's already-authored abstract sequential-latent-variable boundary, its formal distinctions, its source metadata, and its citation integration. It did **not** re-open, reproduce, inspect, or operationalize the underlying experimental procedures, and it launched no domain-specific research lane. Bibliographic verification rests on the R4 pass's official publisher/Crossref records; no re-fetch of the study text was performed or needed for the repository-integrity work below. That access limitation is recorded honestly here and in the ledger, and it blocked nothing.

## What was wrong (audit §8, reproduced)

The candidate carried a real Decision 0015, a related-work note, a worked Markdown example, and LS-1…LS-7 contract fixtures — but the *repository integration* the controlling amendment promised was absent, and several formulations were stronger than the machinery supports.

| Defect | Status at candidate head `25d035a` |
|---|---|
| Three sources in an orphan `references/latent-state-additions.bib`, invisible to `validate_claim_sources.py` (which reads only `orthemology.bib`) | reproduced |
| No `source-status.yaml` rows | reproduced |
| No sourcing-ledger or claim-source-matrix rows | reproduced |
| No bounded related-work subsection in the manuscript | reproduced (no "latent" text anywhere in `manuscript/`) |
| No formal-core cross-reference | reproduced (none in `theory/`) |
| "six-way typed distinction" vs a seven-row table | reproduced |
| Non-identifiability, transport prohibition, and statability stated absolutely | reproduced |
| Rebinding categories presented as if exclusive | reproduced |
| Model artifact identity not distinguished from analysis version | reproduced |
| "190 checks" presentable as empirical validation | reproduced as a wording risk |

## Repairs

**Integration (E1).** The three records were merged into `references/orthemology.bib` under a scope-of-citation header carrying the Decision 0015 §8 first-author correction and the CSCG nomenclature note; the fragment was **retired** (deleted). Rows **LAT-1…LAT-3** added to `references/source-status.yaml` — each stating exactly what the source supports and, explicitly, that it does not identify latent states with orthemes, does not validate orthemology, supplies no etymological support for "ortheme", and bears nothing on fiṭrah, metaphysical orthability, Necessary Being, or divine Speech. Rows **36–38** added to `docs/sourcing/SOURCING-LEDGER.md` plus a new honest-residual paragraph recording the deliberate non-reproduction of the experimental procedures; one row added to `docs/sourcing/CLAIM-SOURCE-MATRIX.md` with its permitted and forbidden strengths. The manuscript gained **§12.1** (bounded related-work subsection) and `theory/orthemic-core-formalization.md` gained a concise cross-reference before its status ledger. The related-work note's stale "bibliography fragment" pointer was corrected.

**Anti-re-orphaning (E4).** `validate_claim_sources.py` now fails on **any** stray `.bib` beside `orthemology.bib`; requires each of the three keys to be present in the main bibliography **and** to carry a source-status row by DOI; and forbids the erroneous first-author form in any `author` field (scoped to author fields, since the comment block and the entry note deliberately record the error in order to forbid it). All three guards were tamper-probed in both directions: introducing a stray fragment fails; putting `Raju, Rajeev V.` in an author line fails; reverting restores green.

**Precision (E2).** A dated amendment to Decision 0015 corrects: the six/seven count (six represented object kinds plus the analysis index); non-identifiability as holding **absent semantic anchoring/alignment constraints**; transport as prohibited **without an explicit validated alignment/transport map**; statability scoped to **core** orthemology claims, with declared extensions free to use their own vocabulary for extension-specific claims; rebinding categories as non-exclusive kinds that may co-occur (what is forbidden is leaving unstated which changed); model artifact identity/version as distinct from analysis version; and LS "checks" as deterministic contract assertions over authored fixtures, explicitly **not** empirical validation.

**Anti-conflation rules preserved (E3).** §§1–7 of Decision 0015 are unchanged: occurrence ≠ observation ≠ model state; posterior ≠ ground truth; internal representation ≠ worldly state; model-state difference does not yield an ortheme; global geometric orthogonality is neither necessary nor sufficient for orthemic distinction or strict soundness (and its absence is not by itself a pathway defect); endpoint match does not prove mechanism match; no one-unit/one-type inference; not every cue remapping is a metaorthemma.

## The bounded claim as it now stands in the corpus

> A published sequential-learning study provides a neighbouring example in which ambiguous immediate observations are disambiguated by sequence-sensitive latent-state inference; final task performance and final representation do not by themselves determine the learning trajectory or mechanism. This does not identify latent states with orthemes and does not validate orthemology.

The source's reported findings are reported **as that source's reported findings**, with the trajectory-match claim scoped among the compared models under the reported evaluation, never universally.

## Verification at claim time

`validate_claim_sources.py`, `validate_source_status.py`, `validate_latent_state_fixtures.py`, `validate_cross_document_consistency.py`, `validate_repo.py`, `validate_current_state.py`: **0 failures each**, re-derived from the tree after the last edit.
