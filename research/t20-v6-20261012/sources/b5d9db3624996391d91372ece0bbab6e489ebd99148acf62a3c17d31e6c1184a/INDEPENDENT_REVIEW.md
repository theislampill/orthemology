# Independent review: actual HasE Raw-motive boundary

## Verdict

**PASS for the stated source-specific boundary claims.** No blocking mathematical, source-binding, or Lean defect was found in `RawMotiveBoundary.lean` at SHA-256 `ace7022513163b11ee3cc3e6114e3ffd654f38b4614bf0463d4bbb9b654e8f57`.

The actual source calculus forbids Raw typing of the endpoint coordinate at `N → N`, including in its real two-coordinate J-motive telescope. Therefore the literal `Id_Raw(var 1, q)` motive cannot be formed. Even assuming the original typed identity as a telescope declaration does not permit a proof of the corresponding Raw identity, for any proof polynomial. These are consequences of the **inherited original F/G all-rule soundness**, not a soundness theorem for the newer open-term full-PER model.

The original literal target `HasE [] c3 (W q)` remains **OPEN**. This review proves neither that target nor its negation.

## Verification and source binding

- Lean 4.19.0, executable commit `6caaee842e94`.
- Independently compiled the exact author file with `--trust=0` into this package's new `validation/independent-lib/RawMotiveBoundary.olean`; exit 0, no warnings or errors.
- Independently compiled `validation/IndependentBoundaryChecks.lean` with `--trust=0`; exit 0, no warnings or errors. Its eight checks establish explicit coordinate reductions, semantic non-vacuity, closed-polynomial Raw typing, formation of the negative assumed-context target, Raw typing of the fixed q endpoint, and existential noninhabitation.
- Reused the already independently rebuilt 83-source closure in `hase-imported-compiler-transport-20261010/validation/independent-lib`, as requested. This review did **not** repeat that closure build. Existing third-party libraries were reused from the pinned package environment.
- Recomputed every one of the frozen package manifest's 113 file hashes and byte sizes; all match. Recomputed all 83 project-source SHA-256 and Git-blob hashes, checked their exact-path entries in the retained source index, and matched them to the prior independent source build records. Recorded current import-object hashes.
- The retained index's Git blob is `964b610cad10e90ec42311721e111cf55e221b4e`, bound by its acquisition receipt to repository `theislampill/orthemology`, commit `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`. No new remote fetch was performed; this is verification of retained pin/receipt/index/source bindings, not a fresh remote provenance claim.
- The seven author axiom reports and eight reviewer-check reports contain only `propext`, `Classical.choice`, and `Quot.sound` (or subsets). No `sorryAx` or new postulate is present in successful outputs. Both new Lean sources were scanned outside comments for unapproved escape constructs.
- The author file and all frozen manifest files were unchanged after validation. Reviewer additions are confined to this package's `validation/` directory. An initial reviewer-only check used `ContextLaws.hends` instead of `ends`; Lean rejected that E/H mismatch. It was corrected in the reviewer file, with the failed attempt retained separately. The author file required no correction.

This remains verification relative to the installed Lean executable and dependencies, not a bootstrap verification of Lean itself.

## Mathematical audit

### Literal source endpoints and the real telescope

The definitions at author lines 15–21 use `variableExpr.closed` and `redundantExpr.closed` from `UnaryCurrentIdentityBoundary`, not `UArrowControl.p/q` or the newer model's mirror terms. The original definitions are `.variable` and `.add .variable (.constant 0)` at source lines 38–39. The source's raw nonconversion theorem is at lines 67–70; semantic checker acceptance is at line 72.

`AllSyntax.lean:89–97` defines lookup with weakening and

`theta Γ A x = identity (wk A) (pren Nat.succ x) (var 0) :: A :: Γ`.

Consequently the final motive telescope has proof coordinate 0 and endpoint coordinate 1. The author uses these coordinates correctly. The assumption-variable control has type `wk B`, as the actual `Lookup.zero` rule requires; no binder shift is silently discarded. Reviewer checks confirm the exact telescope shape and evaluation of both coordinates by definitional equality.

`motiveAt` substitutes proof first and endpoint second (`AllSyntax.lean:28`), agreeing with this order. Since q is closed source syntax, leaving q literally in the displayed motive does not turn it into a bound endpoint. The reviewer independently proves q Raw-typable in this same theta context.

### Context formation and semantic non-vacuity

The author proves old formation of B, formation of `[B]`, the actual assumption-variable judgement, and formation of theta (lines 24–31). These are actual grammar judgements, obtained through source structural lemmas and source inclusion theorems. They are not definitions that assume well-formedness.

`typed_related` obtains `F EndN ρ zeroEnv p0 q0` by projecting the **semantic** identity-checker theorem. It does not obtain or assume `HasE [] r B`. Likewise `p_self` uses ordinary typing of the original compiler endpoint, not the disputed identity.

`endpoint_environments` relates the two explicitly different environments with heads p0 and q0. `theta_environments` extends them with proof head I. The head relation uses p0 self-relatedness in the left environment because that is how E is defined (`AllPredicates.lean:116–118`); the tail already carries p0/q0 relatedness. This apparent left bias is legitimate. The inherited `ContextLaws.ends` law derives D-membership for **both** resulting environments, and the reviewer checks this explicitly.

For `[B]`, the identity-checker semantic theorem supplies an actual D/E witness with proof coordinate I. Thus none of the negative results relies on an empty or inconsistent semantic context. Syntactic formation of the assumed identity does not imply a closed syntactic proof of it, nor is such a proof needed for the context assumption test.

### Endpoint Raw typing and literal motive formation

In the inherited interpretation, `F Raw` is raw conversion (`AllPredicates.lean:13, 51–53`). Applying the actual `ExtensionalRepair.unary_fundamental` to a hypothetical endpoint-Raw derivation forces conversion between p0 and q0 when evaluated in the exhibited related environments. The original source proves those terms nonconvertible. This establishes both `no_endpoint_raw` and `no_theta_endpoint_raw`.

These arguments quantify over **every derivation of the claimed HasE judgement**, not just the variable rule. The imported soundness proof covers all HasE constructors, including proof erasure, J, term conversion, Pi extensionality, and All extensionality (`ExtensionalRepairSoundness.lean:113–164`). Indirect elimination, J, or conversion paths are therefore covered.

`endpoint_motive_not_formed` inverts actual `FormE.identity`, whose explicit premises require Raw typing of both endpoints (`ExtensionalRepairSyntax.lean:15–22`). Its first endpoint premise contradicts `no_theta_endpoint_raw`. There is no independent type-formation conversion constructor bypassing that inversion.

The positive proof-coordinate control at author lines 34–39 uses `HasE.proofErase` exactly on an identity-typed proof variable. It shows that legitimate proof erasure still works. It does not erase the function endpoint, quote its code, add a coercion, or identify a typed term with a Raw code variable.

### No Raw reflection even under the typed-identity assumption

For arbitrary r, a hypothetical `HasE [B] r (identity raw p q)` is interpreted in the explicit assumed-identity environment. Projecting the Raw-identity semantic relation yields conversion of the endpoints evaluated in that environment. The source `eval_closed` lemmas, justified by each compiler endpoint's actual closed typing, reduce those evaluations to the original zero-environment p0/q0 pair. The original nonconversion theorem gives the contradiction.

This is a stronger test than merely rejecting the displayed varying-endpoint motive. The reviewer independently proves `FormE [B] (identity raw p q)`: both p and q are closed source polynomials, so structural Raw-atom/application rules type them. The target really is formed but uninhabited. The closed-syntax lemma has an impossible variable case at scope 0; it supplies no new coercion for an open bound variable.

## Novelty and limits

The narrow addition is an explicit specialization to the original x/x+0 compiler endpoints, their real endpoint and J-motive coordinates, and a semantically inhabited context assuming their typed identity, together with a positive proof-erasure control.

This is **not** a new general theorem that extensional repair preserves Raw separation. The imported source already contains `closed_raw_identity_conversion` and `raw_separation_no_has` for another witness in `ExtensionalRepairTheorems.lean:12–39`, plus a positive proof-erasure control at lines 59–61. The new results use the same inherited semantic mechanism in the newly audited contexts; their value is the precise boundary diagnosis.

No broad claim that all non-Raw terms resist erasure, that all possible motives are invalid, or that all routes to the original target are blocked follows. No raw conversion relation is extended. No soundness of the newer full-PER whole calculus is supplied. No closed HasE proof of B or of the original `HasE [] c3 (W q)` target is assumed or established.

**Disposition:** accept the stated additive boundary result without source changes; retain the original target and new whole-model soundness gaps explicitly.
