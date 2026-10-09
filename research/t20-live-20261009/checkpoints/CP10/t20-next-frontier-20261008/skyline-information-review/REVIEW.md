# Independent bounded review: skyline likelihood and count information

2026-10-08 UTC. Prospective mathematical follow-on only, not a new research tranche. No historical-floor certification, GitHub action, protected integration, actual-instrument validation, or T20 closure. Frozen predecessors and source artifacts were not modified. This review concerns the retained endpoint oracle and the specified iid hard pair, not arbitrary dependent or heterogeneous route laws.

## Outcome

The skyline-count-information written proof passes this independent mathematical review. The ordered-stratum likelihood and factorial singular-mass claims also independently derive correctly; source-specific final review of their author's artifact is recorded below when available. Claims about finite-grid implementations are excluded unless separately appended. Deterministic controls pass; they corroborate rather than replace the written derivations. No Lean assurance is claimed here.

## Independent likelihood derivation and support audit

Let N continuously distributed iid pairs have density f and law μ. Write skyline points in increasing x order as z_1,...,z_k, with strictly decreasing y. The event density on this ordered 2k-dimensional antichain domain is

    (N)_k × product_i f(z_i) × μ(U(z))^(N−k),

where U(z) is the union of upper rectangles of the displayed points. There are (N)_k assignments of distinct labeled observations to the ordered visible points. All remaining labeled points must lie in U(z). Conversely that condition leaves exactly those displayed minimal points, except null ties. No k! divisor appears on the ordered domain. For k=N the factor with exponent zero is 1. Neither the lower-rectangle union nor its complement can be substituted for U.

For baseline n versus alternative m=n+1, both f and μ(U) are strictly positive for every interior antichain. Thus every k≤n stratum has mutually positive densities. Alternative k=m is the sole singular stratum modulo null boundary configurations. This is a statement about the full ideal skyline channel, not only a particular finite staircase certificate. The formal likelihood ratio on the shared stratum is

    [m/(m−k)] × product_i f_c(z_i)
       × μ_c(U)^(m−k) / area(U)^(n−k).

For the Joe density, direct differentiation yields

    ∂xy log f_c = (2−c)/(1−xy)^2 − c/(1−cxy)^2 ≥ 0.

The inequality follows because 2−c≥c and 1−xy≤1−cxy. Conditional on the increasing ordered X coordinates and increasing ordered Y coordinates, rank-pairing permutations have probabilities proportional to product_i f_c(x_i,y_pi(i)). Swapping a concordant pair to discordance weakly reduces its product by TP2. Iterating yields the fully reversed permutation as a minimum. All m! permutations have positive weights, so its conditional probability is at most 1/m!. K=m is precisely that reversal. Integrating establishes P1(K=m)≤1/m!. Infinite forward KL therefore does not give a favorable waiting-time rate for detecting this singular event; it does not rule out faster use of common-support information.

## Independent mean derivation and low-n controls

A point z is minimal exactly when the other N−1 points avoid its lower rectangle. Hence

    E K = N ∫ f(z) (1−F(z))^(N−1) dz.

For Joe with mc=n and t=xy, integrating along products gives

    E1 K = n ∫_0^1 (−log t)(1−t)^(n−2)(1−ct) dt.

For n>1, split 1−ct=(1−c)+c(1−t), use the integrals H_(n−1)/(n−1) and H_n/n, and simplify. This gives E1 K=H_n+(H_n−1)/(n²−1). At n=2 this is 5/3, with gap 1/6; neither a zero gap nor the naive H_3 answer is correct. For n=1 direct integration instead gives (1+ζ(2))/2, with gap (ζ(2)−1)/2. The n>1 quotient must not be used literally at n=1. In that case K=1+Bernoulli(gap), so the exact variance is gap times (1−gap), and P1(K=2)=gap<1/2.

## Conditional independence and variance audit

Conditioning on the ordered X values leaves independent Y concomitants with respective conditional laws Y|X=x_i. Sorting merely applies the X-determined label permutation; it does not introduce dependence among these conditional Y variables. TP2 implies increasing conditional likelihood ratio, hence stochastic increase with x. Their quantiles Q_i therefore increase in i. Couple them as Y_i=Q_i(U_i), with independent uniforms U_i independent of ordered X.

If j<i has U_j≤U_i, then Q_j(U_j)≤Q_j(U_i)≤Q_i(U_i). Consequently every strict lower-record event among Y implies the corresponding lower-record event among U, simultaneously. Thus K≤R_m pathwise. This is stronger than a mere mean comparison and does not assert independence of Joe record indicators. The ordinary iid record count has mean H_m and variance V_m=H_m−H_m^(2), by independent insertion ranks.

Taking second moments and subtracting the exact mean square gives

    Var1 K ≤ V_m+H_m²−(H_n+δ_n)²
           ≤ V_m+2H_n/m+1/m² = O(log n).

This subtraction is essential: E K²=O(log² n) alone would not prove the claimed variance scale. The authored proof correctly makes it. E1 K≤H_m follows as an independent consistency check from δ_n≤1/m, including n=1.

## Testing conclusion and limits

The midpoint mean test on s independent ideal retained vectors has each error bounded by 4 max(V_n,W_n)/(s δ_n²). Since δ_n∼log n/n², constant error needs O(n^4/log n) such vectors. Independent constant-error blocks and majority vote give O((n^4/log n) log(1/α)) vectors for 0<α<1/2, with absolute constants after including the finite low-n cases. This is an upper bound for this known simple pair, not an optimal rate, uniform model-class guarantee, finite-probe complexity, or actual instrument result. Independent vector resets are substantive; retaining a single vector indefinitely does not supply independent K samples.

The full endpoint function identifies the Pareto antichain but leaves dominated points invisible. Thus it does not generally reveal total route count. No finite procedure reconstructing arbitrary continuous threshold coordinates exactly is implied. Any separate finite-grid claim needs its own approximation event, total error allocation, query cost, and coordinate selectability assumptions.

## Own controls

controls.py was executed successfully and CONTROL_RESULTS.json records: 45-digit quadrature agreement with exact mean formulas for n=1,2,3,4,10,30,100; nonnegative variance bounds and mean domination; exhaustive 5!=120 permutation-product comparisons at a specified positive grid; and 250 deterministic lower-record implications under ordered conditional quantiles. These are independent implementations, not simulations or exhaustive verification over continuous inputs. They check the exceptional n=1 case separately. Negative comparisons reject zero mean gap at n=2 and an erroneously uniform rank-permutation law.

## Final authored likelihood artifact: additional review

The final retained-skyline-likelihood/RESULT.md was read in full, including claims beyond the initial handoff. No blocking issue was found. Given the skyline and its selected labels, remaining labels really are independent μ conditioned on D: the likelihood factorization establishes this regular conditional law, not positive-probability conditioning on an exact coordinate value. Uniform injections follow label exchangeability. The positive strip integral and its v=(1−t)^c substitution have the correct orientation, integrand and endpoint conventions. The warning that this is not a rigorous quadrature-error certificate is appropriate.

The finite conditional-KL proof also passes. The bounds f_c≥c and D_c≥cD_0, and the routewise finite logarithmic moments under both laws, control the positive logarithms in both KL directions. Normalizing the common-support restriction contributes only a finite constant. The general density-ratio negative-part bound supplies the other half. The k=1 likelihood limits 1 near (0,0), versus 0 as x→1 at fixed interior y, prove nonconstancy on positive-measure sets by continuity. The exponent cn−(n−1)=1/(n+1) is correct, including n=1. This establishes finite strictly positive conditional KL at each fixed n, with no asymptotic-rate conclusion.

The exact n=1 masses match the independently checked mean identity: probability of K=2 is π²/12−1/2, and probability of K=1 is 3/2−π²/12. Strict TP2 correctly strengthens the support bound to <1/m! for this c<1 pair. The countable union of rational staircase certificates equals the full k=m singular event modulo null boundaries; a fixed staircase can be much rarer.

Both authored control programs were independently rerun successfully. Their output is supporting numerical evidence, not generalized proof. The likelihood artifact explicitly reports its finite quadrature error, avoiding a false numerical-normalization claim. SOURCE_BINDINGS.json records hashes of the reviewed final proof files and controls; any subsequent substantive edit requires renewed review. Final scope remains the core likelihood/count results only. No finite-grid implementation artifact was available for this review and none is accepted by this report.

## Comparator revision receipt

The count artifact was subsequently revised only to strengthen its comparison to the already established exact face-minimum experiment. The earlier count RESULT.md hash c2b40ad691a59dc3b2a60eb1171881747a85aa46b0ba3d92222de37f20794827 is superseded by b96715873d240787ea6343538b4df54d94dc4bd7a52b79615fcaa9b2d34c2e4d. SOURCE_BINDINGS.initial.json preserves the initial review bindings.

I read the revised comparison paragraphs, SOURCE_AUDIT.md, and the entire cited full-face-threshold-kl-rate/RESULT.md. The stronger comparison passes the transport/assumption review. The existing predecessor's KL is asymptotic to 1/(2n^4), and its sections 1 and 6 cover exact minima and arbitrary adaptive face-only words, including incomplete words charged from their first observation. Its lower bound uses the same n versus Joe n+1 pair, independent fresh vectors, common policy, fixed α in (0,1/2), and unconditional terminal correctness. The skyline test has deterministic vector cost s, independent fresh observations and unconditional error bounded by α, so its O_α(n^4/log n) cost is genuinely below that predecessor's Ω_α(n^4) bound for the narrower face-only observation channel. No repeated face access is mistakenly treated as an independent vector, and no conditional-on-termination correctness is substituted.

This consumes the established comparator theorem rather than adding a new face-KL proof or extending either oracle to a physical finite-cost readout. The new source audit and comparator source are included in the renewed bindings. Core proofs and controls were unchanged. Finite-grid approximation remains outside this review.
