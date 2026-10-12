# Independent Lean review of exact reset continuation

9 October 2026 UTC. No blocking definition-faithfulness or proof-verification issue was found in the bound source. This review is not integration approval or T20 closure.

## Bound sources

- Ordinary theorem: constructive-t20-20261009/revocation-dependency/THEOREM.md, SHA-256 95a636b7eaa8a054657426caeeb569991f6e32ba5bc8f53639d2c919a812aa34.
- Main Lean source: ResetContinuation.lean, SHA-256 480520d76d4bef1f080bd4ef925e13840ab81efa4a6ead7cae533eb67166ec11.
- Author checks: Checks.lean, SHA-256 0c2cae60093a7716a30b28cad85faeca8ae7f989ed2652417dc4970e6fd6b9a2.
- Verify.lean, SHA-256 6ad4053e42149aeff9303d06381cceff5661aea30c5ea3fbec80d2a5a0c829e6.

The complete main source and check modules were read before execution. A clean copy was made under this review directory; author files were not edited. The package manifest contains no external packages. The only library import of the main source is Std.

## Definition faithfulness

State I is the complete function space I → Bool. It is not an arbitrary finite sample or a restricted set of admitted valuations. The general theorem assumes an exhaustive finite coordinate list; the final theorem specializes uniformly to Fin n for every natural n. That specialization represents exactly the full finite Boolean product in the ordinary theorem, including dimension zero.

Essential is semantic single-coordinate dependence. Although its definition does not separately assert a difference at the distinguished coordinate, the separate witness_coordinate_diff lemma proves that consequence from the different outputs and equality at all other coordinates. No syntactic variable-occurrence surrogate is substituted.

Action includes every reset of every coordinate to both Boolean values, plus every supplied coupled-action label. Step and run are total; continuation equivalence quantifies over all finite lists of these same labels, including the empty list. No admissibility restriction, reachability restriction, or hidden permission guard weakens the observation contract. T is an arbitrary total coupled transition map. The formal theorem even allows an arbitrary label type A; finite action catalogues in the source theorem are covered as a special case.

Closure is independently defined by output-essential coordinates and backward semantic transition dependencies. It does not refer to continuation equivalence. Stage matches the source's iterative recurrence. Both closure_iff_stage and closure_least are proved, so the relevant dependency set is not defined by the desired behavioral conclusion. There is no Reach or Stable premise that assumes the characterization.

## Proof and coarseness review

The sufficiency direction proves that finite-coordinate functions are determined by their essential coordinates, then establishes preservation under resets and arbitrary coupled actions, and finally inducts over every action word.

The necessity direction explicitly constructs reset contexts. Boolean pair matching exposes an essentiality witness from every pair differing at the relevant coordinate, including arbitrary differences elsewhere. The induction over Closure composes the exposing prefix, the coupled action, and a distinguishing suffix. This is the stronger induction required by the ordinary proof.

Summary states must decode the actual output and update under every named action on every encoded state. Equality of summaries is proved to imply equality after all common words. The characterization then proves every_summary_refines_projection. ProjectionState, project, fill, project_fill, and projection_summary establish a realizing projection summary. summary_factors_projection supplies a recovery function on all summary values, including unreachable values. This faithfully proves abstract coarseness rather than merely asserting it in a definition.

The independent audit module also compiled an explicitly typed restatement: equality of h after all finite action words is equivalent to coordinate agreement on the union of all source stages, uniformly for every Fin n state product.

## Fresh independent verification

Toolchain used: Lean 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release. The lean executable SHA-256 is 92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023. This is the provided release toolchain used by the author; it was not independently rebuilt by this review.

The independent copy had no copied build artifacts. LEAN_PATH, LEAN_SRC_PATH, and LEAN_SYSROOT overrides were cleared. The following fresh commands all exited zero:

1. lean -DwarningAsError=true ResetContinuation.lean
2. lake build ResetContinuation Checks Verify
3. lake env lean -DwarningAsError=true IndependentAudit.lean

Logs are retained under logs/. The fresh build compiled all three author modules rather than reusing their build directory.

The main characterization, projection summary, refinement, recovery factorization, and Fin n specialization use only the standard axioms propext, Classical.choice, and Quot.sound. The expanded audit also inspected the relevant helper theorem dependencies. closure_iff_stage, closure_least, summary_eq_continuation, the guarded control, and constant-output control report no axioms. No sorryAx or added domain axiom appears in these receipts. Static inspection found no sorry, admit, new axiom declaration, unsafe, partial, extern, implemented_by, or native_decide in the main source. The finite Boolean controls use ordinary kernel-checked decide, not native_decide.

## Explicit formalization ceiling

Verified here:

- The full general continuation-equivalence iff coordinate-agreement theorem.
- The actual iterative-stage union and least backward closure.
- The abstract projection summary, its correctness, summary refinement, and recovery factorization.
- Uniform specialization to all natural finite dimensions and the stated edge/guard controls.

Not formalized by this package:

- The exact 2^|I*| class count or fixed-width bit arithmetic.
- A finite stabilization bound or distinguishing-word length bounds.
- The positive-certificate support/cost antichain specialization.
- The source-specific residual-frontier or certificate-catalogue claims.

The zero-fill summary and recovery constructions are explicitly noncomputable and use classical reasoning. Their mathematical existence and correctness are verified; this is not an extracted executable dependency-discovery procedure or a complexity result. The proof does not establish actual source-status meanings, authorization to reset trust, authenticated evidence semantics, scientific truth, human warrant, or correctness of a deployed implementation. Kernel checking verifies the supplied conditional mathematical model and proof under the listed foundations; it does not validate those application bridges.
