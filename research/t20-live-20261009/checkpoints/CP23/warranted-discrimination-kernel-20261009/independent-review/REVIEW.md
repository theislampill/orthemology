# Independent review: certificate-frontier kernel formalization

9 October 2026. Revision-bound review of Theorem 1 only.

**Finding:** No blocking mathematical defect or mismatch with Theorem 1 was found in the frozen source. Canonical inverse, necessity, and persistent update are proved; they are not imported as hypotheses. The formal result concerns finite support/cost catalogues and their observations.

## Revision binding

SHA-256:

- `CertificateFrontier.lean`: `5e799995b95e37105dff8dfe10e5ba78dfe44034334353bcf66107069e8a67e0`
- `Controls.lean`: `7d49f0df7d1b5eb633e6edebf17bc0a967eeff1718b9e1cc3fcab1513afb5132`
- `replay.sh`: `925769666b67cdccae6da51365e58bc4beaf81c7512f3d5673c7f157d3038593`
- Compared manuscript `../warranted-discrimination-research-20261009/RESULT.md`: `71551ae962a17ec72709b6d36cfb58ed99237a2ef776339709a43b8d3b436d28`
- Compared mathematical review `../warranted-discrimination-research-20261009/review/REVIEW.md`: `35c595f3626c7c86bddd4d0941708a938085ce96a1e67da5adf2bde7804b1149`

The compared manuscript paths above are relative to the kernel directory. Frozen source copies and logs are retained beside this review. Original source and manuscript/review files were not edited by this reviewer.

## Substance and correspondence

1. **Theorem 1.1:** `cost_le_iff` proves finite-threshold attainment from the finite catalogue. `exists_frontier_le` derives a dominating retained pair from finiteness, without assuming that the input is normalized. `cost_frontier` and `inventory_cost_recovery` prove exact cost recovery.
2. **Theorem 1.2 and exact inverse:** `frontier_inverse` has no catalogue-membership premise on its right-hand side. Its reverse proof obtains an attaining catalogue pair, proves its support equals the proposed support using immediate deletion tests, and proves equality of costs. Empty support is covered. `frontier_eq_iff_cost`, `inventory_canonical`, and `per_verdict_canonical` then prove both directions of canonical equivalence, preserving verdict identity.
3. **Theorem 1.3:** `residual_eligible` proves the support identity, `cost_residual` proves the union cost law, and `residual_residual` proves composition. `frontier_residual_normalize` derives normalization/update commutation via the already-proved canonical equivalence. `inventory_update` and `inventory_congruence` supply the manuscript's actual-inventory formulation. No algebraic update equality is assumed as an extra hypothesis.
4. **Theorem 1.4:** `inventory_summary_necessity` assumes only the appropriate decoder-correctness contract for inventories of a fixed per-verdict catalogue. Equal summary values are proved to imply equal frontier tuples. Together with recovery/update, this establishes the stated coarseness among exact cost summaries, without claiming uniqueness of encodings or minimum physical storage.

`frontier_antichain` and `frontier_idempotent` additionally derive normalization properties. Duplicate pairs are identified by `Finset`.

## Cost and infinity boundary

`C` is an arbitrary linearly ordered price type; observations have type `WithTop C`. Every admitted price embeds strictly below the newly added infeasibility value. This is a valid order-theoretic generalization of finite nonnegative real prices: Theorem 1 needs neither addition nor nonnegativity. The source does not prove numerical cost calibration.

Choosing a price type that itself has a top still produces a *second*, distinct observation top. Therefore the theorem must not be described as allowing an actual infinite certificate price to coincide with infeasibility. `infinite_price_counterexample` correctly demonstrates failure under the deliberately different, collapsed-infinity observation semantics.

Token and verdict types need not be finite in the generalization; catalogues, inventories, and continuation supports are finite sets. Specializing to the manuscript's finite universe/verdict family is immediate. A separate explicit real-import probe was unavailable because the reused installation lacks `Mathlib.Data.Real.Basic.olean`; no separately compiled real-instance test is claimed.

## Verified execution

The frozen `replay.sh` was copied unchanged into this review directory and executed independently: exit 0. Lean 4.19.0 (`6caaee842e94`), mathlib checkout `c44e0c8ee63ca166450922a373c7409c5d26b00b`, existing compiled dependencies reused read-only.

- Main theorem file and positive controls compiled with `-DwarningAsError=true`.
- All three false strengthening files failed specifically because `decide` proved their propositions false, rather than because of a missing import or elaboration error.
- Supplementary `ScopeChecks.lean` compiled, checking Nat specialization, empty catalogue, empty support, and distinct nested top.
- Printed axiom dependencies for all 13 main exposed results and all four controls were only `propext`, `Classical.choice`, and `Quot.sound`; no `sorryAx` appeared. No custom axiom or admitted proof was found in the reviewed source. This is a classical Lean proof, not an axiom-free or intuitionistic certification.

Evidence: `final-replay.log`, `scope-replay.log`, `mutations/*.log`, `INPUT_HASHES.txt`. Replay does not rebuild or independently audit the full Lean/mathlib dependency stack.

## Unproved adjacent matters

The admitted inputs are support/cost pairs, not derivation objects. `frontier_subset` supplies a realizing original pair; it does not construct a certificate ID, validate a proof grammar, authenticate evidence, or preserve a concrete proof object. Connecting an admitted proof catalogue to these pairs remains a representation boundary.

No Bellman/planning theorem, permitted-action sequence realization, physical-memory bound, full provenance preservation, source-trust claim, semantic warrant, or philosophical conclusion is certified here. No integration, adoption, or programme-closure conclusion is made.
