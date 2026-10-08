# Finite source-context continuation checker

This is an isolated research checker for the corrected design in ../ARTICLE.md and ../EXACT_EFFECT_ALGEBRA.md. Python 3.12 and the standard library suffice. It is not a natural-language parser, source-authentication service, permissions engine, deployed agent or extension of G1/P15.

## Run

From this directory:

    python -m unittest discover -s tests -v
    python exhaustive_validation.py
    python source_and_release_validation.py
    python semantic_mutations.py

The scripts write bounded results under logs/. The original test-first missing-module failure is preserved in logs/tdd_red.txt. No test reads a connected account or queries an external source.

## API

context_effects.py provides opaque-model Origin keys, incoming Ref expressions, compile_effect, compose, rename_outputs, apply_effect and resolve_demands. The normal form and exact domain follow EXACT_EFFECT_ALGEBRA.md. compile_effect accepts a finite event list using enter/leave/exit/emit; selected IDs, when specified, belong to that fragment. Keyed exit constraints retain exact original-key equality. Source key fields are Python values in this implementation; the mathematical lower bound separately restricts policy use to the opaque-handle API.

read_cover.py provides:

- role_decision: true, false or unresolved from supplied source-role evidence. None is not completion.
- cover_dp: exact subset-state shortest path for at most 20 demanded original keys. Its worst-case complexity is exponential; no general efficient card optimizer is claimed.
- interval_cover: exact weighted recurrence after supplied adequate coverage has been checked convex on the demanded original order. This does not infer adequacy from raw text contiguity.
- minimax_cost: independent finite observation-tree optimization for at most 256 worlds and 24 windows, using all declared metadata and full responses. It does not call either cover optimizer.
- star_locality: the finite sufficient all-positive-star transcript condition only.
- coverage_sufficiency: a separate finite response-fibre check that each covered role is determined by the observed response/metadata.

The last two checks are distinct. A constant all-key response passes locality vacuously but fails sufficiency. Neither proves actual source truth, authenticity, parse adequacy, permission, a physical service's conformance or target-model correspondence. The full finite response table supplies the interpretation used by the control. Eligible/adequate window flags are supplied model assumptions, not self-authorizing certificates.

## Evidence scope

The named tests trace all 44 independently proposed adversarial cases and add service/retention/verdict/locality-adequacy controls. Some are narrow interface/scope checks rather than algorithmic benchmarks; no evidential weight is inferred from their count.

The exhaustive script compares a separately written bottom-first conventional stack with symbolic effects, checks all bounded splits and selected parenthesisations, and compares interval/subset algorithms with independent subfamily enumeration. Small product-source models compare the cover result with a finite adaptive decision-tree calculation. The numerical limits and exact counts are in logs/exhaustive_results.json. These finite checks corroborate implementation; the universal mathematical argument is separate.

The 16 semantic mutation controls are executed wrong-summary, wrong-cost or wrong-interface variants. They are not compiler-generated production mutations and are not a weak baseline from which superiority is inferred. The strongest conventional stack/shared-ID/cover baseline is expected to tie.

## Source and joined-release fixtures

fixtures/source_roles.json is a supplied, reviewable analytical extraction linked to the compact source capsule. Tests check its internal scope-return and source-key relations; they do not establish its natural-language interpretation. The source's actual full-page availability is retained as a negative control against manufactured hardness. Bilingual proposition preservation is not certified.

The release fixture is a different, explicitly synthetic role-record service. Fixed, role-independent retention of a or c gives worst-case later cost1; fixed b or unrelated old-task d gives2. A legitimate adequate fixed-Q verdict or agreed label-dependent selection code gives0. Negative witnessed roles permit early termination. No moral obligation follows from the arithmetic; the separate practical-authority application supplies its normative premises.

## Costs and custody

Costs are positive exact Fraction values. Infinity denotes no completing cover/policy under this model. Read cost is conditional on already supplied identity maps and adequate witness services; map preparation, source interpretation, record construction, authentication, storage and transfer costs are separate. Public metadata or a value-dependent retention selector can reveal information and must not be hidden to preserve a lower bound.

The source roles refer to the original witnessed document. Current-carrier speech act remains a separate field. Copying an original assertion does not grant a new assertion or permission. Origin equality is not proposition equality, acquisition independence, numerical identity or a proof of actual source authenticity.
