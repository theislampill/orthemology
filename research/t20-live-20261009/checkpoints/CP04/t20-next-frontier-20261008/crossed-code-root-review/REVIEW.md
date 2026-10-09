# Independent review: crossed-code support certificate

8 October 2026 UTC. Mathematical review only. No physical validation, empirical trial, kernel proof, protected-repository modification, integration, owner acceptance, or T20 closure is asserted.

## Verdict

**Pass for the stated four-label mathematical model, with the scope clarifications adopted during this review.** The two crossed ideal profiles identify all four catalogue weights from the population ordered-pair law. The near-corner certificate correctly recovers support under the declared weight/calibration floors and independent groups, while allowing arbitrary conditional dependence between the two endpoints of each group. The 211-group example, conservative Chernoff constants, rare-label oracle obstruction, and all nine supplied corner-control rows check.

The separate known product-channel interior determinant also checks exactly and is nonzero precisely when the swapped rates differ. This extension has stronger channel assumptions than the coupling-robust support certificate. The separate compression boundary is correct under the product-channel assumptions, and at exact corners needs no within-pair independence.

The reviewed bytes and their SHA-256 values are recorded in `SOURCE_BINDINGS.json`; snapshots are in `frozen/`. No author file was edited by this reviewer. Author revisions during review are reflected in the final snapshots and bindings.

## 1. Model and information retained

Use **success**, rather than the predecessors' no-effect convention. The inherited route law is

`P(success | H,a,b) = 1 - product_over_route_occurrences (1 - product_of_its_root_rates)`.

Thus the four catalogue responses, in order A, B, OR={A,B}, AND={AB}, are

`a, b, a+b-ab, ab`.

Independent route-success events within an episode are part of that law. They are separate from conditional independence of different episodes and from independence of groups. In particular A+AB uses two independent route-success events even though their support names overlap; literal shared-root Boolean absorption would be a different model.

At `(1,0)` followed by `(0,1)`, the codes are `10,01,11,00`. Marginal probabilities zero or one already force deterministic endpoint values, so the full code is deterministic regardless of within-pair coupling. The four conditional code distributions form a permutation matrix. At population level every code probability is exactly its corresponding mixture weight.

The inventory must remain the same across the two probes, and ordered profile-associated outcomes must remain paired. Counts alone collapse A and B to count one. Finite observations estimate arbitrary real weights; they do not provide exact numerical real-weight recovery. With unknown near-corner channel errors, the statement under review is support recovery under a floor, not exact weight inversion.

## 2. Coupling-free near-corner guarantee

For a profile within eta of `(1,0)`, `a>=1-eta` and `b<=eta`. Wrong-bit probabilities are bounded by eta:

- A: `1-a<=eta`;
- B: `b<=eta`;
- OR: `(1-a)(1-b)<=eta`;
- AND: `ab<=eta`.

The other corner is symmetric. Conditional on any fixed latent label, the probability that either bit is wrong is at most `beta=2eta`, by a union bound. This uses **conditional** marginal promises for each label, not merely marginal promises averaged over a mixture. No conditional independence between the two outcomes is needed.

The union bound is genuinely sharp under allowed coupling. For A, let the two success marginals be `1-eta` and `eta`, and choose joint mass `P(11)=eta`. Then `P(10)=1-2eta`. In the certificate's admissible range `eta<=1/16`, this is a valid joint law. General-proof validity comes from the union bound; 2,592 exact Fréchet-endpoint controls test boundary and intermediate rational calibration values without replacing that proof.

## 3. Support threshold and sample constant

The implicit probability-domain assumptions are `0<w<=1`, `0<delta<1`, and `0<=beta<=w/8`. Since weights sum to one and some weight is present, `w<=1` is automatic whenever the model exists.

For absent label i, every observed occurrence of its code is a misclassification, so `p_i<=beta<=w/8`. For a present label,

`p_i >= (1-beta)w_i >= (1-beta)w >= 7w/8`.

The last inequality uses `beta<=w/8<=1/8`. The threshold `hat_p_i>=w/2` lies strictly between the absent and present population bounds. Ties therefore create no gap in the proof: false absence is the strict lower-tail event, bounded by the usual weak lower-tail event; false presence is the weak upper-tail event.

Across independent groups the code-i indicators are independent Bernoulli variables. Conditional dependence between the two endpoints in a group does not alter that fact. For identical group laws with mean p, multiplicative Chernoff gives

`P(hat_p < w/2) <= exp(-n(p-w/2)^2/(2p))`, when `p>w/2`.

For `c=w/2`, `f(p)=(p-c)^2/(2p)` has derivative `(1-c^2/p^2)/2>0` above c. At `p=7w/8`, `f(p)=9w/112>w/16`. For an absent label, independence and exponential Markov at `lambda=log 2` give

`P(hat_p>=w/2) <= exp(n[p-(w/2)log 2]) <= exp(-nw/8)`.

Here the Bernoulli moment generating function is `1+p`, bounded by `exp(p)`, and `log 2>=1/2`. A union bound over four labels yields `4exp(-nw/16)`. The four empirical frequencies need not be independent of each other.

Consequently `ceil((16/w)log(4/delta))` groups suffice. At `w=1/3`, `delta=1/20`, the exact value is 211, or 422 endpoint observations. The independent code proves the rounding with rational Taylor enclosures `exp(210/48)<80<exp(211/48)`, rather than a floating-point comparison. The accompanying constraints are `beta<=1/24`, `eta<=1/48`.

This is a sufficient conservative design bound. It is not a claim that 211 is optimal, that this experiment was performed, or that the older 40,000-group example solves the same catalogue problem.

## 4. Fixed-mixture adaptive one-trial obstruction

The two **fixed** mixture laws `0.5 A+0.5 B` and `0.5 OR+0.5 AND` have equal one-trial success probabilities at every profile, since `a+b=(a+b-ab)+ab`. Under the declared memoryless Bernoulli emission kernel, the conditional distribution of the next outcome given any common history and chosen profile is identical. The next profile, stopping decision, and auxiliary policy randomness therefore have the same transcript law by induction. Randomized policies are included by conditioning on their parameter-independent random seed.

Fresh independent labels alone would not justify that proof if cross-group emissions could share arbitrary hidden randomness. A concrete excluded process at `a=b=1/2` uses one global uniform U, independent of all fresh labels, and gives success thresholds `1/2,1/2,3/4,1/4` for A,B,OR,AND. Every label has the correct unconditional one-trial success probability. Nevertheless the two-group laws in order `11,10,01,00` are respectively

`(1/2,0,0,1/2)` and `(3/8,1/8,1/8,3/8)`.

Thus they can be distinguished. The OR threshold can even be realized with two independent marginal route events of size 1/2 on four equal U intervals: one event uses intervals 1,2 and the other 1,3. Their union has size 3/4. What fails is cross-group memorylessness, not the one-episode route law. The corrected author paragraph explicitly excludes this counterexample.

At exact crossed corners with a held label, the two mixtures instead have disjoint code supports. If labels are freshly and independently redrawn between the two probes, both yield the uniform distribution over four ordered codes. Persistence is the source of the extra information.

## 5. Same-profile rank obstruction and its correct scope

For **one fixed profile** with conditionally independent identical repeats, each label's ordered two-bit distribution has equal 01 and 10 cells. The four-label channel has rank at most three. Since its columns are normalized, a nonzero kernel vector sums to zero and has both signs; small perturbations of an interior weight vector along it give two different valid mixtures with the same observed law. Thus it cannot identify arbitrary four-label weights.

This obstruction does not extend to combining distinct calibration panels. An exact control uses same-profile repeats at `(1/4,1/2)` and `(1/2,1/4)`. The matrix whose rows are normalization, the first panel's first and second success moments, and the second panel's first success moment has determinant `-3/256`. It identifies all four weights when those known panel laws are jointly available. The corrected author text properly retains this possibility.

## 6. Oracle rare-label lower bound

Compare H0=`delta_A` and H1=`(1-w)delta_A+w delta_B`, for `0<w<=1/2`. Both obey the floor. With n independent oracle label draws, their common all-A transcript has H1 probability `q=(1-w)^n`, and total variation is `1-q`. Every binary test has sum of errors at least q; if both errors are at most delta, necessarily `q<=2delta`. This proves exactly the stated lower bound

`n >= log(1/(2delta))/[-log(1-w)]`.

It is nontrivial for `delta<1/2`. A parameter-independent observation channel, even controlled adaptively, cannot improve on being given the labels themselves.

Optional sharpening, not a correction: simultaneous minimax error for this particular pair is exactly `q/(1+q)`. On the common all-A event choose H1 with probability `q/(1+q)`; on every other transcript choose H1. Thus both errors can be at most delta iff `q<=delta/(1-delta)`. At `w=1/3`, `delta=1/20`, the stated looser condition requires at least 6 groups; this sharper two-point condition requires at least 8. Neither establishes optimality of the 211-group sufficient certificate for its full four-label noisy model.

## 7. Corner multiplicity boundary

Independently recomputing the nine supplied JSON rows gives exactly the saved values. The identities are

`P_A=a`, `P_AA=1-(1-a)^2`, `P_(A+AB)=1-(1-a)(1-ab)`,

`P_AA-P_A=a(1-a)`, and `P_(A+AB)-P_A=ab(1-a)`.

They coincide at every deterministic two-root corner. At `(1/2,1/2)` the three responses are `1/2,3/4,5/8`. General deterministic-corner observations recover the monotone Boolean response function, whose construction discards duplicate and absorbed routes. They do not identify arbitrary route histograms. Positive interior information can distinguish these examples under the inherited independent-route law; no universal stability or apparatus controllability conclusion follows.

## 8. Separate interior determinant and compression extension

For swapped profiles `(a,b),(b,a)`, with one persistent label and conditional independence, form the four-by-four joint channel in row order A,B,OR,AND and column order 00,01,10,11. An independent symbolic construction verifies its determinant is

`(a-b)(a+b-2ab)[(a-b)^2+2ab(1-a)(1-b)]`.

For `a,b` in `[0,1]` with `a!=b`, the second factor is `a(1-b)+b(1-a)>0` and the third is at least `(a-b)^2>0`. Thus the channel is invertible. At `a=b`, the A and B rows coincide. All 289 rational pairs on the sixteenth grid agree with the expression, including boundaries, and the symbolic polynomial difference vanishes identically.

The displayed formula is for the known product channel. General inversion only requires a **known full-rank joint channel**; conditional independence is not universally necessary. Conversely, knowing only noisy endpoint marginals does not license this product determinant. A determinant tending to zero near equal rates also prevents treating nonzero determinant as a uniform stability claim.

Under that product channel, the total-count distributions for A and B agree exactly:

`P(count=0,1,2)=((1-a)(1-b),a+b-2ab,ab)`.

Their ordered laws differ whenever `a!=b`. Thus the predecessor's exchangeable count compression cannot be reused after replacing identical conditional rates with these heterogeneous profiles. If arbitrary within-pair coupling is allowed, equal marginals with swapped means do not by themselves force equal count laws away from the corners; the product-channel scope of this formula must remain explicit.

## 9. Evidence and replay

- `independent_controls.py`: 12 finite control families, exact fractions and integer arithmetic only. It imports no author implementation.
- `symbolic_interior_control.py`: independent channel construction and identity check using installed SymPy 1.14.0.
- `results/EXACT_CONTROLS.json` and `results/SYMBOLIC_INTERIOR_CONTROL.json`: final observed passes.
- `HARNESS_NOTE.md`: records one corrected reviewer-harness assertion issue; it was structural-versus-polynomial equality, not a mathematical discrepancy in the author result.
- `SOURCE_BINDINGS.json`: final author/dependency hashes and binding checks.

Replay each Python script from this folder or by absolute path. The finite controls support, but do not replace, the general mathematical arguments above. No random data were generated, no external primary-source access was claimed, and no original-efficacy or identity inference was made.
