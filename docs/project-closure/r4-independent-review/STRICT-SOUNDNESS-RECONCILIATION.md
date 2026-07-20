# Phase C — strict-soundness reconciliation (R4 independent review)

**Date:** 2026-07-20 · **Session:** independent Fable review of PR #3 (harness identity `claude-fable-5`).

## The defects (audit §3–§5, all reproduced)

1. **Two adopted, incompatible normative definitions.** Decision 0009 (adopted) defined `StrictlySoundReasoning_q(e) := PathwayAdequate(e) ∧ TOKEN_TRUTH_LINKED_q(e)`; Decision 0011 (adopted) defined it as `ReasoningPathAdequate_q(e) ∧ TOKEN_TRUTH_LINKED_q(e)` while declaring "0007–0010 all stand" — no supersession notice existed anywhere.
2. **False closure on Decision 0011's artifacts.** The decision, the companion, and correction-ledger row C6 (marked DONE) cited fixture CR-9, `examples/shared-upstream-corroboration-failure.json`, `scripts/validate_claim_reasoning_paths.py`, and six claim-relative cases. None existed; `tests/reason-fixtures.json` held only CR-1…CR-8, and `validate_reason_fixtures.py` still computed strict soundness from the superseded whole-episode formula.
3. **`ReqReason_q(e)` had no governance derivation.** The cross-record layer recomputed adequacy over whatever projection the record supplied, so omitting an inconvenient verdict manufactured claim-level adequacy.

## The repairs

### One normative definition, machine-guarded
- Dated **SUPERSESSION NOTICE** added at the superseded formula in Decision 0009 (body otherwise preserved); dated amendment in Decision 0011 stating the partial supersession explicitly.
- New `docs/decision-status.yaml` (status + supersession registry, incl. registered current/superseded formulas for `StrictlySoundReasoning_q`) and `scripts/validate_decision_dependencies.py` (CI): every decision file registered; superseded sites must retain their historical formula AND carry the notice; **no other decision and no current normative surface may restate a superseded formula**. Tamper-probed: stripping the notice → exit 1; restating the old formula in `docs/glossary.md` → exit 1.

### The claimed artifacts now exist and are exercised
- `tests/claim-reasoning-fixtures.json`: **CR-9** (two agreeing evaluators, symmetry recorded, one shared distorted upstream — all reasoning adequate, nothing strictly sound), **CR-10/CR-11** (claim sound while downstream route / later closure fails — both explicitly diverge from the superseded formula), **CR-12** (mixed episode: one sound, one unsound claim), **CR-13** (correct-by-luck), **CR-14** (rare miss through adequate claim-relevant reasoning), **CR-15** (unresolved claim), **CR-OMIT-1** (omission attack).
- `scripts/validate_claim_reasoning_paths.py` (CI): recomputes per claim — `ReqPath(e)` (via the existing governance derivation), **derived** `ReqReason_q(e)` with a per-verdict inclusion/exclusion trace, `ReqReason_q ⊆ ReqPath`, four-valued aggregation, `ReasoningPathAdequate_q`, truth-link factivity, strict soundness, and a mechanical **independence probe** (flipping unrelated route/closure statuses must not move any non-routing/non-closure claim). 81 checks; tamper probes (flipped expectations, honest-projection drift) all fail as required.
- `examples/shared-upstream-corroboration-failure.json`: full schema-valid bundle (2 episodes, 2 ledgers, 2 verdict records with `claim_reasoning_paths` and full index blocks) making dependent corroboration representable. It doubles as the **D4 regression**: the pre-repair cross-ledger scope loop (run from commit `1223110`'s tree) flags it with two reciprocal false positives; the repaired owner-scoped check accepts it.

### `ReqReason_q(e)` is now governance-derived
- `docs/claim-reason-requirements.yaml`: the machine-readable `RequiredReasonBy(A, governance, claim-type, evidence-kind, token-dependencies, risk-class)` instance — baseline reasoning verdicts always claim-relevant; `GOV_TOKEN_ADEQUATE` iff the claim declares token dependencies; `ROUTE_ADMISSIBLE`/`CLOSURE_TRUTHFUL` iff the claim itself is a routing/closure claim; `ROBUST_NEIGHBORHOOD` under a predeclared per-claim obligation. Honest-status header mirrors the ReqPath table: one complete deterministic instance, not a universal calculus.
- Omission attack CR-OMIT-1: recorded projection omitting the failing token verdict is detected; the derived projection decides (defective), and the validator also proves the recorded projection would have manufactured "adequate".
- `validate_reason_fixtures.py` migrated: CR-1…CR-8 keep their episode-level pathway checks, but strict soundness is computed claim-relatively from each fixture's now-explicit `claim_shape` via the same rule table. No expected value changed (no CR-1…8 fixture fails solely on route/closure verdicts — verified before migration).

### Cross-record token-identity groundwork pulled forward (D3/D4)
Global `token_id` uniqueness with coherent-redeclaration allowance; standalone tokens must name `owning_episode` (schema field added; both standalone-token examples updated) or declare `scope.external_scope`; token claim-scope checks now run only against the owning episode's ledgers.

## Non-reopening statement
D1, M1, O2, Decisions 0004–0008, 0010 untouched. The verdict registry is unchanged — no primitive `SOUND_REASON` verdict was added. Decision 0009's type/token doctrine, concrete-reason disambiguation, and higher-order-cognition clauses all stand.
