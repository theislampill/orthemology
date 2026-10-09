# One rational calibration for every finite root signature

8 October 2026. This is a new sibling of the frozen productive-identifiability package. Its earlier design-rank results remain intact. The root-proposed CRT construction was independently implemented, simplified to linear selector exponents, and checked before this report.

## Result

**For any known nonempty finite set of root indices, one fixed vector of rational survival rates can identify every finite nonnegative integer multiplicity of active positive-support routes from one exact no-effect probability.** The response law is the same specified independent, support-dependent route-success law used in the preceding operation. No hidden route label is observed.

The construction assigns a private prime to each possible nonempty positive support. CRT then encodes all those selectors into one rate for each root. The valuation at a support's private prime records only that support's multiplicity. Large numerator factorisation is unnecessary: the decoder knows which primes to test.

This improves the earlier universal incidence-mask upper bound from 2^r−1 calibrations to one. It does not invalidate that earlier design or make a poorly chosen probe identifiable. It also does not reduce the number of issued profiles needed to recover absence guards or the joint-output information needed to recover effect bundling. “One calibration” is not one finite observation or one probability for the entire guarded, multi-effect problem.

## Model and exact theorem

Let R have r>=1 known root indices. For each nonempty P contained in R, n_P is a nonnegative integer counting distinct active productive-route occurrences with positive support P. Under a calibration x=(x_i), each such route succeeds with probability product(x_i for i in P), and distinct route successes are independent. Independent incidence gates are one implementation; the endpoint law does not identify that physical architecture.

For the designated source-neutral effect, the exact no-effect probability is

q(n;x) = product over nonempty P of f_P(x)^n_P,
where f_P(x)=1-product(x_i for i in P).

The theorem constructs x_i in the rational interval (0,1), depending only on the known root signature, such that n maps injectively to q(n;x) on all finite integer multiplicity vectors. It concerns anonymous support counts, not numerical route IDs, arbitrary real intensities, actual source perfections or unknown additional roots.

## Step 1 Select exactly one nonempty support modulo a prime

For each nonempty selected support P, write k=|P| and choose a distinguished member p*. Give root indices the integer exponents

- +1 on P except p*;
- −(k−1) at p*;
- +k outside P.

For a subset S, let a(S) be the sum of these exponents over its members.

If S is contained in P and omits p*, its sum is |S|, so it is zero only for the empty subset. If S is contained in P and includes p*, the sum is |S|-1-(k-1)=|S|-k, so it is zero only for S=P. If S contains any outsider, that outsider contributes at least k, whereas the sole negative term has magnitude k−1; all other terms are nonnegative. The sum is then at least one. Thus only the empty subset and P have zero sum.

This also handles k=1: the selected root has exponent zero, and every outsider has exponent one. The selected singleton is exactly the sole nonempty zero-sum subset.

Every subset sum has absolute value at most r². Choose a distinct prime q_P for every P such that q_P−1>r², and choose a primitive root g_P modulo q_P. Define the nonzero residue for root i by

rho_i(P) = g_P^(a_i(P)) modulo q_P.

Negative powers are interpreted in the nonzero residue group. The product of rho_i(P) over i in S is one if and only if a(S) is divisible by q_P−1. The strict bound on its absolute value makes that equivalent to a(S)=0. Among nonempty S, this happens exactly when S=P.

The ingredients are the ordinary existence of arbitrarily many primes and a primitive root modulo each prime. The executable constructor deterministically checks primality and generator order for its finite test instances.

## Step 2 Put all selectors into one rational rate vector

Let M be the product of all private primes and set D=M+1. For each root i, use CRT to choose the representative b_i modulo M satisfying

b_i = rho_i(P) modulo q_P for every nonempty P.

Choose 0<=b_i<M. Every prescribed residue is nonzero, so b_i cannot be zero. Hence 1<=b_i<M<D. Put x_i=b_i/D; then each rate is strictly between zero and one.

For every private prime, D=1 modulo q_P and gcd(D,q_P)=1. For any nonempty S, the numerator of the unreduced failure factor is

D^|S| - product(b_i for i in S).

It is positive, since every b_i<D. Modulo q_P it is zero exactly when the selected residue product is one, hence exactly when S=P. The denominator has no factor q_P, even after fraction reduction.

Consequently

v_(q_P)(f_S) = 0 if S differs from P,
and e_P = v_(q_P)(f_P) is a known positive integer.

The private-prime valuation matrix is therefore diagonal with nonzero diagonal. The e_P values need not equal one. The six-root executable control includes an e_P>1 case and verifies division by that coefficient.

## Step 3 Decode unknown multiplicities

Valuations turn finite rational products into sums. The exact readout therefore satisfies

v_(q_P)(q(n;x)) = e_P n_P.

Recover n_P by dividing the left side by the known e_P. This proves injectivity and gives an explicit decoder without observing any route ID or factoring the entire readout numerator. The executable decoder rejects negative or nonintegral recovered counts and reconstructs the complete rational probability to reject unrelated extra factors. Those are checks of membership in the declared mathematical response family, not certificates of causal realism.

The result uses integer multiplicities essentially. It is not an injective scalar measurement of arbitrary real-valued support intensities. Nor does an exact rational carry only one bit: its denominator and numerator may encode arbitrarily many bits as multiplicities grow.

## Guards and multiple effects

Keep the same calibration vector at every issued profile S. Absence guards are evaluated on S before attenuation. The recovered support count at that profile is

m_P(S) = sum over N contained in R minus S of n_(P,N), for P contained in S.

The private-prime decoder recovers those aggregates. The earlier guard-transform inverse then recovers every guard-specific count. The implementation checks this composition through four roots.

Every nonempty issued profile is still necessary in the unrestricted guarded class, among protocols using one fixed issued profile per query. For any omitted S0, a route with positive support S0 and absence guard R minus S0 is enabled exactly there. Adding it cannot affect any retained-profile readout, at any attenuation rates. A shared baseline keeps the unattenuated effect present in both compared models. The new calibration makes the previously stated 2^r−1-profile requirement sufficient as well as necessary within this query family.

For multiple created effects, the same private-prime readout applied to joint absence for U recovers the number of routes whose output subset intersects U, separately for each positive support. The earlier hit-transform inverse composes with this decoder. This is a direct consequence of the written transform theorem, not a new multi-effect implementation in this sibling. Required higher-order coordinates remain required when the observer receives only the restricted coordinate oracle. Full paired endpoint observations allow those coordinates to be recomputed.

## Calibration and sampling costs remain real

The construction uses 2^r−1 private primes and potentially large CRT integers. No claim is made that these rates are practical, statistically optimal, easy to calibrate physically, or represented at low precision. The chosen q_P−1>r² bound is convenient and conservative.

The theorem concerns exact population probabilities and exactly known rational rates. A tiny unknown calibration error can invalidate private-prime factorisation. An empirical rational frequency must not be decoded as if it were the exact model probability. Known finite model classes can instead be compared against their predicted panels with a confidence bound.

For a total-route bound K, every readout denominator divides D^(rK), so distinct exact panels have a coordinate separation at least D^(−rK). This supplies a conservative finite-class margin, though it can be extremely small. The predecessor's variance/union-bound argument then applies using that margin and the number of retained coordinates.

Without a route-count bound, uniform finite-sample recovery remains impossible for this fixed calibration. For k versus k+1 routes using a single root of survival rate x, let f=1−x. The two no-effect probabilities are f^k and f^(k+1), separated by x f^k. With n independent informative trials, their total variation distance is at most n x f^k. The equal-prior success bound approaches one-half as k grows for any fixed n. Even two bounded nondegenerate Bernoulli models cannot be discriminated with zero error from finitely many trials.

These statistical limits also show why the single-calibration theorem is not a claim that arbitrary productive ground is cheaply observable.

## Source and ontology boundary

The calibration presupposes known root indices and the externally warranted support-dependent success law. It does not establish independent original beings, genuine productive-route individuation, the completeness of the effect catalogue, or admissibility of changing the original agents' operative efficacy. The source's same-complete-willing or unchanged-productive-conditions requirement may disallow these probes.

The numerical effect identity convention is retained; private primes, gate variables and CRT residues are mathematical instrumentation data, not additional created effects or additional original bearers. A duplicate record of one occurrence does not acquire a second independent success event. The construction cannot cure an incorrect alias interpretation or an incorrect causal model by arithmetic.

No new Arabic source reading is claimed in this sibling. The preceding operation's source limits and distinctions remain in force. Standard modular arithmetic, primitive-root existence, CRT and valuations supply the mathematical ingredients; no global originality or prior-art priority claim is made.

## Verification

Eleven author control groups pass. They check unique integer selectors through six roots, primitive-root residue separation and positive private diagonals through four roots, strict interior rates, all binary support models through three roots, unknown and large multiplicities, guarded recovery through four roots, profile omission, rational-grid membership, decoder membership rejection, and a nonunit private valuation.

The independent reviewer used a separately implemented CRT route and confirmed the construction through larger finite signatures. Its receipts belong to the separate single-calibration-review directory. Verification coverage is not a count of independent discoveries and does not establish the external stochastic or source-faithfulness premises.

The prior d5cdb418 productive-identifiability package is unchanged. This sibling supplies a sharper design theorem and an exact decoder. It grants no final integration or T20 closure.
