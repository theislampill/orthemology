# Independent exact-atoms and approximation audit

## Disposition and exact object

PASS within the stage-3 scope. No semantic or seal defect found. The extension genuinely computes finite-state-presented target masses, enumerates all positive output atoms without repeated streams, reconstructs the actual atomic restriction, and provides a terminating exact-rational search for a finite atomic approximation with a uniform later-index error bound.

Archive: `private-locator:bdc24e97d339e66cf78d`

SHA256: `9533e5bbd7023c113141391e87bd597d76a77528822e65532405c14b7a3ee962`

All sealed-v3 files matched archive bytes and SHA256SUMS. All prior stage-1/2 proof-source hashes matched the existing independently rebuilt audit dependencies. The audit rebuilt only the nine new modules plus AtomVerification into `atoms-build`, with imports resolved against fresh local audit outputs and the exact pinned official Mathlib/package caches. Prior completed phases were not replayed or recounted. Original source trees and canonical repository were unchanged.

## Reproduction

`audit_atoms.py`, `atoms-audit.log`, `atoms-receipts/` and `ATOMS_STAGE_AUDIT_RESULT.json` record commands, source hashes, exits and durations. TargetMass, PositiveAtomMass, AtomEnumeration, GeneratorEquality, EffectiveAtoms, AtomicReconstruction, AtomicApproximation, TargetMassFixtures, AtomicApproximationFixtures and AtomVerification each returned exit 0 using Lean 4.19.0 commit `6caaee842e94`, `-j1`, and Mathlib `c44e0c8ee63ca166450922a373c7409c5d26b00b`.

All 39 new principal type/axiom readbacks have footprints contained in `{propext, Classical.choice, Quot.sound}`. The printed executable definitions include targetMassQ, atomCandidateMassQ, generatorsEqual, enumerateAtoms, partialMassQ, residualMassQ and approximationCutoff; none is replaced by a noncomputable choice-based implementation.

The eight supplementary executions reproduced: target masses 1, 0, 0, 1/2; singleton enumeration `some ([],1)` followed by `none`; cutoff 1 for the singleton law and cutoff 0 for the atomless law at precision k=2. General correctness remains supplied by the kernel proofs, not these evaluations.

## Target monitor and exact singleton law

`mismatchMachine` synchronizes an original state with an input-free finite target generator. In every non-sink state it outputs the current input bit, so its two immediate outputs differ. Its deterministic-output domain is therefore exactly its permanent mismatch sink, independently of any desired target-mass conclusion.

`mismatch_state` tracks equality of the first n output symbols after n input steps. The next original output is compared against the target at that same tick, and a mismatch on input n causes sink entry at time n+1. `mismatch_hits_eq` proves actual eventual sink entry equals the complement of the original output singleton's preimage.

The stage-2 solver's auxiliary defect is consequently the probability of never mismatching, which is the original target singleton's measure. `targetMassQ_correct` checks measurability and finite-probability complement arithmetic before the real conversion. It does not confuse the auxiliary copied output with the target output.

The target must have the supplied finite-state generator presentation. This does not compute the mass of an arbitrary unrepresented infinite sequence.

## Positive-atom generators and duplicate elimination

Every positive atom has some original D-hitting input prefix. The prefixDriver reads that finite prefix and then false forever, with its finite position saturating at the prefix length. Driving the original machine by this driver generates the same entire output: the hitting prefix fixes the rest independently of the chosen false continuation. Thus every positive atom has an explicit finite generator, and its singleton mass is rational by the new target solver.

`atomCandidate` ranges over finite input words with false tails. `atomCandidateMassQ` is the exact singleton mass, not a candidate-prefix probability. A positive rational value is proved equivalent to actual positive-singleton membership.

`generatorsEqual` turns two finite generators into an input-ignoring Mealy machine on their disjoint union. The earlier finite universal-input refinement bound then decides equality of their complete infinite streams. The proof establishes both semantic directions and handles the two different state types through the sum generator. Duplicate tests therefore compare output streams rather than finite words or transient prefixes.

`wordAt` is total: an unused decoded natural code yields the empty word. Its encode/decode theorem ensures all finite words appear. `enumerateAtoms n` returns an Option value, keeping only positive candidates whose stream has no earlier equivalent candidate. Completeness uses the least index denoting a positive output. Comparing even earlier zero-mass candidates cannot hide a positive atom, because equal output streams have the same actual singleton mass.

This is a total enumeration with skips. It provides neither a total nth-positive-atom selector nor a guarantee that waiting for another positive result will terminate after finite support is exhausted. No support-finiteness decision is asserted.

## Actual measure reconstruction

For each enumeration index, atomSet is either empty or a singleton; atomPointMeasure is either zero or the corresponding exact rational-weighted Dirac measure. Soundness, stream-level duplicate-freedom and completeness prove that these measurable sets are pairwise disjoint and their union is exactly the law's positive-singleton support.

`atomPointMeasure_eq_restrict` identifies each weighted Dirac with the actual singleton restriction, including conversion from the rational weight using finiteness. `atomic_measure_reconstruction` then uses countable restriction additivity to establish equality of measures, not just equality of supports. `atomic_mass_eq_tsum_weights` identifies the entire exact weight sum with total atomic mass.

`partialPointMeasure_eq_restrict` separately proves every finite initial sum equals restriction to its already-listed atoms. `finite_atomic_measure_decomposition` splits the whole atomic restriction into that finite measure plus the actual restriction to remaining atoms. No duplicate mass is counted twice, and skipped indices contribute exactly zero.

## Exact residual and effective approximation

The residual subtracts the finite rational atomic sum from `solveHitting`, the already-certified exact total atomic mass. It does not subtract from total probability one. `residualMassQ_correct` proves equality to the remaining atomic set's actual measure; nonnegativity and antitonicity are established, not assumed.

The countable reconstruction identity and continuity of finite ENNReal sums give convergence of rational partial masses to that known total. Finiteness justifies conversion to real limits. Hence residuals converge to zero, so the strict rational predicate `residualMassQ N < 1/2^k` eventually holds.

`approximationCutoff` uses Nat.find on that decidable rational predicate with a proof of existence. The implementation is executable unbounded search, with termination proved for every k. The exact computable total is what makes the test effective; the argument does not incorrectly extract a rate from arbitrary convergence alone. No runtime bound or practical scalability guarantee is implied.

`approximationCutoff_uniform_measure_error` combines residual antitonicity with the successful cutoff: every N at or after that cutoff leaves actual atomic measure strictly below `2^(-k)`. The threshold is strict, and N counts enumeration indices, including skips, not returned positive atoms.

## Four independent boundary endpoints

`atoms-sources/AtomicBoundaryWitnesses.lean` and its successful axiom log establish:

1. `duplicate_descriptions_same_stream`: distinct finite words can describe exactly one infinite output, so word-level deduplication would be insufficient
2. `atomless_enumeration_always_skips`: every natural index returns none for the fair copying machine
3. `atomless_residual_exact_zero`: that machine's residual atomic mass is exactly zero at every finite index
4. `atomic_approximation_not_full_law`: its actual law still assigns mass one to the whole space while every finite atomic approximant assigns zero

All four compiled with the freshly built new dependencies and the standard axiom ceiling. The last two guard the central interpretation: these measures approximate the positive-singleton restriction. They do not approximate a remaining diffuse component or a normalized full output distribution.

## Exclusions

Still outside this seal: a total nth-positive-atom selector; effective handling of arbitrary unrepresented infinite target streams; deciding finite support; a practical or polynomial complexity bound; universal realization of every rational defect; correctness of the predecessor Python solver/byte codec; or canonical adoption. The earlier non-dyadic example is not promoted to the universal realization theorem.
