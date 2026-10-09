# What grouped count mixtures identify without a known calibration

8 October 2026 UTC. This sibling synthesizes the frozen grouped-moment and global-calibration stages. It does not change either. Its conclusions concern mathematical population laws in the declared one-root count model, not empirical certification, numerical route identity, physical original agents, protected integration or T20 closure.

## Result in brief

At one genuinely interior survival setting, held-count grouped observations identify the mixture's sorted weights, zero-count mass, and **primitive positive integer count vector**. Two compatible positive count supports differ by one common positive rational rescaling; equivalently each is an integer dilation of that same primitive vector. Their direct rescaling need not be an integer.

An independently warranted gcd-one prior removes the dilation. A known maximum M generally does not: without a calibration-error restriction, exactly d=1,...,floor(M/max(v)) remain, where v is the identified primitive vector. A known calibration band can remove additional scales by an exact criterion below.

These are population-identifiability statements. The finite-horizon version needs a component bound on both competing laws. It does not turn approximate moments into exact logarithmic ratios or supply a uniform finite-sample recovery theorem.

## 1. Observation model

A world has a probability law on finitely many distinct nonnegative integer route counts. Every supported count has positive weight; multiple records of the same count are combined. The count is the number of independent copies of the same one-root route, under the inherited conditional response law.

At a nominal command x0, let the actual survival probability be t=1-r(x0), and assume **0<t<1**. Its value is unknown. At the start of a group, draw one count J from the mixture and retain that same J for every repetition in that group. Conditional on J, the repeated no-hit indicators are independent Bernoulli variables with parameter t^J. For count zero the no-hit probability is identically one by the empty-inventory model, including at endpoint commands.

The actual calibration r is **common to every latent count component**. Equal nominal commands do not establish this premise. Allowing a separate hidden r_j for each count would replace the common powers t^j by unrelated bases t_j^j and invalidate the count-ratio theorem, even if each count persists within its group.

Thus the all-no-hit moments are

m_h=E[t^(hJ)], h>=0,

and the full length-R grouped law is a mixture of Bernoulli product laws, whose count law is a binomial mixture, with scalar mixing measure

mu = sum_j w_j delta_(t^j).

The inherited theorem makes the full ordered grouped law, its exchangeable count law and moments m_0,...,m_R equivalent for this one fixed calibration. Between-group independence is not needed to define these population laws, but is an additional premise for independent-group empirical estimation. Retaining J does not by itself establish conditional repetition independence.

The count model uses independently successful route occurrences with the same numerical rate. Reusing one perfectly shared random root gate across every occurrence would collapse duplicate routes and change the response law. No gate architecture is identified by the mathematics.

## 2. Exact equivalence theorem

Consider two such worlds (Pi,t) and (Pi',s), with 0<t,s<1. Their full grouped laws agree at every finite length if and only if their scalar mixing measures agree. For the forward implication it is enough that their laws agree through length R>=2C-1 when **each** mixture has at most C supported counts. Indeed their combined scalar support has at most 2C nodes, so the inherited finite-atomic interpolation theorem applies. Conversely equality of scalar measures gives every grouped law directly.

If only one competitor has a known finite support bound, the 2C-1 argument is not sufficient against arbitrarily larger competitors. The inherited positive-moment support certificate through degree 2s can instead certify an s-atom scalar law against arbitrary positive scalar laws, under its exact-population premises. This is a separate stronger observation requirement.

Because t^j strictly decreases in j, there are no within-world collisions. The scalar atom at one is present exactly when count zero is present, and its mass is w0. All positive-count scalar atoms lie strictly between zero and one. Sorted atom matching therefore identifies zero-count mass and the weight attached to each increasing positive count rank.

If the only count is zero, the law is delta_0, every grouped endpoint is no-hit, and calibration is wholly undetermined. There is no positive count vector or gcd to recover. This degenerate case is excluded from the following dilation statement.

The excluded calibration endpoints have different losses. At t=1, the scalar law is delta_1 for every count distribution, so even zero-count mass is hidden. At t=0, the scalar law is w0 delta_1+(1-w0)delta_0: count zero still always has no hit, and every positive count always has a hit. Thus only zero-count mass survives. These formulas use the empty-inventory convention directly rather than an undefined 0^0 expression.

Let the increasing positive supports be j_1<...<j_h and ell_1<...<ell_h. Equality of scalar laws gives matched positive weights and

t^(j_i)=s^(ell_i) for every i.

Taking real logarithms, which are nonzero because t,s are interior, yields

ell_i/j_i = log(t)/log(s) = c>0

for every i. Since the counts are positive integers, c is a positive rational number. Put d=gcd(j_1,...,j_h) and v_i=j_i/d. Then v is an increasing positive integer vector with gcd one. Every ell_i=c d v_i is an integer. A Bezout combination of the v_i equals one, so c d is itself an integer, say e. Consequently

j_i=d v_i, ell_i=e v_i,
gcd(ell_1,...,ell_h)=e,
t^d=s^e=:b in (0,1).

This proves uniqueness of the primitive vector v. It also proves that the invariant information is the pair (v, matched weights), together with w0 and the primitive scalar base b. The unknown absolute scale is d; the actual survival is t=b^(1/d).

Conversely, choose any increasing primitive positive integer vector v, matched positive weights and optional common zero mass, a base b in (0,1), and any positive integers d,e. The two worlds with count supports d v and e v and survivals b^(1/d) and b^(1/e) have identical scalar atoms b^(v_i) and therefore identical grouped laws at every length.

For example, supports {2,4} and {3,6} are equivalent at t=1/8 and s=1/4 with the same ranked weights: both produce scalar atoms 1/64 and 1/4096. Their direct scale is 3/2, while each support is an integer dilation of {1,2}. The theorem is not a statement that every direct scale is an integer.

## 3. What different priors do

### An independently warranted primitive-support prior

If every admissible world is required to have gcd one among its positive supported counts, then d=e=1. The absolute positive counts and weights are identified, and the actual survival at x0 is the identified base b. The prior is doing real work: data compatible with v are also compatible with 2v,3v,... under transformed calibration. One cannot infer the gcd-one premise by selecting the smallest compatible counts.

For a mixture with a single positive count, the primitive vector is (1); there are no nontrivial relative count ratios. A gcd-one promise in that case forces that count to be one. It is not an empirical discovery of a unit route.

### A known maximum only

Suppose all counts are known to lie in 0,...,M and there is positive-count mass. Set V=max(v) and D=floor(M/V). Under otherwise unrestricted unknown interior calibration, exactly the scales

d=1,...,D

are possible. Necessity follows from dV<=M; sufficiency follows by taking t_d=b^(1/d). Any prescribed interior actual value at an interior nominal command can be extended to a static continuous strictly increasing endpoint-preserving calibration map, so global monotonicity by itself removes none of these pointwise candidates.

Thus D=1 identifies absolute counts without a gcd prior. If D>=2, the upper bound alone leaves genuine alternatives. A different promise that the supported maximum is **exactly** M would force d=M/V when this is an integer; an upper bound does not assert that its endpoint is attained.

### A known command-error band

If the static calibration also obeys sup_x |r(x)-x|<=eta, unrestricted d=1,...,D is no longer the correct candidate set. At the measured command x0, scale d is feasible exactly when

|1-b^(1/d)-x0| <= eta.

Necessity is the pointwise error promise. For sufficiency, interpolate linearly through (0,0), (x0,1-b^(1/d)), and (1,1). This is a continuous strictly increasing endpoint-preserving map, and its difference from the identity is linear on each segment with maximum absolute value at the middle knot. Its uniform error is therefore exactly the displayed point error.

Equivalently, with A=max(0,1-x0-eta) and B=min(1,1-x0+eta), admissibility is the root-free test A^d<=b<=B^d. If b,x0,eta are exact rationals, all of these finite candidate tests use exact rational comparisons. This does not recover such exact inputs from empirical frequencies.

## 4. All commands and the remaining calibration equivalence

Suppose two integer dilations d v and e v have the same weights. Let t(x)=1-r_d(x). Defining

s(x)=t(x)^(d/e), r_e(x)=1-s(x)

gives s(x)^(e v_i)=t(x)^(d v_i) at every command. Nondecreasing endpoint-preserving calibrations remain in that unrestricted class; continuity or strict monotonicity is preserved when present. A specified error band need not be preserved and must be checked separately.

The componentwise endpoint kernels agree, not merely their averages. Couple the latent rank selected for each group and the protocol's randomness, then generate each fresh conditional endpoint with the same uniform random number. This gives identical transcripts even when commands change adaptively within a group, provided its latent count rank persists. Across groups, use the same rank draws under the matched weights. Extra command variation cannot break an admissible common-power reparameterization.

Conversely, equality of sufficiently informative grouped laws at one interior command already forces the single common rational scale and matched weights proved above. If entire command-indexed grouped laws also agree, the corresponding power relation must hold at every command, with the endpoint cases interpreted by continuity of the nonnegative power functions or directly from the endpoint laws. The known zero mass and nonzero positive mass distinguish survival endpoints even when positive atoms merge there.

A qualification is essential: a merely nondecreasing endpoint-preserving map need not offer any interior survival setting. The map r(x)=0 for x<1/2 and r(x)=1 for x>=1/2 has uniform identity error 1/2. Every positive count gives the same deterministic command response, so even all commands and all group lengths lose all positive count ratios. A genuine interior command is an explicit premise; strict monotonicity guarantees it for interior commands, and eta<1/2 guarantees it at x0=1/2.

## 5. Retained countermodels

### Too short a group can lose the claimed invariants

At t=3/4, let

Pi = (27/175) delta_1 + (148/175) delta_3,
Pi' = (111/175) delta_2 + (64/175) delta_4.

These are the inherited two-component interpolation counterexample with every count increased by one. Their grouped moments agree through order two but differ at order three. Their primitive positive supports are {1,3} and {1,2}, and their ranked weights differ. Thus the full length-two grouped laws do not identify these invariants, even though both worlds have interior calibration and two components. The 2C-1 sufficient horizon is consequential, not a cosmetic premise.

### Fresh resampling erases more under unknown calibration

Use identity calibration, t=1-x, and a half-mixture on counts {1,2}, independently resampling the count before every endpoint. Its one-trial no-hit mean is F(t)=(t+t^2)/2. A pure count-one world with survival s(x)=F(1-x) has the same conditional one-trial response at every command. Its actual-rate function is continuous, strictly increasing and endpoint-preserving, with

r'(x)-x = t(1-t)/2, hence sup_x |r'(x)-x|=1/8.

Fresh conditional draws therefore give equal adaptive transcript laws under these two fixed worlds. The number of positive components, primitive support and individual weights are not identified.

Under true held-count independent repeats at one interior t, however, the half-mixture has a two-repeat all-no-hit probability (t^2+t^4)/2, while the pure world has [(t+t^2)/2]^2. Their difference is (t-t^2)^2/4>0. Persistence supplies an actual discriminating observable.

More generally, any finite fresh count mixture with zero mass w0<1 and generating polynomial F(t)=w0+sum_(j>0) w_j t^j can be matched by the two-count mixture w0 delta_0+(1-w0)delta_1 using survival [F(t)-w0]/(1-w0). This transformation preserves monotone endpoints. Zero mass survives an endpoint query, but the distribution among positive counts need not survive fresh resampling with unrestricted calibration.

### Label-dependent calibration defeats ratios despite persistence

Let the original support be {1,2}, with any fixed positive ranked weights and a common survival t(x)=1-x. An alternative support {1,3} has identical component endpoint curves if the count-one component uses survival t(x) while its count-three component uses t(x)^(2/3). Both component-specific maps are static, continuous, strictly monotone and endpoint-preserving. The held-group laws then agree at every command and every length, although the primitive supports differ. At t=1/8 all relevant numbers are rational: the alternative component survivals are 1/8 and 1/4, and both worlds' scalar atoms are 1/8 and 1/64. What failed is common calibration across components, not inventory persistence.

## 6. Mathematical recovery is not an approximate-data algorithm

The ratio expression log(q_i)/log(q_j)=v_i/v_j is an identity between exact population atoms. It is not a procedure for deciding rational ratios or exact equality from Cauchy approximations. Nor does an empirical near-zero Hankel determinant certify an exact support bound.

There is a direct obstruction even with two components, equal weights and a gcd-one promise when counts are unbounded. Compare counts {1,2} at survival t with counts {n,2n+1} at survival t^(1/n), for fixed 0<t<1. Both positive supports have gcd one, but the scalar nodes of the second law are t and t^(2+1/n), approaching t and t^2. Every finite collection of grouped moment or word-probability queries at that command with positive error tolerances can therefore have the same valid replies in these distinct primitive models, once n is large enough. An algorithm that halts on the first model after only such queries must then give the same answer on a sufficiently close second model. Exact primitive recovery is not a generally halting operation from this approximation oracle. The competitor count bound remains two; the absolute count bound is deliberately absent in this example. A separate rare-component obstruction can persist at a fixed count ceiling when no positive-weight floor is promised.

A narrow constructive contract is available if the identified positive-count scalar atoms q_i, all in (0,1), are explicitly represented rational numbers; first remove the zero-count atom at one if present. Choose a prime p dividing the denominator of one reduced q_i, compute its integer valuations a_i=v_p(q_i), and put g=gcd(|a_1|,...,|a_h|). Under the promised common-power model all a_i have the same nonzero sign and |a_i|/g=v_i. Indeed q_i=b^(v_i), and a Bezout combination of v makes b a rational product of the q_i, so a_i=v_i v_p(b). Conversely, after constructing v, a Bezout vector c with sum c_i v_i=1 gives b=product q_i^(c_i); verifying b in (0,1) and q_i=b^(v_i) checks membership in this rational common-power family. The decoder also requires distinct atoms sorted decreasingly, an increasing positive integer v with gcd one, and the nonzero common valuation sign; malformed inputs are rejected. Terminating integer factor/valuation and gcd arithmetic suffice; no efficient bit-complexity claim is made.

This rational-atom contract is stronger than an approximate-observation contract. Obtaining those atoms from moments still requires the inherited exact input/oracle conditions. Arbitrary real calibration and weights need not produce rational atoms or moments. If M is known, finite candidate testing can instead use an explicitly supplied exact real-equality facility, but ordinary approximations do not supply one.

No uniform finite-sample guarantee is proved. Weights may approach zero, and an interior t may approach one so distinct count atoms become arbitrarily close. For fixed finite groups these laws can approach the all-no-hit law. Positive weights, finite support and mere strict interiority provide no uniform separation or sample budget. Calibration-error bands, weight floors and dependence controls would need their own statistical theorem.

The invariant counts remain anonymous route multiplicities in a stipulated model. Common scalar ranks do not identify individual routes, physical bearers, underived ownership or actual source perfections. No metaphysical or empirical validity follows from the quotient calculation.
