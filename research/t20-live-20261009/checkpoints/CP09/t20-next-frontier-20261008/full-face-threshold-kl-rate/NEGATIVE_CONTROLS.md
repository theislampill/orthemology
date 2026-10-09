# Failed shortcuts and strict scope controls

1. **Global L2 perturbation is false.** The likelihood ratio is not in L2(P0) for any fixed n. The local polynomial score (1-u)(1-v) does not furnish a globally dominating chi-square envelope. The proof expands only on growing logarithmic boxes and treats the complement by entropy bounds.

2. **Finite KL alone says nothing about the exponent.** The inherited bound D_n<=2+log(3/2) proves integrability but gives no n^-4 rate. It is useful only after being localized with the shared exponential tails.

3. **A pointwise CDF expansion is insufficient.** The full density needs mixed derivatives. Equations (7)-(11) explicitly control all partial derivatives through total order two on the expanding square; no interchange of differentiation with a bare pointwise limit is used.

4. **Using different transformations would change the problem.** The same reference n transforms both worlds. Transforming the alternative with m=n+1 would destroy the common Exp(1) normalization used in the proof.

5. **Dependence cannot be discarded in cross tails.** Shared exponential margins do not make U and V independent under P1. The inequality E[U 1_{V>L}]<=(L+1)e^-L follows by integrating min(e^-s,e^-L), and is valid even for complete positive dependence. Multiplying marginal probabilities would be unjustified.

6. **The first-order term does not vanish on a finite box by itself.** For a direct expansion of R log R, its integral is the bulk mass discrepancy. That discrepancy is the negative tail mass discrepancy. The centered nonnegative entropy psi(R)=R log R-R+1 performs the exact global cancellation before truncation.

7. **A fixed truncation does not suffice.** The proof takes L_n=C log n with C>4. This makes n^4 times the entropy tail O(n^(4-C)log n) tend to zero while derivative remainders still vanish. Claiming the result from a fixed numerical truncation or from C=4 under the displayed estimate would leave a gap.

8. **Infinite chi-square does not imply an improved testing exponent.** Here the exact same channel has infinite chi-square and D_n~1/(2n^4). Its remote corner tail can dominate one divergence and be negligible for another.

9. **Exact readout is an upper-information comparison, not a free instrument.** Finite face words are functions of the pair of minima, but no finite word is asserted to recover an arbitrary real pair exactly. Any finite precision, number-of-probes, actuator noise, or retention cost requires separate analysis. The expected-cost inequality counts fresh independent vectors used; repeated probes of one vector are not counted as independent replicas.

10. **Full face-only count identification in the whole unknown-calibration class is false.** For any m>n, take m routes with independent A and B gates, each coordinate having marginal threshold CDF H_(n/m)(a)=1-(1-a)^(n/m). The two coordinate minima are then independent and have exactly the reference-n margins. Thus the entire face-minimum law equals the reference law, although the route count is m. Their fresh interior absence law [1-H_(n/m)(a)H_(n/m)(b)]^m generally differs from (1-ab)^n. The known broader reference test also uses fresh diagonal information; it is not a face-minima-only identification theorem. RESULT.md claims only the hard-pair lower bound and does not infer broad identification or a matching all-class upper bound.

11. **Face-only is essential.** On the same retained vector, interior AB endpoint probes can depend on matching A and B thresholds to routes. That information need not be determined by just the two separate minima. Gate-level labels, route labels, or changed latent states likewise fall outside the kernel/data-processing argument.

12. **Information coefficients are not practical sample constants.** The ratio (1/2)/0.2096995101... compares asymptotic one-replicate KL for the ideal full channel with the best old nonadaptive two-face hard-pair channel. It proves neither an attainable sequential sample ratio nor an optimal physical probe budget or broad wrong-count design.

13. **Termination correctness is unconditional.** The rejection event argument requires high probability of a finite correct decision under both worlds. A guarantee only among terminating paths could hide failure on nontermination and does not imply the stated expected-replicate lower bound.

14. **Diagnostics are bounded.** The quadrature and finite-grid derivative controls are not empirical observations, certified numerical quadrature, global supremum proofs, or a substitute for the analytic argument.
