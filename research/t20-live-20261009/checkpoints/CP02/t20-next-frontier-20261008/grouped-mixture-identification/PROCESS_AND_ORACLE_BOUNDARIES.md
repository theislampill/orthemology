# What the grouped observation preserves, and what it does not

This file is a companion to `RESULT.md`. All occurrences of `q(H)` retain the preceding stage's finite unguarded independent-route model. Repetition independence is an additional assumption, distinct from route independence within one episode.

## 1. The exact binary grouped tensor and the moment panel

Use `Y=1` for no effect. In coordinate order `(no effect, effect)`, let `v(z)=(z,1−z)`. A length-`R` group sampled from one fixed latent histogram has endpoint law

`T_R = sum_a w_a v(z_a)^(tensor R)`.

For any particular binary word with `t` no-effect coordinates and `R−t` effect coordinates, its probability is

`sum_a w_a z_a^t(1−z_a)^(R−t)`

`= sum_(j=0)^(R−t) (−1)^j binom(R−t,j) m_(t+j)`.

Thus moments through `R` determine every tensor coordinate. Conversely, marginalizing a length-`R` tensor to any `r<=R` coordinates and asking for all no-effect outcomes gives `m_r`. There is exact equivalence between the full binary grouped law at length `R` and the moment panel `m_0,...,m_R`.

The count `S_R=sum_(j=1)^R Y_j` also suffices: exchangeability makes every word with the same count equally likely. Its binomial-mixture law is

`P(S_R=t)=binom(R,t) integral z^t(1−z)^(R−t) dmu(z)`.

Equivalently `m_r=E[(S_R)_r]/(R)_r` for `0<=r<=R`, using falling factorials and the ratio one at `r=0`. Hence a full ordered tensor is not necessary when this exchangeable count distribution is preserved. However, keeping only the single scalar probability of an all-no-effect group of length `R` gives only `m_R`; lower moments do not follow unless they are measured separately or available by marginalization of a richer grouped observation.

The retained information is the distribution of the shared conditional no-effect propensity and, under scalar injection, of the anonymous histograms. The latent grouping label is not observed; the common cause induces higher-order correlations. For example `Cov(Y_1,Y_2)=m_2−m_1^2=Var_mu(z)`. Zero covariance under the declared held-fixed independent-repeat model means a one-node scalar law, but does not test all premises of that model.

## 2. Specific map into the inherited continuation hierarchy

The parent supplied a fresh targeted reading of the inherited H-Continuation text, §§3–5, repository `theislampill/orthemology`, commit `fd0903d99d657c35e32fddcc8864d2a77930cf40`, blob `99d0434aad8b8a841f59eb078e2b70c0b961d226`, received lines 108–292. Local source-return record: `../root-audit-addenda/H_CONTINUATION_108_292.md`. This stage does not claim its general continuation hierarchy or dimension theorem anew.

On a declared finite candidate set `X` of histograms, let the state remain fixed. The no-effect and effect observation instruments act on functions by

`(K_0 f)(H)=q(H)f(H)`, and `(K_1 f)(H)=(1−q(H))f(H)`.

Equivalently their matrices are diagonal with entries `q(H)` and `1−q(H)`, respectively, and `K_0+K_1=I`. In particular

`K_0^j 1=q^j`.

For the branch-probability contract, starting with constants and allowing these two instruments through horizon `h`, the inherited observable hierarchy specializes to

`C_h=span{1,q,...,q^h}`.

One inclusion follows because every instrument multiplies by a degree-one polynomial in `q`; the other follows from the repeated no-effect words. With distinct calibrated codes on `X`, the evaluation matrix is Vandermonde and

`dim C_h=min(h+1,|X|)`.

For **all** probability laws on a fixed known finite `X`, the inherited full-simplex theorem therefore gives `min(h,|X|−1)` necessary and sufficient continuous real summary coordinates for these horizon-`h` expectations. Once `h>=|X|−1`, those moments identify the entire law on that known candidate set.

The unknown-support family with at most `k` components is a different, restricted family. A `2k`-column Vandermonde argument identifies its elements at horizon `2k−1` even when the ambient candidate set has more than `2k` elements. It would be a failed transport to impose the full-simplex dimension lower bound on that sparse family. It would also be a failed transport to treat the single exact histogram code as a continuous scalar encoding of arbitrary real-weight mixtures: linear averaging discards information.

These spaces preserve the stated branch observables. They do not automatically preserve unlisted bearer identity, physical origin, normative entitlement, or source-level willing. The inherited text explicitly requires such semantics to be independently supplied.

## 3. Fresh latent resampling erases the higher moments

If a new histogram is sampled independently from `Pi` before **each repetition**, the group has law

`T_R^fresh = (sum_a w_a v(z_a))^(tensor R) = v(m_1)^(tensor R)`.

The all-no-effect probability is `m_1^R`, not `m_R`. Taking a tensor power after averaging is different from averaging component tensor powers. Every mixture with the same first moment has the same complete law of all such independently resampled endpoint sequences at the fixed calibration. More endpoint trials estimate that common one-trial law more accurately; they do not restore the lost latent-mixture information.

The earlier two-port example is a stronger all-rate, all-profile obstruction. The half-and-half mixture with `q_A=1−x` and `q_B=1−y` has the same one-trial law as the half-and-half mixture with `q_OR=(1−x)(1−y)` and `q_AND=1−xy`, because `q_A+q_B=q_OR+q_AND`. Under fixed-within-group independent repeats, their second moments differ by `xy(1−x)(1−y)`.

At the actual first two base4 port rates `x=1/4`, `y=1/16`, the nodes are `{3/4,15/16}` and `{45/64,63/64}`; their common first moment is `27/32`, their second moments are `369/512` and `2997/4096`, and the gap is `45/4096`. Their within-trial route histograms are permitted finite codes. Fresh resampling gives `(27/32)^2` on both sides. Grouping therefore repairs that demonstrated pair, while the positive `k=2` counterexample in `RESULT.md` proves that second order alone is not a general repair for two-component mixtures.

Independent resampling across groups is compatible with the repair; independent resampling **within** groups destroys it. Other latent transition processes need separate analysis and cannot be silently equated with either extreme.

## 4. Holding a histogram fixed is insufficient without independent repeats

Conditional marginal probabilities alone do not imply products. For example, sample a single Bernoulli variable `B` with parameter `q(H)` conditional on the fixed histogram, then set every repeated endpoint `Y_j=B`. The full grouped law, at every length, is concentrated on the two constant words and depends only on `E[q(H)]`.

Thus the point mass at the one-route histogram with `q=3/4` and the mixture of weights `3/7` at `q=1` and `4/7` at `q=9/16` remain indistinguishable under this dependent-repeat scheme, even while the histogram is genuinely fixed throughout each group. This isolates conditional repetition independence from merely fixed latent state. Likewise, if repetitions use different untracked calibration rates, their no-effect product is not a power of one scalar node.

## 5. Stationary persistence can be certified with an independent marginal reference

This is a transport of the standard squared-difference/Dirichlet-form identity, not a new general persistence theorem.

Let `X,Y` be histograms at consecutive observation times with the same marginal law `Pi`. They need not form a Markov chain and their joint law need not be reversible. Put `Q=q(X)`, `R=q(Y)`, and let `m_2=E[Q^2]=E[R^2]` be independently established from that marginal law.

Assume the two endpoint indicators `U,V`, **conditional on the pair `(X,Y)`**, are independent with conditional means `q(X),q(Y)`. Then the observed double-no-effect probability is

`c=E[UV]=E[QR]`.

Expanding the square and using equal marginals gives

`E[(Q−R)^2]=2(m_2−c)`.

Write `d=m_2−c>=0`. If `d=0`, then `Q=R` almost surely. Provided each state is in the finite unguarded histogram class where scalar injection holds, `X=Y` almost surely. Only the anonymous histogram is preserved: occurrences or bearers can be exchanged while their histogram is unchanged.

For a known finite marginal support of at least two distinct histograms, put

`Delta=min_(a!=b)|q(H_a)−q(H_b)|>0`.

On a histogram change the squared scalar difference is at least `Delta^2`, yielding

`P(X!=Y) <= min(1, 2d/Delta^2)`.

For one marginal histogram, histogram changes have probability zero already. If independently certified enclosures give `d<=epsilon`, the analogous conditional bound uses `2epsilon/Delta^2`; this still needs a justified positive separation and all process premises. A negative exact deficit contradicts at least one premise or the exact data. It is not evidence for stronger preservation.

There is no reversibility requirement. For example the stationary directed three-cycle on codes `1,3/4,9/16`, with uniform marginal, is nonreversible. It has `m_2=481/768`, `c=37/64`, `d=37/768`, and squared-difference mean `37/384`, exactly twice the deficit.

### The independent-marginal requirement is not optional

One cannot infer `m_2` from the very pair experiment whose fixed-inventory property is being tested by first assuming it is fixed. That would set `m_2=c` by the disputed model and make the test circular. The marginal mixture, or at least its second scalar moment, must come from an independently warranted source. Single-trial endpoint means alone give only `m_1` and do not establish `m_2`.

### Dependent endpoint measurements can counterfeit the entire pair law

Let `a=3/4`, `b=9/16`, take uniform marginal on the corresponding one-route and two-route histograms, and let the latent transition swap them with probability one. The histograms change on every step. Their independently known marginal second moment is

`m_2=(a^2+b^2)/2=225/512`.

For the transition `(a,b)`, choose a conditional joint law of `(U,V)` with probabilities, in order `(11,10,01,00)`,

`(225,159,63,65)/512`.

It has conditional marginals `a,b`. For the reverse transition swap the middle two probabilities. Every entry is nonnegative: the chosen joint `225/512` lies in the Fréchet interval `[a+b−1,min(a,b)]=[5/16,9/16]`.

Averaging the transitions produces

`(225,111,111,65)/512`,

exactly the pair law of independent repeats from a fixed uniform mixture on `{a,b}`. The observed joint equals `m_2`, while histogram-change probability is one. This does not contradict the identity's observable conclusion because conditional endpoint independence has failed. Under truly independent swap emissions, `c=ab=27/64`, `d=9/512`, and `Delta=3/16`; the bound becomes equality at one.

### Equal marginal laws cannot be omitted either

As an elementary control, let `Q=1` with probability `27/91` and `Q=9/16` with probability `64/91`, but let `R=3/4` always. Then `E[Q^2]=E[QR]=27/52`, despite `Q!=R` always. Independent endpoints would give a spurious zero deficit if one substituted only the first-time second moment and ignored the different second-time marginal. All nodes are permitted codes. Equal marginal laws are a sufficient simple hypothesis; equality of the two scalar second moments is the exact algebraic premise needed for the square identity.

### No uniform gap over the countable histogram class

Take a fixed finite histogram with code `a>0`, and add one route at a fresh high-index port with support code `E=2^i`. Its code is `b=a(1−4^(−E))`, so `Delta=a4^(−E)` tends to zero. A stationary uniform deterministic swap on these two finite histograms changes every time, but its independent-emission deficit is only `Delta^2/2`.

Hence no fixed positive tolerance on the deficit can certify small histogram-change probability uniformly across unknown finite supports. For genuinely countably supported scalar laws, the infimum separation can be zero within one law. Exact zero still implies equality almost surely by the nonnegative-square argument; approximate zero does not provide a uniform discrete-change bound.

The certificate applies to the observed transition. It does not exclude changes and reversals between observation times, and it does not prove persistence forever unless the corresponding transition conditions are independently warranted throughout. For any fixed finite or countable set of tested transitions, almost-sure equality on each gives almost-sure equality simultaneously by a union bound over null events.

## 6. Exact rational access, real equality, and finite data

The main uniqueness statements quantify over exact moment values. The optional algorithmic statements explicitly require exact zero testing. The following are different contracts:

- Rational mixture weights and explicitly represented exact rational moment replies permit exact elimination, rank and singularity tests, polynomial reconstruction, and scalar histogram decoding.
- A suitable algebraic-number representation can also support exact operations, but no such representation is implied merely by permitting arbitrary real weights.
- General real moments known only by valid Cauchy enclosures do not provide an exact equality test. Empirical frequencies provide still less without additional statistical assumptions and bounds.

Indeed no deterministic finite-stopping exact identification algorithm exists from an arbitrary-valid Cauchy oracle for these fixed-calibration moments, even with known bound `k=1`. Run a proposed halting algorithm on any finite histogram `H`, letting every requested order/precision pair `(r,n)` return the exact rational center `q(H)^r` with allowed error `2^(−n)`. Its finite transcript contains only finitely many orders and positive tolerances. Add a route at a fresh port with sufficiently large code `E`. With `q'=q(H)(1−4^(−E))`,

`|q(H)^r−q'^r| <= r|q(H)−q'| <= r4^(−E)`.

Choose `E` large enough that these differences fit every queried tolerance; order zero is unchanged exactly. The same finite reply transcript is valid for the different histogram. Therefore the algorithm cannot halt correctly on both. The argument also survives finitely many queries to individual grouped-word probabilities, since those are fixed finite polynomials in `q` and hence continuous. It does not concern stronger canonical digit or exact-rational oracles, or arbitrary rate interventions outside the prescribed calibration.

No supplied bound on mixture order or finite rank calculation removes this obstruction. Nor do exact arithmetic controls demonstrate a uniform finite sample size. Nodes can approach one another and mixture weights can approach zero. Group sizes bound which population moments exist in the retained law; the number and precision of sampled groups needed to infer them is a separate problem.

## 7. Failed transports and the remaining ownership boundary

The following extensions are explicitly rejected:

1. Finite histogram scalar injection does not imply injectivity after a single linear averaging step over inventories.
2. A pairwise separation example does not imply that two moments identify all finite mixtures.
3. Grouping without conditional independence does not manufacture power moments.
4. Independent latent resampling within groups yields powers of the mean, not moments of the latent propensity.
5. A bound against at most `k` components is not a certificate against larger competitors; the `2k+1` permitted-code construction witnesses the difference.
6. A zero squared-polynomial moment certifies finite **scalar** support, not finite productive inventories at those nodes. Infinite-route mimics survive every grouped moment when they share a scalar code.
7. Unknown guards can make different histograms share the observed scalar code. For example an all-issued experiment disables any nonempty absence guard. Repeating that same experiment cannot recover what its component law does not see.
8. Zero stationary deficit without independent emissions or independently warranted marginal information is not a persistence certificate; the exact counterfeits above show why.
9. Exact finite identifiability is not stable recovery from arbitrary tolerances, finite frequencies, or a generic computable-real representation.
10. A recovered histogram counts route-support occurrences within the stipulated model. It does not assign underived ownership, establish actual productive reality, prove completeness of the observed output, certify physical control of the countable calibration, or supply the source's original-efficacy bridge.

Mixture component labels, observable tensor coordinates, port indices, individual productive routes, physical bearers, and numerically particular effects are different things. The transport identifies the first of these only up to relabeling and the finite anonymous route histograms only under their declared eligibility assumptions. No additional ontological inference follows from the algebra.
