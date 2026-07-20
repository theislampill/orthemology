# Phase D — reference-model completion and adversarial audit (R4 independent review)

**Date:** 2026-07-20 · **Session:** independent Fable review of PR #3 (harness identity `claude-fable-5`).

Every schema probe in independent-audit §6 was reproduced (or accepted-plausible) in the read-only pass and is repaired below. Nothing in D1/M1/O2/0004–0010 was reopened.

## Repairs by audit item

| Item | Defect | Repair | Regression evidence |
|---|---|---|---|
| 6.1 / D1 | inheritance checked only for parent resolution; cycles, self-edges, and effective incompleteness silent | cycle + self-inheritance detection; materialized effective analysis must declare all 12 constitutive components; multi-parent remains structurally unsupported (schema: single `inherits_from` object) | fixtures I29 (self), I30 (2-cycle), I31 (unresolved chain); mutation family 19 (6/6 killed) |
| 6.2 / D2 | schema does not require `domain_ref`/`policy_class` while the audit read the prose as constitutive | resolved by documentation, per the owner's Decision 0001 component list, which excludes both: `M_A` is induced by boundary+repertoires; policy lives at the governance layer. Schema descriptions and Decision 0012 amendment state this explicitly — schema and theory no longer disagree about what a full analysis is | schema description text; 0012 amendment |
| 6.3 / D3 | duplicate embedded `token_id` across episodes undiagnosed; flat global resolution set | ONE rule chosen: `token_id` globally unique across the bundle; standalone redeclaration of an embedded token allowed only with matching `of_type` and `anchor` | fixture I32; mutation family 20 (2/2 killed) |
| 6.4 / D4 | every token's scope checked against every ledger → reciprocal false positives on legitimate two-episode bundles | owner-scoped check: token claim-scope resolves only against its OWNING episode's ledger(s); standalone tokens carry `owning_episode` (schema field) or `scope.external_scope` | `examples/shared-upstream-corroboration-failure.json` is the positive regression — the pre-repair validator (from commit `1223110`'s tree) reproducibly emits the two false positives on it; fixtures I33, I34; mutation family 21 (2/2 killed) |
| 6.5 / D5 | `of_type`/`mu_refs` unresolved references and precedence edges unchecked | metaortheme-edition resolution wherever the bundle declares the `mu_id`; embedded tokens must sit inside the declared governing configuration; precedence irreflexive + acyclic over declared types; transitive closure documented as derived | pillar bundle now declares its two metaorthemes + a precedence edge; fixtures I35–I38; mutation families 22 (3/3), 23 (2/2) |
| 6.6 / D6 | silent external analysis/occurrence references accepted on audit-ready records | explicit reference modes: bundle-local resolution, `external_refs` (kind/ref/registry/resolution_status) on the episode schema, and `unresolved` → not audit-ready | fixtures I39, I40; mutation family 26 (13/13 killed) |
| 6.7 / D7 | lexicographic ISO-timestamp comparison; no naive-timestamp rejection; no validity ordering | `_parse_ts`: timezone-aware parse, UTC normalization, naive rejected wherever ordering matters; RelSpec pre-outcome ordering and token `effective_from ≤ expiry` computed on UTC instants | fixtures I41 (mixed-offset postdated RelSpec that string-compares "before"), I42 (naive), I43 (inverted validity); mutation families 24 (4/4), 25 (7/7) |
| 6.8 / D9 | bundle-local checks described in global-completeness language | scope statement in the validator docstring and Decision 0012 amendment: all claims are bundle-local; store-level validation is an acknowledged open extension | wording, not code |
| §5 / D8 | supplied `req_reason` projection trusted | projection must EQUAL the governance derivation from the ledger claim's declared shape (`claim_type`, `depends_on_tokens`, `currency_exempt`, `robustness_obligation`); claim-wise truth-link factivity check added | fixture I44; mutation family 27 (38/38 killed, generated only where the ledger claim resolves — same guard philosophy as family 5) |

One derivation refinement surfaced by running the new equality check against the existing corpus: `stale-directive`'s authenticity claim legitimately excludes `EVIDENCE_CURRENT` (the truth of "this copy is faithful" does not decay with evidence currency). Rather than force the record wrong, the rule table gained the typed dimension `currency_exempt` (`EVIDENCE_CURRENT: when: not_currency_exempt`), declared on the ledger claim and defaulting to false.

## Mutation suite state (re-derived from the final tree at claim time)

`validate_recursive_mutations.py`: **9 example bundles, 27 operator families, 1,813 mutants — 1,546 schema-killed, 248 semantic-killed, 19 survivors, all 19 declared equivalent with stated reasons, 0 unjustified.** Per-family counts are printed by the validator itself (no family generated zero mutants — an empty family fails the run). The 19 equivalents are one adjudicated class: residuals disposed `validated-resolved` carrying BOTH `evidence_refs` and `verdict_refs`, where deleting one leaves the other discharging the conditional-field requirement, plus the empty-residual-list well-formedness cases — extended to the new shared-upstream bundle and re-signed for the pillar bundle's new part indices.

Prior figures for comparison, neither citable as completeness: R3's "208 mutants" (three top-level operators) and the R4 candidate's "1,247 mutants / 18 families" (no coverage of the §6 gap classes above).

## Invalid-record corpus

`tests/invalid`: 28 → **44** fixtures (I29–I44 added); the negative-fixture harness now supports multi-record bundles (`parts`) for defects that only exist between records. Every semantic fixture is schema-valid by design and flagged by the semantic layer; every schema fixture is rejected by the schema layer.

## What is deliberately NOT claimed

- No store-level (cross-bundle) validation exists; all consistency results are bundle-local (D9).
- `RequiredReasonBy`/`RequiredBy` remain governance-supplied parameterized interfaces; the shipped tables are single complete deterministic instances.
- Mutation coverage is relative to the declared operator families and the shipped example corpus; "0 unjustified survivors" is a statement about those, not about all possible mutations.
