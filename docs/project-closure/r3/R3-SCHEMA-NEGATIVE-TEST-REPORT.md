# R3 schema negative-test report

**Date:** 2026-07-20 · **Baseline:** the R3 read-only audit's adversarial pass found the R2 schemas ACCEPTED **7/7** malformed record classes (`R2-INDEPENDENT-READONLY-AUDIT.md` §1.4).

## Hardening applied

- `additionalProperties: false` on every object node declaring `properties` in all 8 schemas — except the declared map-style extension points (`binding`, `statuses`, `na_reasons`, `rel_spec`, `perturb_spec`, `evidence_status`), which keep their typed value constraints.
- Constitutive metaorthemma requirements: `governed_component` and `scope` now required; `binding` requires `minProperties: 1` (M1: a token exists only where material binding exists); `instrument`, when present, requires `id` + `calibration_provenance`; declared optional `designated_executor` / `policy_ref` / `evidence_selector_ref` fields added (binder role stays independently recorded).
- Episode auditability: `observation`, `evidence` (may be empty, must be declared), `warrant` (nullable, declared), `policy`, and `verdict_record_ref` (nullable, declared) now required — a skeletal six-field episode no longer validates.
- Verdict record: `required_path` gains `uniqueItems`; claim-wise **factivity is now schema-encoded** (`token_truth_linked = pass` forces `result_correct = pass` via `if/then`); the verdict-id enum is **generated from the registry** (`scripts/generate_from_registry.py`, drift-checked in CI along with the generated prose alias table `docs/generated/verdict-aliases.md`).
- `minLength: 1` on identity-bearing strings.

The 7 positive examples were upgraded to the new constitutive requirements (auditability fields added; no semantics changed) and all still validate.

## Negative fixtures (`tests/schema-negative/`) — 10 fixtures, layered

| ID | Defect | Rejection layer | Result |
|---|---|---|---|
| N1 | empty binding, no governed component/scope | schema | REJECTED |
| N2 | skeletal six-field episode | schema | REJECTED |
| N3 | required verdict fail + `pathway_state: adequate` | semantic (recompute) | schema-valid by design → FLAGGED |
| N4 | truth-linked pass on failed claim | schema (if/then) | REJECTED |
| N5 | meta-token anchored to different occurrence/analysis | semantic (cross-record) | schema-valid by design → FLAGGED |
| N6 | duplicate evidence ids | semantic (uniqueness) | schema-valid by design → FLAGGED |
| N7 | undeclared extra fields | schema | REJECTED |
| N8 | required not-applicable without reason | semantic | FLAGGED |
| N9 | per-token V3c referencing a ghost token | semantic | FLAGGED |
| N10 | non-registry verdict id in statuses | schema (propertyNames enum) | REJECTED |

## Cross-record semantic validator (`scripts/validate_cross_record_semantics.py`)

Checks over every example bundle (and every semantic negative fixture): episode↔token analysis and anchor equality; unique evidence/token ids; binder role independently populated; pathway-state exact recomputation; NA-reason coverage on the required path; `GOV_TOKEN_ADEQUATE` required **iff** tokens exist (zero-burden rule) and `ROUTE_ADMISSIBLE` required when a route is selected (declared ≠ derived fails); per-token V3c references resolve; V3c aggregate recomputes from per-token statuses; handoff state claims carry `valid_for_version`. All 7 examples: **0 failures**.

## Deterministic mutation testing (`tests/schema-mutations/` + `validate_negative_fixtures.py`)

Operators (exhaustive, no randomness): drop each top-level required field; corrupt each top-level enum; add an undeclared field — over every positive example part. **Result: 204 mutants generated, 0 survivors.**

## Honest residuals

- Conditional structure (route/closure/residual/trace requirements derived from governance) is enforced at the **semantic** layer via the shipped governance table, not in pure JSON Schema — recorded as the intended division of labor, not a gap.
- `of_type` remains single-typed; plural `MetaInst` is the declared extension point (R3-FORMAL-AUDIT Q8).
- Property-based/metamorphic *generation* beyond the enumerated operators was not added, keeping CI deterministic; the enumerated corpus (10 negative + 204 mutants + omission-attack RP-5) is the shipped floor, not a ceiling.
