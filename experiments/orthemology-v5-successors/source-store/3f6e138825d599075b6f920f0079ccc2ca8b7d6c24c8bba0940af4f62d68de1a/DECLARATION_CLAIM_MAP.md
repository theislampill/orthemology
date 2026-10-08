# Exact declaration/claim map

Names below are exact Lean declarations. Their definitions and theorem statements in the indicated source are authoritative, including all hypotheses. `DECLARATION_INVENTORY.json` lists every compiled declaration originating in the 88 root modules; each entry records its originating module and whether it is a theorem or unsafe/partial runtime auxiliary. A declaration's presence alone does not prove an external classification.

## Preserved foundations: 65 modules

The existing object syntax, raw conversion, current `P01AC.Has` typing, original `P01AC.F`/`P01AC.G` interpretation, intensional identity, separately named extensional repair, natural standardness and associated controls are unchanged. The machine inventory assigns these declarations to their exact originating modules. This integration asserts no new theorem for these foundations and does not identify the research P01AC interface with the distinct public P01DF interface.

## Preserved Raw bridge: six modules

- `EffectiveStandardness.lean`: `P01AC.EffectiveCompleteness.semantic_church_standardness` extracts an iteration index from a semantic natural. Self-related inputs are unrestricted raw terms.
- `EffectiveObserver.lean`: the canonical observer and reduction interfaces preserve explicit representation hypotheses.
- `EffectiveReduction.lean` and `EffectiveRuleBoundary.lean`: original F/G identity and semantic-witness transfer; current syntactic identity implies validity only.
- `EffectiveCanonicalTests.lean`: `P01AC.IdentityComplexity.related_iff_same_index` and `endpoint_valid_iff_canonical_tests` retain the required self-relations/current endpoint typings.
- `EffectivePartialObserver.lean`: `P01AC.IdentityComplexity.original_universal_identity_iff_total` and `original_universal_identity_iff_total_of_no_normal_form` retain their positive and negative representation/no-normal-form assumptions.

The global Raw Π₂ classification and existence/effectivity of the needed machine representation are written results, not claims of these Lean interfaces.

## Preserved Boolean bridge: five modules

- `EffectiveBooleanStandardness.lean`: `P01AC.BooleanIdentity.boolean_standardness`, `unique_boolean`, `pick_conv_injective`, `boolean_related_iff_observation`.
- `EffectiveBooleanCertificates.lean`: `P01AC.BooleanIdentity.bool_valid_iff_tests` and `invalid_iff_mismatch`, on the currently typed endpoint domain.
- `EffectivePrimitiveRecursion.lean`: `P01AC.BooleanPrimitive.PR`, `PR.denote`, `PR.compile`, `PR.compile_has`, `PR.compile_obs`, `discriminator_has`, `discriminator_obs`, `simFamily_has`, `sim_valid_iff_all_zero`. These construct actual source polynomials and current typings, with adequacy on arbitrary observed raw naturals.
- `EffectiveBooleanInterfaces.lean`: `P01AC.BooleanIdentity.original_identity_iff_all_zero`, `original_F_identity_iff_all_zero`, `family_semantic_proof_exists_iff_all_zero`, `current_family_identity_implies_all_zero`.
- `EffectiveBooleanControls.lean`: arithmetic, recursion-coordinate, zero-arity and explicit mismatch controls.

All-input validity and finite mismatch interfaces retain both endpoint typings where their statements require them. The typed Π₁ classification, finite machine/certificate encodings and no-computable-uniform-bound result remain written mathematics.

## Accepted pure-syntax and positive gate: two modules

- `BareBooleanGateSyntax.lean`, namespace `P01AC.BareBooleanGateSyntax`: `Pure`, `pure_abstract`, `compile_pure`, `simFamily_pure`, and the source-to-raw conversion lifting lemmas. Their purity/scope hypotheses are retained; compound raw atoms are outside the purity fragment.
- `BareBooleanGatePositive.lean`, namespace `P01AC.BareBooleanGatePositive`: `count_obs`, `family_input_obs`, `gate_closed`, `gate_pure`, `state_choice`, `state_halts`, `gate_halts`, `gated_has`, `gated_valid_iff`, `noHas_of_no_observation`.

The successful-gate theorems explicitly assume a nonzero observation exists. `noHas_of_no_observation` is a conditional elimination interface. The written nonhalting/head-standardization argument is not kernel formalized by these modules. In `verification/CheckGateInterfaces.lean`, `OperationalExclusion` is an explicit hypothesis in the checked equivalence; it is not a new axiom or a proved global exclusion theorem. The bare-code d.c.e. classification remains a written result.

## Accepted restricted compiler: one module

All names are in `P01AC.RestrictedIdentity`, source `RestrictedCompiler.lean`.

- `Expr`: constants in Nat, variables in `Fin r`, addition, multiplication and zero conditionals; arbitrary finite arity includes zero.
- `Expr.toPR_denote`, `Expr.body_has`, `Expr.body_obs`: genuine PR compilation, current Has typing and raw-observation adequacy.
- `Expr.closed_has`, `Expr.closed_obs`: repeated unchanged bracket abstraction; application order is coordinates r−1 through 0.
- `FragmentValid`, `fragment_valid_iff_denote`: equality on every natural tuple is equivalent to the exact original F relation at `Curried r`, uniformly in every unary environment and with independently related arguments.
- `fragment_F_identity_iff_denote`, `fragment_G_identity_iff_denote`, `fragment_semantic_witness_iff_denote`, `fragment_identity_formed`: exact original identity/witness and formation interfaces.

`Curried 0` is the natural carrier, not a one-arrow type. No raw eta axiom or inverse System F transfer is added.

## Full restricted decision procedure: seven modules

All new names are in `P01AC.RestrictedIdentityV2`.

- `ComputablePrelude.lean`: `finFunctionDecEq`, `coefficient`, `coeffEqual`, `zeroTest`, `masks`; finite executable list/tuple operations.
- `PositiveSeparation.lean`: `nat_polynomial_eq_of_positive_eval`; Nat-coefficient polynomial equality follows from agreement on all positive natural tuples, including arity zero. The proof uses pinned library polynomial facts via integer coefficient embedding and finite-variable induction. This is not a direct invalid Nat-field application.
- `SparsePolynomial.lean`: `coeffEqual_spec`, `coeffEqual_iff_polynomial`, `polynomial_append`, `polynomial_multiply`, `zeroTest_iff_eval_zero`, `zeroTest_iff_polynomial_zero`; duplicate coefficients are aggregated and zero entries are permitted. The positive-tuple premise is essential in the evaluation zero test.
- `MaskNormalisation.lean`: `normalise`, `normalise_correct`, `normalise_at_input`, `normalise_supported`, `denote_eq_iff_normal_polynomial_eq`; syntax-directed normalization, dead-coordinate support and all-input mask coverage.
- `IdentityChecker.lean`: `masks_complete`, `identityCheck`, `identityCheck_iff_denote`, `identityCheck_iff_fragmentValid`, `identityCheck_iff_F_identity`, `identityCheck_iff_G_identity`, `identityCheck_iff_semantic_witness`, `fragmentIdentityDecidable`.
- Also in `IdentityChecker.lean`: `verifyCertificate`, `makeCertificate`, `verifyCertificate_sound`, `makeCertificate_complete`, `finite_certificate_complete`; finite-table certificate verification is sound and complete for the exact declared semantic interface.
- `CheckerControls.lean`: concrete kernel-reduced and executed algorithm/certificate controls.
- `CheckerKernelAudit.lean`: complete restricted-v2 namespace proof-closure audit, with unsafe/partial runtime auxiliaries reported separately.

The complete typed Lean equivalences are:

    identityCheck e f = true ↔ FragmentValid e f
    (∃ certificate, verifyCertificate e f certificate = true) ↔ FragmentValid e f

These cover the whole declared grammar, not merely a compiler bridge or tested examples. Their endpoint relation is the unchanged original F/G identity, and they do not imply current-Has syntactic identity completeness.

## Accepted root polynomial-equality bridge: two modules

The exact new declarations are in `P01AC.PolynomialTestBoundary`, source `PolynomialTestBoundary.lean`.

- `predPR_denote`, `reverseSubPR_denote`, `equalPR_denote`: actual finite primitive-recursive descriptions implement predecessor, second-minus-first truncated subtraction, and an equality indicator with value 1 on equality and 0 otherwise.
- `Arithmetic`: constants, finite variables, addition and multiplication only. `Root` is either an old expression or one root equality test on two pure-arithmetic expressions. Neither pure zero tests nor nested new root tests enter this grammar.
- `Root.toPR_denote`, `Root.body_has`, `Root.closed_has`, `Root.closed_obs`: exact compilation, current Has typings at `Curried r` and adequacy on arbitrary raw natural observations. Arity zero is nonvacuous and the endpoint carrier is Church-natural.
- `valid_iff_denote`, `F_identity_iff_denote`, `G_identity_iff_denote`, `semantic_witness_iff_denote`: equality of the total denotations is equivalent to the exact original F/G semantic relations, retaining both self-related endpoint outputs and independently related input lists.
- `identity_formed`: current identity formation is available. Semantic validity is not cast into current-Has identity inhabitation.
- `root_equal_zero_iff`: validity of the root equality indicator against old constant zero is equivalent to the two arithmetic comparands never being equal. This is the non-equality polarity required by the separately written classification.
- `PolynomialTestAudit.lean`: all safe declarations of the new namespace are audited transitively. Compiler-generated unsafe/partial nonproof runtime auxiliaries are reported and excluded as roots; no unsafe/partial dependency is permitted in a checked proof closure.

The full polynomial-test hierarchy theorem, parser/enumeration coding, integer coefficient transformations, specialization/reduction construction and certificate/bound impossibility consequences remain written mathematics. These modules supply no representation axiom, numerical witness-arity bound, runnable machine-to-polynomial reducer, or general bare endpoint-code recognizer. The restricted Lean decision procedure above continues to cover its original zero-test grammar only.

## Explicit nonclaims and representation distinction

The unchanged Python JSON reference has no proved refinement relation to the new Lean program. Its strict canonical JSON validation differs from the Lean typed-list certificate interface, which allows harmless reordered, duplicate or extra rows when every required mask has valid coverage. The Lean interfaces do not include a JSON parser, arbitrary source-code recognizer, or serialized typing-derivation validator. Consumers making a separate endpoint claim must bind it to the exact compiled fragment expressions.

The explicit degree-plus-one finite-grid bound and grid witness search remain at the written/reference-code boundary; they are not used to justify the kernel-checked coefficient decision procedure. No decision procedure for unrestricted PR equality, arbitrary subtraction or general nested equality tests is added. Higher-order inputs, arbitrary currently typed source equality and global arithmetic-hierarchy classifications are outside the kernel claims. No world-novelty claim is made.
