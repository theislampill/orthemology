# Decision 0033 — Governed corrective search and transition witness

**Date:** 2026-07-21 · **Authority:** R7D owner authorization (Opus candidate pass) · **Status:** proposed-candidate · **Reopens nothing:** Decisions 0001–0032 stand (amends Decision 0025's descent model).

**Provenance:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE.

## Problem

The R7C audit (B26–B30) found the corrective-dynamics model still labeled G1 `adopted`
inside an unmerged candidate, used "locally sound" too freely, and compressed distinct
runtime stages under "descent". The project's strict-soundness predicate is factive and
claim-relative (Decision 0011): a runtime transition is not strictly sound merely
because it obeyed hard constraints, improved a declared order, landed a burden, or
reached closure. Fast episode correction and slow standard/ecology adaptation were named
but not connected.

## Decision

**1. G1 is candidate.** `NOETIC-FIELD-DYNAMICS.yaml` reclassifies the route-ranked
descent model G1 from `adopted` to `proposed-candidate`; promotion is a fresh-Fable +
protected-merge act.

**2. Predicate vocabulary.** A runtime transition is an `AdmissibleCorrectiveTransition`
/ `PathwayAdequateCorrection` / `GovernedCorrectiveSearch`. **Strict soundness is
reserved for the factive claim-relative predicate (Decision 0011)** and is never
asserted of a merely admissible runtime transition.

**3. Transition witness.** `CORRECTIVE-TRANSITION.schema.json` records one transition
with all stages separate: state-before, live burdens, hard constraints, eligible routes
(feasibility filtered first), ranking witness, selected route, governing types,
represented standards, metaorthemmata, executor operation, evidence, delta, state-after,
field diagnostics, whole-state reread, terminal posture (STOP/HOLD/PARTIAL/RECURSE/
CLOSURE), verdicts, and non-claims. `scripts/validate_corrective_transition.py` (CI)
enforces: the selected route is admissible; a ranking witness exists (route pressure is
not a differential gradient); delta is not correctness and an admissible transition is
never `strictly_sound`; CLOSURE requires a performed reread; runtime closure is never
human restoration; no burden is deleted/concealed; and one episode never silently
revises the global standard (slow-timescale revision needs explicit authorization).
Fixtures `CT1..CT8` cover each rejection.

**4. Two timescales.** Fast episode correction and slow represented-standard/ecology/
metaortheme/analysis revision are coupled through the update-coupling governance
(Decision 0024 amendment / Phase I): a repeated failure may *propose* a slow-timescale
revision, but no single episode licenses global standard revision by itself.

## Non-claims

Corrective-search discipline only; reopens no settled Decision, adopts no terminology,
runs no experiment, asserts no soul-state. Admissibility, pathway adequacy, result
correctness, strict soundness, runtime closure, and human uptake stay distinct.
