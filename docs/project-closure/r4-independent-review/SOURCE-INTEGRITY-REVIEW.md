# Phase F — source-status and attribution integrity (R4 independent review)

**Date:** 2026-07-20 · **Session:** independent Fable review of PR #3 (harness identity `claude-fable-5`).

> **PROVENANCE QUALIFIER (added 2026-07-20 by the fresh Fable recovery review; original text below is unmodified).**
> This report was authored inside the post-substitution window (commit `de19ccf4`,
> after the last definitely pre-substitution commit `00cf05d6`). The "harness
> identity `claude-fable-5`" line above records that session's *internal harness
> claim only*; the owner observed a UI substitution to `claude-opus-4.8` for this
> window (see `docs/project-closure/r4/MODEL-SUBSTITUTION-INTERRUPTION-PR3.md`).
> Neither observation is adjudicated. This report is POST-SUBSTITUTION CANDIDATE
> material; its findings were independently re-verified by the fresh review in
> `docs/project-closure/r4-fresh-fable-review/POST-SUBSTITUTION-HUNK-REVIEW.md`.

The supplied epistemology collection and the El-Tobgui dissertation were treated as **research inputs**, not automatically as primary texts. The adopted Atharī doctrine was not altered; only evidence-status precision was audited.

## F1. Registry scope — rescoped honestly rather than inflated

Decision 0013 declared `references/source-status.yaml` authoritative for **every load-bearing claim**. Reproduced and false: the registry carries 20 rows while the sourcing ledgers carry 38 plus the companion ledger and the Qurʾānic locus registry. Of the audit's two honest options, expanding the registry to cover every load-bearing claim would have meant manufacturing rows to match a slogan, so the registry is **rescoped to what it actually adjudicates**, with the coverage now machine-declared in the file:

- `covered_claim_families`: `CIR-*` (concrete/ideal-reason chain), `ELT-*` (El-Tobgui records), `ATH-*` (enumerated Atharī claims), `LAT-*` (latent related work), `EXT-*` (this project's extension).
- `not_covered`: names the surfaces carrying the rest (`docs/sourcing/SOURCING-LEDGER.md`, the companion ledger, `references/quran-loci.yaml`) and states explicitly that **absence from this registry is not a claim that a source is unverified**.

`validate_source_status.py` enforces it: every row must belong to a declared family (probe: an out-of-family `ZZZ-1` row fails), every declared family must have rows, the header may not reassert whole-corpus coverage, and the header must state that the validator does not verify source truth. Decision 0013 carries a dated amendment recording the rescope.

**What the validator establishes** is now stated in its own docstring and in the registry header: offline record-shape and internal-agreement checks. It does **not** verify that a source is true, that a quotation was read, that a page locus is right, or that a DOI resolves. A green run is evidence about the records, never about the world.

## F2. Concrete/ideal reason chain — CIR-1 split

`CIR-1` carried `SECONDARY_VERIFIED` while its own notes admitted publisher metadata was verified (Crossref, Cambridge Core) but the chapter text was read only through the supplied compilation, the publisher's version returning 403. Two claims, two evidence accesses, one status. Now two rows:

- **CIR-1** — bibliographic existence/authorship/DOI/pages: `SECONDARY_VERIFIED`, with an explicit `status_scope` field saying the status covers bibliography only.
- **CIR-1W** — exact in-chapter application/wording: `COMPILATION_MEDIATED`, with a recorded promotion trigger (direct publisher full-text access) and an explicit statement that no corpus claim rests on it alone.

The rest of the chain was audited and is correct as it stands: **Doko & Turner 2023** credited as the verified modern application (Doko is a co-author and is credited in prose); **Evans 1998** as the reported underlying distinction with the p. 94 locus never asserted as directly verified (`SECONDARY_RECONSTRUCTION`, `page_edition_dependent: true`, research residual RR-2); **Turner 2022** rescoped to its actual theistic-signs subject; **Turner 2023** as the distinct Common-Sense chapter; **El-Tobgui 2013 dissertation / 2018 Oriens article / 2020 Brill monograph** as three separate records (ELT-1/2/3). The supplied compilation is nowhere cited as one monograph.

## F3. Taymiyyan and fiṭrah claims

The concrete/sound distinction is preserved with bearers kept typed (concrete faculty; concrete reasoning episode; concrete placement/judgment; represented governing standard; metaorthemma; execution; result). "Concrete ortheme" as a judgment token and "concrete metaortheme" as a token are not reintroduced — verified by `validate_type_token_semantics.py` (0 failures) and by corpus grep. The circularity language stands as corrected in Decision 0011: evaluator symmetry prevents privileged self-certification and independence-aware corroboration supplies defeasible corrective evidence; neither proves non-circularity or eliminates a shared upstream source — now with fixture CR-9 and a full schema-valid bundle making shared-upstream dependence representable.

## F4. Atharī companion — one real contradiction found and repaired

**Finding (new; audit §9.2's final bullet made operational).** `ATH-3` recorded `PRIMARY_TEXT_EXACT` with `wording_directly_checked: true` for the "words of the Creator / voice of the reciter" formula in *Majmūʿ al-Fatāwā* vol. 12 — while the companion prose labels that **same locus `[via compilation]`**. One citation cannot have two evidence accesses. Unable to confirm for itself that a printed edition or authoritative full-text rendering was opened, this review took the **weaker** of the two claims: `ATH-3` is now `COMPILATION_MEDIATED`, `wording_directly_checked: false`, with the promotion trigger recorded (direct edition access, which would also settle the edition-dependent pagination, RR-1).

**The adopted doctrine is unchanged.** What changed is the recorded strength of one row's evidence access. The claim is carried elsewhere by primary texts: `ATH-1` (29 Qurʾānic loci, `PRIMARY_TEXT_EXACT`, machine-enforced by `validate_quran_loci.py`) and `ATH-2` (Muslim 2708). No claim rests on `ATH-3` alone.

**Recurrence prevented mechanically.** `validate_source_status.py` now fails any `PRIMARY_TEXT_EXACT` row whose work is cited inside a `[via compilation]`-labelled passage in the companion. The check ASCII-folds both surfaces first — a necessary detail, since the registry writes `Majmu' al-Fatawa` and the prose writes `Majmūʿ al-Fatāwā`; an unfolded substring check silently never matches, which is exactly how the contradiction survived. Tamper-probed: restoring `ATH-3` to `PRIMARY_TEXT_EXACT` fails the run; reverting restores green.

Remaining Atharī rows were audited and are correctly typed: `ATH-4` `PRIMARY_WORK_THEME` (work and theme confirmed, wording not); `ATH-5`/`ATH-6` `PRIMARY_LOCUS_EDITION_DEPENDENT`; `ATH-7` `SECONDARY_VERIFIED` and school-flagged "Ashʿarī and Māturīdī (described, not adopted)" — a modern secondary is not standing in as an unstated primary locus for a speech-specific claim, and school-internal synthesis stays distinct from neutral comparative description. Created human recitation/voice and uncreated divine Speech remain correctly distinguished in §3's vessel/carried-Word treatment.

## Verification at claim time

`validate_source_status.py`, `validate_claim_sources.py`, `validate_quran_loci.py`, `validate_type_token_semantics.py`, `validate_cross_document_consistency.py`: **0 failures each**, re-derived from the tree after the last edit. Three guards were tamper-probed in both directions (out-of-family row; stray `.bib`; `PRIMARY_TEXT_EXACT`-vs-`[via compilation]`).
