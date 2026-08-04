# STATUS

**Draft / research-stage (revision R6, 2026-07-20).** This repository is a versioned working state, published honestly with its open decisions on record. The authoritative machine-readable statement of the current revision, counts, statuses, review state, and burdens is [docs/current-state.yaml](docs/current-state.yaml); this file, VERSION, README, the primary document headers, and OPEN-DECISIONS are checked against it in CI.

> **Current review state (R6, 2026-07-20): fresh-session repository review completed; not external human peer review; not empirically validated.** The R4 revision was produced as a mixed-provenance candidate under a mid-run model-provenance dispute (recorded, unadjudicated, in [docs/project-closure/r4/AUTONOMOUS-R4-STATE.json](docs/project-closure/r4/AUTONOMOUS-R4-STATE.json) and [docs/project-closure/r4/MODEL-SUBSTITUTION-INTERRUPTION-PR3.md](docs/project-closure/r4/MODEL-SUBSTITUTION-INTERRUPTION-PR3.md)). A fresh-session review then reproduced the substitution boundary, re-reviewed the pre- and post-substitution ranges hunk by hunk, selectively recovered the quarantined work, repaired its findings, and merged PR #3 through protected CI — sign-off: [docs/project-closure/r4-fresh-fable-review/FABLE-REVIEW-SIGNOFF.md](docs/project-closure/r4-fresh-fable-review/FABLE-REVIEW-SIGNOFF.md). The later R7E Sol reviewed lineage reached protected `main` through the verified cascade recorded in [docs/project-closure/r7e-sol/R7E-SOL-MERGED-MAIN-VERIFICATION.md](docs/project-closure/r7e-sol/R7E-SOL-MERGED-MAIN-VERIFICATION.md). These reviews concern repository formal, schema, source-record, and build integrity. Git integration is **not** theory or terminology adoption, **not** external human peer review, **not** empirical validation, and **not** legal/publication closure; those remain open exactly as listed below. Historical candidate reports remain intact and are classified in [docs/project-closure/HISTORICAL-STATUS-INDEX.yaml](docs/project-closure/HISTORICAL-STATUS-INDEX.yaml).

- **Not peer reviewed.**
- **No completed empirical validation** — no designed public experiment packet has been run. The V11 reconciliation separately records one historical internal eight-seed synthetic T299/T300 pilot with a negative result at its tested evidential class; it supplies no external framework-validation, theorem, or meniscus credit. Deterministic validators remain internally conformance-checked over declared schemas, examples, fixtures, and adversarial operators (never a mathematical consistency proof). This is not a completed paper program in the empirical sense.
- **Terminology not adopted** — orthemma, ortheme, metaortheme, metaorthemma, and orthing are candidate coinages; the pilot-0 v2 packet is **READY_FOR_HUMAN_MATCHING_REVIEW (Decision 0018); NOT RUN; NO TERM ADOPTED**. `orthable` is excluded from the operational core.
- **Companion papers are complete DRAFTS, not settled results** — the school-neutral paper's conclusions are conditional on labeled premises with named unresolved exits; the Atharī paper is explicitly school-internal and never presented as neutral.
- **Sourcing: the machine registry is authoritative for its declared claim families** — [`references/source-status.yaml`](references/source-status.yaml) carries per-claim statuses for the families it declares (`CIR-*`, `ELT-*`, `ATH-*`, `LAT-*`, `EXT-*`, `ETY-*`, `AM-*`); paper prose must agree with it bidirectionally, and blanket source-status statements are no longer used. Broader current sourcing state starts at the consolidated view [`docs/sourcing/CURRENT-SOURCING-LEDGER.md`](docs/sourcing/CURRENT-SOURCING-LEDGER.md) (R3 overlays are current where they regrade; the R2 ledgers are historical baselines with banners — Decision 0019); the Qurʾānic registry is [`references/quran-loci.yaml`](references/quran-loci.yaml). A green offline validator establishes record shape and internal agreement, never source truth.
- **Internal casebook/longitudinal records are private and not independently auditable** — they motivate the design and validate nothing.
- **Draft PDFs are drafts** — byte-reproducible, DRAFT-stamped, commit-pinned; no numbered release, DOI, or archival claim exists.
- **License: OPEN DECISION** — none chosen; default copyright applies.
- **Citation metadata: OPEN DECISION** — no CITATION.cff; cite by commit per [docs/CITING.md](docs/CITING.md).

**Correction carried by R4 (SELF-1):** the R2 and R3 closeout prose reported the pilot-0 **v1** freeze hash as `ece0412f…`. The committed `terminology/pilot0/FREEZE-HASH.txt` has recorded `988a6522498df73ad1c7b0f73961a054ff20862d50fff6d644d0274877412772` since it was created, and `freeze_pilot0.py --check` has always passed against it. The packet was never wrong; three R3 documents and two closeout messages mis-stated the value. The historical documents' bodies are preserved; the correction is recorded here, in the R4 correction ledger, and is now machine-checked by `validate_current_state.py`.

## Claim status by lane

Exact per-lane claim wording, generated-format and machine-checked against `authored.claim_status_wording` in [docs/current-state.yaml](docs/current-state.yaml):

<!-- state:claim-status-by-lane -->
- formal: internally conformance-checked current specification over the declared definitions, schemas, positive and adversarial fixtures, and source-status contract; acknowledged open parameters; no proof of consistency, completeness, or utility
- manuscript: complete research draft, source-verified to the stated threshold; not peer reviewed; not empirically validated
- companion_school_neutral: complete conditional philosophical draft; no claim of universal proof
- companion_athari: complete, source-verified-to-threshold, explicitly Athari/Taymiyyan school-internal draft; comparative positions accurately sourced; not a neutral theological conclusion
- terminology: v2 instrument READY_FOR_HUMAN_MATCHING_REVIEW (Decision 0018), not run; no term adopted
- empirical: designed public experiment packets not run / open; one separately classified historical internal synthetic AR8R pilot is negative at its tested evidential class and supplies no external framework-validation credit
- pdfs: reproducibly built and visually inspected draft artifacts
- legal_publication: open on license, identity, peer review, and external submission
<!-- /state:claim-status-by-lane -->

Reconciliation state: **D1/M1/O2** (owner decisions, R1) and decisions **0004–0015** remain intact and are not reopened. Remaining owner-only burdens: [OPEN-DECISIONS.md](OPEN-DECISIONS.md).

AR8R V11 Task 7 reconciliation status: expanded public owners and exact-source custody are implemented on the isolated branch and remain subject to final validation and independent whole-diff review. Candidate E/G remain `DEFERRED_INSUFFICIENT_AUDIT`; all ten PMR results remain owner-pending proposals; T354 remains formally blocked; the Ten Advances count remains `CONFLICTING_38_42`; and the Connes-rigidity dispute remains `UNRESOLVED_PENDING_OPERATOR_ALGEBRA_SPECIALIST_REVIEW`. No Lean build/kernel authority, integrated champion, meniscus, or natural closure is claimed.
