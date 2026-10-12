# Independent observer and actual-measure audit, sealed stage

## Disposition

No semantic defect found in the precise sealed claims inspected. The three specified seals independently reproduce at the pinned toolchain. This is bounded audit evidence, not canonical adoption, proof of the whole Orthemology programme, a numeric-code hardness result, or approval of unsealed extensions.

- Audit workspace: `private-locator:7aad77b447f0fee61f52`
- Toolchain: Lean 4.19.0, commit `6caaee842e94`
- Mathlib: `c44e0c8ee63ca166450922a373c7409c5d26b00b`
- Original project source trees were read only. Project oleans were regenerated in the audit workspace, using `lean -j1`; no whole caches were copied.
- Canonical repository was not modified or adopted. This report does not purport to verify unrelated activity by other workers.

## Exact objects

1. Mealy archive `Mealy_Measure_Bridge_Stage1_20260930.zip`, SHA256 `a4755cb68772a0394458fb81a2a77ca4d2388aff6d1f8d4073ecfe8e0da3e590`. Its file bytes were compared directly with every file in `mealy-measure/sealed-v1`; the sealed directory's SHA256SUMS also passed.
2. LOOP receipt `p02-qualification/receipts/loop-20260930T142933Z/LOOP_RESULT.json`, SHA256 `0d7a327ec9d8f73a3481972d31f494258d63613459f0c48f01ada7c24a311a9e`.
3. Sigma2 receipt `p02-qualification/receipts/sigma2-20260930T144631Z/SIGMA2_RESULT.json`, SHA256 `266c4a739a092eb9ba474ebc819b183ef22bc9e7cdf5f7f0ccc6b563694d23de`.

All receipt-listed source hashes matched the actual files before copying. All 26 copied source modules and their origins are enumerated and hashed in `manifest.json`; the original files were rehashed after rebuilding and again before this report. The local import search path contains only the fresh audit build and pinned Mathlib/package build directories. It excludes pre-existing project output directories.

## Reproduction evidence

- `rebuild.py`, `rebuild.log`, `BUILD_RESULTS.json`: all 26 project/dependency modules compiled with exit 0, including PERRefinement, MealyRefinement, BlockMismatch, MeasureCore, Q8Measure, ObserverCore, Q8Machine and Q8Compiler.
- `check_controls.py`, `controls.log`, `CONTROL_RESULTS.json`: exact receipt source checks, archive byte comparisons, theorem census and seven controls.
- `AXIOM_READBACKS.json`: 31 Mealy + 41 LOOP + 56 Sigma2 original named declarations, plus five independent adversarial endpoints. Every recorded axiom set is contained in `{propext, Classical.choice, Quot.sound}`. No `sorryAx` occurred in successful readbacks.
- The seven original controls comprised two compiling baselines and five deliberately false statements that failed for the intended reason. The three inlining controls report a false proposition from kernel `decide`; the quantifier and endpoint controls reduce to an unsolved `False` goal, rather than failing on imports or missing declarations.
- `sources/AdversarialWitnesses.lean`, `receipts/AdversarialWitnesses.log`: additional independent kernel-checked boundary examples described below.
- `SEALED_STAGE_AUDIT_RESULT.json`: machine-readable scoped result.

## Mealy proof chain

### Genuine measure and finite blocks

`Q8Measure.lean:15–37` defines the bit law from Mathlib's Bernoulli PMF and the stream law as `Measure.infinitePi`; `fairCantor_cylinder` invokes the actual infinite-product cylinder theorem. It is not a finite counting proxy named “measure.”

`MealyMeasure.lean:67–118` gives literal tick-by-tick state/output execution and proves its correspondence with list execution. The deterministic relation originates in `MealyRefinement.lean:18–19,89–122`, which compares every independent input pair. It is not same-input bisimulation.

`MealyMeasure.lean:155–278` parses actual disjoint coordinate blocks `x(kL+i)`, proves that flattening gives the first `jL` input coordinates, and proves injectivity at fixed block length/count. The union of corresponding cylinders is genuinely disjoint. Thus the exact event measure is `card(F) * (1/2)^(jL)`. No independence of state-dependent survival events is asserted or needed. The block-language recurrence counts the entire branching path tree, retaining its state-dependent allowed sets.

The generic block result handles `L=0` and `j=0` correctly because length/count are fixed. The substantive finite-state theorems have finite and nonempty state hypotheses and an initial state, so the sharp `L=2m−1` horizon is positive and no empty-state vacuity is used.

### Avoidance and quantifiers

`finite_survivor_measure_bound` (`MealyMeasure.lean:458–487`) explicitly includes the non-D endpoint at time `jL`. `blocks_mem_surviving_finite` propagates deterministic-domain closure to show that this excludes every earlier entry into D. The proof therefore has not silently removed the essential avoidance condition.

`avoidMatch_null` (`:319–327`) proves nullity for each fixed infinite output restricted to trajectories that never enter D, by an actual ENNReal geometric limit. It does not say the union over all outputs is null, nor that every non-hitting input has a non-atomic output.

`hits_output_positive` uses a positive-measure hitting-prefix cylinder. Conversely, `positive_avoiding_null` (`:360–369`) only unions null fibres over the countable set of positive singleton outputs. That countability follows from the SFinite actual output law. `atomic_mass_eq_hitting_probability` consequently proves equality of measures of the two events, not literal equality of the input events. `positive_iff_hitting_prefix` is existential over a hitting input producing a given atom.

The periodicity theorem uses a repeated state on a constant-input trajectory after D is reached. It makes no claim that every eventually periodic output has positive mass.

### Rationality

`MealyHitting.lean` has an executable finite D test derived from the sharp refinement theorem, executable finite-horizon rational counts, an exact bridge to genuine hit-at-time events, and their increasing limit.

`MealyRational.lean:11–49` derives the one-step equations from head/tail decomposition of actual finite input words and uniqueness of real limits. Its maximum principle (`:79–135`) separately pins D and every state that cannot reach D. A positive global maximum propagates along an actual finite path to D, contradicting its zero boundary. Closed non-D recurrent components are not assumed transient.

The rational solution in this seal is existential: finite-dimensional injectivity implies surjectivity over Q, and uniqueness over R identifies the cast solution with the actual measure. The sealed text correctly excludes kernel-verified extraction of a general infinite-horizon solver. That exclusion cannot be removed merely because finite probabilities are executable.

## LOOP proof chain

`LoopRenaming.lean` includes every read/write/index register in finite support. `exec_rename` requires injection only on the supplied support, not a global bijection, and carries exact finite-support store agreement. `exec_frame` and `renamed_frame` preserve registers outside that support.

`inlineCode_correct` (`:246–271`) requires:

- source body support and output are in the reset list's finite set
- renaming is injective on that set
- argument destinations are in the set
- argument-expression reads are disjoint from its renamed image

It resets the whole local bank, loads arguments with their values from the original caller, executes the renamed body, and copies the result. The caller frame property explicitly excludes both the renamed bank and the final destination. It does not falsely promise to preserve locals, or require an unnecessary global renaming injection.

`LoopPrimrec.lean` supplies a finite store evaluator and proves it simulates the actual ObserverCore semantics whenever all used registers fit the bound. Primitive recursion is proved for fixed expressions/statements by syntax induction; the loop bound is snapshotted before execution, matching ObserverCore. `programBound` includes arity, body registers and output. `program_denotation_primrec` thus establishes Mathlib Primrec membership for each fixed program's denotation. It does not provide a uniformly primitive-recursive universal interpreter over arbitrary program codes, nor PR completeness/compilation of all PR functions into the grammar.

## Sigma2 proof chain

`SurvivorCandidates.lean` chooses the least stage-n candidate passing every test `t≤n`, with default `n+1`. Candidates are nondecreasing. A true witness bounds the entire sequence, so it stabilizes; conversely a stabilized value is shown to pass an arbitrary test by choosing a stage at least the stabilization time, test index and candidate value. The direction is exactly `∃s∀t`, not `∀t∃s`.

Innovation compares the current candidate with its predecessor, with predecessor zero at stage zero. Finite innovation is equivalent to eventual non-innovation and hence to a witness. The stage-zero convention cannot change this finite/infinite distinction.

`SurvivorPrimrec.lean` proves joint primitive-recursiveness for one fixed PR matrix family, using bounded quantification and a bounded graph for least search. It does not assert uniform primitive recursion over every matrix program code.

`Sigma2RowLaw.lean:17–34` identifies the synchronous sentinel-prefix observer with copying exactly input coordinate n at each innovative n, and false otherwise. This is an actual map of the fair infinite product. `InnovationMeasure.lean` proves finite copied coordinates give a finite carrier; infinitely many copied coordinates make every singleton zero by extracting arbitrarily large finite sets of distinct coordinates. Thus defect is zero iff `∃s∀t R`, and one iff no such witness exists.

`Sigma2SourceMatrix.lean` discharges the PR premise for every fixed arity-three LOOP matrix program. It still uses the mathematical prefix family, not an emitted numeric-code compiler correctness theorem. The original seal explicitly retains that boundary.

## Independent boundary countermodels

All five endpoints below compiled with the fresh dependencies and the stated axiom ceiling; they are countermodels to possible overstatements, not defects in the sealed theorem statements.

1. `constant_fibre_measure_one`: a one-state constant-output machine has fixed-output fibre measure one. Nullity without avoidance is false.
2. `nonreaching_harmonic_countermodel`: a one-state copy machine has no D state, while the nonzero constant-one rational function satisfies every harmonic equation and the vacuous D zero condition. Omitting non-reaching zero boundaries destroys uniqueness.
3. `positive_output_can_avoid_D`: in the three-state split machine, the input beginning true and continuing false enters the copying sink forever but produces the all-false atom. The same atom has positive mass because inputs beginning false reach the deterministic sink. This disproves universal pathwise hitting or equality of the two input events; their measures still coincide.
4. `repeated_bit_defect_zero`: the observer outputting `x(0)` at every tick has finite carrier and defect zero despite infinitely many output ticks. Distinct fresh copied coordinates are essential to the infinite-revelation result.
5. `omitted_register_breaks_simulation`: executing `set register 1 := 7` on the unbounded store yields 7 at register 1, whereas a one-register finite evaluator extended by zeros yields 0 there. The register-support hypothesis cannot be dropped.

The original tests additionally witness history dependence without reset, corruption from colliding renaming, overwritten nonfresh arguments, the quantifier-swap failure `R(s,t) := t≤s`, and reversed defect endpoints.

## Explicit exclusions and pending work

No evidence here is credited to the unsealed constructive Mealy solver, candidate compiler binding, or tagged-row fair-selector/tail disintegration. They require distinct exact-object checks and fresh rebuilds after their final receipts arrive.

Also excluded: correctness of a Python byte interpreter/codec, a numeric-code or arity-index many-one reduction, full hierarchy membership/hardness, primitive-recursive universality, every singleton's rational mass, realization of every rational defect, novelty, canonical adoption, and physical/ethical or empirical consequences. The inspected claims are formal model theorems at the stated pin.
