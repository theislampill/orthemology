# Decision 0030 — Evidence-bound multi-target noetic claims

**Date:** 2026-07-21 · **Authority:** R7D owner authorization (Opus candidate pass) · **Status:** proposed-candidate · **Reopens nothing:** Decisions 0001–0029 stand (amends the Decision 0027 target map).

**Provenance:** OPUS CANDIDATE — REQUIRES FRESH FABLE REVIEW BEFORE MERGE.

## Problem

The R7C audit (B10/B11, probes P2/P3) showed the multi-target model had the right
bearers but under-enforced support. `NOETIC-TARGET-MAP.schema.json` and the
`claim_valid` helper accepted an **asserted `m_subject` claim** with `in_scope:false`,
an empty evidence list, no observation bridge, unresolved evidence IDs, and no
analysis identity — and the helper returned *valid* for `evidence_scope: "no evidence
at all"` whenever a `non_claims: ["no soul access"]` disclaimer was present. A
disclaimer prevents an overclaim; it is not support. "Subject interior" was also a
single coarse target type (B11), collapsing overt avowal, a concrete reasoning
episode, an inferred profile, a disposition hypothesis, and an unobserved motive.

## Decision

**1. Typed claim record.** `NOETIC-CLAIM.schema.json` defines a `NoeticClaim`:
`claim_id`, `target_bearer` (six occurrences incl. `m_reasoning_episode`),
`target_id`/`target_version`, `target_type` (overt-discourse, avowed-commitment,
reasoning-episode, represented-standard, inferred-noetic-profile, faculty-disposition,
motive-culpability-soul-state, runtime-closure, route-quality, uptake), analysis
identity/version, proposition, `candidate_alternatives`, `evidence_ids`, observation
`bridges` (each `establishes_truth: false`), `support_rule`, `uncertainty`
(level+basis), `status`, `defeaters`, and `non_claims`.

**2. Evidence registry.** `NOETIC-EVIDENCE-REGISTRY.schema.json` types every evidence
record: observed occurrence, property class (structural/behavioral/provenance),
provenance, scope, currentness, validity, relation-to-target. **Every `evidence_id`
in a claim must resolve here; a non-claim is never an evidence record.**

**3. Support gate.** `scripts/validate_noetic_claims.py` (CI) enforces: target must
exist (bearer+identity+version resolve) and be in scope before it may be asserted; a
subject-interior TYPE never attaches to `m_discourse`; motive/culpability/soul-state
is normally held or out of scope, never asserted; an asserted **inferred** interior
claim needs ≥2 resolvable evidence IDs and an observation bridge (thin evidence
defaults to `held`/`underdetermined`); an overt **avowed-commitment** may be asserted
on its own public wording; any subject claim citing evidence must carry a bridge; and
held/underdetermined inferred profiles keep live candidate alternatives. Fixtures
`NC1..NC10` cover the required rejections and positive controls.

**4. Operation signature.** The DAEE operation runs: input occurrence → claim target
→ governing type → represented standard → metaorthemma → executor → operation target →
action → runtime transition → response successor → possible later uptake. A
metaortheme governs an episode; it never directly manipulates an unobserved soul-state.

## Non-claims

Adds evidence discipline over the existing bearers; reopens no settled Decision,
adopts no terminology, runs no experiment, and asserts no soul access, motive, or
culpability. Interior subject-level claims remain inferential, scoped, held under
uncertainty, and defeasible.
