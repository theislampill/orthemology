# Independent review of the uniform law completion formalisation

3 October 2026 UTC.

## Verdict and independence

**Accept the checked uniform mathematical scope.** Fresh isolated compilation, exact definition and theorem inspection, axiom readbacks, and independent control proofs found no target or proof-scope defect.

I authored the ordinary mathematical correction used as the implementation's design input. I did not author the four Lean implementation modules. This is therefore independent implementation, verification, and scope review; it is not an independent discovery of my own mathematical argument and not external specialist validation.

Admitted packet: `tranche10/research/law-completion-correction/ARTIFACT_MANIFEST.json`, SHA-256 `5d7b52d653a818641b2fd818a95fc3a13a159dd89cd75bb597435b818f0a55d4`. All 33 manifest entries matched their hashes. The original packet and manifest were not modified.

## Fresh validation

Only the four `.lean` implementation sources were copied into this separate review directory. No author-generated `.olean` was copied or used. The review source directory was the first and only task-source directory on `LEAN_PATH`; all other paths were the existing trusted Lean/Mathlib dependencies.

Sequential fresh builds used `timeout 180 lean -j1` with default heartbeat and recursion limits:

- Core: exit 0, 6.390 seconds
- Compact: exit 0, 4.922 seconds
- Counterexample A: exit 0, 5.343 seconds
- Finite branches B: exit 0, 5.066 seconds
- Author's theorem/definition readback: exit 0
- Final independent reviewer controls: exit 0, 5.515 seconds

The 51 original axiom readbacks were complete: 50 used only `propext`, `Classical.choice`, and `Quot.sound`; one used no axioms. All five additional reviewer-control readbacks used only those same standard axioms. No custom axiom, admitted proof hole, unsafe/native proof bypass, or resource-limit increase occurs in the inspected implementation sources. This trusts the installed Lean kernel and Mathlib dependency build; it does not independently bootstrap them.

Exact environment, source and log identities are retained in `INPUT_IDENTITIES.sha256`, `logs/environment.txt`, and `REVIEW_VALIDATION.json`. An initial reviewer-control linter warning concerned a bound variable resembling a constructor. The variable was renamed and the final replay was clean; both logs are retained.

## Actual interfaces and mathematical fidelity

`Survives f x` quantifies over every natural-number depth and permits a different predecessor witness at each depth. `Backward f b` instead requires one function on all natural numbers satisfying every compatibility equation. `UniqueBackward` uses exact existence-and-uniqueness of that whole function, not an at-most-one property or finite-prefix uniqueness.

`UniformAttraction` puts the existential cutoff before both the future-time and starting-state quantifiers. It is checked equivalent to Mathlib's `TendstoUniformly`. `PointwiseAttraction` quantifies separately over starting states. The distinction driving the ordinary argument is thus preserved in the formal signatures.

The compact repair retains arbitrary `MetricSpace X`, `CompactSpace X`, a total self-map, and its actual `Continuous f` hypothesis. Its predecessor proof uses nested closed compact fibers and earns a surviving predecessor. It does not assume that an arbitrary predecessor survives or assume the desired infinite path as a hypothesis. Classical choice then builds a compatible infinite sequence. A second compactness proof earns uniform shrinkage. The central theorem retains the requested nonempty-space premise and states the equivalence using standard uniform convergence.

Control A uses an explicit 0/1 metric on an infinite state type, with actual completeness, boundedness, and continuity proofs. Its full range and iterate formulas quantify over arbitrary natural-number depths. The failure of convergence also holds from a state in the map's image.

Control B likewise has an explicit complete bounded 0/1 metric and actual continuity. Branch n contains n+1 states indexed from 0 to n; this exactly reindexes the ordinary positive-index convention. Its proof-valued bound field does not create extra distinguishable states. The arbitrary-depth capacity theorem excludes finite branch points, while the exact survival and backward-realization theorems separate {e,r} from the unique all-e realization. Every forward orbit is proved eventually fixed.

## Independent controls

`ReviewerControls.lean` adds five checked statements:

1. Control A refutes replacing compactness by complete bounded continuity in the singleton-survival-to-uniform-attraction implication.
2. Control B refutes the corresponding unique-realization-to-singleton-survival implication without the compact bridge.
3. The natural-number successor map has no compatible infinite backward realization.
4. That successor map satisfies at-most-one vacuously but fails exact `UniqueBackward`; existence cannot be silently dropped.
5. A two-state constant map refutes the inference from a surviving image to survival of an arbitrary preimage.

These are representative assumption and inference controls, not a claim to have mechanically tested every possible hypothesis deletion.

## Limits that must remain explicit

The accepted packet does not mechanise Control C, eventual compactness, bounded strict-contraction sufficiency, the unbounded contraction control, or additional Hausdorff/supremum formulations. Those remain ordinary mathematical arguments.

The new nonuniform compact extension is a separate proposal and potential separate implementation. This acceptance does not extend to it. The uniform packet also does not mechanise source-domain interpretation, the completeness of Ω as a comparison class, explanatory adequacy, metaphysical possibility, existential production, or any original-source/necessary-participant conclusion.

No claim should describe the whole philosophical correction as Lean-verified. The precise formal results above are accepted, and the broader application boundaries remain unchanged.
