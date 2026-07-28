# Current DAEE runtime correspondence — boundaries (R7D, Phase G)

**Label:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE.

This note fixes the boundaries under which the current `daee-epistemics` runtime objects
(`CURRENT-RUNTIME-CROSSWALK.yaml`) are read against Orthemology. All adjudication is
**read-only**; no DAEE file is modified and no DAEE object becomes a school-neutral
Orthemology core primitive.

## Dual-pin

The live published `daee-epistemics` `main` is `c86b3c66` (2026-06-18) — **the same
commit as the R7B/R7C pin.** The Diagnostic IR, field-witness, Mid-Reread Pressure,
owner-activation, route-pressure, Δ, Ψ-N and Ψ-I content the audit describes as "current
developments" exists **at that pinned commit** (verified read-only this pass). There is
**no published post-pin delta** to adopt; the "112 commits ahead" in the R7C
`DAEE-DELTA.md` was a local scratch checkout, not `origin/main`. What R7C actually left
undone was a *fuller crosswalk of the pinned content* — supplied here.

## Critical boundaries (audit G4)

- **The Diagnostic IR is not ground truth.** It is an episode-internal control
  representation / inferred operational state.
- **A field witness is an auditable projection/trace, not the full world.**
- **Owner activation is a plan, not execution, and not automatically a metaorthemma.**
- **Route pressure (∇) is an eligibility/ranking read over admissible routes, not a
  differential gradient.**
- **Δ is an event-local runtime/control-state transition, not result correctness.**
- **Runtime closure (Ψ-N) is not human restoration; Ψ-I is uncertainty-bearing
  inference with no soul access.**
- **Hard registers / live lenses are application-specific derived registers, not
  school-neutral core primitives.**
- **Shared owner/model lineage prevents any independent-validation claim.**
  Co-development with DAEE is a stress-test and an application, never evidence for the
  Orthemology theory.

## What is adopted

Nothing from DAEE is merged or imported as a core primitive. The crosswalk is a typed,
read-only, application-layer correspondence with per-object non-claims. Promotion of any
of this to `adopted-merged` is a fresh-Fable-review + protected-merge act.
