# Open-term full-PER standardness and the retained compiler

10 October 2026. **The literal `HasE [] c3 (W q)` remains OPEN.** This pass establishes a new-to-project, kernel-checked model-class result. It does not claim a new mathematical discovery, a derivation of the literal target, a full HasE soundness theorem, or a general noninhabitation result.

## Result first

In the explicitly defined carrier of finite **open** SKI terms, including the source's inert `zero` and `one` markers, let conversion be compatible SKI conversion. Interpret the Church type by the intersection of its ordinary extensional arrow PER over **all conversion-saturated PERs** on that carrier.

Three facts are now checked in Lean 4.19.0:

1. A term belongs to this Church interpretation **if and only if** there exists a single finite count k such that, for every raw f and a, `n f a` converts to the k-fold iteration of f on a.
2. For the formula mirror of the unchanged pair-state compiler, `n f a` converts to `(q n) f a` whenever n belongs to this interpretation.
3. The interpreter's identity combinator and that compiler mirror are related at the extensional arrow PER `N → N`, including arbitrary **related** Church inputs, not just the same input on both sides.

Every finite successor numeral inhabits the Church interpretation. The test is therefore not an empty-domain argument. The forward standardness proof does not assume heterogeneous relational parametricity, numerical induction for n, normalization of arbitrary n, or the scalar-fusion property it establishes.

This removes the unavailable HRR paper as a dependency for **this direct route and this particular class**. It does not retrospectively supply a reading of HRR, recover its theorem, or extend the result to every PER model.

## The discriminating operation

The tested object is one coherent erased application algebra. A semantic term n is an arbitrary finite open syntax tree, so it has finite variable support. Choose two fresh generators u and v above that support. Define the orbit PER by

    R(x,y) iff x converts to y and x converts to u^k v for some k.

The definition allows two iteration counts to have convertible representatives; no distinctness-of-counts or confluence premise is hidden in the construction. The source proves symmetry, transitivity and conversion saturation of R.

The generator v belongs to R, and u is an R-endomorphism. Church membership at this one PER therefore gives a count k with

    n u v converts to u^k v.

Now simultaneously substitute arbitrary f for u and a for v. Compatible SKI conversion is stable under this substitution. Freshness ensures that n itself is fixed by the substitution, even when n has other free generators. This yields

    for all f,a: n f a converts to f^k a.

The converse is independently proved by induction on the finite count, preservation of a PER by related endomorphisms, and conversion saturation. The result is an exact membership characterization of this particular Church domain.

The orbit step is genuinely stronger than the failed strict-iterator probes in the preceding pass. It excludes every nonuniform finite open-term candidate in the tested full-PER interpretation at once. No strict successor/zero iterator was retried.

## Exact compiler calculation

The second file defines a separate polynomial syntax P and directly mirrors the retained source formulas for the whole-subterm K-priority bracket abstraction, Church zero, successor, pair/projections, diagonal step and compiled body. It does not use eta contraction or normalize the body before abstraction.

The mirror proves the bracket application equation for arbitrary valuations, then the actual elementary equations:

    delta(pair a b) converts to pair(succ a)(succ b)
    q n converts to snd(n delta z0)
    z0 = pair(zero)(zero).

Its state invariant is proved for every finite k:

    delta^k z0 converts to pair(succ^k zero)(succ^k zero).

Standardness of n thus makes `q n` convert to the successor numeral at its uniform count. The independently checked scalar behavior of that numeral gives the desired applied scalar conversion. This is not a claim that n itself converts to the numeral without application, or that q converts to I as a bare raw term.

The third file packages ordinary arrow PERs and their Church intersection. It lifts scalar conversion to

    (arrowPER churchPER churchPER).rel I q.

This last statement handles n and m related at Church N. It uses the relation between `n f a` and `m g b`, then the scalar conversion on m. The stronger relation is useful for a conditional whole-model transport; it is not merely a list of numeral tests.

## Source binding and availability

The starting local directory contained only `ExtensionalRepairSyntax.lean`, `ScalarFusionCore.lean` and `LiteralScalarFusion.lean`, plus the earlier report and bindings. Required imports including `IntensionalIdentityBridge`, `EffectiveObserver`, `ScalarFusionReverse`, `UnaryCurrentIdentityBoundary` and `ClosedProofCanonicalisation` were initially absent. `INITIAL_AVAILABILITY.json` records the exact read-only scan.

Five useful source files were subsequently retrieved read-only from `theislampill/orthemology`, commit `7efc6217c090b92d65f2c4cb8b011c18eb96bf7c`. Their source-store SHA-256 digests and Git blob digests are independently checked by `check_bindings.py` and recorded in `SOURCE_BINDINGS.json` and `validation/SOURCE_CHECK.json`.

Fourteen relevant definition right-hand sides in the compiler mirror match the pinned definitions after whitespace removal and the explicit syntax-name change `Poly → P`. The independent reviewer also inspected their correspondence. The source's `redundant_closed_exact` explicitly identifies the original `redundantExpr.closed` with `abstract literalPairStateBody`; that source theorem was inspected, **not imported and replayed** here.

The exact `PolyConvPlus` has its seven SKI/congruence constructors plus the atom/application packing bridge. Under the ordinary raw evaluation used here, the bridge is reflexive: a compound raw atom and its exposed application evaluate to the same term. The pinned `polyConvPlus_sound` states this directly. No new raw equation was added to the source or the test.

The acquired sources are not a complete dependency closure. No full inherited HasE build is claimed. The new proofs deliberately import only Init and the two preceding isolated files. Formula correspondence and the ordinary source-to-mirror interpretation are separate from a kernel-imported theorem equating this q with the original typed q.

## Precise model-class boundary

The unconditional new kernel claims concern the newly defined open-term reduct, its full saturated-PER Church interpretation and its compiler formula mirror.

A conditional whole-HasE conclusion follows only for a proposed model whose:

- erased applicative reduct and conversion interpretation transport to this finite open-term construction;
- Church interpretation uses all these saturated PERs, or at least the fresh orbit required for each candidate n;
- compiler is interpreted by the inspected unchanged formulas; and
- identity interpretation represents the relevant type-PER equality, as in the singleton-I represented identity convention.

Such a model cannot separate the retained endpoints by the N-to-N PER equality, and with the stated represented identity it cannot make their identity empty. This is a precise **separator-class exclusion**. It is not a construction or certification of a model validating all twenty HasE rules.

In particular, no new fundamental theorem has been supplied for dependent J, proof-coordinate coherence, proofErase, piExt/allExt or the impredicative universe. A model with a different identity interpretation is not excluded merely by the relational endpoint result. Nor is existence of an appropriate whole-HasE extension asserted.

Fullness matters. Closure under the source's finite type constructors does not by itself show that every orbit PER used in the proof occurs in a syntax-generated Henkin universe. Dropping that premise would invalidate the forward argument. Closed-term applicative algebras without fresh generators, partial combinatory algebras with different elements, semantic completions and arbitrary domain models are not covered by this proof.

## Inherited and new claims

Inherited, unchanged: the original compiler and target; the reported four-way equivalence and fixed-witness construction; the warning that raw proof normalization does not authorize introduction inversion; and the preceding failed candidate tests.

Newly checked here: the orbit-PER test, freshness/substitution argument, exact Church-domain characterization for the stated reduct, the bracket/compiler formula mirror and scalar-fusion calculation, and the typed I/q endpoint relation in that reduct.

Not established: a witness of `HasE [] c3 (W q)`; its negation; a syntax-directed decision procedure; uniqueness or computable extraction of the count; general semantic completeness; a universal standardness theorem; or any metaphysical/actual-world conclusion.

The earlier HRR author PDF still returned a cache miss in this pass. The suggested thesis URL returned 404. Neither is a premise of the new proofs, and the misleading ResearchGate text was not used as the target paper. These access results did not stop the direct formal operation.

## Replay

Use the retained Lean 4.19.0 executable (commit `6caaee842e94`). From this directory, run `bash replay.sh` with `LEAN_BIN` set if it is not at the recorded neighboring toolchain path.

The principal theorem names are `church_standard`, `one_fresh_orbit_suffices`, `church_iff_uniformIter`, `church_scalar_fusion`, `successorNumeral_church` and `identity_q_related`. Final replay is in `validation/FINAL_REPLAY.json` and `validation/FINAL_REPLAY.log`. The only reported logical axioms are `propext` and, for the compiler mirror's well-founded definition/proof infrastructure, `Quot.sound`; there are no custom axioms or admitted proofs.
