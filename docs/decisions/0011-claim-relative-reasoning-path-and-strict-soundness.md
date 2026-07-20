# Decision 0011 — Claim-relative reasoning paths, strict soundness, objectivity indexing, and circularity language

**Date:** 2026-07-20 · **Authority:** R4 owner authorization (consolidated prompt v2) · **Status:** adopted in a **candidate revision requiring independent review** *(historical wording; review discharged 2026-07-20 by the fresh-session review and protected merge — docs/project-closure/r4-fresh-fable-review/FABLE-REVIEW-SIGNOFF.md, Decision 0016)* · **Reopens nothing:** D1, M1, O2, D3 (0004), D4 (0005), O3 (0006), 0007–0010 all stand.

## Problem

Three R3 formulations were stronger or coarser than the machinery supports.

1. **Granularity.** `StrictlySoundReasoning_q(e) := PathwayAdequate(e) ∧ TOKEN_TRUTH_LINKED_q(e)` names a claim-level predicate but conjoins a whole-episode one. `PathwayAdequate(e)` aggregates all of `ReqPath(e)`, including `ROUTE_ADMISSIBLE` and `CLOSURE_TRUTHFUL`. A claim soundly reached would therefore become "not strictly sound" because the operator later routed the case poorly or made a false closure claim; and a mixed episode could not carry one sound and one unsound claim.
2. **Objectivity.** "Objective given `A`" understates the index: `EX_ANTE_JUSTIFIED` ∈ CorePath is indexed to actor, decision time, and information state.
3. **Circularity.** "Non-circularity comes from evaluator symmetry + corroboration" overstates what either provides.

## Decision

### 1. Claim-relevant reasoning requirement projection

> `ReqReason_q(e) ⊆ ReqPath(e)` — the required verdicts causally or evidentially relevant to claim `q`.

It is **derived, recorded, and auditable**, never chosen after the outcome to rescue a claim. Its derivation inputs are exactly: the claim's declared dependencies (`depends_on_claims`, `depends_on_tokens`); its evidence IDs and their scopes; the metaorthemmata governing those components; the analysis and governance rules that make a verdict required at all; and the procedure/execution portions bearing on the claim. Verdicts required of the episode but irrelevant to `q` (typically downstream route and closure obligations) are excluded from `ReqReason_q(e)` and remain in `ReqPath(e)`.

### 2. Two distinct predicates

- `ReasoningPathAdequate_q(e)` iff every verdict in `ReqReason_q(e)` passes — **non-factive** (O2 preserved).
- `PathwayAdequate(e)` — the **whole-episode** predicate, unchanged.
- **`StrictlySoundReasoning_q(e) := ReasoningPathAdequate_q(e) ∧ TOKEN_TRUTH_LINKED_q(e)`** — factive at the claim level, still a **derived profile over existing verdicts**. **No primitive `SOUND_REASON` verdict is added**; the registry (0004) is unchanged.

Verdict records carry the projection and its recomputed result in a `claim_reasoning_paths` block, kept structurally distinct from the episode-level `pathway_state`.

### 3. Objectivity is indexed, not unindexed

> Verdicts are objectively assessable relative to the complete declared index: analysis and version, governance regime, occurrence and version, actor, time, information state, and evidence available then. Actor-indexing does not make a verdict whatever the actor believes.

The verdict schema now requires the index block. "Objective given `A`" is withdrawn wherever it stood unqualified in current normative prose.

### 4. Circularity language

> Evaluator symmetry prevents privileged self-certification. Independence-aware corroboration provides defeasible corrective evidence. Neither by itself proves non-circularity, eliminates shared-source dependence, or terminates regress.

The Taymiyyan architecture (sound/corrupted fiṭrah, tawātur, mutual corroboration) is preserved as a sourced tradition-specific proposal, never as a theorem of orthemology. Fixture **CR-9** and `examples/shared-upstream-corroboration-failure.json` make dependent corroboration representable: several evaluators agree, all inherit one upstream source or institutional metaortheme, evaluator symmetry holds, and the shared distortion survives.

## Fixtures

`CR-9` (shared-upstream corroboration) plus the claim-relative family: claim sound with defective downstream route; claim sound with later false closure; mixed episode (one strictly sound, one unsound claim); correct-by-luck claim with unrelated pathway verdicts passing; rare false result through adequate claim-relevant reasoning; unresolved claim with adequate unrelated episode components. Checked by `scripts/validate_claim_reasoning_paths.py`.

## Consequences

Core, manuscript, both companions, `CONCRETE-AND-SOUND-REASON.md`, the verdict schema, cross-record semantics, and the R4 formal audit all carry the corrected forms. R3's documents retain their bodies and are superseded by dated notice.

---

## Amendment (2026-07-20, R4 independent review) — explicit supersession and delivered artifacts

1. **Explicit partial supersession of Decision 0009.** The header's "0007–0010 all stand" was imprecise: this decision **supersedes Decision 0009's strict-soundness formula** (`PathwayAdequate(e) ∧ TOKEN_TRUTH_LINKED_q(e)`) while every other clause of 0009 stands. A dated supersession notice now sits at the superseded formula in 0009, and the relationship is machine-checked (`docs/decision-status.yaml`, `scripts/validate_decision_dependencies.py`) so two current decisions can no longer define one normative symbol incompatibly without failing CI.
2. **The claimed artifacts now exist.** At candidate head `25d035a…` this decision cited fixture CR-9, `examples/shared-upstream-corroboration-failure.json`, `scripts/validate_claim_reasoning_paths.py`, and the six claim-relative cases, but none was in the tree — a false-closure defect (independent audit §4; correction ledger row C6 wrongly marked DONE). The independent review implemented them: fixtures CR-9…CR-15 plus the CR-OMIT-1 omission attack in `tests/claim-reasoning-fixtures.json`, the validator, and the machine-readable derivation table `docs/claim-reason-requirements.yaml` giving `ReqReason_q(e)` a governance derivation (`RequiredReasonBy` instance with per-verdict trace) rather than a merely supplied projection. `validate_reason_fixtures.py` no longer computes strict soundness from the superseded whole-episode formula.
