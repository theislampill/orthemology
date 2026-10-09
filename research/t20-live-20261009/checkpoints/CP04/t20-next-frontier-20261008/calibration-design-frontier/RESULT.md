# Calibration design changes the identification problem

8 October 2026 UTC. Mathematical sibling, with the predecessor directories unchanged. No experiment, physical calibration, route architecture, original-agent discovery, kernel proof, protected integration, owner acceptance, or T20 closure is claimed.

## Main findings

1. For the inherited four-histogram catalogue A, B, OR, AND, **two different calibrated interventions on the same latent inventory identify every mixture**. At ideal corners they reveal the latent catalogue label itself. A one-endpoint-per-inventory experiment cannot identify the mixture, even with arbitrary adaptive calibration choices under the specified history-independent response kernel.
2. Near those corners, support recovery needs only certified conditional endpoint error bounds, not conditional independence between the two endpoints. If each coordinate error is at most eta and every positive weight is at least w, then eta <= w/16 and n >= ceil[(16/w) log(4/delta)] independent groups suffice for exact support with probability at least 1-delta. A latent-label oracle gives a matching order w^-1 log(1/delta) lower bound on the number of groups. Constants are not claimed optimal.
3. This improvement has a precise boundary: all deterministic corners reveal only the minimal-support Boolean response antichain. Multiplicity and absorbed productive routes can remain hidden. A separate appendix proves that identifying an unknown one-root count bounded by K requires order K^2 log(1/delta) endpoint observations even with arbitrary adaptive rates, and a K-dependent fixed rate attains that order. Scalar-code injectivity alone does not provide either guarantee.

The first two results change the allowed instrument and exploit a restricted known catalogue. They are not a replacement for the predecessor's general base4 moment theorem or its H0/H1/H2 sampling example.

## 1. The four labels are inventories, not gate architectures

There are two known root indices A,B and one designated effect. Each listed support is one distinct unguarded route occurrence. The four histograms are:

- H_A: one support {A};
- H_B: one support {B};
- H_OR: one support {A} and one support {B};
- H_AND: one support {A,B}.

Under the inherited independent-route law at survival rates (a,b), their effect probabilities are respectively

f_A=a, f_B=b, f_OR=a+b-ab, f_AND=ab.

Every label uses the same response-law assumptions. These are not competing physical gate implementations. Independent incidence gates and any whole-route mechanism producing the same independent support-product laws remain observationally equivalent here.

The issued profile AB is held fixed. The intervention changes attenuation rates, first to (1,0), then to (0,1), without changing the inventory. A zero attenuation rate does not remove an issued root or reevaluate a guard. The present catalogue has no guards. Calling the two rate vectors different issued profiles would conflate distinct operations.

For every group g, draw a label J_g with fixed probabilities w_j and retain that same label across the two interventions. Write Y_1,Y_2 for effect indicators. At exact corner rates the codewords are

H_A -> 10; H_B -> 01; H_OR -> 11; H_AND -> 00.

Thus the four ordered outcome probabilities equal the four mixture weights after this known permutation. Exact population weights are identified. A finite sample estimates real weights; it does not recover arbitrary real weights exactly.

The corners use zero and one rates, outside the earlier strictly interior prime/base4 calibration. They are an explicitly stronger instrument idealization. The next section covers strictly interior rates sufficiently close to them without assuming exact zero or one calibration.

## 2. Sharp one-versus-two endpoint boundary for this catalogue

The two fixed mixture laws

Pi_0 = (delta_A+delta_B)/2,
Pi_1 = (delta_OR+delta_AND)/2

have disjoint supports yet the same one-trial response at every (a,b), since f_A+f_B=f_OR+f_AND=a+b.

For the adaptive claim, specify the process: at each one-trial group choose a rate vector from the past and independent protocol randomness, then draw a fresh label from the same fixed Pi; conditional on that label, chosen vector, and past, the next endpoint is Bernoulli with the displayed response probability. There is no additional history-dependent emission channel or shared cross-group noise. The rate-selection rule is the same under the two alternatives. At every past transcript their conditional next-endpoint laws coincide, so induction gives equal full transcript laws, including chosen rates. This is a fixed pair of alternatives, not an adversary changing its mixture after seeing the design.

Two crossed endpoints escape this obstruction by preserving the same latent label. If labels are independently resampled between the two endpoints, the ideal rate pair instead yields independent Bernoulli(1/2) endpoints under both Pi_0 and Pi_1. Pairing records after fresh resampling cannot restore the lost information.

For comparison, two conditionally independent repetitions of **one fixed** calibration have only three exchangeable count cells. Their four conditional component-law columns therefore cannot identify all four unrestricted mixture weights: a nonzero null vector sums to zero because every column sums to one, and its positive and negative parts give distinct probability mixtures with equal observations. Three repeats at the inherited base4 rates suffice, since its four scalar codes are distinct. This rank statement concerns one fixed panel. Combining several different retained panels can change the result and is not excluded.

The crossed design requires two endpoints per group and their order. Discarding the order merges 10 and 01 and loses the distinction between H_A and H_B. A same-rate exchangeable count is sufficient in the predecessor; it is not sufficient for this nonexchangeable instrument.

### Exact interior extension under a known product channel

The exact population identification is not confined to boundary rates. Suppose the rates (a,b) then (b,a) are known, a!=b, and the two endpoints are conditionally independent given the persistent label. Put c=a+b-ab and d=ab. In label order A,B,OR,AND their ordered pair laws are products with success-parameter pairs (a,b),(b,a),(c,c),(d,d). The determinant of the matrix with these four label rows and outcome columns 00,01,10,11 is

(a-b)(a+b-2ab)[(a-b)^2+2ab(1-a)(1-b)].

Expansion is an exact polynomial identity, independently verified by the rational polynomial control. For 0<=a,b<=1 and a!=b the last bracket is positive and a+b-2ab=a(1-b)+b(1-a)>0. Thus the full channel is invertible. If a=b the A and B laws coincide. This gives an exact design criterion for the swapped-pair family, including all unequal strictly interior rates.

This paragraph assumes a known conditional product channel; it is not the arbitrary-coupling robustness result below. A small determinant signals no uniform stability guarantee. Near-corner decoding avoids needing an exact joint channel. At any swapped rates the total-success count laws of A and B are equal, because swapping coordinates leaves their sum unchanged. The information-loss counterexample therefore survives strictly interior calibration too.

## 3. Robust decoding without within-group independence

Allow actual first rates (a_1,b_1) with a_1 >= 1-eta and b_1 <= eta, and actual second rates (a_2,b_2) with a_2 <= eta and b_2 >= 1-eta. All rates lie in [0,1]. More generally it suffices that, conditional on each fixed label, each endpoint differs from its intended code bit with probability at most eta.

The inherited marginal response law certifies those bit bounds. At the first intervention, for example:

- H_A's error is 1-a_1 <= eta;
- H_B's error is b_1 <= eta;
- H_OR's error is (1-a_1)(1-b_1) <= eta;
- H_AND's error is a_1 b_1 <= eta.

The second intervention is symmetric. The within-episode response formula still requires its stipulated route law. Accurate root marginals alone cannot certify that formula under arbitrary within-episode route dependence.

Decode every observed ordered pair by the ideal four-code lookup, calling the result Z. Regardless of dependence between Y_1 and Y_2 conditional on the retained inventory,

P(Z != J | J=j) <= beta := min(1,2 eta).

This is a union bound. The stronger 2 eta-eta^2 expression requires an additional independence premise and is deliberately not used. If two bit errors have disjoint conditional supports, their union reaches 2 eta, so arbitrary coupling cannot be silently given the product bound.

Let p_i=P(Z=i). Then

|p_i-w_i| <= beta,
w_i=0 implies p_i <= beta,
w_i>0 implies p_i >= (1-beta) w_i.

The last lower bound is stronger than w_i-beta for a rare true label and is the reason the support proof below has a linear, rather than quadratic, inverse weight-floor cost.

Assume the full groups, including label, actual calibration and endpoint pair, are independent, with the same label weights and the displayed per-label error bound. The groups may have different deterministic calibration errors or different conditional couplings. In that case p_i may vary with g; the same proofs apply to independent nonidentically distributed code indicators and their average means. Shared random drift requires independently justified conditional independence and the same conditional mixture/error promises before conditioning and integrating. A marginal calibration bound does not establish those promises. Arbitrary cross-group dependence is not covered.

For weight estimation, ordinary Hoeffding and a union bound yield simultaneously

|hat_p_i-w_i| <= beta + sqrt[log(8/delta)/(2n)]

with probability at least 1-delta. This is a calibration-aware error radius, not an exact inverse of an unknown joint noise channel.

## 4. Support certificate and a matched group-count order

Take 0<delta<1 and assume every w_i is zero or at least w, where 0<w<=1. If beta<=w/8, classify label i as present exactly when its empirical decoded-code frequency is at least w/2.

For an absent label each group indicator has mean at most w/8. Using exp(lambda X) with lambda=log 2 and 1+u<=exp(u),

P(hat_p_i >= w/2) <= exp[n(w/8-(w/2)log 2)] <= exp(-nw/8),

where log 2 >= 1/2. For a present label every mean is at least (1-beta)w >=7w/8. The standard exponential lower-tail calculation gives

P(hat_p_i < w/2) <= exp[-n(p-w/2)^2/(2p)] <= exp(-9nw/112) <= exp(-nw/16),

where p is the average mean. The expression (p-w/2)^2/p increases for p>w/2. For completeness, the lower-tail bound follows from E exp(-lambda sum X_g) <= exp[-np(1-exp(-lambda))], choosing exp(-lambda)=1-t for t=1-(w/2)/p and using t+(1-t)log(1-t)>=t^2/2. The latter follows by differentiating and using -log(1-t)>=t. No independence between coordinates i is required.

Therefore total support error is at most 4 exp(-nw/16), proving the stated sufficient budget. Since beta<=2eta, eta<=w/16 suffices. The threshold allows ties as present; the absent tail includes equality and the present failure is contained in the bounded lower-tail event.

For w=1/3 and delta=1/20, n=211 independent groups, hence 422 endpoints, suffice when eta<=1/48. This is a theoretical sufficient bound for these four labels. The preceding 40,000-group example used a different multiplicity catalogue and is not a direct comparator. At exact corners, the support is simply the set of labels observed; its failure probability is at most 4 exp(-nw), so the factor 16 is unnecessary there.

Conversely, for 0<w<=1/2 compare delta_A with (1-w)delta_A+w delta_B. Both respect the floor w. Even an oracle showing each true label fails to encounter B with probability (1-w)^n under the second law. The overlap mass of the two n-label distributions is exactly (1-w)^n. Hence their optimal equal-prior error is (1-w)^n/2. Any procedure with both errors at most delta<1/2 must satisfy

n >= log(1/(2delta)) / [-log(1-w)].

As -log(1-w)<=w/(1-w), this is at least ((1-w)/w)log(1/(2delta)). A design whose observations are generated from labels by a parameter-independent stochastic channel, even with adaptive interventions inside or between groups, cannot improve on the full-label oracle. Thus additional endpoints from one inventory do not replace independent opportunities to encounter a rare label. At fixed four-label catalogue the achieved dependence on w and confidence is optimal up to constants in the small-delta regime. This does not claim optimal constants, all-N logarithmic factors, or optimal arbitrary weight estimation.

## 5. A real calibration nonidentifiability example

Unknown calibration is not merely an estimator nuisance. Fix 0<epsilon<=1/2. In world 0 the true label is always H_A, and the actual rates are (1,0) then (epsilon,1). Its code law is 10 with probability 1-epsilon and 11 with probability epsilon. In world 1 the rates are the ideal corners and the mixture is (1-epsilon)H_A+epsilon H_OR. Its code law is exactly the same. Both worlds fit the corner-error promise eta=epsilon; the same fixed world is used for every independent group. They have different supports and every positive weight is at least epsilon.

Thus, for 0<w<=1/2, no number of crossed groups identifies support uniformly when this uncertainty class permits eta>=w. This example uses admitted boundary rates. The sufficient eta<=w/16 regime and this impossibility leave a constant-factor gap; no sharp calibration threshold is claimed. Under a wholly abstract unknown code channel the analogous contamination example works at its code-error radius beta. The physical route-rate example is stated separately rather than assuming every stochastic code channel is physically realizable.

## 6. General code principle and exact corner quotient

For any known finite catalogue with distinct ideal binary codewords of length R, a decoder correct on those codewords and per-coordinate conditional errors epsilon_t has P(wrong label|J)<=sum_t epsilon_t by union bound. Unused words can be assigned arbitrarily; observing the ideal word still guarantees a correct label. The weight-bias and rare-category support argument above generalize, replacing four by catalogue size N and beta by that error sum. Deterministic one-group labelling requires N<=2^R; this elementary bit bound is about a single transcript, not an all-protocol lower bound for mixture estimation with multiple differently designed panels.

For the unguarded route model on a finite known root set, all corners together reveal exactly the inclusion-minimal positive supports present in the histogram. At corner T, the effect occurs iff at least one present route support P is contained in T. Duplicates do not change this statement, and a support containing another present support does not change it. Conversely the inclusion-minimal subsets T with positive corner response are precisely those minimal supports. This proves both directions of the quotient characterization.

In particular one A route, two A routes, and one A route plus one AB route agree at every corner. At a=b=1/2 their effect probabilities are 1/2,3/4,5/8 respectively. This is an exact negative result: corner-code design does not generally recover anonymous multiplicity histograms. Interior information can distinguish those labels, and the appendix quantifies a remaining cost even under arbitrary rate design.

## Verification and remaining scope

The source and predecessor audit is in SOURCE_AUDIT.md. EXACT_CONTROLS.md explains finite rational controls, including extreme within-group couplings, ordered-code loss, fixed-panel rank, adaptive count inequalities, and exact calibration confounding. These are deterministic calculations, not empirical samples or general proofs by enumeration. The separate crossed-code-root-review directory reviews the root's independent derivation; its scope must not be widened to the appendix without a further receipt.

All continuations require stable eligible labels, admissible interventions, a correct response law and adequate calibration. The instrument does not identify route tokens, bearers, underived ownership, or complete actual productive efficacy. No philosophical bridge or physical architecture is validated by the code.
