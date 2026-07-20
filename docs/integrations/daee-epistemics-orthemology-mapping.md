# Bounded integration note — daee-epistemics → orthemology

**Date:** 2026-07-20 (R3) · **Reviewed:** public `theislampill/daee-epistemics` (read-only). **Non-identity boundary, stated first:** the two projects are not merged and are not the same system; daee-epistemics's theological commitments are **not evidence** for orthemology (and vice versa); no term is imported merely because both projects have a nearby concept; no large prose body is copied. What is imported is *generic control discipline*, translated into ordinary language and re-derived inside orthemology's own formalism.

## R4 recheck (2026-07-20)

The current public `theislampill/daee-epistemics` repository was re-inspected. All five controls described below still hold as stated: canonical atomized source (`atomics/skill/`) generating an uncommitted runtime with freshness checks; evaluator/practitioner symmetry; the inference-boundary legend; whole-state reread after a burden lands; and the bounded release/closure contract. **Two further engineering applications are adopted in R4** (and only these):

1. **`docs/current-state.yaml` as one canonical project-state source**, with generated/validated public surfaces — the direct analogue of that repository's atomized-source→generated-surface discipline (Decision 0014).
2. **Transition-triggered whole-state reread extended to source-status changes** — R3 implemented only the closure-floor slice; R4 requires the whole-state pass after any burden disposition, source-status transition, analysis-version change, or canonical-artifact change, not only at final closure.

**Still rejected, unchanged:** the domain-specific deformation ontology; theological claims as operational evidence; field-pressure notation adopted for aesthetics; routing modules irrelevant to orthemology; any claim of repository isomorphism or merger. The non-identity boundary below is unchanged.

## Imports adopted

| # | daee-epistemics discipline (source location) | Orthemology implementation |
|---|---|---|
| 1 | **Evaluator/practitioner symmetry** (`atomics/skill/SKILL.md`: the practitioner runs the same deformation check on itself before applying it outward) | Fixture **CR-7** (`tests/reason-fixtures.json`): the auditor's own audit episode is reified and scored under the same verdict vector — no privileged evaluator exemption; enforced by `validate_reason_fixtures.py`; conceptually anchored in the core's episode-reification (ι) machinery |
| 2 | **Whole-state reread after a burden lands** (`references/diagnostics/recursive-state-transitions.md`: `Land(Bn)` → reread the entire live field before continue/stop) | Example `examples/whole-state-reread.json` (resolving one burden invalidates another; the reread blocks the closure claim) + a new cross-record rule in `validate_cross_record_semantics.py`: a non-null `closure_claim` is ill-formed while any residual is `unresolved` (Definition 13 made machine-checkable); negative fixture N11 proves the rejection |
| 3 | **Inference-boundary / source-status legend** (`references/diagnostics/diagnostic-ir.md`) | The four-way legend [direct-source] / [secondary-reconstruction] / [synthesis] / [orthemological extension] adopted in `companion/CONCRETE-AND-SOUND-REASON.md` §1 and the R3 companion sourcing ledger |
| 4 | **Canonical atomized source → generated surfaces** (`atomics/skill/` source vs generated `skill/` runtime with freshness checks) | `scripts/generate_from_registry.py`: the verdict registry generates the schema enum and the prose alias table (`docs/generated/verdict-aliases.md`), with a `--check` drift gate in CI |
| 5 | **Bounded release/closure contract** (`references/rubrics/diagnostic-render-contract.md`: closure as a formal residual condition) | Mapped onto **V5 (CLOSURE_TRUTHFUL)** + the residual-disposition taxonomy: closure quantifies over the burden ledger; the R3 rule in import 2 is its machine floor; the project's own R2→R3 supersession practice is the discipline applied to itself |

## Imports rejected (with reasons)

- **The deformation taxonomy itself** (hawā, gharaḍ, etc.): theological/noetic content — outside orthemology's school-neutral operational layer; the *generic* lesson (evaluator self-check) is import 1; the specific taxonomy is not evidence here.
- **Field-pressure metaphors** (`∇·T`, `∇×T`, MRP): metaphor-laden control vocabulary with no orthemological definition; importing names without semantics would violate the project's own benchmark-gated-vocabulary rule.
- **Routing-precedence machinery**: solves a dispatch problem orthemology does not have.
- **Layer A/B traversal and render contracts**: output-formatting governance specific to that skill's runtime.
- **Any suggestion the systems are isomorphic**: they share a false-closure ethic, not an ontology.

## Assessment: canonical-source generation (import 4), scope decision

Generated now: verdict enum + alias table (highest-drift surfaces; both had hand-maintained copies in R2). Assessed and deliberately **not** generated: fixture skeletons (hand-authored fixtures carry intent that generation would flatten) and validators (generating checkers from the registry they check would weaken independence). Recorded as a scoping decision, not an omission.
