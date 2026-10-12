# Actual fair-input measure bridge for finite Mealy machines

New external research at the unchanged Lean 4.19.0 / mathlib c44e0c8ee63ca166450922a373c7409c5d26b00b pin. This directory does not modify the canonical repository, the predecessor finite-refinement project, or the qualification project.

## Established statements

1. `MealyMeasure.measure_block_event` interprets an actual finite family of consecutive input block words as an event under `Q8Measure.fairCantor = Measure.infinitePi fairBit`. Its measure is exactly the family cardinality times `2^(-jL)`. This is proved from the predecessor cylinder theorem, a literal input-coordinate block encoding, and disjoint measurable cylinders.
2. `finite_survivor_measure_bound` gives the literal finite-horizon estimate: matching any fixed output through `jL` steps and remaining outside D at that time has measure at most `(1-2^(-L))^j`, with `L=2m-1`. D is transition closed, so remaining outside at the endpoint means never entering it earlier.
3. `avoidMatch_null` passes to zero via the actual ENNReal geometric limit. It concerns every fixed infinite output and input paths never entering D.
4. `atomic_mass_eq_hitting_probability` proves that total positive-singleton output mass is exactly fair-input probability of ever entering D. Every hitting prefix contains a positive-measure cylinder with one output; the converse uses countability of the positive singleton support and the null-fibre result.
5. `positive_iff_hitting_prefix` characterizes each positive atom by a D-hitting input that produces it. `positive_output_eventually_periodic` proves every positive atom is ultimately periodic, using a genuine repeated state on a constant-input trajectory.
6. `deterministicBit` is an executable decision procedure for D using the proved sharp finite approximation. `hittingProbabilityQ` computes exact rational finite-horizon probabilities; `hittingProbabilityQ_correct` identifies those values with actual event probabilities, and `atomic_mass_tendsto_finite_hitting` identifies their increasing limit with atomic mass.
7. `atomic_mass_zero_iff_unreachable` characterizes zero atomic mass by absence of any finite word reaching D.
8. `rational_hitting_probability`, `atomic_mass_rational`, and `defect_rational` prove rationality of the actual infinite-horizon hitting law, atomic mass, and nonatomic defect. The proof establishes the actual probability's one-step equations from finite counts and convergence. The homogeneous finite system is injective by a maximum principle propagated along a literal finite path into D, with every non-reaching component separately pinned to zero. Finite-dimensional injectivity implies surjectivity over ℚ; uniqueness over ℝ identifies the rational solution with the measured law.

## Important limits

- The current infinite-horizon rational solution is existential. Its finite system uses the proposition `Reaches`, and finite-dimensional surjectivity supplies a solution. This is not yet a kernel-verified extracted solver for general infinite-horizon hitting probabilities.
- Exact finite-horizon probabilities and D-membership are executable. `#eval` checks are explicitly supplementary; they do not substitute for the kernel proofs of semantic correctness.
- No Gaussian-elimination source correspondence is claimed for the predecessor Python experiments.
- The proof of rationality uses the maximum principle, not an unproved assertion that every state outside D is transient. Closed non-D recurrent components are assigned zero boundary value.
- Rational mass of each eventually periodic singleton target and realizability of every rational defect are not yet established in these files.
- These are mathematical model results. They do not establish physical observability, substrate adequacy, ethical authority, or empirical validation of the surrounding theory.

## Files

- `MealyMeasure.lean`: actual stream execution, product cylinders, finite block count bridge, infinite null limit, atomic mass equality
- `MealyHitting.lean`: executable D and finite probability computation, exact law correspondence, monotone limit, zero-mass reachability criterion
- `MealyAtoms.lean`: ultimate periodicity of every positive singleton output
- `MealyRational.lean`: finite count recurrence, actual law equations, finite maximum principle, rationality
- `MealyMeasureFixtures.lean`: kernel-checked actual masses 1, 0, and 1/2, plus separate executable finite-horizon checks
- `Verification.lean`: full type and axiom readbacks for every main theorem
- `verify.sh`: fresh recompilation of all five predecessor sources and all new proof files, with axiom-ceiling check

Run `./verify.sh`. The script does not download or copy caches. It fresh-compiles predecessor source files to this directory's `dependency-build` and uses only their regenerated outputs plus the pinned mathlib build.

## Dependency provenance

The actual measure is not invented here: `Q8Measure.fairCantor` is the countable product of fair Bernoulli measures, and `fairCantor_cylinder` is used directly. `P02A2.mass` is the measure of the positive-singleton set; its countability is imported from the freshly recompiled `MeasureCore.lean` source. The historical header of that predecessor source says "UNEXECUTED"; the new verification receipt explicitly fresh-compiles it, rather than treating that stale header as current evidence.

The pre-existing `Mealy.refine` universally compares independent input bits, not same-input bisimulation. The finite `BoundedPaths.words` accepted-language construction, its length proof, and its sharp mismatch cardinality bound are imported unchanged and recompiled from source in the verification script.
