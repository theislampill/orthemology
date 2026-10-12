# Control, restoration and epistemic-interface research return

This is a sealed, isolated research tranche against Orthemology commit `03e2604dfcef278b01c60d19b05370fcec4194b6`, tree `3d06e80277ce39286c94307e0f14b215bc94ed83`. It contains proofs, sharp countermodels, exact finite checkers and reproducible probes. It is not canonical adoption, a claim of actual-world model adequacy, or permission to take an intervention. The time-bound research programme continues outside this checkpoint; this package is being handed to a fresh synthesis reviewer.

## Main findings

- Ongoing hidden disturbance makes eventual actual target persistence different from eventual public knowledge of target status. Exact belief alone may be insufficient controller memory, and hidden coBüchi acceptance can require general ω-regular public monitoring.
- A bounded hidden-history bad-visit solver is implemented and independently checked. The general sure-winning finite-memory/parity construction is proved separately; the implementation does not claim general determinization, a complete unbounded solver, or impossibility from one failed bound.
- Almost-sure migration needs the correct probability laws and an executable information interface. Full initial/per-step couplings transfer restoration without conditioning away unfavourable paths. Private memory and public warrant must be distinguished, including when composing migrations.
- Hall deficits exactly quantify unconstrained coupling violations; licensed/incentive-constrained couplings have their own possibly larger optimum. Conditional summability governs adapted violations. A public certificate failure need not be physical target failure.
- A fixed hidden standard can be learnable almost surely only with unbounded memory, while no finite zero-error stopping declaration exists. Very high stationary accuracy can coexist with zero probability of eventual permanent correctness.
- Approximate relation exits need actual recovery. Summable departure hazards alone can leave restoration probability at 1/2; public recovery and complete reentry-law/memory contracts give a sound regenerative repair.
- The P14 return resolves its eight obligations with positive theorems and explicit obstructions. Its pre-existing sealed archive is carried unchanged, including scalarization strictness, policy-information and equilibrium-versus-convergence limits.

## Read in this order

1. `INTERFACE_MAP.json`: concise assumptions, conclusions, implementation boundaries and review status for every theorem family
2. `research.md`: hidden-history acceptance, bounded sure synthesis, Markov/end-component semantics, rank migration, provenance and repeated switching
3. `correlated_restoration.md`: Hall sharpness, adapted summability, constrained incentives and certificate/physical-state gaps
4. `hidden_standard_learning.md`: fixed hidden-standard memory and zero-error-declaration boundaries
5. `stochastic_refinement.md`: full distributional migration and infinite path-law gluing
6. `regenerative_refinement.md`: approximate departures, occupancy defects and lawful regenerative recovery
7. `private_interface_composition.md`: split private/public memory and compositional exact migration
8. `memory_accuracy_boundary.md`: stationary accuracy versus eventual correctness, including singular limits
9. `switching_innovation_threshold.md`: brief fresh-switching corollary with exact filtration, provenance and permission guards
10. `P14/P14_Completed_Research_Return.zip`: immutable P14 proofs, interface, tests, manifest and receipt

## Reproduce

Use Python 3.10 or newer; only the standard library is needed. Extract to a fresh directory. Verify the manifest and detached digest before running; replay writes new result/log files in that extracted working copy.

```sh
python verify_tranche.py
```

With the pinned repository locally available, also verify each inspected source file's bytes:

```sh
python verify_tranche.py --source-repo /path/to/orthemology
```

The replay runs the 34-test control suite and every `probe_*.py`, then extracts P14 to a temporary working copy, checks its 15 manifest artifacts, runs its seven tests and its two probe suites. The immutable nested archive is never modified. P14’s probe imports the sibling `restoration.py`; that previously external dependency is supplied by this complete bundle and is explicitly hash-bound in the replay report. P14 alone is not advertised as a standalone replay environment. `verification_report.json` and `verification-run.log` record the fresh complete replay used for this seal.

## Evidence ceiling and review handoff

Finite probes validate the declared algorithms and countermodels, not infinite-horizon measure theorems by empirical extrapolation. The infinite results have ordinary proofs with named dependencies. Selected results have separate mathematical readbacks, identified in the interface map; that is not external peer review or Lean verification. The companion Lean project is outside this archive and its kernel-checked scope is not silently inherited.

All authority, provenance-root independence/corruption timing, admissible standards, target labels, public-state adequacy and actual-world model fit remain explicitly supplied premises. A mathematical counterexample is never asserted as an observed cognitive or institutional fact. The P14 archive's identity is preserved, and its new successor results are not retroactively added to that predecessor.

The two consolidation repairs are recorded in `REVIEW_CORRECTIONS.md`. A fresh reviewer should prioritize: counterfactual policy-menu conformance; the source-adversary information class in stochastic marginalization; public/private mode projection under composition; fault detectability and reentry laws in regenerative recovery; and finite-memory versus unbounded-memory scope in hidden-standard learning. Subsequent work should respond to that review, rather than accumulating more examples.
