# Independent review: actual polynomial moment certificate

10 October 2026 UTC. Disposition: **ACCEPT AT THE STATED TRUNCATED POLYNOMIAL SCOPE.** No blocking defect was found. This is an independent source review and isolated Lean replay, not a release decision, novelty assessment, or T20 closure.

## Findings first

1. The certificate is genuinely about `MvPolynomial (Fin 3) ℝ`, its ordinary multiplication, total degree, coefficient linear maps, and Mathlib evaluation. It is not a scalar certificate labeled as a polynomial theorem.
2. Strict square positivity covers **every** nonzero real polynomial of total degree at most two. The parameterization is proved by polynomial coefficient extensionality over every exponent, with a complete ten-case classification and a separate proof that higher-degree coefficients vanish. There is no sampling restriction, assumed Gram identity, or hidden positivity hypothesis.
3. The witness is the actual polynomial `1−4xyz+x²y²+x²z²+y²z²`. Its global evaluation nonnegativity, degree bound, and functional value `−2` are kernel-checked. An independent additional probe checks that its degree is exactly four.
4. All seven production modules replayed successfully with Lean 4.19.0 and `--trust=0` into a clean, review-owned output directory. The seven fresh object hashes exactly match the author's. All 72 production theorem axiom closures contain only `propext`, `Classical.choice`, and `Quot.sound`.
5. The five compiler-negative controls were all rejected with the remaining goal `False`, not missing imports or identifiers. All 35 truncated moments independently match the intended exponent set and values.
6. **General measure nonrepresentation is not a separately formalized MeasureTheory theorem in this packet.** The author's result says so explicitly. Its ordinary mathematical corollary is sound with the stated finite moments; the integrability argument is spelled out below. The checked positive-functional theorem is not silently being treated as a full-domain integral theorem.
7. The actual continuation of Λ to higher-degree monomials fails square positivity: `Λ((x³−x)²)=−96`. This prevents extending the degree-scoped conclusion to the full polynomial algebra. The theorem and the failure are both checked.

## Reviewed candidate and isolation

Author directory: `lean-truncated-moment-obstruction-20261010`.

- Sealed manifest SHA-256: `c4d985e8227b1f3d7680850782c1bb72bd0769306d25ef9cdc182e48408afcbb`
- Author RESULT.md SHA-256: `afc8450bf849a4e0ec5458b60a6e77bf6414b042a9602de6bbf12425fec81c67`
- Author replay receipt SHA-256: `e9cabffee429c5d755b636ca33922158ac65f225fb0efbe493463d1e30f7d456`

All 33 sealed files were digest-verified, copied to `candidate/`, and rechecked against the unchanged author files after replay. No author source, dependency object, original diagnostic, or earlier review was modified. `replay/` was initially empty and held every newly compiled local module. `LEAN_PATH` excluded the author directory and its object directory. Fresh `lean --deps` output independently confirms local imports resolve to review-owned objects.

The 2,447 retained external dependency objects and their available source files matched the author's manifest exactly; none had an unavailable source. Adding the seven newly compiled local modules accounts for all 2,454 manifest entries. This verifies dependency identity, not a new build of Mathlib from source. No baseline or dependency rebuild occurred.

## Mathematical and semantic checks

### Functional and complete degree coverage

`TruncatedMoment.lean` defines Λ as a genuine real linear combination of coefficient maps. The moments are 1 on the constant, 4 on the three coordinate squares, 50 on the three pure fourth powers, 1 on the three mixed even fourth powers, 3/2 on xyz, and 0 on all other nonconstant monomials through degree four.

`Lambda_quadratic_square` derives the full ten-variable quadratic form by actual polynomial multiplication and coefficient extraction. `DegreeBridge.lean` proves every finite exponent vector has three coordinates, exhausts the ten exponent triples of total degree at most two, and proves all remaining coefficients vanish under the total-degree hypothesis. `every_quadratic_square_positive` has only the advertised degree and nonzero hypotheses.

`ScalarPositivity.lean` proves exact rational square decompositions, nonnegativity, and equality-at-zero characterizations for the four-dimensional even block and each two-dimensional odd block. Positivity is therefore strict, including mixed linear/quadratic combinations. Independent symbolic reconstruction in a differently ordered monomial basis also checks the universal ten-coefficient square identity and an exact positive LDL decomposition.

`quadratic_square_degree` places each square within degree four. `finite_sos_positive` covers finite sums of degree-at-most-two squares when at least one summand polynomial is nonzero. The author correctly does not claim a separately formalized theorem recovering quadratic summands from every unrestricted SOS representation of a quartic.

### Actual global witness

`eval_term` and `eval_witness` link the polynomial syntax to real evaluation. Global nonnegativity is proved by exact identities:

- For xy≥0: F=(xy−1)²+z²(x−y)²+2xy(z−1)².
- For xy≤0: F=(xy+1)²+z²(x+y)²−2xy(z+1)².

Every term has the required sign in its branch, for every real x,y,z. The witness has coefficient 1 at x²y²; the independent probe combines that fact with the author's upper bound to prove `witness.totalDegree = 4`. Direct coefficient calculation gives Λ(F)=1−6+3=−2.

### Nonrepresentation and integrability

The formal `PositiveOnNonnegativeQuartics` property quantifies over every actual degree-at-most-four polynomial and every real evaluation. The theorem `no_positive_functional_agrees` rules out a real linear functional on the whole polynomial type that has this property and agrees with Λ through degree four. It does not construct or assume an integral linear functional on all polynomials.

Ordinary measure nonrepresentation follows directly from F, without needing such a full-domain functional. Let μ be a positive Borel measure on ℝ³ with the prescribed finite moments. Its mass is 1, and each pure fourth moment is 50. For a monomial xᵃyᵇzᶜ with a+b+c≤4, set M=max(1,|x|,|y|,|z|). Then

    |xᵃyᵇzᶜ| ≤ M⁴ ≤ 1+|x|⁴+|y|⁴+|z|⁴.

Thus every required monomial, and hence F, is absolutely integrable. Finite linearity yields ∫F dμ=−2, while global nonnegativity gives ∫F dμ≥0, a contradiction. This argument is valid even if integrability is inferred from the four nonnegative finite moments rather than separately built into the representation definition.

`attempts/MeasureBridge.lean.unbuilt` is explicitly excluded and was never compiled by this review. Its theorem names have no acceptance status. To supply a future formal measure bridge, one must continue distinguishing totalized Bochner integral expressions from the finite-moment/integrability hypotheses needed to derive polynomial agreement from monomial agreement.

The review additionally kernel-checks a limited semantic consequence in `IndependentProbes.lean`: no finite positive weighted evaluation rule can match all degree-at-most-four polynomials. This is a finite atomic statement, not a replacement for general MeasureTheory formalization.

## Replay, axioms, and negative controls

`REPLAY_RECEIPT.json` records the seven fresh compilations and five expected failures. `evidence/AllAxiomClosures.log` expands the author's selected 16 closure checks to **all 72 production theorems**, including all 35 moments. No new axiom, sorry, admitted proof, native_decide, or implementation substitution occurs in production source or theorem closure.

The rejected claims are:

- Λ(F)=−1
- Λ(xyz)=0
- 0≤Λ(F)
- 0≤Λ((x³−x)²)
- 0<−Λ(1)

Each failed by explicit reduction using the checked value theorem and arithmetic. The core replay command is `python3 polynomial-moment-certificate-independent-review-20261010/replay_independent.py` from the retained workspace. `verify_dependencies.py` checks the retained dependency source/object identities. Review-owned Lean probes and their complete compiler logs are included separately.

## Comparison with the reference diagnostic

The reference `heat-truncated-certificate-diagnostic-20261010/RESULT.md` was copied and its exact checker replayed without editing the original. Its block-matrix moments, strict quadratic-square positivity, globally nonnegative F, and Λ(F)=−2 are exactly the portion now covered by the polynomial certificate.

The reference's heat evolution, dilation covariance, inverse heat composition, arbitrary fixed backward-time obstruction, and rational T=1,a=10 value −3797/2500 remain written/exact-symbolic results. They are **not** Lean theorems in this packet. The copied exact diagnostic checker passes, but that does not enlarge the kernel scope.

Neither packet establishes an extension of the 35 moments to a square-positive functional on the entire polynomial algebra. The explicit higher-degree failure concerns the particular zero continuation defined here, not a proof that every possible extension fails.

## Terminal review disposition

Accepted at the precise scope stated above. No source correction is required. The general MeasureTheory bridge, heat formalization, unrestricted SOS-degree extraction, full-algebra extension, literature novelty, empirical application, and T20 closure are outside this acceptance. Evidence is preserved in this review directory; author files remain unchanged.
