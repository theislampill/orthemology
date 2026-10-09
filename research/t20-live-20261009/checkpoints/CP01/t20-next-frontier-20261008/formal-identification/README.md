# Kernel-checked exact calibrated identification

## Result

Lean 4.19 checks the complete following mathematical statement:

For an arbitrary finite type of effects E, let H and K each comprise five functions from finite subsets of E to natural numbers. Each function vanishes at the empty subset. Define the hit count of f at U as the sum of f(T) over all T meeting U. Define three exact rational panels:

- A: (1/2)^(hit_a(U) + hit_d(U))
- B: (2/3)^(hit_b(U) + hit_e(U))
- AB: (1/2)^hit_a(U) (2/3)^hit_b(U) (5/6)^hit_c(U)

If these panels agree for every nonempty U, all five histogram functions agree on every subset T. Counts are unbounded natural numbers; E is arbitrary, not a checked enumeration of small catalogues. The empty effect type is covered as a degenerate case.

Main declaration: `CalibratedIdentification.calibrated_panels_identify` in `CalibratedPanels.lean`.

An explicit coefficientwise corollary is `calibrated_panels_identify_coefficients`.

## Proof architecture

1. `Calibration.lean` proves that the actual rational product code is injective on natural triples. It computes p-adic valuations at 5, 3 and 2 and solves the resulting integer equations. It also proves the two solo exponent maps injective, then recovers all five hit counts. No decoder or injectivity assumption is supplied.
2. `HitTransform.lean` proves the finite hit transform injective when the empty coefficient is fixed. Complement-hit and subset-mass sums partition the histogram; strong induction on subsets recovers every coefficient. A bridge lemma identifies the finite-type sum with the explicitly filtered powerset sum. A stronger theorem characterizes all observational equivalence, including the invisible empty coefficient.
3. `CalibratedPanels.lean` composes those proved inversions. The five empty-zero constraints are fields of the histogram, and the observation hypothesis is equality only of the three rational panels.
4. `Verification.lean` checks the exported signatures, prints their axiom dependencies, instantiates both empty and arbitrary finite catalogues, and verifies the numerical rational code normalization.

## Reproduce

Prerequisites: Linux x86-64, Bash, curl, Git, tar with zstd support, and network access to the official dependency hosts.

Run `./bootstrap.sh`, then `./verify.sh`, then `./mutation_checks.sh` from this directory.

The bootstrap installs entirely beneath this directory. It pins:

- Lean 4.19.0, binary commit 6caaee842e94
- Official Lean Linux archive SHA-256: 6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe
- Mathlib v4.19.0, commit c44e0c8ee63ca166450922a373c7409c5d26b00b
- Mathlib's own checked-in dependency manifest, copied in `DEPENDENCY_MANIFEST.json`

The verification script compiles every deliverable Lean source with warnings treated as errors. Its module-root argument permits this package to remain separate from the dependency checkout. No protected repository is modified.

`results/full-verification.log` is the successful full-build output. All five printed principal theorem dependencies are exactly the standard Lean axioms `propext`, `Classical.choice`, and `Quot.sound`; no admitted-proof axiom occurs. No new axioms, `sorry`, `admit`, or `native_decide` are used in the deliverable Lean files.

Two mutation controls are rejected by Lean: replacing the 5/6 joint failure factor by 1/6, and replacing query intersection in the hit transform by mere nonemptiness. The controls modify temporary copies only. An intentionally unproved-goal control is preserved as plain text alongside its rejection log, outside the successful build.

## Exact assurance boundary

The kernel result identifies the anonymous histogram in this declared algebraic observation model. It does not prove the factorization from a probability space; independent route survival, the meaning of an actual occurrence, rate calibration, intervention feasibility, exact access to population probabilities, and the relation to productive-ground/source claims remain external premises.

It does not establish finite-sample identification, physical realization of gates, numerical route identities, an arbitrary-root valuation-channel criterion, or metaphysical uniqueness. This package supplies stronger assurance for the stated inverse mathematics, not those additional premises.

Research and installation records are separate. No total active-research duration is certified, and installation, waits, recovery and packaging receive no research-duration credit.
