# Full-polynomial functional: additive intermediate evidence

10 October 2026 UTC. This archive preserves two separately reviewed levels of
evidence for one normalized bivariate functional and its positive separating
polynomial. It is an intermediate mathematical artifact. T20 remains active;
this is not integration, closure, a rank-classification certificate, or a
field-novelty claim.

## Result and evidence levels

Let F = 1 + x^4 y^2 + x^2 y^4 − x^2 y^2. The construction gives a real-linear
functional Λ on the whole algebra R[x,y] with Λ(1)=1, Λ(p²)>0 for every nonzero
real polynomial p, F(x,y)≥3/4 at every real point, and Λ(F)=−1.

1. **Ordinary construction and independent mathematical review.** The explicit
   exceptional monomial ordering and recursive Schur extension define compatible
   finite Gram matrices, one infinite moment sequence, and the full functional.
   The ordinary proof also establishes computable dyadic moments, the explicit
   inverse-index algorithm, determinant invariant 4, and the resulting absence
   of a representing positive Borel measure. The author’s 37,588 exact checks
   and independent determinant-based 44,637 checks are bounded diagnostics;
   neither count supplies the universal proof. The ordinary independent verdict
   is PASS_UNIVERSAL_MATHEMATICAL_CONSTRUCTION_WITH_BOUNDED_REPLAYS.
2. **New full-functional algebraic Lean proof and independent review.** Seven
   sources construct the actual real-linear map on MvPolynomial (Fin 2) ℝ and
   prove the above statement without an assumed functional, positivity premise,
   or degree cutoff. The author recorded 22 standard-axiom dependency audits
   and three false controls. The final independent verdict is
   PASS_INDEPENDENT_FULL_FUNCTIONAL_LEAN_REVIEW, with seven fresh trust-zero
   builds, four positive-control audits, and seven rejected false controls.
   Its explicit theorem binder rules out hidden-premise/type drift, and its
   arbitrary-N cutoff theorem proves every zero-tail finite-degree truncation
   kills a nonzero square. The observed import closure has 2,775 modules:
   seven local sources plus 2,768 retained external source/object pairs.

The earlier scalar-only Lean report remains byte-for-byte historical evidence.
Its statement that it had no full-functional Lean proof describes that earlier
packet. The new full-functional review is the additive upgrade; no historical
scope statement has been silently rewritten.

## Important boundaries

- The Lean enumeration inverse uses classical choice from a proved bijection;
  the real moment sequence and linear map are noncomputable Lean definitions.
  Executable/dyadic correspondence with the Python algorithm, the explicit
  inverse algorithm, and determinant 4 are not formalized in this Lean packet.
- `not_pointwise_positive` formally proves the algebraic obstruction to positivity
  on all pointwise nonnegative polynomials. No Lean MeasureTheory integral or
  positive-Borel-measure representation theorem is claimed. The integration
  argument belongs to the separately reviewed ordinary proof.
- This bivariate construction does not extend or repair the earlier failed
  finite ternary truncated datum. Its higher-degree failure remains unchanged.
  The ordinary rank-substitution discussion is retained at its stated scope;
  no new heat/diffusion, positive-direction, rank, or protected-state certificate
  is awarded by packaging.
- Imported Lean/Mathlib objects are retained prerequisites checked at trust zero.
  Hashing their source and object bytes binds that environment; it does not
  establish independently rebuilt source-to-object provenance. No baseline
  library is rebuilt or bundled, and no software is installed.
- All proof and review files, logs, receipts, and local historical `.olean` files
  are exact copies. Local historical objects are evidence only and never enter
  the replay import path. Object bytes can vary with compilation context; see
  HISTORICAL_OBJECT_NOTE.json for the old scalar receipt/current-object mismatch.
- Preservation, compilation, finite tests, and guard tests do not count as new
  independent mathematical research or research-time credit.

## Read first

- evidence/full-polynomial-moment-countermodel-20261010/PROOF.md
- evidence/full-polynomial-moment-independent-review-20261010/REVIEW.md
- evidence/full-functional-lean-20261010/RESULT.md
- evidence/full-functional-lean-20261010/Countermodel.lean
- evidence/full-functional-lean-independent-review-20261010/REVIEW.md
- evidence/full-functional-lean-independent-review-20261010/controls/PositiveChecks.lean

COPY_MANIFEST.json binds exact original-to-copy bytes. ACCEPTANCE_BINDINGS.json
binds the four author/reviewer freezes. MANIFEST.json covers every archive payload
file except itself. Historical Python drivers remain unchanged for provenance;
they include original workspace paths and are not the portable entrypoint.

## Reproduce from a fresh extraction

Required: CPython 3.12.14 and the exact retained Lean 4.19.0 distribution and
Mathlib/peer package objects and sources identified in prerequisites/. Use the
version actually pinned in RUNTIME_PINS.json if its value differs from this
summary. There is no automatic retrieval, baseline build, or fallback to
unverified dependency bytes. A package commit alone is insufficient: its
selected object hashes must also match. The toolchain executable and its three
Lean shared libraries are hash-bound; ordinary system C runtime details are
recorded rather than fully bundled or certified.

Run from any directory (replace the two external paths with your retained roots):

    python3 /path/to/extracted/T20_Full_Polynomial_Functional_Intermediate_20261010/replay.py \
      --lean-home /path/to/lean-4.19.0-linux \
      --packages-dir /path/to/retained/.lake/packages \
      --output-dir /path/to/new-replay-output

The output directory must not exist and must be separate from this immutable
packet and both external roots. Missing or mismatched prerequisites stop before
any proof or exact-control execution. The wrapper verifies the packet and
historical freezes, checks dependency hashes, creates fresh local proof objects,
compiles the independent semantic and historical availability probes, rejects
3+7+2 mathematical controls, and reruns the unchanged ordinary exact programs.
It verifies direct and actual transitive imports, then rechecks packet and
external bytes. All logs and new receipts go to the output directory.

Only standard Lean axioms propext, Classical.choice, and Quot.sound are accepted
in the target audit outputs. No new axiom, sorry/admit, native_decide, or unsafe
production source is accepted. The explicit all-polynomial theorem and its
independent controls, rather than test counts, provide the formal evidence.

To test wrapper failure behavior, use the same options with `test_guards.py` and
a different new output directory. Nine guard cases cover absent prerequisites,
missing files, corruption, wrong external digest, disabled Python assertions,
stale output, and unsafe output placement. These are packaging checks only.

preservation/ contains the pre-seal replay and guard receipts/logs and original
byte-integrity inventory. A final fresh-extraction replay is recorded in the
sibling PRESERVATION_RECEIPT.json and SEAL.json supplied with the archive. The
archive’s own SHA-256 is necessarily outside the archive to avoid self-reference.
