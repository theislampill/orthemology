# Decision 0012 — Reference-model semantic contract

**Date:** 2026-07-20 · **Authority:** R4 owner authorization · **Status:** adopted in a **candidate revision requiring independent review** · **Reopens nothing.**

## Problem

The R3 schemas compiled and every positive example validated, but they did not encode the settled theory. An independent probe submitted eleven malformed but theory-relevant records; **ten were accepted by both the schema layer and the cross-record validator** — an analysis with an empty task and none of D1's declared components; a metaortheme with empty identifiers, duplicate states, and no policy relation; a metaorthemma with empty anchors and binder data and no validity semantics; residuals dispositioned `owner-assigned`, `deferred`, `transferred`, or `risk-accepted` with no owner, trigger, receiver, or risk record; a handoff carrying no payload; a skeletal record passing as "audit-ready"; a `not-applicable` status with no reason when outside `required_path`; and arbitrary strings standing in for reliability and perturbation specifications.

## Decision

### 1. Constitutive fields are nonempty or explicitly dispositioned

`minLength: 1` on every constitutive string/ID/version field; `additionalProperties: false` outside documented typed extension maps; `uniqueItems: true` on array-as-set fields. Where a component genuinely does not apply, the record carries an explicit typed disposition (`not_applicable` / `unspecified_with_reason` with a reason) — **never an empty string**.

### 2. The analysis schema encodes the D1 declaration contract

An analysis declares domain/system boundary, task, evidence and action repertoires, loss, hard constraints, horizon, tolerance, representation family, permitted merger/abstraction family, and governance boundary — each with a value or an explicit disposition. A compact form is admissible only when the omitted components are inherited from a **resolvable** parent analysis reference.

### 3. Metaortheme / metaorthemma

Metaorthemes require nonempty ID and version, a unique declared state family, a typed selector, provenance/currentness, an explicit meta-policy relation, and declared exclusivity semantics (exclusive / overlapping / uncertain). Metaorthemmata require a nonempty **material** binding map, occurrence and analysis anchors, binder plus binding warrant, binding time, validity/expiry/supersession semantics, claim scope or a typed no-claim-dependency reason, and **exactly one `of_type`** — the R4 single-typing rule; many-to-many `MetaInst` is marked an **unimplemented future extension**.

### 4. Claim ledger, handoffs, episodes, verdicts

Residual dispositions carry conditional required fields (`unresolved` → responsible queue + next-review condition; `deferred` → trigger or review date; `transferred` → receiver + transfer record; `owner-assigned` → owner + acceptance state; `risk-accepted` → risk owner, rationale, scope, review trigger; `validated-resolved` → evidence/verdict references). Handoffs must carry at least one substantive payload, with analysis and occurrence versions on state claims. Episodes declare a `record_mode`; an **audit-ready** episode cannot be skeletal. Verdict records require a status for every required verdict, a reason for **every** `not-applicable` anywhere, the declared index block (analysis, version, actor, decision time, information state — the objectivity repair of Decision 0011), and a `claim_reasoning_paths` block keeping claim-level reasoning paths structurally distinct from the episode-level `pathway_state`.

### 5. Typed reliability and perturbation specifications

`schemas/reliability-spec.schema.json` (procedure ID/version, reference class, risk stratum, metric, threshold, evaluation protocol, evidence basis, **declaration time** proving pre-outcome declaration, validity) and `schemas/perturbation-spec.schema.json` (neighborhood family, finite enumeration or declared measure, invariants, varied fields, metaorthemma rebinding rule, failure criterion, version, validity) replace free-form string maps.

### 6. Cross-record semantics carry what JSON Schema cannot

ID uniqueness; reference resolution; analysis/version compatibility; occurrence anchoring; scope-vs-dependent-claims; binder/executor separation; the zero-burden rule; the single-type rule; claim dependency cycles; handoff transport and versioning; residual conditional completeness; the Definition-13 closure floor; required-verdict completeness; **claim-level and episode-level pathway recomputation**; RelSpec pre-outcome declaration; PerturbSpec invariant/varied-field disjointness.

## Result

Re-running the same eleven-class probe against the hardened layer: **0 of 11 accepted** — every class is rejected at a declared layer (previously 10 of 11 accepted by both).

## Honest scope limit

This decision covers the **contract**. The recursive/path-aware mutation engine and the `tests/invalid/` corpus specified by the R4 program are **not complete in this candidate pass** — see `../project-closure/r4/R4-SCHEMA-AND-MUTATION-REPORT.md`, which states exactly what exists and what does not. The pre-existing top-level mutation suite (three operators) still runs; its narrow coverage is reported as narrow and is **not** described as semantic completeness.
