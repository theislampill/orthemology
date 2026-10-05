# Checked mathematical scope and limits

3 October 2026 UTC. Isolated mathematical verification for the foundation-facing comparison. This is not a publication, canonical change, philosophical closure, or bootstrap validation.

## Result

The final Lean 4.19.0 replay passed all four modules and the readback module. The 51 requested theorem dependency readbacks contain only the standard axioms `propext`, `Classical.choice`, and `Quot.sound`; one of the 51 has no axiom dependency. No custom axioms, admitted proof holes, heartbeat increases, or extra compiler lanes were used.

### Checked universally, without topology

`LawCompletionCore.lean` defines finite-depth survival, compatible infinite backward sequences, exact uniqueness (including existence), pointwise attraction, and uniform attraction. It proves:

- Every coordinate of every compatible backward sequence survives every finite depth.
- Finite-depth survival is forward invariant.
- Singleton survival gives a fixed point, the unique fixed point, and exactly one infinite backward sequence.
- Exact uniqueness of a backward sequence makes that sequence constant at a fixed point.
- Uniform attraction to a fixed point implies singleton survival, without compactness or continuity.
- The epsilon-based uniform-attraction definition is equivalent to Mathlib's `TendstoUniformly`; it implies pointwise attraction.

These quantify over arbitrary types, maps, sequences, and natural-number depths. They do not enumerate a finite test horizon.

### Checked Control A

`LawCompletionCounterexample.lean` uses `State := Option Nat`, with `none` representing e and `some n` representing n. Its distance is explicitly 0 for equal states and 1 otherwise. The packaged theorem includes actual `CompleteSpace State` and `Infinite State` witnesses, boundedness of the entire space, and continuity of the actual self-map.

The full iterate formula and full range formula are checked for every natural-number depth. The surviving set is exactly {e}; the only backward sequence is the all-e sequence. Every natural starting state remains at distance 1 from e at every time, so its orbit does not converge to e. Failure is also checked from `some 1`, which belongs to the map's image. No fixed point can be substituted to recover universal pointwise attraction.

### Checked Control B

`LawCompletionBranches.lean` uses e, r, and branch points `branch n k hk` with `k ≤ n`. Branch n has n+1 points indexed 0 through n. This is an exact reindexing of the ordinary derivation's positive-indexed point (n+1,k+1); no extra invalid branch states are introduced. Proof fields do not introduce distinct states.

The same explicit complete bounded 0/1 metric and actual continuity witnesses are checked. The type is infinite. An arbitrary depth-t predecessor of branch point k forces `k+t ≤ n`, which excludes each finite branch point from survival. The exact surviving set is {e,r}; the only compatible backward sequence is all-e. Every forward orbit reaches e after finitely many steps, so pointwise attraction holds, while singleton survival does not.

### Checked compact continuous repair

`LawCompletionCompact.lean` proves for an arbitrary compact metric space and continuous self-map:

- Every finite-depth survivor has a surviving predecessor, using nested nonempty closed compact predecessor sets.
- Classical predecessor choice produces a compatible infinite backward sequence starting at each survivor. Thus finite-depth survivors equal starts of compatible realizations.
- A singleton intersection of iterate ranges forces uniform attraction, using nested closed compact sets of points outside an epsilon-ball.
- Singleton survival, exact uniqueness of a backward sequence, and uniform attraction to a fixed point are equivalent. The packaged theorem explicitly retains the requested nonempty-space premise and uses the standard `TendstoUniformly` conclusion.

Compactness and continuity are actual hypotheses. They are not replaced by an assumption that infinite predecessor paths or uniform shrinkage already exist. Classical choice is disclosed; the theorem is not a constructive algorithm for computing predecessors.

## Not mechanised here

- Control C: the compact homeomorphism on {0} union {±1/n}; its pointwise-convergence/unique-fixed-point failure to imply uniqueness remains an ordinary mathematical argument in the reviewer’s correction.
- Eventual-compactness extension.
- Strict-contraction sufficiency and the unbounded x/2 control.
- Hausdorff/supremum reformulations beyond the checked equivalence with standard uniform convergence.
- Interpretation of the paper's declared state space versus already-realized values, modal adequacy, metaphysical possibility, existential explanation, or conclusions about the author's philosophical position.

Do not describe the whole correction or the whole source comparison as Lean-verified. The checked results are precisely the modules and theorem interfaces above.

## Source/domain boundary

The sole ordinary mathematical design input is the central independent review file `tranche10/reviews/existential-completion/INVERSE_LIMIT_AND_CONVERGENCE_CORRECTION.md`; its identity at admission is in `DERIVATION_INPUT.sha256`. The source owner, source locators, interpretive comparison, and exposition budget remain centralized there and in its referenced review material. This packet introduces no new historical/source exposition. Applying these theorems to the displayed general metric-domain claims still requires the stated declared-domain qualification. Restricting a map's state space to already admitted complete realizations is a different target.

## Validation and trusted boundary

Run `bash validate.sh <new-log-directory-name>` from this directory or invoke it by its full path. It rebuilds each module sequentially, then records theorem/axiom readbacks and a source-bound JSON report. Each invocation uses `timeout 180 lean -j1`; default heartbeat settings are unchanged. The final replay is in `logs/final-validation-20261003T1223Z/`:

- Core: 4.415 seconds, exit 0
- Compact: 4.298 seconds, exit 0
- Control A: 4.600 seconds, exit 0
- Control B: 4.458 seconds, exit 0
- All 51 dependency readbacks passed the whitelist and completeness checks

The environment file records Lean's exact version/commit, paths, and SHA-256 identities for the environment script, Lean executable, Mathlib umbrella source, toolchain pin, and dependency manifest. This uses the existing trusted Lean/Mathlib installation. It neither bootstraps nor independently verifies that installation. Earlier development diagnostics are retained under `logs/`; only the named final replay is bound to the final source hashes. The earliest log records the unavailable `/usr/bin/time` utility before any compiler ran; subsequent measurements use the shell's built-in timing without installation.

Independent review is requested, not represented as already passed.
