# Independent review of the finite moment/continuation bridge

9 October 2026 UTC. Ordinary mathematical research review. No audit disposition, formal-kernel certification, readiness decision, release authorization, or T20 closure is made.

## Result

No mathematical correction is needed in the reviewed frozen tensor result within its explicitly stated scope. The additive Fisher countermodel is also correct. The finite known-support interpolation, exact continuation equivalence, and affine-independence criterion are supported by independent derivations and exact controls.

The proof was derived independently from the parent-supplied model and claims before the tensor author's full text was read. The separate `INDEPENDENT_DERIVATION.md` records that argument and the negative controls. The tensor author received no proof details from this reviewer until after the frozen result had been supplied. The later suggestion to extend the interval beyond time zero was optional and was not incorporated into the frozen result.

## Frozen objects actually reviewed

- `tensor-moment-continuation-20261009/RESULT.md`: SHA256 `03f027122c0a908f1f6bcfcc61951223ca1fca547d8599aac2aa3437e3c01a11`.
- Its `MANIFEST.json`: SHA256 `0dd84c31bdefffd339dffc94075de75abbb4028a0163ee3fc72392ec714c72c9`.
- `state-dependent-gradient-obstruction-20261009/RESULT.md`: SHA256 `dc9adfc33c622c989de9204ef1349e6a5c36255152bc286c5c0e11da731b60f2`.
- Its `MANIFEST.json`: SHA256 `0d71011be67d49914a6225b093c4719449b673d499fecfdc34b8696f97bf5161`.

Both results were read in full. Both verification scripts were inspected and executed. Every listed artifact byte length and SHA256 in both manifests was recomputed and matched. The separate `INPUT_BINDINGS.json` records the concrete bytes reviewed. This binds this review to those artifacts, rather than asserting continuing currentness of a mutable upstream source.

## Claim-level assessment

1. **Hierarchy.** Direct differentiation proves the displayed contraction identity for every tensor degree. The zeroth-degree equation, one-slot contraction convention, fixed support, nonswitching times, and integrated interpretation at control switches are handled correctly.

2. **Finite known-support closure.** A separating projection exists, and the stated finite polynomial-curve search is valid when exact equality tests are available. Vandermonde/Lagrange inversion reconstructs aggregate weights and all tensors from degrees 0 through N−1. The top closure gives an exact nonlinear controlled ODE on the admissible moment image. The explicit N=1 treatment is necessary and correct. The record need not be coordinate-minimal or more economical than storing weights.

3. **Degree sharpness.** N−1 is sufficient for every fixed support. The collinear truncated-Vandermonde argument shows worst-case necessity within the stated cutoff moment-record family. This does not claim that each support requires that degree, that tensor degree is an arbitrary-encoding dimension lower bound, or that low-order closure never works.

4. **Continuation equivalence.** The normalized exponential solution, positivity at finite times, uniqueness, and tilt-composition identity are correct under the declared locally finite piecewise-constant controls. Equal aggregate weights give all equal q-continuations. Under one separating constant control, equality of the exact scalar response on [0,ε] gives equality of normalized partition functions and then weights by finite exponential independence. Duplicate fine allocations remain invisible precisely because only their aggregate enters this interface.

5. **First-moment descent.** The optional criterion is correct on the entire positive aggregate simplex for every real covector. Fibre constancy forces quadratic coordinate products into the affine evaluation space; that becomes a unital separating algebra and hence all functions on the finite support. The converse follows from unique barycentric coordinates. The proposition correctly concerns existence of a q-only field, rather than requiring canonical coarse Fisher geometry.

6. **Concrete controls and repair.** The three-point fibre countermodel, quotient mobility, quotient energies, two-moment coordinate inverse, and closed two-moment ODE check exactly. The four-point example correctly has equal first two moments but a third-moment and second-response-derivative difference of 1/54. It therefore supplies a real continuation distinction beyond the immediate covariance obstruction.

7. **Typing and semantic scope.** The full moment sequence has nonzero components in every grade, so it belongs to a graded product and cannot be placed wholesale in the inherited algebraic direct sum. The retained finite symmetric tuple has a declared numerical factor type and a legitimate finite graded realization. Its full dynamics are nonlinear. The result does not identify semantic workflow composition with tensor multiplication, transfer a finite-state theorem to a continuous system without proof, or claim preservation of an undeclared inquiry landscape.

## Executed evidence

- Tensor author script: **21 exact groups**, rerun successfully; output in `author_rerun.txt`.
- Additive precursor script: **19 exact groups**, rerun successfully; output in `precursor_rerun.txt`.
- Independently written script: **38 exact groups**, run successfully; output in `verification.txt`.

These are separate overlapping finite control suites, not an additive measure of proof strength. The general claims rest on the written derivations, not on finite enumeration. The independent suite includes a distinct positive four-weight witness, worst-case finite-difference controls, N=1, duplicate aggregation, symbolic arbitrary-control tensor identities, exact closure, a tilted Vandermonde at a positive time, failure under the nongeneric all-ones control, and noisy affine-independent support with a descended but noncanonical field.

## Source comparison

The inspected retained H-formalisation passages explicitly define the algebraic direct sum, the elementary fibre criterion, and the future-safe quotient criterion. The H-ICS observation-congruence proof already identifies invariance of observation fibres as the condition for descended actions. The retained H-Continuation §5 gives finite-instrument observable-span closure and predictive updates. The tensor paper accurately credits this ancestry and does not claim a new generic congruence principle. The retained source bytes agree with the declared Git blob identities; this review did not independently re-query the remote commit tree or certify the whole inherited papers.

Targeted primary-source reads also support the classical ancestry claimed. Harper connects categorical Fisher/Shahshahani geometry, gradient replicator equations, and exponential-family solutions; this review does not import the paper's separate exponential-map terminology. [Harper, §§2.2–3.1 and 3.5](https://arxiv.org/html/0911.1383v1).

Karev's preprint gives normalized exponential representations, the partition function, and trait-expectation covariance evolution. This supports the attribution of the tensor identity as a specialization of a classical calculation. Only these targeted formulas were checked; no broader variational or empirical claim is imported. [Karev, §§3–4, equations (12) and (17)–(20)](https://arxiv.org/pdf/0901.2378).

## Optional observation, not a required revision

The frozen theorem deliberately uses [0,ε]. The stronger statement for any interval of positive duration also holds. Equality of scalar responses implies Z_a=CZ_b on that interval. At an interior time t₀, derivatives of orders 0 through N−1 yield a Vandermonde system multiplied by nonzero diagonal exponential factors, so a=Cb. Normalization gives C=1. This avoids using analytic continuation as a black box. The independent derivation records it, but the reviewed theorem's stated time-zero scope is sufficient and unchanged.

## Limits that must remain attached to use of the result

- The finite reconstruction uses declared fixed vector support and exact arithmetic. The scalar-response theorem assumes an exact continuous record. No finite-precision, noisy-data, observation-cost, or sample-complexity guarantee follows.
- The independent unknown-support countercontrol concerns only one selected scalar response. Full vector outputs under all real controls are a stronger observation contract; the countercontrol does not assert their failure to determine an unknown finite measure.
- The equivalence is relative to the declared control and output interface. Source-token withdrawal, provenance-sensitive operations, additional outputs, or changing channel columns may distinguish states that this interface merges.
- An exact computed model does not establish physical control availability, actual observation, truth, cognitive realization, epistemic warrant, field-wide novelty, or permission to act.
- The earlier fixed-reference metric result is not contradicted; the Fisher countermodel changes the dependence of the metric on the current state.

No author or inherited source file was edited during this review. The parent may use the bounded mathematical conclusions and attached derivation; all broader project decisions remain outside this review.
