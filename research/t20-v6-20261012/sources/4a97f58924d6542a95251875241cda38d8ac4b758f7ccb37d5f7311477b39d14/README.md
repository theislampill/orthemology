# Fresh kernel verification: exact reset continuation core

9 October 2026 UTC.

## Result and status

This standalone Lean 4.19.0 package proves the general exact backward-dependency characterization and the coarsest deterministic-summary property for every full finite Boolean product. It does not merely check finitely many examples. It does not define dependency closure to mean behavioral equivalence: the two are defined independently, and both implications are proved.

The main source is `ResetContinuation.lean`. It has no `sorry`, admitted proof, custom axiom declaration, unsafe definition, or external package dependency. Lean's reported foundations for the main results are the standard `propext`, `Classical.choice`, and `Quot.sound`. The stage-union correspondence itself has no axiom dependencies. This is fresh kernel verification of the specified mathematical result; it is not evidence of scientific novelty, source truth, metaphysical possibility, human warrant, or permission to integrate with a protected repository.

## General theorem

For any natural dimension n, any output type O and map h : (Fin n → Bool) → O, and any family of total coupled maps T indexed by an arbitrary type A, include every independent set-coordinate-to-false/set-coordinate-to-true action in the alphabet. All full product states and all finite action words are admitted, and compared states receive the same labels.

Define essentiality using two full states equal away from one coordinate and unequal in their f outputs. Start from essential output coordinates and close backwards under the essential dependencies of coupled-action component functions. The package proves:

1. Two states have the same output after every finite action word, including the empty word, if and only if they agree on that backward dependency closure.
2. The inductively generated closure is exactly the union of the source theorem's recursively defined finite stages, and it is the least set containing the initial essential coordinates and closed under those dependency edges.
3. Projection onto retained coordinates has a zero-fill decoder and a well-defined update for every named reset/coupled action. Every retained Boolean assignment is realized by a full state (`project_fill`).
4. Every deterministic summary with a correct output decoder and action updates refines that projection. In fact a recovery function from any such summary to the retained assignment exists on the entire summary type.

The coordinate-generic results take an explicit exhaustive finite list. This is a transparent finite-domain presentation, not an extra semantic assumption. `fin_continuation_iff_agreement` discharges it uniformly for every n with `List.ofFn id`. The action-index type need not be finite, a harmless strengthening of the finite coupled alphabet in the source theorem.

## Proof content

- `essential_determines`: sequentially replace every coordinate; nonessential replacements cannot change f, and essential replacements already agree.
- `contextWord_realizes`: a concrete finite word resets every coordinate except i to the witness context. Duplicates in the enumeration do not matter.
- `expose_essential`: any two Boolean states differing at i can be sent, by one common reset word, to an essentiality witness in either orientation. Booleanity is used explicitly in `bool_pair_match`.
- `closure_distinguishes`: the strengthened induction handles arbitrary differences in the surrounding coordinates. For a dependency edge, expose the component witness, apply the coupled action, and use the inductive distinguishing suffix.
- `agreement_continuation`: finite-word induction, using dependency closure for coupled actions and direct coordinate preservation for resets.
- `continuation_iff_agreement`: combines necessity and sufficiency.
- `projection_summary`, `every_summary_refines_projection`, `summary_factors_projection`: explicit summary and universal coarseness/factorization properties.

`fill`, `projection_summary`, and the recovery argument use classical reasoning because arbitrary output and action types are admitted, without supplied decision procedures. The zero-fill implementation is a mathematically specified operation, not a claim that this package computes the least dependency set from arbitrary black-box programs. An executable minimization algorithm would need its own decidability/representation contract.

## Exact assumptions and source map

The source document is `constructive-t20-20261009/revocation-dependency/THEOREM.md`, SHA-256 `95a636b7eaa8a054657426caeeb569991f6e32ba5bc8f53639d2c919a812aa34`. Its independent ordinary-proof review is `constructive-t20-reset-review-20261009/REVIEW.md`, SHA-256 `03f4349692c72952bd2fe5d84dba33c4193826e42859870061b07c3f87f4db6c`.

- Full Boolean product: `State I := I → Bool`; no admissible-state predicate or partial valuation is hidden.
- Finite coordinates: `coords` with `covers : ∀ i, i ∈ coords`; discharged by the Fin n corollary.
- Fixed output semantics: one arbitrary function `h`.
- Declared total coupled actions: one arbitrary family `T : A → State I → State I`.
- All independent resets: constructors `Action.reset i b` for every i and Bool b, interpreted by `reset`.
- Every common finite word: `ContinuationEq` quantifies over all lists of the same `Action I A` type.
- Observation initially and after words: `run [] x = x` and universal word quantification.
- Semantic rather than syntactic dependency: `Essential` quantifies over actual component values at witness states.
- Backward closure: `Closure` has only initial-essential and component-dependency constructors; `Stage` separately matches the displayed recursion.
- Continuation-complete summary: `Summary` explicitly supplies encode/decode/update and the two soundness equations. The universal result does not assume the summary already encodes the closure.

## Included checks

`Checks.lean` contains uniform theorem-signature checks, the arbitrary-dimension stage-union statement, the arbitrary-summary recovery statement, a proof that constant output has empty closure for every coupled family, and the zero-dimensional edge case. A small guard example is only a regression control: its guard coordinate is not an output-essential coordinate but is in backward closure, and one coupled action separates equal present outputs.

`verify_controls.py` mutates (a) the direction of backward propagation and (b) reset semantics to no-ops. Both must fail compilation. These are sensitivity controls, not proofs of the theorem and not successful builds of the altered statements. Logs from failed attempts/mutants can contain Lean's diagnostic placeholders for failed elaboration; the successful source and final axiom receipts do not.

## Reproduction

Put official Lean 4.19.0's `bin` directory on PATH and run `./verify.sh` in this directory. It cleans and rebuilds all three library targets, recompiles each source with warnings as errors, audits source tokens, runs both expected-rejection controls, and records source hashes.

The toolchain used here was downloaded from the official Lean repository release URL:
https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst

Observed version: Lean 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release. Downloaded archive SHA-256: `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`. This is a recorded downloaded-byte hash, not an independently authenticated upstream checksum. No global install was made. The large official toolchain archive and derived build cache are not part of this source package.

## Boundaries

Not formalized in this package: class-count arithmetic, fixed-width bit lower-bound arithmetic, finite stabilization/depth bounds, distinguishing-word length bounds, the positive-certificate antichain specialization, the CP23 source provenance comparison, or restricted/partial/correlated transition protocols. The exact coarsest summary result is proved; these further consequences and specializations are not being silently claimed from it.

No protected repository changes, publication, integration, audit-governor closure, or project-wide certification are performed by this package.
