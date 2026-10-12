# Independent review: finite full Raw obstruction

Verdict: PASS for the exact stated algebraic and semantic claims. No blocking mathematical or source-bridge issue found. This review does not integrate the result or close any programme target.

## Frozen object

The author packet is `hase-finite-raw-obstruction-20261010`, manifest SHA-256 `bbc40b7307ce0ef5300999bb2bb28bbc333a779233b22793fe8dcd4a1034603e`. Its eight manifest-bound files and manifest were copied byte-for-byte to `frozen/` before replay. The original directory and all predecessor sources/objects are read-only inputs. `REVIEW_INPUTS.json` records the exact file hashes.

## Proof and source audit

1. The abstract proof is correct. In a total K-algebra, `x ↦ K·x` is injective because one more application to K recovers x. On a finite carrier it is surjective, so K has a preimage a. Then `K·x=(K·a)·x=a` for all x, and injectivity collapses every pair. K supplies inhabitation, strengthening subsingleton to exactly one element. No S or I reduction, full function-space assumption, pairing, extensionality or impredicativity is needed.
2. `SourceRaw.lean` uses the actual retained `ExtensionalRepairSyntax.HasE`, `Poly`, `Term`, and `PolyConvPlus` declarations. The two-variable telescope is literally `[raw,raw]`; both variable lookups, formation premises, rawAtom and both rawApp constructors are supplied. The source identity with witness I is valid and optional. Both the original `P01DF.PolyConv.k` judgement and its direct `PolyConvPlus.k` counterpart are checked; no atom/application bridge is needed for the no-go.
3. The semantic premise is appropriately explicit and conditional. Variables range over every A-value, the interpretation is compositional with total A-valued application, and actual Raw-typed conversion in this telescope is respected as equality for every assignment. Instantiating the assignment at arbitrary x,y yields the global K law. This is not derived from mere unary membership soundness, and it is not a proof about every conceivable semantic notion.
4. `RawImages.lean` uses original closed Term syntax and original Conv directly. Surjectivity allows arbitrary carrier values to be represented by closed terms; composition plus the literal `Step.k` supplies the K law. The quotient construction retains both full application congruence and inclusion of conversion. The conclusion that a finite such equivalence is universal follows by quotient exactness.
5. The dependency audit's distinction is correct: declaration bodies demonstrate which rules a proof uses, while full axiom closure checks logical trust. The latter may include mutual grammar constructor dependencies through theorem signatures. Its assertions should not be read as claiming that the full signature dependency closure excludes all unused grammar constructors.
6. The author documentation correctly limits the result. It is an elementary classical fact, not a historical-novelty claim, not HasE noninhabitation, and not a decision of universal W. Finite typed data and bounded/partial/restricted observation methods remain possible. Singleton Raw alone does not collapse every type-indexed carrier without a further embedding or comparable premise.

## Independent executable additions

`IndependentControls.lean` contains four useful checks beyond rerunning the author proof.

- `finite_exact_summary_constant`: if A is finite, `q : Term → A` preserves every original raw application through a binary transition δ and respects original Conv as equality, then q is constant. This requires no surjectivity onto all A. The proof builds a ClosedRawImage on the reachable subtype `{a | ∃t, q t=a}`. Unreachable summary states therefore need no global K law. This is a direct exact-composition transport of the reviewed obstruction, not an independent novelty claim or a result about computational complexity.
- `finite_partial_K_subsingleton`: even an Option-valued partial application collapses a finite carrier when `K·x` is defined for every x and the resulting encoded constant applies to every y with result x. The proof directly repeats the injectivity/surjectivity argument for the encoded constants. Merely labeling the ambient operation partial is consequently insufficient under that global K-slice premise.
- A constant false-valued Term summary into Bool with OR as binary transition is compositional and conversion-respecting, yet is not surjective and its unreachable true value prevents the whole Bool carrier from satisfying K. This witnesses why the author's ClosedRawImage surjectivity premise cannot simply be dropped while still concluding the entire target carrier is a singleton; the reachable-image conclusion remains valid.
- The Boolean syntax-shape summary distinguishes atoms from applications and composes via the constant-true binary transition, but fails conversion already at the source K redex. This witnesses why exact application composition alone does not trigger the no-go.

These controls do not refute finite summaries for restricted typed contexts, bounded horizons, selected observations, non-compositional predicates, or genuine partial fragments whose K-slice contract is weaker.

## Replay and preservation

Run `python3 hase-finite-raw-review-20261010/replay.py --workspace /path/to/workspace`. An optional `--output` must name a new directory. Review sources and replay outputs are kept in separate directories.

The harness verifies the author freeze, original current bytes, source and object bindings, standard Lean binary, and the review manifest before and after compilation. It independently matches all 30 retained source/object pairs to the predecessor prerequisite trust-zero build receipt. It reuses 526 author-bound external source/object pairs plus eight additional external pairs required by the independent finite-subtype proof. These external objects are hash-bound, not freshly rebuilt. Core Lean/Init/Std libraries are inherited from the retained official Lean 4.19.0 toolchain.

Only the four frozen author modules and the independent control module are compiled, all with `--trust=0`, into a fresh separate output directory. The harness rejects warnings, errors, admitted-proof/unsafe/native escapes in these new sources, and axioms outside `propext`, `Classical.choice`, and `Quot.sound`. The full logs, exact commands, module/object hashes, input hash checks and terminal result are in the output's `REPLAY.json` and `REPLAY.log`.

Scope: isolated reviewed mathematical evidence and reviewer controls only. No original grammar changes, predecessor edits, repository integration, publication, provenance claim, universal-W solution, or audit-closure authority.
