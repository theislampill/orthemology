# Bounded-count recovery with certified arithmetic

This is a different instrument from the fixed rational prime probes. It uses a known valid route-count bound K>=1 to avoid saturated endpoint probabilities. All results remain conditional on the declared finite direct-route response law and admissible observations.

## Model and mask instrument

There are r>=1 known root indices and m>=1 known effect indices. A finite histogram n(P,N,T) counts distinct productive routes, with nonempty positive root support P, disjoint absence guard N, and nonempty effect-output subset T. Its total count is at most K. A bound on every relevant enabled-route count would suffice for the elementary estimates; the theorem uses the simpler global bound.

At each nonempty issued profile S, choose a nonempty attenuation mask V contained in S. Issued roots and guards remain fixed. Set each incidence survival probability to

p=1/(2K) on V, and zero outside V.

A route's success probability is the product of its incidence probabilities, and different route successes are independent. Equivalent whole-route mechanisms with these same independent support-dependent success probabilities are allowed by the mathematical observation law. Physical actuator separability, statistical independence, and metaphysical absence of foreign receipt are distinct claims; none follows from another.

For nonempty effect query U, observe the indicator that no member of U occurs. Its ideal mean q_(S,V)(U) is a product of route-failure probabilities. Grouping by positive support gives

log q_(S,V)(U) = sum over nonempty P subset of V of h_P(S,U) log(1-p^|P|),

where h_P(S,U) is the integer number of enabled routes with support P whose outputs intersect U.

The count h_P(S,U) is at most K. All original-root indices here are model indices, not a theorem that the indexed entities are necessary originals.

## A lower probability floor

Each relevant route succeeds with probability at most p. A union bound over at most K routes therefore gives q>=1-Kp=1/2. This floor alone does not require independence across routes. The logarithmic product formula and inverse do require the stipulated factorisation. A correlated model can satisfy the floor while violating the inverse's premises.

## Statistical error and integer rounding

Set

epsilon = p^r/(16·2^r).

Suppose every empirical absence estimate qhat differs from its ideal q by at most epsilon. Since epsilon<=1/64, qhat>=1/4. The derivative of log on the interval joining q and qhat has magnitude at most four, so

|log qhat - log q| <=4 epsilon.

For fixed S,U, apply Boolean-lattice inversion to the mask values. At positive support P the exact-real empirical estimate is

hhat_P = [sum over V subset of P of (-1)^(|P|-|V|) log qhat_V] / log(1-p^|P|),

with qhat_empty=1 exactly. The numerator error is at most 4·2^|P| epsilon. Because -log(1-z)>=z for 0<z<1,

|log(1-p^|P|)| >= p^|P| >=p^r.

Thus |hhat_P-h_P|<=4·2^r epsilon/p^r=1/4. Each hit/support count has a unique nearest integer. For smaller issued profiles the same global epsilon is conservative: the numerator has fewer terms and the denominator has magnitude at least p^|S|.

After rounding these counts, apply the existing exact guard and effect-hit inverses. There is no subsequent propagation of continuous error through those inverses: their inputs are already the exact integer aggregates on the good event. This recovers the full anonymous histogram.

## A finite precision certificate

The implementation does not use floating logarithms for its certificates. For any positive rational z, set t=(z-1)/(z+1). Then

log z = 2 sum from j=0 to infinity of t^(2j+1)/(2j+1).

After n terms, the remainder has the sign of t and absolute value at most

B_n(t)=2 |t|^(2n+1)/[(2n+1)(1-t²)].

This follows by replacing every denominator in the tail by its first denominator and summing a geometric series. The resulting endpoints are exact rationals and contain the mathematical logarithm. Integer inputs are converted exactly; floating inputs are rejected rather than silently called certified.

On the good event qhat>=1/4 and qhat<=1, so |t|<=3/5. The model denominator argument 1-p^|P| lies in [1/2,1). A common interval-width upper bound is therefore

B_n <= (25/8)(3/5)^(2n+1)/(2n+1).

Let s=p^r and choose n so that B_n<=s²/(64·2^r). The code doubles n until this exact rational inequality holds. Geometric convergence proves a finite such n for every finite r,K. An optional smaller external arithmetic cap causes an explicit uncertified return; it is not promoted to an all-K termination guarantee.

To bound division error, write the exact empirical numerator as a and its exact denominator as w. Each input-log interval has width at most B. The numerator interval has width at most 2^r B and contains a. Also |a|<2^(r+1), because each empirical logarithm has magnitude at most log4<2. The denominator interval has width at most B, contains w, and |w|>=s. Since B<=s/2, every denominator point has magnitude at least s/2 and stays negative.

For any resulting quotient endpoint, its distance from a/w is at most

2·2^r B/s + 2·2^(r+1)B/s²
<=5·2^r B/s²
<=5/64,

using s<=1/2. The interval therefore lies wholly within h_P ± (1/4+5/64)=h_P ±21/64. That is strictly inside the correct integer's rounding cell. The entire interval, not a floating midpoint, certifies the rounding operation.

This certificate concerns the exact log inversion of the empirical panel. It does not by itself establish that the panel came from the model or that the statistical good event occurred. Those are the premises carrying the truth and confidence conclusion.

## Finite-sample confidence and cost

Let L be the number of retained absence coordinates. With n independent trials at each actuator setting and the same conditional law across those trials, each coordinate is an average of Bernoulli indicators. For any tolerance tau,

Pr(|qhat-q_actual|>=tau) <=2 exp(-2n tau²).

For completeness, the Bernoulli bound follows directly. If Y has mean u, the log moment-generating function of Y-u has value and first derivative zero at zero, and second derivative v(1-v)<=1/4 for a tilted Bernoulli mean v. Integrating gives log E exp(t(Y-u))<=t²/8. Independent trials, the exponential Markov inequality and t=4tau give the one-sided bound exp(-2n tau²); the other sign gives the two-sided bound. No independence among different effect-query coordinates within one trial is needed.

A union bound gives a good-event probability at least 1-delta whenever

n >= ceil[log(2L/delta)/(2 tau²)], with 0<delta<1.

Under exact calibration take tau=epsilon. The coefficient is

1/(2epsilon²)=128·(16K²)^r.

Thus the sample budget is polynomial in K for fixed r and a fixed observation menu. It is not a polynomial bound jointly in all dimensions, and its constants are conservative.

For the full guarded, multi-effect panel there are G=3^r-2^r distinct issued-profile/mask settings. Each provides 2^m-1 query indicators from one paired endpoint observation, so L=G(2^m-1). Total trials are Gn, not Ln. For a single full issued profile without guard recovery, G=2^r-1. The code computes a safe integer ceiling using a rational upper bound for log(2L/delta), with range reduction; it does not round a floating budget downward.

The K-dependent calibration changes the instrument as K changes. Consequently this polynomial bound does not contradict the earlier impossibility of uniform finite-sample identification over unbounded counts at one fixed nonzero calibration.

## A separately warranted calibration-error budget

Suppose the actual gate probabilities differ from their ideal values by at most eta per incidence, including intended-zero mask positions, and actual gates have the assumed product law. Couple each actual Bernoulli gate to its ideal counterpart. A given gate differs with probability at most eta. There are at most Kr relevant incidences, so a union bound gives endpoint-distribution total variation, and hence every event-probability bias, at most Kr eta.

Allocate sampling error epsilon/2 and choose

eta <= epsilon/(2Kr).

Sampling plus calibration bias then stays within epsilon. The sample budget becomes

n >= ceil[2 log(2L/delta)/epsilon²],

four times the exact-calibration coefficient, namely 512·(16K²)^r. Numerical interval error has its own separate 5/64 count-space allowance.

A marginal calibration bound does not control unknown correlations. Two gates can have exactly the same individual success probabilities yet be perfectly correlated instead of independent, changing the endpoint law. The implementation includes this separating control. More generally, an independently warranted bound beta on total variation between the actual full joint gate law and the ideal law directly bounds every event-probability bias by beta. Such a beta is not inferred from the same endpoint observations used in the inverse.

The valid K, calibrated probabilities or TV bound, trial assumptions, correct aliasing, declared effect catalogue and source admissibility all remain external obligations.

## Matching restricted-family lower bound

The independent reviewer proves a complementary result in `../noise-aware-review/RESTRICTED_MASK_LOWER_BOUND.md`. For K>=2 and the fixed p=1/(2K) mask family, even adaptive choice of masks with a fixed total trial budget requires

N >= (2K)^(2r)/45

to achieve identification probability at least 2/3 uniformly over the K-bounded class. A K-1 singleton-route baseline versus that baseline plus one full-support route differs only at the full mask. A per-trial relative-entropy bound, the adaptive chain rule and the testing inequality give the result. When K>=r+1, the baseline can include every root without changing the bound.

The lower-bound proof was read and its scope checked here; its independent executable checks are retained with that separate note. Together, the upper and lower bounds match the exponent of K for this particular fixed-p mask family, at fixed r and confidence. They do not establish optimal constants, optimal confidence dependence or a lower bound against arbitrary rates, other observations, narrower classes or expected stopping-time protocols.
