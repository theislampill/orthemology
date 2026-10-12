# New Orthemology frontier theorems, independently staged

This project contains actual new frontier mathematics proved with the official Lean 4.19.0 kernel. It is external to the frozen Orthemology repository and does not alter or approve that repository's original claims.

## Provenance

- Repository basis: `theislampill/orthemology` at `03e2604dfcef278b01c60d19b05370fcec4194b6`
- Lean: `leanprover/lean4:v4.19.0`, release compiler commit `6caaee842e94`
- Mathlib: `c44e0c8ee63ca166450922a373c7409c5d26b00b`
- All ten dependency identities are checked against the preserved v5 manifest by `verify.sh`
- Official compiler acquisition URL: https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst

These are the v5 lock identities. They do not claim compatibility with other historical Orthemology toolchain profiles.

## Meaning of the modules

### RankTransport.lean

Formalizes the relational continuation theorem from the research packet's `frontier-programme.md`, §11. Every possible source alternative in a destination successor fibre must have a selected-policy predecessor in the old fibre (C4). From this actual coverage condition and source rank descent, the maximum fibre rank contracts by at least one until zero. It proves target persistence by the computed initial maximum, matching infinite source runs under C3, explicit action eligibility and safety under the supplied contract, and nonblocking existence of a run.

The finite nonempty fibre contract admits overlapping, many-to-one fibres. A checked five-source/three-destination fixture has lifted ranks 2,1,0. A separate stale-alternative counterexample satisfies source descent and alternating matching but violates coverage and keeps lifted rank one. No target convergence is smuggled into the destination assumptions.

The lower-level rank inequalities need only finite fibres, not a globally finite arena. The full contract expressly requires nonempty fibres and a destination successor at every selected step. The action and observation model, source readout meaning, real-world permission, and completeness of the successor relation remain application obligations.

### PERRefinement.lean

Formalizes a finite-height potential for arbitrary partial equivalence relations. Complete the relation on two tagged copies of each state by equality or the original relation. A deleted state leaves two singleton classes; a surviving equivalence class contributes one class. Proper refinement induces a surjective, noninjective coarse quotient map, so the finite quotient cardinality strictly increases. It starts at one and is at most twice the number of original states. A deterministic decreasing iteration therefore stabilizes within `2m-1` rounds.

`PERPotentialFormula.lean` additionally constructs an explicit equivalence from the completed quotient to active equivalence classes plus two copies of each inactive state. It kernel-checks the exact identity `potential = 2(m-|D|)+c`, including empty active domains. The upper-bound theorem itself only requires the quotient argument.

### MealyRefinement.lean

Uses the actual universal-input operator from repository v5 `mathematics/DEFECT_COMPUTABILITY.md`, §5. It compares every pair of independent input symbols, not identical-input bisimulation. It proves that approximants are partial equivalences and decreasing; derives the `2m-1` stabilization bound; identifies the result with every finite approximant; proves equivalence with all pairs of actual length-n input words; and constructs two distinguishing words of uniform length `2m-1` for any state outside the deterministic-output domain.

Kernel-evaluated two-state and three-state machines require three and five rounds. This refutes a literal m-round count in this model. `MealySharpness.lean` now mechanizes the universal lower-bound family as well: for every positive m it constructs an actual m-state binary Mealy machine with a distinguished state surviving depth `2m-2` and failing at `2m-1`. Positive states are reindexed as a countdown, reversing the ordinary source family’s chain labels. Thus both the upper bound and its all-size optimality are kernel-checked.

### BlockMismatch.lean

Further quantitative continuation: counts actual finite lists of admissible input blocks, proves their recursive path semantics and cardinality, uses the distinguishing-word theorem to exclude at least one of all `2^L` blocks, and derives the geometric upper bound with `L=2m-1`. The complete input sample space has the explicit cardinality `(2^L)^j`, and accepted paths form a subset. The normalised result is a rational finite-sample-space statement. It is not a proof of the infinite-stream measure limit, atomic-mass decomposition, hierarchy reductions, or complete defect theorem.

### GuardedRefinement.lean

The literal partial-partition operator `R ∩ refine(R)` is mechanized separately. Its guard is proved redundant on every top-started approximant. The guarded and unguarded iterations agree at all stages, so both the upper bound and universal sharpness family apply to that literal displayed operator too.

## Reproducing in a fresh Linux directory

Keep the small source/configuration files together and run `./bootstrap.sh`. It downloads the official Lean release, verifies the recorded acquisition SHA-256, checks out the exact Mathlib commit, lets Lake obtain the pinned transitive packages/cache, and runs `verify.sh`. Standard prerequisites are Bash, Git, curl, tar with zstd support, and Python 3. The project has no dependency on the frozen source projection or any absolute workspace path.

The live research workspace uses `.lake/packages` as a relative symlink to `mathlib4/.lake/packages` to reuse the already fetched identical dependency cache. This is an environment convenience, not a requirement: a fresh bootstrap uses Lake’s ordinary package directory. `mathlib4` is a local path dependency so that the exact source checkout and complete dependency identities can be inspected directly. The compiler and dependency caches are excluded from the small deliverable archive.

## Verification

Run `./verify.sh`. This verifies the exact compiler/dependency identities, runs the full build, freshly invokes Lean on `Verification.lean`, checks all listed axiom footprints against `{propext, Classical.choice, Quot.sound}`, and hashes source/configuration files. No `sorry`, custom axiom, or native-decision axiom is used. Ordinary `decide` fixtures are kernel reduced.

The live research workspace retains the full attempt history, including failures that do not count as passing evidence. The compact archive includes the final consolidated passing receipt `receipts/verify-20260930T134917Z.log`, its 38 declaration axiom footprints, and compiler/acquisition hashes.

## Not established

- A mechanization of the full measure-theoretic CV-C theorem, arithmetical hierarchy, or real-time reduction
- A proof that a particular physical/noetic system instantiates the supplied transition, authority, or observation model
- A metaphysical conclusion, personal identity result, empirical validation, or historical novelty claim
- Compilation or acceptance of the frozen repository's retained formal project (tracked separately)

### LowerEnvelopeBudget.lean

A companion for disturbed restorative systems is also mechanized. Under pairwise bad-label reflection and synchronous source matching, the minimum finite-fibre source rank transfers a concrete bad-visit budget, without C4 coverage. Along every supplied destination run, the number of bad visits is bounded by the initial minimum rank and eventually no bad state occurs. This is different from a known time-to-core bound: a compiled family delays its single bad visit arbitrarily long while initial rank stays one. A checked fixture shows the earlier stale-fibre non-target example fails the stronger pairwise reflection assumption, so the lower-envelope theorem cannot be misapplied to it.

Safety, observation-uniform action choice, authority and nonblocking remain separate model obligations in this companion; its theorem is about all supplied infinite runs, not policy synthesis or real-world licensing.
