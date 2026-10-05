# Independent review: closed polymorphic source-normalization boundary

Disposition: ACCEPTED for the bounded contract. Exact evidence is recorded in `VERIFICATION.json`. This is a bounded automated independent source and kernel review, not human-specialist or empirical validation. No canonical source or accepted calculus is changed.

## Contract and source binding

The ordinary admission `../../reviews/final-scope/POLYMORPHIC_NONNORMALIZATION_ADMISSION_v1.md` and independent design `../../reviews/normalization-boundary-design/DESIGN_REVIEW_v1.md` control this review. All 17 entries of the design input manifest were rehashed successfully. The 47-module mathematical dependency closure of AllLegacyDerivations and P01Omega was reconstructed from accepted source alone and verified against the accepted dependent-All SOURCE_IDENTITIES manifest. AuditSupport is the 48th inherited source; its bytes also match that manifest. No author-generated object is used. The exact candidate and readback are copied as source, with identities in the receipt. The small independent control is additional review source.

Historical author attempts are not rewritten or counted as independent successes. This review's source snapshots and logs are separate from author evidence. Package-relative paths identify all bound review sources and logs. The explicit external TOOLCHAIN_ENV is a reproduction parameter, not a portable package path.

## Literal positive result

Inspection of the concrete definitions finds exactly t = S K (K Omega) and the matching application polynomial p = app(app(atom S, atom K), app(atom K, atom Omega)). The universal `eval_p` theorem is literal definitional equality, not an atom/application conversion rule.

`tree` is a Type-valued inherited Derivation tree. S is instantiated at (param 0, Raw, param 0), the first K at (param 0, Raw), and the second K at (Raw, param 0). Only atom Omega enters through Raw. Two applications then All introduction give the closed old identity type. `tree_supported` checks the complete tree at term scope zero. `old_typed` erases that exact tree to old Has; `new_typed` invokes accepted Supported.raw_embed with the identical p. `new_finite_target` reads the same result as fin(identityCode), whose inherited definition is All(var0 → var0). The term telescope is empty, and All type weakening keeps it empty. No unsafe unshifted open-context generalization is used.

`target_inhabited` is an actual FiniteDerives certificate for I at identityCode. This witnesses the precise finite result type's nonemptiness. It does not assert FiniteDerives for the Raw-using tree or for t.

## Exact negative result

`application_S` and `application_K` display two root contractions from t a through K a ((K Omega) a) to a. Their Red composition is valid for every raw a, but is not universal strategy termination or a source-conversion proof t ~ I.

The inherited Step has exactly I, K, S root contractions and left/right compatible contexts. In `wrapper q`, the outer S has two arguments and K has one. Exhaustive constructor inversion excludes root contractions and all movement in the normal S/K constants. `wrapper_step` leaves exactly a Step inside q; `wrapper_red` inducts over the full reflexive-transitive relation, preserving the wrapper and a Red proof on q. `wrapper_normal` uses both required compatible right lifts. Thus `no_normal_reduct` applies the inherited Omega all-reduct theorem, not a finite cycle/census argument or a weak-head divergence claim.

`no_finite_source_representative` quantifies every u and every finite TypeCode C. It uses inherited finite_normal_form on u, composes the actual source Conv with source red_conv, applies conv_join, and uses normal_red to identify the common reduct. This would give a normal reduct of t, contradicting the wrapper theorem. The source Conv is the inherited equivalence closure of Step, not PER equivalence or target-language conversion. `boundary_control` joins the positive and negative statements for the same p and t.

## Independent discriminators

`IndependentBoundaryControls.lean` provides four small checks, without duplicating normalization or confluence:

- p is not the opaque atom(t) polynomial.
- Those two distinct polynomials nevertheless have equal evaluations in every environment.
- Normal(wrapper q) iff Normal(q), isolating the exact contextual obstruction.
- The older discarded term K I Omega has I as a normal reduct. Its known non-SN status therefore cannot substitute for this no-normal-reduct conclusion.

The first pair detects the important syntactic/evaluation distinction; the latter pair prevents confusing weak normalization with strong normalization or an unqualified operational divergence claim.

## Ownership and interpretation

The old Raw/K/S/application/All rules already admit this witness. The exact source reduction, Omega shape theorem, finite normalization and Church–Rosser machinery are inherited. P01Omega already owns Omega's finite source-representation obstruction; NormalisationAndNumerals owns discarded non-SN expansions in inhabited unary semantic Codes. The present result is an explicit boundary corollary/control from those rules, not a new calculus capability, historical-novelty certification, or refutation of an earlier full-normalization claim.

The boundary rules out source-Conv-preserving finite reification for all enlarged-judgment certificates even at the inhabited polymorphic identity result type. It leaves intact FiniteDerives normalization and all general-normalization exclusions. No absence of a PER-equivalent finite representative follows. The unapplied term is weak-head function-shaped, and its application can return a normal argument in the two displayed head contractions. No target reduction, canonical edit, publication, external contact, or empirical validation is claimed.

## Reproduction and evidence

`logs/` and `historical-sources/clean-replay/` retain the successful independent run. The exact historical helper is in `historical-scripts/compile-one-clean-replay.sh`. The current helper directs subsequent output to `reproduction-logs/` and `reproduction-sources/`; it does not overwrite acceptance evidence. For a fresh independent reproduction, copy only manifest-listed `.lean` sources into a clean package-local source directory before following `dependency-order.txt`; never import author or prior review objects. Set TOOLCHAIN_ENV explicitly and coordinate a serial lane before running.
