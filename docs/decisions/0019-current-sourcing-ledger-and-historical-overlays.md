# Decision 0019 — Current sourcing state, historical ledgers, and overlays

**Date:** 2026-07-20 · **Authority:** R6 owner authorization · **Status:** adopted · **Reopens nothing:** Decisions 0001–0018 stand; no source status is re-adjudicated here — this decision fixes *navigation and classification* only.

## Problem

Current navigation (STATUS, README, papers) pointed readers at `docs/sourcing/SOURCING-LEDGER.md` and `companion/sourcing/COMPANION-SOURCING-LEDGER.md` as the broader sourcing surface — but those are R2-era ledgers whose statuses (`WEB-VERIFIED` / `RECORD-CONFIRMED` / `VIA-COMPILATION` vocabulary) were superseded row-by-row by the R3 regrading overlays (`R3-SOURCING-LEDGER.md`, `R3-COMPANION-SOURCING-LEDGER.md`) and, for the declared claim families, by `references/source-status.yaml`. The R3 overlays say so; the R2 bodies carried no prominent banner; a reader landing on the R2 ledgers reasonably took stale statuses as current (independent audit, finding B4).

## Decision

1. **Canonical machine-readable classification:** `docs/sourcing/SOURCING-STATUS-INDEX.yaml` classifies every sourcing surface as `current-authoritative`, `current-view`, `overlay`, or `historical-baseline`, and names, for each claim area, where the current status actually lives.
2. **One current consolidated view:** `docs/sourcing/CURRENT-SOURCING-LEDGER.md` — a navigational materialization that does **not** duplicate contradictory status values: per claim area it points at the authoritative rows (source-status registry families; R3 overlay rows; the Qurʾānic registry) and lists the standing research triggers. Inference-boundary labels are retained by reference.
3. **Additive historical banners** on both R2 ledgers (bodies preserved verbatim; the R4-era additive rows 36–38 of the main ledger are noted as later additions superseded for their families by the registry's LAT rows).
4. **Navigation:** STATUS, README, and paper surfaces point current readers at the consolidated view / index, never at an R2 ledger as current.
5. **Validation:** `scripts/validate_sourcing_state.py` (CI) fails: a historical ledger without its banner; a current navigation surface naming an R2 ledger as the current destination; an index misclassification; a consolidated-view row contradicting the registry; R2-only status vocabulary presented inside the current view. It validates classification and agreement — never source truth.

## Consequences

New: the index, the consolidated view, the validator, the CI step, the banners. `references/source-status.yaml` remains authoritative exactly for its declared families; `references/quran-loci.yaml` remains the separate Qurʾānic locus registry; nothing about any individual source's status changes in this decision.
