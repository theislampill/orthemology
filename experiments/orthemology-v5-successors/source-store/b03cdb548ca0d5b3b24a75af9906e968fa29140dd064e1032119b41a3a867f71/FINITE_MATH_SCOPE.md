# Finite-mathematical scope and replay limits

## Frozen recorded-coordinate statistic

The application fixes the complete exported game/roster/round opportunity population. Each game has equal total opportunity weight, and its members and 48 scheduled rounds have equal weights within that game. For opportunity i in game g, let w_i = 1/(K m_g 48), where K is the number of games and m_g the exported roster size. Agreement rounds remain population coordinates. Set E_i to one exactly when the two reconstructed cue directions disagree, and zero otherwise.

A valid recorded final-state decimal forecast F_i lies in [0,100]. Absence is an empty or whitespace-only field. A present 50 is available and neutral, not absent; malformed nonempty values fail validation. Let L_i be the binary local cue direction. On available responses B_i = (2 L_i − 1)(F_i/50 − 1), and let Y_i equal B_i when available and zero otherwise. An absent response's zero is a zero recorded contribution, not an imputed neutral belief. Stored correctness and reward flags do not determine availability or the statistic.

Put a_i = w_i E_i Y_i. If A_i is +1 for recorded local-left and −1 for recorded global-left, S = sum_i a_i A_i and t = |S|. The retained aggregate also supplies H = sum_i w_i E_i, total absolute coefficient mass sum_i |a_i|, and V = sum_i a_i². The side-specific fields named V in the descriptive JSON denote available weighted mass; the top-level V is the sum of squared coefficients. The two uses must not be confused.

For each side, M is its weighted disagreement mass, V its available weighted disagreement mass, Q its signed response mass, and availability_rate = V/M. The stored identities S = Q_local-left − Q_global-left, H = M_local-left + M_global-left, and S_R = V_local-left − V_global-left are checkable from the aggregate certificate. They do not recover the omitted rows.

## Maintained probability contract

Reference calculations freeze the full recorded response trajectory, including availability and all response-derived ingredients, under a sharp full-trajectory invariance hypothesis. They also require legitimate fixed inputs and an assignment-law condition given the fixed potential-response world. Marginal placement fairness alone is insufficient. The full cue schedule, exported roster and retention are maintained assumptions here, not verified design facts.

In the rectangular full-prefix family, each next sign's conditional probability is between 1/(1+Gamma) and Gamma/(1+Gamma), for every applicable full history. The robust inclusive tail is the supremum of Q{|sum_i a_i A_i| ≥ t} over that family. Gamma is a sensitivity parameter; no finite value has been established as the historical design for the archive. The frozen reporting grid is exactly 1, 11/10, 5/4, 3/2, 2, 3, 5, 10, followed by the unrestricted endpoint.

For rho = (Gamma−1)/(Gamma+1), D = rho sum_i |a_i|, and V > 0, the original closed upper bound is min(1, 2 exp(−max(t−D,0)²/(2V))). The frozen service returns one if t=0 or V=0. It computes an upper bound, not an exact robust probability. The unrestricted full-cube supremum is one at the observed threshold. An upper bound of one alone does not establish a lower bound on the exact robust tail.

The recorded coordinate does not certify rendering or attention. Final-state forecasts need not equal historical scoring snapshots. Archive identity with the final published analysis/deployment remains unresolved. All-game aggregation does not establish a multiplayer- or collective-reward-specific result. Nothing here identifies latent reliance, source exclusion, irrationality, mediation, or an unqualified causal effect.

## Exact exponential enclosure

The copied primary implementation uses only integers and rational numbers. For nonnegative rational x choose k so y=x/2^k ≤ 1/8. Alternating partial sums of sum_n (−y)^n/n! bracket exp(−y). Terms decrease in absolute value, so each odd partial sum is a lower bound and each even partial sum an upper bound. Continue until the rational bracket is narrower than the declared working tolerance.

For M=2^bits, round the lower endpoint down and the upper endpoint up to multiples of 1/M. Both endpoints are nonnegative. Repeated squaring is monotone there: floor(lower_integer²/M) and ceil(upper_integer²/M) give outward bounds at each of k steps. This induction encloses exp(−x). A positive upper integer cannot become zero under upward squaring. The guarantee is an absolute enclosure; relative accuracy at underflow scale is not claimed. Multiplication by two and endpoint-wise capping at one preserve inclusion for the closed bound. An upper decimal display rounds upward.

The independent oracle instead bounds the positive Taylor series for exp(y), encloses the remaining tail geometrically, inverts the endpoints, and squares with outward rounding. It is separately implemented. Synthetic enumeration also checks small finite examples; it is never applied to the actual coefficient array in this package.

## Post-inspection lower certificate and external theorem

The separate lower certificate was chosen after inspection of the frozen aggregate and upper bounds. It does not inherit prospective status from the earlier plan. It evaluates only:

- A: 100 t² < 121 V
- B: 1000000 M² < 3721 V, with M = 1/(K × 48)

The coefficient cap |a_i| ≤ M follows from the fixed weighting and |Y_i| ≤ 1. Under the fair independent-sign reference law, the sum is centered, its variance is V, and its standardized third absolute moment is at most M/sqrt(V). The fair law belongs to each frozen full-prefix family.

The external input is the independent, not necessarily identically distributed, Berry–Esseen bound. Attribution: Ilya Tyurin, *New estimates of the convergence rate in the Lyapunov theorem*, arXiv:0912.0726v1 (2009), Theorem 7, PDF page 6: https://arxiv.org/abs/0912.0726v1. The application weakens its constant to C=1. The sharper-constant proof and its computer-assisted calculations are not reproduced here. Consequently this is a theorem-dependent certificate, not a self-contained proof of that probability result.

The inclusive tail uses F(−z) + 1 − F(z−), with z=t/sqrt(V)>0, so atoms at either threshold are retained. The elementary rational comparison uses pi>3, 1/sqrt(2 pi)<5/12, and exp(−v)≤1−v+v²/2 for v≥0. Integration to 11/10 gives 11021153/12000000 < 23/25, hence Phi(11/10)<53/60. If A and B hold strictly, the fair inclusive tail, and therefore the robust supremum, is strictly greater than 7/30−2(61/1000)=167/1500>1/20. The exact certificate margin above 1/20 is 23/375. Equality in either predicate is failure for this particular sufficient certificate; the constants are not retuned.

This lower bound is not the exact fair-product or robust tail and does not apply to every individual law in a family. At t=0 the inclusive tail is exactly one. Positive observed t with V=0 is inconsistent with the frozen coefficient sum and is rejected. The result establishes nonrejection for this test within its assumptions; it does not establish invariance, equivalence, power, cognitive mechanism, or historical design validity.

## Attribution and proof status

The historical archive/project is https://osf.io/x5hye/; the related publication is https://journals.sagepub.com/doi/10.1177/26339137251372605. These links identify the source family. No author notebook or primary-source text is distributed. The calculation modules and synthetic controls are separately authored implementations; they are not represented as the source authors' code.

The companion retains its own attribution for exact transformation testing and explains the stronger joint-symmetry premise of its block-orbit construction. The finite examples supplement written arguments rather than proving a real assignment mechanism. No classical randomization, concentration, dynamic-programming, or Berry–Esseen result is claimed as new historical authorship. No Lean or other proof-kernel verification is claimed, and no canonical calculus is changed.
