# STATUS

**Draft / research-stage (revision R5, 2026-07-20).** This repository is a versioned working state, published honestly with its open decisions on record. The authoritative machine-readable statement of the current revision, counts, statuses, review state, and burdens is [docs/current-state.yaml](docs/current-state.yaml); this file, VERSION, README, the primary document headers, and OPEN-DECISIONS are checked against it in CI.

> **Current review state (R5, 2026-07-20): fresh-session repository review completed; not external human peer review; not empirically validated.** The R4 revision was produced as a mixed-provenance candidate under a mid-run model-provenance dispute (recorded, unadjudicated, in [docs/project-closure/r4/AUTONOMOUS-R4-STATE.json](docs/project-closure/r4/AUTONOMOUS-R4-STATE.json) and [docs/project-closure/r4/MODEL-SUBSTITUTION-INTERRUPTION-PR3.md](docs/project-closure/r4/MODEL-SUBSTITUTION-INTERRUPTION-PR3.md)). A fresh-session review then reproduced the substitution boundary, re-reviewed the pre- and post-substitution ranges hunk by hunk, selectively recovered the quarantined work, repaired its findings, and merged PR #3 through protected CI — sign-off: [docs/project-closure/r4-fresh-fable-review/FABLE-REVIEW-SIGNOFF.md](docs/project-closure/r4-fresh-fable-review/FABLE-REVIEW-SIGNOFF.md); merged-state verification: [docs/project-closure/r5/FINAL-MERGED-VERIFICATION.md](docs/project-closure/r5/FINAL-MERGED-VERIFICATION.md). That review's scope is the repository's formal, schema, source-record, and build integrity. It is **not** external human peer review, **not** empirical validation, and **not** legal/publication closure; those remain open exactly as listed below. Historical candidate reports remain intact and are classified in [docs/project-closure/HISTORICAL-STATUS-INDEX.yaml](docs/project-closure/HISTORICAL-STATUS-INDEX.yaml).

- **Not peer reviewed.**
- **No completed empirical validation** — no designed study has been run; nothing here reports an experimental result; deterministic validators check consistency only. This is not a completed paper program in the empirical sense.
- **Terminology not adopted** — orthemma, ortheme, metaortheme, metaorthemma, and orthing are candidate coinages; the pilot-0 v2 packet is **INSTRUMENT-READY PENDING BLIND HUMAN MATCHING REVIEW; NOT RUN; NO TERM ADOPTED**. `orthable` is excluded from the operational core.
- **Companion papers are complete DRAFTS, not settled results** — the school-neutral paper's conclusions are conditional on labeled premises with named unresolved exits; the Atharī paper is explicitly school-internal and never presented as neutral.
- **Sourcing: the machine registry is authoritative for its declared claim families** — [`references/source-status.yaml`](references/source-status.yaml) carries per-claim statuses for the families it declares (`CIR-*`, `ELT-*`, `ATH-*`, `LAT-*`, `EXT-*`); paper prose must agree with it bidirectionally, and blanket source-status statements are no longer used. Broader current sourcing state starts at the consolidated view [`docs/sourcing/CURRENT-SOURCING-LEDGER.md`](docs/sourcing/CURRENT-SOURCING-LEDGER.md) (R3 overlays are current where they regrade; the R2 ledgers are historical baselines with banners — Decision 0019); the Qurʾānic registry is [`references/quran-loci.yaml`](references/quran-loci.yaml). A green offline validator establishes record shape and internal agreement, never source truth.
- **Internal casebook/longitudinal records are private and not independently auditable** — they motivate the design and validate nothing.
- **Draft PDFs are drafts** — byte-reproducible, DRAFT-stamped, commit-pinned; no numbered release, DOI, or archival claim exists.
- **License: OPEN DECISION** — none chosen; default copyright applies.
- **Citation metadata: OPEN DECISION** — no CITATION.cff; cite by commit per [docs/CITING.md](docs/CITING.md).

**Correction carried by R4 (SELF-1):** the R2 and R3 closeout prose reported the pilot-0 **v1** freeze hash as `ece0412f…`. The committed `terminology/pilot0/FREEZE-HASH.txt` has recorded `988a6522498df73ad1c7b0f73961a054ff20862d50fff6d644d0274877412772` since it was created, and `freeze_pilot0.py --check` has always passed against it. The packet was never wrong; three R3 documents and two closeout messages mis-stated the value. The historical documents' bodies are preserved; the correction is recorded here, in the R4 correction ledger, and is now machine-checked by `validate_current_state.py`.

## Claim status by lane

Exact per-lane claim wording, generated-format and machine-checked against `authored.claim_status_wording` in [docs/current-state.yaml](docs/current-state.yaml):

<!-- state:claim-status-by-lane -->
- formal: internally coherent current specification under the declared definitions, schemas, positive and adversarial fixtures, source-status contract, and acknowledged open parameters
- manuscript: complete research draft, source-verified to the stated threshold; not peer reviewed; not empirically validated
- companion_school_neutral: complete conditional philosophical draft; no claim of universal proof
- companion_athari: complete, source-verified-to-threshold, explicitly Athari/Taymiyyan school-internal draft; comparative positions accurately sourced; not a neutral theological conclusion
- terminology: matched instrument-ready v2, not run; no term adopted
- empirical: not run / open
- pdfs: reproducibly built and visually inspected draft artifacts
- legal_publication: open on license, identity, peer review, and external submission
<!-- /state:claim-status-by-lane -->

Reconciliation state: **D1/M1/O2** (owner decisions, R1) and decisions **0004–0015** remain intact and are not reopened. Remaining owner-only burdens: [OPEN-DECISIONS.md](OPEN-DECISIONS.md).
