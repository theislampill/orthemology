# STATUS

**Draft / research-stage (revision R4, 2026-07-20).** This repository is a versioned working state, published honestly with its open decisions on record. The authoritative machine-readable statement of the current revision, counts, statuses, and burdens is [docs/current-state.yaml](docs/current-state.yaml); this file, VERSION, README, and OPEN-DECISIONS are checked against it in CI.

> **R4 corrective revision — CANDIDATE PASS, REQUIRES INDEPENDENT REVIEW (2026-07-20).** An independent audit accepted R3 as a strong baseline but withheld final sign-off. The R4 pass repairs, under a mid-run model-provenance dispute recorded in [docs/project-closure/r4/AUTONOMOUS-R4-STATE.json](docs/project-closure/r4/AUTONOMOUS-R4-STATE.json): the `p̂`/`Ĉ` type contradiction; claim-relative reasoning paths and strict soundness (Decision [0011](docs/decisions/0011-claim-relative-reasoning-path-and-strict-soundness.md)); full-index objectivity language; the evaluator-symmetry/non-circularity overclaim; metaorthemma existence and single-typing rules; the reference-model semantic contract with recursive mutation testing (Decision [0012](docs/decisions/0012-reference-model-semantic-contract.md)); one machine-readable source-status registry with the corrected concrete/ideal-reason attribution chain (Decision [0013](docs/decisions/0013-source-attribution-and-status-normalization.md)); this generated project-state contract (Decision [0014](docs/decisions/0014-generated-project-state-and-whole-state-reread.md)); and a bounded latent-state related-work boundary (Decision [0015](docs/decisions/0015-latent-state-observation-and-representation-boundary.md)). **This revision is not independently signed off and is not final closure.**

- **Not peer reviewed.**
- **No completed empirical validation** — no designed study has been run; nothing here reports an experimental result; deterministic validators check consistency only. This is not a completed paper program in the empirical sense.
- **Terminology not adopted** — orthemma, ortheme, metaortheme, metaorthemma, and orthing are candidate coinages; the pilot-0 v2 packet is **INSTRUMENT-READY PENDING BLIND HUMAN MATCHING REVIEW; NOT RUN; NO TERM ADOPTED**. `orthable` is excluded from the operational core.
- **Companion papers are complete DRAFTS, not settled results** — the school-neutral paper's conclusions are conditional on labeled premises with named unresolved exits; the Atharī paper is explicitly school-internal and never presented as neutral.
- **Sourcing is governed by one registry** — [`references/source-status.yaml`](references/source-status.yaml) carries a per-claim status (`PRIMARY_TEXT_EXACT`, `PRIMARY_WORK_THEME`, `PRIMARY_LOCUS_EDITION_DEPENDENT`, `SECONDARY_VERIFIED`, `SECONDARY_RECONSTRUCTION`, `COMPILATION_MEDIATED`, `INFERENCE_CROSS_SOURCE`, `ORTHEMOLOGICAL_EXTENSION`, `UNVERIFIED_REMOVE_OR_DOWNSCOPE`); paper prose must match it, and blanket source-status statements are no longer used.
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
