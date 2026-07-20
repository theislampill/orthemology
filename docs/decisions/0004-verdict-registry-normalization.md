# Decision 0004 — Verdict registry normalization (D3)

**Date:** 2026-07-20 · **Decider:** Claude Fable 5 under the owner's standing autonomy mandate (R2 closure) · **Status:** implemented, registry-driven, machine-validated.

**Question.** The verdict vector carried provisional lettering: the conceptual adequacy chain ran V3 → V3a → V3c → V3b → V3d while the labels stayed alphabetical-by-accident, and the `^proc`/`^tok` superscripts were explicitly provisional ("labels provisional pending the verdict-index decision"). What is the final, machine-stable registry?

**Decision.** Adopt canonical **semantic identifiers** (authoritative in schemas, tests, fixtures, and machine-readable records) with **display aliases** in conceptual order (used in prose and equations). The registry lives in [`docs/verdict-registry.yaml`](../verdict-registry.yaml), which drives `scripts/validate_verdict_semantics.py` and the schema validator, so reordering can never silently change semantics.

| Semantic ID | Alias | Meaning |
|---|---|---|
| `RESULT_CORRECT` | `V1` | result/profile correctness |
| `EVIDENCE_SUPPORT` | `V2a` | evidence meets the declared support standard |
| `PROCEDURE_RELIABLE` | `V2b-P` | configured-procedure/reference-class truth-conduciveness |
| `TOKEN_TRUTH_LINKED` | `V2b-T` | factive, claim-wise truth linkage |
| `EVIDENCE_CURRENT` | `V2c` | currentness and admissible provenance |
| `GOV_CONFIG_ADEQUATE` | `V3a` | governing configuration/type adequacy |
| `GOV_POLICY_ADEQUATE` | `V3b` | policy adequacy |
| `GOV_TOKEN_ADEQUATE` | `V3c` | metaorthemma/binding adequacy |
| `EXECUTION_FAITHFUL` | `V3d` | executor fidelity |
| `EX_ANTE_JUSTIFIED` | `V3e` | decision-time reasonableness |
| `ROUTE_ADMISSIBLE` | `V4a` | route safety/admissibility |
| `ROUTE_QUALITY` | `V4b` | near-optimality/advisory route quality |
| `CLOSURE_TRUTHFUL` | `V5` | closure matches the burden ledger |
| `ROBUST_NEIGHBORHOOD` | `V6` | robustness under declared perturbations |

The V3-block display order now **matches the conceptual chain**: configuration (V3a) → policy (V3b) → token binding (V3c) → execution (V3d) → decision-time justification (V3e). The result-free pathway core (Decision 0003) is unchanged in *content* and reads, under the new aliases: `CorePath = {V2a, V2b-P, V2c, V3a, V3b, V3c, V3d, V3e, V4a, V5, V6}`, excluding `V1`, `V2b-T`, and `V4b`. The sole declared entailment is claim-wise `V2b-T_q → V1_q`.

**Legacy migration table** (historical aliases; documents under `archive/` are never rewritten and retain the old labels):

| Old label | New label |
|---|---|
| `V3` (configuration adequacy) | `V3a` |
| `V3a` (policy adequacy) | `V3b` |
| `V3b` (executor fidelity) | `V3d` |
| `V3c` (token adequacy) | `V3c` (unchanged) |
| `V3d` (ex-ante justification) | `V3e` |
| `V2b^proc` | `V2b-P` |
| `V2b^tok` | `V2b-T` |
| manuscript bare `V4` (route safety) | `V4a` |

**Consequences applied:** formal core, manuscript, multi-actor note, architecture overview, glossary, `tests/verdict-fixtures.json` (schema v2, keyed by semantic ID), `scripts/validate_verdict_semantics.py` (registry-driven), episode/verdict JSON schemas, README, and all current non-historical documentation. Supersession notes added to Decisions 0002/0003 readers via this record; the archived R1 patches and ledgers retain the old aliases as immutable history.

**Non-decision.** No semantic content of any verdict changed; this is a naming/indexing normalization only.
