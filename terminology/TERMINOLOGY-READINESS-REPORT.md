# Terminology program — readiness report (R2, 2026-07-20)

**Overall status: READY TO RUN, NOT RUN.** No utility experiment of any kind has been executed; no human data collected; no model-scored result is treated as evidence of term utility; no term is adopted, and none is retired. Only deterministic packet validation and synthetic parser/rubric smoke tests have run (they validate the *instruments*, not the *terms*).

## Inventory

| Artifact | Status |
|---|---|
| Frozen design v0 (`orthemic-terminology-evaluation-spec.md`) | immutable history; hash `ff68084f…67b5` |
| Pilot protocol note (`orthemic-terminology-pilot-protocol.md`) | history; superseded operationally by pilot0/ |
| **Pilot 0 packet** (`pilot0/`) | complete: protocol (DESIGN-V1: adds Arm C′ + metaorthemma/binding family), 4 primers + matched filler, 9 items with per-arm renderings (`items/ITEMS.json`), deterministic rubrics + adjudication manual, sham-label criteria and mapping (orth→tarv), contamination/carryover plan, model-pinning + run-manifest schema, deviation ledger (empty), analysis skeleton (smoke-tested on synthetic data), packet freeze hash (`FREEZE-HASH.txt`) |
| **Pilot 1 template** (`pilot1/`) | complete: item-variant inventory (≥3/family plan incl. binding family), held-out-domain plan, simulation-based power script (SYNTHETIC placeholders, clearly marked), rater-assignment plan, mixed-model analysis spec |
| **Confirmatory v1 template** (`confirmatory-v1-template/`) | complete: freeze checklist with unfillable-until-pilot slots, decision surface restated, metric-freeze rule (AURC/alternative chosen before freeze only) |

## Dispositions of record

- **C′ (sham labels):** mandatory in Pilot 0; mandatory in Pilot 1 if Pilot 0 shows the shams matched and interpretable (gates defined in the protocol); preregistered secondary control in confirmatory v1 if power permits; never a replacement for A/B/C. Its role: separate benefit of *these terms* vs *any labels* vs *the distinctions*.
- **Metaorthemma family:** added (correct standard + defective binding + faithful execution + lucky result), with the word tested against *configuration token / instantiated governing configuration / bound governing record* in Arm B.
- **`orthable`:** excluded from the operational confirmatory core; exploratory in the companion lane only; no philosophical-comprehension module is currently justified.
- **No fabricated estimates:** every power/variance number in the templates is a marked synthetic placeholder.

## What stands between "ready" and "run" (owner-only burdens)

Executing model runs at pinned versions (spend), recruiting ≥3 human raters (human participants), and the confirmatory freeze decision. None is a repository artifact; all are listed in `docs/project-closure/UNAVOIDABLE-OWNER-ACTIONS.md`.
