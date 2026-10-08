# Independent dependent-All review controls

Status: in progress. The frozen v5 contract and accepted-nucleus reconciliation have been read and hash checked. No dependent-All implementation is accepted and no compiler has been invoked for this review.

## Required contract gates

- Syntax-only finite mutual Ctx/Form/Has rules; genuine recursive All; finite-instance literal atom import with binder-aware finite image support, Bottom default, and smaller formation premises.
- Structural pair F/G, followed by raw zero-padded D/E/H. No lawfulness or semantic membership in syntactic constructors.
- Conditional paired mixed semantic substitution with replacement law packages, including diagonal environment equality for nested All, preceding its use in mutual soundness.
- Full context/type laws, universal heterogeneous fundamental theorem, endpoint validity and two-sided invariance, and strong diagonal at related unequal valuations.
- Separate literal syntactic mixed substitution, finite zero-padded term images and scoped identity; term/type binder lifts and both J coordinates.
- Exact-code intrinsic contexts/types/terms/substitutions. Full nucleus derivation translation and predicate agreement.
- Support-certified Type-valued old-rule-tree comparison including allIntro/allElim and non-finite All. Preserve opaque Prop-valued PolyConv internals and displayed endpoint support.
- Exact inherited D/self, joined Q/self, genuinely open Id replacement, nonempty dependent Sigma replacement, and retained negative boundaries.

## Discriminating controls to implement against actual interfaces

1. Reject unshifted All introduction from an assumption of Param 0: its shifted declaration is Param 1, and instantiation at Bottom separates the incorrect rule. Test actual absence through universal soundness, rather than only checking a constructor name.
2. Substitution through All(Pi(Raw,Param 1)) with replacement Id(Param 0,var 0,I) must produce All(Pi(Raw,Id(Param 1,var 1,I))). This one test exercises both binding sorts. Repeat with a second term binder and Sigma and with the two-coordinate J motive.
3. Establish that raw malformed replacement types need not satisfy unequal-valuation diagonal/transport; do not accidentally certify a semantic substitution theorem lacking its replacement-law hypotheses. Inspect its nested All proof to identify exactly where diagonal equality of the induced replacement environment is used.
4. Use independent nonempty total/raw endpoint PERs, I versus SKK valuations, and an Id replacement to show either endpoint equality may fail while both cross links hold. Require the actual elimination theorem to instantiate the two-endpoint replacement Link.
5. Exercise U transport at unequal E-related valuations. A theorem specialized to identical valuations, or a proof using only the pointwise unary intersection, fails the contract.
6. Import an accepted finite proof with an opaque atom whose source term is an application. Require the final polynomial literally atom(t); inspect unchanged PolyConv and reject any atom/application bridge. Include a nested finite All whose free parameter support must subtract binder depth.
7. Check finite image maps beyond their list length are atom zero and type tables outside support are Bottom. Disprove global equality of finite identity images and var; prove scoped polynomial/type identity and valid-valuation identity instead.
8. Instantiate the new legacy certificate on old allIntro/allElim and dependentPolyType, and reject a retained tree with an unscoped Raw premise but closed conclusion. Exercise legacy J through its Id proof coordinate using restricted proofErase, not a claim that Theta is all-Raw.
9. Preserve I/SKK non-convertibility, nonempty changing Raw fibres, invalid typed-to-Raw coercion, missing Id endpoint equality, missing J proof-coordinate transport, typed Omega, and canonical/universe/normalization exclusions.

## Evidence discipline

Source-only reconstruction will copy Lean source bytes, never candidate object files. The existing hash-verified Lean 4.19.0/Mathlib toolchain will be used with one explicitly coordinated serial lane, -j1, 180 seconds per module, default heartbeats and recursion, and at most two global compiler processes. Exact declaration contracts and all transitively collected axioms will be audited. Failed historical attempts will retain their source hashes and logs; no failed attempt counts as accepted evidence.

This is automated independent mathematical/source/kernel review, not human-specialist validation, novelty certification, canonical adoption, or U11 closure.
