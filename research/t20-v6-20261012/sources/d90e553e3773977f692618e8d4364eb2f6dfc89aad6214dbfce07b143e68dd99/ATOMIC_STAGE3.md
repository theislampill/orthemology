# Exact singleton masses, atomic measure reconstruction, and effective approximation

This extension adds new source files only. The Stage-1 and Stage-2 seals and their proof sources remain unchanged.

## Target singleton probabilities

`Generator T` is a deterministic input-free finite-state presentation of a target stream. `mismatchMachine` synchronizes that generator with the original Mealy machine. It copies the fresh input bit before mismatch, and emits constant false from its absorbing mismatch sink.

The proof does not assume the key correspondences:

- `mismatch_domain` proves its deterministic-output domain is exactly the mismatch sink. Every non-sink state's two immediate outputs differ.
- `mismatch_state` proves the exact prefix-monitor invariant against actual original execution and the target generator.
- `mismatch_hits_eq` proves hitting the auxiliary D is precisely failure to equal the entire target stream.
- `targetMassQ_correct` identifies the executable rational target-mass program with the actual original output-law singleton probability.

This handles finite-state-presented targets. It does not compute singleton masses for an arbitrary unrepresented infinite stream.

## All positive atoms

A positive atom has a D-hitting prefix by Stage 1. `positive_atom_finite_generator` explicitly builds a finite generator that follows that finite input prefix and then supplies false input forever. Its generated output is the given positive atom. `positive_singleton_mass_rational` therefore derives rationality of each positive singleton from the target solver.

`atomCandidate` uses all finite binary input words followed by a false tail. `atomCandidateMassQ` computes each candidate's exact rational singleton mass. `positive_iff_candidate` proves positive candidates cover exactly the positive singleton support.

`generatorsEqual_spec` derives a terminating equality decision for two finite-state-generated infinite streams, using the earlier kernel-checked universal-input finite refinement bound on their disjoint union. Thus candidate equality is checked as infinite-output equality, not equality of finite descriptions.

## Enumeration semantics

`enumerateAtoms M s n : Option (List Bool × ℚ)` processes the nth decoded finite-word candidate. It returns a word/weight pair only for a positive mass and only at the first index denoting that same infinite output. Otherwise it returns `none`.

- `enumerateAtoms_sound`: each returned entry is a genuine positive atom with its exact rational mass
- `enumerateAtoms_complete`: every positive singleton appears at some index
- `enumerateAtoms_no_duplicates`: distinct returned entries denote distinct infinite streams

This is enumeration **with skips**. It is not a total function that returns the nth positive atom. No termination is claimed for waiting for another positive atom after a finite support has been exhausted; no support-finiteness decision is supplied.

## Actual measure reconstruction

Enumeration alone is not called a measure decomposition. The following separate proofs establish the measure equalities:

- `atomic_measure_reconstruction`: the original law restricted to its positive-singleton set equals `Measure.sum` of the enumerated rational-weighted Dirac measures; skipped indices contribute the zero measure
- `atomic_mass_eq_tsum_weights`: those exact singleton weights sum to the full atomic mass
- `partialPointMeasure_eq_restrict`: each finite initial sum equals restriction to its already-enumerated atoms
- `finite_atomic_measure_decomposition`: the full atomic restriction is exactly the finite initial sum plus restriction to the remaining atoms

These use the proved pairwise disjointness and full union of the enumerated singleton sets, not an assumed summation correspondence.

## Effective residual and approximation modulus

`partialMassQ N` is the rational sum of weights returned through enumeration indices below N. `residualMassQ N` is the exact rational total from `solveHitting` minus that partial mass.

- `residualMassQ_correct`: this rational residual equals the actual remaining atomic measure
- `residualMassQ_nonneg` and `residualMassQ_antitone`: it is nonnegative and never increases
- `partialMassQ_tendsto` and `residualMassQ_tendsto_zero`: finite measure sums converge to the atomic restriction's total
- `approximationCutoff k` is executable unbounded search (`Nat.find`) on the decidable rational condition `residualMassQ N < 1/2^k`
- `exists_residualMassQ_lt` proves that search terminates for every k
- `approximationCutoff_uniform_measure_error` proves that every N at or beyond the returned cutoff omits actual atomic measure less than `2^(-k)`

There is no assumed effective convergence rate: the known exact rational total makes the residual test effective, and the measure sum theorem proves eventual success. No runtime/scalability bound is asserted. The naive finite refinement and determinant procedures can be expensive.

## Controls and evidence

Kernel controls cover constant false matched exactly, constant false versus constant true, fair input copying versus constant false, and a genuine mixed law whose false target singleton has mass 1/2. Supplementary executions return 1, 0, 0, and 1/2 for those targets; the finite singleton atom enumeration returns one entry then skips a duplicate. Approximation executions terminate with cutoff 1 for the singleton law and cutoff 0 for the atomless law.

`verify-atoms.sh` first performs the full earlier source replay, then fresh-compiles all Stage-3 sources, runs exact fixture-output checks, and reads back the types and axiom sets of 39 new principal theorems. No new axiom, proof hole, or native-decision axiom is introduced.

## Source order

After unchanged Stage 2: `TargetMass.lean`, `PositiveAtomMass.lean`, `AtomEnumeration.lean`, `GeneratorEquality.lean`, `EffectiveAtoms.lean`, `AtomicReconstruction.lean`, `AtomicApproximation.lean`, `TargetMassFixtures.lean`, `AtomicApproximationFixtures.lean`; then `AtomVerification.lean`.

The universal converse realization theorem for every rational defect remains outside these Lean seals. The Stage-2 non-dyadic fixture establishes one actual defect1/3 example, not the entire realization family.
