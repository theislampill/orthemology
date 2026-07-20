# Counterexample ledger R2

**Date:** 2026-07-20 · **Method:** for each target pattern, attempt to construct a concrete case; determine whether the current formalism represents it; add or point to a deterministic fixture where useful; repair the theory where it could not represent the case. Verdicts: **REP** (representable, witness cited) / **REP+FIX** (representable after adding a fixture) / **REP+REPAIR** (required a theory repair in this revision). No pattern earned new terminology: none was unrepresentable-but-nameable.

| # | Pattern | Concrete case | Verdict | Witness |
|---|---|---|---|---|
| 1 | Correct result, defective procedure | Marker-string validator right today | **REP** | F2 (stopped clock): `RESULT_CORRECT` pass, `PROCEDURE_RELIABLE`+`ROBUST_NEIGHBORHOOD` fail |
| 2 | Incorrect result, adequate procedure | Triage router's justified rare miss | **REP** | F3 (`AdequatePathError`) — the cell Decision 0003 unblocked |
| 3 | Correct type, wrong token binding | Right standard, wrong reference plane / stale calibration | **REP** | F4: `GOV_TOKEN_ADEQUATE` sole failure |
| 4 | Correct token, executor deviation | Faithful binding, procedure not followed | **REP** | `EXECUTION_FAITHFUL` fail with `GOV_TOKEN_ADEQUATE` pass is directly encodable; no fixture needed (single-verdict flip of F1) |
| 5 | Adequate evidence strength, stale provenance | Strong but wrong-vintage evidence | **REP+FIX** | F6 separates `EVIDENCE_SUPPORT` pass from `EVIDENCE_CURRENT` fail |
| 6 | Safe route, nonoptimal route | Admissible but wasteful routing | **REP+FIX** | F7: `ROUTE_ADMISSIBLE` pass, `ROUTE_QUALITY` fail, PathwayAdequate |
| 7 | No route vs omitted route | Deliberately-none (recorded reason) vs defect | **REP** | Four-valued statuses: `not-applicable`+reason vs `fail`; F2/F3 na_reasons |
| 8 | Closure with deferred residual vs false closure | Release with deferred flake-investigation | **REP** | Definition 12/13: deferred disposition + truthful claim passes V5; collapse fails V5 |
| 9 | Shared task, different analysis | Two testers, same task, different tolerance | **REP** | Definition 3/§2.6: same `T`, different `A`; shorthand forbidden; composition requires declared fusion analysis |
| 10 | Shared occurrence, different observations | Poker deal; `Ω_α(m) ≠ Ω_β(m)` | **REP** | §10.1/note C4: information set = observation, never identity |
| 11 | Different profile spaces, compatible goals | Two actors' targets both realizable at one reachable occurrence | **REP+REPAIR** | Pass-1 item 11: typed `Compat_m` via `O*(m′; A_α) ∈ 𝒢_α ∧ O*(m′; A_β) ∈ 𝒢_β` — the pre-repair informal wording could not type this case |
| 12 | Robust locally, unreliable over reference class | Stable on the declared neighborhood, failing the declared reference-class criterion | **REP** | V6 pass + `PROCEDURE_RELIABLE` fail is encodable (no entailment either way, implication table); the F2 inverse |
| 13 | Reliable over reference class, fragile under perturbation family | Meets RelSpec threshold; fails PerturbSpec tolerance | **REP** | `PROCEDURE_RELIABLE` pass + `ROBUST_NEIGHBORHOOD` fail (F5's undetermined V6 shows the third state; direct fail variant is a status flip) |
| 14 | Authentic but stale directive | Recovered superseded instruction, faithfully followed | **REP+FIX** | F6 + `examples/compaction-stale-steer.md` (five predicates; Decision 0006) |
| 15 | Correct subepisodes, incorrect composite | Each verdict true in scope; composition transports one out of scope | **REP** | Core §5.2: `correct(e_Γ)` can fail with every `correct(eᵢ)` true; composite audited separately (machine-readable example: `examples/composite-episode.json`) |
| 16 | Incorrect subepisode corrected by a valid composite | Downstream validator catches an upstream error | **REP** | Core §5.2: `correct(e_Γ)` can hold while some `correct(eᵢ)` fails; supersession edge carries the correction |

**Outcome:** 16/16 representable; fixtures added: F6, F7; repairs induced: Pass-1 item 11 (typed compatibility), item 8 (robustness specification made well-formed — patterns 12/13 are only *statable* once `PerturbSpec` and `RelSpec` are both explicit). No unrepresentable pattern remains on this list; anything later found unrepresentable should be added here with a repair, not named around.
