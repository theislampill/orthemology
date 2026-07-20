# Decision 0018 — Experiment-packet readiness and registration status

**Date:** 2026-07-20 · **Authority:** R6 owner authorization (experiment-readiness/sourcing-state tie-off) · **Status:** adopted · **Reopens nothing:** Decisions 0001–0017 stand; this is research-governance engineering, not a theory claim.

## Problem

`OPEN-DECISIONS.md` said "Every packet is INSTRUMENT-READY, NOT RUN" while the public `experiments/` tree contained only a README: the false-closure/selective-prediction benchmark (manuscript §13.1) and the episode-reification incremental-value test (§13.2) existed only as prose designs. Unfinished, non-owner design work had been transferred into an owner-only "execution" burden — false closure under the project's own standard (independent audit, finding B1). The manuscript also called the unbuilt, unregistered design "preregistered" (B2), and the terminology lane's "INSTRUMENT-READY PENDING BLIND HUMAN MATCHING REVIEW" conflated readiness states (M1).

## Decision

1. **Closed readiness vocabulary** (one machine-readable status per packet):

   `DRAFT → SPEC_COMPLETE → DETERMINISTICALLY_VALIDATED → READY_FOR_HUMAN_MATCHING_REVIEW → READY_TO_RUN → RUN_IN_PROGRESS → RUN_COMPLETE_UNADJUDICATED → ADJUDICATED`

   `READY_FOR_HUMAN_MATCHING_REVIEW` applies only to packets that declare a required pre-run human review gate (currently the terminology instrument); a packet with no such declared gate may go from `DETERMINISTICALLY_VALIDATED` to `READY_TO_RUN`. A packet may not be `READY_TO_RUN` while any declared required review is pending.

2. **Separate registration vocabulary**:

   `NOT_REGISTERED · PREREGISTRATION_READY · LOCALLY_PROTOCOL_FROZEN · EXTERNALLY_PREREGISTERED`

   **A Git freeze is not an external preregistration.** No document may say "preregistered" unless it names a real external registry record (identifier/URL). External registry submission is an owner/external act.

3. **Canonical per-packet state** lives in `experiments/experiment-status.yaml`: packet ID, path, purpose, readiness state, registration state, freeze hash, required remaining gates, whether any run exists, and what result/adoption (if anything) is licensed. Outward summaries (the experiments README) defer to it.

4. **Freeze discipline**: each packet carries `FREEZE-HASH.txt` (sha256 over sorted `relpath NUL content NUL` records of every packet file except the hash file itself — the pilot-0 recipe); any post-freeze edit is a new packet version; inferentially material revisions preserve the prior packet version as history.

5. **No-run guard**: deterministic smoke/mock outputs are labeled synthetic and confined to packet `tests/` trees; nothing in the repository may present a synthetic traversal as an empirical run. `scripts/validate_experiment_readiness.py` enforces 1–5 in CI with tamper tests in both directions.

## Consequences

New: `experiments/experiment-status.yaml`; `experiments/false-closure-selective-prediction/` (packet `FCSP-1`); `experiments/episode-reification/` (packet `ER-1`); `scripts/validate_experiment_readiness.py` + CI step. Amended: `OPEN-DECISIONS.md` burden 3 (execution/spend/ethics only — packet preparation was never owner-only); manuscript §13 (actual paths and exact statuses; "preregistered" removed wherever no registry record exists); terminology status wording (Decision 0018 vocabulary; Phase E reconciliation in `terminology/`).
