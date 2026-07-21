# Decision 0020 — Experiment inferential readiness and packet versioning

> **OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE.** R7 candidate decision on the unmerged PR #8 chain (Decision 0026 reclassified this proposed-candidate; `main` R6 has only 0001–0019).

**Date:** 2026-07-20 · **Authority:** R7 owner authorization (noetic-application/experiment-validity tie-off) · **Status:** proposed-candidate · **Reopens nothing:** Decisions 0001–0019 stand; Decision 0018's vocabularies are unchanged — this decision corrects their *application*.

## Problem

R6 classified `FCSP-1` and `ER-1` as `READY_TO_RUN`. The independent R6 audit reproduced, and this pass confirmed (live probes included), that neither packet was executionally or inferentially ready: no run harness or parser existed; most declared endpoints were not computed; FCSP's AURC ignored its own declared aggregation hierarchy and its scenario templates stated target defects in near-diagnostic language; ER's E1 completion scoring was wrong (refusing legitimate closure scored as prevention), E5/traceability were presence flags, and its treatment fixtures leaked ground-truth labels (`binding_defect: true`, interpretation-bearing `reliability_note`, diagnostic case titles); neither packet had a defensible inferential unit. The R6 readiness validator checked *shape*, not scientific readiness — so its green run coexisted with an unready instrument (the project's own false-closure class, again).

## Decision

1. **Immediate downgrade.** `FCSP-1` and `ER-1` are reclassified as **historical R6 instrument versions** with corrected status `DETERMINISTICALLY_VALIDATED` (the highest state their evidence ever justified — deterministic shape/smoke validation only). They are not, and never were, ready to run.
2. **Version-preserving archival.** The R6 packet directories and `FREEZE-HASH.txt` files are preserved **byte-for-byte** (their in-packet `STATUS.yaml` files record what R6 claimed, as history). The canonical corrected classification lives in `experiments/experiment-status.yaml` (`historical: true`, `superseded_by`, and a dated correction note per packet); `validate_experiment_readiness.py` exempts historical packets from the index↔packet-STATUS agreement check and instead requires the correction note. Nothing is silently overwritten.
3. **Current packet identities.** Corrected current packets are built as **`FCSP-2`** (`experiments/false-closure-selective-prediction-v2/`) and **`ER-2`** (`experiments/episode-reification-v2/`). Manuscript and state surfaces point only at current versions.
4. **Readiness ceiling until the methods gate.** No current packet may hold `READY_TO_RUN` unless the full Decision 0022 methods/readiness gate passes (executable harness; public/scoring isolation; strict parser with retry; every declared endpoint and decision rule implemented; coherent units; aligned simulation; leakage and information-match audits; synthetic end-to-end run; adversarial methods pass with no blocker). Failing any gate, the highest honest lower status is used.
5. **Burden hygiene.** Unfinished packet engineering is never an owner burden; `OPEN-DECISIONS.md` names only execution/review/registration acts.

## Consequences

Amended: `experiments/experiment-status.yaml`, `experiments/README.md`, `validate_experiment_readiness.py`, `OPEN-DECISIONS.md`, manuscript §13, current state, changelog. Additive dated correction notices on the R6 closeout surfaces that asserted `READY_TO_RUN`. New packets under Decision 0022's gate.
